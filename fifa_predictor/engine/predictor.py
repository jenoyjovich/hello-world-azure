"""
Statistical prediction engine for the 2026 FIFA World Cup.

This module is pure Python (no external deps) so it can run anywhere. It turns
the team/player data into:
  * a single team "power rating" that folds in form, squad quality, depth,
    experience, pressure handling, and current injuries,
  * head-to-head match probabilities (Poisson-based scoreline model),
  * injury-impact simulations ("what happens without player X"),
  * penalty-shootout odds for knockout scenarios.

The AI narration layer (agent.py) sits on top of these numbers.
"""

import math
from typing import List, Optional, Tuple

from ..models import Team, Player, InjuryImpact, MatchPrediction


# Weights for the composite team power rating. Tunable.
_W = {
    "squad_quality": 0.30,
    "form": 0.20,
    "attack": 0.12,
    "defense": 0.12,
    "depth": 0.08,
    "experience": 0.08,
    "pressure": 0.10,
}


def _form_score(team: Team) -> float:
    """0-100 score from recent results and goal difference."""
    s = team.stats
    win_component = s.win_rate * 70.0
    gd = max(-2.0, min(2.0, s.goal_difference_per_game))
    gd_component = (gd + 2.0) / 4.0 * 30.0
    return win_component + gd_component


def _attack_score(team: Team) -> float:
    s = team.stats
    # xg_for typically 0.5-2.5 -> scale to 0-100
    xg = max(0.0, min(2.5, s.xg_for)) / 2.5 * 70.0
    sot = max(0.0, min(8.0, s.avg_shots_on_target)) / 8.0 * 30.0
    return xg + sot


def _defense_score(team: Team) -> float:
    s = team.stats
    # lower xg_against is better; 0.5 great, 1.6 poor
    xga = max(0.0, min(1.8, s.xg_against))
    xga_component = (1.8 - xga) / 1.8 * 70.0
    cs_rate = s.clean_sheets / s.games_played if s.games_played else 0
    return xga_component + cs_rate * 30.0


def team_power_rating(team: Team) -> float:
    """
    Composite 0-100 rating accounting for CURRENT injuries (avg_squad_rating
    only counts available players, and key-player absences are penalised
    separately below).
    """
    squad_quality = team.avg_squad_rating  # already ~75-92 scale
    form = _form_score(team)
    attack = _attack_score(team)
    defense = _defense_score(team)
    depth = team.squad_depth_index * 10.0
    experience = team.tournament_experience * 10.0
    pressure = team.pressure_handling * 10.0

    rating = (
        _W["squad_quality"] * squad_quality +
        _W["form"] * form +
        _W["attack"] * attack +
        _W["defense"] * defense +
        _W["depth"] * depth +
        _W["experience"] * experience +
        _W["pressure"] * pressure
    )

    # Penalise for unavailable key players (sum of contribution scores lost,
    # scaled by how irreplaceable they are via squad depth).
    depth_factor = 1.0 - (team.squad_depth_index / 12.0)  # deeper squad = smaller hit
    for p in team.squad:
        if not p.is_available():
            lost = p.contribution_score * (1.0 - p.availability_factor())
            rating -= lost * 40.0 * depth_factor

    # Host advantage bump.
    if team.is_host:
        rating += 2.5

    return max(0.0, rating)


def _expected_goals(attacker: Team, defender: Team) -> float:
    """Expected goals for `attacker` against `defender`."""
    base_attack = attacker.stats.xg_for
    base_defense = defender.stats.xg_against
    league_avg = 1.35

    # Combine attacker strength and defender weakness multiplicatively.
    xg = base_attack * (base_defense / league_avg)

    # Adjust by power-rating gap (a stronger overall side finishes/creates more).
    gap = (team_power_rating(attacker) - team_power_rating(defender)) / 100.0
    xg *= (1.0 + gap * 0.6)

    # Injury drag on attack: lose key attackers -> fewer goals.
    attack_health = _attacking_health(attacker)
    xg *= attack_health

    return max(0.15, xg)


def _attacking_health(team: Team) -> float:
    """Fraction of attacking output available given injuries (0.5-1.0)."""
    attackers = [p for p in team.squad
                 if p.position in ("ST", "RW", "LW", "CAM")]
    if not attackers:
        return 1.0
    total = sum(p.contribution_score for p in attackers)
    available = sum(p.contribution_score * p.availability_factor()
                    for p in attackers)
    if total == 0:
        return 1.0
    ratio = available / total
    return 0.5 + 0.5 * ratio


def _poisson_pmf(k: int, lam: float) -> float:
    return (lam ** k) * math.exp(-lam) / math.factorial(k)


def predict_match(team_a: Team, team_b: Team,
                  knockout: bool = False,
                  max_goals: int = 8) -> MatchPrediction:
    """
    Poisson scoreline model. Returns win/draw/loss probabilities, expected
    score, most likely exact scoreline, and (for knockouts) penalty odds.
    """
    xg_a = _expected_goals(team_a, team_b)
    xg_b = _expected_goals(team_b, team_a)

    # Head-to-head psychological nudge.
    h2h = team_a.h2h.get(team_b.code)
    if h2h:
        total = h2h["wins"] + h2h["draws"] + h2h["losses"]
        if total > 0:
            edge = (h2h["wins"] - h2h["losses"]) / total
            xg_a *= (1.0 + edge * 0.08)
            xg_b *= (1.0 - edge * 0.08)

    prob_a = prob_draw = prob_b = 0.0
    best_score = (0, 0)
    best_p = 0.0
    for ga in range(max_goals + 1):
        for gb in range(max_goals + 1):
            p = _poisson_pmf(ga, xg_a) * _poisson_pmf(gb, xg_b)
            if p > best_p:
                best_p = p
                best_score = (ga, gb)
            if ga > gb:
                prob_a += p
            elif ga == gb:
                prob_draw += p
            else:
                prob_b += p

    total = prob_a + prob_draw + prob_b
    if total > 0:
        prob_a, prob_draw, prob_b = prob_a / total, prob_draw / total, prob_b / total

    # Penalty shootout odds (knockout only).
    pen_a = _penalty_win_prob(team_a, team_b)
    goes_to_pens = prob_draw if knockout else 0.0

    if knockout:
        # Redistribute the draw probability via the shootout.
        adv_a = prob_a + prob_draw * pen_a
        adv_b = prob_b + prob_draw * (1.0 - pen_a)
        prob_a, prob_b, prob_draw = adv_a, adv_b, 0.0

    key_factors = _key_factors(team_a, team_b, xg_a, xg_b)
    injury_alerts = _injury_alerts(team_a) + _injury_alerts(team_b)

    confidence = min(1.0, abs(prob_a - prob_b) + 0.35)

    return MatchPrediction(
        team_a=team_a, team_b=team_b,
        team_a_win_prob=round(prob_a, 4),
        draw_prob=round(prob_draw, 4),
        team_b_win_prob=round(prob_b, 4),
        predicted_score_a=round(xg_a, 2),
        predicted_score_b=round(xg_b, 2),
        most_likely_score=best_score,
        goes_to_penalties_prob=round(goes_to_pens, 4),
        penalty_win_prob_a=round(pen_a, 4),
        key_factors=key_factors,
        injury_alerts=injury_alerts,
        confidence=round(confidence, 3),
        ai_narrative="",
    )


def _penalty_win_prob(team_a: Team, team_b: Team) -> float:
    """Shootout win probability for team_a based on historical record,
    goalkeeper quality, and big-game temperament."""
    a = team_a.stats.shootout_rate
    b = team_b.stats.shootout_rate

    gk_a = max((p.overall_rating for p in team_a.squad if p.position == "GK"), default=80)
    gk_b = max((p.overall_rating for p in team_b.squad if p.position == "GK"), default=80)
    gk_edge = (gk_a - gk_b) / 100.0

    nerve_a = team_a.pressure_handling / 10.0
    nerve_b = team_b.pressure_handling / 10.0

    raw = (a * 0.4 + nerve_a * 0.4 + 0.5 * 0.2) + gk_edge * 0.15
    raw_b = (b * 0.4 + nerve_b * 0.4 + 0.5 * 0.2)
    total = raw + raw_b
    return raw / total if total > 0 else 0.5


def _key_factors(team_a: Team, team_b: Team, xg_a: float, xg_b: float) -> List[str]:
    factors = []
    pa, pb = team_power_rating(team_a), team_power_rating(team_b)
    if abs(pa - pb) > 6:
        stronger = team_a if pa > pb else team_b
        factors.append(f"{stronger.name} hold a clear overall quality edge "
                       f"({pa:.0f} vs {pb:.0f} power rating).")
    else:
        factors.append(f"Finely balanced on paper ({pa:.0f} vs {pb:.0f}).")

    # Style clash: possession vs pressing.
    if abs(team_a.stats.avg_possession - team_b.stats.avg_possession) > 0.08:
        hog = team_a if team_a.stats.avg_possession > team_b.stats.avg_possession else team_b
        other = team_b if hog is team_a else team_a
        factors.append(f"{hog.name} will dominate the ball; {other.name} must "
                       f"be clinical on the counter.")

    # Set-piece edge.
    if team_a.stats.set_piece_goal_ratio > team_b.stats.set_piece_vulnerability + 0.06:
        factors.append(f"{team_a.name}'s set-piece threat targets a "
                       f"{team_b.name} weakness from dead balls.")
    if team_b.stats.set_piece_goal_ratio > team_a.stats.set_piece_vulnerability + 0.06:
        factors.append(f"{team_b.name}'s set-piece threat targets a "
                       f"{team_a.name} weakness from dead balls.")

    # Depth / fatigue note.
    if abs(team_a.squad_depth_index - team_b.squad_depth_index) > 1.5:
        deeper = team_a if team_a.squad_depth_index > team_b.squad_depth_index else team_b
        factors.append(f"{deeper.name}'s superior squad depth matters most in "
                       f"the latter stages and extra time.")

    return factors


def _injury_alerts(team: Team) -> List[str]:
    alerts = []
    for p in team.injured_players:
        tag = "OUT" if p.injury_status == "injured" else "DOUBTFUL"
        alerts.append(f"[{tag}] {team.name}: {p.name} ({p.injury_detail or 'fitness'})"
                      f" — contribution score {p.contribution_score:.2f}")
    for p in team.suspended_players:
        alerts.append(f"[SUSP] {team.name}: {p.name} suspended")
    return alerts


# ---------------------------------------------------------------------------
# Injury-impact simulation
# ---------------------------------------------------------------------------
def simulate_injury(team: Team, player_name: str) -> Optional[InjuryImpact]:
    """
    Quantify what the team loses if `player_name` is unavailable, and identify
    the most likely replacement and the resulting quality gap.
    """
    player = team.get_player(player_name)
    if player is None:
        return None

    # Find best available replacement in the same position bucket.
    replacement = _best_replacement(team, player)

    if replacement:
        quality_gap = max(0.0, (player.overall_rating - replacement.overall_rating) / 100.0)
        repl_name = replacement.name
        repl_rating = replacement.overall_rating
    else:
        quality_gap = 0.25  # no like-for-like cover is a big problem
        repl_name = "no like-for-like cover"
        repl_rating = max(70, player.overall_rating - 10)

    # Strength loss scales with the player's contribution and irreplaceability,
    # dampened by overall squad depth.
    depth_damp = 1.0 - (team.squad_depth_index / 14.0)
    strength_loss = (player.contribution_score * 0.6 + quality_gap * 0.4) * depth_damp
    strength_loss = max(0.0, min(0.6, strength_loss))

    affected = _affected_areas(player)
    narrative = _injury_narrative(team, player, repl_name, strength_loss, affected)

    return InjuryImpact(
        player=player,
        team_strength_loss=round(strength_loss, 4),
        replacement_name=repl_name,
        replacement_rating=repl_rating,
        replacement_quality_gap=round(quality_gap, 4),
        affected_areas=affected,
        narrative=narrative,
    )


_POSITION_GROUPS = {
    "GK": {"GK"},
    "RB": {"RB", "LB"}, "LB": {"RB", "LB"},
    "CB": {"CB"},
    "CDM": {"CDM", "CM"}, "CM": {"CDM", "CM", "CAM"}, "CAM": {"CAM", "CM"},
    "RW": {"RW", "LW"}, "LW": {"RW", "LW"}, "ST": {"ST"},
}


def _best_replacement(team: Team, player: Player) -> Optional[Player]:
    group = _POSITION_GROUPS.get(player.position, {player.position})
    candidates = [p for p in team.squad
                  if p is not player and p.is_available() and p.position in group]
    if not candidates:
        return None
    return max(candidates, key=lambda p: p.overall_rating)


def _affected_areas(player: Player) -> List[str]:
    areas = []
    if player.goals_per_game >= 0.4:
        areas.append("goalscoring")
    if player.assists_per_game >= 0.25 or player.key_passes_per_game >= 2.0:
        areas.append("creativity / chance creation")
    if player.tackles_per_game >= 2.5:
        areas.append("defensive solidity / ball-winning")
    if player.aerial_win_rate >= 0.65:
        areas.append("aerial duels & set pieces")
    if player.big_game_rating >= 8.5:
        areas.append("big-game leadership")
    if player.position == "GK":
        areas.append("goalkeeping & shot-stopping")
    if not areas:
        areas.append("squad balance")
    return areas


def _injury_narrative(team, player, repl_name, strength_loss, affected) -> str:
    pct = strength_loss * 100
    severity = ("a catastrophic blow" if pct > 20 else
                "a significant loss" if pct > 12 else
                "a notable but manageable absence" if pct > 6 else
                "a minor dip")
    return (
        f"Losing {player.name} ({player.position}, rating {player.overall_rating}) "
        f"would be {severity} for {team.name}, cutting estimated team strength by "
        f"~{pct:.1f}%. Most affected: {', '.join(affected)}. "
        f"{repl_name} steps in. "
        + (f"{player.name} contributes {player.contribution_score*100:.0f}% of the "
           f"team's measured output, so the knock-on effect on "
           f"{', '.join(affected[:2])} is the key worry."
           if player.contribution_score >= 0.12 else
           "The squad has the depth to largely absorb this.")
    )


def power_ranking() -> List[Tuple[Team, float]]:
    """Return all teams sorted by current power rating (injuries included)."""
    from ..data.teams import list_teams
    rated = [(t, team_power_rating(t)) for t in list_teams()]
    return sorted(rated, key=lambda x: x[1], reverse=True)

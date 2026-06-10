"""
Team builder: derive a full Team object from a small set of REAL anchors.

For the top contenders we hand-author detailed squads (see teams.py). For the
remaining nations we don't fabricate fake-precise micro-stats for ~16 players
each. Instead we anchor each team to verifiable facts — FIFA ranking,
confederation, coach, and a few real key players — and DERIVE the rest with a
single documented model:

    strength_factor in [0,1]  <-  FIFA ranking
    team stats (xG, form, possession, ...) <- strength_factor
    squad ratings              <- strength_factor (+ real key players on top)

This keeps the engine fully functional for all 48 teams while being honest
about which numbers are measured vs. modelled. Tune the model in one place.
"""

from ..models import Player, Team, TeamStats


def strength_from_rank(fifa_rank: int) -> float:
    """Map a FIFA ranking to a 0..1 strength factor (rank 1 ~1.0, rank 60 ~0)."""
    return max(0.0, min(1.0, (60 - fifa_rank) / 59.0))


def _base_rating(sf: float) -> int:
    """Average squad rating, ~74 (weak) to ~90 (elite)."""
    return round(74 + 16 * sf)


def _key_player(name, position, club, rating, sf):
    """Construct a key player with stats scaled to position and strength."""
    attacking = position in ("ST", "RW", "LW", "CAM")
    midfield = position in ("CM", "CDM")
    defender = position in ("CB", "RB", "LB")
    gk = position == "GK"
    return Player(
        name=name, position=position, age=27, club=club,
        overall_rating=rating,
        goals_per_game=(0.45 * sf if attacking else 0.08 if midfield else 0.04),
        assists_per_game=(0.3 * sf if attacking or midfield else 0.06),
        key_passes_per_game=(2.4 * sf if attacking else 1.4 if midfield else 0.6),
        tackles_per_game=(2.6 if defender or midfield else 0.8),
        aerial_win_rate=(0.7 if defender else 0.45 if gk else 0.4),
        injury_status="fit", injury_detail="", expected_return="",
        big_game_rating=6.0 + 2.5 * sf,
        form_rating=6.0 + 2.0 * sf,
        contribution_score=0.16 if attacking else 0.12 if midfield else 0.10,
    )


def _filler(position, rating, idx, sf):
    return Player(
        name=f"{position} depth {idx}", position=position, age=26,
        club="—", overall_rating=rating,
        goals_per_game=(0.2 * sf if position in ("ST", "RW", "LW", "CAM") else 0.03),
        assists_per_game=0.1, key_passes_per_game=1.0,
        tackles_per_game=(2.0 if position in ("CB", "CDM", "RB", "LB") else 0.6),
        aerial_win_rate=(0.6 if position in ("CB",) else 0.4),
        injury_status="fit", injury_detail="", expected_return="",
        big_game_rating=5.5, form_rating=6.0, contribution_score=0.04,
    )


# A standard 4-3-3 spine to flesh out a squad around the real key players.
_SQUAD_SHAPE = ["GK", "RB", "CB", "CB", "LB", "CDM", "CM", "CM",
                "RW", "ST", "LW", "GK", "CB", "CM", "RW", "ST"]


def build_team(name, code, confederation, fifa_rank, coach,
               formation="4-3-3", style=None, key_players=None,
               is_host=False) -> Team:
    """
    key_players: list of (name, position, club) tuples — REAL players. Their
    ratings are set a few points above the squad baseline.
    """
    sf = strength_from_rank(fifa_rank)
    base = _base_rating(sf)
    key_players = key_players or []

    # Build squad: real key players first (rated above baseline), then fillers
    # following the standard shape, skipping positions already covered.
    squad = []
    used_positions = []
    for i, (pname, ppos, pclub) in enumerate(key_players):
        bump = 4 - i * 2  # first key player strongest (+4, +2, 0)
        # Cap below the hand-authored elite tier so superstars stay on top.
        squad.append(_key_player(pname, ppos, pclub, min(89, base + bump), sf))
        used_positions.append(ppos)

    shape = _SQUAD_SHAPE[:]
    for pos in used_positions:
        if pos in shape:
            shape.remove(pos)
    for idx, pos in enumerate(shape):
        # depth players slightly below baseline
        squad.append(_filler(pos, max(70, base - 2 - (idx // 4)), idx + 1, sf))

    stats = _derive_stats(sf)

    depth = round(5.0 + 4.5 * sf, 1)
    experience = round(4.5 + 5.0 * sf, 1)
    pressure = round(5.0 + 4.0 * sf, 1)
    age_profile = "balanced"

    return Team(
        name=name, code=code, confederation=confederation,
        fifa_ranking=fifa_rank, coach=coach, formation=formation,
        playing_style=style or _default_style(sf),
        squad=squad, stats=stats,
        tournament_experience=experience, pressure_handling=pressure,
        is_host=is_host, squad_depth_index=depth, age_profile=age_profile,
        h2h={},
    )


def _derive_stats(sf: float) -> TeamStats:
    games = 18
    # Win share scales with strength; losses inversely.
    win_rate = 0.25 + 0.55 * sf
    draw_rate = 0.20
    wins = round(games * win_rate)
    draws = round(games * draw_rate)
    losses = max(0, games - wins - draws)

    gpg = 0.9 + 1.4 * sf
    cpg = 1.7 - 0.9 * sf
    goals_for = round(gpg * games)
    goals_against = round(cpg * games)

    return TeamStats(
        wins=wins, draws=draws, losses=losses,
        goals_scored=goals_for, goals_conceded=goals_against, games_played=games,
        avg_shots_per_game=round(9 + 8 * sf, 1),
        avg_shots_on_target=round(3 + 3.5 * sf, 1),
        xg_for=round(0.9 + 1.4 * sf, 2),
        pass_accuracy=round(0.78 + 0.12 * sf, 2),
        xg_against=round(1.7 - 0.9 * sf, 2),
        clean_sheets=round(games * (0.15 + 0.45 * sf)),
        pressing_intensity=round(5.0 + 3.0 * sf, 1),
        set_piece_goal_ratio=0.25,
        set_piece_vulnerability=round(0.28 - 0.12 * sf, 2),
        avg_possession=round(0.44 + 0.20 * sf, 2),
        avg_yellow_cards=2.0,
        avg_fouls_per_game=12.0,
        shootout_wins=round(3 * sf),
        shootout_losses=round(3 * (1 - sf)),
    )


def _default_style(sf: float) -> str:
    if sf > 0.8:
        return "Elite all-round side capable of controlling games and winning tight knockouts."
    if sf > 0.55:
        return "Well-organised, competitive side that can trouble the favourites on its day."
    if sf > 0.3:
        return "Disciplined, hard-working outfit that relies on structure and moments of quality."
    return "Tournament underdog focused on defensive organisation and set-piece moments."

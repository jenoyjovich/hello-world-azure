"""
Monte Carlo tournament simulator for the 2026 FIFA World Cup.

Two entry points:

  * simulate_bracket(teams, runs)      — a standalone knockout bracket among a
    power-of-two set of teams (quick what-if).
  * simulate_world_cup(runs)           — the FULL real format: 12 groups of 4,
    round-robin group stage, top 2 of each group plus the 8 best third-placed
    teams into a Round of 32, then straight single elimination to the final.

Both use the injury-adjusted Poisson match model from predictor.py, so squad
availability flows through automatically.
"""

import random
from collections import defaultdict
from typing import List, Dict, Optional

from ..models import Team, TournamentSimResult
from .predictor import predict_match, team_power_rating


# ---------------------------------------------------------------------------
# Single match outcome helpers
# ---------------------------------------------------------------------------
def _play_group_match(team_a: Team, team_b: Team):
    """Simulate a group match. Returns (goals_a, goals_b) sampled from the
    model's win/draw/loss probabilities and expected scoreline."""
    pred = predict_match(team_a, team_b, knockout=False)
    r = random.random()
    if r < pred.team_a_win_prob:
        # team A wins — bias the scoreline toward A
        return _sample_decisive(pred.predicted_score_a, pred.predicted_score_b, a_wins=True)
    elif r < pred.team_a_win_prob + pred.draw_prob:
        g = max(0, round((pred.predicted_score_a + pred.predicted_score_b) / 2))
        return g, g
    else:
        return _sample_decisive(pred.predicted_score_a, pred.predicted_score_b, a_wins=False)


def _sample_decisive(xg_a, xg_b, a_wins):
    ga = max(0, round(random.gauss(xg_a, 0.9)))
    gb = max(0, round(random.gauss(xg_b, 0.9)))
    if a_wins and ga <= gb:
        ga = gb + 1
    if not a_wins and gb <= ga:
        gb = ga + 1
    return ga, gb


def _play_knockout(team_a: Team, team_b: Team) -> Team:
    """Simulate one decisive knockout match (penalties resolve draws)."""
    pred = predict_match(team_a, team_b, knockout=True)
    return team_a if random.random() < pred.team_a_win_prob else team_b


# ---------------------------------------------------------------------------
# Group stage
# ---------------------------------------------------------------------------
class _Standing:
    __slots__ = ("team", "played", "won", "drawn", "lost", "gf", "ga", "points")

    def __init__(self, team: Team):
        self.team = team
        self.played = self.won = self.drawn = self.lost = 0
        self.gf = self.ga = self.points = 0

    @property
    def gd(self):
        return self.gf - self.ga

    def record(self, scored, conceded):
        self.played += 1
        self.gf += scored
        self.ga += conceded
        if scored > conceded:
            self.won += 1
            self.points += 3
        elif scored == conceded:
            self.drawn += 1
            self.points += 1
        else:
            self.lost += 1


def simulate_group(teams: List[Team]) -> List[_Standing]:
    """Round-robin (each plays each once). Returns standings sorted by
    points, then goal difference, then goals for (FIFA tiebreakers, simplified)."""
    standings = {t.code: _Standing(t) for t in teams}
    for i in range(len(teams)):
        for j in range(i + 1, len(teams)):
            a, b = teams[i], teams[j]
            ga, gb = _play_group_match(a, b)
            standings[a.code].record(ga, gb)
            standings[b.code].record(gb, ga)
    return sorted(
        standings.values(),
        key=lambda s: (s.points, s.gd, s.gf, random.random()),
        reverse=True,
    )


# ---------------------------------------------------------------------------
# Knockout bracket (seeded, single elimination)
# ---------------------------------------------------------------------------
def _seed_bracket(qualified: List[Team]) -> List[Team]:
    """Order qualifiers into a serpentine-seeded single-elim bracket so that
    stronger teams are kept apart in early rounds. Length must be a power of
    two."""
    ranked = sorted(qualified, key=team_power_rating, reverse=True)
    n = len(ranked)
    # Standard bracket seeding order (1 vs n, 2 vs n-1 spread across the draw).
    seeds = _bracket_seed_order(n)
    return [ranked[s] for s in seeds]


def _bracket_seed_order(n: int) -> List[int]:
    """Return the 0-based seed positions for a single-elim bracket of size n
    (power of two) using the classic recursive method."""
    order = [0]
    while len(order) < n:
        size = len(order) * 2
        new = []
        for x in order:
            new.append(x)
            new.append(size - 1 - x)
        order = new
    return order


def _run_knockout(bracket: List[Team], reach: Dict[str, Dict[str, int]]):
    """Play a seeded bracket to completion, tagging the round each team
    reaches in `reach` (mutated). Returns the winning Team."""
    round_names = _round_names(len(bracket))
    idx = 0
    while len(bracket) > 1:
        label = round_names[idx]
        for t in bracket:
            reach[t.code][label] += 1
        nxt = []
        for i in range(0, len(bracket), 2):
            nxt.append(_play_knockout(bracket[i], bracket[i + 1]))
        bracket = nxt
        idx += 1
    reach[bracket[0].code]["winner"] += 1
    return bracket[0]


def _round_names(size: int) -> List[str]:
    names = {32: "r32", 16: "r16", 8: "quarter", 4: "semi", 2: "final"}
    out = []
    s = size
    while s >= 2:
        out.append(names.get(s, f"round_{s}"))
        s //= 2
    return out


# ---------------------------------------------------------------------------
# Public: standalone knockout bracket
# ---------------------------------------------------------------------------
def simulate_bracket(teams: List[Team], runs: int = 5000,
                     seed: Optional[int] = None) -> TournamentSimResult:
    n = len(teams)
    if n & (n - 1) != 0 or n < 2:
        raise ValueError("Number of teams must be a power of two (2,4,8,16,32).")
    if seed is not None:
        random.seed(seed)

    reach = defaultdict(lambda: defaultdict(int))
    for _ in range(runs):
        bracket = teams[:]
        random.shuffle(bracket)
        _run_knockout(bracket, reach)

    return _assemble_result(runs, [t.code for t in teams], reach)


# ---------------------------------------------------------------------------
# Public: full World Cup (group stage + knockout)
# ---------------------------------------------------------------------------
def simulate_world_cup(runs: int = 2000, seed: Optional[int] = None
                       ) -> TournamentSimResult:
    """Simulate the full 2026 format and return per-team probabilities of
    advancing past the group, reaching each knockout round, and winning."""
    from ..data.groups import GROUPS, BEST_THIRD_PLACED
    from ..data.teams import get_team

    if seed is not None:
        random.seed(seed)

    # Resolve group letter -> list[Team], skipping any codes not yet in the
    # registry (lets the model run before all 48 squads are populated).
    resolved = {}
    for letter, codes in GROUPS.items():
        teams = [get_team(c) for c in codes]
        teams = [t for t in teams if t is not None]
        if len(teams) == 4:
            resolved[letter] = teams

    reach = defaultdict(lambda: defaultdict(int))
    advanced = defaultdict(int)   # reached the knockout stage
    all_codes = [t.code for letter in resolved for t in resolved[letter]]

    for _ in range(runs):
        winners, runners, thirds = [], [], []
        for letter, teams in resolved.items():
            standings = simulate_group(teams)
            winners.append(standings[0].team)
            runners.append(standings[1].team)
            thirds.append(standings[2])  # _Standing for best-third ranking

        # Rank third-placed teams; take the best N.
        thirds_sorted = sorted(
            thirds, key=lambda s: (s.points, s.gd, s.gf, random.random()),
            reverse=True)
        best_thirds = [s.team for s in thirds_sorted[:BEST_THIRD_PLACED]]

        qualified = winners + runners + best_thirds
        for t in qualified:
            advanced[t.code] += 1

        # Pad/trim to a power of two for the bracket (should be 32).
        bracket = _seed_bracket(qualified)
        _run_knockout(bracket, reach)

    result = _assemble_result(runs, all_codes, reach)
    result.group_exit_prob = {
        code: round(1.0 - advanced.get(code, 0) / runs, 4) for code in all_codes
    }
    return result


def _assemble_result(runs, codes, reach) -> TournamentSimResult:
    def col(name):
        return {c: round(reach[c].get(name, 0) / runs, 4) for c in codes}

    return TournamentSimResult(
        runs=runs,
        winner_prob=col("winner"),
        finalist_prob=col("final"),
        semifinal_prob=col("semi"),
        quarterfinal_prob=col("quarter"),
        group_exit_prob={},
        top_scorer_prob={},
        avg_goals_per_game=0.0,
    )

"""
Monte Carlo tournament simulator.

Plays out a knockout bracket many times using the Poisson match model from
predictor.py, then reports each team's probability of reaching each round and
of lifting the trophy. Injuries are baked in because predict_match uses the
current (injury-adjusted) team state.
"""

import random
from collections import defaultdict
from typing import List, Dict

from ..models import Team, TournamentSimResult
from .predictor import predict_match


def _play_knockout(team_a: Team, team_b: Team) -> Team:
    """Simulate one knockout match (decisive — penalties resolve draws)."""
    pred = predict_match(team_a, team_b, knockout=True)
    r = random.random()
    return team_a if r < pred.team_a_win_prob else team_b


def simulate_bracket(teams: List[Team], runs: int = 5000,
                     seed: int = None) -> TournamentSimResult:
    """
    Simulate a single-elimination bracket among `teams` (length must be a
    power of two: 2, 4, 8, 16, 32). Returns aggregated round-reach
    probabilities. Bracket order is shuffled each run for seeding neutrality.
    """
    n = len(teams)
    if n & (n - 1) != 0 or n < 2:
        raise ValueError("Number of teams must be a power of two (2,4,8,16,32).")

    if seed is not None:
        random.seed(seed)

    winner = defaultdict(int)
    finalist = defaultdict(int)
    semi = defaultdict(int)
    quarter = defaultdict(int)
    rounds = n.bit_length() - 1  # e.g. 8 teams -> 3 rounds

    for _ in range(runs):
        bracket = teams[:]
        random.shuffle(bracket)
        round_index = 0
        while len(bracket) > 1:
            # Tag reach for this round's participants.
            remaining = len(bracket)
            if remaining == 2:
                for t in bracket:
                    finalist[t.code] += 1
            elif remaining == 4:
                for t in bracket:
                    semi[t.code] += 1
            elif remaining == 8:
                for t in bracket:
                    quarter[t.code] += 1
            next_round = []
            for i in range(0, len(bracket), 2):
                w = _play_knockout(bracket[i], bracket[i + 1])
                next_round.append(w)
            bracket = next_round
            round_index += 1
        winner[bracket[0].code] += 1

    def norm(d):
        return {code: round(v / runs, 4) for code, v in d.items()}

    # Ensure every team appears in every dict.
    codes = [t.code for t in teams]
    for d in (winner, finalist, semi, quarter):
        for c in codes:
            d.setdefault(c, 0)

    return TournamentSimResult(
        runs=runs,
        winner_prob=norm(winner),
        finalist_prob=norm(finalist),
        semifinal_prob=norm(semi),
        quarterfinal_prob=norm(quarter),
        group_exit_prob={},
        top_scorer_prob={},
        avg_goals_per_game=0.0,
    )

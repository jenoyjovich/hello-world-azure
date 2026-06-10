"""
Command-line interface for the 2026 FIFA World Cup prediction agent.

Examples:
    python -m fifa_predictor.cli rankings
    python -m fifa_predictor.cli teams
    python -m fifa_predictor.cli team ARG
    python -m fifa_predictor.cli predict ARG FRA --knockout
    python -m fifa_predictor.cli injury FRA Mbappe
    python -m fifa_predictor.cli simulate ARG FRA BRA ESP ENG POR GER NED --runs 5000
"""

import argparse
import sys

from .data.teams import get_team, list_teams
from .engine.predictor import team_power_rating, power_ranking
from .engine.tournament import simulate_bracket, simulate_world_cup
from .agent import narrate_match, narrate_injury


def _hr(char="="):
    print(char * 64)


def cmd_teams(_args):
    _hr()
    print("2026 FIFA WORLD CUP — TEAMS IN MODEL")
    _hr()
    for t in list_teams():
        injuries = len(t.injured_players)
        flag = f"  ⚠ {injuries} injury concern(s)" if injuries else ""
        print(f"  [{t.code}] {t.name:<16} FIFA #{t.fifa_ranking:<3} "
              f"{t.coach}{flag}")
    print("\nNote: ratings are illustrative seed data — see data/teams.py.")


def cmd_rankings(_args):
    _hr()
    print("POWER RANKINGS (form + quality + depth + injuries)")
    _hr()
    for i, (team, rating) in enumerate(power_ranking(), 1):
        bar = "█" * int(rating / 3)
        print(f"  {i:>2}. {team.name:<16} {rating:5.1f}  {bar}")


def cmd_team(args):
    t = get_team(args.team)
    if not t:
        print(f"Unknown team: {args.team}")
        return 1
    _hr()
    print(f"{t.name}  [{t.code}]   FIFA #{t.fifa_ranking}")
    _hr("-")
    print(f"  Confederation : {t.confederation}")
    print(f"  Coach         : {t.coach}")
    print(f"  Formation     : {t.formation}")
    print(f"  Power rating  : {team_power_rating(t):.1f}")
    print(f"  Avg squad age : {t.avg_squad_age:.1f}  ({t.age_profile})")
    print(f"  Squad depth   : {t.squad_depth_index}/10")
    print(f"  Experience    : {t.tournament_experience}/10")
    print(f"  Pressure      : {t.pressure_handling}/10")
    print(f"  Style         : {t.playing_style}")
    s = t.stats
    print(f"\n  Form (last {s.games_played}): {s.wins}W-{s.draws}D-{s.losses}L, "
          f"{s.goals_scored} GF / {s.goals_conceded} GA")
    print(f"  xG for/against: {s.xg_for} / {s.xg_against} per game")
    print(f"  Possession    : {s.avg_possession*100:.0f}%   "
          f"Press intensity: {s.pressing_intensity}/10")
    print(f"  Set-piece goals: {s.set_piece_goal_ratio*100:.0f}% of goals  |  "
          f"vulnerability {s.set_piece_vulnerability*100:.0f}%")
    print(f"  Shootout record: {s.shootout_wins}-{s.shootout_losses}")

    print("\n  KEY PLAYERS (by contribution):")
    for p in t.key_players:
        status = "" if p.is_available() else f"  [{p.injury_status.upper()}]"
        print(f"    {p.name:<22} {p.position:<4} {p.overall_rating}  "
              f"contrib {p.contribution_score*100:>4.0f}%{status}")

    if t.injured_players or t.suspended_players:
        print("\n  AVAILABILITY CONCERNS:")
        for p in t.injured_players:
            print(f"    ⚠ {p.name} — {p.injury_status} "
                  f"({p.injury_detail or 'fitness'}), "
                  f"return: {p.expected_return or 'unknown'}")
        for p in t.suspended_players:
            print(f"    ⚠ {p.name} — suspended")
    return 0


def cmd_predict(args):
    a = get_team(args.team_a)
    b = get_team(args.team_b)
    if not a or not b:
        print("Unknown team(s). Use the 'teams' command to list valid codes.")
        return 1
    pred = narrate_match(a, b, knockout=args.knockout)
    _hr()
    print(f"PREDICTION — {a.name} vs {b.name}"
          f"{'  (KNOCKOUT)' if args.knockout else ''}")
    _hr()
    print(f"  {a.name} win : {pred.team_a_win_prob*100:5.1f}%")
    if not args.knockout:
        print(f"  Draw       : {pred.draw_prob*100:5.1f}%")
    print(f"  {b.name} win : {pred.team_b_win_prob*100:5.1f}%")
    print(f"  Expected score: {pred.predicted_score_a} - {pred.predicted_score_b}")
    print(f"  Most likely   : {pred.most_likely_score[0]} - "
          f"{pred.most_likely_score[1]}")
    print(f"  Confidence    : {pred.confidence*100:.0f}%")
    if args.knockout:
        print(f"  Penalty edge  : {a.name} {pred.penalty_win_prob_a*100:.0f}% / "
              f"{b.name} {(1-pred.penalty_win_prob_a)*100:.0f}%")
    _hr("-")
    print("ANALYSIS:\n")
    print(pred.ai_narrative)
    return 0


def cmd_injury(args):
    t = get_team(args.team)
    if not t:
        print(f"Unknown team: {args.team}")
        return 1
    result = narrate_injury(t, args.player)
    if result is None:
        print(f"Player '{args.player}' not found in {t.name}'s squad.")
        print("Players:", ", ".join(p.name for p in t.squad))
        return 1
    _hr()
    print(f"INJURY IMPACT — {t.name}: {args.player}")
    _hr()
    print(result)
    return 0


def cmd_simulate(args):
    teams = [get_team(code) for code in args.teams]
    if any(t is None for t in teams):
        bad = [c for c, t in zip(args.teams, teams) if t is None]
        print(f"Unknown team code(s): {', '.join(bad)}")
        return 1
    n = len(teams)
    if n & (n - 1) != 0:
        print(f"Need a power-of-two number of teams (2,4,8,16,32); got {n}.")
        return 1
    print(f"Simulating {args.runs} knockout brackets among {n} teams...\n")
    res = simulate_bracket(teams, runs=args.runs, seed=args.seed)
    _hr()
    print(f"TOURNAMENT SIMULATION ({res.runs} runs)")
    _hr()
    ranked = sorted(res.winner_prob.items(), key=lambda x: x[1], reverse=True)
    print(f"  {'Team':<6}{'Win':>8}{'Final':>9}{'Semi':>8}{'Quarter':>9}")
    for code, wp in ranked:
        print(f"  {code:<6}{wp*100:>7.1f}%{res.finalist_prob[code]*100:>8.1f}%"
              f"{res.semifinal_prob[code]*100:>7.1f}%"
              f"{res.quarterfinal_prob[code]*100:>8.1f}%")
    return 0


def cmd_groups(_args):
    from .data.groups import GROUPS
    _hr()
    print("2026 FIFA WORLD CUP — GROUPS (official final draw)")
    _hr()
    for letter in sorted(GROUPS):
        names = []
        for code in GROUPS[letter]:
            t = get_team(code)
            names.append(t.name if t else f"{code}(?)")
        print(f"  Group {letter}: " + ", ".join(names))


def cmd_worldcup(args):
    print(f"Simulating the full 48-team World Cup {args.runs} times")
    print("(12 groups -> top 2 + 8 best thirds -> Round of 32 -> Final)...\n")
    res = simulate_world_cup(runs=args.runs, seed=args.seed)
    _hr()
    print(f"WORLD CUP SIMULATION ({res.runs} runs)")
    _hr()
    ranked = sorted(res.winner_prob.items(), key=lambda x: x[1], reverse=True)
    print(f"  {'Team':<6}{'Win':>7}{'Final':>8}{'Semi':>7}{'QF':>7}"
          f"{'Adv':>8}")
    limit = args.top if args.top else len(ranked)
    for code, wp in ranked[:limit]:
        adv = (1.0 - res.group_exit_prob.get(code, 0)) * 100
        print(f"  {code:<6}{wp*100:>6.1f}%{res.finalist_prob[code]*100:>7.1f}%"
              f"{res.semifinal_prob[code]*100:>6.1f}%"
              f"{res.quarterfinal_prob[code]*100:>6.1f}%{adv:>7.1f}%")
    print("\n  Win/Final/Semi/QF = reach probability; Adv = escapes the group.")
    return 0


def build_parser():
    p = argparse.ArgumentParser(
        prog="fifa_predictor",
        description="2026 FIFA World Cup statistical prediction agent.")
    sub = p.add_subparsers(dest="command", required=True)

    sub.add_parser("teams", help="List teams in the model").set_defaults(
        func=cmd_teams)
    sub.add_parser("rankings", help="Power rankings (injury-adjusted)"
                   ).set_defaults(func=cmd_rankings)

    pt = sub.add_parser("team", help="Detailed team profile")
    pt.add_argument("team")
    pt.set_defaults(func=cmd_team)

    pp = sub.add_parser("predict", help="Predict a single match")
    pp.add_argument("team_a")
    pp.add_argument("team_b")
    pp.add_argument("--knockout", action="store_true",
                    help="Resolve draws via penalty shootout")
    pp.set_defaults(func=cmd_predict)

    pi = sub.add_parser("injury", help="Simulate a player's absence")
    pi.add_argument("team")
    pi.add_argument("player")
    pi.set_defaults(func=cmd_injury)

    ps = sub.add_parser("simulate", help="Monte Carlo a knockout bracket")
    ps.add_argument("teams", nargs="+", help="Team codes (power-of-two count)")
    ps.add_argument("--runs", type=int, default=5000)
    ps.add_argument("--seed", type=int, default=None)
    ps.set_defaults(func=cmd_simulate)

    sub.add_parser("groups", help="Show the official 12 groups").set_defaults(
        func=cmd_groups)

    pw = sub.add_parser("worldcup", help="Simulate the full 48-team tournament")
    pw.add_argument("--runs", type=int, default=2000)
    pw.add_argument("--seed", type=int, default=None)
    pw.add_argument("--top", type=int, default=24,
                    help="Show only the top N teams (0 = all 48)")
    pw.set_defaults(func=cmd_worldcup)

    return p


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args) or 0


if __name__ == "__main__":
    sys.exit(main())

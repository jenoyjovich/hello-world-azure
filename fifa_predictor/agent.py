"""
AI narration layer.

The statistical engine produces the numbers; this module asks Claude to turn
them into a sharp, pundit-style analysis. It degrades gracefully: if no API key
is configured, it returns a clean rule-based summary instead, so the tool always
works offline.

Set ANTHROPIC_API_KEY in the environment to enable AI narration.
"""

import os
from typing import Optional

from .models import Team, MatchPrediction, InjuryImpact
from .engine.predictor import (
    predict_match, simulate_injury, team_power_rating,
)

_MODEL = os.environ.get("FIFA_PREDICTOR_MODEL", "claude-sonnet-4-6")


def _client():
    """Return an Anthropic client, or None if unavailable."""
    if not os.environ.get("ANTHROPIC_API_KEY"):
        return None
    try:
        import anthropic
    except ImportError:
        return None
    return anthropic.Anthropic()


def _ask_claude(system: str, prompt: str) -> Optional[str]:
    client = _client()
    if client is None:
        return None
    try:
        msg = client.messages.create(
            model=_MODEL,
            max_tokens=900,
            system=system,
            messages=[{"role": "user", "content": prompt}],
        )
        return "".join(block.text for block in msg.content
                       if getattr(block, "type", None) == "text").strip()
    except Exception as e:  # network/credit/etc. — fall back gracefully
        return None


_SYSTEM = (
    "You are a world-class football (soccer) analyst and data scientist "
    "covering the 2026 FIFA World Cup. You are given the output of a "
    "statistical model. Explain it like an expert pundit: confident, concrete, "
    "and grounded ONLY in the numbers provided. Be concise (3-5 short "
    "paragraphs). Never invent statistics not given to you."
)


def narrate_match(team_a: Team, team_b: Team, knockout: bool = False) -> MatchPrediction:
    """Run the model AND attach an AI (or fallback) narrative."""
    pred = predict_match(team_a, team_b, knockout=knockout)

    facts = _match_facts(pred, knockout)
    ai = _ask_claude(_SYSTEM, facts)
    pred.ai_narrative = ai if ai else _fallback_match_narrative(pred, knockout)
    return pred


def _match_facts(pred: MatchPrediction, knockout: bool) -> str:
    a, b = pred.team_a, pred.team_b
    lines = [
        f"MATCH: {a.name} vs {b.name} "
        f"({'KNOCKOUT' if knockout else 'GROUP STAGE'})",
        f"FIFA rankings: {a.name} #{a.fifa_ranking}, {b.name} #{b.fifa_ranking}",
        f"Power ratings: {a.name} {team_power_rating(a):.1f}, "
        f"{b.name} {team_power_rating(b):.1f}",
        f"Win probability: {a.name} {pred.team_a_win_prob*100:.1f}%, "
        f"Draw {pred.draw_prob*100:.1f}%, {b.name} {pred.team_b_win_prob*100:.1f}%",
        f"Expected goals: {a.name} {pred.predicted_score_a}, "
        f"{b.name} {pred.predicted_score_b}",
        f"Most likely scoreline: {pred.most_likely_score[0]}-{pred.most_likely_score[1]}",
        f"Model confidence: {pred.confidence*100:.0f}%",
        f"{a.name} style: {a.playing_style}",
        f"{b.name} style: {b.playing_style}",
        "KEY FACTORS:",
    ]
    lines += [f"  - {f}" for f in pred.key_factors]
    if knockout:
        lines.append(
            f"Penalty shootout edge if drawn: {a.name} "
            f"{pred.penalty_win_prob_a*100:.0f}% / {b.name} "
            f"{(1-pred.penalty_win_prob_a)*100:.0f}%"
        )
    if pred.injury_alerts:
        lines.append("INJURY / AVAILABILITY:")
        lines += [f"  - {al}" for al in pred.injury_alerts]
    lines.append("\nWrite the analysis and give a clear final prediction.")
    return "\n".join(lines)


def _fallback_match_narrative(pred: MatchPrediction, knockout: bool) -> str:
    a, b = pred.team_a, pred.team_b
    favourite = a if pred.team_a_win_prob >= pred.team_b_win_prob else b
    fav_prob = max(pred.team_a_win_prob, pred.team_b_win_prob)
    out = [
        f"{a.name} vs {b.name} — model read:",
        f"  {a.name} win {pred.team_a_win_prob*100:.1f}% | "
        f"Draw {pred.draw_prob*100:.1f}% | "
        f"{b.name} win {pred.team_b_win_prob*100:.1f}%",
        f"  Expected goals {pred.predicted_score_a}-{pred.predicted_score_b}, "
        f"most likely {pred.most_likely_score[0]}-{pred.most_likely_score[1]}.",
        "",
        f"Verdict: {favourite.name} are favoured ({fav_prob*100:.0f}%).",
    ]
    out += ["", "Why:"] + [f"  - {f}" for f in pred.key_factors]
    if knockout:
        out.append(
            f"  - If it goes to penalties, {a.name} hold a "
            f"{pred.penalty_win_prob_a*100:.0f}% shootout edge."
        )
    if pred.injury_alerts:
        out += ["", "Watch:"] + [f"  - {al}" for al in pred.injury_alerts]
    out += ["", "(Set ANTHROPIC_API_KEY for full AI pundit narration.)"]
    return "\n".join(out)


def narrate_injury(team: Team, player_name: str) -> Optional[str]:
    """Statistical injury impact + AI (or fallback) explanation."""
    impact = simulate_injury(team, player_name)
    if impact is None:
        return None

    facts = (
        f"INJURY SCENARIO for {team.name}.\n"
        f"Player out: {impact.player.name} ({impact.player.position}, "
        f"age {impact.player.age}, rating {impact.player.overall_rating}).\n"
        f"Stats: {impact.player.goals_per_game} goals/game, "
        f"{impact.player.assists_per_game} assists/game, "
        f"{impact.player.key_passes_per_game} key passes/game, "
        f"big-game rating {impact.player.big_game_rating}/10.\n"
        f"Contribution score: {impact.player.contribution_score*100:.0f}% of "
        f"team output.\n"
        f"Estimated team strength loss: {impact.team_strength_loss*100:.1f}%.\n"
        f"Replacement: {impact.replacement_name} "
        f"(rating {impact.replacement_rating}, quality gap "
        f"{impact.replacement_quality_gap*100:.0f}%).\n"
        f"Most affected areas: {', '.join(impact.affected_areas)}.\n"
        f"Team power rating now: {team_power_rating(team):.1f}.\n\n"
        f"Explain the tactical and statistical impact of this absence, how "
        f"{team.name} should adapt, and how much it changes their title odds."
    )
    ai = _ask_claude(_SYSTEM, facts)
    return ai if ai else impact.narrative

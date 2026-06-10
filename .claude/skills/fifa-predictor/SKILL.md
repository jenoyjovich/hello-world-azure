---
name: fifa-predictor
description: >
  Predict 2026 FIFA World Cup outcomes from team statistics. Use when the user
  asks to predict a match, rank teams, analyze a squad, simulate the tournament
  bracket, or assess the impact of an injured/absent player ("what happens if X
  is injured"). Wraps the fifa_predictor Python engine and adds AI narration.
---

# FIFA 2026 World Cup Prediction Agent

A statistical + AI prediction engine for the 2026 FIFA World Cup. The
statistical core (`fifa_predictor/`) is deterministic and runs offline; an
optional Claude narration layer turns the numbers into pundit-style analysis
when `ANTHROPIC_API_KEY` is set.

## When to use this skill

Trigger on requests like:
- "Predict Argentina vs France" / "Who wins England vs Spain?"
- "Rank the World Cup teams" / "Who are the favourites?"
- "What happens to France if Mbappé is injured?"
- "Simulate the knockout bracket"
- "Show me Brazil's squad and key players"

## How to run it

All commands run from the repo root as a Python module:

```bash
# List teams in the model
python -m fifa_predictor.cli teams

# Injury-adjusted power rankings
python -m fifa_predictor.cli rankings

# Detailed team profile (stats, key players, availability)
python -m fifa_predictor.cli team ARG

# Predict a match (add --knockout to resolve draws on penalties)
python -m fifa_predictor.cli predict ARG FRA --knockout

# What-if: impact of a player's absence
python -m fifa_predictor.cli injury FRA Mbappe

# Monte Carlo a knockout bracket (power-of-two team count)
python -m fifa_predictor.cli simulate ARG FRA BRA ESP ENG POR GER NED --runs 5000
```

Team codes: ARG, FRA, BRA, ENG, ESP, POR, GER, NED, USA. You can also pass a
partial team name (e.g. `Argentina`) or partial player name (e.g. `Mbappe`).

## What the model accounts for

- **Squad quality** — per-player ratings, only counting available players
- **Recent form** — W/D/L, goals, xG for & against over the last ~19 games
- **Attack & defense** — xG, shots on target, clean sheets
- **Squad depth** — how well backups cover absences (matters in extra time)
- **Tournament experience & pressure handling**
- **Set-piece threat vs vulnerability**
- **Penalty shootout odds** — keeper quality + temperament + history
- **Head-to-head psychological edges**
- **Playing-style clashes** — possession vs pressing/counter
- **Injuries** — contribution score, replacement quality gap, affected areas

## Enabling AI narration

```bash
export ANTHROPIC_API_KEY=sk-...
# optional: export FIFA_PREDICTOR_MODEL=claude-sonnet-4-6
```

Without a key, the tool prints a clean rule-based analysis instead — it never
fails closed.

## Important: data is illustrative

Ratings and stats in `fifa_predictor/data/teams.py` are hand-seeded
placeholders, NOT a live feed. For accurate predictions, replace the values in
that one file with real data (FIFA rankings, Opta/FBref stats, transfermarkt
injuries). The schema in `fifa_predictor/models.py` is the contract.

## Extending

- **Add a team**: append a `Team(...)` to `data/teams.py` and register it.
- **Tune the model**: weights live in `engine/predictor.py` (`_W`).
- **Add attributes**: extend the dataclasses in `models.py`, then use them in
  `engine/predictor.py`.

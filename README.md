# FIFA 2026 World Cup Prediction Agent ⚽

A statistical + AI prediction engine for the 2026 FIFA World Cup. It turns team
and player statistics into match predictions, power rankings, injury-impact
analysis, and full knockout-bracket simulations — with optional Claude-powered
pundit narration on top.

> **Heads-up on data:** the ratings and stats shipped in
> [`fifa_predictor/data/teams.py`](fifa_predictor/data/teams.py) are
> **hand-seeded, illustrative values** — not a live data feed. The engine,
> simulations, and narration are fully real; to get accurate predictions, swap
> the numbers in that one file for a real source (FIFA rankings, Opta/FBref,
> transfermarkt injuries). The schema in `models.py` is the contract.

## Quick start

```bash
pip install -r requirements.txt

# Injury-adjusted power rankings
python -m fifa_predictor.cli rankings

# Predict a match (knockout resolves draws on penalties)
python -m fifa_predictor.cli predict ARG FRA --knockout

# What-if: how much does an absence hurt?
python -m fifa_predictor.cli injury FRA Mbappe

# Simulate a knockout bracket thousands of times
python -m fifa_predictor.cli simulate ARG FRA BRA ESP ENG POR GER NED --runs 5000
```

No dependencies are required for the statistical engine — `pip install` only
enables the optional AI narration layer.

## Commands

| Command | What it does |
|---|---|
| `teams` | List all teams in the model |
| `rankings` | Power rankings (form + quality + depth + injuries) |
| `team <CODE>` | Full squad profile, stats, key players, availability |
| `predict <A> <B> [--knockout]` | Single-match prediction |
| `injury <TEAM> <PLAYER>` | Simulate a player's absence |
| `simulate <CODES...> [--runs N]` | Monte Carlo a knockout bracket |

Team codes: `ARG FRA BRA ENG ESP POR GER NED USA` (partial names also work).

## What the prediction model accounts for

The engine folds many attributes into a single **power rating** and a
Poisson-based scoreline model:

- **Squad quality** — per-player ratings, counting only *available* players
- **Recent form** — results, goals, and xG for/against
- **Attack & defense** — xG, shots on target, clean sheets
- **Squad depth** — how well backups absorb absences (decisive in extra time)
- **Tournament experience & pressure handling**
- **Set-piece threat vs vulnerability**
- **Penalty shootout odds** — goalkeeper quality, temperament, history
- **Head-to-head** psychological edges
- **Playing-style clashes** — possession vs pressing/counter
- **Injuries & suspensions** — each player has a *contribution score*; the
  engine computes the strength lost, the best replacement, the quality gap, and
  the specific areas affected (goals, creativity, defense, aerials, leadership)

### The injury / "what-if" engine

Ask *"what happens if this player isn't in the team?"* and the model returns:

- estimated **% team strength lost**, damped by squad depth
- the **most likely replacement** and the **quality gap**
- the **affected areas** of the team's game
- a narrative verdict (AI-written if a key is set, rule-based otherwise)

This works for **any** player regardless of current fitness — it's a simulation,
so you can stress-test every scenario.

## AI narration (optional)

```bash
export ANTHROPIC_API_KEY=sk-...
# optional model override:
export FIFA_PREDICTOR_MODEL=claude-sonnet-4-6
```

With a key, predictions and injury reports are narrated by Claude as an expert
analyst, grounded strictly in the model's numbers. Without a key, you still get
a clean rule-based breakdown — the tool never fails.

## Use it as a Claude Code skill

A skill wrapper lives in
[`.claude/skills/fifa-predictor/SKILL.md`](.claude/skills/fifa-predictor/SKILL.md),
so inside Claude Code you can just ask:

> "Predict Spain vs England in a knockout, and tell me what happens if Bellingham is injured."

## Project layout

```
fifa_predictor/
├── models.py            # Dataclasses: Player, Team, TeamStats, predictions
├── data/teams.py        # Illustrative dataset — REPLACE with real data
├── engine/
│   ├── predictor.py     # Power rating, Poisson match model, injury sim
│   └── tournament.py    # Monte Carlo bracket simulator
├── agent.py             # Claude narration layer (+ offline fallback)
└── cli.py               # Command-line interface
```

## Extending

- **Add a team**: append a `Team(...)` in `data/teams.py` and register it in
  `ALL_TEAMS`.
- **Plug in real data**: keep the `models.py` schema, replace the values.
- **Tune the model**: adjust the weights (`_W`) in `engine/predictor.py`.
- **Add a new attribute**: extend the dataclasses, then use it in the engine.

## Ideas for future attributes

Group-of-death difficulty rating, rest-days/fatigue modelling across the
tournament calendar, weather/altitude/venue effects, live in-tournament form
updates, manager tactical tendencies, and a proper group-stage simulator
feeding into the knockout bracket.

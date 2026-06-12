"""
Real 2026 FIFA World Cup match results, updated as the tournament progresses.

Add results here as games are played. The engine reads these to:
  1. Build live group standings for every group.
  2. Apply a form-momentum modifier to each team's power rating — a win
     boosts confidence, a loss deflates it, a draw is neutral.

Format per result:
  {"group": "A", "home": "MEX", "away": "RSA", "hg": 2, "ag": 0, "played": True}

Set played=False for fixtures not yet completed (won't affect standings/form).
"""

RESULTS = [
    # ── GROUP A ──────────────────────────────────────────────────────────
    # Matchday 1
    {"group": "A", "home": "MEX", "away": "RSA", "hg": 2, "ag": 0, "played": True},
    {"group": "A", "home": "KOR", "away": "CZE", "hg": 2, "ag": 1, "played": True},
    # Matchday 2 (upcoming)
    {"group": "A", "home": "MEX", "away": "KOR", "hg": None, "ag": None, "played": False},
    {"group": "A", "home": "RSA", "away": "CZE", "hg": None, "ag": None, "played": False},
    # Matchday 3 (upcoming)
    {"group": "A", "home": "MEX", "away": "CZE", "hg": None, "ag": None, "played": False},
    {"group": "A", "home": "KOR", "away": "RSA", "hg": None, "ag": None, "played": False},

    # ── GROUP B ──────────────────────────────────────────────────────────
    # Matchday 1
    {"group": "B", "home": "CAN", "away": "BIH", "hg": None, "ag": None, "played": False},
    {"group": "B", "home": "QAT", "away": "SUI", "hg": None, "ag": None, "played": False},
    # Matchday 2
    {"group": "B", "home": "CAN", "away": "QAT", "hg": None, "ag": None, "played": False},
    {"group": "B", "home": "SUI", "away": "BIH", "hg": None, "ag": None, "played": False},
    # Matchday 3
    {"group": "B", "home": "CAN", "away": "SUI", "hg": None, "ag": None, "played": False},
    {"group": "B", "home": "BIH", "away": "QAT", "hg": None, "ag": None, "played": False},

    # ── GROUP C ──────────────────────────────────────────────────────────
    {"group": "C", "home": "BRA", "away": "MAR", "hg": None, "ag": None, "played": False},
    {"group": "C", "home": "HAI", "away": "SCO", "hg": None, "ag": None, "played": False},
    {"group": "C", "home": "BRA", "away": "HAI", "hg": None, "ag": None, "played": False},
    {"group": "C", "home": "SCO", "away": "MAR", "hg": None, "ag": None, "played": False},
    {"group": "C", "home": "BRA", "away": "SCO", "hg": None, "ag": None, "played": False},
    {"group": "C", "home": "MAR", "away": "HAI", "hg": None, "ag": None, "played": False},

    # ── GROUP D ──────────────────────────────────────────────────────────
    {"group": "D", "home": "USA", "away": "PAR", "hg": None, "ag": None, "played": False},
    {"group": "D", "home": "AUS", "away": "TUR", "hg": None, "ag": None, "played": False},
    {"group": "D", "home": "USA", "away": "AUS", "hg": None, "ag": None, "played": False},
    {"group": "D", "home": "TUR", "away": "PAR", "hg": None, "ag": None, "played": False},
    {"group": "D", "home": "USA", "away": "TUR", "hg": None, "ag": None, "played": False},
    {"group": "D", "home": "PAR", "away": "AUS", "hg": None, "ag": None, "played": False},

    # ── GROUP E ──────────────────────────────────────────────────────────
    {"group": "E", "home": "GER", "away": "CUW", "hg": None, "ag": None, "played": False},
    {"group": "E", "home": "CIV", "away": "ECU", "hg": None, "ag": None, "played": False},
    {"group": "E", "home": "GER", "away": "CIV", "hg": None, "ag": None, "played": False},
    {"group": "E", "home": "ECU", "away": "CUW", "hg": None, "ag": None, "played": False},
    {"group": "E", "home": "GER", "away": "ECU", "hg": None, "ag": None, "played": False},
    {"group": "E", "home": "CUW", "away": "CIV", "hg": None, "ag": None, "played": False},

    # ── GROUP F ──────────────────────────────────────────────────────────
    {"group": "F", "home": "NED", "away": "JPN", "hg": None, "ag": None, "played": False},
    {"group": "F", "home": "SWE", "away": "TUN", "hg": None, "ag": None, "played": False},
    {"group": "F", "home": "NED", "away": "SWE", "hg": None, "ag": None, "played": False},
    {"group": "F", "home": "TUN", "away": "JPN", "hg": None, "ag": None, "played": False},
    {"group": "F", "home": "NED", "away": "TUN", "hg": None, "ag": None, "played": False},
    {"group": "F", "home": "JPN", "away": "SWE", "hg": None, "ag": None, "played": False},

    # ── GROUP G ──────────────────────────────────────────────────────────
    {"group": "G", "home": "BEL", "away": "EGY", "hg": None, "ag": None, "played": False},
    {"group": "G", "home": "IRN", "away": "NZL", "hg": None, "ag": None, "played": False},
    {"group": "G", "home": "BEL", "away": "IRN", "hg": None, "ag": None, "played": False},
    {"group": "G", "home": "NZL", "away": "EGY", "hg": None, "ag": None, "played": False},
    {"group": "G", "home": "BEL", "away": "NZL", "hg": None, "ag": None, "played": False},
    {"group": "G", "home": "EGY", "away": "IRN", "hg": None, "ag": None, "played": False},

    # ── GROUP H ──────────────────────────────────────────────────────────
    {"group": "H", "home": "ESP", "away": "CPV", "hg": None, "ag": None, "played": False},
    {"group": "H", "home": "KSA", "away": "URU", "hg": None, "ag": None, "played": False},
    {"group": "H", "home": "ESP", "away": "KSA", "hg": None, "ag": None, "played": False},
    {"group": "H", "home": "URU", "away": "CPV", "hg": None, "ag": None, "played": False},
    {"group": "H", "home": "ESP", "away": "URU", "hg": None, "ag": None, "played": False},
    {"group": "H", "home": "CPV", "away": "KSA", "hg": None, "ag": None, "played": False},

    # ── GROUP I ──────────────────────────────────────────────────────────
    {"group": "I", "home": "FRA", "away": "SEN", "hg": None, "ag": None, "played": False},
    {"group": "I", "home": "IRQ", "away": "NOR", "hg": None, "ag": None, "played": False},
    {"group": "I", "home": "FRA", "away": "IRQ", "hg": None, "ag": None, "played": False},
    {"group": "I", "home": "NOR", "away": "SEN", "hg": None, "ag": None, "played": False},
    {"group": "I", "home": "FRA", "away": "NOR", "hg": None, "ag": None, "played": False},
    {"group": "I", "home": "SEN", "away": "IRQ", "hg": None, "ag": None, "played": False},

    # ── GROUP J ──────────────────────────────────────────────────────────
    {"group": "J", "home": "ARG", "away": "ALG", "hg": None, "ag": None, "played": False},
    {"group": "J", "home": "AUT", "away": "JOR", "hg": None, "ag": None, "played": False},
    {"group": "J", "home": "ARG", "away": "AUT", "hg": None, "ag": None, "played": False},
    {"group": "J", "home": "JOR", "away": "ALG", "hg": None, "ag": None, "played": False},
    {"group": "J", "home": "ARG", "away": "JOR", "hg": None, "ag": None, "played": False},
    {"group": "J", "home": "ALG", "away": "AUT", "hg": None, "ag": None, "played": False},

    # ── GROUP K ──────────────────────────────────────────────────────────
    {"group": "K", "home": "POR", "away": "COD", "hg": None, "ag": None, "played": False},
    {"group": "K", "home": "UZB", "away": "COL", "hg": None, "ag": None, "played": False},
    {"group": "K", "home": "POR", "away": "UZB", "hg": None, "ag": None, "played": False},
    {"group": "K", "home": "COL", "away": "COD", "hg": None, "ag": None, "played": False},
    {"group": "K", "home": "POR", "away": "COL", "hg": None, "ag": None, "played": False},
    {"group": "K", "home": "COD", "away": "UZB", "hg": None, "ag": None, "played": False},

    # ── GROUP L ──────────────────────────────────────────────────────────
    {"group": "L", "home": "ENG", "away": "CRO", "hg": None, "ag": None, "played": False},
    {"group": "L", "home": "GHA", "away": "PAN", "hg": None, "ag": None, "played": False},
    {"group": "L", "home": "ENG", "away": "GHA", "hg": None, "ag": None, "played": False},
    {"group": "L", "home": "PAN", "away": "CRO", "hg": None, "ag": None, "played": False},
    {"group": "L", "home": "ENG", "away": "PAN", "hg": None, "ag": None, "played": False},
    {"group": "L", "home": "CRO", "away": "GHA", "hg": None, "ag": None, "played": False},
]


# ── Standings builder ─────────────────────────────────────────────────────────

def group_standings(group_letter: str) -> list:
    """
    Return a sorted standings list for a group based on played results.
    Each entry is a dict: code, played, won, drawn, lost, gf, ga, gd, points.
    """
    from .groups import GROUPS
    codes = GROUPS.get(group_letter.upper(), [])
    table = {c: dict(code=c, played=0, won=0, drawn=0, lost=0,
                     gf=0, ga=0, gd=0, points=0) for c in codes}

    for r in RESULTS:
        if r["group"].upper() != group_letter.upper() or not r["played"]:
            continue
        h, a, hg, ag = r["home"], r["away"], r["hg"], r["ag"]
        for code in (h, a):
            if code not in table:
                table[code] = dict(code=code, played=0, won=0, drawn=0, lost=0,
                                   gf=0, ga=0, gd=0, points=0)
        table[h]["played"] += 1
        table[a]["played"] += 1
        table[h]["gf"] += hg; table[h]["ga"] += ag
        table[a]["gf"] += ag; table[a]["ga"] += hg
        if hg > ag:
            table[h]["won"] += 1;  table[h]["points"] += 3
            table[a]["lost"] += 1
        elif hg < ag:
            table[a]["won"] += 1;  table[a]["points"] += 3
            table[h]["lost"] += 1
        else:
            table[h]["drawn"] += 1; table[h]["points"] += 1
            table[a]["drawn"] += 1; table[a]["points"] += 1

    for row in table.values():
        row["gd"] = row["gf"] - row["ga"]

    return sorted(table.values(),
                  key=lambda r: (r["points"], r["gd"], r["gf"]),
                  reverse=True)


def all_standings() -> dict:
    """Return standings for all 12 groups."""
    from .groups import GROUPS
    return {g: group_standings(g) for g in sorted(GROUPS)}


def momentum_modifier(code: str) -> float:
    """
    Tournament form modifier for a team's power rating.
    Win  → +3%, Draw → 0%, Loss → -4% per game played.
    Caps at ±8% so one bad result doesn't ruin a team.
    """
    delta = 0.0
    for r in RESULTS:
        if not r["played"]:
            continue
        if r["home"] == code:
            hg, ag = r["hg"], r["ag"]
            delta += 3.0 if hg > ag else (-4.0 if hg < ag else 0.0)
        elif r["away"] == code:
            hg, ag = r["hg"], r["ag"]
            delta += 3.0 if ag > hg else (-4.0 if ag < hg else 0.0)
    return max(-8.0, min(8.0, delta)) / 100.0

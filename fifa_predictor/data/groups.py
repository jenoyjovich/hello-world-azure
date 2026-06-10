"""
Official 2026 FIFA World Cup final draw — the 12 groups (A-L).

This is the REAL group draw (drawn 5 December 2025). Team codes map into the
team registry in teams.py. Tournament format constants reflect the real 2026
structure: 48 teams, 12 groups of 4, top 2 of each group plus the 8 best
third-placed teams advance to a Round of 32, then straight single elimination.
"""

# group letter -> list of team codes (in pot/draw order)
GROUPS = {
    "A": ["MEX", "RSA", "KOR", "CZE"],
    "B": ["CAN", "BIH", "QAT", "SUI"],
    "C": ["BRA", "MAR", "HAI", "SCO"],
    "D": ["USA", "AUS", "PAR", "TUR"],
    "E": ["GER", "CUW", "CIV", "ECU"],
    "F": ["NED", "JPN", "SWE", "TUN"],
    "G": ["BEL", "EGY", "IRN", "NZL"],
    "H": ["ESP", "CPV", "KSA", "URU"],
    "I": ["FRA", "SEN", "IRQ", "NOR"],
    "J": ["ARG", "ALG", "AUT", "JOR"],
    "K": ["POR", "COD", "UZB", "COL"],
    "L": ["ENG", "CRO", "GHA", "PAN"],
}

# Tournament format
NUM_GROUPS = 12
TEAMS_PER_GROUP = 4
DIRECT_QUALIFIERS_PER_GROUP = 2   # top two of each group
BEST_THIRD_PLACED = 8             # plus the 8 best third-placed teams
KNOCKOUT_TEAMS = 32               # -> Round of 32

# Points
WIN_POINTS = 3
DRAW_POINTS = 1
LOSS_POINTS = 0


def all_codes():
    """Every team code in the tournament, in group order."""
    codes = []
    for letter in sorted(GROUPS):
        codes.extend(GROUPS[letter])
    return codes


def group_of(code):
    """Return the group letter a team code belongs to, or None."""
    for letter, codes in GROUPS.items():
        if code in codes:
            return letter
    return None

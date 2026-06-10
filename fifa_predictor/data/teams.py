"""
Illustrative 2026 FIFA World Cup dataset.

IMPORTANT: These ratings and statistics are hand-seeded, illustrative values
intended to drive the prediction engine — they are NOT scraped from a live
data provider. To make predictions accurate, replace the values below with a
real feed (Opta, FBref, FIFA rankings, transfermarkt injury data, etc.).
The schema (see fifa_predictor/models.py) is designed so you only edit this
one file to plug in live data.

Injury data reflects an illustrative snapshot as of the seed date.
"""

from ..models import Player, Team, TeamStats


def _p(name, position, age, club, rating, gpg, apg, kpg, tkl, aerial,
       status="fit", detail="", ret="", big=6.0, form=6.5, contrib=0.1):
    return Player(
        name=name, position=position, age=age, club=club,
        overall_rating=rating, goals_per_game=gpg, assists_per_game=apg,
        key_passes_per_game=kpg, tackles_per_game=tkl, aerial_win_rate=aerial,
        injury_status=status, injury_detail=detail, expected_return=ret,
        big_game_rating=big, form_rating=form, contribution_score=contrib,
    )


# ---------------------------------------------------------------------------
# ARGENTINA
# ---------------------------------------------------------------------------
ARGENTINA = Team(
    name="Argentina", code="ARG", confederation="CONMEBOL", fifa_ranking=3,
    coach="Lionel Scaloni", formation="4-3-3",
    playing_style="Balanced possession with lethal transitions; world-class "
                  "individual quality up front and a compact midfield.",
    squad=[
        _p("Emiliano Martinez", "GK", 33, "Aston Villa", 89, 0, 0, 0.1, 0.0, 0.0,
           big=9.5, form=8.0, contrib=0.12),
        _p("Nahuel Molina", "RB", 28, "Atletico Madrid", 82, 0.05, 0.15, 0.8, 2.1, 0.55),
        _p("Cristian Romero", "CB", 28, "Tottenham", 86, 0.08, 0.05, 0.4, 2.8, 0.72,
           big=8.0, form=7.5, contrib=0.09),
        _p("Lisandro Martinez", "CB", 28, "Manchester United", 84, 0.03, 0.05, 0.6, 2.5, 0.60),
        _p("Nicolas Tagliafico", "LB", 33, "Lyon", 80, 0.04, 0.12, 0.7, 2.0, 0.50),
        _p("Rodrigo De Paul", "CM", 31, "Atletico Madrid", 83, 0.1, 0.2, 1.6, 2.4, 0.45,
           big=8.0, form=7.0, contrib=0.10),
        _p("Enzo Fernandez", "CM", 25, "Chelsea", 85, 0.15, 0.25, 2.2, 1.8, 0.50,
           big=8.5, form=7.8, contrib=0.13),
        _p("Alexis Mac Allister", "CM", 27, "Liverpool", 85, 0.2, 0.25, 2.0, 1.9, 0.55,
           big=8.5, form=8.0, contrib=0.13),
        _p("Lionel Messi", "RW", 38, "Inter Miami", 90, 0.75, 0.6, 3.5, 0.5, 0.30,
           big=9.8, form=8.5, contrib=0.22),
        _p("Julian Alvarez", "ST", 26, "Atletico Madrid", 86, 0.55, 0.25, 1.5, 1.2, 0.45,
           big=8.8, form=8.2, contrib=0.16),
        _p("Lautaro Martinez", "ST", 28, "Inter Milan", 87, 0.6, 0.2, 1.0, 0.8, 0.60,
           big=8.5, form=7.5, contrib=0.15),
        # Bench / depth
        _p("Geronimo Rulli", "GK", 33, "Marseille", 80, 0, 0, 0.1, 0.0, 0.0, contrib=0.02),
        _p("Gonzalo Montiel", "RB", 29, "River Plate", 78, 0.04, 0.1, 0.6, 2.0, 0.50, contrib=0.04),
        _p("Leandro Paredes", "CDM", 31, "Roma", 80, 0.06, 0.15, 1.4, 2.2, 0.50, contrib=0.06),
        _p("Giovani Lo Celso", "CAM", 29, "Real Betis", 80, 0.12, 0.2, 1.8, 1.5, 0.40, contrib=0.06),
        _p("Nicolas Gonzalez", "LW", 27, "Juventus", 81, 0.3, 0.2, 1.4, 1.3, 0.50, contrib=0.07),
        _p("Paulo Dybala", "CAM", 32, "Roma", 83, 0.4, 0.3, 2.2, 0.8, 0.30, big=7.5, contrib=0.07),
    ],
    stats=TeamStats(
        wins=14, draws=3, losses=2, goals_scored=38, goals_conceded=12, games_played=19,
        avg_shots_per_game=14.5, avg_shots_on_target=5.8, xg_for=2.0, pass_accuracy=0.86,
        xg_against=0.85, clean_sheets=10, pressing_intensity=7.0,
        set_piece_goal_ratio=0.28, set_piece_vulnerability=0.20,
        avg_possession=0.56, avg_yellow_cards=2.1, avg_fouls_per_game=12.0,
        shootout_wins=4, shootout_losses=1,
    ),
    tournament_experience=9.5, pressure_handling=9.5, is_host=False,
    squad_depth_index=8.5, age_profile="balanced",
    h2h={"FRA": {"wins": 3, "draws": 2, "losses": 6}, "BRA": {"wins": 16, "draws": 26, "losses": 43}},
)


# ---------------------------------------------------------------------------
# FRANCE
# ---------------------------------------------------------------------------
FRANCE = Team(
    name="France", code="FRA", confederation="UEFA", fifa_ranking=1,
    coach="Didier Deschamps", formation="4-2-3-1",
    playing_style="Devastating on the counter with elite pace; pragmatic and "
                  "tournament-savvy with arguably the deepest squad on Earth.",
    squad=[
        _p("Mike Maignan", "GK", 30, "AC Milan", 87, 0, 0, 0.2, 0.0, 0.0, big=8.0, contrib=0.10),
        _p("Jules Kounde", "RB", 27, "Barcelona", 84, 0.05, 0.1, 0.8, 2.4, 0.65, contrib=0.07),
        _p("Dayot Upamecano", "CB", 27, "Bayern Munich", 84, 0.05, 0.03, 0.4, 2.6, 0.70, contrib=0.07),
        _p("William Saliba", "CB", 25, "Arsenal", 86, 0.06, 0.04, 0.5, 2.5, 0.75, big=7.5, contrib=0.09),
        _p("Theo Hernandez", "LB", 28, "AC Milan", 84, 0.12, 0.2, 1.2, 2.0, 0.55, contrib=0.08),
        _p("Aurelien Tchouameni", "CDM", 26, "Real Madrid", 85, 0.08, 0.1, 1.0, 2.8, 0.65,
           big=8.0, form=7.5, contrib=0.10),
        _p("Eduardo Camavinga", "CM", 23, "Real Madrid", 84, 0.06, 0.15, 1.4, 2.6, 0.55, contrib=0.09),
        _p("Antoine Griezmann", "CAM", 35, "Atletico Madrid", 85, 0.35, 0.35, 2.6, 1.4, 0.40,
           big=9.0, form=7.5, contrib=0.13),
        _p("Ousmane Dembele", "RW", 28, "PSG", 86, 0.4, 0.35, 2.4, 0.8, 0.30, big=8.0, form=8.5, contrib=0.14),
        _p("Kylian Mbappe", "LW", 27, "Real Madrid", 91, 0.85, 0.4, 2.8, 0.6, 0.45,
           big=9.5, form=9.0, contrib=0.24),
        _p("Marcus Thuram", "ST", 28, "Inter Milan", 84, 0.5, 0.25, 1.2, 1.0, 0.70, contrib=0.12),
        # Depth
        _p("Brice Samba", "GK", 31, "Rennes", 80, 0, 0, 0.1, 0.0, 0.0, contrib=0.02),
        _p("Ibrahima Konate", "CB", 26, "Liverpool", 83, 0.05, 0.03, 0.4, 2.4, 0.72, contrib=0.06),
        _p("N'Golo Kante", "CDM", 35, "Al-Ittihad", 82, 0.05, 0.1, 1.0, 3.2, 0.50, big=9.0, contrib=0.07),
        _p("Warren Zaire-Emery", "CM", 20, "PSG", 82, 0.1, 0.18, 1.6, 2.2, 0.50, contrib=0.06),
        _p("Bradley Barcola", "LW", 23, "PSG", 82, 0.35, 0.3, 1.8, 0.9, 0.30, contrib=0.07),
        _p("Randal Kolo Muani", "ST", 27, "Juventus", 81, 0.4, 0.2, 1.2, 1.1, 0.60, contrib=0.07),
    ],
    stats=TeamStats(
        wins=15, draws=2, losses=2, goals_scored=42, goals_conceded=14, games_played=19,
        avg_shots_per_game=15.0, avg_shots_on_target=6.0, xg_for=2.1, pass_accuracy=0.85,
        xg_against=0.9, clean_sheets=9, pressing_intensity=7.5,
        set_piece_goal_ratio=0.25, set_piece_vulnerability=0.18,
        avg_possession=0.55, avg_yellow_cards=1.8, avg_fouls_per_game=11.0,
        shootout_wins=2, shootout_losses=2,
    ),
    tournament_experience=9.5, pressure_handling=9.0, is_host=False,
    squad_depth_index=9.5, age_profile="balanced",
    h2h={"ARG": {"wins": 6, "draws": 2, "losses": 3}},
)


# ---------------------------------------------------------------------------
# BRAZIL
# ---------------------------------------------------------------------------
BRAZIL = Team(
    name="Brazil", code="BRA", confederation="CONMEBOL", fifa_ranking=6,
    coach="Carlo Ancelotti", formation="4-2-3-1",
    playing_style="Technical, flair-driven attacking play with full-backs "
                  "bombing forward; reorganised defensively under Ancelotti.",
    squad=[
        _p("Alisson", "GK", 33, "Liverpool", 88, 0, 0, 0.2, 0.0, 0.0, big=8.5, contrib=0.11),
        _p("Danilo", "RB", 34, "Flamengo", 80, 0.05, 0.1, 0.8, 2.2, 0.55, contrib=0.05),
        _p("Marquinhos", "CB", 31, "PSG", 85, 0.08, 0.04, 0.6, 2.4, 0.70, big=7.5, contrib=0.09),
        _p("Gabriel Magalhaes", "CB", 28, "Arsenal", 85, 0.1, 0.03, 0.5, 2.6, 0.78, contrib=0.09),
        _p("Wendell", "LB", 32, "Porto", 78, 0.06, 0.15, 1.0, 2.0, 0.45, contrib=0.05),
        _p("Bruno Guimaraes", "CDM", 28, "Newcastle", 85, 0.12, 0.18, 1.6, 2.8, 0.55,
           big=7.5, form=7.5, contrib=0.11),
        _p("Andre", "CDM", 24, "Wolves", 80, 0.05, 0.1, 1.2, 2.9, 0.50, contrib=0.07),
        _p("Raphinha", "RW", 29, "Barcelona", 87, 0.5, 0.4, 2.6, 1.0, 0.40, big=8.0, form=8.5, contrib=0.16),
        _p("Rodrygo", "CAM", 25, "Real Madrid", 85, 0.4, 0.3, 2.2, 0.8, 0.30, big=8.0, contrib=0.12),
        _p("Vinicius Junior", "LW", 25, "Real Madrid", 89, 0.6, 0.45, 2.8, 0.7, 0.35,
           big=8.5, form=8.0, contrib=0.18),
        _p("Matheus Cunha", "ST", 27, "Manchester United", 82, 0.4, 0.25, 1.6, 1.2, 0.50, contrib=0.10),
        # Depth
        _p("Bento", "GK", 26, "Al-Nassr", 79, 0, 0, 0.1, 0.0, 0.0, contrib=0.02),
        _p("Eder Militao", "CB", 28, "Real Madrid", 84, 0.06, 0.03, 0.4, 2.3, 0.72, contrib=0.06),
        _p("Vanderson", "RB", 24, "Monaco", 79, 0.05, 0.12, 0.9, 2.1, 0.50, contrib=0.04),
        _p("Joao Gomes", "CM", 25, "Wolves", 80, 0.08, 0.1, 1.2, 3.0, 0.55, contrib=0.06),
        _p("Estevao", "RW", 18, "Chelsea", 81, 0.4, 0.3, 2.0, 0.8, 0.25, form=8.0, contrib=0.08),
        _p("Endrick", "ST", 19, "Real Madrid", 80, 0.45, 0.15, 1.0, 0.9, 0.55, contrib=0.07),
    ],
    stats=TeamStats(
        wins=12, draws=4, losses=3, goals_scored=34, goals_conceded=16, games_played=19,
        avg_shots_per_game=15.5, avg_shots_on_target=5.5, xg_for=1.9, pass_accuracy=0.87,
        xg_against=1.0, clean_sheets=7, pressing_intensity=7.0,
        set_piece_goal_ratio=0.22, set_piece_vulnerability=0.24,
        avg_possession=0.58, avg_yellow_cards=2.0, avg_fouls_per_game=13.0,
        shootout_wins=3, shootout_losses=2,
    ),
    tournament_experience=9.0, pressure_handling=7.5, is_host=False,
    squad_depth_index=8.5, age_profile="balanced",
    h2h={"ARG": {"wins": 43, "draws": 26, "losses": 16}},
)


# ---------------------------------------------------------------------------
# ENGLAND
# ---------------------------------------------------------------------------
ENGLAND = Team(
    name="England", code="ENG", confederation="UEFA", fifa_ranking=4,
    coach="Thomas Tuchel", formation="4-2-3-1",
    playing_style="Talent-rich and control-oriented; questions remain over "
                  "converting dominance and tournament killer instinct.",
    squad=[
        _p("Jordan Pickford", "GK", 32, "Everton", 84, 0, 0, 0.2, 0.0, 0.0, big=8.0, contrib=0.09),
        _p("Trent Alexander-Arnold", "RB", 27, "Real Madrid", 84, 0.06, 0.3, 2.0, 1.8, 0.45, contrib=0.09),
        _p("John Stones", "CB", 31, "Manchester City", 84, 0.06, 0.05, 0.6, 2.2, 0.68, contrib=0.07),
        _p("Marc Guehi", "CB", 25, "Crystal Palace", 82, 0.05, 0.03, 0.4, 2.6, 0.72, contrib=0.06),
        _p("Myles Lewis-Skelly", "LB", 19, "Arsenal", 80, 0.06, 0.15, 1.2, 2.2, 0.45, contrib=0.05),
        _p("Declan Rice", "CDM", 27, "Arsenal", 87, 0.15, 0.2, 1.4, 2.8, 0.62, big=8.0, form=8.0, contrib=0.12),
        _p("Jude Bellingham", "CM", 22, "Real Madrid", 89, 0.4, 0.3, 2.4, 2.0, 0.60,
           big=8.5, form=8.5, contrib=0.17),
        _p("Bukayo Saka", "RW", 24, "Arsenal", 87, 0.45, 0.4, 2.6, 1.4, 0.35, big=7.5, form=8.0, contrib=0.15),
        _p("Cole Palmer", "CAM", 23, "Chelsea", 86, 0.5, 0.4, 2.8, 0.9, 0.35, big=8.0, form=8.0, contrib=0.15),
        _p("Phil Foden", "LW", 25, "Manchester City", 86, 0.4, 0.35, 2.4, 1.0, 0.30, contrib=0.13),
        _p("Harry Kane", "ST", 32, "Bayern Munich", 89, 0.75, 0.3, 1.8, 0.6, 0.65, big=8.5, form=8.5, contrib=0.18),
        # Depth
        _p("Dean Henderson", "GK", 29, "Crystal Palace", 79, 0, 0, 0.1, 0.0, 0.0, contrib=0.02),
        _p("Ezri Konsa", "CB", 28, "Aston Villa", 80, 0.04, 0.03, 0.4, 2.3, 0.65, contrib=0.05),
        _p("Kobbie Mainoo", "CM", 21, "Manchester United", 81, 0.1, 0.12, 1.4, 2.4, 0.50, contrib=0.06),
        _p("Anthony Gordon", "LW", 25, "Newcastle", 82, 0.35, 0.3, 1.8, 1.4, 0.30, contrib=0.07),
        _p("Morgan Rogers", "CAM", 23, "Aston Villa", 80, 0.3, 0.3, 2.0, 1.2, 0.40, contrib=0.06),
        _p("Ollie Watkins", "ST", 30, "Aston Villa", 82, 0.5, 0.2, 1.2, 1.0, 0.55, contrib=0.08),
    ],
    stats=TeamStats(
        wins=13, draws=4, losses=2, goals_scored=36, goals_conceded=10, games_played=19,
        avg_shots_per_game=15.0, avg_shots_on_target=5.5, xg_for=2.0, pass_accuracy=0.87,
        xg_against=0.7, clean_sheets=11, pressing_intensity=6.5,
        set_piece_goal_ratio=0.30, set_piece_vulnerability=0.16,
        avg_possession=0.60, avg_yellow_cards=1.6, avg_fouls_per_game=10.0,
        shootout_wins=2, shootout_losses=3,
    ),
    tournament_experience=8.5, pressure_handling=7.0, is_host=False,
    squad_depth_index=9.0, age_profile="youthful",
    h2h={},
)


# ---------------------------------------------------------------------------
# SPAIN
# ---------------------------------------------------------------------------
SPAIN = Team(
    name="Spain", code="ESP", confederation="UEFA", fifa_ranking=2,
    coach="Luis de la Fuente", formation="4-3-3",
    playing_style="Possession-dominant positional play with relentless "
                  "pressing and youthful, fearless wide forwards.",
    squad=[
        _p("Unai Simon", "GK", 28, "Athletic Bilbao", 84, 0, 0, 0.3, 0.0, 0.0, big=7.5, contrib=0.09),
        _p("Pedro Porro", "RB", 26, "Tottenham", 82, 0.08, 0.2, 1.4, 2.0, 0.45, contrib=0.07),
        _p("Pau Cubarsi", "CB", 19, "Barcelona", 83, 0.04, 0.03, 0.5, 2.4, 0.65, contrib=0.07),
        _p("Robin Le Normand", "CB", 29, "Atletico Madrid", 83, 0.06, 0.04, 0.4, 2.5, 0.72, contrib=0.07),
        _p("Marc Cucurella", "LB", 27, "Chelsea", 82, 0.05, 0.15, 1.2, 2.4, 0.50, contrib=0.07),
        _p("Rodri", "CDM", 29, "Manchester City", 90, 0.15, 0.15, 1.6, 3.0, 0.65,
           big=9.0, form=8.0, contrib=0.15),
        _p("Pedri", "CM", 23, "Barcelona", 87, 0.15, 0.25, 2.4, 1.8, 0.40, big=8.0, form=8.5, contrib=0.14),
        _p("Fabian Ruiz", "CM", 30, "PSG", 84, 0.18, 0.2, 1.8, 1.6, 0.55, contrib=0.10),
        _p("Lamine Yamal", "RW", 18, "Barcelona", 88, 0.45, 0.5, 3.0, 0.9, 0.25,
           big=8.5, form=9.0, contrib=0.18),
        _p("Alvaro Morata", "ST", 33, "Como", 81, 0.45, 0.2, 1.2, 0.8, 0.60, contrib=0.10),
        _p("Nico Williams", "LW", 23, "Athletic Bilbao", 85, 0.4, 0.4, 2.4, 1.2, 0.30,
           big=8.0, form=8.0, contrib=0.14),
        # Depth
        _p("David Raya", "GK", 30, "Arsenal", 83, 0, 0, 0.2, 0.0, 0.0, contrib=0.03),
        _p("Dani Vivian", "CB", 26, "Athletic Bilbao", 80, 0.05, 0.03, 0.4, 2.4, 0.68, contrib=0.05),
        _p("Martin Zubimendi", "CDM", 27, "Arsenal", 84, 0.08, 0.12, 1.4, 2.8, 0.55, contrib=0.09),
        _p("Dani Olmo", "CAM", 28, "Barcelona", 84, 0.3, 0.3, 2.4, 1.2, 0.45, big=7.5, contrib=0.10),
        _p("Mikel Oyarzabal", "ST", 29, "Real Sociedad", 83, 0.4, 0.25, 1.8, 1.2, 0.50, big=8.0, contrib=0.09),
        _p("Ferran Torres", "LW", 26, "Barcelona", 82, 0.4, 0.2, 1.6, 1.0, 0.40, contrib=0.08),
    ],
    stats=TeamStats(
        wins=16, draws=2, losses=1, goals_scored=45, goals_conceded=11, games_played=19,
        avg_shots_per_game=17.0, avg_shots_on_target=6.5, xg_for=2.3, pass_accuracy=0.90,
        xg_against=0.7, clean_sheets=12, pressing_intensity=8.5,
        set_piece_goal_ratio=0.20, set_piece_vulnerability=0.15,
        avg_possession=0.65, avg_yellow_cards=1.5, avg_fouls_per_game=9.5,
        shootout_wins=3, shootout_losses=1,
    ),
    tournament_experience=9.0, pressure_handling=8.5, is_host=False,
    squad_depth_index=9.0, age_profile="youthful",
    h2h={},
)


# ---------------------------------------------------------------------------
# PORTUGAL
# ---------------------------------------------------------------------------
PORTUGAL = Team(
    name="Portugal", code="POR", confederation="UEFA", fifa_ranking=5,
    coach="Roberto Martinez", formation="4-3-3",
    playing_style="Star-studded attack with elite wingers and creators; "
                  "occasionally vulnerable defensively against pace.",
    squad=[
        _p("Diogo Costa", "GK", 26, "Porto", 85, 0, 0, 0.3, 0.0, 0.0, big=8.0, contrib=0.10),
        _p("Joao Cancelo", "RB", 31, "Al-Nassr", 83, 0.1, 0.25, 1.8, 1.8, 0.45, contrib=0.08),
        _p("Ruben Dias", "CB", 28, "Manchester City", 87, 0.06, 0.04, 0.6, 2.6, 0.75, big=8.0, contrib=0.10),
        _p("Goncalo Inacio", "CB", 24, "Sporting CP", 83, 0.08, 0.05, 0.6, 2.4, 0.70, contrib=0.07),
        _p("Nuno Mendes", "LB", 23, "PSG", 85, 0.08, 0.2, 1.4, 2.4, 0.50, big=7.5, contrib=0.09),
        _p("Joao Palhinha", "CDM", 30, "Bayern Munich", 84, 0.1, 0.08, 0.8, 3.4, 0.65, contrib=0.09),
        _p("Vitinha", "CM", 26, "PSG", 86, 0.15, 0.2, 2.0, 2.0, 0.40, big=8.0, form=8.5, contrib=0.12),
        _p("Bruno Fernandes", "CAM", 31, "Manchester United", 87, 0.4, 0.45, 3.0, 1.6, 0.45,
           big=8.0, form=8.0, contrib=0.15),
        _p("Bernardo Silva", "RW", 31, "Manchester City", 86, 0.25, 0.3, 2.6, 1.6, 0.35, big=8.5, contrib=0.12),
        _p("Cristiano Ronaldo", "ST", 41, "Al-Nassr", 84, 0.7, 0.15, 1.2, 0.4, 0.70,
           big=9.0, form=7.5, contrib=0.15),
        _p("Rafael Leao", "LW", 26, "AC Milan", 85, 0.4, 0.35, 2.2, 0.8, 0.40, contrib=0.13),
        # Depth
        _p("Jose Sa", "GK", 33, "Wolves", 80, 0, 0, 0.2, 0.0, 0.0, contrib=0.02),
        _p("Antonio Silva", "CB", 22, "Benfica", 81, 0.05, 0.03, 0.4, 2.4, 0.70, contrib=0.05),
        _p("Ruben Neves", "CDM", 29, "Al-Hilal", 83, 0.12, 0.15, 1.6, 2.4, 0.55, contrib=0.08),
        _p("Joao Neves", "CM", 21, "PSG", 84, 0.12, 0.15, 1.8, 2.6, 0.45, form=8.0, contrib=0.09),
        _p("Pedro Neto", "RW", 26, "Chelsea", 82, 0.3, 0.3, 2.0, 1.2, 0.30, contrib=0.08),
        _p("Goncalo Ramos", "ST", 25, "PSG", 82, 0.5, 0.2, 1.2, 1.0, 0.60, contrib=0.08),
    ],
    stats=TeamStats(
        wins=14, draws=3, losses=2, goals_scored=40, goals_conceded=15, games_played=19,
        avg_shots_per_game=15.5, avg_shots_on_target=5.8, xg_for=2.1, pass_accuracy=0.87,
        xg_against=1.0, clean_sheets=8, pressing_intensity=7.0,
        set_piece_goal_ratio=0.26, set_piece_vulnerability=0.22,
        avg_possession=0.58, avg_yellow_cards=1.9, avg_fouls_per_game=11.5,
        shootout_wins=3, shootout_losses=2,
    ),
    tournament_experience=8.5, pressure_handling=7.5, is_host=False,
    squad_depth_index=8.5, age_profile="balanced",
    h2h={},
)


# ---------------------------------------------------------------------------
# GERMANY
# ---------------------------------------------------------------------------
GERMANY = Team(
    name="Germany", code="GER", confederation="UEFA", fifa_ranking=10,
    coach="Julian Nagelsmann", formation="4-2-3-1",
    playing_style="Resurgent possession football with creative midfield "
                  "talents; reborn under Nagelsmann after lean years.",
    squad=[
        _p("Marc-Andre ter Stegen", "GK", 34, "Barcelona", 86, 0, 0, 0.3, 0.0, 0.0, big=8.0, contrib=0.10),
        _p("Joshua Kimmich", "RB", 31, "Bayern Munich", 87, 0.1, 0.3, 2.2, 2.6, 0.50,
           big=8.5, form=8.0, contrib=0.13),
        _p("Antonio Rudiger", "CB", 33, "Real Madrid", 85, 0.06, 0.04, 0.5, 2.6, 0.75, big=8.0, contrib=0.09),
        _p("Jonathan Tah", "CB", 30, "Bayern Munich", 83, 0.06, 0.03, 0.4, 2.4, 0.74, contrib=0.07),
        _p("David Raum", "LB", 28, "RB Leipzig", 81, 0.06, 0.25, 1.8, 2.2, 0.45, contrib=0.07),
        _p("Robert Andrich", "CDM", 31, "Bayer Leverkusen", 81, 0.08, 0.1, 1.0, 3.0, 0.60, contrib=0.07),
        _p("Florian Wirtz", "CAM", 23, "Bayern Munich", 88, 0.4, 0.45, 3.0, 1.4, 0.35,
           big=8.5, form=8.5, contrib=0.17),
        _p("Jamal Musiala", "CAM", 23, "Bayern Munich", 88, 0.45, 0.4, 2.8, 1.0, 0.30,
           big=8.5, form=8.5, contrib=0.17),
        _p("Serge Gnabry", "RW", 30, "Bayern Munich", 83, 0.4, 0.25, 1.8, 0.9, 0.40, contrib=0.11),
        _p("Kai Havertz", "ST", 26, "Arsenal", 84, 0.45, 0.25, 1.6, 1.2, 0.60, big=7.5, contrib=0.12),
        _p("Leroy Sane", "LW", 30, "Galatasaray", 83, 0.35, 0.3, 2.0, 0.8, 0.40, contrib=0.10),
        # Depth
        _p("Oliver Baumann", "GK", 35, "Hoffenheim", 79, 0, 0, 0.2, 0.0, 0.0, contrib=0.02),
        _p("Nico Schlotterbeck", "CB", 26, "Borussia Dortmund", 83, 0.06, 0.05, 0.6, 2.4, 0.70, contrib=0.06),
        _p("Aleksandar Pavlovic", "CDM", 22, "Bayern Munich", 82, 0.08, 0.15, 1.6, 2.6, 0.50, contrib=0.07),
        _p("Angelo Stiller", "CM", 25, "Stuttgart", 82, 0.1, 0.18, 1.8, 2.4, 0.45, contrib=0.07),
        _p("Karim Adeyemi", "RW", 24, "Borussia Dortmund", 81, 0.35, 0.25, 1.6, 1.0, 0.30, contrib=0.07),
        _p("Niclas Fullkrug", "ST", 33, "West Ham", 80, 0.5, 0.15, 1.0, 0.8, 0.70, contrib=0.07),
    ],
    stats=TeamStats(
        wins=13, draws=3, losses=3, goals_scored=39, goals_conceded=18, games_played=19,
        avg_shots_per_game=16.0, avg_shots_on_target=6.0, xg_for=2.1, pass_accuracy=0.88,
        xg_against=1.1, clean_sheets=7, pressing_intensity=7.5,
        set_piece_goal_ratio=0.24, set_piece_vulnerability=0.22,
        avg_possession=0.60, avg_yellow_cards=1.7, avg_fouls_per_game=10.5,
        shootout_wins=5, shootout_losses=0,
    ),
    tournament_experience=9.0, pressure_handling=8.5, is_host=False,
    squad_depth_index=8.0, age_profile="balanced",
    h2h={},
)


# ---------------------------------------------------------------------------
# NETHERLANDS
# ---------------------------------------------------------------------------
NETHERLANDS = Team(
    name="Netherlands", code="NED", confederation="UEFA", fifa_ranking=8,
    coach="Ronald Koeman", formation="4-3-3",
    playing_style="Structured build-up with elite ball-playing defenders and "
                  "incisive wide attackers; tactically flexible.",
    squad=[
        _p("Bart Verbruggen", "GK", 23, "Brighton", 82, 0, 0, 0.3, 0.0, 0.0, contrib=0.08),
        _p("Denzel Dumfries", "RB", 30, "Inter Milan", 83, 0.15, 0.25, 1.4, 2.2, 0.65, contrib=0.09),
        _p("Virgil van Dijk", "CB", 34, "Liverpool", 87, 0.1, 0.05, 0.6, 2.4, 0.82,
           big=8.5, form=8.0, contrib=0.12),
        _p("Jurrien Timber", "CB", 24, "Arsenal", 83, 0.06, 0.08, 0.8, 2.6, 0.65, contrib=0.07),
        _p("Nathan Ake", "LB", 31, "Manchester City", 82, 0.06, 0.06, 0.6, 2.2, 0.65, contrib=0.06),
        _p("Frenkie de Jong", "CM", 28, "Barcelona", 86, 0.1, 0.2, 2.0, 2.4, 0.45,
           big=8.0, form=7.5, contrib=0.13),
        _p("Tijjani Reijnders", "CM", 27, "Manchester City", 84, 0.2, 0.2, 1.8, 2.2, 0.45, contrib=0.10),
        _p("Ryan Gravenberch", "CDM", 23, "Liverpool", 84, 0.1, 0.15, 1.6, 2.8, 0.55, form=8.0, contrib=0.10),
        _p("Cody Gakpo", "LW", 26, "Liverpool", 85, 0.45, 0.3, 2.0, 1.0, 0.55, big=7.5, contrib=0.13),
        _p("Memphis Depay", "ST", 32, "Corinthians", 82, 0.4, 0.35, 2.4, 1.0, 0.45, big=8.0, contrib=0.11),
        _p("Xavi Simons", "RW", 22, "RB Leipzig", 84, 0.35, 0.4, 2.6, 1.2, 0.30, contrib=0.12),
        # Depth
        _p("Mark Flekken", "GK", 32, "Bayer Leverkusen", 79, 0, 0, 0.2, 0.0, 0.0, contrib=0.02),
        _p("Stefan de Vrij", "CB", 34, "Inter Milan", 81, 0.06, 0.04, 0.4, 2.2, 0.72, contrib=0.05),
        _p("Micky van de Ven", "CB", 24, "Tottenham", 83, 0.05, 0.05, 0.5, 2.4, 0.68, contrib=0.06),
        _p("Joey Veerman", "CM", 27, "PSV", 80, 0.12, 0.25, 2.2, 1.6, 0.40, contrib=0.06),
        _p("Brian Brobbey", "ST", 24, "Ajax", 80, 0.45, 0.15, 1.0, 1.0, 0.55, contrib=0.06),
        _p("Donyell Malen", "RW", 27, "Aston Villa", 81, 0.35, 0.25, 1.8, 1.0, 0.35, contrib=0.07),
    ],
    stats=TeamStats(
        wins=12, draws=5, losses=2, goals_scored=35, goals_conceded=14, games_played=19,
        avg_shots_per_game=14.5, avg_shots_on_target=5.4, xg_for=1.9, pass_accuracy=0.87,
        xg_against=0.9, clean_sheets=9, pressing_intensity=7.0,
        set_piece_goal_ratio=0.28, set_piece_vulnerability=0.18,
        avg_possession=0.59, avg_yellow_cards=1.8, avg_fouls_per_game=11.0,
        shootout_wins=2, shootout_losses=3,
    ),
    tournament_experience=8.5, pressure_handling=7.5, is_host=False,
    squad_depth_index=7.5, age_profile="balanced",
    h2h={},
)


# ---------------------------------------------------------------------------
# USA (co-host)
# ---------------------------------------------------------------------------
USA = Team(
    name="United States", code="USA", confederation="CONCACAF", fifa_ranking=16,
    coach="Mauricio Pochettino", formation="4-3-3",
    playing_style="Athletic, high-energy pressing with a European-based core; "
                  "home advantage and rising belief.",
    squad=[
        _p("Matt Turner", "GK", 32, "Lyon", 80, 0, 0, 0.2, 0.0, 0.0, contrib=0.08),
        _p("Sergino Dest", "RB", 25, "PSV", 81, 0.08, 0.2, 1.6, 1.8, 0.40, contrib=0.08),
        _p("Chris Richards", "CB", 26, "Crystal Palace", 80, 0.06, 0.04, 0.4, 2.4, 0.70, contrib=0.06),
        _p("Tim Ream", "CB", 38, "Charlotte", 76, 0.04, 0.03, 0.4, 2.2, 0.65, contrib=0.05),
        _p("Antonee Robinson", "LB", 28, "Fulham", 81, 0.06, 0.2, 1.4, 2.6, 0.45, contrib=0.08),
        _p("Tyler Adams", "CDM", 27, "Bournemouth", 81, 0.06, 0.1, 1.0, 3.2, 0.50, big=7.5, contrib=0.09),
        _p("Weston McKennie", "CM", 27, "Juventus", 81, 0.15, 0.2, 1.6, 2.4, 0.60, contrib=0.09),
        _p("Yunus Musah", "CM", 23, "AC Milan", 80, 0.08, 0.12, 1.4, 2.2, 0.45, contrib=0.07),
        _p("Christian Pulisic", "RW", 27, "AC Milan", 85, 0.5, 0.4, 2.6, 1.2, 0.30,
           big=8.0, form=8.5, contrib=0.18),
        _p("Folarin Balogun", "ST", 24, "Monaco", 80, 0.4, 0.2, 1.2, 1.0, 0.50, contrib=0.10),
        _p("Tim Weah", "LW", 26, "Juventus", 79, 0.25, 0.25, 1.6, 1.4, 0.40, contrib=0.08),
        # Depth
        _p("Patrick Schulte", "GK", 25, "Columbus Crew", 75, 0, 0, 0.1, 0.0, 0.0, contrib=0.02),
        _p("Cameron Carter-Vickers", "CB", 28, "Celtic", 79, 0.05, 0.03, 0.4, 2.4, 0.70, contrib=0.05),
        _p("Johnny Cardoso", "CDM", 24, "Atletico Madrid", 80, 0.08, 0.12, 1.2, 2.8, 0.50, contrib=0.06),
        _p("Gio Reyna", "CAM", 23, "Borussia Monchengladbach", 79, 0.25, 0.3, 2.2, 1.0, 0.30, contrib=0.06),
        _p("Ricardo Pepi", "ST", 23, "PSV", 79, 0.45, 0.15, 1.0, 0.9, 0.55, contrib=0.06),
        _p("Malik Tillman", "CAM", 23, "Bayer Leverkusen", 80, 0.3, 0.25, 2.0, 1.2, 0.40, contrib=0.07),
    ],
    stats=TeamStats(
        wins=11, draws=4, losses=4, goals_scored=30, goals_conceded=20, games_played=19,
        avg_shots_per_game=13.0, avg_shots_on_target=4.6, xg_for=1.6, pass_accuracy=0.83,
        xg_against=1.2, clean_sheets=6, pressing_intensity=8.0,
        set_piece_goal_ratio=0.27, set_piece_vulnerability=0.25,
        avg_possession=0.52, avg_yellow_cards=2.2, avg_fouls_per_game=13.0,
        shootout_wins=2, shootout_losses=2,
    ),
    tournament_experience=6.5, pressure_handling=6.5, is_host=True,
    squad_depth_index=6.5, age_profile="youthful",
    h2h={},
)


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------
# Nine elite contenders are hand-authored above with detailed squads. The other
# 39 nations are built from real anchors (FIFA ranking, coach, key players) in
# extra_teams.py. Together they make up the full 48-team field.
_DETAILED = {
    t.code: t for t in [
        ARGENTINA, FRANCE, BRAZIL, ENGLAND, SPAIN,
        PORTUGAL, GERMANY, NETHERLANDS, USA,
    ]
}

from .extra_teams import build_extra_teams  # noqa: E402

ALL_TEAMS = {**build_extra_teams(), **_DETAILED}


def get_team(identifier: str):
    """Look up a team by 3-letter code or (partial) name, case-insensitive."""
    ident = identifier.strip().upper()
    if ident in ALL_TEAMS:
        return ALL_TEAMS[ident]
    ident_lower = identifier.strip().lower()
    for team in ALL_TEAMS.values():
        if ident_lower in team.name.lower():
            return team
    return None


def list_teams():
    return sorted(ALL_TEAMS.values(), key=lambda t: t.fifa_ranking)

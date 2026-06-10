"""
The remaining 39 nations of the 2026 World Cup, built from REAL anchors:
official April 2026 FIFA ranking, confederation, head coach, and three real key
players each. Team-level stats and squad depth are DERIVED from the ranking via
team_builder.build_team (see that module for the model). Mexico and Canada are
flagged as co-hosts.

The nine elite contenders (ARG, FRA, BRA, ENG, ESP, POR, GER, NED, USA) have
richer hand-authored squads in teams.py and are not rebuilt here.

Data gathered from public sources (ESPN, Goal, FourFourTwo, UEFA, Olympics.com,
etc.). Player clubs marked uncertain in sourcing are best-effort; names and
positions are reliable. Coaching changes through early 2026 are reflected
(e.g. Morocco: Ouahbi, Ghana: Queiroz, Saudi Arabia: Donis, Uzbekistan:
Cannavaro, Sweden: Potter, Tunisia: Lamouchi).
"""

from .team_builder import build_team

# (name, code, confederation, fifa_rank, coach, [key players], is_host)
_SPECS = [
    # ---- Group A ----
    ("Mexico", "MEX", "CONCACAF", 15, "Javier Aguirre", [
        ("Raul Jimenez", "ST", "Fulham"),
        ("Edson Alvarez", "CDM", "West Ham"),
        ("Gilberto Mora", "CAM", "Tijuana")], True),
    ("South Africa", "RSA", "CAF", 60, "Hugo Broos", [
        ("Ronwen Williams", "GK", "Mamelodi Sundowns"),
        ("Teboho Mokoena", "CM", "Mamelodi Sundowns"),
        ("Lyle Foster", "ST", "Burnley")], False),
    ("South Korea", "KOR", "AFC", 25, "Hong Myung-bo", [
        ("Son Heung-min", "LW", "LAFC"),
        ("Lee Kang-in", "CAM", "Paris Saint-Germain"),
        ("Kim Min-jae", "CB", "Bayern Munich")], False),
    ("Czechia", "CZE", "UEFA", 41, "Miroslav Koubek", [
        ("Patrik Schick", "ST", "Bayer Leverkusen"),
        ("Ladislav Krejci", "CB", "Wolves"),
        ("Tomas Soucek", "CM", "West Ham")], False),

    # ---- Group B ----
    ("Canada", "CAN", "CONCACAF", 30, "Jesse Marsch", [
        ("Alphonso Davies", "LB", "Bayern Munich"),
        ("Jonathan David", "ST", "Juventus"),
        ("Stephen Eustaquio", "CM", "Porto")], True),
    ("Bosnia and Herzegovina", "BIH", "UEFA", 65, "Sergej Barbarez", [
        ("Edin Dzeko", "ST", "Schalke"),
        ("Ermedin Demirovic", "ST", "Stuttgart"),
        ("Benjamin Tahirovic", "CM", "Ajax")], False),
    ("Qatar", "QAT", "AFC", 55, "Julen Lopetegui", [
        ("Akram Afif", "RW", "Al-Sadd"),
        ("Almoez Ali", "ST", "Al-Duhail"),
        ("Boualem Khoukhi", "CB", "Al-Sadd")], False),
    ("Switzerland", "SUI", "UEFA", 19, "Murat Yakin", [
        ("Granit Xhaka", "CM", "Sunderland"),
        ("Manuel Akanji", "CB", "Inter Milan"),
        ("Breel Embolo", "ST", "Monaco")], False),

    # ---- Group C ---- (Brazil hand-authored)
    ("Morocco", "MAR", "CAF", 7, "Mohamed Ouahbi", [
        ("Achraf Hakimi", "RB", "Paris Saint-Germain"),
        ("Brahim Diaz", "CAM", "Real Madrid"),
        ("Youssef En-Nesyri", "ST", "Fenerbahce")], False),
    ("Haiti", "HAI", "CONCACAF", 83, "Sebastien Migne", [
        ("Duckens Nazon", "ST", "Al-Markhiya"),
        ("Wilson Isidor", "ST", "Sunderland"),
        ("Frantzdy Pierrot", "ST", "Aris")], False),
    ("Scotland", "SCO", "UEFA", 42, "Steve Clarke", [
        ("Scott McTominay", "CM", "Napoli"),
        ("Andy Robertson", "LB", "Liverpool"),
        ("John McGinn", "CM", "Aston Villa")], False),

    # ---- Group D ---- (USA hand-authored)
    ("Australia", "AUS", "AFC", 27, "Tony Popovic", [
        ("Mathew Ryan", "GK", "Roma"),
        ("Jackson Irvine", "CM", "St. Pauli"),
        ("Nestory Irankunda", "RW", "Bayern Munich")], False),
    ("Paraguay", "PAR", "CONMEBOL", 40, "Gustavo Alfaro", [
        ("Miguel Almiron", "RW", "Atlanta United"),
        ("Diego Gomez", "CM", "Brighton"),
        ("Julio Enciso", "CAM", "Brighton")], False),
    ("Turkey", "TUR", "UEFA", 22, "Vincenzo Montella", [
        ("Arda Guler", "CAM", "Real Madrid"),
        ("Kenan Yildiz", "LW", "Juventus"),
        ("Kerem Akturkoglu", "RW", "Fenerbahce")], False),

    # ---- Group E ---- (Germany hand-authored)
    ("Curacao", "CUW", "CONCACAF", 82, "Dick Advocaat", [
        ("Tahith Chong", "RW", "Sheffield United"),
        ("Leandro Bacuna", "CM", "Almere City"),
        ("Juninho Bacuna", "CM", "Hull City")], False),
    ("Ivory Coast", "CIV", "CAF", 33, "Emerse Fae", [
        ("Amad Diallo", "RW", "Manchester United"),
        ("Franck Kessie", "CM", "Al-Ahli"),
        ("Yan Diomande", "LW", "RB Leipzig")], False),
    ("Ecuador", "ECU", "CONMEBOL", 23, "Sebastian Beccacece", [
        ("Moises Caicedo", "CDM", "Chelsea"),
        ("Piero Hincapie", "CB", "Arsenal"),
        ("Kendry Paez", "CAM", "Chelsea")], False),

    # ---- Group F ---- (Netherlands hand-authored)
    ("Japan", "JPN", "AFC", 18, "Hajime Moriyasu", [
        ("Takefusa Kubo", "RW", "Real Sociedad"),
        ("Wataru Endo", "CDM", "Liverpool"),
        ("Kaoru Mitoma", "LW", "Brighton")], False),
    ("Sweden", "SWE", "UEFA", 38, "Graham Potter", [
        ("Viktor Gyokeres", "ST", "Arsenal"),
        ("Anthony Elanga", "RW", "Newcastle"),
        ("Victor Lindelof", "CB", "Manchester United")], False),
    ("Tunisia", "TUN", "CAF", 46, "Sabri Lamouchi", [
        ("Ellyes Skhiri", "CM", "Eintracht Frankfurt"),
        ("Hannibal Mejbri", "CM", "Burnley"),
        ("Elias Achouri", "CM", "Copenhagen")], False),

    # ---- Group G ----
    ("Belgium", "BEL", "UEFA", 9, "Rudi Garcia", [
        ("Kevin De Bruyne", "CAM", "Napoli"),
        ("Romelu Lukaku", "ST", "Napoli"),
        ("Youri Tielemans", "CM", "Aston Villa")], False),
    ("Egypt", "EGY", "CAF", 29, "Hossam Hassan", [
        ("Mohamed Salah", "RW", "Liverpool"),
        ("Omar Marmoush", "ST", "Manchester City"),
        ("Mohamed Elneny", "CM", "Al-Jazira")], False),
    ("Iran", "IRN", "AFC", 21, "Amir Ghalenoei", [
        ("Mehdi Taremi", "ST", "Inter Milan"),
        ("Alireza Jahanbakhsh", "RW", "Heerenveen"),
        ("Saeid Ezatolahi", "CDM", "Esteghlal")], False),
    ("New Zealand", "NZL", "OFC", 85, "Darren Bazeley", [
        ("Chris Wood", "ST", "Nottingham Forest"),
        ("Marko Stamenic", "CM", "Olympiacos"),
        ("Tyler Bindon", "CB", "Nottingham Forest")], False),

    # ---- Group H ---- (Spain hand-authored)
    ("Cape Verde", "CPV", "CAF", 69, "Bubista", [
        ("Ryan Mendes", "ST", "Al-Wakrah"),
        ("Dailon Livramento", "ST", "Casa Pia"),
        ("Jamiro Monteiro", "CM", "San Jose Earthquakes")], False),
    ("Saudi Arabia", "KSA", "AFC", 61, "Georgios Donis", [
        ("Salem Al-Dawsari", "LW", "Al-Hilal"),
        ("Firas Al-Buraikan", "ST", "Al-Ahli"),
        ("Nawaf Al-Aqidi", "GK", "Al-Nassr")], False),
    ("Uruguay", "URU", "CONMEBOL", 17, "Marcelo Bielsa", [
        ("Federico Valverde", "CM", "Real Madrid"),
        ("Darwin Nunez", "ST", "Al-Hilal"),
        ("Ronald Araujo", "CB", "Barcelona")], False),

    # ---- Group I ---- (France hand-authored)
    ("Senegal", "SEN", "CAF", 14, "Pape Thiaw", [
        ("Sadio Mane", "LW", "Al-Nassr"),
        ("Nicolas Jackson", "ST", "Bayern Munich"),
        ("Kalidou Koulibaly", "CB", "Al-Hilal")], False),
    ("Iraq", "IRQ", "AFC", 57, "Graham Arnold", [
        ("Aymen Hussein", "ST", "Al-Qadsiah"),
        ("Ali Al-Hamadi", "ST", "Ipswich"),
        ("Ali Jasim", "CM", "Como")], False),
    ("Norway", "NOR", "UEFA", 31, "Stale Solbakken", [
        ("Erling Haaland", "ST", "Manchester City"),
        ("Martin Odegaard", "CAM", "Arsenal"),
        ("Alexander Sorloth", "ST", "Atletico Madrid")], False),

    # ---- Group J ---- (Argentina hand-authored)
    ("Algeria", "ALG", "CAF", 28, "Vladimir Petkovic", [
        ("Riyad Mahrez", "RW", "Al-Ahli"),
        ("Ibrahim Maza", "CAM", "Bayer Leverkusen"),
        ("Aissa Mandi", "CB", "Lille")], False),
    ("Austria", "AUT", "UEFA", 24, "Ralf Rangnick", [
        ("David Alaba", "CB", "Real Madrid"),
        ("Marcel Sabitzer", "CM", "Borussia Dortmund"),
        ("Marko Arnautovic", "ST", "Red Bull Salzburg")], False),
    ("Jordan", "JOR", "AFC", 63, "Jamal Sellami", [
        ("Mousa Al-Tamari", "RW", "Rennes"),
        ("Ali Olwan", "ST", "Zamalek"),
        ("Yazan Al-Naimat", "ST", "Al-Hussein")], False),

    # ---- Group K ---- (Portugal hand-authored)
    ("DR Congo", "COD", "CAF", 45, "Sebastien Desabre", [
        ("Yoane Wissa", "ST", "Newcastle"),
        ("Chancel Mbemba", "CB", "Lille"),
        ("Cedric Bakambu", "ST", "Real Betis")], False),
    ("Uzbekistan", "UZB", "AFC", 50, "Fabio Cannavaro", [
        ("Eldor Shomurodov", "ST", "Roma"),
        ("Abdukodir Khusanov", "CB", "Manchester City"),
        ("Jaloliddin Masharipov", "CM", "Tashkent")], False),
    ("Colombia", "COL", "CONMEBOL", 13, "Nestor Lorenzo", [
        ("Luis Diaz", "LW", "Bayern Munich"),
        ("James Rodriguez", "CAM", "Club Leon"),
        ("Jhon Duran", "ST", "Fenerbahce")], False),

    # ---- Group L ---- (England hand-authored)
    ("Croatia", "CRO", "UEFA", 11, "Zlatko Dalic", [
        ("Luka Modric", "CM", "AC Milan"),
        ("Mateo Kovacic", "CM", "Manchester City"),
        ("Andrej Kramaric", "ST", "Hoffenheim")], False),
    ("Ghana", "GHA", "CAF", 73, "Carlos Queiroz", [
        ("Thomas Partey", "CDM", "Villarreal"),
        ("Antoine Semenyo", "ST", "Bournemouth"),
        ("Mohammed Kudus", "CAM", "Tottenham")], False),
    ("Panama", "PAN", "CONCACAF", 34, "Thomas Christiansen", [
        ("Ismael Diaz", "ST", "Leon"),
        ("Anibal Godoy", "CM", "San Jose Earthquakes"),
        ("Adalberto Carrasquilla", "CM", "Houston Dynamo")], False),
]


def build_extra_teams():
    """Return {code: Team} for all 39 derived nations."""
    out = {}
    for name, code, confed, rank, coach, players, is_host in _SPECS:
        out[code] = build_team(
            name=name, code=code, confederation=confed, fifa_rank=rank,
            coach=coach, key_players=players, is_host=is_host)
    return out

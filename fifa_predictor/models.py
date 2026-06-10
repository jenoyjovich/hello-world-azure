from dataclasses import dataclass, field
from typing import List, Optional, Dict, Tuple


@dataclass
class Player:
    name: str
    position: str          # GK, CB, RB, LB, CDM, CM, CAM, RW, LW, ST
    age: int
    club: str
    overall_rating: int    # 1-100
    goals_per_game: float
    assists_per_game: float
    key_passes_per_game: float
    tackles_per_game: float
    aerial_win_rate: float  # 0.0-1.0
    injury_status: str      # "fit", "injured", "doubtful", "suspended"
    injury_detail: str      # e.g. "hamstring strain", "" if fit
    expected_return: str    # ISO date or "out_of_tournament" or ""
    big_game_rating: float  # 1-10, performance in high-stakes matches
    form_rating: float      # 1-10, last 5 games
    contribution_score: float  # 0.0-1.0, share of team's output

    def is_available(self) -> bool:
        return self.injury_status == "fit"

    def availability_factor(self) -> float:
        """Returns 1.0 if fit, 0.5 if doubtful, 0.0 if injured/suspended."""
        mapping = {"fit": 1.0, "doubtful": 0.5, "injured": 0.0, "suspended": 0.0}
        return mapping.get(self.injury_status, 1.0)


@dataclass
class InjuryImpact:
    player: Player
    team_strength_loss: float       # 0.0-1.0, percentage of team strength lost
    replacement_name: str
    replacement_rating: int
    replacement_quality_gap: float  # 0.0-1.0, how much worse the replacement is
    affected_areas: List[str]       # e.g. ["goals", "dribbling", "pressing"]
    narrative: str                  # human-readable analysis


@dataclass
class TeamStats:
    # Recent 12-month form
    wins: int
    draws: int
    losses: int
    goals_scored: int
    goals_conceded: int
    games_played: int

    # Attacking
    avg_shots_per_game: float
    avg_shots_on_target: float
    xg_for: float           # expected goals for, per game
    pass_accuracy: float    # 0.0-1.0

    # Defensive
    xg_against: float       # expected goals against, per game
    clean_sheets: int
    pressing_intensity: float  # 1-10

    # Set pieces
    set_piece_goal_ratio: float     # fraction of goals from set pieces
    set_piece_vulnerability: float  # fraction of conceded from set pieces

    # Style
    avg_possession: float   # 0.0-1.0

    # Discipline
    avg_yellow_cards: float
    avg_fouls_per_game: float

    # Penalty shootouts
    shootout_wins: int
    shootout_losses: int

    @property
    def win_rate(self) -> float:
        if self.games_played == 0:
            return 0.0
        return self.wins / self.games_played

    @property
    def goals_per_game(self) -> float:
        if self.games_played == 0:
            return 0.0
        return self.goals_scored / self.games_played

    @property
    def conceded_per_game(self) -> float:
        if self.games_played == 0:
            return 0.0
        return self.goals_conceded / self.games_played

    @property
    def goal_difference_per_game(self) -> float:
        return self.goals_per_game - self.conceded_per_game

    @property
    def shootout_rate(self) -> float:
        total = self.shootout_wins + self.shootout_losses
        return self.shootout_wins / total if total > 0 else 0.5


@dataclass
class Team:
    name: str
    code: str           # 3-letter FIFA code
    confederation: str  # UEFA, CONMEBOL, CONCACAF, CAF, AFC, OFC
    fifa_ranking: int
    coach: str
    formation: str
    playing_style: str  # narrative description
    squad: List[Player]
    stats: TeamStats

    # Meta attributes
    tournament_experience: float  # 1-10
    pressure_handling: float      # 1-10, performance under pressure
    is_host: bool
    squad_depth_index: float      # 1-10
    age_profile: str              # "veteran", "balanced", "youthful"

    # Head-to-head data keyed by opponent team code
    h2h: Dict[str, Dict] = field(default_factory=dict)

    @property
    def avg_squad_age(self) -> float:
        if not self.squad:
            return 0.0
        return sum(p.age for p in self.squad) / len(self.squad)

    @property
    def avg_squad_rating(self) -> float:
        if not self.squad:
            return 0.0
        available = [p for p in self.squad if p.is_available()]
        if not available:
            return sum(p.overall_rating for p in self.squad) / len(self.squad)
        return sum(p.overall_rating for p in available) / len(available)

    @property
    def key_players(self) -> List[Player]:
        """Top 5 players by contribution score."""
        return sorted(self.squad, key=lambda p: p.contribution_score, reverse=True)[:5]

    @property
    def injured_players(self) -> List[Player]:
        return [p for p in self.squad if p.injury_status in ("injured", "doubtful")]

    @property
    def suspended_players(self) -> List[Player]:
        return [p for p in self.squad if p.injury_status == "suspended"]

    def get_player(self, name: str) -> Optional[Player]:
        name_lower = name.lower()
        for p in self.squad:
            if name_lower in p.name.lower():
                return p
        return None


@dataclass
class MatchPrediction:
    team_a: Team
    team_b: Team
    team_a_win_prob: float
    draw_prob: float
    team_b_win_prob: float
    predicted_score_a: float
    predicted_score_b: float
    most_likely_score: Tuple[int, int]
    goes_to_penalties_prob: float  # only meaningful in knockouts
    penalty_win_prob_a: float
    key_factors: List[str]
    injury_alerts: List[str]
    confidence: float  # 0.0-1.0
    ai_narrative: str  # populated by Claude agent


@dataclass
class TournamentSimResult:
    runs: int
    winner_prob: Dict[str, float]        # team_code -> win probability
    finalist_prob: Dict[str, float]
    semifinal_prob: Dict[str, float]
    quarterfinal_prob: Dict[str, float]
    group_exit_prob: Dict[str, float]
    top_scorer_prob: Dict[str, float]    # player_name -> probability
    avg_goals_per_game: float

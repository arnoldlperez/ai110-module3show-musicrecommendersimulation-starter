import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import asdict, dataclass

# Columns in songs.csv that hold numbers, and the type to convert each one to.
NUMERIC_COLUMNS = {
    "id": int,
    "energy": float,
    "tempo_bpm": float,
    "valence": float,
    "danceability": float,
    "acousticness": float,
}

# Algorithm Recipe weights (max total = 6.0).
GENRE_WEIGHT = 2.0
MOOD_WEIGHT = 1.0
ENERGY_WEIGHT = 1.5
VALENCE_WEIGHT = 1.0
ACOUSTIC_WEIGHT = 0.5

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool
    target_valence: Optional[float] = None

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top k Song objects for the user, ranked by score_song."""
        ranked = sorted(
            self.songs,
            key=lambda song: (-score_song(asdict(user), asdict(song))[0], song.id),
        )
        return ranked[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return the score and reasons for one song as a readable string."""
        score, reasons = score_song(asdict(user), asdict(song))
        return f"Score {score:.2f}: " + "; ".join(reasons)

def load_songs(csv_path: str) -> List[Dict]:
    """Read songs.csv into a list of dicts, converting number columns to int/float."""
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            for column, convert in NUMERIC_COLUMNS.items():
                row[column] = convert(row[column])
            songs.append(row)
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song against the user's preferences and return (score, reasons)."""
    score = 0.0
    reasons: List[str] = []

    if song["genre"] == user_prefs["favorite_genre"]:
        score += GENRE_WEIGHT
        reasons.append(f"genre match (+{GENRE_WEIGHT:.1f})")

    if song["mood"] == user_prefs["favorite_mood"]:
        score += MOOD_WEIGHT
        reasons.append(f"mood match (+{MOOD_WEIGHT:.1f})")

    # Closeness: 1.0 for an exact match, 0.0 for the farthest possible value.
    energy_points = ENERGY_WEIGHT * (1 - abs(song["energy"] - user_prefs["target_energy"]))
    score += energy_points
    reasons.append(
        f"energy {song['energy']:.2f} vs target {user_prefs['target_energy']:.2f} (+{energy_points:.2f})"
    )

    target_valence = user_prefs.get("target_valence")
    if target_valence is not None:
        valence_points = VALENCE_WEIGHT * (1 - abs(song["valence"] - target_valence))
        score += valence_points
        reasons.append(
            f"valence {song['valence']:.2f} vs target {target_valence:.2f} (+{valence_points:.2f})"
        )

    likes_acoustic = user_prefs.get("likes_acoustic")
    if likes_acoustic is not None:
        fit = song["acousticness"] if likes_acoustic else 1 - song["acousticness"]
        acoustic_points = ACOUSTIC_WEIGHT * fit
        score += acoustic_points
        label = "acoustic" if likes_acoustic else "non-acoustic"
        reasons.append(f"{label} fit (+{acoustic_points:.2f})")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score every song, sort highest first (ties by id), and return the top k with explanations."""
    scored = [(song, *score_song(user_prefs, song)) for song in songs]
    ranked = sorted(scored, key=lambda item: (-item[1], item[0]["id"]))
    return [(song, score, "; ".join(reasons)) for song, score, reasons in ranked[:k]]

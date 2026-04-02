import csv
from typing import List, Dict, Tuple
from dataclasses import dataclass


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


class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top-k Song objects best matching the given UserProfile."""
        scored = [(song, self._score(user, song)) for song in self.songs]
        scored.sort(key=lambda x: x[1], reverse=True)
        return [song for song, _ in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a human-readable string describing why a song was recommended."""
        reasons = _build_reasons_song(user, song)
        return "; ".join(reasons) if reasons else "no strong match"

    def _score(self, user: UserProfile, song: Song) -> float:
        """Compute a numeric score for a Song against a UserProfile using genre, mood, and energy."""
        score = 0.0
        if song.genre == user.favorite_genre:
            score += 2.0
        if song.mood == user.favorite_mood:
            score += 1.0
        score += 1.0 - abs(user.target_energy - song.energy)
        return score


def _build_reasons_song(user: UserProfile, song: Song) -> List[str]:
    """Shared helper: produce reason strings from a UserProfile + Song pair."""
    reasons = []
    if song.genre == user.favorite_genre:
        reasons.append(f"genre match (+2.0)")
    if song.mood == user.favorite_mood:
        reasons.append(f"mood match (+1.0)")
    energy_score = 1.0 - abs(user.target_energy - song.energy)
    reasons.append(f"energy proximity ({energy_score:.2f})")
    return reasons


def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file and returns a list of dicts.
    Numerical fields are converted to float/int for math operations.
    Required by src/main.py
    """
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                "id":           int(row["id"]),
                "title":        row["title"],
                "artist":       row["artist"],
                "genre":        row["genre"],
                "mood":         row["mood"],
                "energy":       float(row["energy"]),
                "tempo_bpm":    float(row["tempo_bpm"]),
                "valence":      float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            })
    print(f"Loaded songs: {len(songs)}")
    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, str]:
    """
    Scores a single song against user preferences.

    Algorithm recipe:
      +2.0  genre exact match
      +1.0  mood exact match
      +0–1  energy proximity  = 1 - |user_energy - song_energy|
      +0–1  valence proximity = 1 - |user_valence - song_valence|  (if provided)

    Returns:
        (score, explanation_string)
    """
    score = 0.0
    reasons = []

    if song["genre"] == user_prefs.get("genre", ""):
        score += 2.0
        reasons.append("genre match (+2.0)")

    if song["mood"] == user_prefs.get("mood", ""):
        score += 1.0
        reasons.append("mood match (+1.0)")

    if "energy" in user_prefs:
        energy_score = 1.0 - abs(user_prefs["energy"] - song["energy"])
        score += energy_score
        reasons.append(f"energy proximity ({energy_score:.2f})")

    if "valence" in user_prefs:
        valence_score = 1.0 - abs(user_prefs["valence"] - song["valence"])
        score += valence_score
        reasons.append(f"valence proximity ({valence_score:.2f})")

    explanation = "; ".join(reasons) if reasons else "no match"
    return score, explanation


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Scores all songs, ranks them, and returns the top-k.

    Returns a list of (song_dict, score, explanation) tuples.
    Required by src/main.py
    """
    scored = []
    for song in songs:
        score, explanation = score_song(user_prefs, song)
        scored.append((song, score, explanation))

    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:k]

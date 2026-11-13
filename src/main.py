"""Command line runner for the Music Recommender Simulation (run with: python -m src.main)."""

from typing import Dict, List, Tuple

from src.recommender import load_songs, recommend_songs

# Starter example profile (the README's Sample Recommendation Output uses this one).
DEFAULT_PROFILE = {"favorite_genre": "pop", "favorite_mood": "happy", "target_energy": 0.8}

# Three distinct listener types.
STANDARD_PROFILES = {
    "High-Energy Pop": {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.85,
        "target_valence": 0.80,
        "likes_acoustic": False,
    },
    "Chill Lofi": {
        "favorite_genre": "lofi",
        "favorite_mood": "chill",
        "target_energy": 0.40,
        "target_valence": 0.60,
        "likes_acoustic": True,
    },
    "Deep Intense Rock": {
        "favorite_genre": "rock",
        "favorite_mood": "intense",
        "target_energy": 0.90,
        "target_valence": 0.40,
        "likes_acoustic": False,
    },
}

# Edge cases meant to trick the scoring logic.
ADVERSARIAL_PROFILES = {
    # Wants a sad folk song but at gym-level energy, a combination no song has.
    "Conflicting: high-energy sad folk": {
        "favorite_genre": "folk",
        "favorite_mood": "sad",
        "target_energy": 0.90,
        "target_valence": 0.20,
        "likes_acoustic": True,
    },
    # Same as High-Energy Pop, just capitalized.
    "Capitalized: Pop / Happy": {
        "favorite_genre": "Pop",
        "favorite_mood": "Happy",
        "target_energy": 0.85,
        "target_valence": 0.80,
        "likes_acoustic": False,
    },
    # Genre and mood that do not exist in the catalog.
    "Unknown genre and mood: k-pop / dreamy": {
        "favorite_genre": "k-pop",
        "favorite_mood": "dreamy",
        "target_energy": 0.60,
        "target_valence": 0.70,
    },
    # Energy outside the 0.0 to 1.0 scale.
    "Out of range: energy 1.5": {
        "favorite_genre": "edm",
        "favorite_mood": "euphoric",
        "target_energy": 1.5,
    },
}


def print_recommendations(
    name: str, user_prefs: Dict, recommendations: List[Tuple[Dict, float, str]]
) -> None:
    """Print one profile's top recommendations with the reasons behind each score."""
    profile = ", ".join(f"{key}={value}" for key, value in user_prefs.items())
    print(f"\n### {name}")
    print(f"User profile: {profile}")
    print("=" * 60)
    print("Top recommendations")
    print("=" * 60)
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n{rank}. {song['title']} by {song['artist']}  [{song['genre']} / {song['mood']}]")
        print(f"   Score: {score:.2f}")
        for reason in explanation.split("; "):
            print(f"     - {reason}")


def main() -> None:
    """Load the catalog and print the top 5 for the default, standard, and adversarial profiles."""
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    profiles = {"Default (starter)": DEFAULT_PROFILE, **STANDARD_PROFILES, **ADVERSARIAL_PROFILES}
    for name, user_prefs in profiles.items():
        print_recommendations(name, user_prefs, recommend_songs(user_prefs, songs, k=5))


if __name__ == "__main__":
    main()

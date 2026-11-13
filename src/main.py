"""Command line runner for the Music Recommender Simulation (run with: python -m src.main)."""

from src.recommender import load_songs, recommend_songs


def main() -> None:
    """Load the catalog, score it against the starter profile, and print the top 5."""
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    # Starter example profile
    user_prefs = {"favorite_genre": "pop", "favorite_mood": "happy", "target_energy": 0.8}

    recommendations = recommend_songs(user_prefs, songs, k=5)

    profile = ", ".join(f"{key}={value}" for key, value in user_prefs.items())
    print(f"\nUser profile: {profile}")
    print("=" * 60)
    print("Top recommendations")
    print("=" * 60)
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n{rank}. {song['title']} by {song['artist']}  [{song['genre']} / {song['mood']}]")
        print(f"   Score: {score:.2f}")
        for reason in explanation.split("; "):
            print(f"     - {reason}")


if __name__ == "__main__":
    main()

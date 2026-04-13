"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


PROFILES = {
    # --- Standard profiles ---
    "High-Energy Pop": {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.90,
        "likes_acoustic": False,
    },
    "Chill Lofi": {
        "genre": "lofi",
        "mood": "chill",
        "energy": 0.35,
        "likes_acoustic": True,
    },

    # --- Edge case profiles ---

    # Conflicting signals: high energy but sad mood.
    # No song in the catalog has genre=pop + mood=sad,
    # so energy alone drives the result. Expect intense or synthwave songs to surface.
    "Sad but Hype": {
        "genre": "pop",
        "mood": "sad",
        "energy": 0.90,
        "likes_acoustic": False,
    },

    # Contradictory audio features: acoustic songs are generally low energy,
    # so asking for high energy AND acoustic will likely return mediocre scores
    # for everything — no song satisfies both at once.
    "Acoustic Chaos": {
        "genre": "folk",
        "mood": "nostalgic",
        "energy": 0.95,
        "likes_acoustic": True,
    },

    # Perfectly average user: energy 0.5 means every song gets a similar
    # energy score (~0.12–0.25). Scores will be very close together,
    # exposing whether genre/mood alone can break ties.
    "Middle of the Road": {
        "genre": "jazz",
        "mood": "relaxed",
        "energy": 0.50,
        "likes_acoustic": True,
    },
}


def main() -> None:
    songs = load_songs("data/songs.csv")

    for profile_name, user_prefs in PROFILES.items():
        recommendations = recommend_songs(user_prefs, songs, k=3)

        print("\n" + "=" * 44)
        print(f"  {profile_name}")
        print(f"  Genre: {user_prefs['genre']}  |  Mood: {user_prefs['mood']}  |  Energy: {user_prefs['energy']}")
        print("=" * 44)

        for rank, (song, score, explanation) in enumerate(recommendations, start=1):
            print(f"\n  #{rank}  {song['title']} by {song['artist']}")
            print(f"       Score : {score:.2f}")
            print(f"       Why   : {explanation}")

        print()


if __name__ == "__main__":
    main()
            
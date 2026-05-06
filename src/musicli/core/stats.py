"""Statistics helpers for musicli."""

from __future__ import annotations

from typing import Any


def compute_stats(data: dict[str, Any]) -> dict[str, Any]:
    """Compute summary statistics from the database.

    Args:
        data: The full database dictionary.

    Returns:
        A dictionary with keys:

        - ``album_count``: Number of rated albums.
        - ``song_count``: Number of rated singles.
        - ``tier_count``: Number of tier lists.
        - ``track_count``: Total number of rated album tracks.
        - ``avg_album_rating``: Mean album rating (0 if none).
        - ``avg_track_rating``: Mean track rating across all tracks (0 if none).
        - ``top_album``: The highest-rated album entry dict, or ``None``.
        - ``top_song``: The highest-rated single song entry dict, or ``None``.
        - ``artists``: Sorted list of unique artist names.
    """
    album_ratings = data.get("album_ratings", [])
    song_ratings = data.get("song_ratings", [])
    tier_lists = data.get("tier_lists", [])

    album_count = len(album_ratings)
    song_count = len(song_ratings)
    tier_count = len(tier_lists)

    all_track_ratings = [
        t.get("track_rating", 0)
        for a in album_ratings
        for t in a.get("track_ratings", [])
    ]
    all_track_ratings += [s.get("track_rating", 0) for s in song_ratings]
    track_count = len(all_track_ratings)

    avg_album = (
        sum(a.get("album_rating", 0) for a in album_ratings) / album_count
        if album_count
        else 0.0
    )
    avg_track = sum(all_track_ratings) / len(all_track_ratings) if all_track_ratings else 0.0

    top_album = (
        max(album_ratings, key=lambda x: x.get("album_rating", 0)) if album_ratings else None
    )
    top_song = (
        max(song_ratings, key=lambda x: x.get("track_rating", 0)) if song_ratings else None
    )

    artists = sorted(
        {a.get("artist", "") for a in album_ratings}
        | {s.get("artist", "") for s in song_ratings}
    )

    return {
        "album_count": album_count,
        "song_count": song_count,
        "tier_count": tier_count,
        "track_count": track_count,
        "avg_album_rating": round(avg_album, 2),
        "avg_track_rating": round(avg_track, 2),
        "top_album": top_album,
        "top_song": top_song,
        "artists": artists,
    }

"""Tests for musicli.core.stats."""

from __future__ import annotations

from typing import Any

import pytest


class TestComputeStats:
    def test_empty_db(self, empty_db: dict[str, Any]) -> None:
        from musicli.core.stats import compute_stats

        stats = compute_stats(empty_db)
        assert stats["album_count"] == 0
        assert stats["song_count"] == 0
        assert stats["tier_count"] == 0
        assert stats["track_count"] == 0
        assert stats["avg_album_rating"] == 0.0
        assert stats["avg_track_rating"] == 0.0
        assert stats["top_album"] is None
        assert stats["top_song"] is None
        assert stats["artists"] == []

    def test_with_sample_data(self, sample_db: dict[str, Any]) -> None:
        from musicli.core.stats import compute_stats

        stats = compute_stats(sample_db)
        assert stats["album_count"] == 3
        assert stats["song_count"] == 2
        assert stats["tier_count"] == 1
        assert stats["avg_album_rating"] == pytest.approx((10 + 9 + 8) / 3, rel=1e-2)
        assert stats["top_album"]["album"] == "OK Computer"
        assert "Radiohead" in stats["artists"]
        assert "Nirvana" in stats["artists"]

    def test_track_count_includes_album_tracks_and_singles(self, sample_db: dict[str, Any]) -> None:
        from musicli.core.stats import compute_stats

        stats = compute_stats(sample_db)
        # 2 album tracks (Paranoid Android, Karma Police) + 2 singles
        assert stats["track_count"] == 4

    def test_top_song(self, sample_db: dict[str, Any]) -> None:
        from musicli.core.stats import compute_stats

        stats = compute_stats(sample_db)
        assert stats["top_song"] is not None
        assert stats["top_song"]["track_rating"] == 9  # Smells Like Teen Spirit

    def test_artists_sorted(self, sample_db: dict[str, Any]) -> None:
        from musicli.core.stats import compute_stats

        stats = compute_stats(sample_db)
        assert stats["artists"] == sorted(stats["artists"])

    def test_single_album(self) -> None:
        from musicli.core.stats import compute_stats

        data = {
            "album_ratings": [
                {"artist": "A", "album": "B", "album_rating": 7, "track_ratings": []}
            ],
            "song_ratings": [],
            "tier_lists": [],
        }
        stats = compute_stats(data)
        assert stats["avg_album_rating"] == 7.0
        assert stats["top_album"]["album"] == "B"

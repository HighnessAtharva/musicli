"""Tests for musicli.core.ratings (non-interactive paths)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest


class TestAddAlbumManually:
    """Tests for the programmatic (non-interactive) add_album_manually helper."""

    def test_adds_new_album(self, tmp_db: Path) -> None:
        from musicli.core.ratings import add_album_manually
        from musicli.storage.db import load_db

        entry = add_album_manually("Radiohead", "OK Computer", 10, "Masterpiece")
        assert entry["artist"] == "Radiohead"
        assert entry["album"] == "OK Computer"
        assert entry["album_rating"] == 10
        assert entry["review"] == "Masterpiece"

        data = load_db()
        assert len(data["album_ratings"]) == 1

    def test_updates_existing_album(self, tmp_db: Path) -> None:
        from musicli.core.ratings import add_album_manually
        from musicli.storage.db import load_db

        add_album_manually("Radiohead", "OK Computer", 7)
        add_album_manually("Radiohead", "OK Computer", 10, "Changed my mind")

        data = load_db()
        assert len(data["album_ratings"]) == 1
        assert data["album_ratings"][0]["album_rating"] == 10
        assert data["album_ratings"][0]["review"] == "Changed my mind"

    def test_multiple_albums_stored(self, tmp_db: Path) -> None:
        from musicli.core.ratings import add_album_manually
        from musicli.storage.db import load_db

        add_album_manually("Radiohead", "OK Computer", 10)
        add_album_manually("Nirvana", "Nevermind", 9)
        add_album_manually("Radiohead", "Kid A", 8)

        data = load_db()
        assert len(data["album_ratings"]) == 3

    def test_invalid_rating_below_1(self, tmp_db: Path) -> None:
        from musicli.core.ratings import add_album_manually

        with pytest.raises(ValueError, match="Rating must be between 1 and 10"):
            add_album_manually("Radiohead", "OK Computer", 0)

    def test_invalid_rating_above_10(self, tmp_db: Path) -> None:
        from musicli.core.ratings import add_album_manually

        with pytest.raises(ValueError, match="Rating must be between 1 and 10"):
            add_album_manually("Radiohead", "OK Computer", 11)

    def test_boundary_ratings(self, tmp_db: Path) -> None:
        from musicli.core.ratings import add_album_manually

        # Should not raise
        add_album_manually("A", "B", 1)
        add_album_manually("A", "C", 10)

    def test_empty_review_preserved(self, tmp_db: Path) -> None:
        from musicli.core.ratings import add_album_manually

        entry = add_album_manually("Radiohead", "Amnesiac", 8)
        assert entry["review"] == ""

    def test_entry_has_track_ratings_list(self, tmp_db: Path) -> None:
        from musicli.core.ratings import add_album_manually

        entry = add_album_manually("Radiohead", "Pablo Honey", 5)
        assert "track_ratings" in entry
        assert isinstance(entry["track_ratings"], list)

    def test_does_not_update_review_when_empty_string(self, tmp_db: Path) -> None:
        """Passing empty review on update should not overwrite existing review."""
        from musicli.core.ratings import add_album_manually

        add_album_manually("Radiohead", "OK Computer", 7, "First review")
        # Update rating but don't pass review
        add_album_manually("Radiohead", "OK Computer", 10)

        from musicli.storage.db import load_db
        data = load_db()
        # Review should be preserved (not cleared) because empty string means "don't update"
        assert data["album_ratings"][0]["review"] == "First review"

    def test_special_characters_in_artist(self, tmp_db: Path) -> None:
        from musicli.core.ratings import add_album_manually

        entry = add_album_manually("Sigur Rós", "Ágætis byrjun", 10)
        assert entry["artist"] == "Sigur Rós"

    def test_very_long_album_name(self, tmp_db: Path) -> None:
        from musicli.core.ratings import add_album_manually

        long_name = "A" * 200
        entry = add_album_manually("Artist", long_name, 5)
        assert entry["album"] == long_name

"""Legacy core tests updated for new module structure."""

import json
import pytest
from pathlib import Path


def test_load_or_create_json(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """load_db creates file if missing and loads if present."""
    from musicli.storage import db as db_module

    monkeypatch.setattr(db_module, "get_data_dir", lambda: tmp_path)
    monkeypatch.setattr(db_module, "get_db_path", lambda: tmp_path / "albums.json")

    from musicli.storage.db import load_db

    data = load_db()
    assert "album_ratings" in data
    assert "song_ratings" in data
    assert "tier_lists" in data

    # Should not overwrite
    data["album_ratings"].append({"artist": "A", "album": "B"})
    from musicli.storage.db import save_db
    save_db(data)
    data2 = load_db()
    assert data2["album_ratings"] == data["album_ratings"]


def test_get_album_list(mock_lastfm: object) -> None:
    """get_artist_albums filters nulls and returns sorted list."""
    from musicli.core.lastfm import get_artist_albums

    albums = get_artist_albums("Radiohead")
    assert all("(null)" not in a for a in albums)
    assert albums == sorted(albums)


def test_image_generator(tmp_path: Path, mock_http: None) -> None:
    """image_generator creates a PNG file."""
    from musicli.core.tier import image_generator

    data = {
        "artist": "Test",
        "time": "2024-01-01",
        "s_tier": [{"album": "Test Album", "cover_art": "https://example.com/img.png"}],
        "a_tier": [], "b_tier": [], "c_tier": [], "d_tier": [], "e_tier": [],
    }
    result = image_generator("test_tier.png", data, output_dir=tmp_path)
    assert result.exists()

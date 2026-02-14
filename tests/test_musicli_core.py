import os
import json
import pytest
from musicli import musicli

def test_load_or_create_json(tmp_path, monkeypatch):
    """Test that albums.json is created if missing and loads if present."""
    test_file = tmp_path / "albums.json"
    monkeypatch.chdir(tmp_path)
    # Should create file if not exists
    musicli.load_or_create_json()
    assert test_file.exists()
    with open(test_file) as f:
        data = json.load(f)
    assert "album_ratings" in data and "song_ratings" in data and "tier_lists" in data
    # Should not overwrite if exists
    data["album_ratings"].append({"artist": "A", "album": "B"})
    with open(test_file, "w") as f:
        json.dump(data, f)
    musicli.load_or_create_json()
    with open(test_file) as f:
        data2 = json.load(f)
    assert data2["album_ratings"] == data["album_ratings"]

def test_get_album_list(monkeypatch):
    class DummyArtist:
        def get_top_albums(self):
            class DummyAlbum:
                def __init__(self, name):
                    self.item = name
            return [DummyAlbum("A - Album1"), DummyAlbum("A - Album2"), DummyAlbum("(null)")]
    monkeypatch.setattr(musicli.network, "get_artist", lambda name: DummyArtist())
    albums = musicli.get_album_list("A")
    assert "EXIT" in albums
    assert all("(null)" not in a for a in albums)
    assert len(albums) == 3

def test_image_generator(tmp_path, monkeypatch):
    # Minimal test for image generation
    file_name = "test_tier.png"
    data = {tier: [] for tier in ["s_tier","a_tier","b_tier","c_tier","d_tier","e_tier"]}
    data["s_tier"].append({"album": "Test", "cover_art": "https://community.mp3tag.de/uploads/default/original/2X/a/acf3edeb055e7b77114f9e393d1edeeda37e50c9.png"})
    monkeypatch.chdir(tmp_path)
    musicli.image_generator(file_name, data)
    assert (tmp_path / "output" / file_name).exists()

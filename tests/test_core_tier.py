"""Tests for musicli.core.tier (image generation and tier assignment)."""

from __future__ import annotations

import io
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock

import pytest
from PIL import Image


class TestImageGenerator:
    """Tests for the image_generator function."""

    def _make_cover_mock(self) -> bytes:
        """Return bytes for a tiny 1x1 red PNG."""
        img = Image.new("RGB", (1, 1), color=(200, 50, 50))
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        return buf.getvalue()

    def test_creates_output_file(self, tmp_path: Path, mock_http: None) -> None:
        from musicli.core.tier import image_generator

        data = {
            "artist": "Radiohead",
            "time": "2024-01-01",
            "s_tier": [{"album": "OK Computer", "cover_art": "https://example.com/ok.jpg"}],
            "a_tier": [],
            "b_tier": [],
            "c_tier": [],
            "d_tier": [],
            "e_tier": [],
        }
        result = image_generator("test_tier.png", data, output_dir=tmp_path)
        assert result.exists()
        assert result.suffix == ".png"

    def test_empty_tiers_still_creates_file(self, tmp_path: Path, mock_http: None) -> None:
        from musicli.core.tier import image_generator

        data = {
            "artist": "Test",
            "time": "2024-01-01",
            "s_tier": [],
            "a_tier": [],
            "b_tier": [],
            "c_tier": [],
            "d_tier": [],
            "e_tier": [],
        }
        result = image_generator("empty_tier.png", data, output_dir=tmp_path)
        assert result.exists()

    def test_does_not_overwrite_existing_file(self, tmp_path: Path, mock_http: None) -> None:
        from musicli.core.tier import image_generator

        data = {"artist": "A", "time": "2024-01-01", "s_tier": [], "a_tier": [], "b_tier": [], "c_tier": [], "d_tier": [], "e_tier": []}
        result1 = image_generator("my_tier.png", data, output_dir=tmp_path)
        mtime1 = result1.stat().st_mtime

        # Call again — should not overwrite
        image_generator("my_tier.png", data, output_dir=tmp_path)
        mtime2 = result1.stat().st_mtime
        assert mtime1 == mtime2

    def test_multiple_albums_in_tier(self, tmp_path: Path, mock_http: None) -> None:
        from musicli.core.tier import image_generator

        data = {
            "artist": "Radiohead",
            "time": "2024-01-01",
            "s_tier": [
                {"album": "OK Computer", "cover_art": "https://example.com/ok.jpg"},
                {"album": "Kid A", "cover_art": "https://example.com/kida.jpg"},
            ],
            "a_tier": [],
            "b_tier": [{"album": "Amnesiac", "cover_art": "https://example.com/amnesiac.jpg"}],
            "c_tier": [],
            "d_tier": [],
            "e_tier": [],
        }
        result = image_generator("multi.png", data, output_dir=tmp_path)
        assert result.exists()

    def test_creates_output_dir_if_missing(self, tmp_path: Path, mock_http: None) -> None:
        from musicli.core.tier import image_generator

        new_dir = tmp_path / "nested" / "output"
        data = {"artist": "A", "time": "2024-01-01", "s_tier": [], "a_tier": [], "b_tier": [], "c_tier": [], "d_tier": [], "e_tier": []}
        result = image_generator("test.png", data, output_dir=new_dir)
        assert new_dir.exists()
        assert result.exists()

    def test_long_album_name_truncated(self, tmp_path: Path, mock_http: None) -> None:
        """Should not raise even with very long album names."""
        from musicli.core.tier import image_generator

        data = {
            "artist": "A",
            "time": "2024-01-01",
            "s_tier": [{"album": "X" * 100, "cover_art": "https://example.com/x.jpg"}],
            "a_tier": [],
            "b_tier": [],
            "c_tier": [],
            "d_tier": [],
            "e_tier": [],
        }
        result = image_generator("long_name.png", data, output_dir=tmp_path)
        assert result.exists()

    def test_output_is_valid_image(self, tmp_path: Path, mock_http: None) -> None:
        from musicli.core.tier import image_generator

        data = {"artist": "A", "time": "2024-01-01", "s_tier": [], "a_tier": [], "b_tier": [], "c_tier": [], "d_tier": [], "e_tier": []}
        result = image_generator("valid.png", data, output_dir=tmp_path)
        img = Image.open(result)
        assert img.format == "PNG"
        assert img.size[0] > 0


class TestPickTierAlbums:
    """Tests for the _pick_tier_albums helper (mocking questionary)."""

    def test_returns_empty_when_no_albums(self, monkeypatch: pytest.MonkeyPatch) -> None:
        from musicli.core.tier import _pick_tier_albums

        result = _pick_tier_albums([], "S Tier")
        assert result == []

    def test_returns_selected_albums(self, monkeypatch: pytest.MonkeyPatch) -> None:
        import questionary
        from musicli.core.tier import _pick_tier_albums

        monkeypatch.setattr(
            questionary,
            "checkbox",
            lambda *args, **kwargs: MagicMock(ask=lambda: ["OK Computer"]),
        )
        result = _pick_tier_albums(["OK Computer", "Kid A"], "S Tier")
        assert result == ["OK Computer"]

    def test_returns_empty_when_none_selected(self, monkeypatch: pytest.MonkeyPatch) -> None:
        import questionary
        from musicli.core.tier import _pick_tier_albums

        monkeypatch.setattr(
            questionary,
            "checkbox",
            lambda *args, **kwargs: MagicMock(ask=lambda: None),
        )
        result = _pick_tier_albums(["Album A"], "A Tier")
        assert result == []

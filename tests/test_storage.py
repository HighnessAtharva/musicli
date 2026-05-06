"""Tests for musicli.storage.db."""

from __future__ import annotations

import json
import zipfile
from pathlib import Path
from typing import Any

import pytest


class TestLoadDb:
    def test_creates_file_if_missing(self, tmp_db: Path) -> None:
        from musicli.storage.db import load_db

        assert not tmp_db.exists()
        data = load_db()
        assert tmp_db.exists()
        assert data == {"album_ratings": [], "song_ratings": [], "tier_lists": []}

    def test_loads_existing_file(self, tmp_db: Path, sample_db: dict[str, Any]) -> None:
        from musicli.storage.db import load_db

        tmp_db.write_text(json.dumps(sample_db), encoding="utf-8")
        data = load_db()
        assert len(data["album_ratings"]) == 3
        assert data["album_ratings"][0]["artist"] == "Radiohead"

    def test_does_not_overwrite_existing(self, tmp_db: Path) -> None:
        from musicli.storage.db import load_db

        sentinel = {"album_ratings": [{"artist": "Sentinel"}], "song_ratings": [], "tier_lists": []}
        tmp_db.write_text(json.dumps(sentinel), encoding="utf-8")
        data = load_db()
        assert data["album_ratings"][0]["artist"] == "Sentinel"


class TestSaveDb:
    def test_saves_and_reloads(self, tmp_db: Path) -> None:
        from musicli.storage.db import load_db, save_db

        data = {"album_ratings": [{"artist": "Test", "album": "Album"}], "song_ratings": [], "tier_lists": []}
        save_db(data)
        reloaded = load_db()
        assert reloaded["album_ratings"][0]["artist"] == "Test"

    def test_uses_indent_for_readability(self, tmp_db: Path) -> None:
        from musicli.storage.db import save_db

        save_db({"album_ratings": [], "song_ratings": [], "tier_lists": []})
        content = tmp_db.read_text()
        assert "\n" in content  # indented


class TestMigrateLegacyDb:
    def test_migrates_legacy_file(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        from musicli.storage import db as db_module

        legacy = tmp_path / "albums.json"
        legacy_data = {"album_ratings": [{"artist": "Legacy"}], "song_ratings": [], "tier_lists": []}
        legacy.write_text(json.dumps(legacy_data))

        new_db = tmp_path / "new" / "albums.json"
        monkeypatch.setattr(db_module, "get_db_path", lambda: new_db)

        monkeypatch.chdir(tmp_path)
        from musicli.storage.db import migrate_legacy_db

        result = migrate_legacy_db()
        assert result is True
        assert new_db.exists()

    def test_no_legacy_file_returns_false(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.chdir(tmp_path)
        from musicli.storage.db import migrate_legacy_db

        assert migrate_legacy_db() is False

    def test_skips_if_new_db_exists(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        from musicli.storage import db as db_module

        legacy = tmp_path / "albums.json"
        legacy.write_text("{}")

        existing_db = tmp_path / "existing.json"
        existing_db.write_text("{}")
        monkeypatch.setattr(db_module, "get_db_path", lambda: existing_db)

        monkeypatch.chdir(tmp_path)
        from musicli.storage.db import migrate_legacy_db

        result = migrate_legacy_db()
        assert result is False


class TestBackupDb:
    def test_creates_zip(self, tmp_db: Path, sample_db: dict[str, Any]) -> None:
        from musicli.storage.db import backup_db, save_db

        save_db(sample_db)
        backup_path = backup_db()
        assert backup_path.exists()
        assert backup_path.suffix == ".zip"
        with zipfile.ZipFile(backup_path) as zf:
            assert len(zf.namelist()) > 0


class TestExportCsv:
    def test_creates_csv_with_albums(self, tmp_path: Path, sample_db: dict[str, Any]) -> None:
        from musicli.storage.db import export_csv

        dest = tmp_path / "export.csv"
        export_csv(sample_db, dest)
        content = dest.read_text()
        assert "Radiohead" in content
        assert "OK Computer" in content

    def test_empty_db(self, tmp_path: Path, empty_db: dict[str, Any]) -> None:
        from musicli.storage.db import export_csv

        dest = tmp_path / "export.csv"
        export_csv(empty_db, dest)
        assert dest.exists()


class TestExportMarkdown:
    def test_creates_markdown(self, tmp_path: Path, sample_db: dict[str, Any]) -> None:
        from musicli.storage.db import export_markdown

        dest = tmp_path / "export.md"
        export_markdown(sample_db, dest)
        content = dest.read_text()
        assert "# My Music Ratings" in content
        assert "Radiohead" in content
        assert "⭐" in content

    def test_includes_tier_lists(self, tmp_path: Path, sample_db: dict[str, Any]) -> None:
        from musicli.storage.db import export_markdown

        dest = tmp_path / "export.md"
        export_markdown(sample_db, dest)
        content = dest.read_text()
        assert "Tier Lists" in content
        assert "Radiohead Ranked" in content


class TestExportHtml:
    def test_creates_html(self, tmp_path: Path, sample_db: dict[str, Any]) -> None:
        from musicli.storage.db import export_html

        dest = tmp_path / "export.html"
        export_html(sample_db, dest)
        content = dest.read_text()
        assert "<!DOCTYPE html>" in content
        assert "Radiohead" in content
        assert "OK Computer" in content

    def test_valid_html_structure(self, tmp_path: Path, sample_db: dict[str, Any]) -> None:
        from musicli.storage.db import export_html

        dest = tmp_path / "export.html"
        export_html(sample_db, dest)
        content = dest.read_text()
        assert "<html" in content
        assert "</html>" in content
        assert "<table" in content

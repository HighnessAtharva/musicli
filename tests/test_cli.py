"""Tests for the Typer CLI using typer.testing.CliRunner."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest
from typer.testing import CliRunner

from musicli.cli import app

runner = CliRunner()


class TestVersionFlag:
    def test_version_output(self) -> None:
        result = runner.invoke(app, ["--version"])
        assert result.exit_code == 0
        assert "musicli" in result.output
        assert "2.0.0" in result.output


class TestViewAlbums:
    def test_empty_library(self, tmp_db: Path) -> None:
        result = runner.invoke(app, ["view", "albums"])
        assert result.exit_code == 0
        assert "No albums rated" in result.output

    def test_shows_rated_albums(self, tmp_db_with_data: Path) -> None:
        result = runner.invoke(app, ["view", "albums"])
        assert result.exit_code == 0
        assert "Radiohead" in result.output
        assert "OK Computer" in result.output

    def test_sort_by_rating(self, tmp_db_with_data: Path) -> None:
        result = runner.invoke(app, ["view", "albums", "--sort", "rating"])
        assert result.exit_code == 0
        assert "Radiohead" in result.output

    def test_filter_by_artist(self, tmp_db_with_data: Path) -> None:
        result = runner.invoke(app, ["view", "albums", "--artist", "Nirvana"])
        assert result.exit_code == 0
        assert "Nirvana" in result.output

    def test_filter_nonexistent_artist(self, tmp_db_with_data: Path) -> None:
        result = runner.invoke(app, ["view", "albums", "--artist", "DoesNotExist"])
        assert result.exit_code == 0
        assert "No albums rated" in result.output


class TestViewSongs:
    def test_shows_songs(self, tmp_db_with_data: Path) -> None:
        result = runner.invoke(app, ["view", "songs"])
        assert result.exit_code == 0

    def test_empty_songs(self, tmp_db: Path) -> None:
        result = runner.invoke(app, ["view", "songs"])
        assert result.exit_code == 0


class TestViewStats:
    def test_shows_stats(self, tmp_db_with_data: Path) -> None:
        result = runner.invoke(app, ["view", "stats"])
        assert result.exit_code == 0
        assert "Albums rated" in result.output
        assert "3" in result.output

    def test_empty_stats(self, tmp_db: Path) -> None:
        result = runner.invoke(app, ["view", "stats"])
        assert result.exit_code == 0
        assert "0" in result.output


class TestExportCommands:
    def test_export_csv(self, tmp_db_with_data: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.chdir(tmp_path)
        result = runner.invoke(app, ["export", "csv"])
        assert result.exit_code == 0
        assert "Exported" in result.output
        assert (tmp_path / "musicli_export.csv").exists()

    def test_export_csv_custom_output(self, tmp_db_with_data: Path, tmp_path: Path) -> None:
        dest = tmp_path / "my_export.csv"
        result = runner.invoke(app, ["export", "csv", "--output", str(dest)])
        assert result.exit_code == 0
        assert dest.exists()

    def test_export_markdown(self, tmp_db_with_data: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.chdir(tmp_path)
        result = runner.invoke(app, ["export", "markdown"])
        assert result.exit_code == 0
        assert (tmp_path / "musicli_export.md").exists()

    def test_export_html(self, tmp_db_with_data: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.chdir(tmp_path)
        result = runner.invoke(app, ["export", "html"])
        assert result.exit_code == 0
        assert (tmp_path / "musicli_export.html").exists()

    def test_export_backup(self, tmp_db_with_data: Path) -> None:
        result = runner.invoke(app, ["export", "backup"])
        assert result.exit_code == 0
        assert "Backup saved" in result.output


class TestTierCommands:
    def test_tier_list_empty(self, tmp_db: Path) -> None:
        result = runner.invoke(app, ["tier", "list"])
        assert result.exit_code == 0

    def test_tier_show_empty(self, tmp_db: Path) -> None:
        result = runner.invoke(app, ["tier", "show"])
        assert result.exit_code == 0
        assert "No tier lists" in result.output


class TestConfigCommand:
    def test_config_shows_info(self) -> None:
        result = runner.invoke(app, ["config"])
        assert result.exit_code == 0
        assert "LASTFM_API_KEY" in result.output
        assert "OPENAI_API_KEY" in result.output


class TestAiReviewCommand:
    def test_review_command(self, mock_openai: Any, tmp_db: Path) -> None:
        result = runner.invoke(app, ["ai", "review", "Radiohead", "OK Computer", "--rating", "9"])
        assert result.exit_code == 0
        assert "test AI response" in result.output

    def test_review_with_default_rating(self, mock_openai: Any, tmp_db: Path) -> None:
        result = runner.invoke(app, ["ai", "review", "Nirvana", "Nevermind"])
        assert result.exit_code == 0


class TestAiRecommendCommand:
    def test_recommend_empty_library(self, mock_openai: Any, tmp_db: Path) -> None:
        result = runner.invoke(app, ["ai", "recommend"])
        # Should not crash; might say no albums
        assert result.exit_code == 0

    def test_recommend_with_data(self, mock_openai: Any, tmp_db_with_data: Path) -> None:
        result = runner.invoke(app, ["ai", "recommend"])
        assert result.exit_code == 0


class TestAiDescribeTierCommand:
    def test_describe_existing_tier(self, mock_openai: Any, tmp_db_with_data: Path) -> None:
        result = runner.invoke(app, ["ai", "describe-tier", "Radiohead Ranked"])
        assert result.exit_code == 0

    def test_describe_nonexistent_tier(self, mock_openai: Any, tmp_db_with_data: Path) -> None:
        result = runner.invoke(app, ["ai", "describe-tier", "Does Not Exist"])
        assert result.exit_code != 0


class TestAiTagCommand:
    def test_tag_album(self, mock_openai: Any, tmp_db: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        from musicli.ai import assistant as ai_module

        monkeypatch.setattr(ai_module, "_chat", lambda msgs, local=False: '["indie", "90s", "alt rock"]')
        result = runner.invoke(app, ["ai", "tag", "Radiohead", "OK Computer"])
        assert result.exit_code == 0
        assert "indie" in result.output


class TestAiCompareCommand:
    def test_compare_artists(self, mock_openai: Any, tmp_db_with_data: Path) -> None:
        result = runner.invoke(app, ["ai", "compare", "Radiohead", "Nirvana"])
        assert result.exit_code == 0


class TestAiDigestCommand:
    def test_digest(self, mock_openai: Any, tmp_db_with_data: Path) -> None:
        result = runner.invoke(app, ["ai", "digest"])
        assert result.exit_code == 0

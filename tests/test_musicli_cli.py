"""Tests for the CLI help/version output."""

from typer.testing import CliRunner
from musicli.cli import app

runner = CliRunner()


def test_version_flag() -> None:
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert "musicli" in result.output


def test_config_command() -> None:
    result = runner.invoke(app, ["config"])
    assert result.exit_code == 0
    assert "LASTFM_API_KEY" in result.output

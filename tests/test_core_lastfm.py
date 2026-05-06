"""Tests for musicli.core.lastfm (with mocked network)."""

from __future__ import annotations

import pytest


class TestGetNetwork:
    def test_returns_cached_network(self, mock_lastfm: object) -> None:
        from musicli.core.lastfm import get_network

        net1 = get_network()
        net2 = get_network()
        assert net1 is net2

    def test_raises_systemexit_without_credentials(self, monkeypatch: pytest.MonkeyPatch) -> None:
        from musicli.core import lastfm as lastfm_module

        monkeypatch.setattr(lastfm_module, "_network", None)
        monkeypatch.delenv("LASTFM_API_KEY", raising=False)
        monkeypatch.delenv("LASTFM_API_SECRET", raising=False)

        with pytest.raises(SystemExit):
            lastfm_module.get_network()


class TestGetArtistAlbums:
    def test_filters_null_albums(self, mock_lastfm: object) -> None:
        from musicli.core.lastfm import get_artist_albums

        albums = get_artist_albums("Radiohead")
        assert all("(null)" not in a for a in albums)

    def test_returns_sorted_list(self, mock_lastfm: object) -> None:
        from musicli.core.lastfm import get_artist_albums

        albums = get_artist_albums("Radiohead")
        assert albums == sorted(albums)

    def test_does_not_include_exit(self, mock_lastfm: object) -> None:
        """get_artist_albums should NOT prepend EXIT — that's get_album_list's job."""
        from musicli.core.lastfm import get_artist_albums

        albums = get_artist_albums("Radiohead")
        assert "EXIT" not in albums


class TestGetAlbumCoverUrl:
    def test_returns_url_on_success(self, mock_lastfm: object, monkeypatch: pytest.MonkeyPatch) -> None:
        from unittest.mock import MagicMock
        from musicli.core.lastfm import get_album_cover_url

        mock_resp = MagicMock()
        mock_resp.status_code = 200
        monkeypatch.setattr("httpx.get", lambda *a, **kw: mock_resp)

        url = get_album_cover_url("Radiohead", "OK Computer")
        assert url == "https://example.com/cover.jpg"

    def test_returns_placeholder_on_http_failure(self, mock_lastfm: object, monkeypatch: pytest.MonkeyPatch) -> None:
        from musicli.core.lastfm import get_album_cover_url

        monkeypatch.setattr("httpx.get", lambda *a, **kw: (_ for _ in ()).throw(Exception("timeout")))

        url = get_album_cover_url("Radiohead", "OK Computer")
        assert "mp3tag" in url or url.startswith("https://")


class TestResetNetwork:
    def test_resets_to_none(self, mock_lastfm: object) -> None:
        from musicli.core import lastfm as lastfm_module
        from musicli.core.lastfm import get_network, reset_network

        _ = get_network()
        reset_network()
        assert lastfm_module._network is None

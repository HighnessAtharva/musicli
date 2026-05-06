"""Tests for musicli.ai.assistant (all calls mocked)."""

from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock, patch

import pytest


@pytest.fixture
def canned_chat(monkeypatch: pytest.MonkeyPatch) -> None:
    """Replace _chat with a function that returns a canned string."""
    from musicli.ai import assistant as ai_module

    monkeypatch.setattr(ai_module, "_chat", lambda msgs, local=False: "AI response text.")


class TestGenerateReview:
    def test_returns_string(self, canned_chat: None) -> None:
        from musicli.ai.assistant import generate_review

        result = generate_review("Radiohead", "OK Computer", 10)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_passes_rating_in_prompt(self, monkeypatch: pytest.MonkeyPatch) -> None:
        from musicli.ai import assistant as ai_module

        captured: list[Any] = []
        monkeypatch.setattr(ai_module, "_chat", lambda msgs, local=False: captured.append(msgs) or "x")
        from musicli.ai.assistant import generate_review

        generate_review("Radiohead", "OK Computer", 8)
        assert any("8/10" in str(m) for m in captured[0])


class TestRecommend:
    def test_empty_library_returns_message(self, canned_chat: None) -> None:
        from musicli.ai.assistant import recommend

        result = recommend({"album_ratings": [], "song_ratings": [], "tier_lists": []})
        assert "haven't rated" in result

    def test_with_data_calls_chat(self, canned_chat: None, sample_db: dict[str, Any]) -> None:
        from musicli.ai.assistant import recommend

        result = recommend(sample_db)
        assert isinstance(result, str)


class TestDescribeTier:
    def test_empty_tier_returns_message(self, canned_chat: None) -> None:
        from musicli.ai.assistant import describe_tier

        tier_data = {
            "tier_list_name": "Test",
            "artist": "Radiohead",
            "s_tier": [],
            "a_tier": [],
            "b_tier": [],
            "c_tier": [],
            "d_tier": [],
            "e_tier": [],
        }
        result = describe_tier(tier_data)
        assert "empty" in result.lower()

    def test_with_albums_calls_chat(self, canned_chat: None, sample_db: dict[str, Any]) -> None:
        from musicli.ai.assistant import describe_tier

        tl = sample_db["tier_lists"][0]
        result = describe_tier(tl)
        assert isinstance(result, str)


class TestCompareArtists:
    def test_with_both_rated(self, canned_chat: None, sample_db: dict[str, Any]) -> None:
        from musicli.ai.assistant import compare_artists

        result = compare_artists("Radiohead", "Nirvana", sample_db)
        assert isinstance(result, str)

    def test_with_unrated_artist(self, canned_chat: None, sample_db: dict[str, Any]) -> None:
        from musicli.ai.assistant import compare_artists

        result = compare_artists("Radiohead", "Unknown Artist", sample_db)
        assert isinstance(result, str)


class TestDigest:
    def test_generates_text(self, canned_chat: None, sample_db: dict[str, Any]) -> None:
        from musicli.ai.assistant import digest

        result = digest(sample_db)
        assert isinstance(result, str)


class TestChatWithData:
    def test_returns_response(self, canned_chat: None, sample_db: dict[str, Any]) -> None:
        from musicli.ai.assistant import chat_with_data

        result = chat_with_data("What are my top albums?", sample_db)
        assert isinstance(result, str)

    def test_truncates_large_library(self, canned_chat: None) -> None:
        """Should not raise even with a very large data set."""
        from musicli.ai.assistant import chat_with_data

        large_data = {
            "album_ratings": [
                {"artist": "A", "album": f"Album {i}", "album_rating": 7, "review": "x" * 200, "track_ratings": []}
                for i in range(500)
            ],
            "song_ratings": [],
            "tier_lists": [],
        }
        result = chat_with_data("Tell me about my library", large_data)
        assert isinstance(result, str)


class TestTagAlbum:
    def test_returns_list(self, monkeypatch: pytest.MonkeyPatch) -> None:
        from musicli.ai import assistant as ai_module

        monkeypatch.setattr(
            ai_module,
            "_chat",
            lambda msgs, local=False: '["indie rock", "90s", "alternative", "melancholic"]',
        )
        from musicli.ai.assistant import tag_album

        tags = tag_album("Radiohead", "OK Computer")
        assert isinstance(tags, list)
        assert len(tags) > 0
        assert "indie rock" in tags

    def test_handles_malformed_json(self, monkeypatch: pytest.MonkeyPatch) -> None:
        from musicli.ai import assistant as ai_module

        monkeypatch.setattr(ai_module, "_chat", lambda msgs, local=False: "indie, 90s, alt")
        from musicli.ai.assistant import tag_album

        tags = tag_album("A", "B")
        assert isinstance(tags, list)


class TestGetClient:
    def test_raises_without_openai_installed(self, monkeypatch: pytest.MonkeyPatch) -> None:
        import builtins

        real_import = builtins.__import__

        def mock_import(name: str, *args: Any, **kwargs: Any) -> Any:
            if name == "openai":
                raise ImportError("No module named 'openai'")
            return real_import(name, *args, **kwargs)

        monkeypatch.setattr(builtins, "__import__", mock_import)
        from musicli.ai import assistant as ai_module

        # Reset module-level cache
        with pytest.raises(SystemExit):
            ai_module._get_client()

    def test_raises_without_api_key(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)

        with pytest.raises(SystemExit):
            from musicli.ai.assistant import _get_client

            _get_client(local=False)

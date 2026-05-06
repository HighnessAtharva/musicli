"""AI-powered music assistant for musicli.

Requires ``pip install musicli[ai]`` (i.e. the ``openai`` package).

All functions read ``OPENAI_API_KEY`` from the environment (or a ``.env`` file).
Pass ``local=True`` / set ``OLLAMA_BASE_URL`` to use a local Ollama server
instead of the OpenAI API.
"""

from __future__ import annotations

import json
import os
from typing import Any

from rich.markdown import Markdown
from rich.panel import Panel

from musicli.ui.display import console

_OLLAMA_DEFAULT_BASE = "http://localhost:11434/v1"
_OLLAMA_DEFAULT_MODEL = "llama3"
_OPENAI_DEFAULT_MODEL = "gpt-4o-mini"


def _get_client(local: bool = False) -> Any:
    """Return an OpenAI-compatible client.

    Args:
        local: If ``True``, connect to a local Ollama server instead of OpenAI.

    Returns:
        An ``openai.OpenAI`` client instance.

    Raises:
        SystemExit: If ``openai`` is not installed or credentials are missing.
    """
    try:
        import openai
    except ImportError:
        console.print(
            Panel(
                "[bold red]❌ The AI features require the openai package.[/bold red]\n\n"
                "Install it with: [bold]pip install musicli\\[ai\\][/bold]",
                border_style="red",
            )
        )
        raise SystemExit(1)

    try:
        from dotenv import load_dotenv

        load_dotenv()
    except ImportError:
        pass

    if local:
        base_url = os.environ.get("OLLAMA_BASE_URL", _OLLAMA_DEFAULT_BASE)
        return openai.OpenAI(api_key="ollama", base_url=base_url)

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        console.print(
            Panel(
                "[bold red]❌ OPENAI_API_KEY not set.[/bold red]\n\n"
                "Add it to your environment or a [bold].env[/bold] file:\n"
                "  [cyan]OPENAI_API_KEY=sk-...[/cyan]\n\n"
                "Or use [bold]--local[/bold] to run with a local Ollama model.",
                border_style="red",
            )
        )
        raise SystemExit(1)

    return openai.OpenAI(api_key=api_key)


def _chat(messages: list[dict[str, str]], local: bool = False) -> str:
    """Send a chat completion request and return the text response.

    Args:
        messages: A list of ``{"role": ..., "content": ...}`` dicts.
        local: Route request to local Ollama if ``True``.

    Returns:
        The assistant's response as a string.
    """
    client = _get_client(local=local)
    model = _OLLAMA_DEFAULT_MODEL if local else _OPENAI_DEFAULT_MODEL
    response = client.chat.completions.create(model=model, messages=messages)
    return response.choices[0].message.content or ""


def generate_review(
    artist: str, album: str, rating: int, local: bool = False
) -> str:
    """Generate an AI critic-style review for an album.

    The review is contextualised by the user's personal rating so it
    reads like a personalised critic take, not a generic summary.

    Args:
        artist: Artist name.
        album: Album title.
        rating: The user's 1–10 rating.
        local: Use local Ollama model if ``True``.

    Returns:
        A multi-paragraph review string.
    """
    prompt = (
        f"You are a music critic writing for a high-quality music journal.\n\n"
        f"The user rated '{album}' by {artist} a {rating}/10.\n"
        f"Write a 2–3 paragraph review that justifies this rating. Be specific about "
        f"the album's production, lyrics, themes, and cultural impact. "
        f"Sound genuine and opinionated, not like a Wikipedia summary."
    )
    messages = [
        {"role": "system", "content": "You are a deeply knowledgeable music critic."},
        {"role": "user", "content": prompt},
    ]
    return _chat(messages, local=local)


def recommend(data: dict[str, Any], local: bool = False) -> str:
    """Generate personalised album recommendations based on ratings.

    Args:
        data: The full musicli database dictionary.
        local: Use local Ollama model if ``True``.

    Returns:
        A recommendation text string.
    """
    album_ratings = data.get("album_ratings", [])
    if not album_ratings:
        return "You haven't rated any albums yet. Rate some albums first!"

    # Build a compact summary for the prompt (top 10 by rating)
    top = sorted(album_ratings, key=lambda x: -x.get("album_rating", 0))[:10]
    summary = "\n".join(
        f"- {a['artist']} — {a['album']} ({a['album_rating']}/10)"
        for a in top
    )

    prompt = (
        f"Here are some albums the user has rated highly:\n{summary}\n\n"
        f"Based on this taste profile, recommend 5–7 albums they might love "
        f"that aren't already in the list. For each recommendation give a "
        f"one-sentence reason why it matches their taste."
    )
    messages = [
        {
            "role": "system",
            "content": "You are a music recommendation engine with encyclopaedic knowledge.",
        },
        {"role": "user", "content": prompt},
    ]
    return _chat(messages, local=local)


def describe_tier(tier_data: dict[str, Any], local: bool = False) -> str:
    """Generate an AI narrative description of a tier list.

    Args:
        tier_data: A single tier list entry from the database.
        local: Use local Ollama model if ``True``.

    Returns:
        A descriptive analysis of the tier list.
    """
    artist = tier_data.get("artist", "Unknown Artist")
    name = tier_data.get("tier_list_name", "")

    tier_summary_parts = []
    for tier_key in ("s_tier", "a_tier", "b_tier", "c_tier", "d_tier", "e_tier"):
        albums = tier_data.get(tier_key, [])
        if albums:
            label = tier_key.replace("_tier", "").upper()
            album_names = ", ".join(a.get("album", "") for a in albums)
            tier_summary_parts.append(f"{label}: {album_names}")

    if not tier_summary_parts:
        return "This tier list is empty."

    tier_summary = "\n".join(tier_summary_parts)

    prompt = (
        f"The user created a tier list called '{name}' for {artist}:\n\n"
        f"{tier_summary}\n\n"
        f"Analyse what this tier list reveals about the user's taste. "
        f"What patterns do you notice? What does the S tier reveal about what they "
        f"value most in music? Keep it insightful and conversational, 2–3 paragraphs."
    )
    messages = [
        {"role": "system", "content": "You are a music psychology and taste analyst."},
        {"role": "user", "content": prompt},
    ]
    return _chat(messages, local=local)


def compare_artists(
    artist1: str,
    artist2: str,
    data: dict[str, Any],
    local: bool = False,
) -> str:
    """Compare two artists based on the user's own ratings.

    Args:
        artist1: First artist name.
        artist2: Second artist name.
        data: The full musicli database dictionary.
        local: Use local Ollama model if ``True``.

    Returns:
        A comparative analysis string.
    """
    def _artist_summary(artist: str) -> str:
        albums = [
            a for a in data.get("album_ratings", [])
            if a.get("artist", "").lower() == artist.lower()
        ]
        if not albums:
            return f"No ratings for {artist}."
        return "\n".join(
            f"  - {a['album']} ({a['album_rating']}/10)"
            for a in sorted(albums, key=lambda x: -x.get("album_rating", 0))
        )

    summary1 = _artist_summary(artist1)
    summary2 = _artist_summary(artist2)

    prompt = (
        f"Compare the user's relationship with two artists based on their ratings.\n\n"
        f"{artist1}:\n{summary1}\n\n{artist2}:\n{summary2}\n\n"
        f"Discuss: similarities and differences in the artists' styles, "
        f"what the ratings reveal about the user's preferences, "
        f"and which artist seems to resonate more and why. 2–3 paragraphs."
    )
    messages = [
        {"role": "system", "content": "You are a knowledgeable music analyst."},
        {"role": "user", "content": prompt},
    ]
    return _chat(messages, local=local)


def digest(data: dict[str, Any], period: str = "all time", local: bool = False) -> str:
    """Generate a digest/summary of the user's listening stats and trends.

    Args:
        data: The full musicli database dictionary.
        period: A time period description (e.g. ``"this month"``).
        local: Use local Ollama model if ``True``.

    Returns:
        A written digest string.
    """
    from musicli.core.stats import compute_stats

    stats = compute_stats(data)
    top_album = stats.get("top_album")
    top_str = ""
    if top_album:
        top_str = (
            f"Their highest-rated album is {top_album.get('artist')} — "
            f"{top_album.get('album')} ({top_album.get('album_rating')}/10)."
        )

    prompt = (
        f"Write a friendly music listening digest for a user ({period}).\n\n"
        f"Stats:\n"
        f"- Albums rated: {stats['album_count']} (avg {stats['avg_album_rating']:.1f}/10)\n"
        f"- Tracks rated: {stats['track_count']} (avg {stats['avg_track_rating']:.1f}/10)\n"
        f"- Tier lists: {stats['tier_count']}\n"
        f"- Artists: {', '.join(stats['artists'][:8])}\n"
        f"{top_str}\n\n"
        f"Write a warm, personalised 2-paragraph summary. Celebrate their taste, "
        f"note any patterns, and encourage them to keep rating music."
    )
    messages = [
        {"role": "system", "content": "You are a friendly music journal assistant."},
        {"role": "user", "content": prompt},
    ]
    return _chat(messages, local=local)


def chat_with_data(user_message: str, data: dict[str, Any], local: bool = False) -> str:
    """Answer a free-form question about the user's music library.

    This implements a simple RAG pattern — the database is serialised as
    context and prepended to the system prompt.

    Args:
        user_message: The user's question or message.
        data: The full musicli database dictionary.
        local: Use local Ollama model if ``True``.

    Returns:
        The assistant's response string.
    """
    # Build a compact JSON context to stay within token limits
    compact: dict[str, Any] = {
        "albums": [
            {
                "artist": a.get("artist"),
                "album": a.get("album"),
                "rating": a.get("album_rating"),
                "review": (a.get("review") or "")[:120],
            }
            for a in data.get("album_ratings", [])
        ],
        "songs": [
            {
                "artist": s.get("artist"),
                "track": s.get("track"),
                "rating": s.get("track_rating"),
            }
            for s in data.get("song_ratings", [])
        ],
        "tier_lists": [
            tl.get("tier_list_name") for tl in data.get("tier_lists", [])
        ],
    }
    context = json.dumps(compact, ensure_ascii=False)[:8000]  # hard cap

    system = (
        "You are a personal music assistant. The user's rated music library is provided "
        "as JSON context. Answer questions about their library, give recommendations, "
        "or discuss music taste. Be concise and friendly.\n\n"
        f"USER LIBRARY:\n{context}"
    )
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": user_message},
    ]
    return _chat(messages, local=local)


def tag_album(artist: str, album: str, local: bool = False) -> list[str]:
    """Generate mood/genre/era tags for an album using AI.

    Args:
        artist: Artist name.
        album: Album title.
        local: Use local Ollama model if ``True``.

    Returns:
        A list of tag strings (e.g. ``["indie rock", "90s", "melancholic"]``).
    """
    prompt = (
        f"Generate 5–8 concise tags for the album '{album}' by {artist}. "
        f"Tags should cover genre, mood, era, and themes. "
        f"Reply with ONLY a JSON array of strings, e.g. [\"indie\", \"90s\"]."
    )
    messages = [
        {"role": "system", "content": "You are a music metadata expert. Reply with only JSON."},
        {"role": "user", "content": prompt},
    ]
    raw = _chat(messages, local=local).strip()
    # Parse the JSON array from the response
    try:
        start = raw.index("[")
        end = raw.rindex("]") + 1
        return json.loads(raw[start:end])
    except (ValueError, json.JSONDecodeError):
        return [t.strip().strip('"') for t in raw.split(",") if t.strip()]

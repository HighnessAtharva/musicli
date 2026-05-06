"""Backward-compatibility shim for musicli.

All public symbols are now provided by the sub-packages.  This module
re-exports them so that any code that did ``from musicli import musicli``
or ``import musicli.musicli`` continues to work.

For new code use the sub-packages directly:
  - musicli.cli          — Typer CLI app
  - musicli.core.lastfm  — Last.fm helpers
  - musicli.core.ratings — rating flows
  - musicli.core.tier    — tier list logic
  - musicli.core.stats   — statistics
  - musicli.storage.db   — JSON persistence
  - musicli.ui.display   — rich display helpers
  - musicli.ai.assistant — AI features
"""

from __future__ import annotations

# Storage
from musicli.storage.db import (
    export_csv,
    export_html,
    export_markdown,
    get_data_dir,
    get_db_path,
    get_output_dir,
    load_db,
    migrate_legacy_db,
    save_db,
)

# Backward-compat aliases used by existing tests
def load_or_create_json() -> None:
    """Load or create the database (legacy API)."""
    load_db()


# Last.fm helpers
from musicli.core.lastfm import (
    get_album_cover_url,
    get_album_tracks,
    get_artist_albums,
    get_network,
    reset_network,
    search_track,
)

# Alias used by legacy tests that reference ``musicli.network``
try:
    network = get_network()
except SystemExit:
    network = None  # type: ignore[assignment]

def get_album_list(artist: str) -> list[str]:
    """Return sorted album list with EXIT prepended (legacy API)."""
    from rich.panel import Panel
    from musicli.ui.display import console
    albums = get_artist_albums(artist)
    console.print(Panel(
        f"[b cyan]Found {len(albums)} albums for this artist.[/b cyan]",
        border_style="cyan",
    ))
    albums.insert(0, "EXIT")
    return albums


# Rating flows
from musicli.core.ratings import (
    add_album_manually,
    rate_album_tracks,
    rate_by_album,
    rate_by_song,
    rate_single_song,
)

# Tier list
from musicli.core.tier import (
    create_tier_list,
    image_generator,
    see_tier_lists,
)

# Stats
from musicli.core.stats import compute_stats

# UI helpers
from musicli.ui.display import (
    console,
    print_albums_table,
    print_banner,
    print_songs_table,
    print_stats,
    print_tier_list_images,
)

# Legacy aliases
def see_albums_rated() -> None:
    """Show all rated albums (legacy wrapper)."""
    data = load_db()
    print_albums_table(data)


def see_songs_rated() -> None:
    """Show all rated songs (legacy wrapper)."""
    data = load_db()
    print_songs_table(data)


def show_stats() -> None:
    """Show stats panel (legacy wrapper)."""
    data = load_db()
    print_stats(data)


def show_tier_list_images() -> None:
    """List tier list images (legacy wrapper)."""
    print_tier_list_images(get_output_dir())


# CLI entry point
from musicli.cli import app, start

__all__ = [
    "load_or_create_json",
    "get_album_list",
    "get_album_cover_url",
    "rate_by_album",
    "rate_by_song",
    "see_albums_rated",
    "see_songs_rated",
    "create_tier_list",
    "see_tier_lists",
    "image_generator",
    "show_stats",
    "show_tier_list_images",
    "start",
    "network",
]

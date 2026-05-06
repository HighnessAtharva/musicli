"""Interactive rating flows for albums and songs."""

from __future__ import annotations

from datetime import datetime
from typing import Any

import questionary
from rich.panel import Panel

from musicli.core.lastfm import get_album_cover_url, get_album_tracks, get_artist_albums, search_track
from musicli.storage.db import load_db, save_db
from musicli.ui.display import console, spinner

_STAR_OPTIONS = ["★" * n for n in range(1, 11)]


def _pick_rating(prompt: str) -> tuple[str, int]:
    """Interactively ask the user for a 1-10 star rating.

    Args:
        prompt: The question to display.

    Returns:
        A tuple of ``(star_string, 1-based integer rating)``.
    """
    choice = questionary.select(
        prompt,
        choices=_STAR_OPTIONS,
        use_shortcuts=False,
    ).ask()
    if choice is None:
        raise KeyboardInterrupt
    rating = len(choice)  # number of ★ characters
    return choice, rating


def rate_by_album() -> None:
    """Interactive flow: search for an artist, pick albums, assign ratings."""
    import pylast

    from musicli.ui.display import print_albums_table

    data = load_db()

    console.print(
        Panel(
            "[bold green]Enter an artist to rate their albums[/bold green]",
            title="[bold magenta reverse]RATE BY ALBUM[/bold magenta reverse]",
            border_style="green",
        )
    )

    artist_search = questionary.text("Artist name:").ask()
    if not artist_search:
        return

    try:
        with spinner("Fetching albums from Last.fm…"):
            albums = get_artist_albums(artist_search)

        if not albums:
            console.print(Panel("❌ No albums found for this artist.", style="bold red", border_style="red"))
            return

        console.print(
            Panel(
                f"[bold cyan]Found {len(albums)} albums.[/bold cyan]",
                border_style="cyan",
            )
        )

        choices = albums + ["── EXIT ──"]

        while True:
            selected = questionary.select(
                f"Pick an album to rate ({len(albums)} albums):",
                choices=choices,
            ).ask()
            if selected is None or selected == "── EXIT ──":
                break

            artist, album = selected.split(" - ", maxsplit=1)
            star_str, rating = _pick_rating(f"Rating for {album}?")

            write_review = questionary.confirm(f"Write a review for {album}?", default=False).ask()
            review = ""
            if write_review:
                review = questionary.text("Your review:").ask() or ""

            rating_time = str(datetime.now())

            # Update or insert
            found = False
            for entry in data["album_ratings"]:
                if entry["album"] == album and entry["artist"] == artist:
                    entry["album_rating"] = rating
                    entry["time"] = rating_time
                    if review:
                        entry["review"] = review
                    found = True
                    break

            if not found:
                with spinner("Fetching cover art…"):
                    cover = get_album_cover_url(artist, album)
                data["album_ratings"].append(
                    {
                        "artist": artist,
                        "album": album,
                        "cover": cover,
                        "album_rating": rating,
                        "review": review,
                        "time": rating_time,
                        "track_ratings": [],
                    }
                )

            save_db(data)
            console.print(
                f"🎶 [bold cyan]{artist} — {album}[/bold cyan] rated "
                f"[yellow]{star_str}[/yellow] ([bold]{rating}[/bold]/10)"
            )

    except pylast.PyLastError:
        console.print(Panel("❌ Artist not found on Last.fm.", style="bold red", border_style="red"))
    except KeyboardInterrupt:
        pass


def rate_album_tracks() -> None:
    """Interactive flow: pick an already-rated album and rate its tracks."""
    import pylast

    data = load_db()

    if not data["album_ratings"]:
        console.print(Panel("❌ No albums found. Rate some albums first.", style="bold red", border_style="red"))
        return

    album_choices = sorted(
        f"{a['artist']} - {a['album']}" for a in data["album_ratings"]
    )
    album_choices.append("── EXIT ──")

    selected_album = questionary.select("Select an album to rate its tracks:", choices=album_choices).ask()
    if not selected_album or selected_album == "── EXIT ──":
        return

    artist, album = selected_album.split(" - ", maxsplit=1)

    try:
        with spinner("Fetching track listing…"):
            tracks = get_album_tracks(artist, album)

        if not tracks:
            console.print(Panel("❌ No tracks found for this album.", style="bold red", border_style="red"))
            return

        track_choices = tracks + ["── EXIT ──"]

        while True:
            selected_track = questionary.select("Pick a track to rate:", choices=track_choices).ask()
            if not selected_track or selected_track == "── EXIT ──":
                break

            star_str, rating = _pick_rating(f"Rating for {selected_track}?")

            # Update or insert track rating in the album entry
            for entry in data["album_ratings"]:
                if entry["album"] == album and entry["artist"] == artist:
                    found = False
                    for track in entry["track_ratings"]:
                        if track["track"] == selected_track:
                            track["track_rating"] = rating
                            found = True
                            break
                    if not found:
                        entry["track_ratings"].append(
                            {"track": selected_track, "track_rating": rating}
                        )
                    break

            save_db(data)
            console.print(
                f"🎵 [bold cyan]{artist} — {selected_track}[/bold cyan] rated "
                f"[yellow]{star_str}[/yellow] ([bold]{rating}[/bold]/10)"
            )

    except pylast.PyLastError:
        console.print(Panel("❌ Could not fetch tracks from Last.fm.", style="bold red", border_style="red"))
    except KeyboardInterrupt:
        pass


def rate_single_song() -> None:
    """Interactive flow: search for and rate a standalone song."""
    data = load_db()

    song_name = questionary.text("Song name:").ask()
    if not song_name:
        return
    artist_name = questionary.text("Artist name:").ask()
    if not artist_name:
        return

    with spinner("Searching Last.fm…"):
        track = search_track(artist_name, song_name)

    if track is None:
        console.print(Panel("❌ Song not found on Last.fm.", style="bold red", border_style="red"))
        return

    star_str, rating = _pick_rating(f"Rating for {track.title}?")

    found = False
    for entry in data["song_ratings"]:
        if entry["track"] == track.title and entry["artist"] == track.artist.name:
            entry["track_rating"] = rating
            found = True
            break

    if not found:
        data["song_ratings"].append(
            {"track": track.title, "artist": track.artist.name, "track_rating": rating}
        )

    save_db(data)
    console.print(
        f"🎵 [bold cyan]{track.artist.name} — {track.title}[/bold cyan] rated "
        f"[yellow]{star_str}[/yellow] ([bold]{rating}[/bold]/10)"
    )


def rate_by_song() -> None:
    """Interactive flow: choose between rating an album's tracks or a single song."""
    choice = questionary.select(
        "What do you want to rate?",
        choices=["Songs from a rated album", "A standalone song"],
    ).ask()
    if choice is None:
        return
    if "album" in choice:
        rate_album_tracks()
    else:
        rate_single_song()


def add_album_manually(artist: str, album: str, rating: int, review: str = "") -> dict[str, Any]:
    """Add or update an album rating programmatically (non-interactive).

    Useful for scripting and testing.

    Args:
        artist: The artist name.
        album: The album title.
        rating: A 1–10 integer rating.
        review: Optional review text.

    Returns:
        The updated album entry dictionary.
    """
    if not 1 <= rating <= 10:
        raise ValueError(f"Rating must be between 1 and 10, got {rating}")

    data = load_db()
    now = str(datetime.now())

    for entry in data["album_ratings"]:
        if entry["album"] == album and entry["artist"] == artist:
            entry["album_rating"] = rating
            entry["time"] = now
            if review:
                entry["review"] = review
            save_db(data)
            return entry

    new_entry: dict[str, Any] = {
        "artist": artist,
        "album": album,
        "cover": "",
        "album_rating": rating,
        "review": review,
        "time": now,
        "track_ratings": [],
    }
    data["album_ratings"].append(new_entry)
    save_db(data)
    return new_entry

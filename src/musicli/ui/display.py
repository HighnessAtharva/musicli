"""Rich-based terminal UI helpers for musicli."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

console = Console()


def print_banner() -> None:
    """Print the musicli welcome banner."""
    console.print(
        Panel(
            "[bold cyan]🎵  Welcome to musicli 2.0![/bold cyan]\n"
            "[dim]AI-powered music ratings, tier lists, and reviews — from your terminal.[/dim]",
            title="[bold magenta]♪ musicli[/bold magenta]",
            border_style="magenta",
            padding=(1, 4),
        )
    )


def print_separator() -> None:
    """Print a visual separator."""
    console.print(Panel("─" * 60, style="grey50", padding=0))


def spinner(message: str = "Fetching data…") -> Progress:
    """Return a configured rich Progress spinner context manager.

    Usage::

        with spinner("Loading…") as p:
            task = p.add_task("", total=None)
            # … do work …

    Args:
        message: The status message shown next to the spinner.

    Returns:
        A :class:`rich.progress.Progress` instance.
    """
    return Progress(
        SpinnerColumn(),
        TextColumn(f"[bold cyan]{message}[/bold cyan]"),
        transient=True,
    )


def print_albums_table(data: dict[str, Any]) -> None:
    """Print a rich table of all rated albums.

    Args:
        data: The full database dictionary.
    """
    album_ratings = data.get("album_ratings", [])
    if not album_ratings:
        console.print(
            Panel("❌ No albums rated yet.", style="bold red", border_style="red")
        )
        return

    sorted_albums = sorted(album_ratings, key=lambda x: x.get("album", ""))
    table = Table(
        title="🎵 Album Ratings",
        show_header=True,
        header_style="bold magenta",
        box=box.ROUNDED,
        border_style="cyan",
    )
    table.add_column("#", justify="right", style="dim", width=4)
    table.add_column("Artist", style="bold cyan")
    table.add_column("Album", style="white")
    table.add_column("Rating", justify="center", style="yellow")
    table.add_column("Date", style="dim")
    table.add_column("Review", style="italic dim")

    for idx, entry in enumerate(sorted_albums, 1):
        rating = entry.get("album_rating", 0)
        stars = "★" * rating + "☆" * (10 - rating)
        date_raw = entry.get("time", "")
        try:
            date_str = datetime.strptime(date_raw[:10], "%Y-%m-%d").strftime("%b %d, %Y")
        except (ValueError, TypeError):
            date_str = date_raw[:10] if date_raw else "—"
        review = (entry.get("review", "") or "")[:60]
        if len(entry.get("review", "") or "") > 60:
            review += "…"
        table.add_row(str(idx), entry.get("artist", ""), entry.get("album", ""), stars, date_str, review)

    console.print(table)


def print_songs_table(data: dict[str, Any]) -> None:
    """Print rich tables for single-song and album-track ratings.

    Args:
        data: The full database dictionary.
    """
    # Singles
    song_ratings = data.get("song_ratings", [])
    if song_ratings:
        table = Table(
            title="🎤 Song Ratings (Singles)",
            show_header=True,
            header_style="bold magenta",
            box=box.ROUNDED,
            border_style="cyan",
        )
        table.add_column("Artist", style="bold cyan")
        table.add_column("Song", style="white")
        table.add_column("Rating", justify="center", style="yellow")

        for entry in sorted(song_ratings, key=lambda x: x.get("track", "")):
            rating = entry.get("track_rating", 0)
            stars = "★" * rating + "☆" * (10 - rating)
            table.add_row(entry.get("artist", ""), entry.get("track", ""), stars)

        console.print(table)
    else:
        console.print(
            Panel("❌ No single songs rated yet.", style="bold red", border_style="red")
        )

    console.print()

    # Album tracks
    has_tracks = any(
        album.get("track_ratings") for album in data.get("album_ratings", [])
    )
    if has_tracks:
        table = Table(
            title="🎼 Track Ratings (From Albums)",
            show_header=True,
            header_style="bold magenta",
            box=box.ROUNDED,
            border_style="cyan",
        )
        table.add_column("Artist", style="bold cyan")
        table.add_column("Album", style="white")
        table.add_column("Track", style="white")
        table.add_column("Rating", justify="center", style="yellow")

        for album in sorted(data.get("album_ratings", []), key=lambda x: x.get("album", "")):
            for track in album.get("track_ratings", []):
                rating = track.get("track_rating", 0)
                stars = "★" * rating + "☆" * (10 - rating)
                table.add_row(
                    album.get("artist", ""),
                    album.get("album", ""),
                    track.get("track", ""),
                    stars,
                )

        console.print(table)
    else:
        console.print(
            Panel(
                "❌ No album tracks rated yet.", style="bold red", border_style="red"
            )
        )


def print_stats(data: dict[str, Any]) -> None:
    """Print a summary statistics panel.

    Args:
        data: The full database dictionary.
    """
    album_ratings = data.get("album_ratings", [])
    song_ratings = data.get("song_ratings", [])
    tier_lists = data.get("tier_lists", [])

    album_count = len(album_ratings)
    song_count = len(song_ratings)
    tier_count = len(tier_lists)

    # Averages
    avg_album = (
        sum(a.get("album_rating", 0) for a in album_ratings) / album_count
        if album_count
        else 0
    )
    all_track_ratings = [
        t.get("track_rating", 0)
        for a in album_ratings
        for t in a.get("track_ratings", [])
    ]
    all_track_ratings += [s.get("track_rating", 0) for s in song_ratings]
    avg_track = sum(all_track_ratings) / len(all_track_ratings) if all_track_ratings else 0

    # Top rated album
    top_album = (
        max(album_ratings, key=lambda x: x.get("album_rating", 0)) if album_ratings else None
    )

    lines = [
        f"[bold]📀 Albums rated:[/bold]  [cyan]{album_count}[/cyan]  "
        f"(avg [yellow]{avg_album:.1f}[/yellow]/10)",
        f"[bold]🎵 Songs rated:[/bold]   [cyan]{len(all_track_ratings)}[/cyan]  "
        f"(avg [yellow]{avg_track:.1f}[/yellow]/10)",
        f"[bold]🏆 Tier lists:[/bold]    [cyan]{tier_count}[/cyan]",
    ]
    if top_album:
        lines.append(
            f"\n[bold]🥇 Top album:[/bold] "
            f"[cyan]{top_album.get('artist')} — {top_album.get('album')}[/cyan] "
            f"([yellow]{top_album.get('album_rating')}[/yellow]/10)"
        )

    console.print(
        Panel(
            "\n".join(lines),
            title="[bold magenta]📊 Your Stats[/bold magenta]",
            border_style="magenta",
            padding=(1, 4),
        )
    )


def print_tier_list_images(output_dir: Any) -> None:
    """List all tier list PNG images in the output directory.

    Args:
        output_dir: A :class:`pathlib.Path` pointing to the output directory.
    """
    from pathlib import Path

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    images = sorted(f for f in output_path.iterdir() if f.suffix == ".png")

    if not images:
        console.print(
            Panel(
                "No tier list images found.",
                style="bold yellow",
                border_style="yellow",
            )
        )
        return

    table = Table(
        title="🖼️  Tier List Images",
        show_header=True,
        header_style="bold magenta",
        box=box.ROUNDED,
    )
    table.add_column("Filename", style="cyan")
    table.add_column("Size", justify="right", style="dim")
    for img in images:
        size_kb = img.stat().st_size // 1024
        table.add_row(img.name, f"{size_kb} KB")

    console.print(table)
    console.print(
        Panel(
            f"[bold cyan]📁 Images saved in:[/bold cyan]\n{output_path}",
            border_style="cyan",
        )
    )

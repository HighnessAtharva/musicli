"""musicli CLI — AI-powered music ratings, tier lists, and reviews from your terminal.

Entry point: ``musicli`` (interactive TUI) or ``musicli <subcommand>``.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Annotated, Optional

import questionary
import typer
from rich.markdown import Markdown
from rich.panel import Panel

from musicli import __version__
from musicli.storage.db import (
    backup_db,
    export_csv,
    export_html,
    export_markdown,
    get_data_dir,
    get_output_dir,
    load_db,
    migrate_legacy_db,
)
from musicli.ui.display import (
    console,
    print_albums_table,
    print_banner,
    print_separator,
    print_songs_table,
    print_stats,
    print_tier_list_images,
)

app = typer.Typer(
    name="musicli",
    help="🎵 AI-powered music ratings, tier lists, and reviews from your terminal.",
    add_completion=True,
    rich_markup_mode="rich",
    no_args_is_help=False,
)

rate_app = typer.Typer(help="Rate albums, tracks, and songs.")
view_app = typer.Typer(help="View your rated music.")
tier_app = typer.Typer(help="Manage tier lists.")
ai_app = typer.Typer(help="AI-powered features (requires OPENAI_API_KEY).")
export_app = typer.Typer(help="Export your ratings.")

app.add_typer(rate_app, name="rate")
app.add_typer(view_app, name="view")
app.add_typer(tier_app, name="tier")
app.add_typer(ai_app, name="ai")
app.add_typer(export_app, name="export")


def _version_callback(value: bool) -> None:
    if value:
        console.print(f"[bold cyan]musicli[/bold cyan] version [bold]{__version__}[/bold]")
        raise typer.Exit()


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    version: Annotated[
        Optional[bool],
        typer.Option("--version", "-v", callback=_version_callback, is_eager=True, help="Show version."),
    ] = None,
) -> None:
    """Launch the interactive TUI when no subcommand is given."""
    if ctx.invoked_subcommand is None:
        _run_interactive_tui()


# ---------------------------------------------------------------------------
# Interactive TUI (default mode)
# ---------------------------------------------------------------------------

def _run_interactive_tui() -> None:
    """Run the full interactive menu-driven TUI."""
    from musicli.core.ratings import rate_by_album, rate_by_song
    from musicli.core.tier import create_tier_list, see_tier_lists

    _check_and_migrate()
    print_banner()

    menu_choices = [
        "⭐  Rate by Album",
        "🎵  Rate Songs",
        "📀  See Albums Rated",
        "🎤  See Songs Rated",
        "🏆  Make a Tier List",
        "🖼️  See Created Tier Lists",
        "📂  Show Tier List Images",
        "📊  Show Stats",
        "🤖  AI Features",
        "💾  Export Data",
        "🚪  EXIT",
    ]

    while True:
        print_separator()
        choice = questionary.select(
            "What do you want to do?",
            choices=menu_choices,
        ).ask()

        if choice is None or "EXIT" in choice:
            console.print(
                Panel(
                    "[bold green]Thanks for using musicli! Keep listening. 🎵[/bold green]",
                    border_style="green",
                )
            )
            break
        elif "Rate by Album" in choice:
            rate_by_album()
        elif "Rate Songs" in choice:
            rate_by_song()
        elif "Albums Rated" in choice:
            data = load_db()
            print_albums_table(data)
        elif "Songs Rated" in choice:
            data = load_db()
            print_songs_table(data)
        elif "Make a Tier List" in choice:
            create_tier_list()
        elif "Created Tier Lists" in choice:
            see_tier_lists()
        elif "Tier List Images" in choice:
            print_tier_list_images(get_output_dir())
        elif "Stats" in choice:
            data = load_db()
            print_stats(data)
        elif "AI Features" in choice:
            _run_ai_submenu()
        elif "Export" in choice:
            _run_export_submenu()


def _run_ai_submenu() -> None:
    """Interactive AI submenu."""
    from musicli.ai.assistant import (
        chat_with_data,
        describe_tier,
        digest,
        generate_review,
        recommend,
        tag_album,
    )

    choices = [
        "📝  Generate album review",
        "💡  Get recommendations",
        "🏆  Describe my tier list",
        "🎤  Compare two artists",
        "📊  Monthly digest",
        "💬  Chat with my library",
        "🏷️  Auto-tag an album",
        "← Back",
    ]
    local = questionary.confirm("Use local Ollama model instead of OpenAI?", default=False).ask() or False
    data = load_db()

    while True:
        choice = questionary.select("AI Features:", choices=choices).ask()
        if choice is None or "Back" in choice:
            break
        elif "review" in choice:
            artist = questionary.text("Artist:").ask() or ""
            album = questionary.text("Album:").ask() or ""
            rating_str = questionary.text("Your rating (1-10):").ask() or "7"
            try:
                rating = int(rating_str)
            except ValueError:
                rating = 7
            console.print(Panel("[cyan]Generating review…[/cyan]", border_style="cyan"))
            text = generate_review(artist, album, rating, local=local)
            console.print(Markdown(text))
        elif "recommendations" in choice:
            console.print(Panel("[cyan]Analysing your taste…[/cyan]", border_style="cyan"))
            text = recommend(data, local=local)
            console.print(Markdown(text))
        elif "tier list" in choice:
            tier_lists = data.get("tier_lists", [])
            if not tier_lists:
                console.print(Panel("❌ No tier lists yet.", style="bold red", border_style="red"))
                continue
            names = [tl["tier_list_name"] for tl in tier_lists]
            selected = questionary.select("Select tier list:", choices=names).ask()
            tl = next(t for t in tier_lists if t["tier_list_name"] == selected)
            text = describe_tier(tl, local=local)
            console.print(Markdown(text))
        elif "Compare" in choice:
            a1 = questionary.text("Artist 1:").ask() or ""
            a2 = questionary.text("Artist 2:").ask() or ""
            text = compare_artists(a1, a2, data, local=local)  # type: ignore[name-defined]
            console.print(Markdown(text))
        elif "digest" in choice:
            text = digest(data, local=local)
            console.print(Markdown(text))
        elif "Chat" in choice:
            msg = questionary.text("Ask anything about your library:").ask() or ""
            text = chat_with_data(msg, data, local=local)
            console.print(Markdown(text))
        elif "tag" in choice:
            artist = questionary.text("Artist:").ask() or ""
            album = questionary.text("Album:").ask() or ""
            tags = tag_album(artist, album, local=local)
            console.print(Panel(f"Tags: [cyan]{', '.join(tags)}[/cyan]", border_style="cyan"))


def _run_export_submenu() -> None:
    """Interactive export submenu."""
    choices = ["CSV", "Markdown", "HTML", "Backup (zip)", "← Back"]
    fmt = questionary.select("Export format:", choices=choices).ask()
    if fmt is None or "Back" in fmt:
        return
    data = load_db()
    out_dir = Path.cwd()
    if fmt == "CSV":
        dest = out_dir / "musicli_export.csv"
        export_csv(data, dest)
        console.print(f"✅ Exported CSV → [cyan]{dest}[/cyan]")
    elif fmt == "Markdown":
        dest = out_dir / "musicli_export.md"
        export_markdown(data, dest)
        console.print(f"✅ Exported Markdown → [cyan]{dest}[/cyan]")
    elif fmt == "HTML":
        dest = out_dir / "musicli_export.html"
        export_html(data, dest)
        console.print(f"✅ Exported HTML → [cyan]{dest}[/cyan]")
    elif "Backup" in fmt:
        path = backup_db()
        console.print(f"✅ Backup saved → [cyan]{path}[/cyan]")


def _check_and_migrate() -> None:
    """Silently migrate a legacy albums.json if found."""
    if migrate_legacy_db():
        console.print(
            Panel(
                "📦 Found a legacy [bold]./albums.json[/bold] and migrated it to:\n"
                f"[cyan]{get_data_dir()}[/cyan]",
                border_style="cyan",
            )
        )


# ---------------------------------------------------------------------------
# rate subcommands
# ---------------------------------------------------------------------------


@rate_app.command("album")
def rate_album_cmd() -> None:
    """Rate albums for an artist interactively."""
    from musicli.core.ratings import rate_by_album

    rate_by_album()


@rate_app.command("song")
def rate_song_cmd() -> None:
    """Rate a standalone song."""
    from musicli.core.ratings import rate_single_song

    rate_single_song()


@rate_app.command("tracks")
def rate_tracks_cmd() -> None:
    """Rate individual tracks from a rated album."""
    from musicli.core.ratings import rate_album_tracks

    rate_album_tracks()


# ---------------------------------------------------------------------------
# view subcommands
# ---------------------------------------------------------------------------


@view_app.command("albums")
def view_albums_cmd(
    sort: Annotated[str, typer.Option("--sort", help="Sort by: name|rating|date")] = "name",
    artist: Annotated[Optional[str], typer.Option("--artist", help="Filter by artist name.")] = None,
) -> None:
    """Show a table of all rated albums."""
    data = load_db()
    album_ratings = data.get("album_ratings", [])

    if artist:
        album_ratings = [a for a in album_ratings if artist.lower() in a.get("artist", "").lower()]
        data = {**data, "album_ratings": album_ratings}

    sort_keys = {
        "name": lambda x: x.get("album", ""),
        "rating": lambda x: -x.get("album_rating", 0),
        "date": lambda x: x.get("time", ""),
    }
    key_fn = sort_keys.get(sort, sort_keys["name"])
    data["album_ratings"] = sorted(album_ratings, key=key_fn)

    print_albums_table(data)


@view_app.command("songs")
def view_songs_cmd() -> None:
    """Show tables of all rated songs."""
    data = load_db()
    print_songs_table(data)


@view_app.command("stats")
def view_stats_cmd() -> None:
    """Show statistics for your music collection."""
    data = load_db()
    print_stats(data)


# ---------------------------------------------------------------------------
# tier subcommands
# ---------------------------------------------------------------------------


@tier_app.command("create")
def tier_create_cmd() -> None:
    """Interactively create a tier list for an artist."""
    from musicli.core.tier import create_tier_list

    create_tier_list()


@tier_app.command("show")
def tier_show_cmd() -> None:
    """Render all saved tier lists as PNG images."""
    from musicli.core.tier import see_tier_lists

    see_tier_lists()


@tier_app.command("list")
def tier_list_cmd() -> None:
    """List all saved tier list image files."""
    print_tier_list_images(get_output_dir())


# ---------------------------------------------------------------------------
# export subcommands
# ---------------------------------------------------------------------------


@export_app.command("csv")
def export_csv_cmd(
    output: Annotated[Path, typer.Option("--output", "-o", help="Output file path.")] = Path("musicli_export.csv"),
) -> None:
    """Export ratings to CSV."""
    data = load_db()
    export_csv(data, output)
    console.print(f"✅ Exported → [cyan]{output}[/cyan]")


@export_app.command("markdown")
def export_md_cmd(
    output: Annotated[Path, typer.Option("--output", "-o", help="Output file path.")] = Path("musicli_export.md"),
) -> None:
    """Export ratings to a Markdown document."""
    data = load_db()
    export_markdown(data, output)
    console.print(f"✅ Exported → [cyan]{output}[/cyan]")


@export_app.command("html")
def export_html_cmd(
    output: Annotated[Path, typer.Option("--output", "-o", help="Output file path.")] = Path("musicli_export.html"),
) -> None:
    """Export ratings to a self-contained HTML page."""
    data = load_db()
    export_html(data, output)
    console.print(f"✅ Exported → [cyan]{output}[/cyan]")


@export_app.command("backup")
def export_backup_cmd() -> None:
    """Create a timestamped zip backup of your data directory."""
    path = backup_db()
    console.print(f"✅ Backup saved → [cyan]{path}[/cyan]")


# ---------------------------------------------------------------------------
# ai subcommands
# ---------------------------------------------------------------------------


@ai_app.command("review")
def ai_review_cmd(
    artist: Annotated[str, typer.Argument(help="Artist name.")],
    album: Annotated[str, typer.Argument(help="Album title.")],
    rating: Annotated[int, typer.Option("--rating", "-r", help="Your rating (1-10).")] = 8,
    local: Annotated[bool, typer.Option("--local", help="Use local Ollama model.")] = False,
) -> None:
    """Generate an AI critic review for an album."""
    from musicli.ai.assistant import generate_review

    console.print(Panel("[cyan]Generating review…[/cyan]", border_style="cyan"))
    text = generate_review(artist, album, rating, local=local)
    console.print(Markdown(text))


@ai_app.command("recommend")
def ai_recommend_cmd(
    local: Annotated[bool, typer.Option("--local", help="Use local Ollama model.")] = False,
) -> None:
    """Get personalised album recommendations based on your ratings."""
    from musicli.ai.assistant import recommend

    data = load_db()
    console.print(Panel("[cyan]Analysing your taste…[/cyan]", border_style="cyan"))
    text = recommend(data, local=local)
    console.print(Markdown(text))


@ai_app.command("describe-tier")
def ai_describe_tier_cmd(
    name: Annotated[str, typer.Argument(help="Tier list name.")],
    local: Annotated[bool, typer.Option("--local", help="Use local Ollama model.")] = False,
) -> None:
    """Get an AI description of a saved tier list."""
    from musicli.ai.assistant import describe_tier

    data = load_db()
    tl = next((t for t in data.get("tier_lists", []) if t["tier_list_name"] == name), None)
    if not tl:
        console.print(Panel(f"❌ Tier list '{name}' not found.", style="bold red", border_style="red"))
        raise typer.Exit(1)
    text = describe_tier(tl, local=local)
    console.print(Markdown(text))


@ai_app.command("compare")
def ai_compare_cmd(
    artist1: Annotated[str, typer.Argument(help="First artist.")],
    artist2: Annotated[str, typer.Argument(help="Second artist.")],
    local: Annotated[bool, typer.Option("--local", help="Use local Ollama model.")] = False,
) -> None:
    """Compare two artists based on your ratings."""
    from musicli.ai.assistant import compare_artists

    data = load_db()
    text = compare_artists(artist1, artist2, data, local=local)
    console.print(Markdown(text))


@ai_app.command("digest")
def ai_digest_cmd(
    local: Annotated[bool, typer.Option("--local", help="Use local Ollama model.")] = False,
) -> None:
    """Generate an AI digest of your listening habits."""
    from musicli.ai.assistant import digest

    data = load_db()
    text = digest(data, local=local)
    console.print(Markdown(text))


@ai_app.command("chat")
def ai_chat_cmd(
    local: Annotated[bool, typer.Option("--local", help="Use local Ollama model.")] = False,
) -> None:
    """Start an interactive chat about your music library."""
    from musicli.ai.assistant import chat_with_data

    data = load_db()
    console.print(
        Panel(
            "[bold cyan]musicli AI Chat[/bold cyan]\n"
            "[dim]Ask anything about your music library. Type 'exit' to quit.[/dim]",
            border_style="cyan",
        )
    )
    while True:
        try:
            msg = questionary.text("You:").ask()
        except KeyboardInterrupt:
            break
        if not msg or msg.lower() in {"exit", "quit", "q"}:
            break
        response = chat_with_data(msg, data, local=local)
        console.print(Panel(Markdown(response), title="[bold cyan]musicli AI[/bold cyan]", border_style="cyan"))


@ai_app.command("tag")
def ai_tag_cmd(
    artist: Annotated[str, typer.Argument(help="Artist name.")],
    album: Annotated[str, typer.Argument(help="Album title.")],
    local: Annotated[bool, typer.Option("--local", help="Use local Ollama model.")] = False,
) -> None:
    """Auto-tag an album with mood, genre, and era labels."""
    from musicli.ai.assistant import tag_album

    tags = tag_album(artist, album, local=local)
    console.print(Panel(f"[cyan]{', '.join(tags)}[/cyan]", title=f"Tags for {artist} — {album}", border_style="cyan"))


# ---------------------------------------------------------------------------
# config command
# ---------------------------------------------------------------------------


@app.command("config")
def config_cmd() -> None:
    """Configure API keys and settings interactively."""
    console.print(
        Panel(
            "[bold cyan]musicli Configuration[/bold cyan]\n\n"
            "API keys can be set via environment variables or a [bold].env[/bold] file.\n\n"
            "[bold]Last.fm (required):[/bold]\n"
            "  export LASTFM_API_KEY=<key>\n"
            "  export LASTFM_API_SECRET=<secret>\n"
            "  Get a key: https://www.last.fm/api/account/create\n\n"
            "[bold]OpenAI (optional, for AI features):[/bold]\n"
            "  export OPENAI_API_KEY=sk-...\n"
            "  Get a key: https://platform.openai.com/api-keys\n\n"
            "[bold]Ollama (optional, for local AI):[/bold]\n"
            "  Install: https://ollama.ai  then  ollama pull llama3\n"
            "  export OLLAMA_BASE_URL=http://localhost:11434/v1",
            border_style="magenta",
            title="[bold magenta]⚙️ Configuration[/bold magenta]",
        )
    )
    console.print(f"\n[dim]Data directory:[/dim] [cyan]{get_data_dir()}[/cyan]")
    console.print(f"[dim]Output directory:[/dim] [cyan]{get_output_dir()}[/cyan]")


def start() -> None:
    """Legacy entry point — delegates to the Typer app."""
    app()


if __name__ == "__main__":
    app()

"""Tier list creation and image rendering for musicli."""

from __future__ import annotations

import os
from datetime import datetime
from io import BytesIO
from pathlib import Path
from typing import Any

import httpx
import questionary
from PIL import Image, ImageDraw, ImageFont
from rich.panel import Panel

from musicli.core.lastfm import get_album_cover_url, get_artist_albums
from musicli.storage.db import get_output_dir, load_db, save_db
from musicli.ui.display import console, spinner

_TIERS = [
    ("s_tier", "S", "red"),
    ("a_tier", "A", "darkorange"),
    ("b_tier", "B", "gold"),
    ("c_tier", "C", "limegreen"),
    ("d_tier", "D", "royalblue"),
    ("e_tier", "E", "orchid"),
]

_TIER_COLORS_PIL = {
    "s_tier": (200, 0, 0),
    "a_tier": (255, 140, 0),
    "b_tier": (218, 165, 32),
    "c_tier": (50, 205, 50),
    "d_tier": (65, 105, 225),
    "e_tier": (218, 112, 214),
}


def _get_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    """Return a PIL font, trying system fonts before falling back to default.

    Args:
        size: Desired font size in points.

    Returns:
        A PIL font object.
    """
    # Try bundled font first (DejaVuSans via matplotlib/system)
    font_candidates = [
        # Linux/Unix common paths
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/dejavu/DejaVuSans.ttf",
        # macOS
        "/Library/Fonts/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        # Windows
        "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/segoeui.ttf",
    ]
    for path in font_candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except OSError:
                continue
    # Last resort: PIL built-in bitmap font (no sizing)
    return ImageFont.load_default()


def _pick_tier_albums(
    albums_to_rank: list[str], tier_label: str
) -> list[str]:
    """Let the user select albums for a given tier.

    Args:
        albums_to_rank: Remaining un-ranked album names.
        tier_label: Display label for the tier (e.g. ``"S Tier"``).

    Returns:
        List of album names assigned to this tier.
    """
    if not albums_to_rank:
        return []
    picks = questionary.checkbox(
        f"Select albums for {tier_label} (Space to select, Enter to confirm):",
        choices=albums_to_rank,
    ).ask()
    return picks or []


def create_tier_list() -> None:
    """Interactive flow: create a tier list for an artist's albums."""
    import pylast

    data = load_db()

    console.print(
        Panel(
            "[bold magenta]Create an S/A/B/C/D/E tier list for any artist[/bold magenta]",
            border_style="magenta",
        )
    )

    artist_input = questionary.text("Artist name:").ask()
    if not artist_input:
        return

    try:
        with spinner("Fetching albums…"):
            artist_albums_raw = get_artist_albums(artist_input)

        if not artist_albums_raw:
            console.print(Panel("❌ No albums found.", style="bold red", border_style="red"))
            return

        # Get canonical artist name from first album entry
        canonical_artist = artist_albums_raw[0].split(" - ", 1)[0] if artist_albums_raw else artist_input

        # Extract just album names
        albums_to_rank = [a.split(" - ", 1)[1] for a in artist_albums_raw]

        tier_list_name = questionary.text("Tier list name:").ask()
        while not tier_list_name or not tier_list_name.strip():
            console.print(Panel("Please enter a name.", style="bold yellow", border_style="yellow"))
            tier_list_name = questionary.text("Tier list name:").ask()

        tier_list_name = tier_list_name.strip()
        tier_data: dict[str, Any] = {}

        remaining = list(albums_to_rank)
        for tier_key, tier_label, _ in _TIERS:
            picks = _pick_tier_albums(remaining, f"{tier_label} Tier")
            for album in picks:
                remaining.remove(album)
            with spinner(f"Fetching covers for {tier_label} Tier…"):
                covers = [get_album_cover_url(canonical_artist, a) for a in picks]
            tier_data[tier_key] = [
                {"album": album, "cover_art": cover}
                for album, cover in zip(picks, covers)
            ]

        if not any(tier_data.get(k) for k, _, _ in _TIERS):
            console.print(Panel("All tiers empty. Aborting.", style="bold yellow", border_style="yellow"))
            return

        entry = {
            "tier_list_name": tier_list_name,
            "artist": canonical_artist,
            "time": str(datetime.now()),
            **tier_data,
        }
        data["tier_lists"].append(entry)
        save_db(data)

        console.print(
            Panel(
                f"✅ Tier list [bold cyan]{tier_list_name}[/bold cyan] saved!\n"
                "Run [bold]musicli tier show[/bold] to render it as an image.",
                border_style="green",
            )
        )

    except pylast.PyLastError:
        console.print(Panel("❌ Artist not found on Last.fm.", style="bold red", border_style="red"))
    except KeyboardInterrupt:
        pass


def see_tier_lists() -> None:
    """Render all saved tier lists as PNG images in the output directory."""
    data = load_db()
    tier_lists = data.get("tier_lists", [])

    if not tier_lists:
        console.print(
            Panel("❌ No tier lists created yet.", style="bold red", border_style="red")
        )
        return

    output_dir = get_output_dir()
    for tl in tier_lists:
        file_name = f"{tl['tier_list_name']}.png"
        with spinner(f"Rendering {tl['tier_list_name']}…"):
            image_generator(file_name, tl, output_dir)
        console.print(
            f"✅ [bold green]{tl['tier_list_name']}[/bold green] → "
            f"[cyan]{output_dir / file_name}[/cyan]"
        )

    console.print(
        Panel(
            f"[bold cyan]Done! Check [link=file://{output_dir}]{output_dir}[/link][/bold cyan]",
            border_style="green",
        )
    )


def image_generator(
    file_name: str,
    data: dict[str, Any],
    output_dir: Path | None = None,
) -> Path:
    """Generate a tier list image and save it to the output directory.

    The image shows six tiers (S→E) with album cover art thumbnails and
    labels. The canvas height is auto-cropped to the used area.

    Args:
        file_name: Output filename (e.g. ``"my_list.png"``).
        data: Tier list dictionary with keys ``s_tier`` … ``e_tier``.
        output_dir: Directory to save the image in. Defaults to the
            user data output directory.

    Returns:
        The full :class:`pathlib.Path` of the saved image.
    """
    if output_dir is None:
        output_dir = get_output_dir()
    else:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / file_name

    if output_path.exists():
        return output_path

    # --- Layout constants -------------------------------------------------
    image_width = 1920
    image_height = 5000
    increment = 200
    text_cutoff = 22
    text_padding = 8

    font = _get_font(14)
    tier_font = _get_font(36)

    image = Image.new("RGB", (image_width, image_height), (18, 18, 18))

    row_y = 0

    for tier_key, tier_label, _ in _TIERS:
        albums = data.get(tier_key, [])
        color = _TIER_COLORS_PIL[tier_key]
        col_x = 0

        # --- Tier label square --------------------------------------------
        draw = ImageDraw.Draw(image)
        draw.rectangle((col_x, row_y, col_x + increment, row_y + increment), fill=color)
        draw.text(
            (col_x + increment // 2, row_y + increment // 2),
            f"{tier_label}",
            font=tier_font,
            fill="white",
            anchor="mm",
        )
        col_x += increment

        # --- Album cover thumbnails ---------------------------------------
        for album_entry in albums:
            cover_url = album_entry.get("cover_art", "")
            try:
                resp = httpx.get(cover_url, timeout=8)
                cover = Image.open(BytesIO(resp.content)).convert("RGB")
                cover = cover.resize((increment, increment))
            except Exception:
                # Fallback: grey placeholder
                cover = Image.new("RGB", (increment, increment), (50, 50, 50))

            image.paste(cover, (col_x, row_y))

            # Album name label below thumbnail
            draw = ImageDraw.Draw(image)
            name = album_entry.get("album", "")
            if len(name) > text_cutoff:
                name = name[:text_cutoff] + "…"
            draw.text(
                (col_x + text_padding, row_y + increment - 20),
                name,
                font=font,
                fill="white",
            )

            col_x += increment
            if col_x > image_width - increment:
                row_y += increment + 40
                col_x = increment  # keep tier label gutter on new rows

        row_y += increment + 50
        col_x = 0

    # Crop to used height with a small bottom margin
    image = image.crop((0, 0, image_width, max(row_y, 100)))

    # Add artist name watermark at top-right
    draw = ImageDraw.Draw(image)
    artist = data.get("artist", "")
    created = data.get("time", "")[:10]
    watermark = f"{artist}  ·  Generated {created}  ·  musicli"
    draw.text(
        (image_width - 10, 6),
        watermark,
        font=_get_font(13),
        fill=(100, 100, 100),
        anchor="ra",
    )

    image.save(str(output_path))
    return output_path

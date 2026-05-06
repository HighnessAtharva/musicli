"""Storage layer: JSON persistence and path management for musicli."""

from __future__ import annotations

import json
import os
import shutil
import zipfile
from pathlib import Path
from typing import Any

from platformdirs import user_data_dir


def get_data_dir() -> Path:
    """Return the user-specific data directory for musicli.

    On Linux: ~/.local/share/musicli
    On macOS: ~/Library/Application Support/musicli
    On Windows: C:/Users/<user>/AppData/Local/musicli/musicli
    """
    data_dir = Path(user_data_dir("musicli", "musicli"))
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir


def get_db_path() -> Path:
    """Return the path to the main albums.json database file."""
    return get_data_dir() / "albums.json"


def get_output_dir() -> Path:
    """Return the path to the output directory where images are saved."""
    output_dir = get_data_dir() / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


def _empty_db() -> dict[str, Any]:
    """Return a fresh empty database structure."""
    return {"album_ratings": [], "song_ratings": [], "tier_lists": []}


def load_db() -> dict[str, Any]:
    """Load and return the database, creating it if it doesn't exist.

    Returns:
        The full database dictionary with keys:
        ``album_ratings``, ``song_ratings``, and ``tier_lists``.
    """
    db_path = get_db_path()
    if not db_path.exists():
        data = _empty_db()
        save_db(data)
        return data
    with db_path.open(encoding="utf-8") as f:
        return json.load(f)


def save_db(data: dict[str, Any]) -> None:
    """Persist *data* to the database JSON file.

    Args:
        data: The full database dictionary to save.
    """
    db_path = get_db_path()
    with db_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def migrate_legacy_db() -> bool:
    """Detect and migrate a legacy ``./albums.json`` into the user data dir.

    Returns:
        ``True`` if a migration was performed, ``False`` otherwise.
    """
    legacy = Path("albums.json")
    if not legacy.exists():
        return False
    db_path = get_db_path()
    if db_path.exists():
        # New DB already exists — skip migration
        return False
    db_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(legacy, db_path)
    return True


def backup_db() -> Path:
    """Create a timestamped zip backup of the data directory.

    Returns:
        The path to the created backup zip file.
    """
    from datetime import datetime

    data_dir = get_data_dir()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"musicli_backup_{timestamp}.zip"
    backup_path = data_dir.parent / backup_name
    with zipfile.ZipFile(backup_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for file in data_dir.rglob("*"):
            if file.is_file():
                zf.write(file, file.relative_to(data_dir))
    return backup_path


def export_csv(data: dict[str, Any], dest: Path) -> None:
    """Export the database to a CSV file.

    Writes three sections: album_ratings, song_ratings, and tier_lists.

    Args:
        data: The full database dictionary.
        dest: Destination path for the CSV file.
    """
    import csv

    with dest.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        # Album ratings
        writer.writerow(["### Album Ratings ###"])
        writer.writerow(["Artist", "Album", "Rating", "Date", "Review"])
        for entry in data.get("album_ratings", []):
            writer.writerow([
                entry.get("artist", ""),
                entry.get("album", ""),
                entry.get("album_rating", ""),
                entry.get("time", ""),
                entry.get("review", ""),
            ])

        writer.writerow([])

        # Song ratings (singles)
        writer.writerow(["### Song Ratings (Singles) ###"])
        writer.writerow(["Artist", "Song", "Rating"])
        for entry in data.get("song_ratings", []):
            writer.writerow([
                entry.get("artist", ""),
                entry.get("track", ""),
                entry.get("track_rating", ""),
            ])

        writer.writerow([])

        # Song ratings (from albums)
        writer.writerow(["### Track Ratings (From Albums) ###"])
        writer.writerow(["Artist", "Album", "Track", "Rating"])
        for album in data.get("album_ratings", []):
            for track in album.get("track_ratings", []):
                writer.writerow([
                    album.get("artist", ""),
                    album.get("album", ""),
                    track.get("track", ""),
                    track.get("track_rating", ""),
                ])


def export_markdown(data: dict[str, Any], dest: Path) -> None:
    """Export the database to a Markdown file.

    Generates a well-formatted Markdown document suitable for
    sharing as a blog post or GitHub Gist.

    Args:
        data: The full database dictionary.
        dest: Destination path for the Markdown file.
    """
    from datetime import datetime

    lines = [
        "# My Music Ratings",
        "",
        f"> Generated by [musicli](https://github.com/HighnessAtharva/musicli) on "
        f"{datetime.now().strftime('%B %d, %Y')}",
        "",
    ]

    # Albums
    album_ratings = data.get("album_ratings", [])
    if album_ratings:
        lines += [
            "## 🎵 Album Ratings",
            "",
            "| Artist | Album | Rating | Date | Review |",
            "| ------ | ----- | ------ | ---- | ------ |",
        ]
        for entry in sorted(album_ratings, key=lambda x: -x.get("album_rating", 0)):
            stars = "⭐" * entry.get("album_rating", 0)
            date = entry.get("time", "")[:10]
            review = entry.get("review", "").replace("|", "\\|")
            lines.append(
                f"| {entry.get('artist', '')} | {entry.get('album', '')} "
                f"| {stars} ({entry.get('album_rating', 0)}/10) | {date} | {review} |"
            )
        lines.append("")

    # Singles
    song_ratings = data.get("song_ratings", [])
    if song_ratings:
        lines += [
            "## 🎤 Song Ratings (Singles)",
            "",
            "| Artist | Song | Rating |",
            "| ------ | ---- | ------ |",
        ]
        for entry in sorted(song_ratings, key=lambda x: -x.get("track_rating", 0)):
            stars = "⭐" * entry.get("track_rating", 0)
            lines.append(
                f"| {entry.get('artist', '')} | {entry.get('track', '')} "
                f"| {stars} ({entry.get('track_rating', 0)}/10) |"
            )
        lines.append("")

    # Tier lists
    tier_lists = data.get("tier_lists", [])
    if tier_lists:
        lines += ["## 🏆 Tier Lists", ""]
        for tl in tier_lists:
            lines += [f"### {tl.get('tier_list_name', 'Untitled')} — {tl.get('artist', '')}", ""]
            for tier in ("s_tier", "a_tier", "b_tier", "c_tier", "d_tier", "e_tier"):
                albums = tl.get(tier, [])
                if albums:
                    label = tier.replace("_tier", "").upper()
                    album_names = ", ".join(a.get("album", "") for a in albums)
                    lines.append(f"- **{label}**: {album_names}")
            lines.append("")

    dest.write_text("\n".join(lines), encoding="utf-8")


def export_html(data: dict[str, Any], dest: Path) -> None:
    """Export the database to a self-contained HTML page.

    Generates a single HTML file with embedded CSS — ready to publish
    to GitHub Pages or any static host.

    Args:
        data: The full database dictionary.
        dest: Destination path for the HTML file.
    """
    from datetime import datetime

    album_rows = ""
    for entry in sorted(
        data.get("album_ratings", []), key=lambda x: -x.get("album_rating", 0)
    ):
        stars = "⭐" * entry.get("album_rating", 0)
        date = entry.get("time", "")[:10]
        review = entry.get("review", "")
        album_rows += (
            f"<tr><td>{entry.get('artist', '')}</td>"
            f"<td>{entry.get('album', '')}</td>"
            f"<td>{stars} <small>({entry.get('album_rating', 0)}/10)</small></td>"
            f"<td>{date}</td><td>{review}</td></tr>\n"
        )

    song_rows = ""
    for entry in sorted(
        data.get("song_ratings", []), key=lambda x: -x.get("track_rating", 0)
    ):
        stars = "⭐" * entry.get("track_rating", 0)
        song_rows += (
            f"<tr><td>{entry.get('artist', '')}</td>"
            f"<td>{entry.get('track', '')}</td>"
            f"<td>{stars} <small>({entry.get('track_rating', 0)}/10)</small></td></tr>\n"
        )

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>My Music Ratings — musicli</title>
<style>
  :root {{--bg:#121212;--surface:#1e1e2e;--text:#cdd6f4;--accent:#cba6f7;--green:#a6e3a1;--yellow:#f9e2af;}}
  body{{background:var(--bg);color:var(--text);font-family:'Segoe UI',system-ui,sans-serif;margin:0;padding:2rem}}
  h1{{color:var(--accent);font-size:2.5rem;margin-bottom:.25rem}}
  h2{{color:var(--green);border-bottom:1px solid #313244;padding-bottom:.4rem}}
  table{{width:100%;border-collapse:collapse;margin-bottom:2rem}}
  th{{background:var(--surface);color:var(--accent);padding:.6rem 1rem;text-align:left}}
  td{{padding:.5rem 1rem;border-bottom:1px solid #313244}}
  tr:hover td{{background:var(--surface)}}
  .badge{{background:var(--accent);color:var(--bg);padding:.15rem .5rem;border-radius:99px;font-size:.75rem;font-weight:700}}
  footer{{margin-top:3rem;text-align:center;color:#6c7086;font-size:.85rem}}
  a{{color:var(--accent);text-decoration:none}}a:hover{{text-decoration:underline}}
</style>
</head>
<body>
<h1>🎵 My Music Ratings</h1>
<p>Generated by <a href="https://github.com/HighnessAtharva/musicli">musicli</a> on {datetime.now().strftime('%B %d, %Y')}.</p>

<h2>Albums</h2>
<table>
<thead><tr><th>Artist</th><th>Album</th><th>Rating</th><th>Date</th><th>Review</th></tr></thead>
<tbody>{album_rows}</tbody>
</table>

<h2>Songs</h2>
<table>
<thead><tr><th>Artist</th><th>Song</th><th>Rating</th></tr></thead>
<tbody>{song_rows}</tbody>
</table>

<footer>Built with <a href="https://github.com/HighnessAtharva/musicli">musicli</a> — AI-powered music ratings from your terminal.</footer>
</body>
</html>"""
    dest.write_text(html, encoding="utf-8")

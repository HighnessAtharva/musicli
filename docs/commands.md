# Command Reference

Complete reference for all musicli commands.

## Global Options

```
musicli [OPTIONS] COMMAND [ARGS]...

Options:
  --version, -v    Show version and exit.
  --help           Show help message.
```

## `musicli` (Interactive TUI)

Launches the full interactive menu. Recommended for first-time users.

```sh
musicli
```

## `musicli rate`

### `musicli rate album`

Search for an artist on Last.fm, pick albums from the list, assign a 1–10 star rating, and optionally write a review.

```sh
musicli rate album
```

### `musicli rate song`

Search for a standalone song and rate it.

```sh
musicli rate song
```

### `musicli rate tracks`

Pick an already-rated album and rate its individual tracks.

```sh
musicli rate tracks
```

---

## `musicli view`

### `musicli view albums`

Show a Rich table of all rated albums.

```sh
musicli view albums [OPTIONS]

Options:
  --sort [name|rating|date]  Sort order. Default: name.
  --artist TEXT              Filter by artist name (case-insensitive substring match).
```

Examples:
```sh
musicli view albums
musicli view albums --sort rating
musicli view albums --artist "Radiohead"
musicli view albums --sort date --artist "Nirvana"
```

### `musicli view songs`

Show tables of rated singles and rated album tracks.

```sh
musicli view songs
```

### `musicli view stats`

Show statistics: album count, track count, averages, top album.

```sh
musicli view stats
```

---

## `musicli tier`

### `musicli tier create`

Interactively create an S/A/B/C/D/E tier list for an artist.

```sh
musicli tier create
```

### `musicli tier show`

Render all saved tier lists as PNG images in the data output directory.

```sh
musicli tier show
```

### `musicli tier list`

List all saved tier list PNG image files.

```sh
musicli tier list
```

---

## `musicli export`

### `musicli export csv`

Export all ratings to a CSV file.

```sh
musicli export csv [--output PATH]
# Default: musicli_export.csv
```

### `musicli export markdown`

Export ratings as a Markdown document suitable for sharing as a blog post or GitHub Gist.

```sh
musicli export markdown [--output PATH]
# Default: musicli_export.md
```

### `musicli export html`

Export ratings as a self-contained HTML page with embedded CSS — ready to publish to GitHub Pages.

```sh
musicli export html [--output PATH]
# Default: musicli_export.html
```

### `musicli export backup`

Create a timestamped zip backup of the entire data directory.

```sh
musicli export backup
# Output: musicli_backup_YYYYMMDD_HHMMSS.zip
```

---

## `musicli ai`

> Requires `pip install "musicli[ai]"` and `OPENAI_API_KEY`.
> Add `--local` to any command to use a local Ollama model instead.

### `musicli ai review`

Generate an AI critic review for an album, contextualised by your rating.

```sh
musicli ai review ARTIST ALBUM [--rating INT] [--local]

# Examples:
musicli ai review "Radiohead" "OK Computer" --rating 10
musicli ai review "Nirvana" "Nevermind" --rating 8 --local
```

### `musicli ai recommend`

Get personalised album recommendations based on your ratings.

```sh
musicli ai recommend [--local]
```

### `musicli ai describe-tier`

Get an AI narrative description of a saved tier list.

```sh
musicli ai describe-tier TIER_LIST_NAME [--local]

# Example:
musicli ai describe-tier "My Radiohead Ranking"
```

### `musicli ai compare`

Compare two artists based on your ratings of both.

```sh
musicli ai compare ARTIST1 ARTIST2 [--local]

# Example:
musicli ai compare "Radiohead" "Nirvana"
```

### `musicli ai digest`

Generate a digest summary of your listening stats and trends.

```sh
musicli ai digest [--local]
```

### `musicli ai chat`

Start an interactive chat session about your music library.

```sh
musicli ai chat [--local]
```

### `musicli ai tag`

Auto-tag an album with mood, genre, and era labels.

```sh
musicli ai tag ARTIST ALBUM [--local]

# Example:
musicli ai tag "Radiohead" "Kid A"
# → Tags: art rock, experimental, 2000s, dystopian, electronic, melancholic
```

---

## `musicli config`

Show configuration guide and current data/output directory paths.

```sh
musicli config
```

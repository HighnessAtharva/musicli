# Changelog

All notable changes to musicli are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

## [2.0.0] — 2026-05-06

### Added

- **Typer CLI**: Full subcommand structure (`rate`, `view`, `tier`, `ai`, `export`, `config`)
- **AI features** (`pip install "musicli[ai]"`):
  - `musicli ai review <artist> <album>` — AI critic review contextualised by your rating
  - `musicli ai recommend` — Personalised album recommendations from your taste profile
  - `musicli ai describe-tier <name>` — AI narrative of a tier list
  - `musicli ai compare <artist1> <artist2>` — Side-by-side artist comparison
  - `musicli ai digest` — Weekly/monthly listening digest
  - `musicli ai chat` — Free-form chat with your music library as context (RAG)
  - `musicli ai tag <artist> <album>` — Auto-tag albums with mood/genre/era labels
  - `--local` flag on all AI commands for offline Ollama usage
- **Export commands**: `export csv`, `export markdown`, `export html`, `export backup`
- **View flags**: `--sort` (name/rating/date) and `--artist` filter on `view albums`
- **Smart storage**: Data now stored in OS user data directory (platformdirs)
- **Data migration**: Auto-detects and migrates legacy `./albums.json` on first run
- **`questionary`-powered prompts**: Fuzzy search, multi-select checkboxes, inline spinners
- **Rich progress spinners** while fetching Last.fm and cover art data
- **Watermarked tier list images**: Artist name, generation date, and musicli credit
- **`musicli config`**: Interactive configuration guide with data directory paths
- **`--version` flag**
- Comprehensive test suite: 99 tests across all modules with mocked external services
- `CONTRIBUTING.md`, `SECURITY.md` documentation
- MkDocs documentation site with Material theme
- Single-page marketing landing page

### Fixed

- `show_tier_list_images()` and `show_stats()` were dead code (defined inside `start()` after the while-loop) — now proper module-level functions
- `network = pylast.LastFMNetwork(...)` ran at module import time — crashed without credentials; now lazy-initialised via `get_network()`
- `arial.ttf` hardcoded — crashed on Linux/macOS; now uses system font detection with PIL fallback
- `show_tier_list_images()` called `os.listdir()` without `mkdir` — now creates the directory first
- Fragile `os.path.dirname(__file__)` path calculation replaced with `platformdirs`

### Changed

- Python minimum version bumped to 3.10 (3.7/3.8/3.9 are EOL)
- `pillow` → `>=11.0` (multiple CVE fixes in 9.x/10.x)
- `pylast` → `>=5.3`
- `rich` → `>=13.9`
- `requests` replaced by `httpx >=0.27`
- `pick` kept for legacy tests; `questionary >=2.0` used for all interactive prompts
- `albums.json` moved from current working directory to user data dir
- Monolithic `musicli.py` refactored into a proper package (storage, core, ui, ai)
- `musicli.py` retained as backward-compatibility shim

### Removed

- Outdated `requirements.txt` with pinned 2022 hashes (replaced by pyproject.toml extras)
- Python 3.7 classifiers from setup.cfg

---

## [1.0.0] — 2023-xx-xx

### Added

- Initial release
- Rate albums, songs, and album tracks via an interactive `pick`-based menu
- Create S/A/B/C/D/E tier lists with PIL-generated PNG output
- See all ratings in Rich tables
- Last.fm integration via pylast

[Unreleased]: https://github.com/HighnessAtharva/musicli/compare/v2.0.0...HEAD
[2.0.0]: https://github.com/HighnessAtharva/musicli/compare/v1.0.0...v2.0.0
[1.0.0]: https://github.com/HighnessAtharva/musicli/releases/tag/v1.0.0

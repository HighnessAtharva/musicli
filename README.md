<div align="center">

<img src="BANNER.png" alt="musicli banner" width="700"/>

# musicli 2.0

**AI-powered music ratings, tier lists, and reviews — from your terminal.**

[![PyPI](https://img.shields.io/pypi/v/musicli?style=flat-square&color=6c63ff)](https://pypi.python.org/pypi/musicli/)
[![Python Version](https://img.shields.io/pypi/pyversions/musicli?style=flat-square&color=6c63ff)](https://pypi.python.org/pypi/musicli/)
[![License: MIT](https://img.shields.io/pypi/l/musicli?style=flat-square&color=6c63ff)](./LICENCE)
[![Tests](https://img.shields.io/github/actions/workflow/status/HighnessAtharva/musicli/ci.yml?label=tests&style=flat-square&color=6c63ff)](https://github.com/HighnessAtharva/musicli/actions)
[![Downloads](https://img.shields.io/pypi/dm/musicli?style=flat-square&color=6c63ff)](https://pypi.python.org/pypi/musicli/)
[![Docs](https://img.shields.io/badge/docs-online-6c63ff?style=flat-square)](https://HighnessAtharva.github.io/musicli)

[📦 Install](#-installation) · [🚀 Quickstart](#-quickstart) · [🤖 AI Features](#-ai-features) · [📚 Docs](https://HighnessAtharva.github.io/musicli) · [🤝 Contributing](./CONTRIBUTING.md)

</div>

---

## ✨ What is musicli?

**musicli** is the terminal app for music obsessives. Rate every album and track on a 10-point scale, build S/A/B/C/D/E tier lists with gorgeous PNG exports, and — in 2026 — unlock **AI-powered reviews, recommendations, and conversations** about your entire music library.

No GUI. No subscription. Just you, your terminal, and your music opinions.

---

## 🎯 Features

| Feature | Description |
|---------|-------------|
| ⭐ **10-Point Ratings** | Rate albums and tracks on a precise 1–10 scale |
| 🏆 **Tier Lists** | Create S/A/B/C/D/E tier lists exported as full-resolution PNG images |
| 🤖 **AI Reviews** | Generate critic-quality reviews, recommendations, and taste analysis |
| 💬 **AI Chat** | Chat with your music library — ask anything, get personalised answers |
| 📤 **Export** | Export your ratings as CSV, Markdown, or a self-contained HTML page |
| 🔍 **Search** | Filter albums by artist, sort by rating or date |
| 📊 **Stats** | See your average ratings, top albums, and collection overview |
| 💾 **Smart Storage** | Data lives in your OS user directory — never accidentally deleted |
| 🔄 **Migration** | Automatically detects and migrates legacy `./albums.json` files |
| 🎨 **Beautiful TUI** | Rich tables, coloured panels, and spinners — gorgeous in any terminal |

---

## 📦 Installation

```sh
pip install musicli
```

**Want AI features?**
```sh
pip install "musicli[ai]"
```

### API Keys

musicli uses the [Last.fm API](https://www.last.fm/api) for album/artist data.

1. Get a free key at https://www.last.fm/api/account/create
2. Set credentials (via environment or `.env` file):

```sh
# Option A — environment variables
export LASTFM_API_KEY=your_api_key
export LASTFM_API_SECRET=your_api_secret

# Option B — .env file in current directory
echo "LASTFM_API_KEY=your_api_key" >> .env
echo "LASTFM_API_SECRET=your_api_secret" >> .env
```

**For AI features** (optional):
```sh
export OPENAI_API_KEY=sk-...
```

Or use a **free local model** via [Ollama](https://ollama.ai):
```sh
ollama pull llama3
# then pass --local to any ai command
musicli ai recommend --local
```

---

## 🚀 Quickstart

```sh
# Interactive TUI (recommended for new users)
musicli

# Or use subcommands directly
musicli rate album          # Rate an artist's albums
musicli view albums         # See your ratings in a table
musicli tier create         # Build a tier list
musicli ai recommend        # Get AI album recommendations
```

---

## 🖥️ Command Reference

### Interactive Mode
```sh
musicli          # Full interactive TUI menu
```

### Rate
```sh
musicli rate album    # Search artist → pick albums → assign ratings + reviews
musicli rate song     # Rate a standalone song
musicli rate tracks   # Rate individual tracks from a rated album
```

### View
```sh
musicli view albums                          # All rated albums
musicli view albums --sort rating            # Sort by rating (highest first)
musicli view albums --sort date              # Sort by date rated
musicli view albums --artist "Radiohead"     # Filter by artist
musicli view songs                           # All rated songs
musicli view stats                           # Stats overview
```

### Tier Lists
```sh
musicli tier create    # Interactively assign albums to S/A/B/C/D/E tiers
musicli tier show      # Render all tier lists as PNG images
musicli tier list      # List saved tier list images
```

### Export
```sh
musicli export csv                           # Export to musicli_export.csv
musicli export csv --output my_ratings.csv  # Custom path
musicli export markdown                      # Export as Markdown (shareable blog post)
musicli export html                          # Export as self-contained HTML page
musicli export backup                        # Create a timestamped zip backup
```

### AI Commands
```sh
musicli ai review "Radiohead" "OK Computer" --rating 10
musicli ai recommend
musicli ai describe-tier "My Radiohead Ranking"
musicli ai compare "Radiohead" "Nirvana"
musicli ai digest
musicli ai chat
musicli ai tag "Radiohead" "OK Computer"

# Use a local Ollama model (no OpenAI key needed)
musicli ai recommend --local
```

### Config
```sh
musicli config         # Show configuration guide and data directory paths
musicli --version      # Show version
```

---

## 🤖 AI Features

> Requires `pip install "musicli[ai]"` and `OPENAI_API_KEY` (or `--local` for Ollama).

### AI Review
Get a personalised, critic-quality review contextualised by your rating:

```
$ musicli ai review "Radiohead" "OK Computer" --rating 10

A landmark in alternative rock, OK Computer arrived in 1997 sounding
like music from a dystopian future that somehow already felt present.
Your perfect score reflects what so many listeners have experienced:
an album that rewards every revisit with new details…
```

### AI Recommendations
```
$ musicli ai recommend

Based on your love of OK Computer (10/10) and Kid A (9/10), you'd likely
connect with:

1. **Portishead — Dummy** — The same claustrophobic atmospherics and
   emotional alienation, delivered through trip-hop instead of art rock…
```

### AI Chat
```
$ musicli ai chat

You: Which of my rated albums would work best as background music for coding?
musicli AI: Based on your library, I'd suggest Kid A — its ambient
textures and minimal vocals make it ideal for focused work…
```

### Local AI (Ollama)
Run all AI features completely offline and privately:
```sh
# Install Ollama from https://ollama.ai, then:
ollama pull llama3
musicli ai recommend --local
```

---

## 📁 Data Storage

musicli stores all data in your OS user directory:

| Platform | Path |
|----------|------|
| Linux | `~/.local/share/musicli/` |
| macOS | `~/Library/Application Support/musicli/` |
| Windows | `%LOCALAPPDATA%\musicli\musicli\` |

**Legacy migration**: If you have an old `albums.json` in the current directory from a pre-2.0 install, musicli automatically detects and migrates it on first run.

---

## 🛠️ Development

```sh
git clone https://github.com/HighnessAtharva/musicli
cd musicli
poetry install
poetry shell
```

### Run Tests
```sh
pytest tests/ -v
```

### Run with Coverage
```sh
pytest --cov=src/musicli --cov-report=term-missing
```

See [CONTRIBUTING.md](./CONTRIBUTING.md) for the full development guide.

---

## 📚 Documentation

Full documentation: **https://HighnessAtharva.github.io/musicli**

- [Installation Guide](https://HighnessAtharva.github.io/musicli/installation/)
- [Command Reference](https://HighnessAtharva.github.io/musicli/commands/)
- [AI Features Guide](https://HighnessAtharva.github.io/musicli/ai-features/)
- [Configuration](https://HighnessAtharva.github.io/musicli/configuration/)
- [FAQ](https://HighnessAtharva.github.io/musicli/faq/)

---

## 🗺️ Roadmap

- [ ] Spotify integration (`pip install "musicli[spotify]"`)
- [ ] Semantic album search using embeddings
- [ ] `musicli share tier` — copy path to clipboard
- [ ] Web dashboard export
- [ ] Plugin system for custom exporters

---

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](./CONTRIBUTING.md) first.

Found a security issue? See [SECURITY.md](./SECURITY.md).

---

## 📄 License

MIT © [Atharva Shah](https://github.com/HighnessAtharva)

---

<sub>Built with ❤️ using Python, Typer, Rich, Pillow, pylast, and OpenAI. Powered by Last.fm.</sub>

<!-- social-footer -->
---

<div align="center">

**Atharva Shah** — Python & AI Engineer · Developer Advocate · Technical Writer

[![Website](https://img.shields.io/badge/Website-000000?style=for-the-badge&logo=About.me&logoColor=white)](https://atharvashah.com)
[![Blog](https://img.shields.io/badge/Blog-FF6719?style=for-the-badge&logo=substack&logoColor=white)](https://blog.atharvashah.com)
[![Twitter](https://img.shields.io/badge/Twitter-000000?style=for-the-badge&logo=x&logoColor=white)](https://x.com/cultist_dev)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/atharva-shah-tech/)

</div>

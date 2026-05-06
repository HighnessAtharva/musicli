# Contributing to musicli

Thank you for your interest in contributing! This guide will help you get started.

---

## 🚀 Development Setup

### Prerequisites

- Python 3.10+
- [Poetry](https://python-poetry.org/) (recommended) or pip
- A [Last.fm API key](https://www.last.fm/api/account/create) for integration testing

### Clone and Install

```sh
git clone https://github.com/HighnessAtharva/musicli.git
cd musicli

# Install all dependencies including dev tools
poetry install

# Activate the virtual environment
poetry shell
```

### Environment Variables

Create a `.env` file in the project root:

```sh
LASTFM_API_KEY=your_key
LASTFM_API_SECRET=your_secret
OPENAI_API_KEY=sk-...   # optional, for AI feature testing
```

---

## 🏗️ Project Structure

```
src/musicli/
├── __init__.py        # Package version
├── cli.py             # Typer CLI entry point
├── core/
│   ├── lastfm.py      # Last.fm API integration
│   ├── ratings.py     # Interactive rating flows
│   ├── tier.py        # Tier list creation & image rendering
│   └── stats.py       # Statistics helpers
├── storage/
│   └── db.py          # JSON persistence, export, backup
├── ui/
│   └── display.py     # Rich terminal UI helpers
└── ai/
    └── assistant.py   # AI features (OpenAI / Ollama)

tests/
├── conftest.py        # Shared fixtures
├── test_cli.py        # CLI integration tests
├── test_storage.py    # Storage layer tests
├── test_core_*.py     # Core module tests
└── test_ai.py         # AI assistant tests
```

---

## 🧪 Running Tests

```sh
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src/musicli --cov-report=term-missing

# Run a specific test file
pytest tests/test_cli.py -v

# Run tests matching a name pattern
pytest -k "test_export" -v
```

Tests use mocks for all external services (Last.fm, OpenAI) — no real API calls are made.

---

## 🔧 Code Style

We use the following tools (all configured in `pyproject.toml` / `setup.cfg`):

| Tool | Purpose |
|------|---------|
| `black` | Code formatting |
| `isort` | Import ordering |
| `flake8` | Linting |
| `mypy` | Type checking |

Run all checks:

```sh
poetry run black .
poetry run isort .
poetry run flake8 .
```

Or install [pre-commit](https://pre-commit.com/) hooks to run automatically:

```sh
pre-commit install
```

---

## ✅ Pull Request Guidelines

1. **Branch from `main`**: `git checkout -b feat/my-feature`
2. **Write tests**: All new code should have corresponding tests
3. **Update docs**: Update `README.md` and/or `docs/` as needed
4. **Keep PRs focused**: One feature or fix per PR
5. **Update CHANGELOG**: Add an entry under `## Unreleased`
6. **Pass CI**: All tests and linters must pass

### Commit Message Format

```
<type>: <short description>

Types: feat, fix, docs, test, refactor, chore
```

Examples:
- `feat: add Spotify sync command`
- `fix: handle missing cover art gracefully`
- `docs: update AI features guide`

---

## 🐛 Reporting Bugs

Use [GitHub Issues](https://github.com/HighnessAtharva/musicli/issues) with the **bug** label.

Include:
- Operating system and Python version
- musicli version (`musicli --version`)
- Steps to reproduce
- Expected vs. actual behaviour
- Error output (if any)

---

## 💡 Feature Requests

Open a [GitHub Issue](https://github.com/HighnessAtharva/musicli/issues) with the **enhancement** label.

---

## 📚 Documentation

The docs site is built with [MkDocs Material](https://squidfunk.github.io/mkdocs-material/):

```sh
# Serve locally
mkdocs serve

# Build static site
mkdocs build
```

Docs are in `docs/` and auto-deployed to GitHub Pages on each push to `main`.

---

## 🏷️ Releasing

Releases are managed by the maintainer. The process:

1. Bump version in `pyproject.toml` and `src/musicli/__init__.py`
2. Update `CHANGELOG.md`
3. Tag and push: `git tag v2.x.x && git push --tags`
4. GitHub Actions publishes to PyPI automatically

---

Thank you for contributing to musicli! 🎵

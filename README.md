# musicli

<p align="center">
  <img src="https://user-images.githubusercontent.com/HighnessAtharva/musicli/banner.png" alt="Music CLI Banner" width="600"/>
</p>

[![PyPI](https://img.shields.io/pypi/v/musicli?style=flat-square)](https://pypi.python.org/pypi/musicli/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/musicli?style=flat-square)](https://pypi.python.org/pypi/musicli/)
[![PyPI - License](https://img.shields.io/pypi/l/musicli?style=flat-square)](https://pypi.python.org/pypi/musicli/)

---

**musicli** is a powerful, user-friendly Python CLI for rating, reviewing, and cataloguing your favorite artists and albums. With intuitive search, 10-point album and track ratings, tier list creation, and beautiful terminal UI, musicli is the perfect tool for music lovers and collectors.

---

## 🚀 Features

- **Rate & review** albums and tracks from your terminal
- **Create tier lists** and visualize them as images
- **Search and filter** your music library with ease
- **10-point scale** for nuanced ratings
- **Customizable** cataloguing and review options
- **Last.fm integration** for album/artist info (API key required)
- **Command-line interface**—no GUI required
- **Beautiful terminal UI** with colors, tables, and panels
- **Stats and summaries** for your collection
- **All output saved in output/** directory

---

## 📦 Installation

```sh
pip install musicli
```

Get a Last.fm API key from [here](https://www.last.fm/api/account/create) and set it as environment variables:

```sh
set LASTFM_API_KEY=<your_api_key>
set LASTFM_API_SECRET=<your_api_secret>
```

---

## 🏁 Quickstart

```sh
musicli
```

Or run with help:

```sh
python -m musicli.musicli --help
```

Follow the interactive prompts to search, rate, and review your music collection.

---

## 🖥️ CLI Commands & Options

- **Rate by Album**: Search and rate albums for any artist
- **Rate Songs**: Rate individual songs or songs from albums
- **See Albums Rated**: View all rated albums in a table
- **See Songs Rated**: View all rated songs in a table
- **Make a Tier List**: Create a tier list for an artist's albums
- **See Created Tier Lists**: View tier lists you've made
- **Show Tier List Images**: List all tier list images in output/
- **Show Stats**: See stats for albums, songs, and tier lists
- **EXIT**: Quit the CLI

---

## 🛠️ Development

1. **Clone this repository**
2. **Requirements:**
   - [Poetry](https://python-poetry.org/)
   - Python 3.7+
3. **Install dependencies:**

    ```sh
    poetry install
    ```

4. **Activate the virtual environment:**

    ```sh
    poetry shell
    ```

---

## 🧪 Testing

```sh
pytest tests/
```

See [TESTING.md](./TESTING.md) for more info.

---

## 📚 Documentation

Documentation is auto-generated from [docs/](./docs) and docstrings, and published as a [GitHub project page](https://HighnessAtharva.github.io/musicli) on each release.

---

## 📖 Resources

- **Documentation:** [https://HighnessAtharva.github.io/musicli](https://HighnessAtharva.github.io/musicli)
- **Source Code:** [https://github.com/HighnessAtharva/musicli](https://github.com/HighnessAtharva/musicli)
- **PyPI:** [https://pypi.org/project/musicli/](https://pypi.org/project/musicli/)

---

<sub>This project was generated using the [wolt-python-package-cookiecutter](https://github.com/woltapp/wolt-python-package-cookiecutter) template.</sub>

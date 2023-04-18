# musicli

[![PyPI](https://img.shields.io/pypi/v/musicli?style=flat-square)](https://pypi.python.org/pypi/musicli/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/musicli?style=flat-square)](https://pypi.python.org/pypi/musicli/)
[![PyPI - License](https://img.shields.io/pypi/l/musicli?style=flat-square)](https://pypi.python.org/pypi/musicli/)
[![Coookiecutter - Wolt](https://img.shields.io/badge/cookiecutter-Wolt-00c2e8?style=flat-square&logo=cookiecutter&logoColor=D4AA00&link=https://github.com/woltapp/wolt-python-package-cookiecutter)](https://github.com/woltapp/wolt-python-package-cookiecutter)

---
musicli is a powerful and user-friendly Python package that allows users to easily rate, review, and catalogue their favorite artists and albums from the command line. With intuitive search and selection features, users can quickly navigate their music library and rate each album on a 10-point scale. The package also offers the option to rate individual tracks and includes a variety of customization options to personalize the cataloguing experience. Whether you're a music aficionado or simply looking to organize your music library, musicli is the perfect tool for music lovers everywhere.

**Documentation**: [https://HighnessAtharva.github.io/musicli](https://HighnessAtharva.github.io/musicli)

**Source Code**: [https://github.com/HighnessAtharva/musicli](https://github.com/HighnessAtharva/musicli)

**PyPI**: [https://pypi.org/project/musicli/](https://pypi.org/project/musicli/)

---

Rate, review, and catalogue all your artists and albums from the command line

## Installation

```sh
pip install musicli
```

Get a Last.fm API key from [here](https://www.last.fm/api/account/create) and set it as an environment variable:

```sh
set LASTFM_API_KEY=<your_api_key>
set LASTFM_API_SECRET=<your_api_secret>
```

## Development

* Clone this repository
* Requirements:
  * [Poetry](https://python-poetry.org/)
  * Python 3.7+
* Create a virtual environment and install the dependencies

```sh
poetry install
```

* Activate the virtual environment

```sh
poetry shell
```

### Testing

```sh
pytest
```

### Documentation

The documentation is automatically generated from the content of the [docs directory](./docs) and from the docstrings of the public signatures of the source code. The documentation is updated and published as a [Github project page](https://pages.github.com/) automatically as part each release.

### Releasing

Trigger the [Draft release workflow](https://github.com/HighnessAtharva/musicli/actions/workflows/draft_release.yml)
(press _Run workflow_). This will update the changelog & version and create a GitHub release which is in _Draft_ state.

Find the draft release from the
[GitHub releases](https://github.com/HighnessAtharva/musicli/releases) and publish it. When a release is published, it'll trigger [release](https://github.com/HighnessAtharva/musicli/blob/master/.github/workflows/release.yml) workflow which creates PyPI release and deploys updated documentation.

### Pre-commit

Pre-commit hooks run all the auto-formatters (e.g. `black`, `isort`), linters (e.g. `mypy`, `flake8`), and other quality
 checks to make sure the changeset is in good shape before a commit/push happens.

You can install the hooks with (runs for each commit):

```sh
pre-commit install
```

Or if you want them to run only for each push:

```sh
pre-commit install -t pre-push
```

Or if you want e.g. want to run all checks manually for all files:

```sh
pre-commit run --all-files
```

---

This project was generated using the [wolt-python-package-cookiecutter](https://github.com/woltapp/wolt-python-package-cookiecutter) template.

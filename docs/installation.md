# Installation

## Requirements

- Python 3.10 or newer
- A [Last.fm API key](https://www.last.fm/api/account/create) (free)

## Installing musicli

=== "pip"

    ```sh
    pip install musicli
    ```

=== "With AI features"

    ```sh
    pip install "musicli[ai]"
    ```

=== "All extras"

    ```sh
    pip install "musicli[all]"
    ```

=== "Development"

    ```sh
    git clone https://github.com/HighnessAtharva/musicli.git
    cd musicli
    poetry install
    ```

## Setting Up API Keys

### Last.fm (required)

1. Register at [last.fm/api/account/create](https://www.last.fm/api/account/create)
2. Copy your API Key and Shared Secret

```sh
# Option A — environment variables
export LASTFM_API_KEY=your_api_key
export LASTFM_API_SECRET=your_api_secret

# Option B — .env file (recommended)
cat >> .env << DOTENV
LASTFM_API_KEY=your_api_key
LASTFM_API_SECRET=your_api_secret
DOTENV
```

### OpenAI (optional — for AI features)

```sh
export OPENAI_API_KEY=sk-...
```

Get a key at [platform.openai.com/api-keys](https://platform.openai.com/api-keys).

### Ollama (optional — for local/offline AI)

```sh
# Install from https://ollama.ai, then:
ollama pull llama3
```

Use `--local` with any `musicli ai` command to route requests to your local model.

## Verifying Installation

```sh
musicli --version
# musicli version 2.0.0

musicli config
# Shows configuration guide and data directory paths
```

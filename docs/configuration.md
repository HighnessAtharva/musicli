# Configuration

## API Keys

musicli reads credentials from environment variables or a `.env` file.

### Last.fm (required)

Register at [last.fm/api/account/create](https://www.last.fm/api/account/create).

```sh
# Environment variables
export LASTFM_API_KEY=your_api_key
export LASTFM_API_SECRET=your_api_secret

# Or .env file (auto-loaded by musicli)
LASTFM_API_KEY=your_api_key
LASTFM_API_SECRET=your_api_secret
```

### OpenAI (optional — AI features)

```sh
export OPENAI_API_KEY=sk-...
```

### Ollama (optional — local AI)

```sh
# Default: http://localhost:11434/v1
export OLLAMA_BASE_URL=http://localhost:11434/v1
```

Use `--local` with any `musicli ai` command to route to Ollama.

---

## Data Directory

musicli stores data in your OS user data directory:

| Platform | Path |
|----------|------|
| Linux | `~/.local/share/musicli/` |
| macOS | `~/Library/Application Support/musicli/` |
| Windows | `%LOCALAPPDATA%\musicli\musicli\` |

Files inside:

| File | Purpose |
|------|---------|
| `albums.json` | Your ratings and tier lists |
| `output/` | Generated tier list PNG images |

Run `musicli config` to see the exact paths on your system.

---

## Migrating from v1.x

v1.x stored `albums.json` in the current working directory. musicli 2.0 detects
this file on first run and automatically migrates it:

```
📦 Found a legacy ./albums.json and migrated it to:
~/.local/share/musicli/
```

After migration, you can safely delete the old file.

---

## Backup and Restore

### Backup

```sh
musicli export backup
# Creates: musicli_backup_20260506_123456.zip
```

### Restore

Extract the backup zip into your data directory:

```sh
unzip musicli_backup_20260506_123456.zip -d ~/.local/share/musicli/
```

---

## Shell Completion

Enable tab completion for your shell:

```sh
musicli --install-completion
```

Supported shells: bash, zsh, fish, PowerShell.

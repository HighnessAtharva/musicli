# AI Features

musicli 2.0 is **AI-first**. Every AI feature is designed to make your music
ratings smarter, more personal, and more shareable.

## Installation

```sh
pip install "musicli[ai]"
```

This adds the `openai` package. All other dependencies are included in the base install.

## API Key Setup

```sh
export OPENAI_API_KEY=sk-...
```

Or add it to a `.env` file:
```
OPENAI_API_KEY=sk-...
```

## Local AI (Offline Mode)

Prefer to keep your data private? Use [Ollama](https://ollama.ai) to run AI locally:

```sh
# Install Ollama, then:
ollama pull llama3

# Pass --local to any ai command:
musicli ai recommend --local
musicli ai review "Radiohead" "OK Computer" --rating 10 --local
```

Set `OLLAMA_BASE_URL` to customise the Ollama server address (default: `http://localhost:11434/v1`).

---

## Commands

### `musicli ai review`

Generate a personalised, critic-quality review for any album.

The review is contextualised by **your rating**, making it feel like your own expert take rather than a generic summary.

```sh
musicli ai review "Radiohead" "OK Computer" --rating 10
```

**Example output:**
> A landmark in alternative rock, OK Computer arrived in 1997 sounding like
> music from a dystopian future that somehow already felt present. Your perfect
> score reflects what so many listeners experience: an album that rewards every
> revisit with new details — Thom Yorke's paranoid vocals on "Climbing Up The
> Walls," the cinematic sweep of "Exit Music"…

---

### `musicli ai recommend`

Analyse your ratings and generate 5–7 personalised album recommendations.

```sh
musicli ai recommend
```

**Example output:**
> Based on your love of OK Computer (10/10) and Ágætis byrjun by Sigur Rós (9/10):
>
> 1. **Talk Talk — Laughing Stock** — The same slow-burning post-rock atmosphere
>    with an even more radical commitment to space and silence.
> 2. **Bark Psychosis — Hex** — A precursor to post-rock that shares OK Computer's
>    atmospheric tension and unconventional song structures…

---

### `musicli ai describe-tier`

Get an AI narrative of what your tier list reveals about your taste.

```sh
musicli ai describe-tier "My Radiohead Ranking"
```

**Example output:**
> Your S tier — OK Computer and Kid A — reveals a preference for Radiohead at
> their most conceptually ambitious. The fact that Pablo Honey sits in D tier
> suggests you appreciate the band's evolution away from conventional rock more
> than their melodic hooks…

---

### `musicli ai compare`

Side-by-side comparison of two artists based on your ratings.

```sh
musicli ai compare "Radiohead" "Nirvana"
```

---

### `musicli ai digest`

A friendly written summary of your listening statistics and patterns.

```sh
musicli ai digest
```

---

### `musicli ai chat`

A free-form conversation with your music library as context.

```sh
musicli ai chat
```

**Example session:**
```
You: Which of my rated albums would work best as focus music?
musicli AI: Based on your library, Kid A (9/10) is probably your best
bet for focus — its ambient textures and minimal vocals create a
contemplative atmosphere without demanding attention…

You: What's my average rating for Radiohead?
musicli AI: You've rated 4 Radiohead albums with an average of 9.25/10.
Your highest is OK Computer (10/10) and your lowest is Pablo Honey (5/10).
```

Type `exit` or `quit` to end the session.

---

### `musicli ai tag`

Auto-tag any album with mood, genre, era, and thematic labels.

```sh
musicli ai tag "Radiohead" "OK Computer"
# → indie rock, alternative, 90s, dystopian, art rock, melancholic, electronic
```

Useful for building a personalised tagging system for your collection.

---

## Privacy

- By default, AI commands send album/rating data to OpenAI's API.
- Use `--local` with any command to keep everything on your machine.
- Your `.env` file is never committed if it's in `.gitignore`.
- The `chat` command sends a truncated JSON snapshot of your library (≤8000 chars) as context.

See [SECURITY.md](https://github.com/HighnessAtharva/musicli/blob/main/SECURITY.md) for more details.

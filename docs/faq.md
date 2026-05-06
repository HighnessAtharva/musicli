# FAQ

## General

### Is musicli free?

Yes, 100% free and open source (MIT license). The Last.fm API is also free.
OpenAI has a cost, but you can use the free Ollama option instead.

### Does musicli require an internet connection?

For rating features: yes — musicli fetches album lists and cover art from Last.fm.

For AI features: only if you use the OpenAI backend. The `--local` flag works fully offline with Ollama.

### What terminal do I need?

Any modern terminal works. For the best experience, use one with:
- True colour support (most modern terminals)
- Emoji rendering (iTerm2, Windows Terminal, Kitty, Alacritty)
- OSC 8 hyperlink support (iTerm2, Windows Terminal) for clickable cover art links

---

## Ratings

### Can I change a rating?

Yes. Run `musicli rate album` again and pick the same album — the rating is updated in place.

### What's the difference between "Rate Songs" and "Rate Tracks"?

- **Rate Songs** (`musicli rate song`) — rate a standalone single, not linked to any album.
- **Rate Tracks** (`musicli rate tracks`) — rate individual tracks from an album you've already rated.

### Can I add a review to an album?

Yes! When rating an album you'll be asked if you want to write a review.
Reviews appear in the `view albums` table and in exports.

---

## Tier Lists

### Where are tier list images saved?

In your data directory's `output/` folder. Run `musicli config` to see the path.

### Can I re-render a tier list image?

Delete the existing PNG from the `output/` directory, then run `musicli tier show`.

### Can I edit a tier list after creating it?

Not yet — this is on the roadmap. For now, create a new tier list with the same name
(it will be appended; delete the old one from `albums.json` manually if needed).

---

## AI

### Do I need to pay for AI features?

The OpenAI backend costs a small amount per request (typically < $0.01 per query with gpt-4o-mini).
The Ollama backend (`--local`) is completely free and runs on your own machine.

### What data is sent to OpenAI?

Only your album/track ratings and review text — no personal information. A compact JSON
snapshot (≤8000 characters) is sent as context for the `chat` and `recommend` commands.

### Which OpenAI model does musicli use?

`gpt-4o-mini` by default — a fast, cheap, and capable model. This is configurable
in a future release.

### Can I use Claude or Gemini instead of OpenAI?

Not natively yet, but Ollama supports many models. Use `--local` and configure
`OLLAMA_BASE_URL` to point at any OpenAI-compatible API.

---

## Data & Privacy

### Where is my data stored?

See [Configuration → Data Directory](./configuration.md#data-directory).

### How do I backup my data?

```sh
musicli export backup
```

### How do I move data to another machine?

1. Run `musicli export backup` to create a zip
2. Copy the zip to the new machine
3. Extract into the data directory (see `musicli config`)

### How do I delete all my data?

Delete the data directory. Run `musicli config` to find the path.

---

## Troubleshooting

### `❌ Last.fm credentials not found`

Set `LASTFM_API_KEY` and `LASTFM_API_SECRET` in your environment or a `.env` file.
See [Configuration](./configuration.md).

### `❌ Artist not found on Last.fm`

Check the spelling. Last.fm is case-insensitive but requires the exact artist name.
Try searching on [last.fm](https://www.last.fm) first.

### The tier list image uses a plain grey placeholder instead of album art

This happens when the cover art URL from Last.fm is unreachable. The image is still
generated correctly — the placeholder is used for albums where art couldn't be fetched.

### `❌ OPENAI_API_KEY not set`

Set the environment variable or use `--local` for Ollama.

### Tests fail without API keys

Tests use mocked external services — they should never require real API keys.
If you're seeing this, file a bug report.

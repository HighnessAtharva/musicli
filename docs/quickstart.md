# Quickstart

Get up and running in under 5 minutes.

## 1. Install

```sh
pip install musicli
```

## 2. Set API Keys

```sh
export LASTFM_API_KEY=your_key
export LASTFM_API_SECRET=your_secret
```

## 3. Launch

```sh
musicli
```

You'll see the interactive menu:

```
╭───────────────────────────────────────────╮
│           ♪ musicli                       │
│  🎵  Welcome to musicli 2.0!              │
│  AI-powered music ratings from terminal.  │
╰───────────────────────────────────────────╯

What do you want to do?
❯ ⭐  Rate by Album
  🎵  Rate Songs
  📀  See Albums Rated
  🏆  Make a Tier List
  🤖  AI Features
  ...
```

## Quick Example Workflow

### Step 1: Rate Some Albums

```sh
musicli rate album
# → Type "Radiohead"
# → Pick "Radiohead - OK Computer"
# → Select ★★★★★★★★★★ (10/10)
# → Optionally write a review
```

### Step 2: View Your Ratings

```sh
musicli view albums
```

Output:
```
🎵 Album Ratings
┌───┬───────────┬──────────────┬────────────────────┬─────────────┐
│ # │ Artist    │ Album        │ Rating             │ Date        │
├───┼───────────┼──────────────┼────────────────────┼─────────────┤
│ 1 │ Radiohead │ OK Computer  │ ★★★★★★★★★★          │ May 06 2026 │
└───┴───────────┴──────────────┴────────────────────┴─────────────┘
```

### Step 3: Create a Tier List

```sh
musicli tier create
# → Type artist name
# → Select albums for each tier (S/A/B/C/D/E)
# → Tier list saved!

musicli tier show
# → PNG images generated in your data directory
```

### Step 4: Get AI Recommendations

```sh
pip install "musicli[ai]"
export OPENAI_API_KEY=sk-...

musicli ai recommend
# → Based on your taste profile, here are 7 albums you'd love…
```

### Step 5: Export

```sh
musicli export markdown    # → musicli_export.md
musicli export html        # → musicli_export.html (publish-ready!)
musicli export csv         # → musicli_export.csv
```

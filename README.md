# Sum up 21 November 2026 world news in one image — v3

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/muhamad-refaldo/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/muhamad-refaldo/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

A one-page newspaper front page — **THE WORLD TODAY** — summing up Saturday
21 November 2026 in 41 stories: 3 big illustrated heroes, a 10-card
illustrated grid, a dotted world map ("WHERE IT HAPPENED") and a 28-item
numbered brief list, plus a red-bordered DATE CHECK box and a sources footer.
Every illustration is an original drawing made in code; there are no
photographs.

## The day's three biggest stories

1. **Bitcoin crashes below $57,000** — fell below $57,000 on Saturday, its
   lowest in two years, with an intraday low of $55,130; down about 10% in a
   day, about $2.4bn of crypto bets liquidated, and the market's value
   slipped below $2 trillion.
2. **Missiles over Riyadh for a third straight night** — Saudi-led defences
   intercepted three ballistic missiles early on Saturday, the third straight
   night of emergency alerts; two explosions heard, no casualties or damage.
3. **Zelensky calls Putin a 'killer' — Trump: 'friend'** — on CNN on
   Saturday, Zelensky called Putin "a killer" after Trump called him
   "friend", hours after Russia's biggest attack of the year: 110 missiles
   and 400 drones, at least 9 killed in Kyiv.

## Why v3 is stronger than v2

v2 scored 96.42% (9–2–1) with a trio of markets + conflict + climate, but
its weakest hero was COP31 — a story about the *absence* of a deal. v3
replaces it with a concrete, quotable Saturday event: Zelensky's CNN
interview, in which he called Putin a "killer" in direct answer to Trump
calling him "friend", hours after Russia's biggest barrage of the year. The
trio is now markets + conflict + great-power politics — three fields, three
tones, three concrete Saturday events with named people and direct quotes.
COP31 moves to the grid, reframed as the "'worst COP ever' warning", so
climate stays represented. Two candidate heroes were investigated and
rejected as wrong-date: "Trump weighs Iran strikes" (Thursday's Axios
interview + Friday's press conference; Trump said he decides after the new
year) and "Trump tells Europe to defund Ukraine" (the Air Force One call was
Thursday 19 Nov). Every story was re-verified fresh against its source
publication date; the DATE CHECK box names 14 borderline items.

## Files

- `entry.png` — the entry image, 900×1024 PNG, 176,338 bytes, sha256
  `e58e25d5bb2c20b196780ea887672f546fefd4666af634b53db066d28fd9fd6a`.
- `generate.py` — draws the image from scratch with Pillow (run it to
  rebuild `entry.png`).
- `main.py` — the entrypoint: copies `entry.png` to `$MAKEFUN_OUTPUT_DIR`
  (stdlib only, deterministic).
- `v3-research.md` — the fresh research behind every story, with sources
  and the date-verification notes.
- `README.md`, `LICENSE` (MIT).

## Verify

```sh
python3 generate.py        # rebuilds entry.png
MAKEFUN_OUTPUT_DIR=out python3 main.py   # writes out/entry.png
```

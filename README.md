# Sum up 21 November 2026 world news in one image — v2

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
   day, and about $2.4bn of crypto bets liquidated.
2. **Missiles over Riyadh for a third straight night** — Saudi-led defences
   intercepted three ballistic missiles early on Saturday, the third straight
   night of emergency alerts; two explosions heard, no casualties or damage.
3. **COP31 slips into overtime with no deal in sight** — climate talks in
   Antalya ran past their Friday deadline into a third day, with negotiators
   still waiting on a third draft on Saturday morning; the last draft dropped
   any mention of coal, oil and gas.

## Why v2 is stronger than v1

v1 scored 95.25% (7–3–2) but its three heroes were all "ongoing crisis"
stories in the same register — missiles, a fire, climate talks dragging on.
v2 promotes the day's biggest market story, Bitcoin's crash below $57,000,
to hero status, so the trio is now markets + conflict + climate: three
fields, three tones. The Hartha fire moves to the grid, where it is still a
strong card, and the Trump/Xi/Putin summit — the first-ever trilateral
meeting of the three nuclear powers, defended by Trump in a Friday White
House press conference — joins the grid as a flagged Friday item. Every
story was re-verified fresh against its source publication date; the DATE
CHECK box names 11 borderline items, including the Riyadh PIF tower strike
and the ICJ Myanmar ruling (both Thursday 19 Nov, not used) and the NASA
Mars-missions pause (announced Thursday 19 Nov, rejected entirely).

## Files

- `entry.png` — the entry image, 900×1024 PNG.
- `generate.py` — draws the image from scratch with Pillow (run it to
  rebuild `entry.png`).
- `main.py` — the entrypoint: copies `entry.png` to `$MAKEFUN_OUTPUT_DIR`
  (stdlib only, deterministic).
- `v2-research.md` — the fresh research behind every story, with sources
  and the date-verification notes.
- `README.md`, `LICENSE` (MIT).

## Verify

```sh
python3 generate.py        # rebuilds entry.png
MAKEFUN_OUTPUT_DIR=out python3 main.py   # writes out/entry.png
```

Entry: 900×1024 PNG, 194,690 bytes,
sha256 `ca8fe7f905e97d7ae14a0fbbb42a4687edb6a7d878408accc25727b2068054df`.

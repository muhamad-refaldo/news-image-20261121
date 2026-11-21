[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/muhamad-refaldo/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/muhamad-refaldo/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

# Sum up 21 November 2026 world news in one image

One-page newspaper front page (900×1024 PNG) summing up **Saturday, 21 November 2026**
in 41 stories: 3 heroes, 10 grid cards, 28 one-line briefs, a dotted world map,
a "day in numbers" strip, and a truthful DATE CHECK box.

## The day

- **Hero 1 — Missiles over Riyadh for a third straight night.** Saudi-led defences
  intercepted three ballistic missiles fired toward the capital early on Saturday;
  two explosions were heard, no casualties or damage reported.
- **Hero 2 — Fire kills four at Iraq's Hartha power station.** A fire at the plant
  near Basra killed at least four and injured 30; the plant was running at about
  half its 800 MW capacity.
- **Hero 3 — COP31 slips into overtime with no deal in sight.** Climate talks in
  Antalya ran past their Friday deadline; the last draft dropped any mention of
  coal, oil and gas — and a $120bn adaptation target.

The grid covers KL Rahul's 136 in Wellington, Bitcoin crashing below $57,000,
Verstappen inheriting the Las Vegas pole, the Kryvyi Rih strike, NATO's warning
to Russia, Cyclone Akvan weakening over Odisha, the Riemann-proof checks, the
ATP Finals semi-finals, Spaniards abroad voting, and the Premier League's return.

## Date discipline

Every story was verified against its source publication date. The DATE CHECK box
on the page names what was left out and why — for example the Riyadh PIF Tower
strike and the ICJ Myanmar ruling were both Thursday 19 November, not 21 November,
and are not presented as 21 November news. Borderline items (Friday-evening events
reported in Saturday updates, Friday-night US sport, a Friday claim whose Saturday
verification checkpoint is the news) are flagged on the page. Full sourcing and
the rejected wrong-date traps are documented in `v1-research.md`.

## Files

- `entry.png` — the entry image (900×1024, PNG).
- `main.py` — entrypoint: copies `entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png`
  (default `/output`). Standard library only, no network, deterministic.
- `generate.py` — the program that drew `entry.png` (Pillow; original flat
  vector-style illustrations, no photographs).
- `v1-research.md` — story-by-story sources, date verification, rejected traps.

## Licence

MIT — see `LICENSE`.

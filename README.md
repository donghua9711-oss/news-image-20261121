# The World in One Day — Saturday 21 November 2026

[![make.fun — news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121)
[![Rank](https://make.fun/badge/news-image-20261121/donghua9711-oss/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121)
[![Reward](https://make.fun/badge/news-image-20261121/donghua9711-oss/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Output](https://img.shields.io/badge/output-1024%C3%971024%20PNG%20%E2%89%A4%201%20MiB-blue)](entry.png)

One image that sums up the world news of **Saturday 21 November 2026**: a one-page
newspaper. Thirty verified stories from seven regions — Iran's strike on Bahrain, the Kryvyi Rih missile, Mexico's capture of 'Chapo Isidro', COP31 running into overtime, the AI sell-off's correction, BepiColombo reaching Mercury and the FBI database breach — drawn, mapped and footnoted on a single page.

## The page

- Navy masthead with the day and a rainbow band of region
  counts, then a "day in UTC" timeline of five grounded
  moments.
- Three lead stories with artwork on top, then eight more
  illustrated cards — eleven drawn stories in all.
- A dot-matrix world map marking where it happened, and the
  remaining stories as one-line briefs.
- A date-check footer: everything printed happened, or was
  first reported, on Saturday 21 November 2026. Developing stories are framed as
  reports and claims are attributed.

## Run it

```bash
node main.ts
```

Running the program writes `entry.png` (1024×1024 PNG, under
the 1 MiB cap) to the output directory — `MAKEFUN_OUTPUT_DIR`
or `/output` — and nowhere else, byte-identical on every run.
The page itself is composed by `compose.py` from the artwork
in `assets/`; per-story sourcing lives in [SOURCES.md](SOURCES.md).

## License

MIT — see [LICENSE](LICENSE).

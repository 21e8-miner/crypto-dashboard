# Gödel Machine — GitHub Pages

Live interactive dashboard: **https://21e8-miner.github.io/crypto-dashboard/**

Self-contained HTML (no build step). Data: CoinGecko + multi-source metals.

Accuracy is measured, never self-reported:

- **Live scorecard**: BUY/SELL calls are scored against the realized 5-minute move.
- **Historical Replay**: one click replays the same engine over the last 24h of
  5-minute bars and reports its hit rate with 95% confidence intervals, next to a
  coin flip, a "last move continues" baseline, and always-long. It also tests
  whether abstaining filters out bad calls and how often each incompleteness type fires.

This file is a copy of `qwen_setup/expert/godel_wsj.html`; edit that file and re-copy.

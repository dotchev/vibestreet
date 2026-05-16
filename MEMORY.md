# MEMORY

Read first thing every run. Rewrite freely. Keep terse.

## Mandate (from README)

High return + low volatility over a multi-year horizon. US stocks/ETFs only, whole shares, $2/trade fee, cash ≥ 0, append-only ledger and journal.

## Core strategy

Diversified ETF core, three risk drivers (equity / duration / real assets) plus cash buffer. No single names yet — I haven't earned an edge there. No leverage, options, sector bets. Tilts kept small and intentional.

**Standing target allocation:**
- VOO 48% — S&P 500 core
- VXUS 14% — international ex-US (incl. EM)
- AVUV 5% — US small-cap value factor tilt
- BND 20% — US aggregate bonds
- IAU 8% — gold
- Cash 5% — buffer / optionality

≈ 66 / 20 / 8 / 6 across equity / bonds / gold / cash.

## Operating rules

- **Rebalance trigger:** any holding drifts ≥ ±5 percentage points from target, OR cash drifts outside 3–10%. Otherwise hold. Keeps trade count and fee drag low.
- **Per-run trade cap:** prefer ≤ 3 trades unless rebalancing requires more. Five trades/week = ~0.52% annual drag — meaningful.
- **No same-day reversals.** `verify.py` blocks two trades for the same (date, ticker) anyway.
- **Trade-date convention:** use the trading day whose close was the basis (typically the Friday before a Saturday run), not the run day.
- **Always run `python3 verify.py` before writing the journal.** Fix the data, never the script.

## Data sources (what works in this env)

- **Primary:** `stockanalysis.com/etf/<ticker>/history/` via WebFetch — clean historical tables.
- **Cross-check:** `marketbeat.com/stocks/NYSEARCA/<ticker>/chart/` via WebFetch is reliable; WebSearch snippets sometimes return stale or intraday quotes — prefer two WebFetch sources over a search snippet when they disagree.
- **Avoid:** `finance.yahoo.com/quote/.../history` — returns 503 to WebFetch. Google Finance redirects to consent flow. `nasdaq.com/.../historical` has timed out.
- **WebFetch caveat:** the summarizer occasionally mislabels day-of-week (e.g. calling Monday "Sunday"). The numeric prices in the same response have been correct — verify dates against the calendar, not the label.

## Things to evaluate over time (not now)

- Whether AVUV's value tilt is paying its way vs just holding more VOO.
- Whether to add a TIPS sleeve (SCHP) if real-rate regime shifts.
- Whether to swap IAU → physical-gold-plus-miners blend (GDX) for higher beta to gold cycles. Probably no — adds equity correlation.
- Tax-lot tracking is irrelevant here (paper trading, no tax), so always use simple average cost.

## Open questions / watchlist

- Track whether ±5pp drift band actually triggers — if 6 months in we've never rebalanced, that's a sign the band is too loose given low-vol assets like BND.

## File map

- `transactions.csv` — append-only ledger, one row per trade.
- `portfolio.csv` — current state, rewritten each run.
- `journal/YYYY-MM-DD.md` — append-only run log.
- `verify.py` — reconciliation; do not modify.
- `README.md` — charter; do not modify.

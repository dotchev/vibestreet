# MEMORY

Read first thing every run. Rewrite freely. Keep terse.

## Mandate (from README)

**Maximize 3-year rolling Sharpe ratio** (charter updated 2026-05-16). US stocks/ETFs only, whole shares, $2/trade fee, cash ≥ 0, append-only ledger and journal. No fixed end date.

Sharpe meaningfully measurable only with ≥13 weekly obs (rolling estimate, ~Q3 2026); true 3-year Sharpe needs 156 obs (~2029). Until then optimize for the strategy (diversification, low cost, low drift drag), not the metric.

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

## Benchmark (NASDAQ Composite, ^IXIC)

Compare on return + Sharpe every run. Inception baseline: **26,247.08** (2026-05-08 close).
Record the Friday ^IXIC level in each journal's benchmark table and carry the column forward —
since-inception excess return is then one lookup, not a re-fetch. As of 2026-06-12: port −0.46%
vs NDX −1.37% (ahead +0.91pp). Base case: this low-beta book lags in tech-led up-weeks and protects
in down-weeks (edge is risk-adjusted, not raw return) — but breadth weeks (intl/small-cap leading,
as 2026-06-12) can let it keep pace on the upside too. Port weekly stdev ~55% of NDX's so far.

## Operating rules

- **Rebalance trigger:** any holding drifts ≥ ±5 percentage points from target, OR cash drifts outside 3–10%. Otherwise hold. Keeps trade count and fee drag low.
- **Per-run trade cap:** prefer ≤ 3 trades unless rebalancing requires more. Five trades/week = ~0.52% annual drag — meaningful.
- **No same-day reversals.** `verify.py` blocks two trades for the same (date, ticker) anyway.
- **Trade-date convention:** use the trading day whose close was the basis (typically the Friday before a Saturday run), not the run day.
- **Always run `python3 verify.py` before writing the journal.** Fix the data, never the script.

## Data sources (what works in this env)

- **Primary:** `yfinance` (pip-install each run; README-preferred). `yf.download([...tickers, "^IXIC"], start=, end=, auto_adjust=False)["Close"]` returns clean daily closes for ETFs *and* the NASDAQ Composite in one call. Confirmed 2026-06-05.
- **Cross-check (independent):** `stockanalysis.com/etf/<ticker>/history/` via WebFetch — matched yfinance exactly on 2026-06-05. `marketbeat.com/stocks/NYSEARCA/<ticker>/chart/` also reliable. Verify ≥2 tickers each run; cross-check harder on big-move weeks.
- **Avoid:** `finance.yahoo.com/quote/.../history` 503s to WebFetch (but yfinance reaches Yahoo's *API* fine — only the HTML history page is blocked). Google Finance consent redirect. `nasdaq.com/.../historical` times out.
- **WebFetch caveat:** summarizer occasionally mislabels day-of-week; numeric prices in the same response have been correct — verify dates against the calendar, not the label.

## Things to evaluate over time (not now)

- Whether AVUV's value tilt is paying its way vs just holding more VOO.
- Whether to add a TIPS sleeve (SCHP) if real-rate regime shifts.
- Whether to swap IAU → physical-gold-plus-miners blend (GDX) for higher beta to gold cycles. Probably no — adds equity correlation.
- Tax-lot tracking is irrelevant here (paper trading, no tax), so always use simple average cost.

## Open questions / watchlist

- Track whether ±5pp drift band actually triggers — if 6 months in we've never rebalanced, that's a sign the band is too loose given low-vol assets like BND. No-trade streak: 5 weeks (since 2026-05-09 deployment). Largest drift to date: 0.84pp (IAU, 2026-06-12). Review point: ~12 weeks (late Aug 2026).
- **Gold (IAU) watch:** down 4 of first 5 weeks, −10.89% on cost, drift −0.84pp and widening (the only sleeve trending toward the band). Not actionable yet. Reassess sizing/thesis if drift reaches ≈ −2pp or the drawdown deepens materially.
- Build a Sharpe-tracking script once we have ~10+ weekly observations (reads `portfolio.csv` history from git, emits weekly returns + rolling Sharpe). At n=5 now; not worth building yet.
- **Regime watch (did NOT confirm):** the 2026-06-05 real-rates shock (BND *and* IAU falling *with* equities) was a one-session event — on 2026-06-12 BND recovered and behaved as a diversifier again; only IAU stayed weak. TIPS/SCHP sleeve stays parked. Re-arm this trigger only if bonds *and* gold again fall together with equities across multiple weeks.

## File map

- `transactions.csv` — append-only ledger, one row per trade.
- `portfolio.csv` — current state, rewritten each run.
- `journal/YYYY-MM-DD.md` — append-only run log.
- `verify.py` — reconciliation; do not modify.
- `README.md` — charter; do not modify.

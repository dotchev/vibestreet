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
since-inception excess return is then one lookup, not a re-fetch. As of 2026-06-26: port −1.58%
vs NDX −3.62% (**ahead +2.04pp** — raw-return lead flipped back after one protective down-week; was
behind −0.95pp on 06-18). Base case (now well established, symmetric): this low-beta book lags in
tech-led up-weeks (06-18: −1.88pp; 05-29: −1.24pp) and protects in down-weeks (06-26: +2.94pp;
06-05: +2.42pp) — edge is risk-adjusted, but in down-weeks raw return benefits too. Outperformed NDX
in **4 of 7** weeks, incl. **all 3 down-weeks**. The since-inception line keeps flipping with the
tape; don't over-read either direction. Port weekly stdev ~46% of NDX's so far (n=7).

## Operating rules

- **Rebalance trigger:** any holding drifts ≥ ±5 percentage points from target, OR cash drifts outside 3–10%. Otherwise hold. Keeps trade count and fee drag low.
- **Per-run trade cap:** prefer ≤ 3 trades unless rebalancing requires more. Five trades/week = ~0.52% annual drag — meaningful.
- **No same-day reversals.** `verify.py` blocks two trades for the same (date, ticker) anyway.
- **Trade-date convention:** use the trading day whose close was the basis (typically the Friday before a Saturday run), not the run day.
- **Holiday calendar:** US market holidays mean "last close" may be Thu (or earlier), not Fri — confirm the last trading day from the data, not the calendar. Confirmed: Juneteenth (Fri 06-19) closed markets → 06-20 run priced off Thu 06-18. **Next: 07-04 is a Saturday → Independence Day observed Fri 07-03 (full close), so the 07-04 run will likely price off Thu 07-02.**
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

- Track whether ±5pp drift band actually triggers — if 6 months in we've never rebalanced, that's a sign the band is too loose given low-vol assets like BND. No-trade streak: 7 weeks (since 2026-05-09 deployment). Largest drift to date: 1.00pp (IAU, 2026-06-26). Review point: ~12 weeks (late Aug 2026).
- **Gold (IAU) watch:** worst week of the sample on 06-26 (−3.49%), now −13.85% on cost (was −10.73%), drift −1.00pp (new max, still widening). Reassessed 06-27 → **hold**: drift only half the −2pp review level and a tenth of the rebalance band; selling = selling into a drawdown; BND diversified this week so no regime confirmation; long-horizon real-asset thesis intact. Still the only sleeve near any threshold. Re-arm: drift ≈ −2pp, OR gold falls *with* bonds for multiple weeks.
- Build a Sharpe-tracking script once we have ~10+ weekly observations (reads `portfolio.csv` history from git, emits weekly returns + rolling Sharpe). At n=7 now; not worth building yet.
- **Regime watch (still NOT confirmed):** 06-05 real-rates shock (BND *and* IAU falling *with* equities) remains a one-session event. On 06-12 and again **06-26 BND rose and diversified** while only IAU stayed weak — single-asset (idiosyncratic) weakness, not a regime. TIPS/SCHP sleeve stays parked. Re-arm only if bonds *and* gold again fall together with equities across multiple weeks.
- **Data TODO:** no reliable independent ^IXIC cross-check source found — stockanalysis/index/COMP (404), marketwatch/wsj/cnbc all blocked to WebFetch. ETF cross-checks (stockanalysis.com) still work and validate the shared yfinance pull by proxy. Find a working index source for big-move weeks.

## File map

- `transactions.csv` — append-only ledger, one row per trade.
- `portfolio.csv` — current state, rewritten each run.
- `journal/YYYY-MM-DD.md` — append-only run log.
- `verify.py` — reconciliation; do not modify.
- `README.md` — charter; do not modify.

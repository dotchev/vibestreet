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
since-inception excess return is then one lookup, not a re-fetch. As of 2026-07-10: port −0.01%
vs NDX +0.13% (**behind −0.14pp** — raw-return lead flipped back behind after two tech-led up-weeks;
was ahead +2.04pp on 06-26). Base case (well established, symmetric): this low-beta book lags in
tech-led up-weeks (07-02: −1.15; 07-10: −1.12; 06-18: −1.88; 05-29: −1.24pp) and protects in
**material** down-weeks (06-26: +2.94; 06-05: +2.42pp). Beaten NDX in **4 of 9** weeks. Correction to
the 06-27 journal: won the two *material* selloffs but NOT the marginal −0.08% week-1 (low beta gives
no help when the market barely moves) — "all 3 down-weeks" was imprecise. The since-inception line
keeps flipping (5 crossings now); don't over-read either direction. Port weekly stdev **45.4%** of
NDX's (n=9, stable ~46%).

## Operating rules

- **Rebalance trigger:** any holding drifts ≥ ±5 percentage points from target, OR cash drifts outside 3–10%. Otherwise hold. Keeps trade count and fee drag low.
- **Per-run trade cap:** prefer ≤ 3 trades unless rebalancing requires more. Five trades/week = ~0.52% annual drag — meaningful.
- **No same-day reversals.** `verify.py` blocks two trades for the same (date, ticker) anyway.
- **Trade-date convention:** use the trading day whose close was the basis (typically the Friday before a Saturday run), not the run day.
- **Holiday calendar:** US market holidays mean "last close" may be Thu (or earlier), not Fri — confirm the last trading day from the data, not the calendar. Confirmed: Juneteenth (Fri 06-19)→06-20 priced off Thu 06-18; Independence Day observed (Fri 07-03) fully closed markets → that week priced off Thu 07-02 (confirmed from data). **Next holiday: Labor Day, Mon 2026-09-07 (shifts a Monday, not a Fri close).**
- **Always run `python3 verify.py` before writing the journal.** Fix the data, never the script.
- **Keep runs on schedule.** 07-04 & 07-11 runs were both missed; 07-13 (Mon) caught up and reconstructed the two intermediate weekly marks — clean *only* because there were no trades. Gaps degrade the weekly-return series. Next run: **Sat 2026-07-18** (off Fri 07-17).

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

- Track whether ±5pp drift band actually triggers — if 6 months in we've never rebalanced, that's a sign the band is too loose given low-vol assets like BND. No-trade streak: 8 runs (since 2026-05-09 deployment). Largest drift to date: 1.05pp (IAU, 2026-07-10). Review point: ~late Aug 2026.
- **Gold (IAU) watch:** recovered on 07-10 (+0.91% over the 2wk gap), drawdown eased −13.85% → −13.06%, drift −1.05pp (flat, not widening). **Hold** — drift half the −2pp review level and a fifth of the rebalance band; on 07-10 gold rose *while bonds fell* (opposite of a regime); long-horizon real-asset thesis intact. Still the only sleeve near any threshold. Re-arm: drift ≈ −2pp, OR gold falls *with* bonds for multiple weeks.
- Build a Sharpe-tracking script once we have ~10+ weekly observations (reads `portfolio.csv` history from git, emits weekly returns + rolling Sharpe). At n=9 now; build around n≈13 (Q3 2026).
- **Regime watch (still NOT confirmed):** 06-05 real-rates shock (BND *and* IAU falling *with* equities) remains a one-session event. Since then diversifiers keep moving *opposite* each other (06-26: BND up, IAU down; 07-10: BND down, IAU up) — not a regime. TIPS/SCHP sleeve stays parked. Re-arm only if bonds *and* gold again fall together with equities across multiple weeks.
- **Data TODO:** no reliable independent ^IXIC cross-check source found — stockanalysis/index/COMP (404), marketwatch/wsj/cnbc all blocked to WebFetch. ETF cross-checks (stockanalysis.com) still work and validate the shared yfinance pull by proxy. Find a working index source for big-move weeks.

## File map

- `transactions.csv` — append-only ledger, one row per trade.
- `portfolio.csv` — current state, rewritten each run.
- `journal/YYYY-MM-DD.md` — append-only run log.
- `verify.py` — reconciliation; do not modify.
- `README.md` — charter; do not modify.

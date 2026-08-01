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
since-inception excess return is then one lookup, not a re-fetch. As of 2026-07-31: port −0.82%
vs NDX −3.33% (**ahead +2.51pp**; was +3.33pp — up-week gave back ~0.82pp, expected). Base case
(well established, both directions mapped): this low-beta book lags in tech-led up-weeks (07-31:
−0.89; 07-02: −1.15; 07-10: −1.12; 06-18: −1.88; 05-29: −1.24pp) and protects in down-weeks —
**material AND moderate** (07-24's −2.13% NDX still gave +1.77pp; the old "only material >2.5%" bar
was too high). Protection weeks: 07-24 +1.77; 07-17 +1.75; 06-26 +2.94; 06-05 +2.42pp — won **all 4**
down-weeks where NDX fell >2%. Still NO help in flat-to-up noise. Symmetric & predictable. Beaten
NDX in **6 of 12** weeks. Since-inception line flips a lot (don't over-read direction); durable edge
is risk-adjusted, not raw. Port weekly stdev **43.7%** of NDX's (n=12, stable ~44%). `python3 sharpe.py`.

## Operating rules

- **Rebalance trigger:** any holding drifts ≥ ±5 percentage points from target, OR cash drifts outside 3–10%. Otherwise hold. Keeps trade count and fee drag low.
- **Per-run trade cap:** prefer ≤ 3 trades unless rebalancing requires more. Five trades/week = ~0.52% annual drag — meaningful.
- **No same-day reversals.** `verify.py` blocks two trades for the same (date, ticker) anyway.
- **Trade-date convention:** use the trading day whose close was the basis (typically the Friday before a Saturday run), not the run day.
- **Holiday calendar:** US market holidays mean "last close" may be Thu (or earlier), not Fri — confirm the last trading day from the data, not the calendar. Confirmed: Juneteenth (Fri 06-19)→06-20 priced off Thu 06-18; Independence Day observed (Fri 07-03) fully closed markets → that week priced off Thu 07-02 (confirmed from data). **Next holiday: Labor Day, Mon 2026-09-07 (shifts a Monday, not a Fri close).**
- **Always run `python3 verify.py` before writing the journal.** Fix the data, never the script.
- **Keep runs on schedule.** On track — series clean and continuous through n=12 (07-25 off 07-24, 08-01 off 07-31). Gaps degrade the weekly-return series. Next run: **Sat 2026-08-08** (off Fri 08-07).

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

- Track whether ±5pp drift band actually triggers — if 6 months in we've never rebalanced, that's a sign the band is too loose given low-vol assets like BND. No-trade streak: 11 runs (since 2026-05-09 deployment). Largest drift to date: 1.13pp (IAU, 2026-07-17). Review point: ~late Aug 2026.
- **Gold (IAU) watch — quiet 07-31.** Gold −0.08%, so drawdown deepened marginally −14.22% → −14.29% and drift widened −1.03 → −1.09pp — noise, not a trend. **Hold** — long-horizon real-asset thesis intact. Re-arm: drift ≈ −2pp, OR gold + bonds falling *with equities* for multiple weeks.
- **AVUV watch (is the value tilt paying its way?):** now mapped both directions — 07-31 AVUV +0.00% vs VOO +1.11% (**lagged UP**), mirroring the two prior down-weeks it *outperformed* (07-24 −0.06 vs −0.59%; 07-17 +1.13 vs −1.54%). Confirmed a distinct **lower-beta factor**: lags up, cushions down. "Pays its way over a full cycle?" still open. Best sleeve on cost (+4.54%). Keep logging.
- **Sharpe-tracking:** `sharpe.py` + `nav_history.csv` (append one row/run from the journal benchmark table, then `python3 sharpe.py`). At **n=12** now; **n=13 milestone NEXT run (08-08)** — rolling estimate becomes minimally meaningful. Vol ratio 43.7% is the stable durable signal; naive Sharpe still noise.
- **Regime watch (still NOT confirmed):** 06-05 real-rates shock (BND *and* IAU falling *with* equities) remains a one-session event. Diversifiers mostly anti-correlate (06-26 BND↑/IAU↓; 07-10 BND↓/IAU↑; 07-17 BND↑/IAU↓; 07-24 BND↓/IAU↑). **07-31 both dipped slightly (BND −0.11%, IAU −0.08%) — but equities ROSE, so this is normal rotation into risk, NOT the regime.** The trigger is bonds+gold falling *with equities down*. TIPS/SCHP stays parked. Re-arm only if bonds *and* gold fall together *with equities* across multiple weeks.
- **Data TODO:** no reliable independent ^IXIC cross-check source found — stockanalysis/index/COMP (404), marketwatch/wsj/cnbc all blocked to WebFetch. ETF cross-checks (stockanalysis.com) still work and validate the shared yfinance pull by proxy. Find a working index source for big-move weeks.

## File map

- `transactions.csv` — append-only ledger, one row per trade.
- `portfolio.csv` — current state, rewritten each run.
- `journal/YYYY-MM-DD.md` — append-only run log.
- `nav_history.csv` — weekly NAV + NDX series (append one row/run from the journal benchmark table).
- `sharpe.py` — weekly-return / Sharpe / vol-ratio analysis (reads nav_history.csv). Not reconciliation.
- `verify.py` — reconciliation; do not modify.
- `README.md` — charter; do not modify.

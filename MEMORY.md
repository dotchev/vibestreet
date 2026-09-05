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
since-inception excess return is then one lookup, not a re-fetch. As of 2026-09-04: port **+1.94%**
vs NDX **+0.99%** (**ahead +0.95pp**; compressed +2.14 → +1.23 → +0.95pp over two up-weeks as NDX
recovers — leads built on down-week protection give back on up-weeks, expected). Base case (well
established, both directions mapped): **the edge is a DOWN-CAPTURE edge; the up-week lag scales with the
SIZE of the up move.** Lags **big** (>~+1.5%) tech-led up-weeks in proportion (08-07: **−2.45pp** on
+5.19% NDX; 06-18: −1.88; 05-29: −1.24; 07-02: −1.15; 07-10: −1.12; 07-31: −0.89pp). **Small/flat
up-weeks now 3/5** (wins 08-14, 05-22, 06-12; misses 08-28 −0.91pp & 09-04 −0.28pp — two in a row, both
**diversifier-driven**). Refinement (reinforced 09-04): small-up-week wins need the diversifiers to
*hold flat*; when they don't, book lags even a small up move. **Whether the lag lands red or green
depends on equity-carry BREADTH:** 08-28 narrow carry (VOO only) + gold reversal → red −0.06%; 09-04
broad carry (VXUS +1.02% led, AVUV +1.08%) despite BND *and* IAU both soft → green +0.12%.
**Protects in EVERY >2% down-week — 5/5** (06-26 +2.94; 06-05 +2.42; 07-24 +1.77; 07-17 +1.75; 08-21
+1.66pp) — the most reliable leg. Symmetric & predictable (~half-capture at ~half-risk). Beaten NDX in
**8 of 17** weeks. Raw-return lead built almost entirely on down-weeks — **durable edge is risk-adjusted,
not raw**. Port weekly stdev **45.2%** of NDX's (n=17, dead stable <half). n=17 naive Sharpe **0.73 vs NDX
0.25** (both ticked up: NDX mean lifted by 2nd positive week; port's stdev tightened as +0.12% sat on the
mean); port mean still above NDX (+0.120 vs +0.091%) with <half vol. `python3 sharpe.py`.

## Operating rules

- **Rebalance trigger:** any holding drifts ≥ ±5 percentage points from target, OR cash drifts outside 3–10%. Otherwise hold. Keeps trade count and fee drag low.
- **Per-run trade cap:** prefer ≤ 3 trades unless rebalancing requires more. Five trades/week = ~0.52% annual drag — meaningful.
- **No same-day reversals.** `verify.py` blocks two trades for the same (date, ticker) anyway.
- **Trade-date convention:** use the trading day whose close was the basis (typically the Friday before a Saturday run), not the run day.
- **Holiday calendar:** US market holidays mean "last close" may be Thu (or earlier), not Fri — confirm the last trading day from the data, not the calendar. Confirmed: Juneteenth (Fri 06-19)→06-20 priced off Thu 06-18; Independence Day observed (Fri 07-03) fully closed markets → that week priced off Thu 07-02 (confirmed from data). **Next holiday: Labor Day, Mon 2026-09-07 — 09-05 priced off a normal full week (Fri 09-04, done). The holiday shuts the 09-12 week's Monday → that week is 4 sessions (Tue 09-08–Fri 09-11); still price off Fri 09-11. Confirm last trading day from data, not calendar.**
- **Always run `python3 verify.py` before writing the journal.** Fix the data, never the script.
- **Keep runs on schedule.** On track — series clean and continuous through n=17 (08-29 off 08-28, 09-05 off 09-04). Gaps degrade the weekly-return series. Next run: **Sat 2026-09-12** (off Fri 09-11; that week's Mon 09-07 is Labor Day → 4-session week, Friday close still the mark).

## Data sources (what works in this env)

- **Primary:** `yfinance` (pip-install each run; README-preferred). `yf.download([...tickers, "^IXIC"], start=, end=, auto_adjust=False)["Close"]` returns clean daily closes for ETFs *and* the NASDAQ Composite in one call. Confirmed 2026-06-05.
- **yfinance CAN LAG a full trading day in this env** (seen 2026-08-29: NaN close for the latest Fri 08-28 across *all* tickers, 3 retries; last complete bar Thu 08-27). **But the lag is intermittent — 09-05 it was clean** (populated Fri 09-04 first pull; its 08-28 overlap matched last week's verified journal to the cent on all six). So yfinance stays primary; just check the latest Friday isn't NaN before trusting it. Diagnostic that a NaN *is* a lag not a holiday: yf skips weekend rows entirely but *includes* the un-loaded Friday as a NaN row → its calendar counts it as a session. **Fallback when it lags:** price off `stockanalysis.com` (ETFs) + `investing.com/indices/nasdaq-composite-historical-data` (index) + `marketbeat` (cross-check), and validate each on the last overlap day yf *does* have (matched to the cent 08-27). Don't fall back to a stale Thursday when Friday's real, verified close exists.
- **Cross-check (independent):** `stockanalysis.com/etf/<ticker>/history/` via WebFetch — matched yfinance exactly on 2026-06-05 & 08-27. `marketbeat.com/stocks/NYSEARCA/<ticker>/chart/` also reliable. **Index now has a working source: `investing.com/indices/nasdaq-composite-historical-data`** (gave 08-28 = 26,402.42, confirmed by WebSearch). Verify ≥2 tickers each run; cross-check harder on big-move weeks.
- **Avoid:** `finance.yahoo.com/quote/.../history` 503s to WebFetch (but yfinance reaches Yahoo's *API* fine — only the HTML history page is blocked). Google Finance consent redirect. `nasdaq.com/.../historical` times out.
- **WebFetch caveat:** summarizer occasionally mislabels day-of-week; numeric prices in the same response have been correct — verify dates against the calendar, not the label.

## Things to evaluate over time (not now)

- Whether AVUV's value tilt is paying its way vs just holding more VOO.
- Whether to add a TIPS sleeve (SCHP) if real-rate regime shifts.
- Whether to swap IAU → physical-gold-plus-miners blend (GDX) for higher beta to gold cycles. Probably no — adds equity correlation.
- Tax-lot tracking is irrelevant here (paper trading, no tax), so always use simple average cost.

## Open questions / watchlist

- **±5pp drift band — REVIEWED 2026-08-15, keep as-is.** Never triggered because real drift is genuinely tiny (max ever 1.13pp IAU 07-17; 08-28 max −0.75pp BND), the *intended* behavior of a diversified book, not a mis-set band. Tightening would add fee drag for no risk-allocation gain. Only residual watch: slow one-way accumulation the band can't catch — add an annual calendar backstop **only if** directional drift builds past ~2–3pp. Watch item: **BND is now the max-drift sleeve and building one-way** (−0.75 → −0.87pp as bonds softened two weeks); VOO steady +0.62pp. Two weeks ≠ trend; revisit BND only near ~−2pp. No-trade streak: **16 runs** (since 2026-05-09 deployment).
- **Gold (IAU) watch — TWO-WAY VOL NOW ON TAPE BACK-TO-BACK.** +7.23% (08-07), +0.74% (08-14), **+5.48% (08-21, saved a −2% NDX week single-handedly)**, then **−3.42% (08-28, dragged a flat book on a +0.85% NDX up-week)**. Cleanest illustration yet that the sleeve gives *and* takes — it's judged over a **cycle, not a week**. Cost P/L round-tripped **−2.34% → −5.68%** on the 08-28 reversal, then eased to **−6.17%** on a quiet 09-04 (IAU −0.51%, noise — the reversal did *not* extend into a rout; drift −0.64pp). 08-21 remains the **canonical example of why the diversifier is held** (pays off when equities sell off); 08-28 is the price of that optionality on a quiet week. **Hold** — one down-week doesn't unwind a full-cycle thesis. Only re-arm to *reduce* if drift ≈ −2pp returns (nowhere near).
- **AVUV is a TWO-WAY FACTOR TILT, not a hedge.** 08-14 it LED up (+1.46% vs VOO +0.41%); 08-21 it fell MORE than VOO (−1.77% vs −1.39%). Higher beta in *both* directions — amplifies the equity move up and down. So downside cushioning is gold/bonds' job, not AVUV's; re-frame "pays its way?" around **factor return over a full cycle**, not downside protection. 09-04 it again LED up (+1.08% vs VOO +0.11%), part of the broad equity carry that kept a weak-diversifier up-week green. Best cost P/L of the book (**+5.92%**). Keep logging.
- **Sharpe-tracking:** `sharpe.py` + `nav_history.csv` (append one row/run from the journal benchmark table, then `python3 sharpe.py`). At **n=17**: naive Sharpe **0.73 vs NDX 0.25** (both up: NDX mean lifted 0.071→0.091% on a 2nd positive week; port's stdev tightened 1.225→1.186% as +0.12% sat on the mean, nudging Sharpe 0.71→0.73); port weekly mean still above NDX (+0.120 vs +0.091%) with <half the vol. *Encouraging ≠ established*: means unstable; true 3-yr needs n≈156 (~2029). Vol ratio **45.2%** (dead stable, 17 wks) is the durable signal; still <half NDX.
- **Regime watch (still NOT confirmed):** 06-05 real-rates shock (BND *and* IAU falling *with* equities) remains a one-session event. **08-21 equity selloff: gold ROSE +5.48%, bonds ~flat (−0.11%) — classic diversification, NOT the regime.** Note bonds did *not* hedge this selloff (gold did) — holding *multiple* diversifiers is the point; at least one tends to work. The regime trigger is bonds+gold falling *with equities down*. **09-04 counter-example (clarifies the trigger):** BND −0.50% *and* IAU −0.51% both fell — but equities ROSE, so this is NOT the regime, just diversifiers lagging an up-week. The trigger requires equities *down* simultaneously. TIPS/SCHP stays parked. Re-arm only if bonds *and* gold fall together *with equities down* across multiple weeks.
- **Data TODO — RESOLVED 2026-08-29.** Independent ^IXIC source found: **`investing.com/indices/nasdaq-composite-historical-data`** (history table, gave 08-28 = 26,402.42, cross-confirmed by WebSearch; reconciled to −0.52% off the known Thu close). Still dead: stockanalysis/index/COMP (404), marketbeat/COMP (= Compass Inc, wrong entity), marketwatch/wsj/cnbc (blocked). Use investing.com for the index when yfinance lags or on big-move weeks.

## File map

- `transactions.csv` — append-only ledger, one row per trade.
- `portfolio.csv` — current state, rewritten each run.
- `journal/YYYY-MM-DD.md` — append-only run log.
- `nav_history.csv` — weekly NAV + NDX series (append one row/run from the journal benchmark table).
- `sharpe.py` — weekly-return / Sharpe / vol-ratio analysis (reads nav_history.csv). Not reconciliation.
- `verify.py` — reconciliation; do not modify.
- `README.md` — charter; do not modify.

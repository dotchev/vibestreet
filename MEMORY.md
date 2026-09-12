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
since-inception excess return is then one lookup, not a re-fetch. As of 2026-09-11: port **+0.90%**
vs NDX **+0.33%** (**ahead +0.57pp**, was +0.95pp). Lead compressed 4 straight weeks
(+2.14→+1.23→+0.95→+0.57); first three were up-week give-backs (expected), but the 4th (09-11) was the
book *falling more* than NDX on a down-week — a real loss of ground, not a give-back.

**Base case — the edge is a TAIL phenomenon (both directions mapped):**
- **Big (>2%) down-weeks: protect, 5/5** (06-26 +2.94; 06-05 +2.42; 07-24 +1.77; 07-17 +1.75; 08-21 +1.66pp) — the most reliable leg. ~half-capture at ~half-risk.
- **Big (>~+1.5%) tech-led up-weeks: lag in proportion to the up move** (08-07 −2.45 on +5.19% NDX; 06-18 −1.88; 05-29 −1.24; 07-02 −1.15; 07-10 −1.12; 07-31 −0.89pp).
- **Small/flat weeks (EITHER direction): book lags when the diversifiers move against it.** Small-up **3/5** (wins 08-14, 05-22, 06-12; misses 08-28 −0.91, 09-04 −0.28); small/flat-down **0/2** (05-15 −0.82; 09-11 −0.36). 09-11 is the down-side mirror of the small-up misses: NDX −0.66% but book −1.02% because bonds+gold+ALL equity sleeves fell together — diversification had nothing to cushion with, and the ex-US/small-cap/gold tilts fell harder than the mega-cap-carried index.

**Takeaway: the edge lives in the TAILS (big moves) and washes out in the middle.** Raw-return lead built on big down-weeks; **durable edge is risk-adjusted, not raw.** Beaten NDX **8 of 18** weeks. Port weekly stdev **46.3%** of NDX's (n=18, 18 wks <half; the 45.2→46.3 tick is a one-week artifact — large port move vs small NDX move). n=18 naive Sharpe **0.35 vs NDX 0.14** — BOTH ~halved this week as the shared down-week pulled both means down (port 0.120→0.057%, NDX 0.091→0.049%); textbook mean-instability, not a regime change. `python3 sharpe.py`.

## Operating rules

- **Rebalance trigger:** any holding drifts ≥ ±5 percentage points from target, OR cash drifts outside 3–10%. Otherwise hold. Keeps trade count and fee drag low.
- **Per-run trade cap:** prefer ≤ 3 trades unless rebalancing requires more. Five trades/week = ~0.52% annual drag — meaningful.
- **No same-day reversals.** `verify.py` blocks two trades for the same (date, ticker) anyway.
- **Trade-date convention:** use the trading day whose close was the basis (typically the Friday before a Saturday run), not the run day.
- **Holiday calendar:** US market holidays mean "last close" may be Thu (or earlier), not Fri — confirm the last trading day from the data, not the calendar. Confirmed: Juneteenth (Fri 06-19)→06-20 priced off Thu 06-18; Independence Day observed (Fri 07-03)→07-04 week priced off Thu 07-02; **Labor Day (Mon 09-07) shut the 09-12 week's Monday → priced off Fri 09-11, 4-session week (confirmed: no 09-07 row in yf data).** Next holiday: **Thanksgiving, Thu 2026-11-26** (+ early close Fri 11-27). Weeks 09-19 through 11-20 are all normal full weeks.
- **Always run `python3 verify.py` before writing the journal.** Fix the data, never the script.
- **Keep runs on schedule.** On track — series clean and continuous through n=18 (09-12 off Fri 09-11). Gaps degrade the weekly-return series. Next run: **Sat 2026-09-19** (off Fri 09-18; no holiday that week).

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

- **±5pp drift band — REVIEWED 2026-08-15, keep as-is.** Never triggered because real drift is genuinely tiny (max ever 1.13pp IAU 07-17), the *intended* behavior of a diversified book, not a mis-set band. Tightening would add fee drag for no risk-allocation gain. Only residual watch: slow one-way accumulation the band can't catch — add an annual calendar backstop **only if** directional drift builds past ~2–3pp. **BND max-drift −0.87pp (flat vs last wk — bonds & book fell in lockstep); IAU −0.71pp**; both underweight & both fell 09-11, but far from the 2–3pp watch. VOO steady +0.74pp. No-trade streak: **17 runs** (since 2026-05-09 deployment).
- **Gold (IAU) watch — TWO-WAY VOL, judged over a CYCLE not a week.** +7.23% (08-07), **+5.48% (08-21, saved a −2% NDX week single-handedly — canonical example of *why* the diversifier is held)**, then a soft patch: −3.42% (08-28), −0.51% (09-04), **−2.01% (09-11)**. Cost P/L −2.34% → −5.68% → −6.17% → **−8.06%, now the book's deepest drawdown.** 09-11 note: gold fell *with* equities & bonds (see regime watch), not the usual equities-down/gold-up hedge. **Hold** — the sleeve's job is the big-down-week save (08-21); paying for that optionality on soft weeks is the cost. Re-arm to *reduce* only if drift ≈ −2pp (at −0.71pp, nowhere near).
- **AVUV is a TWO-WAY FACTOR TILT, not a hedge.** Higher beta *both* directions: led up 08-14 (+1.46% vs VOO +0.41%) & 09-04 (+1.08% vs +0.11%); fell hardest 08-21 (−1.77%) & **09-11 (−1.91% vs VOO −0.77%)**. Amplifies equity moves up and down — downside cushioning is gold/bonds' job, not AVUV's. Judge "pays its way?" on **factor return over a full cycle**, not downside protection. Cost P/L +5.92% → **+3.89%** after the down-week. Keep logging.
- **Sharpe-tracking:** `sharpe.py` + `nav_history.csv` (append one row/run from the journal benchmark table, then `python3 sharpe.py`). At **n=18**: naive Sharpe **0.35 vs NDX 0.14** — BOTH ~halved this week when the shared down-week pulled both means down (port 0.120→0.057%, NDX 0.091→0.049%). Textbook proof the mean is untrustworthy at this n: one week nearly halved both ratios. *Encouraging ≠ established*; true 3-yr needs n≈156 (~2029). Vol ratio **46.3%** (18 wks <half) is the durable signal — the 45.2→46.3 tick is a one-week artifact (large port move vs small NDX move), not drift.
- **Regime watch — FIRST WEEKLY INSTANCE 09-11 (still NOT confirmed).** Trigger = bonds+gold falling *with equities down*, across multiple weeks. 06-05 fit but was one *session*. **09-11 is the first full *week* of the pattern:** BND −1.01%, IAU −2.01%, equities down (VOO −0.77%, NDX −0.66%) — all three risk drivers red together. Caveats: one week ≠ trend; equity move was small (−0.66%, not a 06-05-style shock); magnitudes modest. **ACTION: watch 09-18 — if all-three-down repeats, that's 2 consecutive weeks → seriously evaluate a response.** Nuance for that eval: if the driver is rising *real rates*, TIPS/SCHP fall too (real duration) — only short-duration/cash truly helps; TIPS win only on *inflation* surprises. SCHP parked. (Contrast: 08-21 gold ROSE as equities fell = classic diversification, NOT regime; 09-04 bonds+gold fell but equities ROSE = not regime. Trigger needs all three down *together*.)
- **Data TODO — RESOLVED 2026-08-29.** Independent ^IXIC source found: **`investing.com/indices/nasdaq-composite-historical-data`** (history table, gave 08-28 = 26,402.42, cross-confirmed by WebSearch; reconciled to −0.52% off the known Thu close). Still dead: stockanalysis/index/COMP (404), marketbeat/COMP (= Compass Inc, wrong entity), marketwatch/wsj/cnbc (blocked). Use investing.com for the index when yfinance lags or on big-move weeks.

## File map

- `transactions.csv` — append-only ledger, one row per trade.
- `portfolio.csv` — current state, rewritten each run.
- `journal/YYYY-MM-DD.md` — append-only run log.
- `nav_history.csv` — weekly NAV + NDX series (append one row/run from the journal benchmark table).
- `sharpe.py` — weekly-return / Sharpe / vol-ratio analysis (reads nav_history.csv). Not reconciliation.
- `verify.py` — reconciliation; do not modify.
- `README.md` — charter; do not modify.

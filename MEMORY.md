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
since-inception excess return is then one lookup, not a re-fetch. As of 2026-09-18: port **+0.58%**
vs NDX **+1.05%** (**BEHIND −0.47pp**, was ahead +0.57pp) — **lead gone, first cumulative deficit since inception.**
Compressed 5 straight weeks (+2.14→+1.23→+0.95→+0.57→−0.47) and crossed to a deficit. NOT a failure:
expected for a half-vol book in a narrow low-vol bull. The lead was built on big down-weeks; a 4-week
small-move grind (no big move since 08-21, lagged all 4: 08-28/09-04/09-11/09-18) bled it away.

**Base case — the edge is a TAIL phenomenon (both directions mapped):**
- **Big (>2%) down-weeks: protect, 5/5** (06-26 +2.94; 06-05 +2.42; 07-24 +1.77; 07-17 +1.75; 08-21 +1.66pp) — the most reliable leg. **This is the falsifiable test: if a big down-week is NOT protected, that's the real strategy problem. Until then, raw-return lag in a grind-up is the insurance premium, not a failure.**
- **Big (>~+1.5%) tech-led up-weeks: lag in proportion to the up move** (08-07 −2.45 on +5.19% NDX; 06-18 −1.88; 05-29 −1.24; 07-02 −1.15; 07-10 −1.12; 07-31 −0.89pp).
- **Small/flat weeks (EITHER direction): book lags when the diversifiers move against it.** Small-up **3/6** (wins 08-14, 05-22, 06-12; misses 08-28 −0.91, 09-04 −0.28, 09-18 −1.04); small/flat-down **0/2** (05-15 −0.82; 09-11 −0.36). 09-18: NDX +0.72% but VOO *flat* (−0.11%) = narrow mega-cap leadership; ex-US (−1.45%) & small-cap (−2.04%) tilts fell → book −0.32%. Book has now MISSED 4 straight small-move weeks — the grind that erased the lead.

**Takeaway: the edge lives in the TAILS (big moves) and washes out — even bleeds — in the middle.** Raw lead built on big down-weeks; **durable edge is risk-adjusted, not raw.** Beaten NDX **8 of 19** weeks. Port weekly stdev **46.3%** of NDX's (n=19, 19 wks <half — the stable signal). n=19 naive Sharpe **0.23 vs NDX 0.24 (edge gone, dead heat)** — but it swung 0.73/0.25→0.35/0.14→0.23/0.24 in 3 wks (one NDX up-week + one book down-week flipped the ranking); textbook mean-instability, NOT a regime change. `python3 sharpe.py`.

## Operating rules

- **Rebalance trigger:** any holding drifts ≥ ±5 percentage points from target, OR cash drifts outside 3–10%. Otherwise hold. Keeps trade count and fee drag low.
- **Per-run trade cap:** prefer ≤ 3 trades unless rebalancing requires more. Five trades/week = ~0.52% annual drag — meaningful.
- **No same-day reversals.** `verify.py` blocks two trades for the same (date, ticker) anyway.
- **Trade-date convention:** use the trading day whose close was the basis (typically the Friday before a Saturday run), not the run day.
- **Holiday calendar:** US market holidays mean "last close" may be Thu (or earlier), not Fri — confirm the last trading day from the data, not the calendar. Confirmed: Juneteenth (Fri 06-19)→06-20 priced off Thu 06-18; Independence Day observed (Fri 07-03)→07-04 week priced off Thu 07-02; **Labor Day (Mon 09-07) shut the 09-12 week's Monday → priced off Fri 09-11, 4-session week (confirmed: no 09-07 row in yf data).** Next holiday: **Thanksgiving, Thu 2026-11-26** (+ early close Fri 11-27). Weeks 09-19 through 11-20 are all normal full weeks.
- **Always run `python3 verify.py` before writing the journal.** Fix the data, never the script.
- **NO git in any form** — not even read-only `git status` (charter says "any form"; slipped once on 09-19, harmless but avoid). Track changed files via `ls`/your own edits; the workflow stages & commits.
- **Keep runs on schedule.** On track — series clean and continuous through n=19 (09-19 off Fri 09-18). Gaps degrade the weekly-return series. Next run: **Sat 2026-09-26** (off Fri 09-25; no holiday that week).

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

- **±5pp drift band — REVIEWED 2026-08-15, keep as-is.** Never triggered because real drift is genuinely tiny (max ever 1.13pp IAU 07-17), the *intended* behavior of a diversified book, not a mis-set band. Tightening would add fee drag for no risk-allocation gain. Only residual watch: slow one-way accumulation the band can't catch — add an annual calendar backstop **only if** directional drift builds past ~2–3pp. Max drift now **VOO +0.84pp** (held up while others fell); **BND −0.82pp, IAU −0.64pp** both underweight, far from the 2–3pp watch. No-trade streak: **18 runs** (since 2026-05-09 deployment).
- **Gold (IAU) watch — TWO-WAY VOL, judged over a CYCLE not a week.** +7.23% (08-07), **+5.48% (08-21, saved a −2% NDX week single-handedly — canonical example of *why* the diversifier is held)**, then a soft patch: −3.42% (08-28), −0.51% (09-04), −2.01% (09-11), **then +0.64% (09-18) — reverted to diversifier role (rose while equity tilts fell), which de-escalated the regime watch.** Cost P/L −8.06% → **−7.47%** (still deepest drawdown, off its low). **Hold** — the sleeve's job is the big-down-week save (08-21); paying for that optionality on soft weeks is the cost. Re-arm to *reduce* only if drift ≈ −2pp (at −0.64pp, nowhere near).
- **AVUV is a TWO-WAY FACTOR TILT, not a hedge.** Higher beta *both* directions: led up 08-14 (+1.46% vs VOO +0.41%) & 09-04 (+1.08% vs +0.11%); fell hardest 08-21 (−1.77%), 09-11 (−1.91% vs VOO −0.77%) & **09-18 (−2.04% vs VOO −0.11%)**. Amplifies equity moves up and down — downside cushioning is gold/bonds' job, not AVUV's. Judge "pays its way?" on **factor return over a full cycle**, not downside protection. Cost P/L +3.89% → **+1.77%** (small-cap/ex-US lagging hard in the narrow mega-cap tape). Keep logging.
- **Sharpe-tracking:** `sharpe.py` + `nav_history.csv` (append one row/run from the journal benchmark table, then `python3 sharpe.py`). At **n=19**: naive Sharpe **0.23 vs NDX 0.24 (edge gone, dead heat)** — swung 0.73/0.25→0.35/0.14→0.23/0.24 in 3 wks as one NDX up-week + one book down-week pulled book mean down (0.057→0.037%) and NDX up (0.049→0.084%). Textbook proof the mean is untrustworthy at this n: the ranking flipped on 2 weeks of data. True 3-yr needs n≈156 (~2029). Vol ratio **46.3%** (19 wks <half) is the durable signal, unchanged — book delivers ~NDX-comparable naive Sharpe at under half the vol.
- **Regime watch — DE-ESCALATED 2026-09-18, back to dormant.** Trigger = bonds+gold falling *with equities down*, across multiple weeks. 09-11 was the first full *week* of the pattern (BND −1.01%, IAU −2.01%, equities down) and I flagged 09-18 as the decider. **09-18 did NOT repeat: gold ROSE +0.64%, bonds flat (−0.03%), VOO flat (−0.11%)** — gold reverted to diversifier. So 09-11 stays a single isolated week, not a trend. Re-arm only if bonds+gold+equities go down *together* again for ≥2 consecutive weeks. Nuance if it ever fires: rising *real rates* sink TIPS/SCHP too (real duration) — only short-duration/cash truly helps; TIPS win only on *inflation* surprises. SCHP parked. (Contrast: 08-21 & 09-18 gold ROSE as equities fell = classic diversification, NOT regime; 09-04 bonds+gold fell but equities ROSE = not regime. Trigger needs all three down *together*.)
- **Data TODO — RESOLVED 2026-08-29.** Independent ^IXIC source found: **`investing.com/indices/nasdaq-composite-historical-data`** (history table, gave 08-28 = 26,402.42, cross-confirmed by WebSearch; reconciled to −0.52% off the known Thu close). Still dead: stockanalysis/index/COMP (404), marketbeat/COMP (= Compass Inc, wrong entity), marketwatch/wsj/cnbc (blocked). Use investing.com for the index when yfinance lags or on big-move weeks.

## File map

- `transactions.csv` — append-only ledger, one row per trade.
- `portfolio.csv` — current state, rewritten each run.
- `journal/YYYY-MM-DD.md` — append-only run log.
- `nav_history.csv` — weekly NAV + NDX series (append one row/run from the journal benchmark table).
- `sharpe.py` — weekly-return / Sharpe / vol-ratio analysis (reads nav_history.csv). Not reconciliation.
- `verify.py` — reconciliation; do not modify.
- `README.md` — charter; do not modify.

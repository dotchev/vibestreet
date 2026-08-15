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
since-inception excess return is then one lookup, not a re-fetch. As of 2026-08-14: port **+2.29%**
vs NDX **+1.84%** (**ahead +0.45pp**; rebuilt from +0.21pp on a flat week). Base case (well
established, both directions mapped): **the up-week lag scales with the SIZE of the up move.** Lags
**big** (>~+1.5%) tech-led up-weeks in proportion (08-07: **−2.45pp** on +5.19% NDX; 06-18: −1.88;
05-29: −1.24; 07-02: −1.15; 07-10: −1.12; 07-31: −0.89pp) BUT **wins small/flat up-weeks** where the
index can't run and non-tech sleeves carry (08-14 +0.24 on +0.14; 05-22 +0.32 on +0.45; 06-12 +0.14
on +0.70 — **3/3**). Protects in down-weeks — material AND moderate: won **all 4** where NDX fell >2%
(06-26 +2.94; 06-05 +2.42; 07-24 +1.77; 07-17 +1.75pp). Symmetric & predictable (~half-capture at
~half-risk). Beaten NDX in **7 of 14** weeks (half). Raw-return lead flips a lot & stays thin
(+0.45pp) — **durable edge is risk-adjusted, not raw**. Port weekly stdev **46.0%** of NDX's (n=14,
stable <half). n=14 naive Sharpe **0.94 vs NDX 0.43**; port mean now fractionally *above* NDX (+0.170
vs +0.168%) with <half vol — ideal combo but razor-thin/unstable. `python3 sharpe.py`.

## Operating rules

- **Rebalance trigger:** any holding drifts ≥ ±5 percentage points from target, OR cash drifts outside 3–10%. Otherwise hold. Keeps trade count and fee drag low.
- **Per-run trade cap:** prefer ≤ 3 trades unless rebalancing requires more. Five trades/week = ~0.52% annual drag — meaningful.
- **No same-day reversals.** `verify.py` blocks two trades for the same (date, ticker) anyway.
- **Trade-date convention:** use the trading day whose close was the basis (typically the Friday before a Saturday run), not the run day.
- **Holiday calendar:** US market holidays mean "last close" may be Thu (or earlier), not Fri — confirm the last trading day from the data, not the calendar. Confirmed: Juneteenth (Fri 06-19)→06-20 priced off Thu 06-18; Independence Day observed (Fri 07-03) fully closed markets → that week priced off Thu 07-02 (confirmed from data). **Next holiday: Labor Day, Mon 2026-09-07 (shifts a Monday, not a Fri close).**
- **Always run `python3 verify.py` before writing the journal.** Fix the data, never the script.
- **Keep runs on schedule.** On track — series clean and continuous through n=14 (08-08 off 08-07, 08-15 off 08-14). Gaps degrade the weekly-return series. Next run: **Sat 2026-08-22** (off Fri 08-21).

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

- **±5pp drift band — REVIEWED 2026-08-15, keep as-is.** Never triggered because real drift is genuinely tiny (max ever 1.13pp IAU 07-17; 08-14 ±0.84pp), the *intended* behavior of a diversified book, not a mis-set band. Tightening would add fee drag for no risk-allocation gain. Only residual watch: slow one-way accumulation the band can't catch — add an annual calendar backstop **only if** directional drift builds past ~2–3pp (none now). No-trade streak: **13 runs** (since 2026-05-09 deployment).
- **Gold (IAU) watch — +7.23% (08-07) then +0.74% (08-14).** Drawdown clawed back −14.29% → −8.09% → −7.42%; drift −1.09 → −0.76pp. Bleed has stopped; vindicates holding the diversifier through the drawdown. Still worst sleeve on cost but improving. **Hold** — real-asset thesis intact. Only re-arm to *reduce* if drift ≈ −2pp returns.
- **AVUV watch (is the value tilt paying its way?):** 08-14 AVUV **+1.46% LED the book**, out-running VOO (+0.41%) on a flat week — first clear week the value tilt added alpha, not just lower beta. Prior weeks lagged up / cushioned down (08-07 +1.28 vs VOO +3.50%; 07-24 −0.06 vs −0.59%). Best sleeve on cost (**+7.42%**). "Pays its way over a full cycle?" still open but ticking favorable. Keep logging.
- **Sharpe-tracking:** `sharpe.py` + `nav_history.csv` (append one row/run from the journal benchmark table, then `python3 sharpe.py`). At **n=14**: naive Sharpe **0.94 vs NDX 0.43**; port weekly mean now fractionally *above* NDX (+0.170 vs +0.168%) with <half the vol — the ideal combo. *Encouraging ≠ established*: mean gap is 0.002pp & unstable; true 3-yr needs n≈156 (~2029). Vol ratio **46.0%** (stable) is the durable signal; still <half NDX.
- **Regime watch (still NOT confirmed):** 06-05 real-rates shock (BND *and* IAU falling *with* equities) remains a one-session event. Diversifiers mostly anti-correlate or move independently. **08-07 both ROSE (BND +0.24%, IAU +7.23%) with equities up — risk-on, NOT the regime.** The trigger is bonds+gold falling *with equities down*. TIPS/SCHP stays parked. Re-arm only if bonds *and* gold fall together *with equities* across multiple weeks.
- **Data TODO:** no reliable independent ^IXIC cross-check source found — stockanalysis/index/COMP (404), marketwatch/wsj/cnbc all blocked to WebFetch. ETF cross-checks (stockanalysis.com) still work and validate the shared yfinance pull by proxy. Find a working index source for big-move weeks.

## File map

- `transactions.csv` — append-only ledger, one row per trade.
- `portfolio.csv` — current state, rewritten each run.
- `journal/YYYY-MM-DD.md` — append-only run log.
- `nav_history.csv` — weekly NAV + NDX series (append one row/run from the journal benchmark table).
- `sharpe.py` — weekly-return / Sharpe / vol-ratio analysis (reads nav_history.csv). Not reconciliation.
- `verify.py` — reconciliation; do not modify.
- `README.md` — charter; do not modify.

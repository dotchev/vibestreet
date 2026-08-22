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
since-inception excess return is then one lookup, not a re-fetch. As of 2026-08-21: port **+1.88%**
vs NDX **−0.25%** (**ahead +2.14pp**; jumped from +0.45pp — **NDX round-tripped NEGATIVE** on a −2.05%
week). Base case (well established, both directions mapped): **the edge is a DOWN-CAPTURE edge; the
up-week lag scales with the SIZE of the up move.** Lags **big** (>~+1.5%) tech-led up-weeks in
proportion (08-07: **−2.45pp** on +5.19% NDX; 06-18: −1.88; 05-29: −1.24; 07-02: −1.15; 07-10: −1.12;
07-31: −0.89pp) BUT **wins small/flat up-weeks** where the index can't run and non-tech sleeves carry
(08-14 +0.24 on +0.14; 05-22 +0.32 on +0.45; 06-12 +0.14 on +0.70 — **3/3**). **Protects in EVERY >2%
down-week — now 5/5** (06-26 +2.94; 06-05 +2.42; 07-24 +1.77; 07-17 +1.75; 08-21 +1.66pp) — the most
reliable leg of the pattern. Symmetric & predictable (~half-capture at ~half-risk). Beaten NDX in
**8 of 15** weeks. Raw-return lead built almost entirely on down-weeks — **durable edge is
risk-adjusted, not raw**. Port weekly stdev **45.3%** of NDX's (n=15, stable <half). n=15 naive Sharpe
**0.76 vs NDX 0.05** (NDX's collapsed as the −2% week erased its cumulative mean); port mean now
*clearly* above NDX (+0.133 vs +0.020%) with <half vol. `python3 sharpe.py`.

## Operating rules

- **Rebalance trigger:** any holding drifts ≥ ±5 percentage points from target, OR cash drifts outside 3–10%. Otherwise hold. Keeps trade count and fee drag low.
- **Per-run trade cap:** prefer ≤ 3 trades unless rebalancing requires more. Five trades/week = ~0.52% annual drag — meaningful.
- **No same-day reversals.** `verify.py` blocks two trades for the same (date, ticker) anyway.
- **Trade-date convention:** use the trading day whose close was the basis (typically the Friday before a Saturday run), not the run day.
- **Holiday calendar:** US market holidays mean "last close" may be Thu (or earlier), not Fri — confirm the last trading day from the data, not the calendar. Confirmed: Juneteenth (Fri 06-19)→06-20 priced off Thu 06-18; Independence Day observed (Fri 07-03) fully closed markets → that week priced off Thu 07-02 (confirmed from data). **Next holiday: Labor Day, Mon 2026-09-07 (shifts a Monday, not a Fri close).**
- **Always run `python3 verify.py` before writing the journal.** Fix the data, never the script.
- **Keep runs on schedule.** On track — series clean and continuous through n=15 (08-15 off 08-14, 08-22 off 08-21). Gaps degrade the weekly-return series. Next run: **Sat 2026-08-29** (off Fri 08-28; no holiday — Labor Day Mon 09-07 shifts a Monday, so 08-29 & 09-05 both price off normal Fridays).

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

- **±5pp drift band — REVIEWED 2026-08-15, keep as-is.** Never triggered because real drift is genuinely tiny (max ever 1.13pp IAU 07-17; 08-21 max −0.79pp BND), the *intended* behavior of a diversified book, not a mis-set band. Tightening would add fee drag for no risk-allocation gain. Only residual watch: slow one-way accumulation the band can't catch — add an annual calendar backstop **only if** directional drift builds past ~2–3pp (none now; VOO drift actually *shrank* +0.84→+0.35pp as equities fell 08-21). No-trade streak: **14 runs** (since 2026-05-09 deployment).
- **Gold (IAU) watch — THESIS VINDICATED.** +7.23% (08-07), +0.74% (08-14), **+5.48% (08-21)** — and 08-21's rip was the single reason the book barely moved (−0.39%) in a −2.05% NDX week (+0.40pp contribution, top sleeve). Held through a −14.29% drawdown on the diversifier thesis; drawdown now pared to **−2.34%**, drift −0.33pp. This is the **canonical example of why the diversifier is held** — it pays off precisely when equities sell off. **Hold.** Only re-arm to *reduce* if drift ≈ −2pp returns.
- **AVUV is a TWO-WAY FACTOR TILT, not a hedge.** 08-14 it LED up (+1.46% vs VOO +0.41%); 08-21 it fell MORE than VOO (−1.77% vs −1.39%). Higher beta in *both* directions — amplifies the equity move up and down. So downside cushioning is gold/bonds' job, not AVUV's; re-frame "pays its way?" around **factor return over a full cycle**, not downside protection. Green on cost (**+5.52%**). Keep logging.
- **Sharpe-tracking:** `sharpe.py` + `nav_history.csv` (append one row/run from the journal benchmark table, then `python3 sharpe.py`). At **n=15**: naive Sharpe **0.76 vs NDX 0.05** (NDX's collapsed — the −2% week erased its cumulative mean, leaving ~zero-drift high-vol); port weekly mean now *clearly* above NDX (+0.133 vs +0.020%) with <half the vol. *Encouraging ≠ established*: means unstable; true 3-yr needs n≈156 (~2029). Vol ratio **45.3%** (stable) is the durable signal; still <half NDX.
- **Regime watch (still NOT confirmed):** 06-05 real-rates shock (BND *and* IAU falling *with* equities) remains a one-session event. **08-21 equity selloff: gold ROSE +5.48%, bonds ~flat (−0.11%) — classic diversification, NOT the regime.** Note bonds did *not* hedge this selloff (gold did) — holding *multiple* diversifiers is the point; at least one tends to work. The regime trigger is bonds+gold falling *with equities down*. TIPS/SCHP stays parked. Re-arm only if bonds *and* gold fall together *with equities* across multiple weeks.
- **Data TODO:** no reliable independent ^IXIC cross-check source found — stockanalysis/index/COMP (404), marketwatch/wsj/cnbc all blocked to WebFetch. ETF cross-checks (stockanalysis.com) still work and validate the shared yfinance pull by proxy. Find a working index source for big-move weeks.

## File map

- `transactions.csv` — append-only ledger, one row per trade.
- `portfolio.csv` — current state, rewritten each run.
- `journal/YYYY-MM-DD.md` — append-only run log.
- `nav_history.csv` — weekly NAV + NDX series (append one row/run from the journal benchmark table).
- `sharpe.py` — weekly-return / Sharpe / vol-ratio analysis (reads nav_history.csv). Not reconciliation.
- `verify.py` — reconciliation; do not modify.
- `README.md` — charter; do not modify.

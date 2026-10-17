# MEMORY

## Strategy (current working hypothesis — mine to revise; README overrides this)

Fixed strategic allocation, rebalanced by bands, **not** market-timed. Targets:
**VOO 48% · VXUS 14% · AVUV 5% · BND 20% · IAU 8% · $CASH 5%.**

- **Rebalance bands:** trade only when a sleeve drifts ≥ **±5pp** from target, or cash leaves the **3–10%** band. Otherwise hold. (As of 2026-10-17: 21 runs, 0 trades — all band-consistent; drifts still tiny, max VOO +1.29pp and *shrinking* as the Oct selloff rebalanced the book toward target.)
- **Thesis:** a half-vol, globally diversified book. Portfolio weekly vol ≈ **44% of NASDAQ's** (stable every week since inception — *the* durable signal). The return edge lives in the **tails** (big equity down-weeks: protected **6/6**) and **bleeds in narrow grind-up / melt-up weeks**. **Proof point 2026-10-16:** AI-led crash, NDX −4.48% (worst week since Apr-2025), book only −1.06% (+3.42pp, best week in series) — that single tail-week erased the entire 5-month since-inception gap (−3.56pp → **+0.04pp ahead**). Mandate = beat NDX on return AND Sharpe over ≥1yr; naive Sharpe is noise at this n (true 3-yr needs n≈156, ~2029) — judge by the vol ratio, not the mean-driven ranking.
- **Do NOT** chase NDX by concentrating into mega-cap tech — that abandons the thesis for a worse, higher-fee index clone. Core falsification = a big equity down-week that is **not** protected.

## Regime (updated 2026-10-17)

**Two layers now: (1) rising-rate regime (named 2026-09-16) + (2) a NEW AI-valuation/debt risk-off.** Week of 10-13 was the pivot:
- **AI-debt unwind = dominant driver of the −4.48% NDX week.** IMF (10-13) flagged AI correction as a top-3 stability risk (~$650B AI debt, $1.4T circular-revenue promises); **CoreWeave −25%/wk** (CDS ~60% default); chips −8 straight days (longest since 2008); 20 biggest AI/semi names −$1T. This is the narrow-mega-cap-tech tail the book deliberately underweights.
- **Rate regime re-intensified, didn't soften:** hot **Sept CPI (10-14): 3.7% headline / 2.6% core**, both above consensus → Dec Fed tightening back in play, cuts off the table. Last week's "softening" (hike odds 51%→19%) reversed.
- **Oil/geopolitics:** **Brent ~$110** (first since May) on **US–Iran / Strait-of-Hormuz** escalation (vessel attacks) — inflation push + safe-haven bid.
- **Hedge mechanism confirmed through the cross-currents:** despite hot CPI, **BND rallied +0.85%** — 10-yr spiked to 5.30% on CPI day then slid to ~5.07% Fri as money rotated tech→bonds. **Risk-off flight-to-safety beat the inflation yield-rise.** That's the growth-scare tail BND exists to hedge.

- **BND + IAU (~26%) hedge *different* tails** (BND = deflation / growth-scare; IAU = inflation / currency / geopolitical). 10-16 proved it: a growth-scare → **BND shone (+0.85%, clean), IAU choppy but flat (−0.67%)** — pulled both ways (hot CPI + oil bullish, yield-spike bearish). Don't conflate them into "one bet."
- **NEW contagion tripwire (top watch):** this week credit *rallied* (flight TO quality). **If investment-grade credit / BND starts cracking alongside equities (correlations → 1), the growth-scare hedge breaks — that's the signal to reassess.** Watch AI-credit events (CoreWeave-type) spilling into IG.
- **Gold tripwire (unchanged):** cut IAU only if it **fails to protect on a genuine equity down-week** (NDX ↓ >~2% while IAU *also falls materially*), or a 2nd hike lands and it bleeds with zero down-week contribution for weeks. 10-16 did **not** trigger it: NDX −4.48% but IAU only −0.67% (held ~3.8pp vs equities); rate-sensitive so noisier than BND, but net did its job. Do **not** sell the hedge merely because it's down on cost (IAU −11.85% on May cost).

## Data sources (what works in this env)

- **Primary: `yfinance`** (pip-install each run). `yf.download([...tickers,"^IXIC"], start=, end=, auto_adjust=False)["Close"]` → clean daily closes for ETFs + NASDAQ Composite in one call. Clean first-pull confirmed repeatedly, incl. through 2026-10-16.
- **yfinance can intermittently LAG a full trading day** (latest Friday comes back as a NaN row — seen 2026-08-29, not since). Diagnostic that it's a *lag* not a holiday: yf omits weekend rows but *includes* the un-loaded Friday as NaN. **Check the latest Friday isn't NaN before trusting; never fall back to a stale Thursday when a real, verified Friday close exists.**
- **Cross-check every run (≥2 ETFs + the index; harder on big-move weeks):** `stockanalysis.com/etf/<ticker>/history/` (ETFs) and `investing.com/indices/nasdaq-composite-historical-data` (^IXIC) via WebFetch — matched yfinance **to the cent** every run (latest: VOO/IAU/BND/^IXIC on all three volatile days 10-14→10-16). `marketbeat.com` also reliable. **Also validate the seam:** the prior run's Friday close must match this pull to the cent (held every run so far).
- **Avoid:** `finance.yahoo.com/quote/.../history` (503s to WebFetch; yf's *API* path is fine), Google Finance (consent redirect), `nasdaq.com/.../historical` (times out).
- **WebFetch caveat:** the summarizer can mislabel day-of-week; trust the numeric price against the calendar date, not the label.

## File map

- `transactions.csv` — append-only trade ledger. `portfolio.csv` — current state, rewritten each run.
- `journal/YYYY-MM-DD.md` — append-only run log (one per run, **current-dated; never backdate**).
- `nav_history.csv` — weekly NAV + ^IXIC series (one row per Friday); drives `sharpe.py`. **Keep weekly spacing uniform** — if a run is missed, backfill that Friday's mark-to-market NAV (deterministic when no trades occurred) so Sharpe stays honest. Did this for the missed 2026-09-26 run (09-25 point).
- `sharpe.py` — weekly-return / Sharpe / vol-ratio analysis (reads nav_history). Not reconciliation.
- `verify.py` — reconciliation; **do not modify.** `README.md` — charter; **do not modify.**

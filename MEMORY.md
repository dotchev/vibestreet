# MEMORY

## Strategy (current working hypothesis — mine to revise; README overrides this)

Fixed strategic allocation, rebalanced by bands, **not** market-timed. Targets:
**VOO 48% · VXUS 14% · AVUV 5% · BND 20% · IAU 8% · $CASH 5%.**

- **Rebalance bands:** trade only when a sleeve drifts ≥ **±5pp** from target, or cash leaves the **3–10%** band. Otherwise hold. (As of 2026-10-10: 20 runs, 0 trades — all band-consistent; drifts still tiny, max ~1.7pp VOO.)
- **Thesis:** a half-vol, globally diversified book. Portfolio weekly vol ≈ **46% of NASDAQ's** (stable every week since inception — *the* durable signal). The return edge lives in the **tails** (big equity down-weeks: protected 5/5) and **bleeds in narrow grind-up / melt-up weeks**. Mandate = beat NDX on return AND Sharpe over ≥1yr; naive Sharpe is noise at this n (true 3-yr needs n≈156, ~2029) — judge by the vol ratio, not the mean-driven ranking.
- **Do NOT** chase NDX by concentrating into mega-cap tech — that abandons the thesis for a worse, higher-fee index clone. Core falsification = a big equity down-week that is **not** protected.

## Regime (updated 2026-10-10)

**Rising-rate regime (named 2026-09-16, Fed's first hike since 2023), now softening at the margin.** As of 10-09: **Oct 2nd-hike odds fell ~51%→~19%** on a soft jobs report; 10-yr hit **5.349% (24-yr high) on 10-05** then eased to ~5.27% by 10-09 on a strong 30-yr auction. Effect reversed for a week: **BND + IAU bounced together** on the yield pullback (IAU +1.18%, BND +0.40%) after weeks of bleeding together — confirms the drag is *rate-regime-dependent, not structural.* Yields still 20+ yr highs → headwind relaxed, not gone. **CPI (week of 10-13) is the swing factor.** Gold still ~−22% off its 2026-01-29 high.

- **BND + IAU (~26%) are rate-correlated on the downside** but hedge *different* tails (BND = deflation / growth-scare; IAU = inflation / currency / geopolitical) — monitor the co-movement, don't conflate them into "one bet."
- **Gold tripwire:** cut IAU only if it **fails to protect on the next real equity down-week** (NDX ↓ >~2% while IAU also falls), or a 2nd hike lands and it keeps bleeding with zero down-week contribution for several weeks. Do **not** sell the hedge merely because it's down during a melt-up. (10-08 check: on NDX −1.25% day, IAU +0.78% / BND +0.31% / AVUV +0.84% — ballast held.)

## Data sources (what works in this env)

- **Primary: `yfinance`** (pip-install each run). `yf.download([...tickers,"^IXIC"], start=, end=, auto_adjust=False)["Close"]` → clean daily closes for ETFs + NASDAQ Composite in one call. Clean first-pull confirmed repeatedly, incl. through 2026-10-09.
- **yfinance can intermittently LAG a full trading day** (latest Friday comes back as a NaN row — seen 2026-08-29, not since). Diagnostic that it's a *lag* not a holiday: yf omits weekend rows but *includes* the un-loaded Friday as NaN. **Check the latest Friday isn't NaN before trusting; never fall back to a stale Thursday when a real, verified Friday close exists.**
- **Cross-check every run (≥2 ETFs + the index; harder on big-move weeks):** `stockanalysis.com/etf/<ticker>/history/` (ETFs) and `investing.com/indices/nasdaq-composite-historical-data` (^IXIC) via WebFetch — matched yfinance **to the cent** every run (latest: VOO/IAU/^IXIC on 10-08 & 10-09). `marketbeat.com` also reliable. **Also validate the seam:** the prior run's Friday close must match this pull to the cent (held every run so far).
- **Avoid:** `finance.yahoo.com/quote/.../history` (503s to WebFetch; yf's *API* path is fine), Google Finance (consent redirect), `nasdaq.com/.../historical` (times out).
- **WebFetch caveat:** the summarizer can mislabel day-of-week; trust the numeric price against the calendar date, not the label.

## File map

- `transactions.csv` — append-only trade ledger. `portfolio.csv` — current state, rewritten each run.
- `journal/YYYY-MM-DD.md` — append-only run log (one per run, **current-dated; never backdate**).
- `nav_history.csv` — weekly NAV + ^IXIC series (one row per Friday); drives `sharpe.py`. **Keep weekly spacing uniform** — if a run is missed, backfill that Friday's mark-to-market NAV (deterministic when no trades occurred) so Sharpe stays honest. Did this for the missed 2026-09-26 run (09-25 point).
- `sharpe.py` — weekly-return / Sharpe / vol-ratio analysis (reads nav_history). Not reconciliation.
- `verify.py` — reconciliation; **do not modify.** `README.md` — charter; **do not modify.**

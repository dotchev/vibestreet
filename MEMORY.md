# MEMORY

## Data sources (what works in this env)

- **Primary:** `yfinance` (pip-install each run; README-preferred). `yf.download([...tickers, "^IXIC"], start=, end=, auto_adjust=False)["Close"]` returns clean daily closes for ETFs *and* the NASDAQ Composite in one call. Confirmed 2026-06-05.
- **yfinance CAN LAG a full trading day in this env** (seen 2026-08-29: NaN close for the latest Fri 08-28 across *all* tickers, 3 retries; last complete bar Thu 08-27). **But the lag is intermittent — 09-05 it was clean** (populated Fri 09-04 first pull; its 08-28 overlap matched last week's verified journal to the cent on all six). So yfinance stays primary; just check the latest Friday isn't NaN before trusting it. Diagnostic that a NaN *is* a lag not a holiday: yf skips weekend rows entirely but *includes* the un-loaded Friday as a NaN row → its calendar counts it as a session. **Fallback when it lags:** price off `stockanalysis.com` (ETFs) + `investing.com/indices/nasdaq-composite-historical-data` (index) + `marketbeat` (cross-check), and validate each on the last overlap day yf *does* have (matched to the cent 08-27). Don't fall back to a stale Thursday when Friday's real, verified close exists.
- **Cross-check (independent):** `stockanalysis.com/etf/<ticker>/history/` via WebFetch — matched yfinance exactly on 2026-06-05 & 08-27. `marketbeat.com/stocks/NYSEARCA/<ticker>/chart/` also reliable. **Index now has a working source: `investing.com/indices/nasdaq-composite-historical-data`** (gave 08-28 = 26,402.42, confirmed by WebSearch). Verify ≥2 tickers each run; cross-check harder on big-move weeks.
- **Avoid:** `finance.yahoo.com/quote/.../history` 503s to WebFetch (but yfinance reaches Yahoo's *API* fine — only the HTML history page is blocked). Google Finance consent redirect. `nasdaq.com/.../historical` times out.
- **WebFetch caveat:** summarizer occasionally mislabels day-of-week; numeric prices in the same response have been correct — verify dates against the calendar, not the label.

## File map

- `transactions.csv` — append-only ledger, one row per trade.
- `portfolio.csv` — current state, rewritten each run.
- `journal/YYYY-MM-DD.md` — append-only run log.
- `nav_history.csv` — weekly NAV + NDX series (append one row/run: Friday date, portfolio value, ^IXIC close).
- `sharpe.py` — weekly-return / Sharpe / vol-ratio analysis (reads nav_history.csv). Not reconciliation.
- `verify.py` — reconciliation; do not modify.
- `README.md` — charter; do not modify.

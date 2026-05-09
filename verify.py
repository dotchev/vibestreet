#!/usr/bin/env python3
"""Verify portfolio.csv reconciles with transactions.csv.

Checks performed:
  Ledger integrity (transactions.csv) — exits 2 if any fail:
    - shares per row > 0
    - fee per row == $2
    - SELL never exceeds shares currently held
    - cash never goes negative after applying a row
    - action is BUY or SELL
    - dates are non-decreasing (each row's date >= previous row's date)
    - a given ticker is traded at most once per date

  Reconciliation (portfolio.csv vs. derived state) — exits 1 if any fail:
    - portfolio has a $CASH row
    - portfolio cash matches cash derived from replaying the ledger
    - per-ticker share counts match the ledger's net shares
    - no portfolio ticker is missing from the ledger (and vice versa)

  Internal portfolio consistency — exits 1 if any fail:
    - shares, price, value parse as numbers
    - shares >= 0
    - only $CASH may have zero shares (sold-out positions must be removed)
    - value == shares * price (within $0.01)
"""
import argparse
import csv
import sys
from collections import defaultdict
from decimal import Decimal

STARTING_CASH = Decimal("100000")
FEE = Decimal("2")
TOLERANCE = Decimal("0.01")
CASH = "$CASH"


def derive_state(tx_path):
    """Replay the ledger to derive cash and per-ticker share counts.

    Raises ValueError on any ledger-integrity violation (see module docstring).
    Returns (cash, {ticker: shares}) with zero-share tickers dropped.
    """
    cash = STARTING_CASH
    shares = defaultdict(int)
    prev_date = ""  # YYYY-MM-DD strings sort lexicographically
    seen_today = set()  # (date, ticker) pairs seen so far
    with open(tx_path) as f:
        # enumerate from 2 because row 1 is the CSV header
        for i, row in enumerate(csv.DictReader(f), start=2):
            if not row.get("date"):
                continue  # tolerate blank trailing lines
            date = row["date"].strip()
            action = row["action"].strip().upper()
            ticker = row["ticker"].strip()
            n = int(row["shares"])
            price = Decimal(row["price"])
            fee = Decimal(row["fee"])
            # Per-row integrity checks
            if n <= 0:
                raise ValueError(f"tx row {i}: shares must be > 0, got {n}")
            if fee != FEE:
                raise ValueError(f"tx row {i}: fee must be {FEE}, got {fee}")
            # Dates must be non-decreasing — the ledger is chronological
            if date < prev_date:
                raise ValueError(
                    f"tx row {i}: date {date} is before previous row's date {prev_date}"
                )
            # A ticker may only be traded once per date (consolidate same-day actions)
            if (date, ticker) in seen_today:
                raise ValueError(
                    f"tx row {i}: {ticker} already traded on {date} — one trade per ticker per day"
                )
            seen_today.add((date, ticker))
            prev_date = date
            if action == "BUY":
                # BUY: cash decreases by notional + fee; shares increase
                cash -= n * price + fee
                shares[ticker] += n
            elif action == "SELL":
                # SELL: must not exceed current holdings; cash gets proceeds minus fee
                if shares[ticker] < n:
                    raise ValueError(
                        f"tx row {i}: SELL {n} {ticker} but only hold {shares[ticker]}"
                    )
                cash += n * price - fee
                shares[ticker] -= n
            else:
                raise ValueError(f"tx row {i}: unknown action {action!r}")
            # Cash must never go negative even momentarily
            if cash < 0:
                raise ValueError(f"tx row {i}: cash went negative ({cash})")
    return cash, {t: n for t, n in shares.items() if n != 0}


def load_portfolio(p_path):
    cash = None
    shares = {}
    rows = []
    with open(p_path) as f:
        for row in csv.DictReader(f):
            if not row.get("ticker"):
                continue
            rows.append(row)
            t = row["ticker"].strip()
            if t == CASH:
                cash = Decimal(row["shares"])
            else:
                shares[t] = int(row["shares"])
    return cash, shares, rows


def verify(tx_path, p_path):
    errors = []
    derived_cash, derived_shares = derive_state(tx_path)
    port_cash, port_shares, port_rows = load_portfolio(p_path)

    # Check 1: portfolio cash matches what the ledger says it should be
    if port_cash is None:
        errors.append(f"portfolio.csv missing {CASH} row")
    elif abs(port_cash - derived_cash) > TOLERANCE:
        errors.append(
            f"cash mismatch: portfolio={port_cash}, derived={derived_cash}"
        )

    # Check 2: per-ticker share counts match the ledger
    # (union of both sides catches orphans: tickers in portfolio not in ledger,
    # and tickers in ledger not in portfolio)
    for t in sorted(set(derived_shares) | set(port_shares)):
        d, p = derived_shares.get(t, 0), port_shares.get(t, 0)
        if d != p:
            errors.append(f"{t} shares: portfolio={p}, derived={d}")

    # Check 3: each portfolio row is internally consistent
    for row in port_rows:
        t = row["ticker"].strip()
        try:
            sh, pr, v = Decimal(row["shares"]), Decimal(row["price"]), Decimal(row["value"])
        except Exception:
            errors.append(f"{t}: non-numeric shares/price/value")
            continue
        if sh < 0:
            errors.append(f"{t}: negative shares ({sh})")
        # Only $CASH may be zero; any other ticker with 0 shares should have
        # been removed from the portfolio (sold out positions don't belong here).
        if t != CASH and sh == 0:
            errors.append(f"{t}: zero shares — drop the row when fully sold")
        # value column must equal shares * price (allows tiny rounding diffs)
        if abs(sh * pr - v) > TOLERANCE:
            errors.append(f"{t}: value {v} != shares*price {sh * pr}")

    return errors, derived_cash, derived_shares


def main():
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Exit codes: 0 = OK, 1 = reconciliation mismatch, 2 = ledger integrity error.",
    )
    ap.add_argument(
        "--transactions",
        default="transactions.csv",
        metavar="PATH",
        help="path to the transactions ledger CSV (default: %(default)s)",
    )
    ap.add_argument(
        "--portfolio",
        default="portfolio.csv",
        metavar="PATH",
        help="path to the portfolio state CSV (default: %(default)s)",
    )
    args = ap.parse_args()
    try:
        errors, cash, holdings = verify(args.transactions, args.portfolio)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 2
    if errors:
        print("FAIL — reconciliation errors:")
        for e in errors:
            print(f"  - {e}")
        return 1
    print(f"OK — cash ${cash}, {len(holdings)} non-cash holding(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Weekly-return + Sharpe tracker for the VibeStreet book vs NASDAQ Composite.

Reads nav_history.csv (append one row per run: friday,portfolio_value,ndx —
source of truth is each journal's benchmark table) and prints weekly returns,
sample stdev, naive annualized Sharpe (rf=0, x sqrt(52)), the portfolio/NDX vol
ratio, and since-inception cumulative returns.

NOT a reconciliation tool (that's verify.py). This is analysis only — read the
CAVEAT it prints. Usage: python3 sharpe.py [--n LAST_N] [--csv PATH]
"""
import argparse
import csv
from statistics import mean, stdev

ANN = 52 ** 0.5  # naive weekly->annual scaling
START_CAPITAL = 100000.0  # portfolio since-inception base (journal convention; pv[0]=99990 is post opening-fee NAV)


def load(path):
    rows = []
    with open(path) as f:
        for r in csv.DictReader(f):
            if not r.get("friday"):
                continue
            rows.append((r["friday"], float(r["portfolio_value"]), float(r["ndx"])))
    return rows


def returns(series):
    return [series[i] / series[i - 1] - 1 for i in range(1, len(series))]


def stats(rets):
    if len(rets) < 2:
        return None
    m, s = mean(rets), stdev(rets)  # sample stdev (ddof=1)
    return m, s, (m / s * ANN if s else float("nan"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", default="nav_history.csv")
    ap.add_argument("--n", type=int, default=0, help="use only the last N weekly returns")
    a = ap.parse_args()
    rows = load(a.csv)
    dates = [r[0] for r in rows]
    pv = [r[1] for r in rows]
    nx = [r[2] for r in rows]
    pr, nr = returns(pv), returns(nx)
    if a.n and a.n < len(pr):
        pr, nr, dates = pr[-a.n:], nr[-a.n:], dates[-a.n - 1:]

    print(f"Weekly returns (n={len(pr)} obs, {dates[0]} .. {dates[-1]}):\n")
    print(f"{'Friday':12} {'Port %':>8} {'NDX %':>8} {'Diff pp':>8}")
    for i in range(len(pr)):
        d = dates[i + 1] if len(dates) == len(pr) + 1 else dates[i]
        print(f"{d:12} {pr[i]*100:>+7.2f}% {nr[i]*100:>+7.2f}% {(pr[i]-nr[i])*100:>+7.2f}")

    ps, ns = stats(pr), stats(nr)
    print(f"\n{'':10} {'wk mean':>9} {'wk stdev':>9} {'naive Sharpe':>13}")
    for name, st in (("Portfolio", ps), ("NASDAQ", ns)):
        if st:
            print(f"{name:10} {st[0]*100:>+8.3f}% {st[1]*100:>8.3f}% {st[2]:>13.2f}")
    if ps and ns and ns[1]:
        print(f"\nPortfolio vol / NASDAQ vol : {ps[1]/ns[1]*100:.1f}%  (the durable signal)")
    if not a.n:  # since-inception only meaningful on the full series
        pcum, ncum = pv[-1] / START_CAPITAL - 1, nx[-1] / nx[0] - 1
        print(f"Since inception            : port {pcum*100:+.2f}%  "
              f"vs NDX {ncum*100:+.2f}%  -> {(pcum-ncum)*100:+.2f}pp")
    beat = sum(1 for i in range(len(pr)) if pr[i] > nr[i])
    print(f"Weeks beating NASDAQ       : {beat}/{len(pr)}")
    print("\nCAVEAT: mean is a tiny, unstable number; naive Sharpe is noise until "
          "n>=13 (~Q3 2026) and only meaningful at n=156 (~2029). Trust the vol ratio.")


if __name__ == "__main__":
    main()

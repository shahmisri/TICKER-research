
from datetime import date

# EDITABLE INPUTS
DECISION_DATE = "2026-03-31"

ROWS = [
    (1, "AAA", "2026-01", "2026-02-10", 101.0),
    (2, "AAA", "2026-02", "2026-03-10", 104.0),
    (3, "AAA", "2026-03", "2026-04-10", 109.0),
    (4, "AAA", "2026-02", "2026-03-25", 103.0),
    (5, "BBB", "2026-01", "2026-02-10", 98.0),
    (6, "BBB", "2026-02", "2026-03-10", 97.0),
    (7, "BBB", "2026-02", "2026-03-10", 97.0),
    (8, "BBB", "2026-03", "2026-04-10", 92.0),
    (9, "CCC", "2026-01", "2026-02-10", 110.0),
    (10, "CCC", "2026-02", "2026-04-05", 112.0),
    (11, "", "2026-02", "2026-03-10", 99.0),
    (12, "CCC", "2026-02", "2026-03-10", 111.0),
]


def clean(rows, cutoff=None):
    funnel = []

    # Rule 1: Quarantine missing tickers
    removed = [r for r in rows if not r[1].strip()]
    rows = [r for r in rows if r[1].strip()]
    funnel.append(("Quarantined: no ticker", removed))

    # Rule 2: Remove exact duplicates
    seen = set()
    kept = []
    removed = []

    for r in rows:
        signature = r[1:]
        if signature in seen:
            removed.append(r)
        else:
            seen.add(signature)
            kept.append(r)

    rows = kept
    funnel.append(("Exact duplicate", removed))

    # Rule 3: Remove future publications
    if cutoff:
        removed = [r for r in rows if r[3] > cutoff]
        rows = [r for r in rows if r[3] <= cutoff]
    else:
        removed = []

    funnel.append(("Published after decision date", removed))

    # Rule 4: Keep latest publication per ticker/month
    newest = {}

    for r in rows:
        key = (r[1], r[2])

        if key not in newest or (
            r[3], r[0]
        ) > (
            newest[key][3], newest[key][0]
        ):
            newest[key] = r

    selected = {r[0] for r in newest.values()}
    removed = [r for r in rows if r[0] not in selected]

    funnel.append(("Older vintage replaced", removed))

    return sorted(newest.values(), key=lambda r: r[0]), funnel


def signals(panel):
    tickers = sorted({r[1] for r in panel})
    output = {}

    for ticker in tickers:
        history = sorted(
            (r for r in panel if r[1] == ticker),
            key=lambda r: r[2]
        )

        if len(history) < 2:
            output[ticker] = "Insufficient monthly history"
            continue

        previous, latest = history[-2:]

        pct = (latest[4] / previous[4] - 1) * 100

        output[ticker] = f"{pct:+.2f}% ({latest[2]})"

    return output


# RUN THE FILTERS
asof, funnel = clean(ROWS, DECISION_DATE)
naive, _ = clean(ROWS)

print("Decision date:", DECISION_DATE)

print("\nROW FUNNEL")
for name, removed in funnel:
    print(
        f"{name}: {len(removed)} removed; "
        f"rows {[r[0] for r in removed]}"
    )

print("\nAS-OF PANEL")
print("Row | Ticker | Month | Published | Index")

for r in asof:
    print(
        f"{r[0]:>3} | {r[1]:>6} | "
        f"{r[2]} | {r[3]} | {r[4]:.1f}"
    )

print("\nSIGNALS")
a = signals(asof)
n = signals(naive)

for ticker in sorted(a):
    print(
        f"{ticker}: as-of {a[ticker]} | naive {n[ticker]}"
    )

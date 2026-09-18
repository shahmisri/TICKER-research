
# ============================================
# EDITABLE TARGET AND PEER INPUTS
# Valuation date: September 1, 2026
# ============================================

target = {
    "name": "Microsoft Corporation",
    "ticker": "MSFT",
    "price": 501.02,
    "eps": 17.95,
}

peers = [
    {
        "name": "Oracle Corporation",
        "ticker": "ORCL",
        "price": 141.32,
        "eps": 5.83,
    },
    {
        "name": "Adobe Inc.",
        "ticker": "ADBE",
        "price": 286.08,
        "eps": 16.70,
    },
]

def valid_company(company):
    return (
        isinstance(company.get("price"), (int, float))
        and isinstance(company.get("eps"), (int, float))
        and company["price"] > 0
        and company["eps"] > 0
    )


def median(values):
    ordered = sorted(values)
    count = len(ordered)
    middle = count // 2

    if count % 2 == 1:
        return ordered[middle]

    return (ordered[middle - 1] + ordered[middle]) / 2


# Deduplicate peers and exclude the target.
unique_peers = []
seen_tickers = set()

for peer in peers:
    ticker = peer["ticker"].upper()

    if ticker == target["ticker"].upper():
        continue

    if ticker in seen_tickers:
        continue

    seen_tickers.add(ticker)
    unique_peers.append(peer)


valid_peers = []

print("PEER P/E MULTIPLES")

for peer in unique_peers:
    if valid_company(peer):
        peer_pe = peer["price"] / peer["eps"]
        valid_peers.append((peer, peer_pe))
        print(f'{peer["name"]} ({peer["ticker"]}): {peer_pe:.6f}x')
    else:
        print(f'{peer["name"]} ({peer["ticker"]}): not meaningful')


if not valid_company(target):
    print("\nTarget calculation: not meaningful")

elif len(valid_peers) == 0:
    print("\nNo usable peers; no estimate.")

else:
    peer_multiples = [peer_pe for peer, peer_pe in valid_peers]
    median_pe = median(peer_multiples)

    minimum_price = min(peer_multiples) * target["eps"]
    median_price = median_pe * target["eps"]
    maximum_price = max(peer_multiples) * target["eps"]

    print(f"\nPeer median P/E: {median_pe:.6f}x")

    if len(valid_peers) == 1:
        print(f"Reference estimate: ${median_price:.2f}")
        print("One valid peer: reference estimate, no range.")
    else:
        print(
            f"Peer-implied range: "
            f"${minimum_price:.2f}-${maximum_price:.2f}"
        )
        print(f"Median-implied price: ${median_price:.2f}")

    print("\nLEAVE-ONE-OUT CHECK")

    for removed_peer, removed_pe in valid_peers:
        remaining_multiples = [
            peer_pe
            for peer, peer_pe in valid_peers
            if peer["ticker"] != removed_peer["ticker"]
        ]

        if not remaining_multiples:
            print(
                f'Remove {removed_peer["ticker"]}: '
                "no remaining estimate"
            )
        else:
            remaining_median = median(remaining_multiples)
            remaining_price = remaining_median * target["eps"]
            dollar_change = remaining_price - median_price 

            print(
                f'Remove {removed_peer["ticker"]}: '
                f'${remaining_price:.2f}; '
                f'change = ${dollar_change:+.2f}'
            )

---
name: legend-investor
description: "Analyze a public company's five most recent fiscal years from SEC EDGAR 10-K XBRL facts using Buffett-style business checks. Use when asked for a Buffett, value-investor, or Legend Investor business-quality assessment."
---

# Legend Investor

Use the bundled [EDGAR facts collector](./scripts/collect_edgar_facts.py) to
build a reproducible five-year operating history and Buffett-style checks.

## Procedure

1. Ask for the ticker if it was not supplied.
2. Ensure `SEC_USER_AGENT_NAME` and `SEC_USER_AGENT_EMAIL` are set in the local
   environment. The collector sends both in the SEC User-Agent and does not
   save them. Never put either value in a source file, report, or commit.

   ```sh
   export SEC_USER_AGENT_NAME="Your Name"
   export SEC_USER_AGENT_EMAIL="you@example.edu"
   ```

3. Run the collector from the course project directory:

   ```sh
   python .github/skills/legend-investor/scripts/collect_edgar_facts.py COST
   ```

4. Treat the collector's output as the only source of numbers. It uses 10-K
   companyfacts for the five latest fiscal-year ends, chooses the latest filing
   when a period appears more than once, and prints the XBRL tag beside each
   source fact plus the formulas for ROE and owner earnings. A missing fact must
   remain `not found`; do not estimate or substitute another tag unless the
   collector's stated fallback list selects it.
5. Apply the three computed checks as printed. For any missing input, preserve
   `not known`; do not turn it into a pass or fail.
6. As Warren Buffett, write a short `.md` memo that chooses **own the business**,
   **watch it**, or **pass**. Judge business quality only, not stock price,
   valuation, or expected returns. Cite only numbers and checks printed by the
   script. For missing owner earnings, say that owner earnings cannot be judged.
7. End with one sentence answering whether to trust the verdict and why. Save
   the memo as `<TICKER>_buffett_memo.md`.
8. Run the app:

   ```sh
   python -m streamlit run lab18_buffett_app.py
   ```

   The app shows five-year owner earnings and net income, the facts and checks,
   and the saved memo. Its memo number audit flags any number not present in the
   collector's formatted output.

The SEC User-Agent values are local environment settings. Do not copy them into
files or expose them in reports.

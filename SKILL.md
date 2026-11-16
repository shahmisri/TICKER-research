---
name: legend-investor
description: "Analyze a public company's five most recent fiscal years from SEC EDGAR 10-K XBRL facts using Buffett-style business checks. Use when asked for a Buffett, value-investor, or Legend Investor business-quality assessment."
---

# Legend Investor and Panel

Use [lab18_edgar.py](lab18_edgar.py) to build a reproducible five-year
operating history and Buffett-style checks.

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
   python lab18_edgar.py COST
   ```

4. Treat the collector's output as the only source of numbers. It uses 10-K
   companyfacts for the five latest fiscal-year ends, chooses the latest filing
   when a period appears more than once, and prints the XBRL tag beside each
   source fact plus the formulas for ROE, owner earnings, and panel ratios. A
   missing fact must remain `not found`; do not estimate or substitute another
   tag unless the collector's stated fallback list selects it.
5. Apply Buffett's three checks as printed. For any missing input, preserve
   `not known`; do not turn it into a pass or fail.
6. As Warren Buffett, write a short `.md` memo that chooses **own the business**,
   **watch it**, or **pass**. Judge business quality only, not stock price,
   valuation, or expected returns. Cite only numbers and checks printed by the
   script. For missing owner earnings, say that owner earnings cannot be judged.
7. End with one sentence answering whether to trust the verdict and why. Save
   the memo as `<TICKER>_buffett_memo.md`.
8. Run the Buffett app:

   ```sh
   python -m streamlit run lab18_buffett_app.py
   ```

   The app shows five-year owner earnings and net income, the facts and checks,
   and the saved memo. Its memo number audit flags any number not present in the
   collector's formatted output.

The SEC User-Agent values are local environment settings. Do not copy them into
files or expose them in reports.

## Lab 19 investor panel

The Graham and Burry panel skills are in
[`ben-graham-expert`](.github/skills/ben-graham-expert/SKILL.md) and
[`michael-burry-expert`](.github/skills/michael-burry-expert/SKILL.md). They use
the same 10-K report and add the current-ratio and liabilities-to-equity facts.
Run the side-by-side app with:

```sh
python -m streamlit run lab19_panel_app.py
```

The default Graham current-ratio threshold is 2.0; use the app control to probe
1.0. The report prints the selected threshold and all eight check results.
Missing facts remain **not found** or **not known**, and all three memo number
audits compare against that printed report.
For each investor, any failed check means **Fails screen**, all passing checks
mean **Passes screen**, and otherwise the verdict is **Not known**.

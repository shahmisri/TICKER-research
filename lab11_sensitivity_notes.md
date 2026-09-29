# Lab 11 — MSFT Pro-Forma Sensitivity

## Drivers and Ranges

Driver 1: Revenue growth
Base: 12%, 11%, 10%, 9%, 8% for FY2027–FY2031
Lower: 10%, 9%, 8%, 7%, 6%
Higher: 14%, 13%, 12%, 11%, 10%
Range reason: Judgment. I test a 2-percentage-point decrease and increase in each forecast year around my existing revenue-growth path. Microsoft's recent historical revenue growth was approximately 15%–18%, while my base forecast already assumes moderation.

Driver 2: Gross margin
Base: 68%
Lower: 66%
Higher: 70%
Affected years: FY2027–FY2031
Range reason: Judgment. I test 2 percentage points below and above the existing 68% assumption to measure how margin changes affect the forecast.

## Locked Changed-Input Record

Prediction before running sensitivity:

Revenue growth:
Base path 12%, 11%, 10%, 9%, 8% -> lower or higher by 2 percentage points in each forecast year.
I expect higher revenue growth to increase final-year operating profit, FCFE, and value per share, while lower growth should decrease them. I expect the effect to build over the forecast because each year's revenue is based on the previous year's revenue.

Gross margin:
Base 68% -> 66% lower / 70% higher.
I expect a higher gross margin to increase operating profit, FCFE, and value per share because Microsoft retains more gross profit from each dollar of revenue.

I expect revenue growth to be a major driver because its effect compounds across the five-year forecast.
## V — Check the Result

### Base Restoration Check

The original base case and restored base case match.

Base FY2031 operating profit: $174,820.3 million
Base FY2031 FCFE: $75,129.9 million
Base value per share: $116.94

Base inputs restored: YES
Base outputs match within rounding tolerance: YES
All balance-sheet checks passed for every usable sensitivity run.

### Revenue Growth Sensitivity

Lower growth path (10%, 9%, 8%, 7%, 6%):
FY2031 operating profit: $152,900.2 million
Change from base: -$21,920.1 million
FY2031 FCFE: $57,754.5 million
Change from base: -$17,375.4 million
Value per share: $91.24
Change from base: -$25.70

Base growth path (12%, 11%, 10%, 9%, 8%):
FY2031 operating profit: $174,820.3 million
FY2031 FCFE: $75,129.9 million
Value per share: $116.94

Higher growth path (14%, 13%, 12%, 11%, 10%):
FY2031 operating profit: $198,394.2 million
Change from base: +$23,573.8 million
FY2031 FCFE: $93,799.4 million
Change from base: +$18,669.5 million
Value per share: $144.44
Change from base: +$27.50

Revenue-growth spans:
Operating profit: $45,493.9 million
FCFE: $36,044.9 million
Value per share: $53.20

### Gross Margin Sensitivity

Lower gross margin (66%):
FY2031 operating profit: $164,136.2 million
Change from base: -$10,684.2 million
FY2031 FCFE: $66,507.6 million
Change from base: -$8,622.3 million
Value per share: $102.70
Change from base: -$14.24

Base gross margin (68%):
FY2031 operating profit: $174,820.3 million
FY2031 FCFE: $75,129.9 million
Value per share: $116.94

Higher gross margin (70%):
FY2031 operating profit: $185,504.5 million
Change from base: +$10,684.2 million
FY2031 FCFE: $83,752.2 million
Change from base: +$8,622.3 million
Value per share: $131.18
Change from base: +$14.24

Gross-margin spans:
Operating profit: $21,368.4 million
FCFE: $17,244.6 million
Value per share: $28.48
## Locked Prediction Reconciliation

My prediction was supported by the results. I expected revenue growth to be a major driver because changes in growth compound across the five-year forecast.

Over the tested ranges, revenue growth produced a $45,493.9 million span in FY2031 operating profit, a $36,044.9 million span in FY2031 FCFE, and a $53.20 span in value per share. These were larger than the corresponding gross-margin spans.

The result did not reverse my valuation conclusion. Even the higher revenue-growth case produced a value per share of $144.44 compared with my base value of $116.94. However, the large sensitivity makes Microsoft's future revenue growth a higher research priority because the valuation changes substantially when the growth path changes.
## E — Find the Driver

Over these ranges, revenue growth was the larger driver of FY2031 operating profit, FY2031 FCFE, and value per share.

Revenue growth produced spans of $45,493.9 million in operating profit, $36,044.9 million in FCFE, and $53.20 per share in value. Gross margin produced smaller spans of $21,368.4 million, $17,244.6 million, and $28.48 per share, respectively.

The causal link is revenue growth -> higher revenue -> higher gross profit and operating profit -> higher FCFE -> higher value per share. Because revenue growth changes in every forecast year, its effects also compound through the forecast.

This conclusion applies only over these tested ranges. The larger span does not prove that revenue growth is inherently more important than gross margin because the result can depend on the ranges selected for each input.
## Partner Exchange 2 — Check the Evidence

**Partner question:** Why does changing revenue growth have such a large effect on Microsoft's value per share?

**My response:** Higher revenue growth increases projected revenue, which increases gross profit and operating profit. This leads to higher FCFE and ultimately a higher estimated value per share. In my higher-growth case, value per share increased from $116.94 to $144.44, a change of +$27.50.

**Partner check on my model:** My partner verified that $144.44 - $116.94 = +$27.50 and checked that gross margin remained at its 68% base assumption while only the revenue-growth path changed.
**My check on my partner's model:** I checked one sensitivity result against the base case, recomputed the change from base, and confirmed that the other independent assumptions remained at their base values.
## Partner Exchange 3 — Explain and Compare

**Partner question:** Could revenue growth appear to be the larger driver simply because of the sensitivity ranges you selected?

**My response:** Yes. My conclusion is only over these tested ranges. Revenue growth produced the larger output spans, but sensitivity results depend on the size of the input ranges being tested. A wider or different gross-margin range could change the comparison.

**My explanation to my partner:** Over my tested ranges, revenue growth was the larger driver of Microsoft's operating profit, FCFE, and value per share. Its effect builds across the forecast because changes in revenue growth compound over multiple years.
## Sensitivity — Learn on My Own

**1. What is one-at-a-time sensitivity?**

One-at-a-time sensitivity changes one independent assumption while keeping all other independent assumptions at their base values. This allows me to isolate how that specific assumption affects the model's outputs.

**2. How does the chosen input range affect the ranking?**

The size of the input range affects the output span. A driver tested over a wider range may produce a larger output span even if it is not inherently more important. Therefore, my conclusion that revenue growth is the larger driver applies only over the ranges I tested.

**3. Why is a sensitivity table not a forecast probability?**

A sensitivity table shows what happens to the model if an assumption changes. It does not tell me how likely the lower, base, or higher scenarios are to occur, so the scenarios should not be interpreted as probabilities.
## Reflect

Over these ranges, revenue growth mattered most for Microsoft's forecast and valuation. It produced the largest spans in FY2031 operating profit, FCFE, and value per share.

The result that surprised me was the size of the valuation change from revenue growth. Moving the growth path up by 2 percentage points in each forecast year increased value per share from $116.94 to $144.44, while moving it down by 2 percentage points reduced value per share to $91.24. This shows how sensitive my valuation is to Microsoft's ability to sustain revenue growth over the forecast period.
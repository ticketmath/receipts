# #009 · The Las Vegas Strip: how much profit is left from each night a room has a guest?

**Video:** coming soon

## The answer

In fiscal 2025 (July 2024 to June 2025), the big casino resorts on the Las Vegas Strip took in **$733** for every night a room had a guest: the casino, the room, food, drinks, shows and everything else. They kept **$5.36** of it as profit, before federal income tax: 0.73% of revenue.

It wasn't only fewer tourists. From fiscal 2022 to fiscal 2024 the resorts filled 9.2% more room nights, and profit per night still fell from $76.04 to $27.55. From 2022 to 2025, each night brought in $59.78 more (in dollars of each year); payroll per night rose by **$42.30**, 70.8% of that new money. Interest and the report's unexplained "other general and administrative" line also grew faster than revenue.

## How we counted

- **The source** is the Nevada Gaming Control Board's annual Gaming Abstract, group "Clark County - Las Vegas Strip Area, Gaming Revenue of $1,000,000 and over" (51 licensees in fiscal 2025). Its fiscal years run from July to June.
- **Per occupied room night** = the year's figure divided by the rooms occupied in the year (28.8 million room nights in fiscal 2025). The abstract divides by the same thing in its "Per Room Per Day Statistics", and `calc.py` checks our division against them.
- **Profit** is the abstract's "Net Income before Federal Income Taxes and Extraordinary Items": after interest, before federal income tax.
- **Payroll** is the sum of the four payroll lines (taxes, employee benefits, officers, other employees) of the five departments (casino, rooms, food, beverage, other income) and of general and administrative.
- **Operating cost** is cost of sales plus departmental expenses. **Everything that went out** is revenue minus profit.
- **Inflation** is the BLS CPI-U (all items, U.S. city average), averaged over the 12 months of each fiscal year.
- **Visitors** are the Las Vegas Convention and Visitors Authority (LVCVA) counts, by calendar year.
- The abstract PDFs have no machine-readable tables, so the lines in `data/gaming_abstract.csv` were read from them. `calc.py` adds the lines back up to the totals each abstract publishes (revenue by department, each department's expenses item by item, departmental income, net income, occupancy and the per-room statistics), so a typo in those lines stops the script. The general and administrative lines we use (its payroll, interest, rent and "other G&A"), the employee and licensee counts and a few fiscal 2019 statistics have no total to check against in our extract: they stand as read.

## One night, fiscal 2025

| Per occupied room night | |
|---|---|
| Casino, after the comps it gave away | $192 |
| Room | $246 |
| Food and beverage | $194 |
| Other income (everything else the resorts sell) | $102 |
| **Revenue** | **$733** |
| Everything that went out | $728 |
| **Profit, before federal income tax** | **$5.36** |

Inside what went out: payroll $234, interest $77.66 and other general and administrative $132; the rest is spread across the abstract's other cost lines. Before interest, $83.02 was left; interest took $77.66 of it. For every dollar of profit, the resorts paid 14.5 dollars in interest.

Gaming was 26.1% of revenue and rooms 33.5%.

## The series, fiscal 2022 to 2025

| Per occupied room night | 2019 (reference) | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|---|
| Revenue | $559 | $673 | $699 | $735 | $733 |
| Casino, after comps | $151 | $205 | $186 | $192 | $192 |
| Room | $177 | $206 | $231 | $250 | $246 |
| Operating cost | $286 | $290 | $313 | $347 | $353 |
| Payroll | $195 | $192 | $199 | $220 | $234 |
| Interest | $50.25 | $57.91 | $69.34 | $73.28 | $77.66 |
| Other general and administrative | $53.78 | $105 | $114 | $128 | $132 |
| Everything that went out | $524 | $597 | $652 | $707 | $728 |
| **Profit** | **$35.33** | **$76.04** | **$46.99** | **$27.55** | **$5.36** |

| The whole group | 2019 | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|---|
| Room nights occupied | 29.6 million | 27.3 million | 29.3 million | 29.8 million | 28.8 million |
| Net income before federal income tax | $1.0 billion | $2.1 billion | $1.4 billion | $820.2 million | $154.2 million |
| Average number of employees | 96,037 | 83,186 | 89,807 | 95,195 | 92,130 |
| Licensees in the group | 44 | 48 | 50 | 54 | 51 |

From fiscal 2022 to 2024, revenue grew 19.3%, rooms occupied 9.2% and Las Vegas visitors 7.3% (LVCVA, calendar 2022 to 2024), and net income went the other way (-60.4%). Two outside reports agree with the series: the board's press release for fiscal 2025 (-81.2% in Strip net income) and CDC Gaming Reports for fiscal 2024 (-40.4%).

## 2022 to 2025: where the extra money went

| Per occupied room night | 2022 | 2022 in 2025 dollars | 2025 | Difference | Change | Change after inflation |
|---|---|---|---|---|---|---|
| Revenue | $673 | $758 | $733 | $59.78 | 8.9% | -3.4% |
| Operating cost | $290 | $327 | $353 | $62.54 | 21.5% | 7.9% |
| Payroll | $192 | $216 | $234 | **$42.30** | 22.1% | 8.3% |
| Interest | $57.91 | $65.24 | $77.66 | $19.76 | 34.1% | 19.0% |
| Other general and administrative | $105 | $119 | $132 | $26.72 | 25.4% | 11.3% |
| Everything that went out | $597 | $673 | $728 | $130 | 21.8% | 8.2% |
| Profit | $76.04 | $85.66 | $5.36 | -$70.67 | -92.9% | -93.7% |

Prices rose 12.7% between the two fiscal years, so just to keep up, a night would have had to bring in $758 in 2025. Of the rise in everything that went out per night, payroll was 32.4%, interest 15.1% and other general and administrative 20.5%. The departments' payroll is part of operating cost, so those two rows overlap. The three shares are separate pieces and leave out the other costs, so they don't add up to 100%.

**Payroll.** The resorts had 10.8% more employees on average in fiscal 2025 than in 2022. The Culinary Union's new contracts with companies including MGM, Caesars and Wynn raised pay 10% in the first year, retroactive to June 1, 2023, and 32% over five years (Nevada Current).

**Interest** is the cost of the resorts' debt; it comes due whether the rooms are full or not.

**Other general and administrative** is a single line in the abstract ("Other G & A"), with no breakdown. Rent of premises is a separate line ($274.1 million in fiscal 2025), so this isn't the rent.

## Fewer tourists?

| | Fiscal 2024 | Fiscal 2025 | Change |
|---|---|---|---|
| Room nights available | 33.5 million | 32.3 million | -3.5% |
| Room nights occupied | 29.8 million | 28.8 million | -3.4% |
| Occupancy | 88.9% | 89.1% | |
| Licensees in the group | 54 | 51 | |
| Revenue per occupied room night | $735 | $733 | |
| Casino per occupied room night | $192 | $192 | |
| Profit per occupied room night | $27.55 | $5.36 | |

Las Vegas had 38.5 million visitors in 2025, against 41.7 million in 2024 (-7.5%). But in the abstract's fiscal 2025 the resorts also had fewer rooms to fill, and occupancy edged up. The Mirage, with about 3,000 rooms, closed on July 17, 2024, just after fiscal 2025 began, to become a Hard Rock. Each night brought in about the same as in fiscal 2024, but costs barely shrank, so each of the fewer nights carried more of them.

Visitors kept gambling: 81% gambled during their stay in 2025 (76% in 2021), with an average gambling budget of $849 per trip among those who did ($718 in 2021; LVCVA Visitor Profile Study).

**2026 so far.** From January to September 2026, the LVCVA counted 28.9 million visitors against 28.9 million in the same months of 2025 (-0.06%), and Strip gaming revenue of $6.6 billion against $6.5 billion (2.7%). The next abstract will show whether profit per night stopped falling.

## 2019 against 2025

| | Fiscal 2019 | Fiscal 2025 | Change |
|---|---|---|---|
| Visitors (LVCVA, calendar year) | 42.5 million | 38.5 million | -9.4% |
| Room nights occupied | 29.6 million | 28.8 million | -2.8% |
| Occupancy | 92% | 89.1% | |
| Total revenue | $16.5 billion | $21.1 billion | 27.4% |
| Net income before federal income tax | $1.0 billion | $154.2 million | -85.3% |

| Per occupied room night | Fiscal 2019 | 2019 in 2025 dollars | Fiscal 2025 | Change after inflation |
|---|---|---|---|---|
| Revenue | $559 | $701 | $733 | 4.5% |
| Casino, after comps | $151 | $189 | $192 | 1.1% |
| Room | $177 | $223 | $246 | 10.4% |
| Interest | $50.25 | $63.04 | $77.66 | 23.2% |
| Profit before interest | $85.58 | $107 | $83.02 | -22.7% |
| Profit | $35.33 | $44.32 | $5.36 | -87.9% |

Prices rose 25.5% between fiscal 2019 and 2025. Fiscal 2019 is only a reference: the series starts in 2022 (why: see "What this number doesn't show").

## The comps

The casino gives players free rooms, meals and drinks. The abstract subtracts them from gaming revenue and books them as room, food and beverage revenue at list price. In fiscal 2025 the casino's comps were 34.8% of what it won before them (30.8% in 2019), or $102 a night; the abstract's own ratio of all complimentaries to gaming revenue was 38.9% (33.7% in 2019). Free rooms alone were $59.67 a night ($32.37 in 2019), next to $191 of paid rooms.

Counted the way most favorable to gaming (what the casino won before comps, $294 a night, against only what customers paid for rooms, food, drinks and the rest), gaming is 39.5% of the total: still under half.

## What this number doesn't show

- The abstract covers only the Strip casinos with at least $1 million a year in gaming revenue, so a few small ones aren't counted, and the group changes from year to year (48 licensees in fiscal 2022, 54 in 2024, 51 in 2025). Per occupied room night, the size of the group matters less.
- The group's profit swings with one-time items: fiscal 2018 ended in the red (-$1.7 billion), and in fiscal 2020 the "other G&A" line was negative (-$1.7 billion), a one-time gain. Fiscal 2021 was the pandemic year. That's why the series runs from 2022 to 2025, four years in a row with no jump of that kind, and 2019 is only a reference.
- "Per occupied room night" divides everything the resorts took in by the rooms occupied. It includes the gambling, dinners and shows of people staying elsewhere (locals and guests of other hotels): it is revenue per room, not what one guest spends.
- The profit is that of the companies that run the casinos, after interest and before federal income tax. A landlord that owns a building and collects rent isn't in it.
- The abstract doesn't break down "other general and administrative", which went from $53.78 a night in fiscal 2019 to $132 in 2025. We don't say what's in it.
- The Culinary contracts cover union workers at the companies that signed them. The payroll in the abstract covers everyone, union or not, executives included, and grew with the number of employees too.
- The abstract reports the group, not each resort. The Mirage's closing date and room count come from news reports, and we don't measure how many of the missing room nights were its.
- The LVCVA counts calendar years and the abstract fiscal years (July to June). The LVCVA's gambling figures come from its annual visitor survey (interviews), and the gambling budget is the average among visitors who gambled. As a sanity check, the LVCVA's Strip gaming revenue for calendar 2025 ($8.8 billion) is within 10% of what the abstract's casinos won before comps in fiscal 2025.

## Reproduce it

```
python calc.py
```

Standard library only, no network. It reads the files in `data/`:

- `gaming_abstract.csv`: every line taken from the Gaming Abstracts (fiscal 2018 to 2025, Las Vegas Strip, $1 million and over), with the line name as in the report, its unit and the PDF's URL;
- `published_figures.csv`: the other published figures (the board's press release, CDC Gaming Reports, Nevada Current, LVCVA), with a description and the source URL;
- `bls_cpi_u_monthly.csv`: the BLS CPI-U months of each fiscal year used.

It prints the consistency checks (every line adds up to the totals each abstract publishes; occupancy, the average room rate and the per-room statistics match the abstract; the board's press release and CDC Gaming agree with the series; 12 months of CPI in each fiscal year) and writes `numbers.json`.

## Sources

- [Nevada Gaming Control Board, Gaming Abstract FY2025](https://www.gaming.nv.gov/siteassets/content/about/abstract/abstract-fy-2025.pdf)
- [Nevada Gaming Control Board, Gaming Abstract 2024](https://www.gaming.nv.gov/uploadedFiles/gamingnvgov/content/about/abstract/Nevada%20Gaming%20Abstract%202024.pdf)
- [Nevada Gaming Control Board, Gaming Abstract 2023](https://www.gaming.nv.gov/uploadedFiles/gamingnvgov/content/about/abstract/2023-abstract.pdf)
- [Nevada Gaming Control Board, Gaming Abstract 2022](https://www.gaming.nv.gov/uploadedFiles/gamingnvgov/content/about/abstract/2022-abstract.pdf)
- [Nevada Gaming Control Board, Gaming Abstract 2020](https://www.gaming.nv.gov/uploadedFiles/gamingnvgov/content/about/abstract/2020-abstract.pdf)
- [Nevada Gaming Control Board, Gaming Abstract 2019](https://www.gaming.nv.gov/uploadedFiles/gamingnvgov/content/about/abstract/2019-abstract.pdf)
- [Nevada Gaming Control Board, Gaming Abstract 2018](https://www.gaming.nv.gov/uploadedFiles/gamingnvgov/content/about/abstract/2018-abstract.pdf)
- [Nevada Gaming Control Board, Gaming Abstract 2025 press release (June 10, 2026)](https://www.gaming.nv.gov/siteassets/content/about/abstract/nevada-gaming-abstract-2025-press-release.pdf)
- [CDC Gaming Reports, Las Vegas casinos FY24 net income declines 40.4% despite 6.8% revenue increase](https://cdcgaming.com/las-vegas-casinos-fy24-net-income-declines-40-4-despite-6-8-revenue-increase/)
- [Nevada Current, Culinary workers get 10% wage increase in 1st year, 32% increase over 5 years under new contracts](https://nevadacurrent.com/?p=206594)
- [LVCVA, Historic Tourism Statistics 1970-2025](https://assets.simpleviewcms.com/simpleview/image/upload/v1/clients/lasvegas/Las_Vegas_Historical_1970_to_2025_f2a79f3a-e9ec-47df-b0c3-dc92f67a3e89.pdf)
- [LVCVA, Executive Summary, September 2026](https://assets.simpleviewcms.com/simpleview/image/upload/v1/clients/lasvegas/ES_Sep2026_revised_37937aa3-f16c-455a-b73c-cec6876e4bbb.pdf)
- [LVCVA, Research FAQs](https://www.lvcva.com/research/faqs/)
- [LVCVA, 2025 Las Vegas Visitor Profile Study](https://assets.simpleviewcms.com/simpleview/image/upload/v1/clients/lasvegas/2025_Las_Vegas_Visitor_Profile_Study_db57c923-1f87-4ab8-868d-d6fc0bf2f972.pdf)
- [U.S. Bureau of Labor Statistics, CPI-U, all items, U.S. city average (CUUR0000SA0)](https://data.bls.gov/timeseries/CUUR0000SA0)
- [Scripps News, The Mirage in Las Vegas is closing: what to know about its Hard Rock rebrand](https://scrippsnews.com/business/company-news/the-mirage-in-las-vegas-is-closing-heres-what-to-know-about-its-hard-rock-rebrand)

## Corrections

None so far. Found an error? Open an issue with the line and the source.

## License

Code (`calc.py`): [MIT](../LICENSE). Data, text and tables: [CC BY 4.0](../LICENSE-DATA.md); the underlying public records keep their own terms.

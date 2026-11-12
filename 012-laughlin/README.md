# #012 · Laughlin's casinos: where did the profit from each night with a guest go?

**Video:** https://youtu.be/pvtBetVs0sU

## The answer

In fiscal 2025 (July 2024 to June 2025), the big casinos of Laughlin, Nevada, lost **$38.62** for every night a room had a guest, after every bill and before federal income tax. In fiscal 2019, the same night made **$43.91**.

Running the casinos, hotels and restaurants still brought in the same money: departmental income was $336.7 million in fiscal 2019 and $336.7 million in fiscal 2025, while occupied room nights fell from 2.2 million to 1.4 million (-35.1%). Two bills ate the profit:

- **Interest** jumped from $23.6 million in fiscal 2020 to $82.2 million in fiscal 2021, the year a new "contracts" debt of $555.4 million appeared on the group's balance sheet. That is the year VICI Properties bought the land and building of Harrah's Laughlin ($434.8 million, closed July 20, 2020) and leased it back to Caesars, which books those leases as a financing obligation, with interest expense. Our reading: much of the interest is most likely that rent. The state report doesn't say who holds the debt.
- **"Other general and administrative"**, a line the report doesn't break down, went from $75.9 million in fiscal 2024 to $132.1 million in fiscal 2025 ($56.2 million in a single year). No public source we found explains it.

## How we counted

- **The source** is the Nevada Gaming Control Board's annual Gaming Abstract, group "Clark County - Laughlin Area, Gaming Revenue of $1,000,000 and over" (9 licensees in fiscal 2025). Its fiscal years run from July to June.
- **Per occupied room night** = the year's figure divided by the rooms occupied in the year (1.4 million room nights in fiscal 2025). `calc.py` checks our division of room revenue against the abstract's published average room rate.
- **Running the place** is the abstract's "Departmental Income": revenue minus cost of sales and the departments' own expenses, before general and administrative.
- **Profit** is the abstract's "Net Income before Federal Income Taxes and Extraordinary Items": after interest and depreciation, before federal income tax.
- **Inflation** is the BLS CPI-U (all items, U.S. city average), averaged over the 12 months of each fiscal year.
- The abstract PDFs have no machine-readable tables, so the lines in `data/gaming_abstract.csv` were read from them. `calc.py` adds them back up to the totals each abstract publishes (revenue, gross margin, departmental income, the 17 general and administrative lines, net income, occupancy, rooms revenue and the average room rate), so a typo in one line stops the script. The long-term debt lines, employees and licensees have no total to check against: they stand as read.

## One night with a guest, fiscal 2025

| Per occupied room night | |
|---|---|
| Running the place (departmental income) | $237 |
| Interest | $61.91 |
| Wear and tear, office staff, ads, power, taxes and the rest of general and administrative | $121 |
| "Other general and administrative" | $93.10 |
| **Result** | **-$38.62** |

## The series, fiscal 2019 to 2025

| Per occupied room night | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|---|---|---|
| Revenue | $326 | $338 | $420 | $461 | $453 | $439 | $452 |
| Running the place | $154 | $155 | $241 | $262 | $248 | $231 | $237 |
| Interest | $9.79 | $15.05 | $58.28 | $60.99 | $62.27 | $61.89 | $61.91 |
| Other general and administrative | $25.33 | $47.81 | $35.48 | $37.87 | $40.32 | $50.87 | $93.10 |
| **Profit** | **$43.91** | **-$8.33** | **$43.17** | **$56.39** | **$36.61** | **$5.58** | **-$38.62** |

| The whole group | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|---|---|---|
| Room nights occupied | 2.2 million | 1.6 million | 1.4 million | 1.4 million | 1.5 million | 1.5 million | 1.4 million |
| Departmental income | $336.7 million | $242.9 million | $340.3 million | $376.9 million | $369.3 million | $344.4 million | $336.7 million |
| Interest expense | $21.4 million | $23.6 million | $82.2 million | $87.8 million | $92.7 million | $92.3 million | $87.8 million |
| Net income before federal income tax | $96.0 million | -$13.1 million | $60.9 million | $81.2 million | $54.5 million | $8.3 million | -$54.8 million |
| Average number of employees | 5,948 | 4,858 | 4,082 | 4,027 | 4,201 | 4,316 | 4,199 |
| Licensees in the group | 12 | 9 | 13 | 9 | 9 | 9 | 9 |

The board's press release for fiscal 2025 agrees with the series: -758.6% in Laughlin net income from fiscal 2024.

## Bill one: the building, sold and rented back

| | Fiscal 2019 | Fiscal 2020 | Fiscal 2021 | Fiscal 2025 |
|---|---|---|---|---|
| Interest expense | $21.4 million | $23.6 million | $82.2 million | $87.8 million |
| Long-term debt: "contracts" | $2.5 million | $4.2 million | $555.4 million | $603.4 million |
| Total long-term debt | $321.4 million | $214.2 million | $910.6 million | $918.4 million |
| Rent of premises (a separate line) | $2.3 million | $3.6 million | $6.6 million | $7.7 million |

- VICI paid $1.8 billion for the real estate of three Harrah's casinos (Atlantic City, New Orleans and Laughlin) and leased them back to Caesars; the annual rent of its Regional Master Lease rose $154.0 million. VICI's Form 8-K gives Harrah's Laughlin's own price: $434.8 million. Its own rent isn't published; split by price, it would be about $36.7 million a year (our estimate).
- Under the accounting rules, Caesars doesn't count these sales as real sales: its 2020 Form 10-K books the VICI and GLPI leases as financing obligations ("failed sale-leaseback"), at imputed rates of 11.3% and 9.8%, with interest expense of $491.0 million in 2020 on all its VICI leases. Initial term: 15 years, plus renewals.
- In the abstract, interest was 9.6% of long-term debt in fiscal 2025, close to those rates. That fits the reading; it doesn't prove it.
- The Tropicana Laughlin's real estate was sold too, to GLPI, on October 1, 2018 ($964.0 million for 5 casinos), which falls inside fiscal 2019: it's already in the 2019 numbers and doesn't explain the 2021 jump.

## Bill two: "other"

From fiscal 2022 to 2025, occupied room nights barely moved (-1.5%), and interest per night barely moved either ($60.99 to $61.91). What changed: running the place went from $262 a night to $237, and "other general and administrative" from $37.87 to $93.10. The abstract publishes "other G&A" as one line with no breakdown, and Golden Entertainment's 2024 and 2025 Forms 10-K show no write-off that explains it. It could be a one-time charge or a lasting cost: the next abstract will tell.

## In today's money

Prices rose 25.5% between fiscal 2019 and 2025. In fiscal 2025 dollars, 2019's departmental income would be $422.4 million; 2025's is -20.3% against it. Per night with a guest, running the place still brings in more than in 2019 even after inflation: $193 (2019, in 2025 dollars) against $237.

## Laughlin today

The LVCVA's Executive Summary counts 1.1 million visitors from January to September 2026, against 1.1 million in the same months of 2025 (3.1%); gross gaming revenue of $370.9 million against $375.7 million (-1.3%). In November 2025, VICI agreed to buy the real estate of 7 Golden Entertainment casinos, the Aquarius and the Edgewater in Laughlin among them, for $1.2 billion, with $87.0 million a year in rent. That sale isn't in these numbers yet.

## What this number doesn't show

- The abstract covers only the Laughlin casinos with at least $1 million a year in gaming revenue, in fiscal years from July to June, and the group changes: 12 licensees in 2019, 13 in 2021 and 9 from 2022 to 2025. Per occupied room night, the size of the group matters less, but it doesn't vanish.
- "Per occupied room night" divides everything the casinos took in by the rooms occupied. It includes the gambling of people who never booked a room (locals from Bullhead City and day-trippers): it is revenue per room, not what one guest spends. Room revenue includes the list price of rooms given to players (50.6% of all room value in fiscal 2025).
- The abstract adds the casinos together and doesn't say which one holds the debt or pays the interest. That much of the interest is the Harrah's Laughlin rent is our reading of the numbers, not something the state prints.
- The profit is before federal income tax and after interest and depreciation; depreciation is part of the abstract's general and administrative expenses.
- The 2026 figures are calendar year-to-date, and visitor counts are estimates.

## Reproduce it

```
python calc.py
```

Standard library only, no network. It reads the files in `data/`:

- `gaming_abstract.csv`: every line taken from the Gaming Abstracts (fiscal 2019 to 2025, Laughlin Area, $1 million and over), with the line name as in the report, its unit and the PDF's URL;
- `published_figures.csv`: the other published figures (VICI, Caesars, GLPI, The Nevada Independent, AP, the LVCVA and the board's press release), with a description and the source URL;
- `bls_cpi_u_monthly.csv`: the BLS CPI-U months of each fiscal year used.

It prints the consistency checks (every line adds up to the totals each abstract publishes; occupancy and the average room rate match the abstract; the fiscal 2025 night closes to the cent; the board's press release and the LVCVA changes agree with their own figures; 12 months of CPI in each fiscal year) and writes `numbers.json`.

## Sources

- [Nevada Gaming Control Board, Gaming Abstract 2019](https://www.gaming.nv.gov/uploadedFiles/gamingnvgov/content/about/abstract/2019-abstract.pdf)
- [Nevada Gaming Control Board, Gaming Abstract 2020](https://www.gaming.nv.gov/uploadedFiles/gamingnvgov/content/about/abstract/2020-abstract.pdf)
- [Nevada Gaming Control Board, Gaming Abstract 2021](https://www.gaming.nv.gov/uploadedFiles/gamingnvgov/content/about/abstract/2021-abstract.pdf)
- [Nevada Gaming Control Board, Gaming Abstract 2022](https://www.gaming.nv.gov/uploadedFiles/gamingnvgov/content/about/abstract/2022-abstract.pdf)
- [Nevada Gaming Control Board, Gaming Abstract 2023](https://www.gaming.nv.gov/uploadedFiles/gamingnvgov/content/about/abstract/2023-abstract.pdf)
- [Nevada Gaming Control Board, Gaming Abstract 2024](https://www.gaming.nv.gov/uploadedFiles/gamingnvgov/content/about/abstract/Nevada%20Gaming%20Abstract%202024.pdf)
- [Nevada Gaming Control Board, Gaming Abstract FY2025](https://www.gaming.nv.gov/siteassets/content/about/abstract/abstract-fy-2025.pdf)
- [CDC Gaming Reports, on VICI Properties and the three Harrah's](https://cdcgaming.com/vici-properties-holds-the-cards-and-50-acres-in-future-las-vegas-strip-development/)
- [VICI Properties, press release (July 20, 2020)](https://www.businesswire.com/news/home/20200720005761/en/VICI-Properties-Completes-Property-Acquisitions-Lease-Modifications)
- [Caesars Entertainment, Form 10-K 2020](https://www.sec.gov/Archives/edgar/data/1590895/000159089521000085/czr-20201231.htm)
- [VICI Properties, Form 8-K (Sept. 26, 2019)](https://www.sec.gov/Archives/edgar/data/1705696/000170569619000145/a8-kxmastertransaction.htm)
- [GLPI, Tropicana deal press release (Oct. 1, 2018)](https://www.sec.gov/Archives/edgar/data/0001575965/000119312518289765/d612515dex991.htm)
- [Nevada Gaming Control Board, Gaming Abstract 2025 press release](https://www.gaming.nv.gov/siteassets/content/about/abstract/nevada-gaming-abstract-2025-press-release.pdf)
- [Las Vegas Review-Journal, Las Vegas closes the book on 2025 visitation](https://www.reviewjournal.com/business/tourism/las-vegas-closes-the-book-on-2025-visitation-down-7-5-3613202/)
- [The Nevada Independent, VICI buys seven Golden casinos](https://thenevadaindependent.com/article/crowded-portfolio-seven-casinos-in-las-vegas-laughlin-and-pahrump-bought-by-vici)
- [AP via KNAU, Don Laughlin obituary (Oct. 2023)](https://www.knau.org/knau-and-arizona-news/2023-10-23/don-laughlin-resort-casino-owner-and-architect-behind-nevada-town-is-dead-at-92)
- [AP via The Washington Times, Laughlin casino to remain closed (May 19, 2020)](https://m.washingtontimes.com/news/2020/may/19/laughlin-casino-to-remain-closed-400-employees-to-/)
- [LVCVA, Executive Summary, September 2026](https://assets.simpleviewcms.com/simpleview/image/upload/v1/clients/lasvegas/ES_Sep2026_revised_37937aa3-f16c-455a-b73c-cec6876e4bbb.pdf)
- [BLS, CPI-U, all items, U.S. city average](https://data.bls.gov/timeseries/CUUR0000SA0)

## Corrections

None so far. Found an error? Open an issue with the line and the source.

## License

Code (`calc.py`): [MIT](../LICENSE). Data, text and tables: [CC BY 4.0](../LICENSE-DATA.md); the underlying public records keep their own terms.

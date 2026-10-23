# #006 · The fare is the bait: what a cruise line earns after you board

**Video:** https://youtu.be/1oi9sRjtwVU

## The answer

At Carnival, the extras (drinks, excursions, the casino, the shops, Wi-Fi) left **$62.79 per passenger per day** in 2025, after their direct cost. The whole company's operating income came to **$44.08** per passenger per day. The part is bigger than the whole because the fare alone doesn't pay for the ship: without the onboard margin, Carnival would have lost **$18.71** per passenger per day. Norwegian works the same way. Royal Caribbean, whose fare alone also lost money in 2019, now makes money on it.

This is an accounting exercise on published annual reports. It is not a forecast, and it is not the companies' own breakdown.

## The unit: one passenger, one day

The cruise lines report "passenger cruise days": one passenger on board for one day. Each number below is a line of the 2025 income statement (Form 10-K) divided by passenger cruise days.

| 2025 | Carnival | Royal Caribbean | Norwegian |
|---|---|---|---|
| Passengers carried | 13.6 million | 9.4 million | 3.0 million |
| Passenger cruise days | 101.7 million | 58.5 million | 25.3 million |
| Average cruise length (days) | 7.5 | 6.2 | 8.4 |
| Occupancy (two guests per cabin = 100%) | 105% | 109.7% | 103.5% |
| Ticket revenue per day | $171 | $214 | $265 |
| Onboard and other revenue per day | $90.48 | $92.60 | $124 |
| Direct cost of what was sold on board | $27.69 | $16.76 | $27.25 |
| **Onboard margin per day** | **$62.79** | **$75.84** | **$96.97** |
| Operating income per day | $44.08 | $83.90 | $61.75 |
| **The fare alone per day** (operating income − onboard margin) | **-$18.71** | **$8.07** | **-$35.22** |
| Interest on debt per day | $13.26 | $16.95 | $37.72 |
| Net income per day | $27.14 | $73.33 | $16.74 |
| Net income per day without the onboard margin | -$35.65 | -$2.51 | -$80.22 |

For the whole year:

| 2025 | Carnival | Royal Caribbean | Norwegian |
|---|---|---|---|
| Onboard margin | $6.4 billion | $4.4 billion | $2.5 billion |
| Operating income | $4.5 billion | $4.9 billion | $1.6 billion |
| Onboard margin as a share of operating income | **142.4%** | **90.4%** | **157.0%** |
| Operating income without the onboard margin | -$1.9 billion | $472.0 million | -$890.3 million |
| Net income | $2.8 billion | $4.3 billion | $423.2 million |
| Net income without the onboard margin | -$3.6 billion | -$147.0 million | -$2.0 billion |
| Onboard share of revenue | 34.6% | 30.2% | 32.0% |
| Onboard revenue as a share of ticket revenue | 52.8% | 43.3% | 47.0% |
| Onboard revenue per passenger, per cruise | $677 | $574 | $1,047 |

The three together carried 26.0 million passengers, 69.8% of the 37.3 million ocean cruise passengers CLIA counted worldwide. Per passenger day, they took in $95.75 on board and kept a margin of $71.57, against an operating income of $59.05 (net income: $40.29). Their onboard margin was 121.2% of their operating income.

## Carnival's receipt for one day at sea

| 2025, per passenger day | |
|---|---|
| Ticket revenue | $171 |
| − Commissions, transportation and other | $32.75 |
| = What the ticket leaves | $139 |
| Payroll (the whole crew) | $25.46 |
| Fuel | $17.78 |
| Food | $14.74 |
| Other ship operating costs | $38.39 |
| Selling and administrative | $33.45 |
| Depreciation | $27.43 |
| = Cost of the ship | $157 |
| **The fare alone** (what the ticket leaves − cost of the ship) | **-$18.71** |
| + Onboard margin ($90.48 − $27.69) | $62.79 |
| = Operating income | $44.08 |

Carnival reports in millions of dollars, so the lines add up to the total within rounding (`calc.py` checks it).

## 2019 against 2025

US consumer prices rose **25.9%** from 2019 to 2025 (BLS CPI-U, annual averages). "After inflation" compares 2025 with 2019 in 2025 dollars.

| Per passenger day | Carnival | Royal Caribbean | Norwegian |
|---|---|---|---|
| Ticket revenue, 2019 | $151 | $175 | $219 |
| Ticket revenue, 2025 | $171 | $214 | $265 |
| Change, dollars of each year | 13.4% | 22.0% | 20.9% |
| Change, after inflation | -10.0% | -3.2% | -4.0% |
| Onboard revenue, 2019 | $67.81 | $69.05 | $94.24 |
| Onboard revenue, 2025 | $90.48 | $92.60 | $124 |
| Change, dollars of each year | 33.4% | 34.1% | 31.8% |
| Change, after inflation | 6.0% | 6.5% | 4.7% |
| Every other cost (all but the onboard cost), 2019 | $163 | $184 | $237 |
| Every other cost, 2025 | $190 | $206 | $300 |
| Change, after inflation | -7.2% | **-11.0%** | 0.5% |
| **The fare alone, 2019** | -$11.52 | **-$8.28** | -$18.04 |
| **The fare alone, 2025** | -$18.71 | **$8.07** | -$35.22 |

| Whole year | Carnival | Royal Caribbean | Norwegian |
|---|---|---|---|
| Onboard margin as a share of operating income, 2019 | 129.1% | 117.8% | 131.6% |
| Onboard margin as a share of operating income, 2025 | 142.4% | 90.4% | 157.0% |
| Operating income without the onboard margin, 2019 | -$954.0 million | -$371.1 million | -$372.2 million |
| Onboard share of revenue, 2019 | 30.4% | 28.3% | 30.1% |

After inflation, the fare per day fell at all three lines. Royal Caribbean turned anyway: in 2019 its fare alone lost $8.28 per passenger day; in 2025 it left $8.07, because every other cost per day fell more than the fare (-11.0% after inflation). Carnival's fare alone went from losing $11.52 to losing $18.71 a day; Norwegian's, from $18.04 to $35.22. After interest, Royal Caribbean's fare alone still roughly breaks even: -$2.51 per passenger day.

## Viking: almost everything in the fare

Viking (ocean and river cruises, Form 20-F 2025) carried 791,582 passengers. Its fare (cruise and land) brought in $823 per passenger day and onboard sales $61.20, only 6.9% of revenue (Carnival: 34.6%). Its operating income was $204 per passenger day.

## What a passenger sees on board (official pages, October 2026)

- **Drinks.** Carnival's CHEERS! package costs $89.94 per person per day bought on board ($83.94 bought before the cruise), service charge included, and covers drinks of up to $20.00. Carnival's average onboard revenue per passenger day, kids included ($90.48), is 100.6% of one day of that package, or 11.3 beers at $8.00. A soda is $3.00; the Bottomless Bubbles soda package is $14.38 a day. Royal Caribbean's Deluxe package covers drinks of up to $14.00; its price varies by sailing and is not published.
- **Food.** A Steakhouse dinner at Carnival is $52.00 per adult; a third main course in the main dining room is $5.00. Carnival adds a 20% service charge to drinks and paid food; Royal Caribbean adds an automatic 18% gratuity to drinks, packages, specialty dining and room service.
- **Wi-Fi.** Carnival: $25.00 a day for social media only, $35.00 a day for the Premium plan.
- **Gratuities.** Carnival recommends $17.00 per person per day (that is 38.6% of Carnival's operating income per passenger day); Royal Caribbean charges $18.50; Norwegian charges a $20.00 daily service charge, 7.6% of its ticket revenue per passenger day. Norwegian's "free" open bar (Free at Sea) comes with $28.50 per person per day in gratuities.
- **Before the cruise.** Royal Caribbean says nearly 50% of its 2025 onboard revenue was booked before passengers boarded.
- **Private destination.** Carnival's own destination, Celebration Key (Grand Bahama), hosted more than 1.0 million guests after it opened in July 2025.

## Method

- **Passenger cruise days:** as each company reports them. Carnival's 2019 report does not publish them, so they come from available lower berth days × occupancy, Carnival's own definition. Occupancy counts two guests per cabin, so it passes 100% when cabins carry third and fourth guests.
- **Onboard margin:** "onboard and other" revenue minus the "onboard and other" expense line, nothing else.
- **The fare alone:** operating income minus the onboard margin. For 2019 it is the ticket per day minus every other cost per day (Carnival's separate "tour and other" line stays out of both sides).
- **Inflation:** BLS CPI-U, all items, U.S. city average, annual averages of the monthly values.
- **Carnival's segments:** onboard was 38% of its North America segment's revenue and 23% of Europe's (10-K text).
- **Income tax** on income before tax, 2025: Carnival 0.4%, Royal Caribbean 1.9%, Norwegian 1.3%.
- **Prices:** the companies' official pages, checked in October 2026.

## What this number doesn't show

- The onboard cost in the 10-K is only the direct cost: drinks, tours, shops, cards. The bartenders' and specialty restaurants' staff are paid inside the whole crew's payroll, and the ship, the fuel and the debt serve the fare and the extras at the same time. So the onboard margin computed here is larger than the real one, and "without the onboard margin" is a bound, not a real balance sheet. That doesn't change Carnival or Norwegian, where the margin passes the whole profit with room to spare. It does mean we can't say Royal Caribbean would also lose money at the net level: without the onboard margin, its net income would be -$147.0 million.
- "Onboard and other" isn't only what is spent on the ship: it includes travel insurance, hotel and tour packages before and after the cruise and, at Norwegian, part of the value of packages sold with the fare, which the company splits between fare and onboard by the price of each item sold on its own.
- The fare includes port charges the company passes on: at Royal Caribbean, $1.3 billion in 2025, or $22.22 per passenger day. Carnival and Norwegian don't publish this figure. The matching cost sits in the commissions and transportation line, so the result doesn't change, but the "fare" is larger than the price of the trip.
- Carnival's fiscal year ends at the end of November; the others' at the end of December. In 2019 Carnival also reported a small separate line, "tour and other" (land packages and, that year, sales of ship exhaust gas cleaning systems to third parties): it counts in total revenue but stays out of the comparison between the fare and the cost of the ship.
- The 2025 inflation figure is an average of eleven months: the BLS did not collect prices for October 2025, during the US government shutdown.
- MSC (privately held, no published financial statements) and Disney (whose report combines cruises with the parks) are left out. CLIA's count is not the same as the companies' either: it covers only ocean cruises of its member lines.
- Viking sells luxury ocean and river cruises to a different public, with fares many times higher and far fewer passengers: it shows that the bait is a choice of business model, not that the others could simply copy it.
- Carnival's onboard shares by segment come from the 10-K text, rounded, and the 10-K doesn't publish passenger days by segment.
- The onboard prices are those on the official pages in October 2026: they vary by ship, by date and by when you buy, and Royal Caribbean publishes no fixed price for its drinks package or Wi-Fi. They are examples of what makes up the average, not what each passenger pays. The average itself covers every passenger, kids included.
- Gratuities and service charges are not clean profit: Carnival's and Royal Caribbean's pages say they go to the crew. Only Norwegian's 10-K says where the charge is booked: inside ticket revenue, not onboard revenue.
- The near-zero income tax is not a choice made each year: the three are incorporated outside the US (Carnival in Panama and in England and Wales, Royal Caribbean in Liberia, Norwegian in Bermuda, per the cover of each 10-K), and a rule of the US tax code cited in Carnival's 10-K (Section 883) exempts foreign companies from federal income tax on international shipping.

## Reproduce it

```
python calc.py
```

Standard library only, no network. It reads `data/inputs.csv` (every income statement line, operating statistic, 10-K sentence, BLS index and published price used, with the source URL on each row), prints the consistency checks and writes `numbers.json`.

## Sources

- [Carnival Corporation & plc, Form 10-K 2025](https://www.sec.gov/Archives/edgar/data/815097/000081509726000007/ccl-20251130.htm)
- [Royal Caribbean Cruises, Form 10-K 2025](https://www.sec.gov/Archives/edgar/data/884887/000088488726000007/rcl-20251231.htm)
- [Norwegian Cruise Line Holdings, Form 10-K 2025](https://www.sec.gov/Archives/edgar/data/1513761/000110465926022067/nclh-20251231x10k.htm)
- [CLIA, State of the Cruise Industry 2026](https://www.cruising.org/sites/default/files/2026-05/CLIA%20001%20Overview%20Global.pdf)
- [BLS, Consumer Price Index (CPI-U)](https://data.bls.gov/timeseries/CUUR0000SA0)
- [Carnival Corporation & plc, Form 10-K 2019](https://www.sec.gov/Archives/edgar/data/815097/000081509720000003/a2019ex-13.htm)
- [Royal Caribbean Cruises, Form 10-K 2019](https://www.sec.gov/Archives/edgar/data/884887/000088488720000009/rcl-20191231.htm)
- [Norwegian Cruise Line Holdings, Form 10-K 2019](https://www.sec.gov/Archives/edgar/data/1513761/000155837020001661/nclh-20191231x10kc19a9c.htm)
- [Viking Holdings, Form 20-F 2025](https://www.sec.gov/Archives/edgar/data/1745201/000174520126000007/vik-20251231.htm)
- [Carnival, onboard prices and fees (carnival.com)](https://help.carnival.com/app/answers/detail/a_id/3525)
- [Carnival, onboard prices and fees (carnival.com)](https://www.carnival.com/help?topicid=1202)
- [Carnival, onboard prices and fees (carnival.com)](https://help.carnival.com/app/answers/detail/a_id/3861)
- [Carnival, onboard prices and fees (carnival.com)](https://www.carnival.com/cruise-food/steakhouse)
- [Royal Caribbean, onboard prices and fees](https://www.royalcaribbean.com/faq/questions/onboard-service-gratuity-expense)
- [Royal Caribbean, onboard prices and fees](https://www.royalcaribbean.com/faq/questions/what-is-the-deluxe-beverage-package)
- [Norwegian, Free at Sea flyer and service charge](https://www.ncl.com/faq/what-is-ncl-onboard-service-charge)
- [Norwegian, Free at Sea flyer and service charge](https://www.ncl.com/sites/default/files/Free-at-Sea-Plus-Comparison-Flyer_0.pdf)
- [Royal Caribbean, 2025 results release](https://www.rclinvestor.com/press-releases/release/?id=1812)

## Corrections

None so far. Found an error? Open an issue with the line and the source.

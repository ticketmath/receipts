# #011 · Villa Vie Odyssey: what did a day on board cost, and what did the ship cost to run?

**Video:** https://youtu.be/A8VJXPM9Ys8

## The answer

Villa Vie rented its cheapest cabin for $3,499 a month per person, with meals, cleaning and a doctor on board: **$115 a day**. Royal Caribbean spends $121 a day on each berth before it buys any fuel ($145 with fuel), on much bigger ships, and sells plenty more once you're aboard.

Before the war with Iran, at the $700 a ton Villa Vie says it paid, fuel alone for the 203 residents aboard at the end would have taken **$79.36 per resident per day**, 69.0% of that price. Since the war, at the low end of what the company says it pays, fuel came to $227 per resident per day, more than a renter paid for everything.

The war made fuel expensive for everyone. Carnival paid $826 a ton from June to August 2026 and made more money than a year earlier. Even at the low end of its own figures, Villa Vie paid 2.4 times that, and the Odyssey burned 4.7 times the fuel per person of a Carnival passenger.

## How we counted

- **Villa Vie's figures are its own words.** The company is private and publishes no accounts. Prices, consumption and spending come from what founder Mikael Petterson and the company told CBS News and Business Insider, what the captain said (Cruise Industry News) and what its own site advertises. They're in `data/published_figures.csv`, each with its source.
- **Per resident per day** = tons a month × price a ton / 203 residents / days in a month (365 / 12). The crew stays out of the per-person count on both sides.
- **The big lines** come from their SEC filings for the same summer: Carnival's 10-Q for June to August 2026, and Royal Caribbean's and Norwegian's 10-Q and earnings release for July to September 2026. Per passenger per day = fuel expense or tons / passenger cruise days. `calc.py` checks that price per ton × tons matches each company's fuel line, and that Carnival's passenger days over berth days give its published occupancy.
- **The market** is marine gasoil in Singapore, the world's largest bunkering port (Ship & Bunker). `calc.py` checks that the pre-war price Villa Vie gives matches Singapore's last session before the rise.
- **Cost per berth per day** is what the cruise lines publish: Royal Caribbean's Net Cruise Costs per APCD (a berth is half a standard cabin) and Norwegian's Net Cruise Cost per Capacity Day.

## The price of a day on board

| Per person, per day | |
|---|---|
| **Villa Vie, inside cabin, everything included** | **$115** |
| Royal Caribbean, cost per berth, before fuel | $121 |
| Royal Caribbean, cost per berth, with fuel | $145 |
| Royal Caribbean, gross cost per berth (with commissions and onboard sales costs) | $218 |
| Royal Caribbean, net revenue per berth (Net Yield) | $304 |
| Norwegian, cost per berth, with fuel | $185 |
| U.S. assisted living, median | $204 |
| Average Social Security retirement benefit | $68.67 |

Villa Vie's daily price sat $29.75 below what Royal Caribbean spends to run a berth, fuel included. Royal Caribbean's cost was 1.3 times Villa Vie's rent, and its net revenue per berth 2.6 times.

The rent came to 56.4% of the median U.S. assisted living home ($6,200 a month) and 1.7 times the average retirement benefit ($2,089 a month). Permanent residency started at $119,999 and five years at $59,999, with owners' monthly fees from $3,500.

## Fuel, a ton

| Price per ton | |
|---|---|
| **Villa Vie, before the war (its own figure)** | **$700** |
| **Villa Vie, since the war (its own range)** | **$2,000 to $3,000** |
| Villa Vie, marine diesel in Cambodia | $2,200 |
| Carnival, June to August 2026 | $826 |
| Carnival, June to August 2025 | $607 |
| Royal Caribbean, July to September 2026, net of hedging | $778 |
| Norwegian, July to September 2026, net of hedges | $819 |
| Norwegian, July to September 2025 | $744 |
| Norwegian's locked-in price for 2026 (heavy oil and diesel) | $506 |

| Singapore market | |
|---|---|
| Marine gasoil, third quarter of 2025 | $674 |
| Marine gasoil, fourth quarter of 2025 | $682 |
| Marine gasoil, February 27, 2026, the last session before the rise | $710 |
| Marine gasoil, April 6, 2026, the year's high | $2,064 |
| Marine gasoil, second quarter of 2026 | $1,238 |
| Marine gasoil, third quarter of 2026 | $1,202 |
| Heavy fuel oil, high sulfur, third quarter of 2026 | $622 |
| Very-low-sulfur fuel oil, third quarter of 2026 | $814 |
| Marine gasoil, October 27, 2026, the day the residents went ashore | $1,342 |
| Marine gasoil, fourth quarter of 2026 through November 6 | $1,286 |

April 6 was the only day of 2026 at $2,000 or more in the daily series: Singapore's market reached the bottom of Villa Vie's range once and stayed below it the rest of the year. The low end of Villa Vie's range was 1.7 times Singapore's third-quarter average, 1.5 times the price on October 27, and $714 a ton above the fourth-quarter average. By the company's own figures, its price rose 2.9 times.

**Against Carnival.** The low end of Villa Vie's range was 2.4 times Carnival's price that summer, the high end 3.6 times. Before the war, Villa Vie's price was 1.2 times Carnival's a year earlier.

**Three things kept the big lines' bill smaller:**

1. **A different fuel.** Carnival's 10-K says "We have Advanced Air Quality Systems on most of our ships": exhaust scrubbers that let them burn heavy fuel oil. In Singapore, marine gasoil cost 1.9 times heavy fuel oil in the third quarter, and 1.5 times Carnival's average price.
2. **Locked-in prices.** Royal Caribbean had 59% of its 2026 fuel hedged on September 30; Norwegian, 48% on October 15.
3. **Full ships.** Carnival's occupancy was 111.8% (above 100% means more than two people per cabin). The Odyssey ended with 203 residents: 21.9% of its 929-passenger capacity and 31.2% of the 650 residents the company advertises.

Carnival's fuel cost $615.0 million from June to August 2026, and higher prices added $149.0 million of it. It still earned $1.9 billion, against $1.9 billion a year earlier.

## Per person

| Fuel, per person per day | Dollars | Kilos |
|---|---|---|
| **Odyssey, per resident, since the war (700 tons at $2,000)** | **$227** | **113** |
| Odyssey, the high end (800 tons at $3,000) | $389 | |
| Odyssey, at Singapore's fourth-quarter price | $146 | |
| Odyssey, at Carnival's price | $93.64 | |
| Odyssey, at the pre-war price | $79.36 | |
| Carnival, per passenger, 2026 | $22.04 | 24 |
| Carnival, per passenger, 2025 | $16.40 | |
| Royal Caribbean, per passenger | $20.79 | 26.7 |
| Norwegian, per passenger | $27.17 | 33.2 |

Per person, the Odyssey burned 4.7 times the fuel of a Carnival passenger and spent 10.3 times the dollars. Even at Carnival's price, it would have spent 4.2 times. Since the war, fuel per resident was 2 times the daily rent.

The fuel bill, by Villa Vie's own figures (700 to 800 tons a month): $490,000 a month before the war, $1.4 million to $2.4 million after. Petterson told CBS spending went from $400,000 to $2.0 million a month; the company told CBS fuel went from $1,800 per cabin a month to $6,000 to $8,000.

## The money runs out

- **April 2026:** the company asked its residents for an emergency loan of $3.0 million, at 12% to 24% interest.
- **The surcharge:** $1,500 a month on top of the fees. Petterson said 70% of residents refused it. Paid in full, it would have covered 21.8% of each resident's fuel ($6,897 a month at the low end).
- **The internal documents** CBS reviewed, undated, show an average operating cost of $3.1 million a month against $2.5 million of revenue with the ship full and everyone paying the full fee: $600,000 short every month. Per cabin, $6,327 of cost against $5,102 of revenue, over 490 cabins; per resident at the end, $502 a day. A source close to the company says the cost was under $1 million a month.
- **August 2026:** 139 cabins still had no owner (351 did).
- **Hong Kong:** court records show the company paid a fuel supplier $167,844 for the ship to be released.
- **A resident paid** a fuel supplier $400,000 straight from a personal checking account, according to CBS's sources.
- **October 2026:** the ship docked in Cambodia with 203 residents and 156 crew. The residents had 36 hours to leave.

## What the cabins came with

A permanent cabin cost $119,999 to $439,999, sold with a promise of at least 15 years aboard, and owners still paid monthly fees. Villa Vie reportedly paid $13.0 million for the ship in 2023, built in 1993, with 485 cabins. Resident Darrell Carp told CBS he's out $250,000.

**The precedent.** In November 2023, with 111 cabins sold, Life at Sea called off its three-year world cruise shortly before departure and admitted it had no ship. Villa Vie's founder had been its managing director and left in May 2023 (CNN).

## What this number doesn't show

- **Villa Vie's numbers are the founder's and the company's words to the press**, not audited accounts. Even the $400,000 a month of pre-war spending Petterson cites is below his own consumption × price ($490,000).
- **Carnival doesn't burn the same fuel.** Its 10-K says most of its ships have scrubbers, which let them use heavy fuel oil; its price is the average of every fuel type, from June to August. Royal Caribbean and Norwegian are July to September and already net of their hedges.
- **The market price is Singapore's**, the world's largest bunkering port; small ports charge more, and there's no public price for Cambodia. The sources don't say whether Villa Vie paid more for buying small amounts, at short notice or on credit, or whether the figure overstates it.
- **The 700 to 800 tons a month** are the founder's figure and include time in port. The 203 residents are those aboard at the end; there were more people aboard earlier, which would spread the bill thinner.
- **The $3,499 rent** is the price on the company's site in November 2026; buyers paid for the cabin plus a monthly fee, and contracts varied. Royal Caribbean's cost and revenue are per berth (two per cabin), on much bigger ships, and include marketing and administration.
- **The internal documents have no date** in CBS's report, and a source close to the company disputes the cost. Assisted living isn't the same service: it includes nursing care the ship didn't offer.
- **Residents' monthly fees differ between sources** and stayed out of the count. As of early November 2026, no Chapter 11 filing had been reported.

## Reproduce it

```
python calc.py
```

Standard library only, no network. It reads the files in `data/`:

- `inputs.csv`: every value taken from the SEC filings, as published and in the filing's unit, with the exact sentence or table row and the document's URL;
- `published_figures.csv`: Villa Vie's figures, the Singapore prices, the site's prices, the internal documents CBS reviewed, assisted living, the retirement benefit and Life at Sea, each with a description and the source URL;
- `quotes.csv`: the sentence from Carnival's 10-K about scrubbers (no number comes from it).

It prints the consistency checks (the founder's $2 million a month fits his own consumption × price; Carnival's passenger days over berth days give its published occupancy; price per ton × tons matches each company's fuel line; Royal Caribbean's cost without fuel plus fuel per berth gives its cost with fuel; Villa Vie's pre-war price matches Singapore's on February 27) and writes `numbers.json`.

## Sources

**SEC filings**

- [Carnival, Form 10-Q, third fiscal quarter of 2026 (June to August; September 29, 2026)](https://www.sec.gov/Archives/edgar/data/815097/000081509726000107/ccl-20260831.htm)
- [Carnival, Form 10-K, fiscal 2025 (January 27, 2026)](https://www.sec.gov/Archives/edgar/data/815097/000081509726000007/ccl-20251130.htm)
- [Royal Caribbean, Form 10-Q, third quarter of 2026 (October 27, 2026)](https://www.sec.gov/Archives/edgar/data/884887/000088488726000044/rcl-20260930.htm)
- [Royal Caribbean, Form 8-K of October 27, 2026 (third-quarter results)](https://www.sec.gov/Archives/edgar/data/884887/000088488726000042/a2026q3earningsrelease.htm)
- [Norwegian Cruise Line Holdings, Form 10-Q, third quarter of 2026 (October 29, 2026)](https://www.sec.gov/Archives/edgar/data/1513761/000110465926120217/nclh-20260930x10q.htm)
- [Norwegian Cruise Line Holdings, Form 8-K of October 29, 2026, exhibit 99.1 (third-quarter results)](https://www.sec.gov/Archives/edgar/data/1513761/000117184326006957/exh_991.htm)

**Villa Vie and the press**

- [CBS News, the Odyssey's never-ending cruise ends over fuel costs (October 28, 2026)](https://www.cbsnews.com/news/mv-odyssey-luxury-never-ending-cruise-ends-fuel-costs/)
- [CBS News, the Villa Vie internal documents (October 30, 2026)](https://www.cbsnews.com/news/forever-cruise-odyssey-villa-vie-documents/)
- [The Walking Cruiser, Villa Vie Odyssey in Cambodia and fuel costs (citing Business Insider and Cambodian authorities)](https://www.thewalkingcruiser.com/post/villa-vie-odyssey-cambodia-fuel-costs)
- [Eye of the Flyer, the Villa Vie Odyssey nightmare for cabin buyers (November 5, 2026)](https://eyeoftheflyer.com/2026/11/05/villa-vie-odyssey-nightmare-cabin-buyers/)
- [Cruise Industry News, Villa Vie captain: guests sent ashore due to critical fuel situation (October 2026)](https://cruiseindustrynews.com/cruise-news/2026/10/villa-vie-captain-guests-sent-ashore-due-to-critical-fuel-situation/)
- [Wikipedia, Villa Vie Odyssey](https://en.wikipedia.org/wiki/Villa_Vie_Odyssey)
- [Villa Vie Residences, home page](https://villavieresidences.com/), [residency options](https://villavieresidences.com/residency-options/) and [rent-to-own](https://villavieresidences.com/residency-options/rent-to-own) (read November 8, 2026)
- [ABC13, citing CNN: the three-year Life at Sea cruise canceled (November 25, 2023)](https://abc13.com/three-year-cruise-canceled-life-at-sea-refund/14102701/)

**Market and U.S. data**

- [Ship & Bunker, Singapore bunker prices](https://shipandbunker.com/prices/apac/sea/sg-sin-singapore) (read November 8, 2026)
- [CareScout, Cost of Care Survey](https://www.carescout.com/cost-of-care)
- [Social Security Administration, Monthly Statistical Snapshot](https://www.ssa.gov/policy/docs/quickfacts/stat_snapshot/)

## Corrections

None so far. Found an error? Open an issue with the line and the source.

## License

Code (`calc.py`): [MIT](../LICENSE). Data, text and tables: [CC BY 4.0](../LICENSE-DATA.md); the underlying public records keep their own terms.

# #013 · Las Vegas airport: fewer passengers, and the airlines pay more for each one

**Video:** https://youtu.be/QqbY0PaNKEs

## The answer

Harry Reid International (LAS) expects to charge airlines **$9.13** for every passenger who boards in fiscal 2027 (July 2026 to June 2027), on average: everything the airlines pay the airport (landing fees, terminal rent, apron, federal inspection), split among the passengers who board. Its estimate for fiscal 2024 was $6.49. The estimate went up every year: $6.49 (2024), $7.27 (2025), $8.69 (2026), $9.13 (2027).

Over the same time, passengers fell. From January 2025 to August 2026, 20 of 20 months had fewer passengers leaving LAS than the same month a year earlier. Most of the drop is one airline: in 2025, Spirit carried 1.7 million fewer passengers out of Las Vegas than in 2024, 99.0% of the whole airport's loss (1.7 million). Spirit stopped flying on May 2, 2026.

Why the charge rises when passengers fall: the airport's agreement with its airlines (extended through June 30, 2030) is residual by cost center. The airlines cover whatever the runways, the terminal and the apron cost each year; the number of passengers only decides how many people that bill is split among.

## How we counted

- **Cost per enplanement (CPE)**, from the FAA's Form 5100-127: line 1.6 (everything passenger airlines pay the airport) / line 16.1 (enplanements: passengers who board, connecting passengers included). `calc.py` checks it against the CPE printed on each form. Fiscal years run from July to June.
- **Estimated and actual.** The airport publishes an estimated CPE at the start of each fiscal year (rates and charges, bond official statements) and an actual one after it ends (its annual report, the ACFR). The FAA form measures a little differently from the ACFR. Fiscal 2025, three ways: estimated $7.27, actual in the ACFR $6.82, Form 127 $7.13. The rise in the answer compares estimate with estimate.
- **Passengers by airline**: BTS T-100 Segment (all carriers), passengers and seats on flights leaving LAS, by airline and month. BTS has published through August 2026. The airport's own monthly reports count passengers arriving and departing, through September.
- **Fares**: US DOT Consumer Airfare Report, Table 1 (the top 1,000 city-pair markets in the lower 48), first quarter of each year, weighted by passengers. "Cheapest fare" is the table's average fare of the airline with the lowest fare in each market.
- **Jet fuel**: EIA, U.S. Gulf Coast kerosene-type jet fuel, spot price, monthly average.

## The bill per passenger, fiscal 2012 to 2025 (Form 127)

| Fiscal year | Enplanements | Everything airlines pay (1.6) | Per enplaned passenger |
|---|---|---|---|
| 2012 | 21.0 million | $128.9 million | $6.15 |
| 2013 | 20.9 million | $257.6 million | $12.34 |
| 2014 | 21.2 million | $252.5 million | $11.90 |
| 2015 | 21.9 million | $257.9 million | $11.79 |
| 2016 | 23.3 million | $262.3 million | $11.24 |
| 2017 | 24.0 million | $258.0 million | $10.75 |
| 2018 | 24.6 million | $247.7 million | $10.05 |
| 2019 | 25.2 million | $253.7 million | $10.06 |
| 2020 | 19.0 million | $243.5 million | $12.79 |
| 2021 | 13.2 million | $220.4 million | $16.71 |
| 2022 | 24.0 million | $170.2 million | $7.09 |
| 2023 | 28.3 million | $202.6 million | $7.17 |
| 2024 | 29.1 million | $156.3 million | $5.36 |
| 2025 | 28.6 million | $204.3 million | $7.13 |

Terminal 3 opened in June 2012; the next fiscal year, the bill per passenger doubled. The 2021 peak is the pandemic, with travelers at home; federal pandemic aid then went partly toward rent relief for the airlines, and the county spent the last of it by mid-2024. `data/form127.csv` also has, for every year, landing fees, terminal rents, parking, non-airline revenue, operating revenue and expenses, grants, debt, cash, interest and debt service.

## The airport's own figures, fiscal 2024 to 2028

| Fiscal year | Estimated CPE | Actual |
|---|---|---|
| 2024 | $6.49 (bond official statement, March 2024) | $5.10 (ACFR); $5.36 (Form 127) |
| 2025 | $7.27 | $6.82 (ACFR); $7.13 (Form 127) |
| 2026 | $8.69 | $9.45 from July 2025 to March 2026, against $7.61 in the same months a year earlier |
| 2027 | $9.13 | |
| 2028 | $10.14 (projection, bond official statement, June 2026) | |

From fiscal 2024 to 2027, the estimate rose $2.64 a passenger. In the rates that took effect on July 1, 2026, the signatory landing fee went from $1.49 to $1.78 per 1,000 pounds of landed weight: it follows the plane's weight, not the people on board. The Passenger Facility Charge, collected on the ticket and not part of the CPE, is $4.50.

## Where the rest of the money comes from, fiscal 2025

| Per enplaned passenger (Form 127) | |
|---|---|
| Operating expenses, before depreciation | $11.99 |
| Debt service | $8.69 |
| **Everything passenger airlines pay** | **$7.13** |
| Parking and ground transportation | $3.81 |
| Rental cars (without the customer facility charge) | $1.96 |
| Food and beverage | $1.37 |
| Retail and duty free | $1.29 |
| Terminal services and other | $3.28 |
| All revenue that doesn't come from airlines | $12.53 |
| Operating revenue | $21.12 |

Passenger airlines paid 33.8% of the airport's operating revenue in fiscal 2025 (28.4% in 2024, 47.2% in 2019). The airport's slot machines brought in $59.6 million in fiscal 2025 (bond official statement, June 2026). Under the airline agreement, slot and rental-car revenue stays with the airport and doesn't lower what airlines pay.

## Against the other large hubs

| | Fiscal 2019 | Fiscal 2024 | Fiscal 2025 |
|---|---|---|---|
| Large hubs with a Form 127 | 30 | 30 | 30 |
| LAS's place (1 = charges airlines least per passenger) | 14 | 3 | 3 |
| Median CPE of the large hubs | $10.52 | $12.82 | $14.83 |
| LAS | $10.06 | $5.36 | $7.13 |

In fiscal 2025, only Atlanta ($4.48) and Charlotte ($6.49) charged airlines less per passenger.

## Who left: Spirit (BTS T-100, flights leaving LAS)

| | 2019 | 2024 | 2025 |
|---|---|---|---|
| Passengers, all airlines | 24.9 million | 28.3 million | 26.7 million |
| Spirit | 2.7 million | 4.0 million | 2.3 million |
| Spirit's share | 10.8% | 14.0% | 8.6% |

Every airline except Spirit, together, changed by -16,870 passengers in 2025. Spirit's busiest month was July 2024, with 384,196 passengers out of Las Vegas; in December 2025 it carried 69,468.

| January to August | 2024 | 2025 | 2026 |
|---|---|---|---|
| Passengers, all airlines | | 18.0 million | 16.7 million |
| Spirit passengers | 2.6 million | 1.8 million | 248,306 |
| Passengers, every airline except Spirit | 16.2 million | 16.2 million | 16.4 million |
| Seats, all airlines | | 23.2 million | 21.1 million |
| Spirit seats | | 2.3 million | 336,028 |
| Seats, every airline except Spirit | | 20.9 million | 20.8 million |
| Load factor (passengers / seats) | 81.1% | 77.6% | 78.7% |
| WestJet, Air Canada, Air Canada Rouge, Flair and Porter | 604,601 | 490,893 | 384,531 |

From January to August 2026, against the same months of 2025: 1.3 million fewer passengers, 1.6 million fewer on Spirit and 232,221 on everyone else; Spirit offered 2.0 million fewer seats and the other airlines -62,369. Month by month, without Spirit, the other airlines went from -4.8% (worst month) to 5.9% (best month) against a year earlier, and were up in 12 of the 20 months.

## Did the other airlines fill Spirit's seats? (January to August 2026)

| | Las Vegas (LAS) | Fort Lauderdale (FLL) | Orlando (MCO) |
|---|---|---|---|
| Spirit seats removed, against 2024 | 2.9 million | 2.7 million | 2.3 million |
| Seats the other airlines added, against 2024 | 833,496 | 1.2 million | 2.1 million |
| **Added per seat Spirit removed, against 2024** | **28.9%** | **45.8%** | **91.8%** |
| Spirit seats in 2025 | 2.3 million | 3.9 million | 2.7 million |
| Spirit seats removed, against 2025 | 2.0 million | 2.0 million | 1.6 million |
| Seats the other airlines added, against 2025 | -62,369 | 1.7 million | 1.2 million |
| Added per seat Spirit removed, against 2025 | -3.2% | 86.2% | 76.3% |
| Passengers leaving, 2026 against 2025 | -7.4% | -1.3% | -0.33% |

The answer depends on the base year, so the table shows both. Two other counts, in other units: Frontier said on its October 28, 2026 earnings call that it had replaced about 25% of the capacity Spirit dropped, across its whole network; the LVCVA's air service consultant told its board on August 11, 2026 that more than 50% of Spirit's lost Las Vegas capacity had been replaced, counting scheduled seats.

## The fare (US DOT, Table 1, first quarter)

| | 2019 | 2024 | 2025 | 2026 |
|---|---|---|---|---|
| Markets with Las Vegas among the top 1,000 | 64 | 63 | 61 | 63 |
| Average fare, markets with Las Vegas | $188 | $226 | $227 | $257 |
| Average fare, all top 1,000 markets | $210 | $234 | $240 | $259 |
| **Las Vegas below the average** | **$21.84** | **$8.80** | **$13.29** | **$1.97** |
| Las Vegas markets where Spirit was the cheapest | 14 | 29 | 25 | 7 |
| Cheapest airline's fare, markets with Las Vegas | $125 | $142 | $141 | $167 |

In 18 Las Vegas markets, Spirit was the cheapest airline in early 2025 and no longer was in early 2026. There, the cheapest fare went from $112 to $188 (67.2%). In the Las Vegas markets where Spirit wasn't the cheapest, it went from $176 to $178 (1.1%). Both averages use early-2026 passengers as weights. Chicago-Las Vegas: Spirit at $122 in early 2025, Southwest at $220 a year later.

Jet fuel (U.S. Gulf Coast, spot, per gallon): $2.15 in October 2025, $2.26 in February 2026, $3.70 in March 2026 and $4.48 in October 2026. Fuel and Spirit's exit hit fares at the same time, and this math doesn't separate them.

## The city and the airport

- The LVCVA counts 28.9 million visitors to Las Vegas from January to September 2026 (-0.1% against 2025), while passengers at the airport fell -7.3% and daily cars on I-15 at the California state line rose 5.8%. The airport's own traffic reports: 38.4 million passengers arriving and departing from January to September 2026, against 41.4 million a year earlier (3.0 million fewer).
- In 2025, 47% of Las Vegas visitors arrived by air (LVCVA visitor profile). Visitors for the whole year: 41.7 million in 2024, 38.5 million in 2025.
- Nonstop air passengers from Canada to Las Vegas: 900,929 in 2024, 678,803 in 2025 (LVCVA).
- Nearby airports didn't fall: Phoenix 0.9% (January to June 2026), Reno 1.4% (January to September 2026).
- On October 20, 2026, the county laid out a plan to take Terminal 1 from 39 gates to about 65 by late 2034, with no price yet.

## What this number doesn't show

- The headline figure is the airport's estimate at the start of the fiscal year, not the final bill. The actual CPE comes later, in the ACFR and in the FAA's Form 127, which measure a little differently.
- The fiscal 2024 figure is the estimate in the March 2024 bond official statement, not a rates and charges book.
- What the airport charges airlines per passenger is a small part of a ticket. Fares to Las Vegas rose in 2026 while jet fuel got more expensive and Spirit left; this math doesn't separate the causes.
- Visitors to Las Vegas held steady from January to September 2026 while airport passengers fell: the drop is in people arriving by air, not in people visiting. That more visitors drove in is a reading of the I-15 count, not a measured switch.
- How many of Spirit's seats were replaced depends on the base: against 2025, the other airlines added no seats in Las Vegas; against 2024, they added less than a third; the LVCVA's consultant, counting scheduled seats, speaks of more than half.
- BTS passengers by airline go through August 2026, the airport's own counts through September. BTS counts passengers leaving; the airport counts arriving and departing.

## Reproduce it

```
python calc.py
```

Standard library only, no network. It reads the files in `data/`:

- `form127.csv`: Harry Reid's Form 5100-127 for every fiscal year from 2012 to 2025, and every large hub's for 2019, 2024 and 2025, with the columns used ("" = not filled in);
- `t100_departures.csv`: passengers and seats on flights leaving LAS (2019, 2024 to 2026), Fort Lauderdale and Orlando (2024 to 2026), added up by year, airline and month;
- `dot_table1.csv`: the rows of DOT's Table 1 for the first quarters of 2019, 2024, 2025 and 2026, with the columns used;
- `eia_jet_fuel.csv`: the jet fuel months cited;
- `published_figures.csv`: the figures read from the airport's documents, the LVCVA, other airports and Frontier, with a description and the source URL.

It prints the consistency checks (the airline lines of every form add up to the declared total; our CPE matches the one printed on each form; the fiscal 2025 revenue lines add up; one form per large hub; Spirit plus everyone else equals all airlines; the Form 127 enplanements match BTS within 5%; the last BTS month is the same at the three airports; enough Las Vegas markets in each DOT quarter; the estimate rises every year) and writes `numbers.json`.

## Sources

- [FAA CATS, Form 5100-127, fiscal 2012 to 2025](https://cats.airports.faa.gov/reports)
- [FAA, Advisory Circular 150/5100-19D (Form 127 line definitions)](https://www.faa.gov/documentLibrary/media/Advisory_Circular/150_5100_19d.pdf)
- [BTS, T-100 Segment (All Carriers)](https://www.transtats.bts.gov/DL_SelectFields.aspx?gnoyr_VQ=FMG&QO_fu146_anzr=Nv4%20Pn44vr45)
- [US DOT, Consumer Airfare Report, Table 1 (top 1,000 city-pair markets)](https://data.transportation.gov/Aviation/Consumer-Airfare-Report-Table-1-Top-1-000-Contiguo/4f3n-jbg2)
- [U.S. EIA, Gulf Coast jet fuel spot price](https://www.eia.gov/dnav/pet/hist/LeafHandler.ashx?n=PET&s=EER_EPJK_PF4_RGC_DPG&f=M)
- [Clark County bonds, Series 2024B official statement](https://dwuconsulting.com/api/documents/download?documentId=LAS-OS_RECENT-2024B)
- [Harry Reid International, Rates and Charges (effective July 1, 2025)](https://fsweb.harryreidairport.com/fswebfile/688d3c86-e8f7-43d3-a5a2-bf93995568fc/1400849/Rates%20and%20Charges.pdf)
- [Harry Reid International, Rates and Charges (effective July 1, 2026)](https://assets.ctfassets.net/2pnrhs9eukyp/4nXNriK8IAhdbEWSLxJD6p/c532afc4ad91c6efc230a3ef091b2e1d/RATE_SHEET_FY27_Rates_and_Charges_-_Eff_7-1-26.pdf)
- [Clark County bonds, Series 2026 official statement](https://emma.msrb.org/P22045925-P21557055-P22016083.pdf)
- [Clark County Department of Aviation, ACFR fiscal 2025](https://assets.ctfassets.net/2pnrhs9eukyp/csh5qFYrkEfJOizUHk3WB/c1802541a7dceede109a18d9c6cc0203/FY25_CCDOA_ACFR_FINAL.pdf)
- [Clark County Dept. of Aviation, Q3 fiscal 2026 report](https://assets.ctfassets.net/2pnrhs9eukyp/RZelfFJtrpKqhttB1qZ1l/4834131d76df7cb8a0d31568543cf399/FY26_Q3_Financial_Report.pdf)
- [Harry Reid International, 2026 traffic statistics](https://www.harryreidairport.com/business/airport-operations/financial-reporting-statistics/airport-activity/2026-aviation-statistics)
- [LVCVA, Executive Summary, September 2026](https://assets.simpleviewcms.com/simpleview/image/upload/v1/clients/lasvegas/ES_Sep2026_revised_37937aa3-f16c-455a-b73c-cec6876e4bbb.pdf)
- [LVCVA, Year to Date Summary 2024](https://assets.simpleviewcms.com/simpleview/raw/upload/v1/clients/lasvegas/Year_to_Date_Summary_for_2024_0d625f44-ecbe-4fc2-917b-a2e6b3c794d3.xlsx)
- [LVCVA, Year to Date Summary 2025 (revised)](https://assets.simpleviewcms.com/simpleview/raw/upload/v1/clients/lasvegas/Year_to_Date_Summary_for_2025_revised_cd675d1a-2e15-4a20-aeeb-e6a6d871b10a.xlsx)
- [LVCVA, Las Vegas Visitor Profile Study 2025](https://assets.simpleviewcms.com/simpleview/image/upload/v1/clients/lasvegas/2025_Las_Vegas_Visitor_Profile_Study_db57c923-1f87-4ab8-868d-d6fc0bf2f972.pdf)
- [LVCVA, 2025 Top Air Markets](https://assets.simpleviewcms.com/simpleview/image/upload/v1/clients/lasvegas/2025_Top_Air_Markets_City_State_Intl_1f39499a-7aed-442c-b405-50c2237e31fe.pdf)
- [Phoenix Sky Harbor, June 2026](https://www.skyharbor.com)
- [Reno-Tahoe, September 2026](https://www.renoairport.com)
- [Frontier Group, Q3 2026 earnings call (Oct. 28, 2026)](https://www.fool.com/earnings/call-transcripts/2026/10/28/frontier-ulcc-q3-2026-earnings-call-transcript/)
- [LVCVA board minutes (Aug. 11, 2026)](https://assets.simpleviewcms.com/simpleview/image/upload/v1/clients/lasvegas/Minutes_August_11_2026_BOD_1b302dc4-aeec-4578-8af4-0680ff1daefb.pdf)
- [96.3 KKLZ (Oct. 20, 2026)](https://963kklz.com/2026/10/20/las-vegas-harry-reid-international-airport-maps-out-multibillion-dollar-overhaul/)

## Corrections

None so far. Found an error? Open an issue with the line and the source.

## License

Code (`calc.py`): [MIT](../LICENSE). Data, text and tables: [CC BY 4.0](../LICENSE-DATA.md); the underlying public records keep their own terms.

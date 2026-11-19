# #015 · UPS is shrinking on purpose: what does each package that stayed pay?

**Video:** https://youtu.be/C38zxLaXWk8

## The answer

UPS told investors in January 2025 that it would cut its largest customer's volume (Amazon, per the 10-K) by more than 50%. It says the cut was done in the second quarter of 2026.

From July–September 2024 to July–September 2026, UPS's U.S. packages went from 18.4 million a day to 15.6 million, and the average revenue per package went from $12.27 to $14.29: **$2.02 more on each package** ($1.23 after inflation).

Operating profit per package rose too, from $0.72 to $0.89 (+$0.18). But in the same years the segment took on the U.S. Postal Service's air cargo, which UPS reports inside this segment and does not count as packages. Spread over the packages, cargo revenue rose $0.22, more than the profit per package did. UPS doesn't publish the cost or the profit of that cargo, so nobody outside can say how much of the profit gain is packages and how much is cargo.

## How we counted

- **Packages** = average daily package volume x operating days, from the U.S. Domestic Package segment table in each 10-Q and 10-K.
- **Revenue per package** = the "Total Average Revenue Per Piece" UPS publishes. It leaves out air cargo, which UPS measures by weight. `calc.py` rebuilds it from the revenue lines and the volume, and checks it against the published one.
- **Profit per package** = segment operating profit / packages. UPS also publishes an "adjusted" profit, without transformation costs (mostly driver buyouts); we show both.
- **2024** uses the figures UPS recast after U.S. air cargo moved into this segment in Q4 2024 (from the comparison columns of the 2025 filings), so the years compare the same way.
- **Q4** = the full year minus the first nine months.
- **Inflation**: CPI-U, July–September average, BLS.

## Per package, quarter by quarter

| U.S. Domestic Package | Packages a day | Revenue per package | Operating profit per package | Adjusted | Cargo revenue per package |
|---|---|---|---|---|---|
| Q1 2024 | 18.1 million | $12.50 | $0.73 | $0.74 | $0.03 |
| Q2 2024 | 17.9 million | $12.35 | $0.86 | $0.87 | $0.07 |
| **Q3 2024** | **18.4 million** | **$12.27** | **$0.72** | **$0.78** | **$0.12** |
| Q4 2024 | 22.4 million | $12.25 | $1.21 | $1.26 | $0.22 |
| Q1 2025 | 17.4 million | $13.06 | $0.91 | $0.93 | $0.32 |
| Q2 2025 | 16.6 million | $13.03 | $0.86 | $0.93 | $0.27 |
| Q3 2025 | 16.2 million | $13.47 | $0.58 | $0.88 | $0.28 |
| Q4 2025 | 20.0 million | $13.27 | $1.15 | $1.38 | $0.26 |
| Q1 2026 | 16.0 million | $13.91 | $0.52 | $0.57 | $0.29 |
| Q2 2026 | 16.0 million | $14.24 | $0.02 | $1.16 | $0.33 |
| **Q3 2026** | **15.6 million** | **$14.29** | **$0.89** | **$1.02** | **$0.35** |

Q2 2026, when the Amazon cut finished, carried $1.14 per package of transformation costs; that is why the operating profit per package was $0.02 and the adjusted one $1.16.

## The receipt of one package

The receipt only closes with the cargo in it: segment revenue per package (packages plus cargo) minus operating expenses per package equals operating profit per package.

| Per package | Q3 2024 | Q3 2026 |
|---|---|---|
| Revenue per package (no cargo) | $12.27 | $14.29 |
| + Cargo revenue spread over packages | $0.12 | $0.35 |
| = Segment revenue per package | $12.39 | $14.64 |
| - Operating expenses per package (cargo included) | $11.68 | $13.75 |
| = Operating profit per package | $0.72 | $0.89 |

With rounding to the cent, 2024 is off by one cent.

## Before and after

| U.S. Domestic Package | Q3 2024 to Q3 2026 | Q3 2025 to Q3 2026 | First nine months, 2024 to 2026 |
|---|---|---|---|
| Revenue per package | +$2.02 (16.5%) | +$0.82 (6.1%) | +$1.78 (14.4%) |
| Operating profit per package | +$0.18 (24.7%) | +$0.31 (52.9%) | -$0.30 (-38.5%) |
| Adjusted profit per package | +$0.24 (30.5%) | +$0.14 (16.3%) | +$0.12 (15.1%) |
| Cargo revenue per package | +$0.22 | +$0.06 | +$0.25 |
| Packages a day | 2.8 million fewer (15.1%) | 529,000 fewer (3.3%) | 2.2 million fewer (12.3%) |
| Total segment operating profit | 7.5% | 50.2% | -46.1% |

Cargo revenue went from $147.0 million in Q3 2024 to $352.0 million in Q3 2026 (up 139.5%). Inflation over the same quarters was 6.5%: in 2026 dollars, Q3 2024's revenue per package would be $13.06 and its profit per package $0.76.

## The cuts

- **Amazon:** 11.8% of UPS's consolidated revenue in 2024 (about $10.7 billion of $91.1 billion), 10.6% in 2025.
- **Jobs:** UPS had 406,000 employees in the U.S. at the end of 2024 and 370,000 at the end of 2025 (36,000 fewer; temporary seasonal employees excluded). It says it cut about 48,000 operational positions in 2025, 15,000 of them seasonal.
- **Buildings:** daily operations closed at 93 buildings in 2025 (85 permanently) and 47 buildings closed from January to September 2026 (46 permanently).
- **Drivers:** the press reports a $150,000 lump sum offered to about 105,000 full-time drivers in 2026, capped at 7,500 buyouts in the settlement with the Teamsters; only 3,000 drivers took the smaller 2025 offer. UPS says $1.2 billion of its expected 2026 transformation costs is for that program.
- **Savings and costs:** UPS says it computed about $3.5 billion of cost savings in 2025, while the program cost $509.0 million that year ($505.0 million in this segment's transformation costs).

## For comparison: FedEx

FedEx's Express U.S. Domestic segment, July–September 2026: 14.4 million packages a day (2.0% against a year earlier), $15.32 of revenue and $1.03 of operating income per package. FedEx defines the segment differently (it includes U.S. air freight), so this is an order of magnitude, not a ranking.

## What this number doesn't show

- **Air cargo is inside the profit and outside the packages.** UPS doesn't say how much of "Cargo and Other" is the Postal Service, and doesn't publish the cost or profit of the cargo. The only cargo cost it mentions is "air cargo expense", up $64.0 million in Q3 2025 while cargo revenue rose $147.0 million; UPS doesn't say what that line includes.
- **Profit per package was already rising before the Amazon cut weighed in:** from Q1 2024 to Q1 2025 it rose $0.17, with cargo revenue going from $32.0 million to $341.0 million.
- **Two profits.** Over the first nine months of 2026, operating profit per package ($0.47) was below 2024's ($0.77); the adjusted one was above ($0.92 against $0.80).
- **UPS doesn't publish how many Amazon packages it carried or what it earned on them.** The 15.1% drop in packages a day also includes other e-commerce volume UPS says it let go and a weak market.
- **UPS gives no split of the revenue gain.** It credits rates, fuel surcharges and customer mix, and calls the Amazon agreement part of a shift to higher-yielding volume, without saying how much came from the cut.
- **Q4, with the holiday peak, earns the most per package** ($1.21 in 2024), so we compare quarter with quarter. Q4 2026 isn't out yet.
- **Ground Saver:** since 2026, part of it has its last mile done by the Postal Service again; the 10-Q doesn't say whether those packages leave UPS's count.
- **Press figures:** the buyout amount, the number of drivers offered, the cap and the 2026 job-cut forecast (30,000) come from the press, not from a UPS filing. The positions UPS reports cutting include seasonal ones; it doesn't say how many were layoffs.
- **Inflation** is consumer inflation (CPI-U), not UPS's costs.

## Reproduce it

```
python calc.py
```

Standard library only, no network. It reads the files in `data/`:

- `ups_segment_tables.csv`: the U.S. Domestic Package segment table of each filing, period by period, as published (thousands of packages, dollars per piece, days, millions of dollars), with the document and its URL;
- `fedex_segment.csv`: FedEx's Express U.S. Domestic segment, July–September 2025 and 2026;
- `bls_cpi_u_monthly.csv`: CPI-U, July to September 2024 and 2026;
- `published_figures.csv`: company statements (Amazon cut, jobs, buildings, program costs, consolidated revenue) and the press figures on the driver buyouts, each with a description and the source URL.

It prints the consistency checks (each table adds up; revenue per piece rebuilt from revenue and volume; three quarters equal the nine months; the receipt closes; FedEx's table adds up; the buyout cap fits the program cost) and writes `numbers.json`.

## Sources

**UPS (CIK 1090727)**

- [UPS, Form 10-K 2024 (February 18, 2025)](https://www.sec.gov/Archives/edgar/data/1090727/000109072725000019/ups-20241231.htm)
- [UPS, Form 10-K 2025 (February 17, 2026)](https://www.sec.gov/Archives/edgar/data/1090727/000162828026008432/ups-20251231.htm)
- [UPS, Form 10-Q, Q1 2025 (May 7, 2025)](https://www.sec.gov/Archives/edgar/data/1090727/000109072725000049/ups-20250331.htm)
- [UPS, Form 10-Q, Q2 2025 (August 6, 2025)](https://www.sec.gov/Archives/edgar/data/1090727/000109072725000064/ups-20250630.htm)
- [UPS, Form 10-Q, Q3 2025 (November 5, 2025)](https://www.sec.gov/Archives/edgar/data/1090727/000162828025049661/ups-20250930.htm)
- [UPS, Form 10-Q, Q1 2026 (May 6, 2026)](https://www.sec.gov/Archives/edgar/data/1090727/000162828026031154/ups-20260331.htm)
- [UPS, Form 10-Q, Q2 2026 (August 5, 2026)](https://www.sec.gov/Archives/edgar/data/1090727/000162828026053249/ups-20260630.htm)
- [UPS, Form 10-Q, Q3 2026 (November 4, 2026)](https://www.sec.gov/Archives/edgar/data/1090727/000162828026070246/ups-20260930.htm)
- [UPS, Form 8-K, January 30, 2025, exhibit 99.1](https://www.sec.gov/Archives/edgar/data/1090727/000109072725000004/exhibit991-earningspressre.htm)
- [UPS, Form 8-K, April 29, 2025, exhibit 99.1](https://www.sec.gov/Archives/edgar/data/1090727/000109072725000046/exhibit991-earningspressre.htm)
- [UPS, Form 8-K, January 27, 2026, exhibit 99.1](https://www.sec.gov/Archives/edgar/data/1090727/000162828026003510/exhibit991-earningspressre.htm)
- [UPS, Form 8-K, October 27, 2026, exhibit 99.1](https://www.sec.gov/Archives/edgar/data/1090727/000162828026067381/exhibit991-earningspressre.htm)

**FedEx (CIK 1048911)**

- [FedEx, Form 10-Q, quarter ended September 30, 2026](https://www.sec.gov/Archives/edgar/data/1048911/000104891126000131/fdx-20260930.htm)

**Press**

- [FreightWaves (February 21, 2026): the $150,000 driver buyout and the judge's ruling](https://www.freightwaves.com/?p=570756)
- [Supply Chain Dive (April 6, 2026): the cap on buyouts in the Teamsters settlement](https://www.supplychaindive.com/news/ups-driver-buyouts-teamsters-union-settlement-deal/816685/)
- [FOX / KTVU (January 27, 2026): UPS may cut up to 30,000 jobs in 2026](https://www.ktvu.com/news/ups-looks-cut-up-30000-jobs-year)

**U.S. prices**

- [BLS, CPI-U, all items, U.S. city average](https://data.bls.gov/timeseries/CUUR0000SA0)

## Corrections

None so far. Found an error? Open an issue with the line and the source.

## License

Code (`calc.py`): [MIT](../LICENSE). Data, text and tables: [CC BY 4.0](../LICENSE-DATA.md); the underlying public records keep their own terms.

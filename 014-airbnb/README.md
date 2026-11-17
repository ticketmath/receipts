# #014 · Airbnb: who gets each part of a night?

**Video:** coming soon

## The answer

In 2025, the average night booked on Airbnb in North America cost **$255**, everything included: the host's price, the cleaning fee, Airbnb's fees and local taxes. Airbnb kept **$32.89** of it, 12.9% of the bill. The other **$222** is the host's side: the host's pay, the cleaning fee and the taxes, which Airbnb's annual report keeps in one pile.

Airbnb's share barely moves. In North America it was 12.6% in 2021 and 12.9% in 2025. Worldwide, the average night went up $55.11 from 2019 to 2025: **$8.27 went to Airbnb** and $46.85 to the host's side.

In 2019, Airbnb lost $2.06 on an average night booked. In 2025 it made $4.71, on 533.0 million nights instead of 326.9 million.

## How we counted

- **The night** = Gross Booking Value / nights booked, both from the key business metrics tables in Airbnb's 10-K filings. Gross Booking Value is everything the guest pays: the host's price, cleaning fees, service fees and taxes. It's an average across studios and lake houses, so no single listing costs exactly that.
- **Airbnb's part** = revenue / nights booked. Worldwide revenue comes from each 10-K's XBRL; North American revenue from the regional table. `calc.py` checks our 2021 GBV per night against the one the 10-K writes in its text ($155.93 worldwide, $221.92 for North America).
- **The host's side** = the night minus Airbnb's part. The report doesn't split it into pay, cleaning and tax, and there's no public figure for the average cleaning fee.
- **Where Airbnb's part goes**: each line of the income statement / nights booked, worldwide (the income statement has no regional split). `calc.py` checks that the costs plus operating income add up to revenue.
- **The fees**: Airbnb's Help Center (read November 16, 2026). `calc.py` checks that the share we compute fits what those fees allow, with taxes anywhere from zero to 20% of the subtotal.

## The night, year by year

| North America | Average night | Airbnb keeps | Airbnb's share |
|---|---|---|---|
| 2020 | $174 | $23.48 | 13.5% |
| 2021 | $222 | $28.08 | 12.6% |
| 2022 | $242 | $31.65 | 13.1% |
| 2023 | $239 | $31.77 | 13.3% |
| 2024 | $246 | $32.51 | 13.2% |
| **2025** | **$255** | **$32.89** | **12.9%** |

| Worldwide | Average night | Airbnb keeps | Airbnb's share |
|---|---|---|---|
| 2019 | $116 | $14.70 | 12.7% |
| 2020 | $124 | $17.48 | 14.1% |
| 2021 | $156 | $19.93 | 12.8% |
| 2022 | $160 | $21.32 | 13.3% |
| 2023 | $164 | $22.14 | 13.5% |
| 2024 | $166 | $22.57 | 13.6% |
| 2025 | $171 | $22.97 | 13.4% |

Worldwide nights are cheaper on average, because most of them are outside North America. In 2025: 533.0 million nights and seats booked, $91.3 billion of gross bookings, $12.2 billion of revenue; 158.0 million of those nights were in North America.

## Who got the increase

| Worldwide, per night | 2019 | 2025 | Change |
|---|---|---|---|
| The night | $116 | $171 | $55.11 (47.5%) |
| Airbnb | $14.70 | $22.97 | $8.27 (56.2%) |
| The host's side | $101 | $148 | $46.85 (46.2%) |

Airbnb got 15.0% of the increase. In North America, from 2021 to 2025, the night went up $33.05 (14.9%) and $4.81 of it went to Airbnb.

For comparison, U.S. prices (CPI-U, BLS): from 2019 to 2025, all items rose 25.9% and lodging away from home (hotels and motels) 12.5%; from 2021 to 2025, all items 18.8% and lodging 14.2%.

## Where Airbnb's part goes

| Worldwide, per night booked | 2019 | 2025 |
|---|---|---|
| Cost of revenue (payment processing, hosting the systems) | $3.66 | $3.91 |
| Operations and customer support | $2.49 | $2.49 |
| Product development (engineering) | $2.99 | $4.42 |
| Sales and marketing | $4.96 | $4.86 |
| General and administrative | $2.13 | $2.52 |
| **Operating income** | **-$1.53** | **$4.77** |
| **Net income** | **-$2.06** | **$4.71** |

In 2019, Airbnb's operating loss was $1.53 per night and its net loss $2.06. In 2025 it earned $2.5 billion.

## The fees Airbnb charges

- **Split fee** (the old model): most hosts pay 3%, and the guest pays 14.1% to 16.5% of the subtotal on top.
- **Single fee** (replacing it since October 2025): most hosts pay 15.5%, taken from their price, and the guest pays no separate service fee.
- **Taxes:** Airbnb says it collected and passed along $2.7 billion in tourism taxes in the U.S. in 2025, by its own count. In some places the host collects the tax.
- Airbnb says it has 5.0 million hosts.

## What this number doesn't show

- **The host's side is one pile.** The 10-K doesn't split it into the host's pay, the cleaning fee and the taxes, and there's no public figure for the average cleaning fee. What's left after taxes is the host's revenue, not profit.
- **Taxes can't be divided per night.** The $2.7 billion is Airbnb's own, unaudited figure; in some places the host collects the tax; and the 10-K's North America includes Canada.
- **Bookings and revenue are counted at different times.** Nights and Gross Booking Value count when a booking is made; revenue counts when the guest checks in. Dividing a year's revenue by the nights booked that year is an approximation that the pandemic distorts: in 2020, Airbnb's worldwide share was the highest in the series (14.1%), because revenue came from stays booked earlier while new bookings fell. Outside 2020 and 2021, the peak is 2024 (13.6%).
- **The count changed in 2025.** Airbnb now reports "nights and seats" (it includes seats on experiences and services); the 10-K says nearly all bookings are still nights. Since 2022 the 10-K rounds nights to the million.
- **The average mixes regions and property types.** If more bookings go to whole houses or pricier regions, the average rises without any listing getting more expensive (the 10-K says this for 2020 and 2021). The comparison with inflation and hotel prices is an order of magnitude.
- **Costs per night are worldwide.** The income statement has no North American split.
- **The fee percentages** are the Help Center's in November 2026; the switch from the split fee to the single fee is gradual, and dates by country come from secondary sources.
- **The BLS didn't collect October 2025's CPI** (government shutdown); the 2025 averages use the other 11 months.

## Reproduce it

```
python calc.py
```

Standard library only, no network. It reads the files in `data/`:

- `key_business_metrics.csv`: nights booked and Gross Booking Value (worldwide), and nights, Gross Booking Value and revenue (North America), in millions, as published in the 10-K tables, with the exact table row and the document's URL;
- `published_checks.csv`: the 2021 GBV per night the 10-K writes in its text, used only as a check;
- `income_statement.csv`: worldwide revenue for 2019 to 2025 and the income statement lines for 2019 and 2025, from each 10-K's XBRL;
- `bls_cpi_u_monthly.csv`: the monthly CPI-U (all items, and lodging away from home) for 2019, 2021 and 2025;
- `published_figures.csv`: the fees from Airbnb's Help Center, the taxes Airbnb says it remitted and the number of hosts, each with a description and the source URL.

It prints the consistency checks (our 2021 GBV per night against the 10-K's; costs plus operating income against revenue; the 2024 peak outside the pandemic; only October missing from the 2025 CPI; the 2025 share inside the range the published fees allow) and writes `numbers.json`.

## Sources

**SEC filings (Airbnb, CIK 1559720)**

- [Airbnb, Form 10-K 2021 (February 25, 2022): key business metrics for 2019 to 2021](https://www.sec.gov/Archives/edgar/data/1559720/000155972022000006/abnb-20211231.htm)
- [Airbnb, Form 10-K 2023 (February 16, 2024): key business metrics for 2022 and 2023](https://www.sec.gov/Archives/edgar/data/1559720/000155972024000006/abnb-20231231.htm)
- [Airbnb, Form 10-K 2025 (February 12, 2026): key business metrics for 2024 and 2025](https://www.sec.gov/Archives/edgar/data/1559720/000155972026000004/abnb-20251231.htm)
- [Airbnb, income statement 2019 (XBRL of the 2021 10-K)](https://www.sec.gov/Archives/edgar/data/1559720/000155972022000006/abnb-20211231_htm.xml)
- [Airbnb, income statement 2025 (XBRL of the 2025 10-K)](https://www.sec.gov/Archives/edgar/data/1559720/000155972026000004/abnb-20251231_htm.xml)
- Revenue by year: the XBRL of each 10-K, with the URL in `data/income_statement.csv`

**Airbnb**

- [Airbnb Help Center, Airbnb service fees](https://www.airbnb.com/help/article/1857) (read November 16, 2026)
- [Airbnb newsroom, hosts and guests boost the U.S. economy by a record $93B in 2025 (April 15, 2026)](https://news.airbnb.com/hosts-and-guests-boost-us-economy-by-a-record-93b-in-2025/)

**U.S. prices**

- [BLS, CPI-U, all items, U.S. city average](https://data.bls.gov/timeseries/CUUR0000SA0)
- [BLS, CPI-U, lodging away from home, U.S. city average](https://data.bls.gov/timeseries/CUUR0000SEHB)

## Corrections

None so far. Found an error? Open an issue with the line and the source.

## License

Code (`calc.py`): [MIT](../LICENSE). Data, text and tables: [CC BY 4.0](../LICENSE-DATA.md); the underlying public records keep their own terms.

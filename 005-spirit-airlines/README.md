# #005 · Spirit filled most of its seats and still went under: what did each passenger cost?

**Video:** https://youtu.be/z9aCdm3hzG0

## The answer

Spirit didn't go broke flying empty planes. In 2024 its planes were **82.4%** full (2019: 84.4%), and each passenger brought in **$111**, the same as in 2019. But each passenger cost **$33.34 more** to fly, before one-time charges. The 2026 fuel spike came after that.

## One Spirit passenger, 2019 against 2024 (operating revenue and costs ÷ passengers)

| | 2019 | 2024 | Change |
|---|---|---|---|
| Revenue per passenger | $111 | $111 | $0.30 |
| Cost per passenger, without special items | $95.88 | $129 | **$33.34** |
| Result per passenger, without special items | $15.03 | -$18.01 | |
| Cost per passenger, with special items | $96.40 | $136 | $39.83 |
| Load factor (10-K) | 84.4% | 82.4% | |

Where the extra cost came from, per passenger:

| Line | 2019 | 2024 | Change |
|---|---|---|---|
| Wages and benefits | $25.05 | $38.23 | $13.19 |
| Aircraft rent | $5.29 | $12.27 | $6.98 |
| Fuel | $28.77 | $33.48 | $4.72 |
| Landing fees and airport rents | $7.42 | $10.21 | $2.79 |
| Depreciation | $6.52 | $7.36 | $0.84 |
| Maintenance | $4.16 | $4.93 | $0.77 |
| Distribution | $4.45 | $4.46 | $0.01 |
| Other | $14.23 | $18.28 | $4.05 |

Wages per employee rose 32.1%, while passengers per employee changed -13.5%.

## Frontier, the same model

Frontier's cost per passenger (without sale-leaseback gains) rose **$19.43** from 2019 to 2024; Spirit's rise was **1.7 times** larger. Frontier: revenue per passenger $110 → $113, load factor 86.1% → 76.8%.

## 2026: the plan against the fuel

Spirit's March 2026 plan assumed fuel at **$2.22 a gallon** for the second quarter. In April 2026 it paid **$4.63** (2.1 times the plan). Above the plan's price, fuel cost **$88.9 million** in March and April, about **$30.10** per passenger in April. In the first quarter of 2026, Spirit's operating result (-$226.9 million) came in $180.9 million below the plan; fuel explains 14.6% of that gap. In April 2026, its last full month, its domestic flights were **83.0%** full.

## After: fares where Spirit left

Top 1,000 city-pair markets, average fare weighted by Q1 2024 passengers:

| Markets | Count | Q1 2024 | Q1 2026 | Change |
|---|---|---|---|---|
| Spirit left | 76 | $233 | $270 | 16.1% |
| Spirit stayed | 91 | $221 | $241 | 9.1% |
| Spirit never flew nonstop | 692 | $244 | $268 | 10.1% |

In 68 markets where Spirit had the lowest fare and another airline the largest share (Q1 2026), Spirit charged $113 against $274.

JetBlue agreed to buy Spirit in July 2022 for $3.8 billion (equity value); a federal court blocked the deal in January 2024. JetBlue lost money in 6 of the years from 2020 to 2025 ($795.0 million in 2024).

## Method

- **Passenger:** each passenger flight segment (a connecting trip counts twice), domestic and international together.
- **Special items:** special charges and loss (gain) on disposal of assets, as reported in Spirit's income statement. 2025 adds the predecessor and successor columns.
- **Frontier:** 2019 comes from the 2021 10-K; its sale-leaseback gains are added back to operating expenses.
- **2026:** the Form 41 data Spirit filed with the US DOT (unaudited) and the company's own plan, written for creditors.
- **Fares:** US DOT Consumer Airfare Report, Table 1. "Spirit left" = at least 3,000 nonstop Spirit passengers in Q1 2024 (both directions, BTS T-100) and none in Q1 2026. The fares include taxes but not bag, seat or change fees.

## What this number doesn't show

- The dollars are not adjusted for inflation. US prices rose 22.7% from 2019 to 2024: adjusted, revenue per passenger fell $24.87 short of 2019, and cost rose $11.57 beyond inflation.
- Load factor counts seats sold, not the price of each.
- Frontier also lost money: -$148.3 million operating result in 2025 and -$283.1 million in Q1 2026.
- Spirit chose which markets to leave, and fuel and other airlines changed too: the fare comparison shows a difference, not a cause.
- Nobody can know whether the JetBlue deal would have saved Spirit.

## Reproduce it

```
python calc.py
```

Standard library only, no network. It reads `data/inputs.csv` (every 10-K line or sentence, BLS index, T-100 and Form 41 total, plan column and assumption used, with the source URL on each row), `data/markets_q1.csv` and `data/cheapest_q1_2026.csv`, prints the consistency checks and writes `numbers.json`.

## Sources

- [Spirit Airlines, Form 10-K 2019](https://www.sec.gov/Archives/edgar/data/1498710/000149871020000083/save-20191231x10kss.htm)
- [Spirit Airlines, Form 10-K 2024](https://www.sec.gov/Archives/edgar/data/1498710/000149871025000008/save-20241231.htm)
- [Spirit Aviation Holdings, Form 10-K 2025](https://www.sec.gov/Archives/edgar/data/1498710/000162828026018265/flyy-20251231.htm)
- [BTS, T-100 Domestic Segment](https://www.transtats.bts.gov/DL_SelectFields.aspx?gnoyr_VQ=FIM&QO_fu146_anzr=Nv4%20Pn44vr45)
- [BLS, Consumer Price Index (CPI-U)](https://data.bls.gov/timeseries/CUUR0000SA0)
- [Frontier Group Holdings, Form 10-K 2021](https://www.sec.gov/Archives/edgar/data/1670076/000167007622000016/fron-20211231.htm)
- [Frontier Group Holdings, Form 10-K 2024](https://www.sec.gov/Archives/edgar/data/1670076/000167007625000041/fron-20241231.htm)
- [Spirit, Form 8-K, March 16, 2026, Exhibit 99.1 (business plan)](https://www.sec.gov/Archives/edgar/data/1498710/000095010326003790/dp243147_ex9901.htm)
- [BTS, Form 41, Schedule P-12(a) (fuel)](https://www.transtats.bts.gov/DL_SelectFields.aspx?gnoyr_VQ=FMH&QO_fu146_anzr=Nv4%20Pn44vr45)
- [BTS, T-100 Segment (all carriers)](https://www.transtats.bts.gov/DL_SelectFields.aspx?gnoyr_VQ=FMG&QO_fu146_anzr=Nv4%20Pn44vr45)
- [BTS, Form 41, Schedule P-1.2 (income statement)](https://www.transtats.bts.gov/DL_SelectFields.aspx?gnoyr_VQ=FMI&QO_fu146_anzr=Nv4%20Pn44vr45)
- [BTS, Form 41, Schedule P-6 (expenses)](https://www.transtats.bts.gov/DL_SelectFields.aspx?gnoyr_VQ=FME&QO_fu146_anzr=Nv4%20Pn44vr45)
- [Spirit, Form 8-K, July 28, 2022, Exhibit 99.2 (JetBlue deal)](https://www.sec.gov/Archives/edgar/data/1498710/000119312522204192/d368049dex992.htm)
- [JetBlue Airways, Form 10-K (2020 to 2025 results)](https://www.sec.gov/Archives/edgar/data/1158463/000115846326000007/)
- [JetBlue Airways, Form 10-K (2020 to 2025 results)](https://www.sec.gov/Archives/edgar/data/1158463/000115846323000002/)
- [JetBlue Airways, Form 10-K (2020 to 2025 results)](https://www.sec.gov/Archives/edgar/data/1158463/000115846324000006/)
- [JetBlue Airways, Form 10-K (2020 to 2025 results)](https://www.sec.gov/Archives/edgar/data/1158463/000115846325000005/)
- [US DOT, Consumer Airfare Report, Table 1](https://data.transportation.gov/Aviation/Consumer-Airfare-Report-Table-1-Top-1-000-Contiguo/4f3n-jbg2)

## Corrections

None so far. Found an error? Open an issue with the line and the source.

# #001 · How much of a $400 airline ticket does the airline keep?

**Video:** https://youtu.be/yJrcfD89yBc

## The answer

On an example $400 nonstop domestic round trip, the 7 major U.S. publicly traded airlines keep about **$12.24** as net profit, on average. That is **3.1%** of the price paid.

Measured against what the airlines took in (their revenue, which excludes taxes and airport fees), profit was 3.6% of every dollar. Per passenger boarding, they took in $255 and kept $9.09.

## The receipt

| Line | On the ticket |
|---|---|
| Federal taxes and fees | $47.56 |
| Airport fee (PFC) | $9.00 |
| **Airline fare (what the airline counts as revenue)** | **$343** |
| Pilots, flight attendants and other employees | $111 |
| Fuel | $63.67 |
| Landing fees and airport rent | $23.01 |
| Depreciation and aircraft rent | $20.42 |
| Aircraft maintenance | $18.80 |
| Regional airline partners | $15.82 |
| Other operating costs (not broken out) | $72.81 |
| Interest and other non-operating items | $2.57 |
| Income taxes | $3.27 |
| **Airline net profit** | **$12.24** |

## By airline (profit as a share of the example ticket)

| Delta | United | Southwest | Alaska | American | JetBlue | Frontier |
|---|---|---|---|---|---|---|
| 6.8% | 4.9% | 1.3% | 0.6% | 0.2% | -5.7% | -3.2% |

## Method

1. Federal taxes and the airport fee come out of the fare first, using the published rates: the 7.5% federal ticket tax, the $5.30 segment fee, the $5.60 TSA fee each way and the $4.50 maximum airport fee per boarding.
2. The rest (the airline fare) is split in the same proportions as the combined 2025 costs of Delta, United, American, Southwest, Alaska, JetBlue and Frontier, from their Form 10-K filings ($232.2 billion in combined revenue).
3. Per boarding: combined net profit divided by the 909.4 million passenger boardings reported to the Bureau of Transportation Statistics (T-100), including the regional airlines that fly for the group.

## What this number doesn't show

- The ticket is an example: a round number for a nonstop round trip. A connection adds fees, and real fares vary.
- The split uses the group average, not the costs of a specific route.
- Airline revenue includes cargo, loyalty programs and credit card deals, not only tickets.
- The average hides a wide spread between airlines (see the table above).
- Fees and taxes are 2026 rates; the airlines' books are from 2025, the last full year.
- A boarding counts every flight: a trip with a connection counts twice, and a nonstop round trip is two boardings. Per-boarding numbers are not per-ticket numbers.
- Shares and boardings include the group's international flights; the example ticket is domestic.
- Depreciation in the 10-K covers ground equipment and buildings, not only planes. Southwest does not report aircraft rent separately in its XBRL data; it stays in other costs.
- Left out of the group: Allegiant (its XBRL data does not split fuel or airport fees), Spirit (in bankruptcy), and Sun Country, Breeze and Avelo (missing the same lines or not publicly traded).

## Reproduce it

```
python calc.py
```

Standard library only, no network. It reads `data/` and writes `numbers.json`. The files in `data/` are extracts of the public sources below, with the source URL on every row.

## Sources

- [IRS Publication 510 (federal ticket tax and segment fee)](https://www.irs.gov/pub/irs-pdf/p510.pdf)
- [TSA, security fees](https://www.tsa.gov/for-industry/security-fees)
- [49 U.S.C. 40117 (Passenger Facility Charge)](https://www.law.cornell.edu/uscode/text/49/40117)
- [DELTA AIR LINES, INC., Form 10-K 2025 (SEC EDGAR)](https://www.sec.gov/Archives/edgar/data/27904/000002790426000013/)
- [United Airlines Holdings, Inc., Form 10-K 2025 (SEC EDGAR)](https://www.sec.gov/Archives/edgar/data/100517/000010051726000023/)
- [American Airlines Group Inc., Form 10-K 2025 (SEC EDGAR)](https://www.sec.gov/Archives/edgar/data/6201/000000620126000014/)
- [SOUTHWEST AIRLINES CO., Form 10-K 2025 (SEC EDGAR)](https://www.sec.gov/Archives/edgar/data/92380/000009238026000004/)
- [ALASKA AIR GROUP, INC., Form 10-K 2025 (SEC EDGAR)](https://www.sec.gov/Archives/edgar/data/766421/000076642126000010/)
- [JETBLUE AIRWAYS CORP, Form 10-K 2025 (SEC EDGAR)](https://www.sec.gov/Archives/edgar/data/1158463/000115846326000007/)
- [Frontier Group Holdings, Inc., Form 10-K 2025 (SEC EDGAR)](https://www.sec.gov/Archives/edgar/data/1670076/000167007626000020/)
- [BTS TranStats, T-100 Segment (All Carriers), 2025](https://www.transtats.bts.gov/DL_SelectFields.aspx?gnoyr_VQ=FMG&QO_fu146_anzr=Nv4%20Pn44vr45)

## Corrections

None so far. Found an error? Open an issue with the line and the source.

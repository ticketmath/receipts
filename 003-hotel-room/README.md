# #003 · Who makes money on a hotel room: the owner of the building, or the brand on the door?

**Video:** https://youtu.be/_b2vcJagr04

## The answer

Per night, the owner keeps far more. Host Hotels & Resorts, a big U.S. hotel owner, kept **$49.38 of net profit per room, per night** in 2025, counting every available night, sold or empty. Marriott's net profit, spread over every room in its system, came to **$4.09** per room per night; Hilton's, **$3.05**.

Per dollar on the books, Marriott and Hilton come out ahead: net profit was **9.4%** of total assets at Marriott and **8.7%** at Hilton, against **5.9%** at Host. The owner paid for the building ($491,603 per room on Host's books) and carries the risk; Marriott's own property comes to $1,630 per system room.

## One room, one night at Host (2025, per available room night)

| Line | Per night |
|---|---|
| Revenue (rooms, food and beverage, events, condominium sales) | $389 |
| Rooms expenses | $57.66 |
| Food and beverage expenses | $77.89 |
| Other departmental and support expenses | $93.29 |
| Other property-level expenses | $27.11 |
| Management fees paid to hotel operators | $16.67 |
| Depreciation and amortization | $50.59 |
| Corporate and other costs outside the hotels | $11.46 |
| Interest | $14.96 |
| Gains and other income (hotel sales, interest income), as a negative | -$12.60 |
| Income tax | $2.67 |
| **Net income** | **$49.38** |

Other ways to count it:

| | Per room, per night |
|---|---|
| Net income per night actually sold | $70.85 |
| Net income without the $143.0 million gain on selling hotels | $40.28 |
| Comparable hotels' EBITDA (before interest, depreciation and corporate costs) | $111 |
| Net income in 2024 | $45.07 |

Host in 2025: 79 hotels, 43,051 rooms on average, occupancy 69.7%, average daily rate $329.

## The brands (2025, whole system, worldwide)

| | Marriott | Hilton | Hyatt |
|---|---|---|---|
| Fees for the year | $5.4 billion | $3.5 billion | $1.2 billion |
| System rooms at year end | 1.8 million | 1.4 million | 372,763 |
| Fees per room, per night | $8.55 | $7.26 | $9.12 |
| **Net income per room, per night** | **$4.09** | **$3.05** | **-$0.40** |
| Net income for the year | $2.6 billion | $1.5 billion | -$52.0 million |
| **Net income / total assets** | **9.4%** | **8.7%** | -0.4% |
| Own property per system room | $1,630 | $866 | $8,751 |

## The owner's risk

- **Host's 2024 purchases** cost $1.0 million per room on average, far above the historical cost on its books ($491,603); 49.7% of that historical cost is already depreciated, in hotels 38 years old on average.
- **The Ritz-Carlton O'ahu (formerly Turtle Bay):** Marriott paid Host $45.0 million ($100,000 per room) tied to the switch to its brand.
- **Park Hotels & Resorts:** net income of $226.0 million in 2024, a net result of -$277.0 million in 2025, including a $318.0 million write-down on its hotels. In San Francisco, two hotels (2,945 rooms) went to a court-appointed receiver after Park stopped paying a $725.0 million loan; the buyer took on the loan.

## Method

1. **Host's nights:** available room nights = rooms revenue / RevPAR; nights sold = rooms revenue / average daily rate (effective basis, all hotels for the period Host owned them). `calc.py` checks that nights sold / available matches the published occupancy and that (revenue − condominium sales) / available nights matches the published Total RevPAR. Every income statement line is divided by available nights, and the lines add back up to revenue.
2. **Brands' nights:** average of system rooms at the start and end of 2025 × 365. The math uses fees (franchise, base and incentive management), not total revenue, because total revenue includes costs the hotels they run pay back to them ($19.2 billion at Marriott).
3. **Per dollar:** net income / total assets, both from the balance sheet at book value.

## What this number doesn't show

- It's one owner, Host, with mostly luxury and upscale hotels (average daily rate $329, against $186 across Marriott's comparable hotels and $160 across Hilton's), in a single year.
- The brands' figures cover every hotel in their systems, worldwide, from luxury to budget, and their fees include income that doesn't come from hotel nights (co-branded credit cards, residences, timeshares). The brands also own some hotels.
- Host's and Park's management fees are only what they pay hotel operators (4.3% of Host's revenue); franchise fees, loyalty programs and reservation systems sit inside other expense lines the 10-K doesn't separate.
- On the brands' balance sheets, goodwill from past acquisitions and other intangibles weigh far more than buildings; total assets are book values, not market values.
- Host's room count is the yearly average; its balance sheet is from the last day of the year, without the hotels sold during the year. Park's room list is from February 2026 and its balance sheet from December 2025, so Park's per-night figures (-$36.40 net, $84.63 hotel EBITDA) are approximate.
- Hyatt had a net loss in 2025, the year it bought the Playa resorts, sold the buildings and kept the contracts to run them. "The brand wins" here means Marriott and Hilton, not every brand.
- Privately held hotel owners don't publish financial statements and are not in this math.

## Reproduce it

```
python calc.py
```

Standard library only, no network. It reads `data/`, prints the consistency checks and writes `numbers.json`. `inputs_2025.csv` has every table line, XBRL fact and 10-K sentence used, with the source URL on each row; `park_hotels_2025.csv` lists the rooms of each Park consolidated hotel.

## Sources

- [Host Hotels & Resorts, Form 10-K 2025](https://www.sec.gov/Archives/edgar/data/1070750/000107075026000054/hst-20251231.htm)
- [Host Hotels & Resorts, Form 10-K 2025, XBRL (SEC EDGAR)](https://www.sec.gov/Archives/edgar/data/1070750/000107075026000054/hst-20251231_htm.xml)
- [Park Hotels & Resorts, Form 10-K 2025](https://www.sec.gov/Archives/edgar/data/1617406/000161740626000006/pk-20251231.htm)
- [Park Hotels & Resorts, Form 10-K 2025, XBRL (SEC EDGAR)](https://www.sec.gov/Archives/edgar/data/1617406/000161740626000006/pk-20251231_htm.xml)
- [Marriott International, Form 10-K 2025](https://www.sec.gov/Archives/edgar/data/1048286/000104828626000007/mar-20251231.htm)
- [Marriott International, Form 10-K 2024](https://www.sec.gov/Archives/edgar/data/1048286/000162828025004818/mar-20241231.htm)
- [Marriott International, Form 10-K 2025, XBRL (SEC EDGAR)](https://www.sec.gov/Archives/edgar/data/1048286/000104828626000007/mar-20251231_htm.xml)
- [Hilton Worldwide Holdings, Form 10-K 2025](https://www.sec.gov/Archives/edgar/data/1585689/000158568926000007/hlt-20251231.htm)
- [Hilton Worldwide Holdings, Form 10-K 2024](https://www.sec.gov/Archives/edgar/data/1585689/000158568925000008/hlt-20241231.htm)
- [Hilton Worldwide Holdings, Form 10-K 2025, XBRL (SEC EDGAR)](https://www.sec.gov/Archives/edgar/data/1585689/000158568926000007/hlt-20251231_htm.xml)
- [Hyatt Hotels, Form 10-K 2025](https://www.sec.gov/Archives/edgar/data/1468174/000146817426000007/h-20251231.htm)
- [Hyatt Hotels, Form 10-K 2024](https://www.sec.gov/Archives/edgar/data/1468174/000146817425000009/h-20241231.htm)
- [Hyatt Hotels, Form 10-K 2025, XBRL (SEC EDGAR)](https://www.sec.gov/Archives/edgar/data/1468174/000146817426000007/h-20251231_htm.xml)

## Corrections

None so far. Found an error? Open an issue with the line and the source.

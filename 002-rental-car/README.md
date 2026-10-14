# #002 · How many rental days a month does a rental car need just to cover what it loses?

**Video:** https://youtu.be/L0zXVfDKga4

## The answer

A Hertz car in the Americas needs the revenue from about **5.5 rental days a month** just to cover what it loses in that month: a fleet cost of **$310** per car per month, against **$56.49** of revenue per rental day (2025). In 2024, the year of the EV write-downs, it took 9.9 days ($587 a month, $59.17 a day).

And the idea that the real money is in selling the used cars? In 2025, the cash from car sales was 95.1% of Hertz's revenue and 89.3% of Avis Budget's. But that cash mostly gives back what the cars cost: after the costs of selling and other charges, both companies lost money on those sales.

## The math per car (Hertz, Americas, 2025)

| Line | Value |
|---|---|
| Fleet cost per car per month (depreciation, rents for leased cars, result of selling the cars) | $310 |
| Revenue per rental day | $56.49 |
| **Rental days a month to cover the fleet cost** | **5.5** |
| Days a month a fleet car is out on rent, on average | 23.6 |
| Revenue per fleet car per month | $1,332 |
| Share of that revenue that goes to fleet cost | 23.3% |
| Average fleet | 422,346 cars |
| Months the cars sold in 2025 spent in the fleet | 18 |

## Selling the cars (2025, whole companies)

| | Hertz | Avis Budget |
|---|---|---|
| Revenue | $8.5 billion | $11.7 billion |
| Cash from selling fleet cars | $8.1 billion | $10.4 billion |
| Car sales as a share of revenue | 95.1% | 89.3% |
| Result of the sales before selling costs and charges | $182.0 million | $152.0 million |
| Costs of selling (Hertz) / fleet disposal charges (Avis Budget) | $246.0 million | $390.0 million |
| **Gain (loss) on selling the cars** | **-$64.0 million** | **-$238.0 million** |
| Net income (loss) for the year | -$747.0 million | -$889.0 million |

At Hertz, 97.7% of the sale cash only gave back the cars' book value (approximate: the cash is what was received during the year).

## Method

1. **Per car:** Hertz publishes operating data for its Americas RAC segment. The fleet cost per car per month (Depreciation Per Unit Per Month) is divided by revenue per rental day (Total RPD). `calc.py` first rebuilds both published figures from the lines of the same table (fleet cost / average vehicles / 12; revenue / transaction days) and checks that they match.
2. **Same base on both sides:** everything "per car" uses the average fleet (Average Vehicles), including revenue per car and rented days per car.
3. **Car sales:** cash from selling cars and the gain or loss on those sales come from each company's XBRL data. The notes say what that line includes: costs of selling the cars at Hertz ($246.0 million); charges for disposing of part of the Americas fleet at Avis Budget ($390.0 million).

## What this number doesn't show

- The per-car math is Hertz in the Americas, where the company publishes segment operating data. Avis Budget does not publish it in the same format.
- The fleet cost per car is not just depreciation: it includes rents for cars Hertz doesn't own and the result of selling the cars, with the costs of selling. Revenue per rental day is the average of all rentals, from one day to a month.
- The per-car math uses the average fleet, which includes cars held for sale. Among rentable cars alone, utilization was 82%.
- Car sales and revenue are for the whole company, in every country; the per-car math is the Americas only.
- Selling almost as much as you rent is not profit: the sale cash gives back part of what the car cost. Before the costs of selling and the charges, both companies had a gain on the sales ($182.0 million at Hertz, $152.0 million at Avis Budget); after them, a loss.
- In 2024, Hertz wrote down $923.0 million of fleet values on a separate line, outside the fleet cost per car. Since then, depreciation is calculated on the lower values, which makes the 2025 cost per car smaller than it would be without the write-down; the 10-K doesn't say by how much.
- Not every car is a bet on resale prices: 11% of Hertz's Americas fleet at the end of 2025 had a buyback or guaranteed depreciation from the carmaker.
- Enterprise, National and Alamo are privately held and don't publish financial statements; Sixt is German and reports under a different standard. None of them is in the math.
- The numbers are for 2025, with 2024 for comparison. Hertz gives four reasons for the lower cost per car: cheaper new cars and stronger resale, a gain on sales in 2025 against a loss in 2024, a smaller fleet, and the EV write-downs in the first half of 2024. One year doesn't show a trend.

## Reproduce it

```
python calc.py
```

Standard library only, no network. It reads `data/`, prints the consistency checks and writes `numbers.json`. The files in `data/` are extracts of the public sources below, with the source URL on every row; `notes_10k_2025.csv` also quotes the sentence each number was read from.

## Sources

- [Hertz Global Holdings, Form 10-K 2025 (Americas RAC operating data)](https://www.sec.gov/Archives/edgar/data/1657853/000165785326000008/htz-20251231.htm)
- [Hertz Global Holdings, Form 10-K 2025, XBRL (SEC EDGAR)](https://www.sec.gov/Archives/edgar/data/1657853/000165785326000008/htz-20251231_htm.xml)
- [Avis Budget Group, Form 10-K 2025, XBRL (SEC EDGAR)](https://www.sec.gov/Archives/edgar/data/723612/000072361226000012/car-20251231_htm.xml)
- [Avis Budget Group, Form 10-K 2025](https://www.sec.gov/Archives/edgar/data/723612/000072361226000012/car-20251231.htm)

## Corrections

None so far. Found an error? Open an issue with the line and the source.

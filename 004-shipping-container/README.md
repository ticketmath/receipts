# #004 · What does it cost to get goods from China to your door?

**Video:** coming soon

## The answer

In 2025, getting goods from China to a US port by container ship cost **7.7% of their value** (freight, insurance and other charges, as importers declared them). The tariff on goods from China came to **30.6%**, **4 times** the ocean's share.

On a box of goods from China worth $100 at customs, the ocean took **$7.65** and the tariff **$30.60**.

## The receipt, leg by leg (2025, per dollar of value at customs)

| Leg | China | Vietnam | All countries |
|---|---|---|---|
| Ocean (container ships) | 7.7% | 5.0% | 4.9% |
| Tariff | 30.6% | 8.7% | 7.6% |
| Tariff / ocean | 4x | 1.7x | 1.6x |
| US imports for the year | $308.7 billion | $193.9 billion | $3.4 trillion |

Per pound of containerized goods from China: the ocean cost **$0.13**, for goods worth **$1.68**.

After the port:

| Leg | Figure | Per dollar of goods |
|---|---|---|
| Train inland (Union Pacific, average revenue per intermodal load) | $1,380 per container | 1.5% |
| Last trip to the door (UPS, average revenue per US package) | $13.21 per package | - |
| Last trip to the door (Amazon shipping costs / store sales, rough) | $102.7 billion for the year | 17.5% of store sales |

## Checks

- **One container:** goods in an average loaded 40-foot container entering Los Angeles were worth $92,129 ($46,064 per TEU, 2 TEU per container). Applied to that box, the declared ocean charges land in the same range as Hapag-Lloyd's average freight rate, $1,376 per TEU across all routes.
- **Tariffs:** the Treasury collected $264.0 billion in customs duties in 2025, close to the duty Census calculated across all countries ($259.4 billion). Collections rose through the year: $7.3 billion in January, $27.9 billion in December.
- **Thesis threshold:** the ocean leg stays below 10% of the value even for China.

## Method

1. **Ocean:** Census import data for containerized goods. `CNT_CHA_YR` (charges: freight, insurance and other costs to the first US port, tariff excluded) / `CNT_VAL_YR` (value). Per pound uses `CNT_WGT_YR` (kg) / 0.45359237.
2. **Tariff:** `CAL_DUT_YR` (calculated duty) / `CON_VAL_YR` (imports for consumption).
3. **Container value:** Port of Los Angeles containerized value (Census, by port) / loaded import TEU (port statistics) x 2.
4. **Land:** Union Pacific and UPS published averages from their 2025 annual reports; Amazon shipping costs / North America + International net sales (AWS excluded).

## What this number doesn't show

- Census charges are what importers declare for freight, insurance and other costs to the first US port. They are not one carrier's price list, and they mix every route and contract.
- The 2025 tariffs include those imposed under the emergency economic powers law (IEEPA), which the Supreme Court struck down in February 2026. Part of what was paid may be refunded, and the tariffs in place in 2026 are different. The tariff line is a snapshot of 2025.
- Freight and tariff are measured against the value at customs, not the shelf price, which is higher. On the shelf, each line is a smaller share.
- Union Pacific's average mixes containers coming off ships with trailers and containers carrying freight within the US; its annual report doesn't separate them.
- Amazon's store sales include advertising, memberships and fees from outside sellers, and its shipping costs include those sellers' packages. Treat that share as an order of magnitude.
- The container value is an average of everything that entered Los Angeles in 2025, from every country. Containers of furniture and of electronics are worth very different amounts.

## Reproduce it

```
python calc.py
```

Standard library only, no network. It reads `data/inputs_2025.csv` (every Census field, Treasury month, 10-K table line or sentence, constant and assumption used, with the source URL on each row), prints the consistency checks and writes `numbers.json`.

## Sources

- [US Census Bureau, international trade API, imports 2025 (China)](https://api.census.gov/data/timeseries/intltrade/imports/enduse?get=CTY_CODE,CTY_NAME,GEN_VAL_YR,CON_VAL_YR,CAL_DUT_YR,DUT_VAL_YR,VES_VAL_YR,VES_CHA_YR,CNT_VAL_YR,CNT_CHA_YR,CNT_WGT_YR&time=2025-12&CTY_CODE=5700)
- [US Census Bureau, international trade API, imports 2025 (Vietnam)](https://api.census.gov/data/timeseries/intltrade/imports/enduse?get=CTY_CODE,CTY_NAME,GEN_VAL_YR,CON_VAL_YR,CAL_DUT_YR,DUT_VAL_YR,VES_VAL_YR,VES_CHA_YR,CNT_VAL_YR,CNT_CHA_YR,CNT_WGT_YR&time=2025-12&CTY_CODE=5520)
- [US Census Bureau, international trade API, imports 2025 (All Countries)](https://api.census.gov/data/timeseries/intltrade/imports/hs?get=GEN_VAL_YR,CON_VAL_YR,CAL_DUT_YR,DUT_VAL_YR,VES_VAL_YR,VES_CHA_YR,CNT_VAL_YR,CNT_CHA_YR,CNT_WGT_YR&time=2025-12)
- [NIST, definition of the pound (kg)](https://www.nist.gov/pml/owm/si-units-mass)
- [US Treasury, Monthly Treasury Statement, table 4 (customs duties), 2025](https://fiscaldata.treasury.gov/datasets/monthly-treasury-statement/receipts-of-the-u-s-government)
- [US Census Bureau, international trade API, imports 2025 by port (Los Angeles)](https://api.census.gov/data/timeseries/intltrade/imports/porths?get=PORT,PORT_NAME,CNT_VAL_YR,CNT_WGT_YR,VES_VAL_YR,GEN_VAL_YR&time=2025-12&PORT=2704)
- [Port of Los Angeles, 2025 container statistics (loaded imports, TEU)](https://www.portoflosangeles.org/business/statistics/container-statistics/historical-teu-statistics-2025)
- [Hapag-Lloyd, average freight rate FY 2025 (USD/TEU), AGM 2026 presentation](https://www.hapag-lloyd.com/content/dam/website/downloads/ir/HLAG_Charts_CEO_Speech_AGM2026.pdf)
- [Union Pacific, Form 10-K 2025](https://www.sec.gov/Archives/edgar/data/100885/000010088526000037/unp-20251231.htm)
- [UPS, Form 10-K 2025](https://www.sec.gov/Archives/edgar/data/1090727/000162828026008432/ups-20251231.htm)
- [Amazon.com, Form 10-K 2025](https://www.sec.gov/Archives/edgar/data/1018724/000101872426000004/amzn-20251231.htm)

## Corrections

None so far. Found an error? Open an issue with the line and the source.

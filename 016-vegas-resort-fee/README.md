# #016 · The Las Vegas resort fee: how much of a night on the Strip is the room, and how much is the fee?

**Video:** coming soon

## The answer

On the Tuesday before Thanksgiving (November 24, 2026), the Flamingo's cheapest room cost $5.60 a night. The resort fee on the line below it was $49.95. **Before tax, the fee was 89.9% of the night**: 8.9 times the room.

The fee is flat and the room rate is what moves, so the cheaper the room, the bigger the fee's share. The same Excalibur room, with the same $45.00 fee: on that Tuesday the room was $6.60 and the fee was 87.2% of the night; on the weekend of November 20 to 22 the room was $134 and the fee was 25.1%.

The promotion only reached the room: the Cyber Monday deal took $5.83 off an $11.43 room (51.0% of the room rate), but only 9.5% off the whole night, which still came to $62.98.

## How we counted

- **Prices**: each hotel company's own booking site, read on November 17, 2026: 2 guests, the lowest rate of each room type, before tax. MGM Resorts for the Excalibur, the Luxor and the Bellagio; Caesars for the Flamingo. Since the federal rule of May 12, 2025, the sites show the room rate, the resort fee and the total separately. The booking engines run in the browser, so the prices were read on screen and are in `data/published_figures.csv` as shown.
- **Fee's share of the night** = resort fee / (room rate + resort fee), before tax.
- **Tax**: Clark County's room tax on the Strip, 13.38%, charged on the room rate and on the resort fee. The Flamingo's own breakdown confirms it: its "Taxes" line is 13.38% of room rate + resort fee.

## Four receipts for the same Tuesday

| November 24, 2026 | Room rate | Resort fee | Fee's share of the night | Fee / room | Night with tax |
|---|---|---|---|---|---|
| Flamingo (Caesars) | $5.60 | $49.95 | 89.9% | 8.9x | $62.98 |
| Excalibur (MGM) | $6.60 | $45.00 | 87.2% | 6.8x | $58.50 |
| Luxor (MGM) | $8.40 | $45.00 | 84.3% | 5.4x | $60.54 |
| Bellagio (MGM) | $155 | $55.00 | 26.2% | 0.4x | $238 |
| Excalibur, November 20 to 22 | $134 | $45.00 | 25.1% | 0.3x | $203 |

The Flamingo's next room up, the Fab Room with 2 Queens, was $10.50 that night, with the same fee: $68.54 with tax.

## The Flamingo receipt, line by line

| Tuesday, November 24, 2026 | |
|---|---|
| Room rate, after the promotions (before them: $11.43) | $5.60 |
| Taxes (13.38% of room rate + resort fee) | $7.43 |
| Resort fee | $49.95 |
| **Total** | **$62.98** |

The resort fee plus the tax charged on it come to 89.9% of the total, tax included.

At the Excalibur, the tax on the fee alone is $6.02, about the price of the room. Add MGM's self-parking ($20.00 for 24 hours) and the Tuesday bill comes to $78.50, of which the room is 8.4%.

## Then and now

- **May 2010**: the Las Vegas Sun reported a guest at the Excalibur whose $39.00 room came with a $4.50 resort fee: 10.3% of the night. In 2026 the fee at the same hotel is 10 times bigger.
- **2010** is the year most of MGM's Strip resorts adopted the fee: its resort fee revenue went from $15.0 million in 2009 to $70.0 million in 2010 (4.7 times), per its 10-K.
- **The FTC** wrote in its 2025 rule that a resort fee "can exceed 20% of the per-night cost, especially at lower cost hotels".

## The whole Strip, by month

A $45.00 fee on top of the Strip's average daily room rate (LVCVA) is 20.0% of it in May 2026 ($225, the priciest month of the year through September) and 29.4% in August ($153, the cheapest). January to September: $195.

Rooms did not get cheaper overall: the Strip's average room rate went from $180 in fiscal 2019 to $251 in fiscal 2025 (39.1%, Gaming Abstract). The fee weighs most on the cheap nights, not on the average one.

For scale: a bottle of water from the minibar at Aria was $26.00 in June 2025, 3.5 times the $7.45 the same water cost at the Starbucks in the complex.

## What this number doesn't show

- The prices come from one search, on November 17, 2026, for specific nights; they change every day. The fee is fixed per room per night; the room rate is what moves.
- The LVCVA's average daily room rate is what hotels report and, as the Las Vegas Review-Journal describes it, leaves out resort fees, taxes and parking; the LVCVA doesn't print the definition in the report.
- The room tax is charged on the resort fee, according to the LVCVA's chief financial officer (Las Vegas Sun, 2016), and the Flamingo's breakdown matches it to the cent.
- Guests with top loyalty status (such as MGM Rewards Gold or Caesars Diamond) or a comped room may have the fee waived, and MGM's all-inclusive packages at the Luxor and the Excalibur (March 2026) fold it into one price. These numbers are for the public rate.
- The idea that room rates fell since 2019 doesn't hold: the Strip's average rate rose 39.1% from fiscal 2019 to fiscal 2025. What matters is the gap between cheap and expensive nights.

## Reproduce it

```
python calc.py
```

Standard library only, no network. It reads `data/published_figures.csv`: every price, fee, rate and figure used, as published, with a description, the source and its URL.

It prints the consistency checks (room rate + resort fee equals the total each MGM site shows; the Flamingo's taxes are 13.38% of room rate + resort fee and its three lines add up to its total, for both rooms; the LVCVA's January to September rate sits between its cheapest and priciest month; the tax on the Excalibur fee is in the same range as the room; the Excalibur fee's share is above the 20% the FTC cited) and writes `numbers.json`.

## Sources

**Prices (read November 17, 2026)**

- [MGM Resorts booking site, Excalibur, night of November 24, 2026](https://excalibur.mgmresorts.com/book-room/room/?guests=2&region=las-vegas&resort=f8d6a944-7816-412f-a39a-9a63aad26833&checkIn=2026-11-24&checkOut=2026-11-25)
- [MGM Resorts booking site, Excalibur, nights of November 20 to 22, 2026](https://excalibur.mgmresorts.com/book-room/room/?guests=2&region=las-vegas&resort=f8d6a944-7816-412f-a39a-9a63aad26833&checkIn=2026-11-20&checkOut=2026-11-22)
- [MGM Resorts booking site, Luxor, night of November 24, 2026](https://luxor.mgmresorts.com/book-room/room/?guests=2&region=las-vegas&resort=607c07e7-3e31-4e4c-a4e1-f55dca66fea2&checkIn=2026-11-24&checkOut=2026-11-25)
- [MGM Resorts booking site, Bellagio, night of November 24, 2026](https://bellagio.mgmresorts.com/book-room/room/?guests=2&region=las-vegas&resort=44e610ab-c209-4232-8bb4-51f7b9b13a75&checkIn=2026-11-24&checkOut=2026-11-25)
- [Caesars, Flamingo Las Vegas](https://www.caesars.com/flamingo-las-vegas) (booking flow for November 24, 2026, Best Available Rate)
- [MGM Resorts, Las Vegas parking](https://www.mgmresorts.com/en/things-to-do/parking.html)

**What the fee covers**

- [MGM Resorts, terms and conditions (resort fee)](https://www.mgmresorts.com/en/terms-and-conditions.html)
- [Caesars, Flamingo Las Vegas FAQ](https://www.caesars.com/flamingo-las-vegas/faqs)
- [Wynn Las Vegas, terms and conditions](https://www.wynnlasvegas.com/terms-and-conditions/686591)
- [Las Vegas Review-Journal, the $26 minibar water at Aria (June 25, 2025, republished by The Spokesman-Review)](https://www.spokesman.com/stories/2025/jun/25/thats-criminal-26-minibar-water-bottle-at-las-vega/)

**Tax and the Strip**

- [Clark County, transient lodging tax rates](https://www.clarkcountynv.gov/business/doing_business_with_clark_county/transient-lodging-tax-rate-increases)
- [LVCVA, 2026 Las Vegas monthly visitor statistics](https://assets.simpleviewcms.com/simpleview/raw/upload/v1/clients/lasvegas/2026_Las_Vegas_Laughlin_and_Mesquite_NV_Monthly_Visitor_Statistics_63263304-bff3-4710-bc2a-8d659b688d49.xlsx)
- [Nevada Gaming Control Board, Gaming Abstract FY2019](https://www.gaming.nv.gov/uploadedFiles/gamingnvgov/content/about/abstract/2019-abstract.pdf)
- [Nevada Gaming Control Board, Gaming Abstract FY2025](https://www.gaming.nv.gov/siteassets/content/about/abstract/abstract-fy-2025.pdf)

**History**

- [Las Vegas Sun, resort fees catch guests by surprise (May 8, 2010)](https://lasvegassun.com/news/2010/may/08/resort-fees-catch-guests-surprise/)
- [MGM Resorts, Form 10-K 2011 (resort fee revenue in 2009 and 2010)](https://www.sec.gov/Archives/edgar/data/789570/000104746912001824/a2207412z10-k.htm)
- [Las Vegas Sun, Caesars hotels will start charging resort fees (February 21, 2013), with the July 21, 2011 showgirl parade](https://lasvegassun.com/news/2013/feb/21/caesars-hotels-will-start-charging-resort-fees/)
- [Caesars Entertainment, prepared remarks, Q2 2013 (July 29, 2013): "minimal impact on occupancy"](https://www.sec.gov/Archives/edgar/data/858339/000085833913000041/ex992preparedremarks-czr2q.htm)
- [Caesars Entertainment, Form 10-K 2025 (resort fees in hotel revenue)](https://www.sec.gov/Archives/edgar/data/1590895/000159089526000011/czr-20251231.htm)
- [FOX5 Las Vegas, MGM launches an all-inclusive package at the Luxor and the Excalibur (March 25, 2026)](https://www.fox5vegas.com/2026/03/25/mgm-resorts-launches-all-inclusive-package-luxor-excalibur/)

**Regulators and booking sites**

- [FTC, warning to hotel operators about price quotes that exclude resort fees (November 28, 2012)](https://www.ftc.gov/news-events/press-releases/2012/11/ftc-warns-hotel-operators-price-quotes-exclude-resort-fees-other)
- [FTC, Economic Analysis of Hotel Resort Fees (2017)](https://www.ftc.gov/system/files/documents/reports/economic-analysis-hotel-resort-fees/p115503_hotel_resort_fees_economic_issues_paper.pdf)
- [FTC, Trade Regulation Rule on Unfair or Deceptive Fees (Federal Register, January 10, 2025)](https://www.federalregister.gov/documents/2025/01/10/2024-30293/trade-regulation-rule-on-unfair-or-deceptive-fees)
- [Skift, Expedia tells hotels adding resort fees will lower their listings (November 14, 2019)](https://skift.com/2019/11/14/expedia-tells-hotels-adding-resort-fees-will-lower-your-listings-on-its-pages/)

## Corrections

None so far. Found an error? Open an issue with the line and the source.

## License

Code (`calc.py`): [MIT](../LICENSE). Data, text and tables: [CC BY 4.0](../LICENSE-DATA.md); the underlying public records keep their own terms.

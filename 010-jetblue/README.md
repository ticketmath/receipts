# #010 · JetBlue: of every passenger it flew from July to September 2026, how much came in, how much went out, and to whom?

**Video:** https://youtu.be/9X-9esbQRwE

## The answer

From July to September 2026, JetBlue's average ticket cost $245, **$39.44 more** than a year earlier. It still lost **$24.23 per passenger**. A year earlier, with fuel much cheaper, it lost $13.78.

Three bills explain most of it. Fuel took $29.91 more per passenger than a year earlier, most of the fare increase, but it isn't the oldest bill: from 2019 to 2025, before this year's spike, fuel rose $9.07 per passenger and payroll rose **$33.49**. And interest went from $1.85 per passenger in 2019 to $14.05 this summer: running the planes lost $13.58 per passenger, and interest dug a second hole about the same size.

## How we counted

- **Per passenger** = the income statement figure divided by JetBlue's revenue passengers in the same period (10.6 million from July to September 2026). A passenger here is one flight segment (see the caveats).
- **The quarter** comes from JetBlue's 10-Q for the third quarter of 2026, which also carries the third quarter of 2025 and both nine-month periods. **2019 and 2025** come from the 10-Ks. `calc.py` checks that the expense lines add up to the published totals in every period, and that passenger revenue divided by passengers gives the average fare JetBlue publishes.
- **Net loss** is the filing's bottom line: after interest and after a tax credit. Before tax, the loss per passenger went from -$18.88 to -$25.45.
- **Inflation** is the BLS CPI-U (all items, U.S. city average), the average of the months published in each year. The BLS didn't collect October 2025, so 2025 averages 11 months.
- **The gallon by airline** is total cost divided by total gallons in Form 41 (BTS, Schedule P-12(a)), which includes taxes and fueling fees and, when this count was closed, went only through June 2026.
- **Market value** is the published stock price times the shares on the cover of the 10-Q, even on other dates.

## One passenger, July to September 2026

| Per passenger | Q3 2026 | Q3 2025 | Change |
|---|---|---|---|
| **In: revenue, counting the fare and the bags** | **$265** | **$224** | $41.43 |
| Payroll (salaries, wages and benefits) | $89.19 | $83.33 | $5.86 |
| Fuel | $81.83 | $51.92 | $29.91 |
| Other operating expenses | $38.56 | $33.91 | $4.65 |
| Maintenance | $19.23 | $20.23 | -$1.00 |
| Landing fees and other rents | $18.76 | $17.24 | $1.52 |
| Depreciation | $17.54 | $16.67 | $0.87 |
| Sales and marketing | $8.67 | $7.51 | $1.16 |
| Special items (one-time) | $3.11 | $0.48 | $2.63 |
| Aircraft rent | $1.79 | $2.02 | -$0.23 |
| **Total operating expenses** | **$279** | **$233** | $45.37 |
| **Running the airline, before interest** | **-$13.58** | **-$9.63** | |
| Interest expense | $14.05 | $14.06 | |
| Result before income taxes, after interest income and other items | -$25.45 | -$18.88 | |
| **Net loss, after the tax credit** | **-$24.23** | **-$13.78** | $10.45 worse |

Without payroll and fuel, the other expense lines came to $108. The whole quarter: net loss of $257.0 million, interest expense of $149.0 million, interest income of $17.0 million, an operating margin of -5.1%, and planes 83.6% full (85.1% a year earlier).

**The loss per passenger grew 1.8 times in a year, but mostly on the last lines.** The net loss rose $114.0 million, from $143.0 million to $257.0 million, and 59.6% of that rise was a smaller tax credit ($53.0 million to $13.0 million) and more special items ($5.0 million to $33.0 million). Before tax, the loss per passenger rose 34.8%. Without special items, the operating result went from -$95.0 million to -$111.0 million.

| Nine months, per passenger | 2026 | 2025 |
|---|---|---|
| Passengers | 30.4 million | 29.6 million |
| Revenue | $255 | $230 |
| Fuel | $77.33 | $52.47 |
| Payroll | $89.33 | $87.08 |
| Other operating expenses | $37.94 | $34.44 |
| Maintenance | $19.79 | $20.19 |
| Landing fees and other rents | $18.12 | $17.19 |
| Depreciation | $18.02 | $17.29 |
| Sales and marketing | $8.29 | $7.60 |
| Special items | $1.08 | $0.98 |
| Aircraft rent | $1.61 | $2.03 |
| Total operating expenses | $272 | $239 |
| Running the airline, before interest | -$16.73 | -$9.05 |
| Interest expense | $14.47 | $14.89 |
| Result before income taxes | -$28.83 | -$18.94 |

Net loss in the nine months of 2026: $823.0 million, or $27.06 per passenger.

| 2026, quarter by quarter | Q1 | Q2 | Q3 |
|---|---|---|---|
| Average fare | $219 | $237 | $245 |
| Change from the same quarter of 2025 | $6.91 | $18.86 | $39.44 |
| Net loss | $319.0 million | $247.0 million | $257.0 million |
| Net loss per passenger | $34.19 | $23.57 | $24.23 |

The average fare for the nine months of 2026 was $235. In the third quarter, it was 19.2% higher than a year earlier.

## Fuel: the loudest bill

JetBlue paid $2.64 a gallon in February 2026 and $4.71 in April (Form 41). Its January guidance assumed $2.17 to $2.37 for the year and an adjusted operating margin of "breakeven or better". By October, it expected $3.95 for the year ($4.64 in the fourth quarter) and a margin of -4.5% to -6.5%. In the third quarter it paid $3.91, 57% more than a year earlier.

On September 30, 2026, the 10-Q says JetBlue had no fuel hedging contracts; a 10% higher gallon would add about $376.0 million of fuel expense over 12 months.

JetBlue says it recaptured 87% of the higher fuel costs in the third quarter. That's its own measure, and it's why fuel alone can't explain the loss: the fare rose by more than the fuel did.

## 2019 against 2025

| Per passenger | 2019 | 2025 | Change |
|---|---|---|---|
| Revenue | $189 | $230 | $40.94 |
| Payroll | $54.30 | $87.78 | **$33.49** |
| Fuel | $43.23 | $52.29 | $9.07 |
| Other operating expenses | $25.88 | $34.93 | $9.05 |
| Maintenance | $14.49 | $20.11 | $5.62 |
| Landing fees and other rents | $11.09 | $16.73 | $5.63 |
| Depreciation | $12.29 | $17.49 | $5.20 |
| Sales and marketing | $6.79 | $7.75 | $0.97 |
| Special items | $0.33 | $0.76 | $0.44 |
| Aircraft rent | $2.32 | $1.88 | -$0.44 |
| Total operating expenses | $171 | $240 | $69.02 |
| Interest | $1.85 | $14.95 | $13.10 (8.1 times) |
| **Net result** | **$13.32** | **-$15.30** | |

| The whole company | 2019 | 2025 | Change |
|---|---|---|---|
| Passengers | 42.7 million | 39.3 million | |
| Average fare | $182 | $212 | 16.3% |
| Average flight, in miles | 1,140 | 1,301 | 14.1% |
| Load factor | 84% | 82.4% | |
| Employees (full-time equivalents) | 18,535 | 19,259 | |
| Payroll per employee | $125,169 | $179,293 | 43.2% |
| Passengers per employee | 2,305 | 2,042 | -11.4% |
| Interest expense | $79.0 million | $588.0 million | |
| Net income | $569.0 million | -$602.0 million | |

Prices across the U.S. rose 25.9% in those years, more than the average fare. In 2025, JetBlue lost $15.30 per passenger.

**The pilots' contract** of March 1, 2023 raised pay 14% at once, 3% in August 2023 and 9% in August 2024: 28.0% compounded (10-K). It's only part of the payroll rise.

## The lenders

JetBlue lost money in all 6 years from 2020 to 2025. From 2020 to September 30, 2026, the losses add up to $4.4 billion. Debt and finance leases went from $2.3 billion at the end of 2019 to $8.4 billion on September 30, 2026 (3.6 times), including $2.0 billion of planes sold and leased back, booked as debt, and $535.0 million of pandemic payroll support loans from the government.

**The lifetime scoreboard.** Retained earnings, every dollar of profit JetBlue kept minus every loss, stood at $4.3 billion at the end of 2019, $717.0 million at the end of 2025 and $151.0 million on June 30, 2026. On September 30, 2026, they were -$106.0 million, or $106.0 million below zero. It's a running score, not cash. JetBlue pays no dividends (10-K), so only results move it, and `calc.py` checks that the losses close the fall.

**The TrueBlue loan.** In 2024, JetBlue raised $2.8 billion from notes due 2031 at 9.9% and a term loan due 2029, both with a first lien on "certain collateral in connection with" its TrueBlue program (8-K of September 3, 2024). On September 30, 2026, $2.7 billion was outstanding: $2.0 billion of notes and $742.0 million of the loan. The notes alone cost $197.5 million a year, about $5.02 per 2025 passenger.

**JetForward**, JetBlue's plan, targets $850.0 million to $950.0 million more a year in operating profit by 2027, before interest; it delivered $305.0 million in 2025. JetBlue expects about $590.0 million of interest in 2026, 62.1% of the top of that target.

## The other airlines, the same quarter

| Q3 2026 | JetBlue | Delta | United | American | Southwest | Frontier |
|---|---|---|---|---|---|---|
| Net result | -$257.0 million | $756.0 million | $1.0 billion | -$269.0 million | $270.0 million | -$104.0 million |
| Net result per passenger | -$24.23 | no count | $20.78 | no count | $6.23 | -$10.61 |
| Interest per passenger | $14.05 | no count | $7.25 | no count | $1.62 | $1.22 |
| **Of every $100 of revenue** | | | | | | |
| Fuel | $30.87 | $24.74 | $27.09 | $28.37 | $25.55 | $31.37 |
| Interest | $5.30 | $0.83 | $2.01 | $2.66 | $0.83 | $0.89 |
| Operating result | -$5.12 | $8.27 | $8.09 | $0.70 | $4.50 | -$7.97 |
| Net result | -$9.14 | $4.30 | $5.76 | -$1.65 | $3.21 | -$7.68 |
| **Fuel per gallon, Q2 2026** | $4.23 | $3.91 | $4.04 | $3.88 | $3.80 | $3.85 |

Frontier lost $10.61 per passenger with little interest: a light interest bill doesn't make an airline profitable either.

**Points are worth a lot at full scale.** American Express paid Delta $2.3 billion from July to September 2026, 81.8% of all of JetBlue's revenue in that quarter. That's revenue, not profit, and only part of what Delta takes in. JetBlue's loyalty revenue was $330.0 million ($31.11 per passenger, up 20%), counting flights paid with points; the "loyalty and related" line alone, mainly the non-flight part of point sales plus lounge access, was $148.0 million ($13.95 per passenger).

## The points and the breathing room

**The points.** On JetBlue's books, unused TrueBlue points are travel it still owes customers: $1.3 billion on September 30, 2026. United (2002), Delta (2005) and American (2011) kept their miles going through Chapter 11, and United, Delta and American had all borrowed against their programs during the pandemic; JetBlue wasn't the first. Spirit stopped flying in 2026 and said its points no longer had value (The Points Guy). Nothing has changed for anyone's points today; in a bankruptcy, it would depend on the case. This is an explanation, not advice.

**The breathing room.** On September 30, 2026, JetBlue reported $2.2 billion of liquidity: $1.6 billion in cash and investments and an undrawn $600.0 million credit line ($2.5 billion of cash and investments at the end of 2025). In the nine months of 2026, operations used -$273.0 million and investments $624.0 million, so $99.7 million a month went out, before any new loans ($495.0 million) or debt repayments ($658.0 million). At that pace, that liquidity covers **22.1 months**.

Principal and interest due: $1.0 billion in 2027, $1.1 billion in 2028, $2.3 billion in 2029 and $11.1 billion in all. JetBlue says it has about $7.0 billion in unencumbered assets.

**What the market said** (press reports, each on its date). JetBlue's 2031 notes traded near $0.84 on the dollar around July 23, 2026 (View from the Wing), about $0.80 in September and $0.42 on October 22 (Fox Business, citing The Wall Street Journal). The stock closed at $2.65 on October 22 and hit an intraday low of $2.16 on October 26 (Bloomberg), which, on 377.4 million shares, is $815.1 million. It closed at $3.18 on November 3 (Yahoo Finance), up 47.2% from that low, or $1.2 billion. At the low, the TrueBlue-backed debt was 3.4 times the company's market value. Carl Icahn's stake went from 9.9% in February 2024 to 3.3% on August 20, 2026 (Schedule 13D).

The Wall Street Journal reported, through Fox Business, that creditors had hired advisers, citing anonymous sources; the adviser named didn't comment. View from the Wing reported a leaked recording of David Neeleman, JetBlue's founder and now the founder of its rival Breeze, citing an analyst's projection of a $1.3 billion loss in 2026; he's a competitor, and what he drew from it is his opinion.

## Spirit

In July 2022, JetBlue agreed to pay $3.8 billion for Spirit's shares, without the debt that would come along. That's 4.7 times what JetBlue's market value was at its October 2026 low. A federal judge blocked the deal in January 2024. JetBlue booked $652.0 million in costs tied to it ($28.0 million in 2022, $92.0 million in 2023, $532.0 million in 2024), had prepaid $403.0 million to Spirit's shareholders by the end of 2023, and paid Spirit a $69.0 million fee on ending it.

Spirit stopped flying on May 2, 2026.

| Domestic seats leaving Fort Lauderdale, July (T-100) | 2025 | 2026 |
|---|---|---|
| JetBlue | 19.4% | 34.8% |
| Spirit | 27.5% | 0% |
| All airlines, seats | 1.2 million | 1.3 million |

JetBlue's release says its capacity at Fort Lauderdale grew more than 65% in the third quarter, with revenue per seat mile up nearly 15%, and that its seat share there should reach about 37% in the fourth quarter, up 14 points. It also bought 22 LaGuardia slots previously operated by Spirit for $58.5 million.

## What this number doesn't show

- **A passenger is one flight segment**, so a connection counts twice. This is one quarter of one company, not the margin of any one flight: it can't tell you what your own flight earned.
- **Most of the rise in the loss is on the last lines.** See the note under the receipt: the tax credit and special items account for 59.6% of the rise in the net loss.
- **Fuel moves both ways.** JetBlue expects a better margin in the fourth quarter and had no hedges, so results can change fast in either direction.
- **Interest lines aren't reported the same way at every airline.** Delta and American publish interest already net of interest income; United, Southwest, Frontier and JetBlue publish the full expense. Because of that, and because the airlines differ in size and network, the comparison is a reference, not a ranking to the cent.
- **Delta and American have no passenger count in these filings**, so they appear only per $100 of revenue and in totals. Delta's refinery sales to third parties were taken out of its revenue base.
- **2019 against 2025 has a limit:** the average flight got longer, and a longer flight costs and earns more. The payroll rise mixes three things: higher pay, fewer passengers per employee and longer flights.
- **The months of liquidity are arithmetic, not a forecast**, and they come before any new loans or debt repayments. The burn moves with fuel and with investment, and JetBlue expects to improve.
- **No bankruptcy filing as of the video.** JetBlue had not filed. Its CEO told CNBC in October 2026 that there's no intention and no plan to file. The 10-Q of October 26, 2026 says: "We believe there is sufficient liquidity available to us to meet our cash requirements for at least the next 12 months", and it carries no going-concern warning.
- **Bond and stock prices and the advisers come from the press**, on the date of each report, not from a filing. We found no public quote for the notes after October. The stock's rebound came with falling oil, and oil can move the other way too.
- **The collateral is "certain collateral in connection with" the TrueBlue program**, in the words of the filing. That doesn't mean a customer's points belong to a lender.
- **The Spirit comparison crosses dates.** The deal price is for the shares, without Spirit's debt, and JetBlue's market value is from October 2026. We can't know whether the deal would have saved the two airlines. The costs are the ones JetBlue booked as tied to it.
- **The loyalty figures are revenue, not profit.** They add flights paid with points to the non-flight part of point sales, such as those to the card partner, and lounge access.
- **Fort Lauderdale:** the T-100 count covers domestic seats only and runs through July 2026. The fourth-quarter share is JetBlue's own forecast, on its own base.
- **The gallon by airline** is for the second quarter, the latest in Form 41 at the time, and it includes taxes and fueling fees.

## Reproduce it

```
python calc.py
```

Standard library only, no network. It reads the files in `data/`:

- `inputs.csv`: every value taken from the SEC filings, as published and in the filing's unit, with the table label or the exact sentence and the document's URL; plus JetBlue's 2025 passengers in the T-100, used only for a check;
- `published_figures.csv`: note and stock prices, Carl Icahn's stake and the projection Neeleman cited, with a description and the source URL;
- `quotes.csv`: the sentences the count relies on in the filings (no number comes from them);
- `form41_fuel_2026.csv`: gallons and total cost by airline and month (BTS, Form 41, P-12(a), summed by airline and month);
- `t100_fll_july_seats.csv`: domestic seats leaving Fort Lauderdale in July by airline (BTS, T-100, summed by airline);
- `bls_cpi_u_monthly.csv`: the CPI-U months of 2019 and 2025.

It prints the consistency checks (the lines add up to the published totals in every period; passenger revenue per passenger matches the published fare; the three quarters add up to the nine months; the losses close the fall in retained earnings; balance sheet debt matches the maturities table; JetBlue's passengers match the T-100 within 3%) and writes `numbers.json`.

## Sources

**JetBlue, SEC filings**

- [JetBlue, Form 10-Q, third quarter of 2026 (October 26, 2026)](https://www.sec.gov/Archives/edgar/data/1158463/000115846326000097/jblu-20260930.htm)
- [JetBlue, Form 10-Q, second quarter of 2026 (July 28, 2026)](https://www.sec.gov/Archives/edgar/data/1158463/000115846326000075/jblu-20260630.htm)
- [JetBlue, Form 10-Q, first quarter of 2026 (April 28, 2026)](https://www.sec.gov/Archives/edgar/data/1158463/000115846326000061/jblu-20260331.htm)
- [JetBlue, Form 8-K of October 26, 2026, exhibit 99.1 (third-quarter results)](https://www.sec.gov/Archives/edgar/data/1158463/000115846326000095/ex991-earningsreleaseq32026.htm)
- [JetBlue, Form 8-K of January 27, 2026, exhibit 99.1 (2025 results and 2026 guidance)](https://www.sec.gov/Archives/edgar/data/1158463/000115846326000004/ex991-earningsreleaseq42025.htm)
- [JetBlue, Form 8-K of September 3, 2024 (the 2031 notes and the TrueBlue term loan)](https://www.sec.gov/Archives/edgar/data/1158463/000121390024075128/ea0213241-8k_jetblue.htm)
- [JetBlue, Form 10-K 2025](https://www.sec.gov/Archives/edgar/data/1158463/000115846326000007/jblu-20251231.htm)
- [JetBlue, Form 10-K 2024](https://www.sec.gov/Archives/edgar/data/1158463/000115846325000005/jblu-20241231.htm)
- [JetBlue, Form 10-K 2023](https://www.sec.gov/Archives/edgar/data/1158463/000115846324000006/jblu-20231231.htm)
- [JetBlue, Form 10-K 2019](https://www.sec.gov/Archives/edgar/data/1158463/000115846320000012/a201910-k.htm)
- [Carl Icahn, Schedule 13D, February 2024](https://www.sec.gov/Archives/edgar/data/1158463/000153949724000264/n2779_x199-sc13d.htm)
- [Carl Icahn, Schedule 13D/A, August 2026](https://www.sec.gov/Archives/edgar/data/1158463/000153949726002326/xslSCHEDULE_13D_X02/primary_doc.xml)

**The other airlines, Form 10-Q, third quarter of 2026**

- [Delta](https://www.sec.gov/Archives/edgar/data/27904/000002790426000038/dal-20260930.htm)
- [United](https://www.sec.gov/Archives/edgar/data/100517/000010051726000186/ual-20260930.htm)
- [American](https://www.sec.gov/Archives/edgar/data/6201/000000620126000065/aal-20260930.htm)
- [Southwest](https://www.sec.gov/Archives/edgar/data/92380/000009238026000107/luv-20260930.htm)
- [Frontier](https://www.sec.gov/Archives/edgar/data/1670076/000167007626000103/fron-20260930.htm)

**Spirit, SEC filings**

- [Spirit, Form 8-K of July 28, 2022, exhibit 99.2 (the deal with JetBlue)](https://www.sec.gov/Archives/edgar/data/1498710/000119312522204192/d368049dex992.htm)
- [Spirit, Form 10-K 2024](https://www.sec.gov/Archives/edgar/data/1498710/000149871025000008/save-20241231.htm)

**U.S. government data**

- [BTS TranStats, Form 41, Schedule P-12(a), fuel cost and consumption](https://www.transtats.bts.gov/DL_SelectFields.aspx?gnoyr_VQ=FMH&QO_fu146_anzr=Nv4%20Pn44vr45)
- [BTS TranStats, T-100 Domestic Segment (U.S. Carriers)](https://www.transtats.bts.gov/DL_SelectFields.aspx?gnoyr_VQ=FIM&QO_fu146_anzr=Nv4%20Pn44vr45)
- [BTS TranStats, T-100 Segment (All Carriers)](https://www.transtats.bts.gov/DL_SelectFields.aspx?gnoyr_VQ=FMG&QO_fu146_anzr=Nv4%20Pn44vr45)
- [U.S. Bureau of Labor Statistics, CPI-U, all items, U.S. city average (CUUR0000SA0)](https://data.bls.gov/timeseries/CUUR0000SA0)

**Press**

- [Fox Business, JetBlue creditors hire advisors as financial concerns grow (citing The Wall Street Journal)](https://www.foxbusiness.com/economy/jetblue-creditors-hire-advisors-financial-concerns-grow)
- [View from the Wing, JetBlue's frequent flyer-backed bonds hit 14% yield](https://viewfromthewing.com/jetblues-frequent-flyer-backed-bonds-hit-14-yield-after-airline-schedules-mysterious-investor-call/)
- [View from the Wing, JetBlue founder warns the airline may go bankrupt this year](https://viewfromthewing.com/jetblue-founder-warns-the-airline-may-go-bankrupt-this-year-and-says-nobody-will-buy-it/)
- [Bloomberg, October 22, 2026](https://www.bloomberg.com/news/articles/2026-10-22/jetblue-jblu-stock-bonds-plunge-to-record-lows-signaling-danger)
- [Bloomberg, October 26, 2026](https://www.bloomberg.com/news/articles/2026-10-26/jetblue-shares-tumble-to-new-low-ahead-of-high-stakes-earnings)
- [Yahoo Finance, JBLU historical prices](https://finance.yahoo.com/quote/JBLU/history/)
- [CNBC, JetBlue stock surges as company outlook calms investors (October 26, 2026, updated October 27)](https://www.cnbc.com/2026/10/26/jetblue-jblu-3q-2026-earnings.html)
- [The Points Guy, what happens to frequent flyer miles in an airline bankruptcy](https://thepointsguy.com/news/frequent-flyer-miles-airline-bankruptcy/)
- [The Points Guy, Spirit's shutdown: refunds, points and vouchers](https://thepointsguy.com/news/spirit-airlines-shutdown-refunds-points-vouchers-bankruptcy/)
- [ABC News, what American Airlines' bankruptcy means for you](https://abcnews.go.com/blogs/business/2011/11/what-american-airlines-bankruptcy-means-for-you)
- [Executive Traveller, United's loan against MileagePlus](https://www.executivetraveller.com/news/how-united-airlines-took-a-7bn-mortgage-on-its-frequent-flyer-scheme)
- [The Points Guy, Delta's loan against SkyMiles](https://thepointsguy.com/news/delta-air-lines-mortgage-skymiles-cash-coronavirus)
- [eGlobal Travel Media, airline loyalty programs as lifelines (American's AAdvantage)](https://eglobaltravelmedia.com.au/airlines-loyalty-programs-as-lifelines/)

The press items on the last seven lines carry no number in `calc.py`: they are context for the sentences above.

## Corrections

None so far. Found an error? Open an issue with the line and the source.

## License

Code (`calc.py`): [MIT](../LICENSE). Data, text and tables: [CC BY 4.0](../LICENSE-DATA.md); the underlying public records keep their own terms.

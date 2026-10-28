# #007 · Parking vs planes: who pays a US airport more, your car or the airlines?

**Video:** coming soon

## The answer

At **23 of the 30** large-hub airports in the FAA's airport finance database, parking and ground transportation brought in more than the passenger airlines paid in landing fees in fiscal 2025. Against everything the passenger airlines pay the airport (landing fees, terminal rent and the rest), parking wins at only **2**: Reagan National (DCA) and Nashville (BNA). At the medium hubs, it wins at **13 of 35**, and at 8 of them it beats even all aeronautical revenue: passenger airlines, cargo, private jets, all of it.

This is revenue, not profit, and it is nobody's parking bill: every number is divided by all the passengers who board, connecting passengers included.

## What counts as "the car" and "the plane"

Airports report their finances to the FAA on Form 5100-127 (Operating and Financial Summary), one form per fiscal year. The line numbers below are the form's; the definitions are in FAA Advisory Circular 150/5100-19D.

- **The car** is line 4.6, *Parking and ground transportation*: the airport's own garages and lots (valet and off-airport parking included) plus the fees it charges taxis, ride-shares, limos and shuttles. The form reports the two together. Rental cars are a separate line (4.5) and stay out.
- **The plane, round one** is line 1.1, *Passenger airline landing fees*: what airlines pay to use the runway.
- **The plane, round two** is line 1.6, *everything the passenger airlines pay*: landing fees, terminal rent, apron charges, federal inspection fees and other fees.
- **Two stricter tests:** line 1.6 plus cargo landing fees and cargo and hangar rentals (lines 2.1 and 2.4), and all aeronautical revenue (line 3.0: passenger and cargo airlines, general aviation, fuel, security reimbursements and the rest).
- **Per passenger:** each line divided by enplanements (line 16.1), the passengers who board there.
- **The groups** are the FAA database's own labels: large hubs and medium hubs, fiscal 2025. Each airport has its own fiscal year; the tables at the end show when each one ends.

## The two groups together

| Fiscal 2025 | Large hubs (30) | per passenger | Medium hubs (35) | per passenger |
|---|---|---|---|---|
| Parking and ground transportation (4.6) | $4.2 billion | **$6.01** | $1.6 billion | **$8.94** |
| Passenger airline landing fees (1.1) | $4.4 billion | $6.19 | $759.6 million | $4.37 |
| Terminal rents paid by the airlines (1.2) | $7.0 billion | | $1.4 billion | |
| Everything passenger airlines pay (1.6) | $12.3 billion | **$17.45** | $2.3 billion | **$13.12** |
| Landing fees as a share of 1.6 | 35.5% | | 33.3% | |
| Rental cars, left out (4.5) | $1.4 billion | | $530.0 million | |
| Enplanements (16.1) | 704.1 million | | 173.9 million | |

Added up, the large hubs' parking and their landing fees come out close to a tie per passenger. The airlines' biggest bill is not the runway but the rent for the terminal.

## The scoreboard

| Airports where parking and ground transportation (4.6) bring in more than... | Large hubs | Medium hubs |
|---|---|---|
| ...passenger airline landing fees (1.1) | **23** of 30 | **31** of 35 |
| ...everything passenger airlines pay (1.6) | **2** | **13** |
| ...1.6 plus cargo landing fees and cargo and hangar rentals | 2 | 9 |
| ...all aeronautical revenue (3.0) | 2 | **8** |

Is it stable? The same counts in the earlier forms:

| | Large hubs | Medium hubs |
|---|---|---|
| Fiscal 2019: parking beats landing fees / everything airlines pay | 22 / 3 of 30 | 29 / 13 of 35 |
| Fiscal 2024: parking beats landing fees / everything airlines pay | 22 / 2 of 30 | 30 / 17 of 35 |

In fiscal 2019, Atlanta was almost a tie, with parking just ahead: $2.93 per passenger against $2.90 from the airlines.

**Where the car wins, what's different?** Across both groups, at the 15 airports where parking beats everything the airlines pay, the median airport takes in $12.39 per passenger from parking, and its airlines pay $9.12. At the other 50: $6.35 from parking, $13.30 from the airlines.

## Nashville: the rides decide

On its Form 127, Nashville reports $131.4 million from parking and ground transportation ($10.61 per passenger), against $116.5 million from everything the passenger airlines pay ($9.41).

Nashville's own annual report (ACFR, fiscal year ending June 30, 2025) splits that parking line in two, and the two parts add up exactly to the Form 127 line (`calc.py` checks it):

| Nashville, fiscal 2025 | Per year | Per passenger |
|---|---|---|
| Parking (the garages and lots) | $113.2 million | $9.14 |
| Ground transportation (fees on Uber, Lyft, taxi and shuttle trips) | $18.2 million | $1.47 |
| Everything passenger airlines pay (Form 127, 1.6) | $116.5 million | $9.41 |

The garage alone minus everything the airlines pay: **-$3.3 million**. Using only the ACFR (terminal rents and fees $66.4 million, landing and related fees $51.7 million), the garage alone comes out at -$4.9 million. Either way, the garage alone loses; the fees the airport charges on every ride-share and taxi trip are what put Nashville ahead.

## Reagan National and Denver

- **Reagan National (DCA):** parking and ground transportation $8.75 per passenger against $7.49 from the airlines; $109.0 million against $93.2 million a year.
- **Denver (DEN)** has the biggest parking business on the list, **$276.8 million** a year. Its passenger airlines pay $651.1 million: $6.72 against $15.80 per passenger. A parking business can be enormous and still lose.

## Medium hubs: Raleigh-Durham and Memphis

- **Raleigh-Durham (RDU)** has the biggest parking business among the medium hubs: $14.90 per passenger, against $9.90 from the airlines. It wins even against all aeronautical revenue: $115.9 million against $89.5 million.
- **Memphis (MEM)** wins against its passenger airlines ($29.8 million against $27.8 million), but cargo changes the picture (Memphis is FedEx's home hub): cargo landing fees alone come to $41.5 million, and all aeronautical revenue to $88.7 million.

## Every airport

Names as they appear in the FAA's database. "Parking" is line 4.6 (parking plus ground transportation fees).

### Large hubs (30), fiscal 2025

Sorted from where parking does best against the airlines to where it does worst.

| Airport | Fiscal year ends | Enplanements | Parking and ground transportation, per passenger | Landing fees, per passenger | Everything passenger airlines pay, per passenger | Parking beats landing fees | Parking beats everything airlines pay |
|---|---|---|---|---|---|---|---|
| Ronald Reagan Washington National (DCA) | 12/31/2025 | 12.5 million | $8.75 | $2.91 | $7.49 | yes | **yes** |
| Nashville Intl (BNA) | 06/30/2025 | 12.4 million | $10.61 | $2.65 | $9.41 | yes | **yes** |
| Washington Dulles Internati (IAD) | 12/31/2025 | 14.3 million | $8.92 | $2.83 | $9.56 | yes | no |
| Hartsfield-Jackson Atlanta International (ATL) | 06/30/2025 | 53.4 million | $3.64 | $1.59 | $4.48 | yes | no |
| Charlotte/Douglas Intl (CLT) | 06/30/2025 | 28.1 million | $4.80 | $2.38 | $6.49 | yes | no |
| Phoenix Sky Harbor Intl (PHX) | 06/30/2025 | 26.1 million | $6.78 | $2.38 | $8.62 | yes | no |
| Tampa Intl (TPA) | 09/30/2025 | 12.3 million | $10.43 | $3.01 | $12.78 | yes | no |
| Harry Reid Intl (LAS) | 06/30/2025 | 28.6 million | $3.81 | $1.35 | $7.13 | yes | no |
| Baltimore-Washington Intl (BWI) | 06/30/2025 | 13.0 million | $8.20 | $4.51 | $11.57 | yes | no |
| Minneapolis-St Paul Intl (MSP) | 12/31/2025 | 17.5 million | $9.04 | $7.01 | $12.71 | yes | no |
| Detroit Metro Wayne (DTW) | 12/31/2025 | 16.7 million | $7.46 | $4.70 | $12.01 | yes | no |
| Fort Lauderdale/ Hollywood Intl (FLL) | 09/30/2025 | 16.2 million | $4.71 | $1.97 | $9.47 | yes | no |
| George Bush Intercontinental (IAH) | 06/30/2025 | 24.1 million | $5.12 | $2.76 | $11.17 | yes | no |
| Dallas/Fort Worth Intl (DFW) | 09/30/2025 | 43.1 million | $6.29 | $3.35 | $13.86 | yes | no |
| Austin-Bergstrom Intl (AUS) | 09/30/2025 | 10.7 million | $8.45 | $5.58 | $16.08 | yes | no |
| Orlando Intl (MCO) | 09/30/2025 | 28.4 million | $4.92 | $2.26 | $12.56 | yes | no |
| Denver Intl (DEN) | 12/31/2025 | 41.2 million | $6.72 | $5.42 | $15.80 | yes | no |
| Philadelphia Intl (PHL) | 06/30/2025 | 15.4 million | $7.15 | $5.58 | $16.33 | yes | no |
| General Edward Lawrence Logan (BOS) | 06/30/2025 | 21.8 million | $12.13 | $7.64 | $23.50 | yes | no |
| San Diego Intl (SAN) | 06/30/2025 | 12.6 million | $6.43 | $4.50 | $18.52 | yes | no |
| Seattle-Tacoma Intl (SEA) | 12/31/2025 | 26.3 million | $5.85 | $5.62 | $19.06 | yes | no |
| Salt Lake City Intl (SLC) | 06/30/2025 | 13.9 million | $5.94 | $5.73 | $19.25 | yes | no |
| Miami Intl (MIA) | 09/30/2025 | 27.7 million | $2.93 | $2.06 | $17.62 | yes | no |
| Chicago Midway International (MDW) | 12/31/2025 | 9.7 million | $3.70 | $10.09 | $19.14 | no | no |
| Laguardia (LGA) | 12/31/2025 | 16.4 million | $5.80 | $19.72 | $23.89 | no | no |
| San Francisco Intl (SFO) | 06/30/2025 | 27.0 million | $7.61 | $9.38 | $28.11 | no | no |
| Chicago Ohare Intl (ORD) | 12/31/2025 | 42.3 million | $3.24 | $17.36 | $29.84 | no | no |
| Los Angeles Intl (LAX) | 06/30/2025 | 37.7 million | $6.07 | $8.72 | $33.85 | no | no |
| Newark Intl (EWR) | 12/31/2025 | 23.6 million | $6.23 | $14.84 | $35.35 | no | no |
| John F Kennedy Intl (JFK) | 12/31/2025 | 31.2 million | $4.17 | $13.65 | $38.37 | no | no |

### Medium hubs (35), fiscal 2025

Sorted from where parking does best against the airlines to where it does worst.

| Airport | Fiscal year ends | Enplanements | Parking and ground transportation, per passenger | Landing fees, per passenger | Everything passenger airlines pay, per passenger | Parking beats landing fees | Parking beats everything airlines pay |
|---|---|---|---|---|---|---|---|
| Burbank-Glendale-Pasadena (BUR) | 06/30/2025 | 3.3 million | $11.92 | $1.25 | $1.92 | yes | **yes** |
| Eppley Airfield (OMA) | 12/31/2025 | 2.6 million | $15.47 | $4.69 | $9.59 | yes | **yes** |
| Bradley Intl (BDL) | 06/30/2025 | 3.4 million | $12.97 | $5.82 | $7.63 | yes | **yes** |
| Cincinnati/Northern Kentucky (CVG) | 12/31/2025 | 4.5 million | $15.69 | $3.65 | $10.59 | yes | **yes** |
| Raleigh-Durham Intl (RDU) | 03/31/2025 | 7.8 million | $14.90 | $2.85 | $9.90 | yes | **yes** |
| Palm Beach Intl (PBI) | 09/30/2025 | 4.3 million | $6.19 | $0.29 | $1.89 | yes | **yes** |
| Port Columbus Intl (CMH) | 12/31/2025 | 4.5 million | $12.98 | $3.93 | $9.12 | yes | **yes** |
| Ontario Intl (ONT) | 06/30/2025 | 3.5 million | $11.59 | $2.24 | $7.74 | yes | **yes** |
| General Mitchell Intl (MKE) | 12/31/2025 | 2.9 million | $12.16 | $8.11 | $9.00 | yes | **yes** |
| Norfolk International (ORF) | 06/30/2025 | 2.4 million | $12.39 | $4.27 | $10.29 | yes | **yes** |
| Boise Air Terminal/Gowen Field (BOI) | 09/30/2025 | 2.6 million | $9.63 | $5.37 | $7.85 | yes | **yes** |
| Memphis Intl (MEM) | 06/30/2025 | 2.4 million | $12.55 | $2.80 | $11.68 | yes | **yes** |
| Indianapolis Intl (IND) | 12/31/2025 | 5.3 million | $14.70 | $4.97 | $14.43 | yes | **yes** |
| Charleston Intl (CHS) | 06/30/2025 | 3.2 million | $11.57 | $0.27 | $12.14 | yes | no |
| Jacksonville Intl (JAX) | 09/30/2025 | 3.8 million | $9.61 | $4.16 | $10.25 | yes | no |
| Reno/Tahoe Intl (RNO) | 06/30/2025 | 2.5 million | $8.86 | $2.92 | $10.05 | yes | no |
| Cleveland-Hopkins Intl (CLE) | 12/31/2025 | 4.9 million | $11.02 | $3.44 | $12.32 | yes | no |
| Kansas City Intl (MCI) | 04/30/2025 | 5.9 million | $13.03 | $4.32 | $15.37 | yes | no |
| Pittsburgh International (PIT) | 12/31/2025 | 4.9 million | $13.74 | $4.92 | $16.10 | yes | no |
| Albuquerque Intl (ABQ) | 06/30/2025 | 2.7 million | $6.40 | $4.07 | $9.31 | yes | no |
| William P Hobby (HOU) | 06/30/2025 | 7.0 million | $5.29 | $3.53 | $8.78 | yes | no |
| Lambert-St Louis Intl (STL) | 06/30/2025 | 7.7 million | $6.23 | $7.34 | $10.76 | no | no |
| Dallas Love Field (DAL) | 09/30/2025 | 8.6 million | $6.24 | $4.29 | $11.34 | yes | no |
| John Wayne Airport-Orange C (SNA) | 06/30/2025 | 5.5 million | $9.00 | $4.13 | $14.93 | yes | no |
| San Antonio Intl (SAT) | 09/30/2025 | 5.4 million | $6.93 | $3.39 | $13.31 | yes | no |
| Sacramento International Airport (SMF) | 06/30/2025 | 6.9 million | $11.78 | $6.18 | $18.41 | yes | no |
| Southwest Florida Intl (RSW) | 09/30/2025 | 5.5 million | $5.99 | $3.91 | $13.05 | yes | no |
| Luis Munoz Marin Intl (SJU) | 12/31/2025 | 6.8 million | $3.17 | $4.91 | $11.29 | no | no |
| Kahului (OGG) | 06/30/2025 | 3.6 million | $1.60 | $5.48 | $10.55 | no | no |
| Anchorage Intl (ANC) | 06/30/2025 | 2.7 million | $4.03 | $3.11 | $13.08 | yes | no |
| New Orleans Intl (MSY) | 12/31/2025 | 6.2 million | $4.13 | $2.19 | $13.29 | yes | no |
| Oakland International Airport (OAK) | 06/30/2025 | 5.0 million | $8.68 | $5.94 | $18.02 | yes | no |
| Portland Intl (PDX) | 06/30/2025 | 9.0 million | $10.87 | $4.39 | $23.68 | yes | no |
| San Jose Internation (SJC) | 06/30/2025 | 5.7 million | $7.29 | $6.28 | $21.57 | yes | no |
| Honolulu Intl (HNL) | 06/30/2025 | 11.0 million | $2.10 | $6.58 | $21.57 | no | no |

## What this number doesn't show

- Line 4.6 combines the airport's own parking with the fees it charges taxis, ride-shares, limos and shuttles; the FAA doesn't split them. Nashville's annual report does, and there the garage alone loses.
- It's revenue, not profit: garages cost money to build and run, and the Form 127 doesn't split expenses by line.
- "Everything the airlines pay" is what passenger airlines pay the airport. Cargo airlines and general aviation stay out of it, and rental cars too, as a separate line. Adding cargo landing fees and cargo and hangar rentals to the plane's side, the car wins at 2 large hubs and 9 medium hubs.
- The Passenger Facility Charge on your ticket goes to construction projects: it is not in the airport's operating revenue or in what the airlines pay.
- Each airport has its own fiscal year (ending in June, September or December, among others), so the 2025 totals mix different periods. The Form 127 enplanements stay close to the BTS T-100 count for calendar 2025 (`calc.py` checks every airport within 10%).
- Per passenger means per passenger who boards, connecting passengers included, and a family of four counts as four passengers but parks one car. It is a fair way to compare airports of very different sizes, not what anyone pays.
- The tables show the forms as filed. A few look unusual (Burbank and Palm Beach report the airlines paying very little per passenger) and were not checked against each airport's own annual report; only Nashville's was.
- The groups follow the FAA database's own labels (large and medium hubs).

## Reproduce it

```
python calc.py
```

Standard library only, no network. It reads the files in `data/`:

- `form127.csv`: one row per Form 127 (large and medium hubs, fiscal 2025, 2019 and 2024), with every line used, exactly as published in the FAA's CATS database, and the source URL; an empty cell means the airport left it blank;
- `bts_t100_enplanements_2025.csv`: passengers boarding at each airport in the BTS T-100 Segment data (all carriers, calendar 2025), used only to check the enplanements;
- `nashville_acfr_fy2025.csv`: the four lines taken from Nashville's annual report, with the printed page.

It prints the consistency checks (every form's lines add up to its declared totals, no airport is missing a line used, one form per airport, enplanements match BTS, Nashville's report matches its form) and writes `numbers.json`.

## Sources

- [FAA, Certification Activity Tracking System (CATS), Form 5100-127 Operating and Financial Summary](https://cats.airports.faa.gov/reports)
- [FAA, Advisory Circular 150/5100-19D (Form 127 line definitions)](https://www.faa.gov/documentLibrary/media/Advisory_Circular/150_5100_19d.pdf)
- [Metropolitan Nashville Airport Authority, Annual Comprehensive Financial Report FY2025](https://flynashville.com/wp-content/uploads/2025/11/Annual-Comprehensive-Financial-Report-ACFR-FY25.pdf)
- [BTS, T-100 Segment (All Carriers), used only to check enplanements](https://www.transtats.bts.gov/DL_SelectFields.aspx?gnoyr_VQ=FMG&QO_fu146_anzr=Nv4%20Pn44vr45)

## Corrections

None so far. Found an error? Open an issue with the line and the source.

"""Ticket Math #013 - Las Vegas airport: fewer passengers, and the airlines pay more for each one.

Recomputes every number in the video from the files in data/ and writes numbers.json.
Standard library only, no network: run `python calc.py` in this folder.

Method
1. FAA CATS, Form 5100-127 (Operating and Financial Summary) of Harry Reid International (LAS), fiscal years 2012 to
   2025 (July to June). Cost per enplanement (CPE) = everything passenger airlines pay the airport (line 1.6: landing
   fees, terminal rents, apron, federal inspection and other fees) / enplanements (line 16.1). The script checks it
   against the CPE the form itself publishes. LAS's place among the 30 large hubs (the CATS's own label), from the one
   that charges airlines least per passenger (1) to the one that charges most.
2. The airport's own documents (rates and charges, bond official statements, the ACFR, the quarterly report): the
   budgeted CPE of each fiscal year and the actual CPE, read from the PDFs (data/published_figures.csv).
3. BTS T-100 Segment (all carriers): passengers and seats on flights leaving LAS, by airline and month, 2019 and 2024 to
   2026; Spirit Airlines (code NK) against everyone else; the same for Fort Lauderdale (FLL) and Orlando (MCO), Spirit's
   other two biggest airports. "Year to date" = January to the last month BTS has published for 2026.
4. US DOT Consumer Airfare Report, Table 1 (top 1,000 city-pair markets in the lower 48): average fare of the markets
   with Las Vegas, weighted by passengers, and the fare of the cheapest airline in each market.
5. EIA: U.S. Gulf Coast kerosene-type jet fuel, spot price, monthly average.
"""
import csv
import json
import statistics
from pathlib import Path

HERE = Path(__file__).parent
LAS, OTHERS, SPIRIT = "LAS", ["FLL", "MCO"], "NK"
FAA_YEARS = list(range(2012, 2026))
FY = 2025                        # last fiscal year in the Form 127 (July 2024 to June 2025)
RANK_YEARS = [2019, 2024, 2025]
BTS_YEARS = [2019, 2024, 2025, 2026]
BTS_FULL, BTS_PARTIAL = 2025, 2026
BASE_YEAR = 2024                 # last full year before Spirit shrank in Las Vegas
FISCAL_START = 7                 # LAS's fiscal year starts in July
CANADIAN = ["WS", "AC", "RV", "07Q", "PD"]   # WestJet, Air Canada, Air Canada Rouge, Flair, Porter
DOT_QUARTERS = [(2019, 1), (2024, 1), (2025, 1), (2026, 1)]
DOT_BEFORE, DOT_AFTER = (2025, 1), (2026, 1)
DOT_EXAMPLE = "Chicago, IL"
MIN_MARKETS = 50
TOL_SUM = 0.001                  # lines of a form against the total the airport declared
TOL_CPE = 0.005                  # our CPE against the one printed on the form (rounded to the cent)
TOL_ENPLANEMENTS = 0.05          # Form 127 enplanements (fiscal year) against BTS passengers leaving (July to June)

AIRLINES = "Total Passenger Airline Aeronautical Revenue"            # line 1.6
ENPLANEMENTS = "Enplanements"                                        # line 16.1
CPE_PRINTED = "Passenger Airline CPE (line 1.6 / 16.1)"
AIRLINE_LINES = ["Passenger airline landing fees", "Terminal arrival fees, rents, and utilities",
                 "Terminal area apron charges/tiedowns", "Federal Inspection Fees", "Other passenger aeronautical fees"]
NON_AERO = "Total Non-Aeronautical Revenue"                          # line 4.9
NON_AERO_LINES = ["Land and non-terminal facility leases and revenues", "Terminal-food and beverage",
                  "Terminal-retail stores and duty free", "Terminal-services and other",
                  "Rental cars-excludes customer facility charges", "Parking and ground transportation", "Hotel",
                  "Other Non-Aeronautical Revenue"]
OPERATING = "Total Operating Revenue"                                # line 5.0
YEARLY = [("cpe", None, "cost per enplanement (1.6 / 16.1)"),
          ("enplanements", ENPLANEMENTS, "enplanements (16.1)"),
          ("signatory_landing_fee_rate", "Signatory landing fee rate per 1,000 lbs",
           "signatory landing fee rate per 1,000 lbs of landed weight"),
          ("airline_payments", AIRLINES, "everything passenger airlines pay (1.6)"),
          ("landing_fees", "Passenger airline landing fees", "passenger airline landing fees (1.1)"),
          ("terminal_rents", "Terminal arrival fees, rents, and utilities", "terminal rents and fees paid by airlines (1.2)"),
          ("parking", "Parking and ground transportation", "parking and ground transportation (4.6)"),
          ("non_aeronautical_revenue", NON_AERO, "all revenue that doesn't come from airlines (4.9)"),
          ("operating_revenue", OPERATING, "operating revenue (5.0)"),
          ("grant_receipts", "Grant receipts", "federal grant receipts"),
          ("operating_expenses", "Subtotal - Operating Expenses", "operating expenses before depreciation"),
          ("debt", "Total Debt at End of Year", "debt at the end of the fiscal year"),
          ("unrestricted_cash", "Unrestricted Cash and Investments", "unrestricted cash and investments"),
          ("interest_expense", "Interest expense (use minus sign)", "interest expense"),
          ("debt_service", "Debt service, excluding coverage", "debt service, excluding coverage")]
PER_PASSENGER = [("parking", "Parking and ground transportation", "parking and ground transportation (taxi, shuttle and "
                  "ride-share fees included)"),
                 ("rental_cars", "Rental cars-excludes customer facility charges", "rental cars, without the customer "
                  "facility charge"),
                 ("food_and_beverage", "Terminal-food and beverage", "food and beverage in the terminal"),
                 ("retail", "Terminal-retail stores and duty free", "retail stores and duty free"),
                 ("terminal_services", "Terminal-services and other", "terminal services and other"),
                 ("non_aeronautical_revenue", NON_AERO, "all revenue that doesn't come from airlines"),
                 ("operating_revenue", OPERATING, "operating revenue"),
                 ("operating_expenses", "Subtotal - Operating Expenses", "operating expenses before depreciation"),
                 ("debt_service", "Debt service, excluding coverage", "debt service")]
TEXT = {"year", "hub_size", "location_id", "airport_name", "state", "fiscal_year_end", "url"}

with open(HERE / "data" / "form127.csv", newline="", encoding="utf-8") as f:
    forms = [{k: (x if k in TEXT else (float(x) if x != "" else None)) for k, x in r.items()} for r in csv.DictReader(f)]
T100 = {}   # (year, origin, carrier, month) -> [passengers, seats]
with open(HERE / "data" / "t100_departures.csv", newline="", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        T100[(int(r["year"]), r["origin"], r["carrier"], int(r["month"]))] = [float(r["passengers"]), float(r["seats"])]
with open(HERE / "data" / "dot_table1.csv", newline="", encoding="utf-8") as f:
    DOT = {}
    for r in csv.DictReader(f):
        DOT.setdefault((int(r["year"]), int(r["quarter"])), {})[tuple(sorted((r["citymarketid_1"], r["citymarketid_2"])))] = r
with open(HERE / "data" / "eia_jet_fuel.csv", newline="", encoding="utf-8") as f:
    JET = {r["month"]: float(r["usd_per_gallon"]) for r in csv.DictReader(f)}
with open(HERE / "data" / "published_figures.csv", newline="", encoding="utf-8") as f:
    K = {r["key"]: float(r["value"]) for r in csv.DictReader(f)}
out = {}


def put(key, value, unit, description):
    out[key] = {"value": value, "unit": unit, "description": description}
    return value


def check(label, ok, detail):
    print(f"{'ok  ' if ok else 'FAIL'} {label}: {detail}")
    if not ok:
        raise SystemExit(1)


def v(form, column):   # an empty cell counts as zero
    return form[column] or 0


def form(year, airport=LAS):
    return next(r for r in forms if int(r["year"]) == year and r["location_id"] == airport)


# ---------------------------------------------------------------- 1. The airport, per passenger (FAA Form 127)
for year in FAA_YEARS:
    r = form(year)
    parts = sum(v(r, c) for c in AIRLINE_LINES)
    check(f"LAS fiscal {year}: the 5 lines airlines pay add up to the declared total (1.6)",
          abs(parts - v(r, AIRLINES)) <= TOL_SUM * v(r, AIRLINES), f"{parts:,.0f} vs {v(r, AIRLINES):,.0f}")
    cpe = v(r, AIRLINES) / v(r, ENPLANEMENTS)
    check(f"LAS fiscal {year}: our CPE (1.6 / 16.1) = the CPE printed on the form",
          abs(cpe - v(r, CPE_PRINTED)) <= TOL_CPE * cpe, f"{cpe:.4f} vs {v(r, CPE_PRINTED)}")
    for k, column, desc in YEARLY:
        if k == "cpe":
            put(f"las_cpe_fy{year}", cpe, "usd per enplaned passenger", f"LAS, fiscal year ending {r['fiscal_year_end']}: "
                "everything passenger airlines pay the airport per enplaned passenger")
        elif r[column] is not None:
            unit = ("passengers" if k == "enplanements" else "usd per 1,000 lbs" if k == "signatory_landing_fee_rate"
                    else "usd per year")
            put(f"las_{k}_fy{year}", abs(v(r, column)), unit, f"LAS, fiscal year ending {r['fiscal_year_end']}: {desc}")

r = form(FY)
parts = sum(v(r, c) for c in NON_AERO_LINES)
check(f"LAS fiscal {FY}: the 8 non-aeronautical lines add up to the declared total (4.9)",
      abs(parts - v(r, NON_AERO)) <= TOL_SUM * v(r, NON_AERO), f"{parts:,.0f} vs {v(r, NON_AERO):,.0f}")
both = v(r, "Total Aeronautical Revenue") + v(r, NON_AERO)
check(f"LAS fiscal {FY}: aeronautical + non-aeronautical = operating revenue (5.0)",
      abs(both - v(r, OPERATING)) <= TOL_SUM * v(r, OPERATING), f"{both:,.0f} vs {v(r, OPERATING):,.0f}")
for k, column, desc in PER_PASSENGER:
    put(f"las_{k}_per_passenger_fy{FY}", v(r, column) / v(r, ENPLANEMENTS), "usd per enplaned passenger",
        f"LAS, fiscal {FY}: {desc}, per enplaned passenger")
    if k in ("rental_cars", "food_and_beverage", "retail", "terminal_services"):
        put(f"las_{k}_fy{FY}", v(r, column), "usd per year", f"LAS, fiscal {FY}: {desc}")
for year in RANK_YEARS:
    r = form(year)
    put(f"las_airline_share_of_operating_revenue_fy{year}", v(r, AIRLINES) / v(r, OPERATING), "share",
        f"LAS, fiscal {year}: share of operating revenue paid by passenger airlines (1.6 / 5.0)")

# Where LAS ranks among the large hubs
for year in RANK_YEARS:
    large = [r for r in forms if int(r["year"]) == year and r["hub_size"] == "Large" and v(r, ENPLANEMENTS) > 0]
    ids = [r["location_id"] for r in large]
    check(f"Large hubs, fiscal {year}: one form per airport", len(ids) == len(set(ids)), f"{len(ids)} forms")
    order = sorted(large, key=lambda r: v(r, AIRLINES) / v(r, ENPLANEMENTS))
    place = [r["location_id"] for r in order].index(LAS) + 1
    put(f"large_hubs_fy{year}", len(large), "airports", f"Large hubs (CATS label) in the Form 127 of fiscal {year}")
    put(f"las_rank_among_large_hubs_fy{year}", place, "place", f"LAS among the large hubs in fiscal {year}, from the one "
        "that charges airlines least per passenger (1) to the one that charges most")
    put(f"large_hubs_median_cpe_fy{year}", statistics.median(v(r, AIRLINES) / v(r, ENPLANEMENTS) for r in order),
        "usd per enplaned passenger", f"Median cost per enplanement of the large hubs, fiscal {year}")
    if year == FY:
        for r in order[:place - 1]:
            put(f"{r['location_id'].lower()}_cpe_fy{year}", v(r, AIRLINES) / v(r, ENPLANEMENTS), "usd per enplaned passenger",
                f"{r['airport_name'].title()} ({r['location_id']}), fiscal year ending {r['fiscal_year_end']}: "
                "cost per enplanement")

# ---------------------------------------------------------------- 2. Who left (BTS T-100)
def total(year, origin, months, keep=lambda c: True, field=0):
    return sum(x[field] for (y, o, c, m), x in T100.items() if y == year and o == origin and m in months and keep(c))


ALL = range(1, 13)
is_nk = lambda c: c == SPIRIT
not_nk = lambda c: c != SPIRIT
last_month = max(m for (y, o, c, m) in T100 if y == BTS_PARTIAL and o == LAS)
YTD = [m for m in ALL if m <= last_month]
for year in BTS_YEARS:
    if year == BTS_PARTIAL:
        continue
    allp = total(year, LAS, ALL)
    put(f"las_passengers_{year}", allp, "passengers", f"Passengers on flights leaving LAS in {year}, all airlines")
    put(f"las_spirit_passengers_{year}", total(year, LAS, ALL, is_nk), "passengers",
        f"Spirit passengers on flights leaving LAS in {year}")
    check(f"BTS {year}: Spirit + everyone else = all airlines at LAS",
          abs(total(year, LAS, ALL, is_nk) + total(year, LAS, ALL, not_nk) - allp) < 1, f"{allp:,.0f}")
    put(f"las_spirit_share_{year}", total(year, LAS, ALL, is_nk) / allp, "share",
        f"Spirit's share of passengers leaving LAS in {year}")
prev = BTS_FULL - 1
lost = total(prev, LAS, ALL) - total(BTS_FULL, LAS, ALL)
lost_nk = total(prev, LAS, ALL, is_nk) - total(BTS_FULL, LAS, ALL, is_nk)
put(f"las_passengers_lost_{BTS_FULL}", lost, "passengers", f"Fewer passengers leaving LAS, {BTS_FULL} against {prev}")
put(f"las_spirit_passengers_lost_{BTS_FULL}", lost_nk, "passengers",
    f"Fewer Spirit passengers leaving LAS, {BTS_FULL} against {prev}")
put(f"spirit_share_of_passengers_lost_{BTS_FULL}", lost_nk / lost, "share",
    f"Spirit's loss as a share of the whole airport's loss, {BTS_FULL} against {prev}")
put(f"las_other_airlines_passenger_change_{BTS_FULL}", total(BTS_FULL, LAS, ALL, not_nk) - total(prev, LAS, ALL, not_nk),
    "passengers", f"Change in passengers of every airline except Spirit leaving LAS, {BTS_FULL} against {prev} "
    "(negative = they lost)")
by_month = {(y, m): total(y, LAS, [m], is_nk) for y in (prev, BTS_FULL) for m in ALL}
(peak_year, peak_month), peak = max(by_month.items(), key=lambda kv: kv[1])
put("las_spirit_best_month", peak, "passengers a month",
    f"Spirit passengers leaving LAS in its best month of {prev}-{BTS_FULL} ({peak_month}/{peak_year})")
put(f"las_spirit_december_{BTS_FULL}", total(BTS_FULL, LAS, [12], is_nk), "passengers a month",
    f"Spirit passengers leaving LAS in December {BTS_FULL}")

span = f"January to month {last_month}"
for name, keep, desc in [("", lambda c: True, "all airlines"), ("spirit_", is_nk, "Spirit"),
                         ("other_airlines_", not_nk, "every airline except Spirit")]:
    for year in (BTS_FULL, BTS_PARTIAL):
        put(f"las_{name}passengers_ytd_{year}", total(year, LAS, YTD, keep), "passengers",
            f"Passengers leaving LAS, {span} of {year}: {desc}")
        put(f"las_{name}seats_ytd_{year}", total(year, LAS, YTD, keep, 1), "seats",
            f"Seats on flights leaving LAS, {span} of {year}: {desc}")
put(f"las_passengers_lost_ytd_{BTS_PARTIAL}", total(BTS_FULL, LAS, YTD) - total(BTS_PARTIAL, LAS, YTD), "passengers",
    f"Fewer passengers leaving LAS, {span} of {BTS_PARTIAL} against {BTS_FULL}")
put(f"las_spirit_passengers_lost_ytd_{BTS_PARTIAL}", total(BTS_FULL, LAS, YTD, is_nk) - total(BTS_PARTIAL, LAS, YTD, is_nk),
    "passengers", f"Fewer Spirit passengers leaving LAS, {span} of {BTS_PARTIAL} against {BTS_FULL}")
put(f"las_spirit_seats_removed_ytd_{BTS_PARTIAL}",
    total(BTS_FULL, LAS, YTD, is_nk, 1) - total(BTS_PARTIAL, LAS, YTD, is_nk, 1), "seats",
    f"Seats Spirit stopped offering out of LAS, {span} of {BTS_PARTIAL} against {BTS_FULL}")
put(f"las_other_airlines_seat_change_ytd_{BTS_PARTIAL}",
    total(BTS_PARTIAL, LAS, YTD, not_nk, 1) - total(BTS_FULL, LAS, YTD, not_nk, 1), "seats",
    f"Change in seats of every other airline out of LAS, {span} of {BTS_PARTIAL} against {BTS_FULL} "
    "(negative = they cut too)")
put(f"las_other_airlines_passenger_change_ytd_{BTS_PARTIAL}",
    total(BTS_PARTIAL, LAS, YTD, not_nk) - total(BTS_FULL, LAS, YTD, not_nk), "passengers",
    f"Change in passengers of every airline except Spirit leaving LAS, {span} of {BTS_PARTIAL} against {BTS_FULL}")
check(f"BTS {BTS_PARTIAL}: the last month published is the same at LAS, FLL and MCO",
      all(max(m for (y, o, c, m) in T100 if y == BTS_PARTIAL and o == x) == last_month for x in OTHERS),
      f"month {last_month}")

# Months in a row with fewer passengers, and everyone but Spirit
down, others = [], []
for year in (BTS_FULL, BTS_PARTIAL):
    for m in (ALL if year == BTS_FULL else YTD):
        down.append(total(year, LAS, [m]) < total(year - 1, LAS, [m]))
        others.append(total(year, LAS, [m], not_nk) / total(year - 1, LAS, [m], not_nk) - 1)
put("months_compared", len(down), "months", f"Months from January {BTS_FULL} to the last published in {BTS_PARTIAL}")
put("months_with_fewer_passengers", sum(down), "months", "Of those months, the ones in which fewer passengers left LAS "
    "than in the same month a year earlier")
put("other_airlines_worst_month", min(others), "share", "Worst month of the airlines other than Spirit against the same "
    "month a year earlier, same period")
put("other_airlines_best_month", max(others), "share", "Best month of the airlines other than Spirit against the same "
    "month a year earlier, same period")
put("other_airlines_months_up", sum(x > 0 for x in others), "months", "Months of the same period in which the airlines "
    "other than Spirit carried more passengers than a year earlier")

# Spirit's three biggest airports: did the other airlines fill the seats?
for base, tag in ((BTS_FULL, "2025"), (BASE_YEAR, "2024")):
    for x in [LAS] + OTHERS:
        i = x.lower()
        removed = total(base, x, YTD, is_nk, 1) - total(BTS_PARTIAL, x, YTD, is_nk, 1)
        added = total(BTS_PARTIAL, x, YTD, not_nk, 1) - total(base, x, YTD, not_nk, 1)
        if base == BTS_FULL:
            put(f"{i}_spirit_seats_offered_ytd_{BTS_FULL}", total(BTS_FULL, x, YTD, is_nk, 1), "seats",
                f"{x}: Spirit seats leaving the airport, {span} of {BTS_FULL}")
            put(f"{i}_passenger_change_ytd_{BTS_PARTIAL}", total(BTS_PARTIAL, x, YTD) / total(BTS_FULL, x, YTD) - 1,
                "share", f"{x}: change in passengers leaving the airport, {span} of {BTS_PARTIAL} against {BTS_FULL}")
        if x != LAS or base == BASE_YEAR:
            put(f"{i}_spirit_seats_removed_ytd_{BTS_PARTIAL}_vs_{tag}", removed, "seats",
                f"{x}: seats Spirit stopped offering, {span} of {BTS_PARTIAL} against {base}")
            put(f"{i}_other_airlines_seats_added_ytd_{BTS_PARTIAL}_vs_{tag}", added, "seats",
                f"{x}: extra seats from the other airlines, {span} of {BTS_PARTIAL} against {base}")
        put(f"{i}_seats_added_per_spirit_seat_ytd_{BTS_PARTIAL}_vs_{tag}", added / removed, "share",
            f"{x}: seats the other airlines added for each seat Spirit removed, {span} of {BTS_PARTIAL} against {base} "
            "(negative = the others cut too)")
for year in (BASE_YEAR, BTS_FULL, BTS_PARTIAL):
    put(f"las_non_spirit_passengers_ytd_{year}", total(year, LAS, YTD, not_nk), "passengers",
        f"Passengers of every airline except Spirit leaving LAS, {span} of {year}")
    put(f"las_load_factor_ytd_{year}", total(year, LAS, YTD) / total(year, LAS, YTD, field=1), "share",
        f"Load factor of flights leaving LAS (passengers / seats), {span} of {year}")
put(f"las_spirit_passengers_ytd_{BASE_YEAR}", total(BASE_YEAR, LAS, YTD, is_nk), "passengers",
    f"Spirit passengers leaving LAS, {span} of {BASE_YEAR}")
for year in (BTS_FULL - 1, BTS_FULL, BTS_PARTIAL):
    put(f"las_canadian_airlines_passengers_ytd_{year}", total(year, LAS, YTD, lambda c: c in CANADIAN), "passengers",
        f"WestJet, Air Canada, Air Canada Rouge, Flair and Porter passengers leaving LAS, {span} of {year}")

# Form 127 enplanements (fiscal year) against BTS (July to June)
bts_fy = total(FY - 1, LAS, [m for m in ALL if m >= FISCAL_START]) + total(FY, LAS, [m for m in ALL if m < FISCAL_START])
check(f"LAS: Form 127 enplanements of fiscal {FY} match BTS (passengers leaving, July to June)",
      abs(v(form(FY), ENPLANEMENTS) / bts_fy - 1) <= TOL_ENPLANEMENTS,
      f"Form 127 {v(form(FY), ENPLANEMENTS):,.0f}; BTS {bts_fy:,.0f}")

# ---------------------------------------------------------------- 3. The fare (US DOT, Table 1)
def vegas(year, quarter):
    return {k: r for k, r in DOT[(year, quarter)].items() if "Las Vegas" in (r["city1"] + r["city2"])}


def weighted(rows, field):
    pax = sum(float(r["passengers"]) for r in rows)
    return sum(float(r[field]) * float(r["passengers"]) for r in rows) / pax


for year, q in DOT_QUARTERS:
    lv, every = vegas(year, q), list(DOT[(year, q)].values())
    tag = f"{year}q{q}"
    check(f"DOT {year} Q{q}: enough markets with Las Vegas", len(lv) >= MIN_MARKETS, f"{len(lv)}")
    put(f"las_vegas_markets_{tag}", len(lv), "markets", f"Markets with Las Vegas among DOT's top 1,000, {year} Q{q}")
    put(f"las_vegas_average_fare_{tag}", weighted(lv.values(), "fare"), "usd per ticket",
        f"Average fare in the markets with Las Vegas, {year} Q{q}, weighted by passengers")
    put(f"top_1000_average_fare_{tag}", weighted(every, "fare"), "usd per ticket",
        f"Average fare in DOT's top 1,000 markets, {year} Q{q}, weighted by passengers")
    put(f"las_vegas_fare_below_average_{tag}", weighted(every, "fare") - weighted(lv.values(), "fare"), "usd per ticket",
        f"How far the Las Vegas average fare sits below the top 1,000 average, {year} Q{q}")
    put(f"las_vegas_markets_spirit_cheapest_{tag}", sum(r["carrier_low"] == SPIRIT for r in lv.values()), "markets",
        f"Markets with Las Vegas in which Spirit had the lowest average fare, {year} Q{q}")
    put(f"las_vegas_cheapest_fare_{tag}", weighted(lv.values(), "fare_low"), "usd per ticket",
        f"Average fare of the cheapest airline in each market with Las Vegas, {year} Q{q}, weighted by passengers")
before, after = vegas(*DOT_BEFORE), vegas(*DOT_AFTER)
common = sorted(set(before) & set(after))
group = [(before[k], after[k]) for k in common if before[k]["carrier_low"] == SPIRIT and after[k]["carrier_low"] != SPIRIT]
rest = [(before[k], after[k]) for k in common if before[k]["carrier_low"] != SPIRIT]
weight = lambda pair: float(pair[1]["passengers"])
avg = lambda pairs, i: sum(float(p[i]["fare_low"]) * weight(p) for p in pairs) / sum(weight(p) for p in pairs)
(ya, qa), (yd, qd) = DOT_BEFORE, DOT_AFTER
put("markets_where_spirit_stopped_being_cheapest", len(group), "markets", f"Markets with Las Vegas in which Spirit was "
    f"the cheapest airline in {ya} Q{qa} and no longer was in {yd} Q{qd}")
for i, (y, q) in enumerate((DOT_BEFORE, DOT_AFTER)):
    put(f"those_markets_cheapest_fare_{y}q{q}", avg(group, i), "usd per ticket", f"In those markets, average fare of the "
        f"cheapest option, {y} Q{q} (weighted by {yd} Q{qd} passengers)")
    put(f"other_las_vegas_markets_cheapest_fare_{y}q{q}", avg(rest, i), "usd per ticket", f"Markets with Las Vegas in "
        f"which Spirit wasn't the cheapest in {ya} Q{qa}: average fare of the cheapest option, {y} Q{q}")
put("those_markets_cheapest_fare_change", avg(group, 1) / avg(group, 0) - 1, "share",
    "Change in the cheapest fare in the markets where Spirit stopped being the cheapest")
put("other_las_vegas_markets_cheapest_fare_change", avg(rest, 1) / avg(rest, 0) - 1, "share",
    "Change in the cheapest fare in the markets where Spirit wasn't the cheapest")
example = [p for p in group if DOT_EXAMPLE in (p[1]["city1"] + p[1]["city2"])]
check(f"DOT: one {DOT_EXAMPLE} market in the group", len(example) == 1, f"{len(example)}")
for i, (y, q) in enumerate((DOT_BEFORE, DOT_AFTER)):
    put(f"chicago_cheapest_fare_{y}q{q}", float(example[0][i]["fare_low"]), "usd per ticket",
        f"Chicago-Las Vegas, {y} Q{q}: average fare of the cheapest airline ({example[0][i]['carrier_low']})")

# ---------------------------------------------------------------- 4. Jet fuel (EIA)
for month, price in JET.items():
    put(f"jet_fuel_{month.replace('-', '_')}", price, "usd per gallon",
        f"Jet fuel, U.S. Gulf Coast, spot, average of {month}")

# ---------------------------------------------------------------- 5. The airport's documents
with open(HERE / "data" / "published_figures.csv", newline="", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        put(r["key"], float(r["value"]), r["unit"], f"{r['description']} ({r['source']})")
budget = [K["las_cpe_estimate_fy2024"], K["las_cpe_budget_fy2025"], K["las_cpe_budget_fy2026"], K["las_cpe_budget_fy2027"]]
check("The budgeted CPE rises every year from fiscal 2024 to 2027", all(b > a for a, b in zip(budget, budget[1:])),
      ", ".join(f"${x:.2f}" for x in budget))
put("las_cpe_rise_fy2024_to_fy2027", K["las_cpe_budget_fy2027"] - K["las_cpe_estimate_fy2024"],
    "usd per enplaned passenger", "Rise of the budgeted cost per enplanement from fiscal 2024 to fiscal 2027")
put("las_passengers_lost_jan_sep_2026", K["las_passengers_jan_sep_2025"] - K["las_passengers_jan_sep_2026"], "passengers",
    "Fewer passengers at LAS (arriving and departing), January to September 2026 against 2025")

(HERE / "numbers.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
print(f"{len(out)} numbers written to numbers.json")

"""Ticket Math #007 - Parking vs planes: who pays a US airport more, your car or the airlines?

Recomputes every number in the video from the files in data/ and writes numbers.json.
Standard library only, no network: run `python calc.py` in this folder.

Method
1. Groups as the FAA's CATS database labels them: the large hubs and the medium hubs that filed a Form 5100-127
   (Operating and Financial Summary) for fiscal 2025. Line definitions: FAA Advisory Circular 150/5100-19D.
2. "The car" = line 4.6, Parking and ground transportation: the airport's own parking plus the fees it charges taxis,
   ride-shares, limos and shuttles (the form reports them together). Rental cars (line 4.5) stay out.
3. "The plane", in two sizes: the passenger airlines' landing fees (line 1.1) and everything the passenger airlines
   pay the airport (line 1.6: landing fees, terminal rents, apron, federal inspection and other fees). Two stricter
   tests: line 1.6 plus cargo landing fees and cargo and hangar rentals (lines 2.1 and 2.4), and all aeronautical
   revenue (line 3.0: passenger and cargo airlines, general aviation, fuel, security reimbursements and the rest).
4. Per passenger: each line / enplanements (line 16.1: passengers who board, connecting passengers included).
5. The same counts for fiscal 2019 and 2024; Nashville's own annual report (ACFR) splits its line 4.6 in two.
"""
import csv
import json
import statistics
from pathlib import Path

HERE = Path(__file__).parent
YEAR, EARLIER = 2025, [2019, 2024]
GROUPS = {"large_hubs": "Large", "medium_hubs": "Medium"}
PARKING = "Parking and ground transportation"                    # line 4.6
LANDING = "Passenger airline landing fees"                       # line 1.1
TERMINAL = "Terminal arrival fees, rents, and utilities"         # line 1.2
AIRLINES = "Total Passenger Airline Aeronautical Revenue"        # line 1.6
RENTAL_CARS = "Rental cars-excludes customer facility charges"   # line 4.5
ENPLANEMENTS = "Enplanements"                                    # line 16.1
CARGO = ["Landing fees from cargo", "Cargo and hangar rentals"]  # lines 2.1 and 2.4
AERONAUTICAL = "Total Aeronautical Revenue"                      # line 3.0
AIRLINE_LINES = [LANDING, TERMINAL, "Terminal area apron charges/tiedowns", "Federal Inspection Fees",
                 "Other passenger aeronautical fees"]
NON_AERO_LINES = ["Land and non-terminal facility leases and revenues", "Terminal-food and beverage",
                  "Terminal-retail stores and duty free", "Terminal-services and other", RENTAL_CARS, PARKING, "Hotel",
                  "Other Non-Aeronautical Revenue"]
TOLERANCE_SUM = 0.001         # the lines of a form against the total the airport declared
TOLERANCE_PASSENGERS = 0.10   # Form 127 enplanements (fiscal year) against BTS T-100 (calendar year)
YEAR_2019_AIRPORT = "ATL"     # in 2019, Atlanta's parking almost tied everything its airlines paid
TEXT = {"year", "hub_size", "location_id", "airport_name", "state", "fiscal_year_end", "url"}
PER_PASSENGER = "usd per enplaned passenger"

with open(HERE / "data" / "form127.csv", newline="", encoding="utf-8") as f:
    forms = [{k: (x if k in TEXT else (float(x) if x != "" else None)) for k, x in r.items()} for r in csv.DictReader(f)]
with open(HERE / "data" / f"bts_t100_enplanements_{YEAR}.csv", newline="", encoding="utf-8") as f:
    t100 = {r["origin"]: float(r["passengers"]) for r in csv.DictReader(f)}
with open(HERE / "data" / f"nashville_acfr_fy{YEAR}.csv", newline="", encoding="utf-8") as f:
    acfr = {r["key"]: float(r["value"]) for r in csv.DictReader(f)}
out = {}


def v(form, column):   # an empty cell counts as zero in the sums; the checks below make sure the lines used are filled
    return form[column] or 0


def group(year, hub):
    return [r for r in forms if int(r["year"]) == year and r["hub_size"] == hub]


def put(key, value, unit, description):
    out[key] = {"value": value, "unit": unit, "description": description}


def check(label, ok, detail):
    print(f"{'ok  ' if ok else 'FAIL'} {label}: {detail}")
    if not ok:
        raise SystemExit(1)


def sums_match(label, rows, parts, total):
    wrong = [f"{r['location_id']} ({sum(v(r, c) for c in parts):,.0f} vs {v(r, total):,.0f})" for r in rows
             if abs(sum(v(r, c) for c in parts) - v(r, total)) > TOLERANCE_SUM * abs(v(r, total))]
    check(label, not wrong, "all match" if not wrong else "do not match: " + ", ".join(wrong))


winners, losers = [], []
for g, hub in GROUPS.items():
    rows = group(YEAR, hub)
    name = g.replace("_", " ")

    # 1. Checks on every form
    sums_match(f"{name} {YEAR}: the 5 passenger airline lines add up to the declared total (1.6)", rows, AIRLINE_LINES, AIRLINES)
    sums_match(f"{name} {YEAR}: the 8 non-aeronautical lines add up to the declared total (4.9)", rows, NON_AERO_LINES,
               "Total Non-Aeronautical Revenue")
    sums_match(f"{name} {YEAR}: aeronautical + non-aeronautical = operating revenue (5.0)", rows,
               [AERONAUTICAL, "Total Non-Aeronautical Revenue"], "Total Operating Revenue")
    for year in [YEAR] + EARLIER:
        ry = group(year, hub)
        empty = [r["location_id"] for r in ry
                 if any(r[c] is None for c in (PARKING, LANDING, AIRLINES, AERONAUTICAL, ENPLANEMENTS, *CARGO))
                 or not v(r, ENPLANEMENTS) > 0]
        check(f"{name} {year}: every airport has the lines used (and enplanements)", not empty,
              "all filled" if not empty else "missing: " + ", ".join(empty))
        ids = [r["location_id"] for r in ry]
        check(f"{name} {year}: one form per airport", len(ids) == len(set(ids)), f"{len(ids)} forms, {len(set(ids))} airports")
        ties = [r["location_id"] for r in ry if v(r, PARKING) in (v(r, AIRLINES), v(r, LANDING), v(r, AERONAUTICAL))]
        check(f"{name} {year}: no exact tie in the comparisons", not ties, "none" if not ties else ", ".join(ties))
    off = [f"{r['location_id']} ({v(r, ENPLANEMENTS):,.0f} vs {t100.get(r['location_id'], 0):,.0f})" for r in rows
           if not t100.get(r["location_id"]) or abs(v(r, ENPLANEMENTS) / t100[r["location_id"]] - 1) > TOLERANCE_PASSENGERS]
    gaps = [abs(v(r, ENPLANEMENTS) / t100[r["location_id"]] - 1) for r in rows if t100.get(r["location_id"])]
    check(f"{name} {YEAR}: Form 127 enplanements match BTS T-100 (calendar year)", not off,
          f"median gap {statistics.median(gaps):.1%}" if not off else "off: " + ", ".join(off))

    # 2. The group totals and the scoreboard
    total = {k: sum(v(r, c) for r in rows) for k, c in
             [("parking", PARKING), ("landing_fees", LANDING), ("terminal_rents", TERMINAL), ("airline_payments", AIRLINES),
              ("rental_cars", RENTAL_CARS), ("enplanements", ENPLANEMENTS)]}
    n = len(rows)
    beats_all = sum(v(r, PARKING) > v(r, AIRLINES) for r in rows)
    put(f"{g}_airports", n, "airports", f"{name.capitalize()} that filed a Form 127 for fiscal {YEAR}")
    put(f"{g}_parking_beats_airline_payments", beats_all, "airports",
        f"{name.capitalize()} where parking and ground transportation (4.6) beat everything passenger airlines pay (1.6)")
    put(f"{g}_parking_beats_landing_fees", sum(v(r, PARKING) > v(r, LANDING) for r in rows), "airports",
        f"{name.capitalize()} where parking and ground transportation (4.6) beat passenger airline landing fees (1.1)")
    put(f"{g}_parking_beats_airlines_plus_cargo", sum(v(r, PARKING) > v(r, AIRLINES) + sum(v(r, c) for c in CARGO) for r in rows),
        "airports", f"{name.capitalize()} where 4.6 beats 1.6 plus cargo landing fees (2.1) and cargo and hangar rentals (2.4)")
    put(f"{g}_parking_beats_all_aeronautical", sum(v(r, PARKING) > v(r, AERONAUTICAL) for r in rows), "airports",
        f"{name.capitalize()} where 4.6 beats all aeronautical revenue (3.0)")
    put(f"{g}_parking_loses_to_airline_payments", n - beats_all, "airports",
        f"{name.capitalize()} where parking and ground transportation bring in less than everything airlines pay")
    for k, desc in [("parking", "parking and ground transportation (4.6)"), ("landing_fees", "passenger airline landing fees (1.1)"),
                    ("terminal_rents", "terminal rents paid by airlines (1.2)"),
                    ("airline_payments", "everything passenger airlines pay (1.6)"),
                    ("rental_cars", "rental cars, without customer facility charges (4.5)")]:
        put(f"{g}_{k}", total[k], "usd", f"{name.capitalize()}, all {n} together: {desc}, fiscal {YEAR}")
    put(f"{g}_enplanements", total["enplanements"], "passengers", f"{name.capitalize()}, all {n} together: enplanements (16.1)")
    for k, desc in [("parking", "parking and ground transportation"), ("landing_fees", "landing fees"),
                    ("airline_payments", "everything passenger airlines pay")]:
        put(f"{g}_{k}_per_passenger", total[k] / total["enplanements"], PER_PASSENGER,
            f"{name.capitalize()}, all together: {desc} per enplaned passenger")
    put(f"{g}_landing_share_of_airline_payments", total["landing_fees"] / total["airline_payments"], "share",
        f"{name.capitalize()}, all together: landing fees as a share of everything passenger airlines pay")

    # 3. Every airport
    for r in rows:
        i, label, pax = r["location_id"].lower(), f"{r['airport_name']} ({r['location_id']})", v(r, ENPLANEMENTS)
        for k, c, desc in [("parking", PARKING, "parking and ground transportation (4.6)"),
                           ("landing_fees", LANDING, "passenger airline landing fees (1.1)"),
                           ("airline_payments", AIRLINES, "everything passenger airlines pay (1.6)")]:
            put(f"{i}_{k}", v(r, c), "usd", f"{label}: {desc}, fiscal year ending {r['fiscal_year_end']}")
            put(f"{i}_{k}_per_passenger", v(r, c) / pax, PER_PASSENGER, f"{label}: {desc} per enplaned passenger")
        put(f"{i}_enplanements", pax, "passengers", f"{label}: enplanements (16.1)")
        put(f"{i}_cargo_landing_fees", v(r, CARGO[0]), "usd", f"{label}: cargo landing fees (2.1)")
        put(f"{i}_all_aeronautical", v(r, AERONAUTICAL), "usd", f"{label}: all aeronautical revenue (3.0)")
        (winners if v(r, PARKING) > v(r, AIRLINES) else losers).append(r)

    # 4. Is it stable? The same counts in other years
    for year in EARLIER:
        ry = group(year, hub)
        put(f"{g}_airports_{year}", len(ry), "airports", f"{name.capitalize()} in the Form 127 for fiscal {year}")
        put(f"{g}_parking_beats_airline_payments_{year}", sum(v(r, PARKING) > v(r, AIRLINES) for r in ry), "airports",
            f"{name.capitalize()} where 4.6 beats 1.6, fiscal {year}")
        put(f"{g}_parking_beats_landing_fees_{year}", sum(v(r, PARKING) > v(r, LANDING) for r in ry), "airports",
            f"{name.capitalize()} where 4.6 beats 1.1, fiscal {year}")

# 5. Where the car wins: do passengers leave more at the garage, or do airlines pay less?
for k, rows, desc in [("winners", winners, "where parking beats everything airlines pay"), ("losers", losers, "where parking loses")]:
    put(f"{k}_count", len(rows), "airports", f"Large and medium hubs {desc}")
    put(f"{k}_median_parking_per_passenger", statistics.median(v(r, PARKING) / v(r, ENPLANEMENTS) for r in rows),
        PER_PASSENGER, f"Median parking and ground transportation per enplaned passenger at the airports {desc}")
    put(f"{k}_median_airline_payments_per_passenger", statistics.median(v(r, AIRLINES) / v(r, ENPLANEMENTS) for r in rows),
        PER_PASSENGER, f"Median of everything airlines pay per enplaned passenger at the airports {desc}")
check("large + medium: winners + losers = every airport in both groups",
      len(winners) + len(losers) == sum(len(group(YEAR, h)) for h in GROUPS.values()), f"{len(winners)} + {len(losers)}")

# 6. Nashville in its own annual report: does the garage alone beat the airlines?
bna = next(r for r in group(YEAR, "Large") if r["location_id"] == "BNA")
check("Nashville: parking + ground transportation in the ACFR = line 4.6 of the Form 127",
      acfr["parking"] + acfr["ground_transportation"] == v(bna, PARKING),
      f"ACFR {acfr['parking'] + acfr['ground_transportation']:,.0f}; Form 127 {v(bna, PARKING):,.0f}")
airlines_acfr = acfr["terminal_rents_airlines"] + acfr["landing_fees_airlines"]
check("Nashville: what the airlines pay in the ACFR is close to line 1.6 of the Form 127",
      abs(airlines_acfr / v(bna, AIRLINES) - 1) <= TOLERANCE_PASSENGERS, f"ACFR {airlines_acfr:,.0f}; Form 127 {v(bna, AIRLINES):,.0f}")
for k, desc in [("parking", "parking"), ("ground_transportation", "ground transportation (Uber/Lyft, taxi cab and shuttle fees)"),
                ("terminal_rents_airlines", "terminal rents and fees paid by the airlines"),
                ("landing_fees_airlines", "landing and related fees paid by the airlines")]:
    put(f"bna_acfr_{k}", acfr[k], "usd", f"Nashville ACFR, fiscal {YEAR}: {desc}")
put("bna_garage_only_per_passenger", acfr["parking"] / v(bna, ENPLANEMENTS), PER_PASSENGER,
    "Nashville: the garage alone (ACFR) per enplaned passenger (Form 127)")
put("bna_ground_transportation_per_passenger", acfr["ground_transportation"] / v(bna, ENPLANEMENTS), PER_PASSENGER,
    "Nashville: ground transportation fees alone (ACFR) per enplaned passenger")
put("bna_garage_only_minus_airline_payments", acfr["parking"] - v(bna, AIRLINES), "usd",
    "Nashville: the garage alone (ACFR) minus everything passenger airlines pay (1.6); negative = the garage loses")
put("bna_garage_only_minus_airlines_acfr", acfr["parking"] - airlines_acfr, "usd",
    "Nashville, ACFR only: the garage minus (terminal rents + landing fees paid by the airlines); negative = the garage loses")

# 7. Atlanta in 2019: the near tie
atl = next(r for r in group(EARLIER[0], "Large") if r["location_id"] == YEAR_2019_AIRPORT)
put(f"atl_parking_per_passenger_{EARLIER[0]}", v(atl, PARKING) / v(atl, ENPLANEMENTS), PER_PASSENGER,
    f"Atlanta: parking and ground transportation per enplaned passenger, fiscal {EARLIER[0]}")
put(f"atl_airline_payments_per_passenger_{EARLIER[0]}", v(atl, AIRLINES) / v(atl, ENPLANEMENTS), PER_PASSENGER,
    f"Atlanta: everything passenger airlines pay per enplaned passenger, fiscal {EARLIER[0]}")

(HERE / "numbers.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
print(f"{len(out)} numbers written to numbers.json")

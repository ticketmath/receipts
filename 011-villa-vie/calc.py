"""Ticket Math #011 - Villa Vie Odyssey: what did a day on board cost, and what did the ship cost to run?

Recomputes every number in the video from the files in data/ and writes numbers.json.
Standard library only, no network: run `python calc.py` in this folder.

Method
1. Villa Vie: what the founder, the company and the captain told the press (CBS News, Business Insider, Cruise Industry
   News, Eye of the Flyer) and what its own site advertises. Villa Vie is private and publishes no accounts, so these
   are its own words, in data/published_figures.csv.
2. The big lines: Carnival's 10-Q for June to August 2026; Royal Caribbean's and Norwegian's 10-Q and earnings release
   for July to September 2026: price per ton, tons, fuel expense, passenger cruise days, cost per berth per day.
3. The market: marine gasoil (MGO) and heavy fuel oil in Singapore, the world's largest bunkering port (Ship & Bunker).
4. Per person: tons a month / residents / days in a month, against tons and fuel expense / passenger cruise days.
5. The price of life on board: the advertised all-inclusive rent per person per day, against what Royal Caribbean and
   Norwegian spend per berth per day, the internal documents CBS reviewed, U.S. assisted living (CareScout) and the
   average Social Security benefit (SSA).
"""
import csv
import json
from pathlib import Path

HERE = Path(__file__).parent
THOUSAND, MILLION, HUNDRED = 1000, 1e6, 100
DAYS_A_MONTH = 365 / 12
TOL = 0.01              # published totals against price x tons, as in the dossier
TOL_OCCUPANCY = 0.005   # passenger cruise days / berth days against the published occupancy
TOL_BEFORE = 0.05       # Villa Vie's pre-war price against Singapore's last session before the rise
EU_ALLOWANCES = 0.15    # Carnival's fuel line includes EU emission allowances, which the per-ton price excludes


def read(name):
    with open(HERE / "data" / name, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


I = {r["key"]: float(r["value"]) for r in read("inputs.csv")}
FIGURES = read("published_figures.csv")
K = {r["key"]: float(r["value"]) for r in FIGURES}
QUOTES = {r["key"]: r["quote"] for r in read("quotes.csv")}
out = {}


def put(key, value, unit, description):
    out[key] = {"value": value, "unit": unit, "description": description}


def check(label, ok, detail):
    print(f"{'ok  ' if ok else 'FAIL'} {label}: {detail}")
    if not ok:
        raise SystemExit(1)


# 0. Every published figure, as published
for r in FIGURES:
    put(r["key"], float(r["value"]), r["unit"], f"{r['description']} ({r['source']})")

# 1. Villa Vie, in its own words
before, low, high = K["villa_vie_fuel_per_ton_before_war"], K["villa_vie_fuel_per_ton_since_war_low"], K["villa_vie_fuel_per_ton_since_war_high"]
tons_low, tons_high = K["odyssey_fuel_tons_a_month_low"], K["odyssey_fuel_tons_a_month_high"]
residents = K["residents_sent_ashore"]
put("fuel_price_rise_times", low / before, "times", "Low end of the price since the war / the price before the war")
put("residents_vs_capacity", residents / K["odyssey_passenger_capacity"], "share", "Residents at the end / the ship's passenger capacity")
put("monthly_fuel_bill_low", tons_low * low, "usd a month", "Fuel bill a month at the lowest consumption and price Villa Vie gives")
put("monthly_fuel_bill_high", tons_high * high, "usd a month", "Fuel bill a month at the highest consumption and price Villa Vie gives")
put("monthly_fuel_bill_before_war", tons_low * before, "usd a month", "Fuel bill a month before the war, at the lowest consumption")
spend = K["villa_vie_monthly_spend_after_war"]
check("the $2 million a month the founder cites fits his own consumption x price", tons_low * low <= spend <= tons_high * high,
      f"consumption x price {tons_low * low:,.0f} to {tons_high * high:,.0f}; quoted {spend:,.0f}")

# 2. The big lines, same quarter
c_price, c_price_prev = I["carnival_fuel_cost_per_ton_2026"], I["carnival_fuel_cost_per_ton_2025"]
c_pcd, c_pcd_prev = I["carnival_passenger_cruise_days_2026"], I["carnival_passenger_cruise_days_2025"]
c_albd, c_occ = I["carnival_albds_2026"], I["carnival_occupancy_2026"]
c_fuel, c_fuel_prev = I["carnival_fuel_expense_2026"], I["carnival_fuel_expense_2025"]
check("Carnival: passenger cruise days / berth days = published occupancy", abs(c_pcd / c_albd * HUNDRED - c_occ) <= TOL_OCCUPANCY * c_occ,
      f"rebuilt {c_pcd / c_albd * HUNDRED:.1f}%; published {c_occ}%")
c_tons = I["carnival_tons_per_thousand_albds_2026"] * c_albd * MILLION / THOUSAND
check("Carnival: price per ton x tons sits just below the fuel line (the gap is EU emission allowances)",
      0 <= c_fuel * MILLION - c_price * c_tons <= EU_ALLOWANCES * c_fuel * MILLION,
      f"price x tons {c_price * c_tons:,.0f}; fuel line {c_fuel * MILLION:,.0f}")
check("Carnival's 10-K: scrubbers on most ships", "Advanced Air Quality Systems" in QUOTES["scrubbers_on_most_ships"], QUOTES["scrubbers_on_most_ships"])
put("carnival_fuel_per_ton_q3_2026", c_price, "usd a ton", "Carnival: fuel cost per metric ton consumed, June to August 2026 (10-Q)")
put("carnival_fuel_per_ton_q3_2025", c_price_prev, "usd a ton", "Carnival: the same, June to August 2025 (10-Q)")
put("carnival_fuel_expense_q3_2026", c_fuel * MILLION, "usd", "Carnival: fuel expense, June to August 2026 (10-Q)")
put("carnival_net_income_q3_2026", I["carnival_net_income_2026"] * MILLION, "usd", "Carnival: net income, June to August 2026 (10-Q)")
put("carnival_net_income_q3_2025", I["carnival_net_income_2025"] * MILLION, "usd", "Carnival: net income, June to August 2025 (10-Q)")
put("carnival_higher_fuel_prices_q3_2026", I["carnival_higher_fuel_prices_2026"] * MILLION, "usd", "Carnival: what higher fuel prices added to fuel expense (10-Q)")
put("carnival_occupancy_q3_2026", c_occ / HUNDRED, "share", "Carnival: occupancy (above 100% means more than two per cabin)")
c_fuel_day = c_fuel / c_pcd
put("carnival_fuel_per_passenger_day_q3_2026", c_fuel_day, "usd per passenger a day", "Carnival: fuel expense / passenger cruise days, 2026")
put("carnival_fuel_per_passenger_day_q3_2025", c_fuel_prev / c_pcd_prev, "usd per passenger a day", "Carnival: fuel expense / passenger cruise days, 2025")
c_tons_day = c_tons / (c_pcd * MILLION)
put("carnival_fuel_kg_per_passenger_day", c_tons_day * THOUSAND, "kg per passenger a day", "Carnival: tons per thousand ALBDs x ALBDs / passenger cruise days")

r_price, r_tons = I["royal_caribbean_fuel_price_per_ton"], I["royal_caribbean_fuel_tons"]
r_fuel, r_pcd = I["royal_caribbean_fuel_expense_2026"], I["royal_caribbean_passenger_cruise_days_2026"]
check("Royal Caribbean: price x tons = fuel line", abs(r_price * r_tons - r_fuel * MILLION) <= TOL * r_fuel * MILLION,
      f"price x tons {r_price * r_tons:,.0f}; fuel line {r_fuel * MILLION:,.0f}")
put("royal_caribbean_fuel_per_ton_q3_2026", r_price, "usd a ton", "Royal Caribbean: bunker price net of hedging, July to September 2026 (8-K)")
put("royal_caribbean_hedged_share_2026", I["royal_caribbean_hedged_2026"] / HUNDRED, "share", "Royal Caribbean: share of 2026 fuel hedged, September 30, 2026 (10-Q)")
put("royal_caribbean_fuel_per_passenger_day", r_fuel * MILLION / r_pcd, "usd per passenger a day", "Royal Caribbean: fuel expense / passenger cruise days")
put("royal_caribbean_fuel_kg_per_passenger_day", r_tons / r_pcd * THOUSAND, "kg per passenger a day", "Royal Caribbean: tons / passenger cruise days")

n_price, n_tons = I["norwegian_fuel_price_per_ton_2026"], I["norwegian_fuel_tons"]
n_fuel, n_pcd = I["norwegian_fuel_expense_2026"], I["norwegian_passenger_cruise_days_2026"]
check("Norwegian: price x tons = fuel line", abs(n_price * n_tons - n_fuel * THOUSAND) <= TOL * n_fuel * THOUSAND,
      f"price x tons {n_price * n_tons:,.0f}; fuel line {n_fuel * THOUSAND:,.0f}")
put("norwegian_fuel_per_ton_q3_2026", n_price, "usd a ton", "Norwegian: fuel price per metric ton net of hedges, July to September 2026 (8-K)")
put("norwegian_fuel_per_ton_q3_2025", I["norwegian_fuel_price_per_ton_2025"], "usd a ton", "Norwegian: the same, July to September 2025 (8-K)")
put("norwegian_hedged_share_2026", I["norwegian_hedged_2026"] / HUNDRED, "share", "Norwegian: share of 2026 fuel hedged, October 15, 2026 (8-K)")
put("norwegian_hedge_price_per_ton", I["norwegian_hedge_price_per_ton_2026"], "usd a ton", "Norwegian: blended HFO and MGO hedge price for 2026 (8-K)")
put("norwegian_fuel_per_passenger_day", n_fuel * THOUSAND / n_pcd, "usd per passenger a day", "Norwegian: fuel expense / passenger cruise days")
put("norwegian_fuel_kg_per_passenger_day", n_tons / n_pcd * THOUSAND, "kg per passenger a day", "Norwegian: tons / passenger cruise days")

# 3. The price per ton
mgo_q3, hsfo_q3, mgo_q4 = K["singapore_mgo_q3_2026"], K["singapore_hsfo_q3_2026"], K["singapore_mgo_q4_2026_to_november_6"]
mgo_feb27 = K["singapore_mgo_february_27_2026"]
check("Villa Vie's pre-war price matches Singapore marine gasoil on the last session before the rise",
      abs(before - mgo_feb27) <= TOL_BEFORE * mgo_feb27, f"Villa Vie {before:,.0f}; Singapore {mgo_feb27:,.2f}")
put("villa_vie_vs_carnival_price_times", low / c_price, "times", "Low end of Villa Vie's price since the war / Carnival's price per ton")
put("villa_vie_vs_carnival_price_times_high", high / c_price, "times", "High end of Villa Vie's price / Carnival's price per ton")
put("villa_vie_vs_carnival_price_times_before_war", before / c_price_prev, "times", "Villa Vie's pre-war price / Carnival's a year earlier")
put("mgo_vs_hsfo_times_q3", mgo_q3 / hsfo_q3, "times", "Singapore marine gasoil / heavy fuel oil, third quarter of 2026")
put("mgo_vs_carnival_times_q3", mgo_q3 / c_price, "times", "Singapore marine gasoil, third quarter / Carnival's average price")
put("villa_vie_vs_singapore_mgo_times_q3", low / mgo_q3, "times", "Low end of Villa Vie's price / Singapore marine gasoil, third quarter")
put("villa_vie_vs_singapore_mgo_times_october_27", low / K["singapore_mgo_october_27_2026"], "times", "Low end of Villa Vie's price / Singapore marine gasoil, October 27")
put("villa_vie_above_singapore_mgo_per_ton_q4", low - mgo_q4, "usd a ton", "Low end of Villa Vie's price - Singapore marine gasoil, fourth quarter through November 6")


# 4. Per person: the empty ship
def per_resident_day(tons, price):
    return tons * price / residents / DAYS_A_MONTH


fuel_day = per_resident_day(tons_low, low)
put("odyssey_fuel_per_resident_day", fuel_day, "usd per resident a day", "700 tons x $2,000 / 203 residents / days in a month")
put("odyssey_fuel_per_resident_day_high", per_resident_day(tons_high, high), "usd per resident a day", "800 tons x $3,000 / 203 residents / days in a month")
put("odyssey_fuel_per_resident_day_at_singapore_price", per_resident_day(tons_low, mgo_q4), "usd per resident a day", "The same at Singapore marine gasoil, fourth quarter")
put("odyssey_fuel_per_resident_day_at_carnival_price", per_resident_day(tons_low, c_price), "usd per resident a day", "The same at Carnival's average price")
put("odyssey_fuel_per_resident_day_before_war", per_resident_day(tons_low, before), "usd per resident a day", "The same at the pre-war price")
kg_day = tons_low / residents / DAYS_A_MONTH * THOUSAND
put("odyssey_fuel_kg_per_resident_day", kg_day, "kg per resident a day", "700 tons / 203 residents / days in a month")
put("odyssey_vs_carnival_kg_times", kg_day / (c_tons_day * THOUSAND), "times", "Odyssey kg per resident / Carnival kg per passenger")
put("odyssey_vs_carnival_fuel_dollars_times", fuel_day / c_fuel_day, "times", "Odyssey fuel per resident a day / Carnival fuel per passenger a day")
put("odyssey_vs_carnival_fuel_dollars_times_same_price", per_resident_day(tons_low, c_price) / c_fuel_day, "times", "The same, if the Odyssey paid Carnival's price")
fuel_month = tons_low * low / residents
put("odyssey_fuel_per_resident_month", fuel_month, "usd per resident a month", "Monthly fuel bill (low end) / residents")
put("surcharge_share_of_fuel_bill", K["fuel_surcharge_a_month"] / fuel_month, "share", "The $1,500 surcharge / fuel per resident a month")

# 5. The price of life on board, before any war
rent = K["inside_cabin_rent_a_month"]
rent_day = rent / DAYS_A_MONTH
put("rent_per_person_day", rent_day, "usd per person a day", "Inside cabin rent per person a month / days in a month")
yld, ncc = I["royal_caribbean_net_yield_2026"], I["royal_caribbean_net_cruise_costs_per_apcd_2026"]
ncc_ex = I["royal_caribbean_net_cruise_costs_ex_fuel_per_apcd_2026"]
check("Royal Caribbean: cost ex fuel + fuel per berth day = cost with fuel",
      abs(ncc_ex + r_fuel * MILLION / I["royal_caribbean_apcd_2026"] - ncc) <= TOL * ncc,
      f"{ncc_ex} + {r_fuel * MILLION / I['royal_caribbean_apcd_2026']:.2f} against {ncc}")
put("royal_caribbean_net_yield_per_day", yld, "usd per berth a day", "Royal Caribbean: Net Yield, July to September 2026 (10-Q)")
put("royal_caribbean_net_cruise_cost_per_day", ncc, "usd per berth a day", "Royal Caribbean: Net Cruise Costs per APCD, with fuel (10-Q)")
put("royal_caribbean_net_cruise_cost_per_day_ex_fuel", ncc_ex, "usd per berth a day", "Royal Caribbean: Net Cruise Costs excluding Fuel per APCD (10-Q)")
put("royal_caribbean_gross_cruise_cost_per_day", I["royal_caribbean_gross_cruise_costs_per_apcd_2026"], "usd per berth a day", "Royal Caribbean: Gross Cruise Costs per APCD (10-Q)")
put("norwegian_net_cruise_cost_per_day", I["norwegian_net_cruise_cost_per_capacity_day"], "usd per berth a day", "Norwegian: Net Cruise Cost per Capacity Day (8-K)")
put("royal_caribbean_cost_vs_rent_times", ncc / rent_day, "times", "Royal Caribbean's cost per berth a day / Villa Vie's rent a day")
put("royal_caribbean_yield_vs_rent_times", yld / rent_day, "times", "Royal Caribbean's net yield per berth a day / Villa Vie's rent a day")
put("rent_below_royal_caribbean_cost_per_day", ncc - rent_day, "usd a day", "Royal Caribbean's cost per berth a day - Villa Vie's rent a day")
put("fuel_before_war_share_of_rent", per_resident_day(tons_low, before) / rent_day, "share", "Pre-war fuel per resident a day (203 aboard) / rent a day")
put("fuel_after_war_vs_rent_times", fuel_day / rent_day, "times", "Fuel per resident a day since the war (low end) / rent a day")
doc_cost, doc_rev, doc_cabins = K["internal_documents_cost_a_month"], K["internal_documents_full_ship_revenue_a_month"], K["internal_documents_cabins"]
put("internal_documents_monthly_gap_full_ship", doc_cost - doc_rev, "usd a month", "Internal documents: cost a month - revenue a month with the ship full")
put("cabins_with_owner_august_2026", doc_cabins - K["cabins_without_owner_august_2026"], "cabins", "Cabins in the documents - cabins with no owner")
put("internal_documents_cost_per_cabin_month", doc_cost / doc_cabins, "usd per cabin a month", "Internal documents: cost a month / cabins")
put("internal_documents_revenue_per_cabin_month", doc_rev / doc_cabins, "usd per cabin a month", "Internal documents: full-ship revenue a month / cabins")
put("internal_documents_cost_per_resident_day", doc_cost / residents / DAYS_A_MONTH, "usd per resident a day", "Internal documents: cost a month / 203 residents / days in a month")
put("residents_vs_advertised", residents / K["residents_advertised"], "share", "Residents at the end / the 650 the company advertises")
put("assisted_living_per_day", K["assisted_living_median_a_month"] / DAYS_A_MONTH, "usd a day", "Assisted living median a month / days in a month")
put("retirement_benefit_per_day", K["average_retirement_benefit_a_month"] / DAYS_A_MONTH, "usd a day", "Average retirement benefit a month / days in a month")
put("rent_vs_retirement_benefit_times", rent / K["average_retirement_benefit_a_month"], "times", "Villa Vie's rent a month / the average retirement benefit")
put("rent_vs_assisted_living", rent / K["assisted_living_median_a_month"], "share", "Villa Vie's rent a month / assisted living median a month")

(HERE / "numbers.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
print(f"{len(out)} numbers written to numbers.json")

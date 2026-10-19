"""Ticket Math #005 - Spirit filled most of its seats and still went under: what did each passenger cost?

Recomputes every number in the video from data/*.csv and writes numbers.json.
Standard library only, no network: run `python calc.py` in this folder.

Method
1. A passenger's receipt: Spirit's income statement (Form 10-K) / passenger flight segments, for 2019, 2024 and 2025.
   Cost with and without special items (special charges and loss or gain on disposal of assets). Where the change came
   from: each expense line / passengers; wages per employee and passengers per employee.
2. Load factor: Spirit's 10-K (all flights) and the BTS T-100 domestic segment data (passenger-miles / seat-miles).
3. Inflation: BLS CPI-U, annual averages for 2019 and 2024.
4. Frontier, the same ultra-low-cost model, from its 10-Ks (2019 comes from the 2021 10-K), without the sale-leaseback
   gains it books inside operating expenses.
5. 2026: Spirit's March 2026 business plan (Form 8-K, exhibit 99.1) against what it reported to the US DOT on Form 41:
   fuel cost per gallon (Schedule P-12(a)) and first-quarter results (Schedules P-1.2 and P-6).
6. After: average fares (US DOT Consumer Airfare Report, Table 1, top 1,000 city-pair markets) in Q1 2024 and Q1 2026,
   in markets Spirit left, kept and never flew nonstop (BTS T-100), weighted by Q1 2024 passengers.
"""
import csv
import json
from pathlib import Path

HERE = Path(__file__).parent
BEFORE, AFTER, LAST, FALL = 2019, 2024, 2025, 2026
LINES = ["wages", "fuel", "aircraft_rent", "airports", "depreciation", "maintenance", "distribution", "other"]
SPECIAL = ["special_encargos", "special_venda_ativos"]   # special charges; loss (gain) on disposal of assets
TOLERANCE = 0.01
MIN_MARKETS = 30


def read(name):
    with open(HERE / "data" / name, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def check(label, ok, detail):
    print(f"{'ok  ' if ok else 'FAIL'} {label}: {detail}")
    if not ok:
        raise SystemExit(1)


inputs = {(r["source"], r["key"]): float(r["value"]) for r in read("inputs.csv")}
get = lambda source, key: inputs[(source, key)]
out = {}


def put(key, value, unit, description):
    out[key] = {"value": value, "unit": unit, "description": description}


# 1. Spirit's receipt per passenger
sp = {}
for year in (BEFORE, AFTER, LAST):
    s = lambda k: get(f"spirit_10k_{year}", k)
    pax = s("passenger_segments")
    lines = sum(s(f"line_{l}") for l in LINES)
    special = sum(s(k) for k in SPECIAL)
    check(f"Spirit {year}: expense lines add up to total operating expenses", abs(lines + special - s("operating_expenses"))
          <= TOLERANCE * s("operating_expenses"), f"{(lines + special) / 1e6:,.1f} vs {s('operating_expenses') / 1e6:,.1f} million")
    d = {"pax": pax, "revenue": s("operating_revenue") / pax, "cost": s("operating_expenses") / pax,
         "cost_ex": (s("operating_expenses") - special) / pax, "special": special / pax, "load": s("load_factor"),
         "employees": s("employees"), "wages": s("line_wages")}
    sp[year] = d
    put(f"spirit_load_factor_{year}", d["load"], "share", f"Spirit load factor, {year} (10-K)")
    put(f"spirit_revenue_per_passenger_{year}", d["revenue"], "usd", f"Spirit operating revenue per passenger, {year}")
    put(f"spirit_cost_per_passenger_{year}", d["cost"], "usd", f"Spirit operating cost per passenger, {year}")
    put(f"spirit_cost_per_passenger_ex_special_{year}", d["cost_ex"], "usd",
        f"Spirit operating cost per passenger without special items, {year}")
    put(f"spirit_result_per_passenger_{year}", d["revenue"] - d["cost"], "usd", f"Spirit operating result per passenger, {year}")
    put(f"spirit_result_per_passenger_ex_special_{year}", d["revenue"] - d["cost_ex"], "usd",
        f"Spirit operating result per passenger without special items, {year}")
    put(f"spirit_passengers_{year}", pax, "passengers", f"Spirit passenger flight segments, {year}")
    put(f"spirit_daily_hours_{year}", s("daily_hours"), "hours", f"Spirit average daily aircraft utilization, {year}")
    put(f"spirit_aircraft_{year}", s("aircraft_end"), "aircraft", f"Spirit aircraft at end of {year}")
    put(f"spirit_employees_{year}", s("employees"), "employees", f"Spirit average full-time equivalent employees, {year}")

a, d = sp[BEFORE], sp[AFTER]
change = d["cost_ex"] - a["cost_ex"]
put("cost_change_ex_special", change, "usd", "Spirit cost per passenger without special items, 2024 minus 2019 (main number)")
put("cost_change", d["cost"] - a["cost"], "usd", "Spirit cost per passenger with special items, 2024 minus 2019")
put("revenue_change", d["revenue"] - a["revenue"], "usd", "Spirit revenue per passenger, 2024 minus 2019")
put("cost_change_pct", d["cost_ex"] / a["cost_ex"] - 1, "share", "Spirit cost per passenger without special items, change 2019-2024")
put("revenue_change_pct", d["revenue"] / a["revenue"] - 1, "share", "Spirit revenue per passenger, change 2019-2024")
put("load_factor_change", d["load"] - a["load"], "share", "Spirit load factor, 2024 minus 2019 (points)")
put("special_items_change", d["special"] - a["special"], "usd", "Spirit special items per passenger, 2024 minus 2019")
total = 0
for l in LINES:
    va = get(f"spirit_10k_{BEFORE}", f"line_{l}") / a["pax"]
    vd = get(f"spirit_10k_{AFTER}", f"line_{l}") / d["pax"]
    total += vd - va
    put(f"line_{l}_2019", va, "usd", f"Spirit {l} per passenger, 2019")
    put(f"line_{l}_2024", vd, "usd", f"Spirit {l} per passenger, 2024")
    put(f"line_{l}_change", vd - va, "usd", f"Spirit {l} per passenger, 2024 minus 2019")
check("the expense lines per passenger add up to the cost change", abs(total - change) <= TOLERANCE * abs(change),
      f"{total:,.2f} vs {change:,.2f}")
for year in (BEFORE, AFTER):
    s = sp[year]
    put(f"wages_per_employee_{year}", s["wages"] / s["employees"], "usd", f"Spirit wages and benefits per employee, {year}")
    put(f"passengers_per_employee_{year}", s["pax"] / s["employees"], "passengers", f"Spirit passengers per employee, {year}")
put("wages_per_employee_change", (d["wages"] / d["employees"]) / (a["wages"] / a["employees"]) - 1, "share",
    "Spirit wages and benefits per employee, change 2019-2024")
put("passengers_per_employee_change", (d["pax"] / d["employees"]) / (a["pax"] / a["employees"]) - 1, "share",
    "Spirit passengers per employee, change 2019-2024")

# 2. Domestic load factor (T-100)
t = lambda k: get("bts_t100_domestic", k)
for year in (BEFORE, AFTER):
    lf = t(f"NK_passenger_miles_{year}") / t(f"NK_seat_miles_{year}")
    check(f"Spirit {year}: 10-K load factor close to T-100 domestic", abs(lf - sp[year]["load"]) <= 0.03,
          f"{sp[year]['load']:.1%} vs {lf:.1%}")
    put(f"spirit_domestic_load_factor_{year}", lf, "share", f"Spirit domestic load factor, {year} (T-100)")
put("frontier_domestic_load_factor_2024", t("F9_passenger_miles_2024") / t("F9_seat_miles_2024"), "share",
    "Frontier domestic load factor, 2024 (T-100)")
put("southwest_domestic_load_factor_2024", t("WN_passenger_miles_2024") / t("WN_seat_miles_2024"), "share",
    "Southwest domestic load factor, 2024 (T-100)")
for month in ("march", "april"):
    put(f"spirit_domestic_load_factor_{month}_2026", t(f"NK_passenger_miles_{month}_2026") / t(f"NK_seat_miles_{month}_2026"),
        "share", f"Spirit domestic load factor, {month} 2026 (T-100)")

# 3. Inflation
inflation = get("bls_cpi_u", "cpi_average_2024") / get("bls_cpi_u", "cpi_average_2019") - 1
put("inflation", inflation, "share", "US consumer prices, 2019 to 2024 (CPI-U annual averages)")
put("revenue_below_inflation", a["revenue"] * (1 + inflation) - d["revenue"], "usd",
    "How far 2024 revenue per passenger fell short of 2019's, adjusted for inflation")
put("cost_above_inflation", d["cost_ex"] - a["cost_ex"] * (1 + inflation), "usd",
    "How far 2024 cost per passenger (without special items) rose beyond 2019's, adjusted for inflation")

# 4. Frontier
fr = {}
for year, doc in ((BEFORE, 2021), (AFTER, AFTER)):
    f = lambda k: get(f"frontier_10k_{doc}", f"{k}_{year}")
    pax = f("passengers")
    fr[year] = {"revenue": f("operating_revenue") / pax, "cost": f("operating_expenses") / pax,
                "cost_ex": (f("operating_expenses") + f("sale_leaseback_gains")) / pax}
    put(f"frontier_load_factor_{year}", f("load_factor"), "share", f"Frontier load factor, {year} (10-K)")
    put(f"frontier_revenue_per_passenger_{year}", fr[year]["revenue"], "usd", f"Frontier revenue per passenger, {year}")
    put(f"frontier_cost_per_passenger_{year}", fr[year]["cost"], "usd", f"Frontier cost per passenger, {year}")
    put(f"frontier_cost_per_passenger_ex_gains_{year}", fr[year]["cost_ex"], "usd",
        f"Frontier cost per passenger without sale-leaseback gains, {year}")
    put(f"frontier_result_per_passenger_ex_gains_{year}", fr[year]["revenue"] - fr[year]["cost_ex"], "usd",
        f"Frontier operating result per passenger without sale-leaseback gains, {year}")
fr_change = fr[AFTER]["cost_ex"] - fr[BEFORE]["cost_ex"]
put("frontier_cost_change_ex_gains", fr_change, "usd", "Frontier cost per passenger without gains, 2024 minus 2019")
put("frontier_cost_change", fr[AFTER]["cost"] - fr[BEFORE]["cost"], "usd", "Frontier cost per passenger, 2024 minus 2019")
put("frontier_revenue_change", fr[AFTER]["revenue"] - fr[BEFORE]["revenue"], "usd", "Frontier revenue per passenger, 2024 minus 2019")
put("spirit_vs_frontier", change / fr_change, "times", "Spirit's cost increase per passenger / Frontier's")

# 5. 2026: plan against actual
p = lambda k: get("spirit_8k_2026_03_16", f"plan_{k}")
put("plan_fuel_per_gallon_q1", p("fuel_per_gallon_q1"), "usd", "March 2026 plan: fuel cost per gallon, Q1 2026")
put("plan_fuel_per_gallon_q2", p("fuel_per_gallon_q2"), "usd", "March 2026 plan: fuel cost per gallon, Q2 2026")
put("plan_fuel_per_gallon_year", p("fuel_per_gallon_year"), "usd", "March 2026 plan: fuel cost per gallon, 2026")
put("plan_operating_income_q1", p("operating_income_q1"), "usd", "March 2026 plan: operating income, Q1 2026")
put("plan_operating_income_q2", p("operating_income_q2"), "usd", "March 2026 plan: operating income, Q2 2026")
put("plan_revenue_q1", p("revenue_q1"), "usd", "March 2026 plan: revenue, Q1 2026")
fuel = lambda kind, m: get("bts_form41_p12a", f"NK_fuel_{kind}_2026_{m:02d}")
per_gallon = {m: fuel("cost", m) / fuel("gallons", m) for m in (1, 3, 4)}
put("fuel_per_gallon_january_2026", per_gallon[1], "usd", "Spirit fuel cost per gallon, January 2026 (Form 41)")
put("fuel_per_gallon_march_2026", per_gallon[3], "usd", "Spirit fuel cost per gallon, March 2026 (Form 41)")
put("fuel_per_gallon_april_2026", per_gallon[4], "usd", "Spirit fuel cost per gallon, April 2026 (Form 41)")
put("april_fuel_vs_plan", per_gallon[4] / p("fuel_per_gallon_q2"), "times", "April 2026 fuel per gallon / plan for Q2")
over_april = fuel("cost", 4) - fuel("gallons", 4) * p("fuel_per_gallon_q2")
over = (fuel("cost", 3) - fuel("gallons", 3) * p("fuel_per_gallon_q1")) + over_april
put("fuel_above_plan_march_april", over, "usd", "Fuel cost above the plan's price, March and April 2026")
pax_month = lambda m: get("bts_t100_all", f"NK_passengers_2026_{m:02d}")
over_pax = over_april / pax_month(4)
put("fuel_above_plan_per_passenger_april", over_pax, "usd", "Fuel cost above the plan's price per passenger, April 2026")
put("fuel_above_plan_vs_2019_profit", over_pax / (a["revenue"] - a["cost_ex"]), "times",
    "April 2026 extra fuel per passenger / 2019 profit per passenger")
f41 = lambda k: get("bts_form41_p12", f"NK_{k}_q1_2026")
fuel_q1 = get("bts_form41_p6", "NK_aircraft_fuel_q1_2026")
pax_q1 = sum(pax_month(m) for m in (1, 2, 3))
put("q1_2026_revenue", f41("op_revenues"), "usd", "Spirit revenue, Q1 2026 (Form 41)")
put("q1_2026_operating_result", f41("op_profit_loss"), "usd", "Spirit operating result, Q1 2026 (Form 41)")
put("q1_2026_result_per_passenger", f41("op_profit_loss") / pax_q1, "usd", "Spirit operating result per passenger, Q1 2026")
put("q1_2026_margin", f41("op_profit_loss") / f41("op_revenues"), "share", "Spirit operating margin, Q1 2026")
put("plan_margin_q1", p("operating_income_q1") / p("revenue_q1"), "share", "March 2026 plan: operating margin, Q1 2026")
short = p("revenue_q1") - f41("op_revenues")
fuel_over = fuel_q1 - p("fuel_q1")
other_over = (f41("op_expenses") - fuel_q1) - (p("operating_expenses_q1") - p("fuel_q1"))
gap = p("operating_income_q1") - f41("op_profit_loss")
check("Q1 2026: revenue short + fuel over + other costs over = gap against the plan", abs(short + fuel_over + other_over - gap)
      <= TOLERANCE * abs(gap), f"{(short + fuel_over + other_over) / 1e6:,.1f} vs {gap / 1e6:,.1f} million")
put("q1_2026_gap_vs_plan", gap, "usd", "Q1 2026 operating result below the plan")
put("q1_2026_revenue_short", short, "usd", "Q1 2026 revenue below the plan")
put("q1_2026_fuel_over", fuel_over, "usd", "Q1 2026 fuel above the plan")
put("q1_2026_other_over", other_over, "usd", "Q1 2026 other costs above the plan")
put("q1_2026_fuel_share_of_gap", fuel_over / gap, "share", "Share of the Q1 2026 gap that came from fuel")
put("frontier_operating_result_2025", get("bts_form41_p12", "F9_op_profit_loss_2025"), "usd", "Frontier operating result, 2025 (Form 41)")
put("frontier_operating_result_q1_2026", get("bts_form41_p12", "F9_op_profit_loss_q1_2026"), "usd",
    "Frontier operating result, Q1 2026 (Form 41)")
put("spirit_cash_end_2025", get(f"spirit_10k_{LAST}", "cash_end"), "usd", "Spirit cash and cash equivalents, end of 2025")

# JetBlue
put("jetblue_breakup_fee", get(f"spirit_10k_{AFTER}", "jetblue_breakup_fee"), "usd", "What JetBlue paid Spirit when the deal ended")
put("jetblue_deal_value", get("spirit_8k_2022_07_28", "jetblue_deal_value"), "usd", "JetBlue's July 2022 deal for Spirit (equity value)")
jb = {y: get("jetblue_10k", f"jetblue_net_income_{y}") for y in range(2020, LAST + 1)}
put("jetblue_net_loss_2024", -jb[AFTER], "usd", "JetBlue net loss, 2024")
put("jetblue_loss_years", sum(1 for v in jb.values() if v < 0), "years", "JetBlue years with a net loss, 2020-2025")

# 6. Fares where Spirit left
cut = get("assumption", "min_route_passengers")
put("min_route_passengers", cut, "passengers", "Assumption: nonstop Spirit passengers per quarter to count a market as served")
markets = read("markets_q1.csv")
groups = {"left": [], "stayed": [], "never": []}
for m in markets:
    pa, pb = float(m["spirit_nonstop_passengers_q1_2024"]), float(m["spirit_nonstop_passengers_q1_2026"])
    if pa > 0 and pa >= cut and pb == 0:
        groups["left"].append(m)
    elif pa > 0 and pb > 0 and pa >= cut and pb >= cut:
        groups["stayed"].append(m)
    elif pa == 0 and pb == 0:
        groups["never"].append(m)


def fare(ms, column):   # weighted by Q1 2024 passengers in both years
    w = sum(float(m["passengers_q1_2024"]) for m in ms)
    return sum(float(m[column]) * float(m["passengers_q1_2024"]) for m in ms) / w


change_by = {}
for name, ms in groups.items():
    check(f"fares: group '{name}' has enough markets", len(ms) >= MIN_MARKETS, f"{len(ms)} markets")
    fa, fb = fare(ms, "fare_q1_2024"), fare(ms, "fare_q1_2026")
    change_by[name] = fb / fa - 1
    put(f"markets_{name}", len(ms), "markets", f"Top-1,000 markets where Spirit {name} (Q1 2024 to Q1 2026)")
    put(f"fare_{name}_2024", fa, "usd", f"Average fare, markets where Spirit {name}, Q1 2024")
    put(f"fare_{name}_2026", fb, "usd", f"Average fare, markets where Spirit {name}, Q1 2026 (Q1 2024 weights)")
    put(f"fare_{name}_change", change_by[name], "share", f"Average fare change, markets where Spirit {name}")
put("fare_left_excess", change_by["left"] - change_by["never"], "share",
    "Extra fare increase where Spirit left, against markets it never flew (points)")
cheap = read("cheapest_q1_2026.csv")
w = sum(float(m["passengers"]) for m in cheap)
t_nk = sum(float(m["fare_low"]) * float(m["passengers"]) for m in cheap) / w
t_lg = sum(float(m["fare_lg"]) * float(m["passengers"]) for m in cheap) / w
put("markets_spirit_cheapest", len(cheap), "markets", "Markets where Spirit had the lowest fare and another airline the largest share, Q1 2026")
put("fare_spirit_cheapest", t_nk, "usd", "Spirit's average fare in those markets, Q1 2026")
put("fare_largest_airline", t_lg, "usd", "Largest airline's average fare in those markets, Q1 2026")
put("spirit_discount", 1 - t_nk / t_lg, "share", "How much cheaper Spirit was than the largest airline in those markets")

(HERE / "numbers.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
print(f"{len(out)} numbers written to numbers.json")

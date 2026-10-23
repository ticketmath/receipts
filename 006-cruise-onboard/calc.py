"""Ticket Math #006 - The fare is the bait: what a cruise line earns after you board.

Recomputes every number in the video from data/inputs.csv and writes numbers.json.
Standard library only, no network: run `python calc.py` in this folder.

Method
1. The receipt per passenger day: each line of the 2025 income statement (Form 10-K) / passenger cruise days (one
   passenger on board for one day, the unit the companies report themselves), for Carnival, Royal Caribbean and Norwegian.
2. Onboard margin = "onboard and other" revenue - "onboard and other" cost (the direct cost of what was sold on board).
   The fare alone = operating income - onboard margin: what would be left without the extras.
3. 2019 against 2025, in dollars of each year and after inflation (BLS CPI-U annual averages). Carnival's 2019 report
   does not publish passenger cruise days: they come from available lower berth days x occupancy, Carnival's own
   definition.
4. Viking (Form 20-F 2025), which sells almost everything inside the fare, as a contrast.
5. Prices on the companies' official pages (October 2026) and the CLIA count of the world's ocean cruise passengers.
"""
import csv
import json
from pathlib import Path

HERE = Path(__file__).parent
YEAR, BEFORE = 2025, 2019
BIG_THREE = ["carnival", "royal_caribbean", "norwegian"]
NAMES = {"carnival": "Carnival", "royal_caribbean": "Royal Caribbean", "norwegian": "Norwegian", "viking": "Viking"}
LINES = ["passenger_ticket_revenue", "onboard_and_other_revenue", "total_revenue", "onboard_and_other_cost",
         "commissions_transportation_other", "payroll", "fuel", "food", "other_operating", "selling_admin", "depreciation",
         "operating_income", "interest_expense", "income_before_tax", "income_tax", "net_income"]
EXPENSES = ["commissions_transportation_other", "onboard_and_other_cost", "payroll", "fuel", "food", "other_operating",
            "selling_admin", "depreciation"]
SHIP = ["payroll", "fuel", "food", "other_operating", "selling_admin", "depreciation"]   # the cost of running the ship
CARNIVAL_LINES = {"commissions_transportation_other": "commissions", "payroll": "payroll", "fuel": "fuel", "food": "food",
                  "other_operating": "other_ship_operating", "selling_admin": "selling_admin", "depreciation": "depreciation"}
TOLERANCE = 0.001             # lines against the published total in the same table (rounding)
TOLERANCE_OCCUPANCY = 0.005   # passenger days / capacity against the published occupancy
TOLERANCE_TEXT = 0.005        # a rounded percentage in the 10-K text against the computed one
PER_DAY = "usd per passenger per day"

with open(HERE / "data" / "inputs.csv", newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))
inputs = {(r["source"], r["key"]): float(r["value"]) for r in rows}
get = lambda source, key: inputs[(source, key)]
out = {}


def put(key, value, unit, description):
    out[key] = {"value": value, "unit": unit, "description": description}


def check(label, ok, detail):
    print(f"{'ok  ' if ok else 'FAIL'} {label}: {detail}")
    if not ok:
        raise SystemExit(1)


def same(label, published, rebuilt, tolerance=TOLERANCE):
    check(label, abs(rebuilt - published) <= tolerance * abs(published), f"published {published:,.0f}; rebuilt {rebuilt:,.0f}")


def occupancy_check(name, days, capacity, occupancy):
    check(f"{name}: passenger days / capacity = published occupancy", abs(days / capacity - occupancy) <= TOLERANCE_OCCUPANCY,
          f"published {occupancy:.1%}; rebuilt {days / capacity:.1%}")


# 1 and 2. The big three in 2025: the receipt per passenger day, and the fare without the onboard margin
G = {}
for c in BIG_THREE:
    src, n = f"{c}_10k_{YEAR}", NAMES[c]
    v = {k: get(src, k) for k in LINES}
    days, pax = get(src, "passenger_cruise_days"), get(src, "passengers_carried")
    occupancy_check(f"{n} {YEAR}", days, get(src, "capacity_days"), get(src, "occupancy"))
    same(f"{n} {YEAR}: ticket + onboard = total revenue", v["total_revenue"],
         v["passenger_ticket_revenue"] + v["onboard_and_other_revenue"])
    same(f"{n} {YEAR}: revenue - expenses = operating income", v["operating_income"],
         v["total_revenue"] - sum(v[k] for k in EXPENSES))
    same(f"{n} {YEAR}: income before tax + tax = net income", v["net_income"], v["income_before_tax"] + v["income_tax"])
    same(f"{n} {YEAR}: operating income in the 10-K text = SEC XBRL", get("sec_xbrl", f"{c}_operating_income_{YEAR}"),
         v["operating_income"])
    G[c] = (v, days, pax)
    margin = v["onboard_and_other_revenue"] - v["onboard_and_other_cost"]
    p = f"{c}_"
    put(p + f"passengers_{YEAR}", pax, "passengers", f"{n}: passengers carried, {YEAR}")
    put(p + f"passenger_days_{YEAR}", days, "passenger days", f"{n}: passenger cruise days, {YEAR} (one passenger on board for one day)")
    put(p + f"occupancy_{YEAR}", get(src, "occupancy"), "share", f"{n}: occupancy, {YEAR} (the industry counts two people per cabin)")
    put(p + f"average_cruise_days_{YEAR}", days / pax, "days", f"{n}: average cruise length, {YEAR}")
    put(p + f"ticket_per_day_{YEAR}", v["passenger_ticket_revenue"] / days, PER_DAY, f"{n}: passenger ticket revenue per passenger day, {YEAR}")
    put(p + f"onboard_per_day_{YEAR}", v["onboard_and_other_revenue"] / days, PER_DAY, f"{n}: onboard and other revenue per passenger day, {YEAR}")
    put(p + f"onboard_cost_per_day_{YEAR}", v["onboard_and_other_cost"] / days, PER_DAY,
        f"{n}: direct cost of what was sold on board, per passenger day, {YEAR}")
    put(p + f"onboard_margin_per_day_{YEAR}", margin / days, PER_DAY, f"{n}: onboard margin per passenger day, {YEAR}")
    put(p + f"operating_income_per_day_{YEAR}", v["operating_income"] / days, PER_DAY, f"{n}: operating income per passenger day, {YEAR}")
    put(p + f"net_income_per_day_{YEAR}", v["net_income"] / days, PER_DAY, f"{n}: net income per passenger day, {YEAR}")
    put(p + f"interest_per_day_{YEAR}", -v["interest_expense"] / days, PER_DAY, f"{n}: interest on debt per passenger day, {YEAR}")
    put(p + f"ticket_alone_operating_result_per_day_{YEAR}", (v["operating_income"] - margin) / days, PER_DAY,
        f"{n}: operating result per passenger day without the onboard margin (the fare alone), {YEAR}")
    if margin > v["operating_income"]:
        put(p + f"ticket_alone_loss_per_day_{YEAR}", (margin - v["operating_income"]) / days, PER_DAY,
            f"{n}: what the fare alone lost per passenger day, {YEAR} (operating loss, before interest and taxes)")
    put(p + f"ticket_alone_net_result_per_day_{YEAR}", (v["net_income"] - margin) / days, PER_DAY,
        f"{n}: net result per passenger day without the onboard margin, {YEAR}")
    put(p + f"onboard_margin_{YEAR}", margin, "usd", f"{n}: onboard margin, {YEAR}")
    put(p + f"operating_income_{YEAR}", v["operating_income"], "usd", f"{n}: operating income, {YEAR}")
    put(p + f"net_income_{YEAR}", v["net_income"], "usd", f"{n}: net income, {YEAR}")
    put(p + f"ticket_alone_operating_result_{YEAR}", v["operating_income"] - margin, "usd",
        f"{n}: operating income without the onboard margin, {YEAR}")
    put(p + f"ticket_alone_net_result_{YEAR}", v["net_income"] - margin, "usd", f"{n}: net income without the onboard margin, {YEAR}")
    put(p + f"onboard_margin_vs_operating_income_{YEAR}", margin / v["operating_income"], "share",
        f"{n}: onboard margin as a share of operating income, {YEAR}")
    put(p + f"onboard_share_of_revenue_{YEAR}", v["onboard_and_other_revenue"] / v["total_revenue"], "share",
        f"{n}: onboard share of total revenue, {YEAR}")
    put(p + f"onboard_vs_ticket_{YEAR}", v["onboard_and_other_revenue"] / v["passenger_ticket_revenue"], "share",
        f"{n}: onboard revenue as a share of ticket revenue, {YEAR}")
    put(p + f"onboard_per_passenger_per_cruise_{YEAR}", v["onboard_and_other_revenue"] / pax, "usd per passenger per cruise",
        f"{n}: onboard revenue per passenger, per cruise, {YEAR}")
    put(p + f"income_tax_rate_{YEAR}", -v["income_tax"] / v["income_before_tax"], "share",
        f"{n}: income tax / income before tax, {YEAR}")

# Carnival's receipt for the fare, line by line
v, days, _ = G["carnival"]
for line, name in CARNIVAL_LINES.items():
    put(f"carnival_{name}_per_day_{YEAR}", v[line] / days, PER_DAY, f"Carnival: {line.replace('_', ' ')} per passenger day, {YEAR}")
ship = sum(v[k] for k in SHIP)
put(f"carnival_ship_cost_per_day_{YEAR}", ship / days, PER_DAY,
    f"Carnival: cost of the ship per passenger day, {YEAR} (payroll, fuel, food, other operating, selling and administrative, "
    "depreciation)")
put(f"carnival_net_ticket_per_day_{YEAR}", (v["passenger_ticket_revenue"] - v["commissions_transportation_other"]) / days, PER_DAY,
    f"Carnival: ticket revenue minus commissions, transportation and other, per passenger day, {YEAR}")
same("Carnival: net ticket - ship cost = operating income without the onboard margin",
     v["operating_income"] - (v["onboard_and_other_revenue"] - v["onboard_and_other_cost"]),
     v["passenger_ticket_revenue"] - v["commissions_transportation_other"] - ship)

# The three together
total = lambda k: sum(G[c][0][k] for c in BIG_THREE)
days3 = sum(G[c][1] for c in BIG_THREE)
pax3 = sum(G[c][2] for c in BIG_THREE)
margin3 = total("onboard_and_other_revenue") - total("onboard_and_other_cost")
put(f"big_three_onboard_per_day_{YEAR}", total("onboard_and_other_revenue") / days3, PER_DAY,
    f"The big three together: onboard revenue per passenger day, {YEAR}")
put(f"big_three_onboard_margin_per_day_{YEAR}", margin3 / days3, PER_DAY, f"The big three together: onboard margin per passenger day, {YEAR}")
put(f"big_three_operating_income_per_day_{YEAR}", total("operating_income") / days3, PER_DAY,
    f"The big three together: operating income per passenger day, {YEAR}")
put(f"big_three_net_income_per_day_{YEAR}", total("net_income") / days3, PER_DAY, f"The big three together: net income per passenger day, {YEAR}")
put(f"big_three_onboard_margin_vs_operating_income_{YEAR}", margin3 / total("operating_income"), "share",
    f"The big three together: onboard margin as a share of operating income, {YEAR}")
put(f"big_three_passengers_{YEAR}", pax3, "passengers", f"The big three together: passengers carried, {YEAR}")
clia = get("clia", f"clia_world_ocean_passengers_{YEAR}")
put(f"clia_world_ocean_passengers_{YEAR}", clia, "passengers", f"CLIA: ocean cruise passengers worldwide, {YEAR}")
put(f"big_three_share_of_world_passengers_{YEAR}", pax3 / clia, "share",
    f"The big three's passengers as a share of the world's ocean cruise passengers (CLIA), {YEAR}")

# 3. 2019 against 2025, with inflation
for year in (BEFORE, YEAR):
    months = get("bls_cpi_u", f"cpi_months_{year}")
    check(f"BLS {year}: months in the annual average", months == 12 or (year == YEAR and months == 11),
          f"{months:.0f}" + (" (October 2025 was not collected during the government shutdown)" if months < 12 else ""))
inflation = get("bls_cpi_u", f"cpi_average_{YEAR}") / get("bls_cpi_u", f"cpi_average_{BEFORE}") - 1
put(f"inflation_{BEFORE}_{YEAR}", inflation, "share", f"US consumer prices, {BEFORE} to {YEAR} (CPI-U annual averages)")
for c in BIG_THREE:
    src, n = f"{c}_10k_{BEFORE}", NAMES[c]
    a = {k: get(src, k) for k in ("passenger_ticket_revenue", "onboard_and_other_revenue", "onboard_and_other_cost", "operating_income")}
    if c == "carnival":
        # in 2019 Carnival reported land packages apart ("tour and other"): they count in total revenue, but leave both
        # sides of the comparison between the fare and the cost of the ship
        a["total_revenue"] = a["passenger_ticket_revenue"] + a["onboard_and_other_revenue"] + get(src, "tour_and_other_revenue")
        tour_cost = get(src, "tour_and_other_cost")
        days_a = get(src, "available_lower_berth_days") * get(src, "occupancy")
    else:
        a["total_revenue"] = get(src, "total_revenue")
        same(f"{n} {BEFORE}: ticket + onboard = total revenue", a["total_revenue"],
             a["passenger_ticket_revenue"] + a["onboard_and_other_revenue"])
        tour_cost = 0
        days_a = get(src, "passenger_cruise_days")
        occupancy_check(f"{n} {BEFORE}", days_a, get(src, "capacity_days"), get(src, "occupancy"))
    same(f"{n} {BEFORE}: operating income in the 10-K = SEC XBRL", get("sec_xbrl", f"{c}_operating_income_{BEFORE}"),
         a["operating_income"])
    margin = a["onboard_and_other_revenue"] - a["onboard_and_other_cost"]
    d, days_d, _ = G[c]
    ta, oa = a["passenger_ticket_revenue"] / days_a, a["onboard_and_other_revenue"] / days_a
    td, od = d["passenger_ticket_revenue"] / days_d, d["onboard_and_other_revenue"] / days_d
    p = f"{c}_"
    put(p + f"ticket_per_day_{BEFORE}", ta, PER_DAY, f"{n}: passenger ticket revenue per passenger day, {BEFORE}")
    put(p + f"onboard_per_day_{BEFORE}", oa, PER_DAY, f"{n}: onboard and other revenue per passenger day, {BEFORE}")
    put(p + f"onboard_margin_vs_operating_income_{BEFORE}", margin / a["operating_income"], "share",
        f"{n}: onboard margin as a share of operating income, {BEFORE}")
    put(p + f"ticket_alone_operating_result_{BEFORE}", a["operating_income"] - margin, "usd",
        f"{n}: operating income without the onboard margin, {BEFORE}")
    put(p + f"onboard_share_of_revenue_{BEFORE}", a["onboard_and_other_revenue"] / a["total_revenue"], "share",
        f"{n}: onboard share of total revenue, {BEFORE}")
    put(p + "ticket_per_day_change_nominal", td / ta - 1, "share", f"{n}: ticket revenue per passenger day, {BEFORE} to {YEAR} (dollars of each year)")
    put(p + "onboard_per_day_change_nominal", od / oa - 1, "share", f"{n}: onboard revenue per passenger day, {BEFORE} to {YEAR} (dollars of each year)")
    put(p + "ticket_per_day_change_real", td / (ta * (1 + inflation)) - 1, "share",
        f"{n}: ticket revenue per passenger day, {BEFORE} to {YEAR}, after inflation")
    put(p + "onboard_per_day_change_real", od / (oa * (1 + inflation)) - 1, "share",
        f"{n}: onboard revenue per passenger day, {BEFORE} to {YEAR}, after inflation")
    # where the turn came from: every other cost (all but the cost of what was sold on board) per passenger day
    ra = (a["total_revenue"] - a["operating_income"] - a["onboard_and_other_cost"] - tour_cost) / days_a
    rd = (d["total_revenue"] - d["operating_income"] - d["onboard_and_other_cost"]) / days_d
    put(p + f"cost_ex_onboard_per_day_{BEFORE}", ra, PER_DAY, f"{n}: cost per passenger day without the onboard cost, {BEFORE}")
    put(p + f"cost_ex_onboard_per_day_{YEAR}", rd, PER_DAY, f"{n}: cost per passenger day without the onboard cost, {YEAR}")
    put(p + "cost_ex_onboard_per_day_change_real", rd / (ra * (1 + inflation)) - 1, "share",
        f"{n}: that cost per passenger day, {BEFORE} to {YEAR}, after inflation")
    put(p + f"ticket_minus_cost_per_day_{BEFORE}", ta - ra, PER_DAY,
        f"{n}: ticket per passenger day minus that cost, {BEFORE} (what the fare alone left)")
    if ra > ta:
        put(p + f"ticket_alone_loss_per_day_{BEFORE}", ra - ta, PER_DAY, f"{n}: what the fare alone lost per passenger day, {BEFORE}")

# 4. Viking: almost everything included
src = f"viking_20f_{YEAR}"
vk = {k: get(src, k) for k in ("passenger_ticket_revenue", "onboard_and_other_revenue", "total_revenue",
                               "cruise_operating_expenses", "other_operating_expenses", "operating_income")}
same(f"Viking {YEAR}: cruise and land + onboard = total revenue", vk["total_revenue"],
     vk["passenger_ticket_revenue"] + vk["onboard_and_other_revenue"])
same(f"Viking {YEAR}: revenue - expenses = operating income", vk["operating_income"],
     vk["total_revenue"] + vk["cruise_operating_expenses"] + vk["other_operating_expenses"])
days_v = get(src, "passenger_cruise_days")
occupancy_check(f"Viking {YEAR}", days_v, get(src, "capacity_days"), get(src, "occupancy"))
put(f"viking_passengers_{YEAR}", get(src, "passengers_carried"), "passengers", f"Viking: passengers, {YEAR} (ocean and river)")
put(f"viking_onboard_share_of_revenue_{YEAR}", vk["onboard_and_other_revenue"] / vk["total_revenue"], "share",
    f"Viking: onboard share of total revenue, {YEAR}")
put(f"viking_ticket_per_day_{YEAR}", vk["passenger_ticket_revenue"] / days_v, PER_DAY,
    f"Viking: cruise and land revenue per passenger day, {YEAR}")
put(f"viking_onboard_per_day_{YEAR}", vk["onboard_and_other_revenue"] / days_v, PER_DAY, f"Viking: onboard revenue per passenger day, {YEAR}")
put(f"viking_operating_income_per_day_{YEAR}", vk["operating_income"] / days_v, PER_DAY,
    f"Viking: operating income per passenger day, {YEAR}")

# 5. Support from the 10-K text
cs = f"carnival_10k_{YEAR}"
put(f"carnival_onboard_share_north_america_{YEAR}", get(cs, "onboard_share_north_america"), "share",
    f"Carnival: onboard share of North America segment revenue, {YEAR} (10-K text, rounded)")
put(f"carnival_onboard_share_europe_{YEAR}", get(cs, "onboard_share_europe"), "share",
    f"Carnival: onboard share of Europe segment revenue, {YEAR} (10-K text, rounded)")
v, days, _ = G["carnival"]
share = v["onboard_and_other_revenue"] / v["total_revenue"]
check(f"Carnival {YEAR}: computed onboard share = the 10-K text", abs(share - get(cs, "onboard_share_total_text")) <= TOLERANCE_TEXT,
      f"text {get(cs, 'onboard_share_total_text'):.0%}; computed {share:.1%}")
rs = f"royal_caribbean_10k_{YEAR}"
port = get(rs, "port_charges_in_ticket_revenue")
put(f"royal_caribbean_port_charges_in_ticket_{YEAR}", port, "usd",
    f"Royal Caribbean: port costs charged to guests inside ticket revenue, {YEAR} (10-K, rounded)")
put(f"royal_caribbean_port_charges_per_day_{YEAR}", port / G["royal_caribbean"][1], PER_DAY,
    f"Royal Caribbean: port costs inside the ticket, per passenger day, {YEAR}")
vr = G["royal_caribbean"][0]
share = vr["onboard_and_other_revenue"] / vr["total_revenue"]
check(f"Royal Caribbean {YEAR}: computed onboard share = the 10-K percentage table",
      abs(share - get(rs, "onboard_share_table")) <= TOLERANCE_TEXT, f"table {get(rs, 'onboard_share_table'):.1%}; computed {share:.1%}")
check(f"Norwegian {YEAR}: the 10-K books service charges inside ticket revenue",
      get(f"norwegian_10k_{YEAR}", "ticket_revenue_includes_service_charges") == 1, "quoted in data/inputs.csv")

# 6. Prices passengers see on board (official pages) and what the averages look like next to them
for r in rows:   # published values, used as they are: the description is the row's label or quote
    if r["source"] in ("published_price", "royal_caribbean_results_release") or r["key"] == "carnival_celebration_key_guests":
        put(r["key"], float(r["value"]), r["unit"], r["label_or_quote"])
price = lambda k: get("published_price", f"price_{k}")
onboard_day = v["onboard_and_other_revenue"] / days
put(f"carnival_onboard_per_day_vs_cheers_{YEAR}", onboard_day / price("carnival_cheers_onboard"), "share",
    f"Carnival: average onboard spending per passenger day, {YEAR}, as a share of a day of the CHEERS! drinks package bought on board")
put(f"carnival_onboard_per_day_in_beers_{YEAR}", onboard_day / price("carnival_beer"), "beers a day",
    f"Carnival: average onboard spending per passenger day, {YEAR}, in single beers at the lowest listed price")
put(f"carnival_gratuity_vs_operating_income_per_day_{YEAR}", price("carnival_gratuity") / (v["operating_income"] / days), "share",
    f"Carnival: the recommended daily gratuity as a share of operating income per passenger day, {YEAR}")
vn, days_n, _ = G["norwegian"]
put(f"norwegian_service_charge_vs_ticket_per_day_{YEAR}", price("norwegian_service_charge") / (vn["passenger_ticket_revenue"] / days_n),
    "share", f"Norwegian: the standard daily service charge as a share of ticket revenue per passenger day, {YEAR}")

(HERE / "numbers.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
print(f"{len(out)} numbers written to numbers.json")

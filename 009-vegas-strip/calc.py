"""Ticket Math #009 - The Las Vegas Strip: how much profit is left from each night a room has a guest?

Recomputes every number in the video from the files in data/ and writes numbers.json.
Standard library only, no network: run `python calc.py` in this folder.

Method
1. Nevada Gaming Control Board, Gaming Abstract, group "Clark County - Las Vegas Strip Area, Gaming Revenue of
   $1,000,000 and over". Fiscal years run July to June (fiscal 2025 = July 2024 to June 2025). Revenue by department,
   complimentaries (contra revenue), expenses, interest, net income before federal income taxes and rooms occupied.
2. Per occupied room night = the year's figure / the rooms occupied in the year (the same denominator as the abstract's
   "Per Room Per Day Statistics", checked against them).
3. The series: fiscal 2022 to 2025, with 2019 as the pre-pandemic reference (2018 and 2020 only in the caveats: a loss
   and a one-time gain). Payroll = the four payroll lines (taxes, employee benefits, officers, other employees) of the
   five departments and of general and administrative. Operating cost = cost of sales + departmental expenses.
4. Inflation: BLS CPI-U (all items, U.S. city average), average of the 12 months of each fiscal year.
5. Visitors: LVCVA (calendar years). The Culinary Union raises: Nevada Current.
The abstract PDFs have no machine-readable tables: the lines in data/gaming_abstract.csv were read from them. The checks
below re-add the lines to the totals each abstract publishes, so a typo in one line would stop the script.
"""
import csv
import json
from pathlib import Path

HERE = Path(__file__).parent
SERIES = (2019, 2022, 2023, 2024, 2025)   # 2019 = pre-pandemic reference; 2022 to 2025 = the series
DEPARTMENTS = ("casino", "rooms", "food", "beverage", "other_income")
PAYROLL = ("payroll_taxes", "payroll_employee_benefits", "payroll_officers", "payroll_other_employees")
DEPT_ITEMS = ("bad_debt_expense", *PAYROLL, "other_departmental_expenses")
CASINO_ITEMS = ("bad_debt_expense", "commissions", "gaming_taxes_and_licenses", "preferred_guest_expenses", *PAYROLL,
                "race_wire_fees", "other_departmental_expenses")
GAMES = ("casino_table_games", "casino_slot_machines", "casino_card_games", "casino_race_book", "casino_sports_book")
REVENUE_LINES = ("gaming_revenue", "rooms_revenue", "food_revenue", "beverage_revenue", "other_revenue")
MONTHS = 12
TOL_CENT = 0.01            # the abstract's per-room statistics are published with 2 decimals
TOL_OCCUPANCY = 0.001      # occupancy published with 1 decimal
TOL_OCCUPANCY_2019 = 0.005 # fiscal 2019 occupancy published with no decimal (92%)
TOL_RATIO = 0.0001         # the complimentary ratio, published with 2 decimals in %
TOL_PRESS = 0.0005         # % changes in press coverage, published with 1 decimal
TOL_LVCVA = 0.10           # LVCVA Strip gaming revenue: calendar year, rounded, against the fiscal-year abstract

with open(HERE / "data" / "gaming_abstract.csv", newline="", encoding="utf-8") as f:
    abstract = list(csv.DictReader(f))
with open(HERE / "data" / "published_figures.csv", newline="", encoding="utf-8") as f:
    published = list(csv.DictReader(f))
with open(HERE / "data" / "bls_cpi_u_monthly.csv", newline="", encoding="utf-8") as f:
    cpi_months = {}
    for r in csv.DictReader(f):
        cpi_months.setdefault(int(r["fiscal_year"]), []).append(float(r["value"]))
NG = {(int(r["fiscal_year"]), r["line"]): float(r["value"]) for r in abstract}
K = {r["key"]: float(r["value"]) for r in published}
out = {}


def put(key, value, unit, description):
    out[key] = {"value": value, "unit": unit, "description": description}


def check(label, ok, detail):
    print(f"{'ok  ' if ok else 'FAIL'} {label}: {detail}")
    if not ok:
        raise SystemExit(1)


def g(year, line):
    return NG[(year, line)]


def change(after, before):
    return after / before - 1


for r in abstract:
    put(f"fy{r['fiscal_year']}_{r['line']}", float(r["value"]), r["unit"],
        f"Gaming Abstract, fiscal {r['fiscal_year']}: {r['description']} (see data/gaming_abstract.csv)")
for r in published:
    put(r["key"], float(r["value"]), r["unit"], f"{r['description']} (see data/published_figures.csv)")

# 1. The lines add up to what each abstract publishes
for y in (2025, 2019):
    total = sum(g(y, x) for x in REVENUE_LINES)
    check(f"fiscal {y}: gaming + rooms + food + beverage + other = total revenue", total == g(y, "total_revenue"),
          f"{total:.0f} vs {g(y, 'total_revenue'):.0f}")
    net = g(y, "departmental_income") - g(y, "total_general_and_administrative")
    check(f"fiscal {y}: departmental income - general and administrative = net income", net ==
          g(y, "net_income_before_federal_income_taxes"), f"{net:.0f} vs {g(y, 'net_income_before_federal_income_taxes'):.0f}")
    rooms = g(y, "rooms_room_sales") + g(y, "rooms_complimentary_room_sales") - g(y, "rooms_contra_revenue")
    check(f"fiscal {y}: paid rooms + complimentary rooms - contra = rooms revenue", rooms == g(y, "rooms_revenue"),
          f"{rooms:.0f} vs {g(y, 'rooms_revenue'):.0f}")
    rate = (g(y, "rooms_room_sales") + g(y, "rooms_complimentary_room_sales")) / g(y, "rooms_occupied")
    check(f"fiscal {y}: (paid + complimentary rooms) / rooms occupied = published average room rate",
          abs(rate - g(y, "average_room_rate_per_day")) <= TOL_CENT, f"{rate:.4f} vs {g(y, 'average_room_rate_per_day')}")
    occ = g(y, "rooms_occupied") / g(y, "rooms_available")
    check(f"fiscal {y}: rooms occupied / rooms available = published occupancy",
          abs(occ - g(y, "occupancy_rate")) <= (TOL_OCCUPANCY if y == 2025 else TOL_OCCUPANCY_2019),
          f"{occ:.4f} vs {g(y, 'occupancy_rate')}")
occ24 = g(2024, "rooms_occupied") / g(2024, "rooms_available")
check("fiscal 2024: rooms occupied / rooms available = published occupancy",
      abs(occ24 - g(2024, "occupancy_rate")) <= TOL_OCCUPANCY, f"{occ24:.4f} vs {g(2024, 'occupancy_rate')}")
occ25 = g(2025, "rooms_occupied") / g(2025, "rooms_available")
check("fiscal 2024 to 2025: fewer rooms available and occupied, occupancy slightly higher (the Mirage closed in July 2024)",
      g(2025, "rooms_available") < g(2024, "rooms_available") and g(2025, "rooms_occupied") < g(2024, "rooms_occupied")
      and g(2025, "occupancy_rate") > g(2024, "occupancy_rate") and occ25 > occ24,
      f"available {g(2024, 'rooms_available'):.0f} -> {g(2025, 'rooms_available'):.0f}; occupancy {occ24:.4f} -> {occ25:.4f}")
gross = sum(g(2025, x) for x in GAMES)
check("fiscal 2025: casino win before comps - casino contra revenue = gaming revenue",
      gross - g(2025, "casino_contra_revenue") == g(2025, "gaming_revenue"),
      f"{gross - g(2025, 'casino_contra_revenue'):.0f} vs {g(2025, 'gaming_revenue'):.0f}")
for dept, line in (("food", "food"), ("beverage", "beverage"), ("other_income", "other")):
    sales = "other_income_sales" if dept == "other_income" else f"{dept}_sales"
    rev = g(2025, sales) + g(2025, f"{dept}_complimentary_{'items' if dept == 'other_income' else 'sales'}") \
        - g(2025, f"{dept}_contra_revenue")
    check(f"fiscal 2025: {dept} paid + complimentary - contra = {line} revenue", rev == g(2025, f"{line}_revenue"),
          f"{rev:.0f} vs {g(2025, f'{line}_revenue'):.0f}")
contra = sum(g(2025, f"{d}_contra_revenue") for d in DEPARTMENTS)
check("fiscal 2025: all contra revenue / casino win before comps = published complimentary ratio",
      abs(contra / gross - g(2025, "contra_revenue_to_gaming_revenue")) <= TOL_RATIO,
      f"{contra / gross:.5f} vs {g(2025, 'contra_revenue_to_gaming_revenue')}")
for game, stat in (("casino_table_games", "table_revenue_per_room_per_day"),
                   ("casino_slot_machines", "slot_revenue_per_room_per_day")):
    per_room = g(2025, game) / g(2025, "rooms_occupied")
    check(f"fiscal 2025: {game} / rooms occupied = published per-room statistic",
          abs(per_room - g(2025, stat)) <= TOL_CENT, f"{per_room:.4f} vs {g(2025, stat)}")
check("LVCVA (calendar 2025, gross, rounded) vs the abstract (fiscal 2025, casino win before comps): same size",
      abs(K["lvcva_strip_gaming_revenue_2025"] / gross - 1) <= TOL_LVCVA,
      f"{K['lvcva_strip_gaming_revenue_2025']:.0f} vs {gross:.0f}")

# 2. The receipt of one occupied room night, fiscal 2019 and 2025
NIGHT_LINES = {"revenue": ("total_revenue",), "gaming": ("gaming_revenue",), "rooms": ("rooms_revenue",),
               "food_and_beverage": ("food_revenue", "beverage_revenue"), "other": ("other_revenue",),
               "interest": ("interest_expense",), "other_ga": ("other_general_and_administrative",),
               "profit": ("net_income_before_federal_income_taxes",), "casino_comps": ("casino_contra_revenue",)}
for y in (2025, 2019):
    nights = g(y, "rooms_occupied")
    for name, lines in NIGHT_LINES.items():
        put(f"{name}_per_night_fy{y}", sum(g(y, x) for x in lines) / nights, "usd per occupied room night",
            f"Fiscal {y}: {' + '.join(lines)} / rooms occupied" + (" (THE MAIN NUMBER)" if (name, y) == ("profit", 2025) else ""))
    put(f"profit_before_interest_per_night_fy{y}",
        (g(y, "net_income_before_federal_income_taxes") + g(y, "interest_expense")) / nights,
        "usd per occupied room night", f"Fiscal {y}: (net income + interest expense) / rooms occupied")
    for name, line in (("gaming", "gaming_revenue"), ("rooms", "rooms_revenue"),
                       ("profit", "net_income_before_federal_income_taxes")):
        put(f"{name}_share_of_revenue_fy{y}", g(y, line) / g(y, "total_revenue"), "share",
            f"Fiscal {y}: {line} as a share of total revenue")
    put(f"paid_rooms_per_night_fy{y}", g(y, "rooms_room_sales") / nights, "usd per occupied room night",
        f"Fiscal {y}: room sales (paid rooms only) / rooms occupied")
    put(f"comp_rooms_per_night_fy{y}", g(y, "rooms_complimentary_room_sales") / nights, "usd per occupied room night",
        f"Fiscal {y}: rooms given to players, at list price / rooms occupied")
    put(f"casino_comps_share_of_casino_win_fy{y}",
        g(y, "casino_contra_revenue") / (g(y, "gaming_revenue") + g(y, "casino_contra_revenue")), "share",
        f"Fiscal {y}: the casino's complimentaries as a share of what it won before them")
paid = sum(g(2025, x) for x in ("rooms_room_sales", "food_sales", "beverage_sales", "other_income_sales"))
put("gaming_before_comps_per_night_fy2025", gross / g(2025, "rooms_occupied"), "usd per occupied room night",
    "Fiscal 2025: what the casino won on tables, slots, cards and books before comps / rooms occupied")
put("gaming_before_comps_share_fy2025", gross / (gross + paid), "share",
    "Fiscal 2025, the count most favorable to gaming: casino win before comps / (that + what guests and customers paid "
    "for rooms, food, beverage and other)")
put("interest_per_dollar_of_profit_fy2025",
    g(2025, "interest_expense") / g(2025, "net_income_before_federal_income_taxes"), "dollars",
    "Fiscal 2025: interest paid for every dollar of net income")

# 3. 2019 against 2025, also in today's dollars
cpi = {}
for y in SERIES:
    check(f"BLS: 12 months of CPI-U in fiscal {y}", len(cpi_months[y]) == MONTHS, f"{len(cpi_months[y])} months")
    cpi[y] = sum(cpi_months[y]) / len(cpi_months[y])
inflation = cpi[2025] / cpi[2019]
put("inflation_fy2019_to_fy2025", inflation - 1, "share", "CPI-U, fiscal 2025 average / fiscal 2019 average - 1")
for name in ("revenue", "gaming", "rooms", "profit", "profit_before_interest", "interest"):
    before, after = out[f"{name}_per_night_fy2019"]["value"], out[f"{name}_per_night_fy2025"]["value"]
    put(f"{name}_per_night_fy2019_in_fy2025_dollars", before * inflation, "usd per occupied room night",
        f"Fiscal 2019 {name} per night in fiscal 2025 dollars (CPI-U)")
    put(f"{name}_per_night_real_change_fy2019_to_fy2025", after / (before * inflation) - 1, "share",
        f"Real change in {name} per night, fiscal 2019 to fiscal 2025")
for key, (a, b) in {"visitors_change_2019_to_2025": ("lvcva_visitors_2019", "lvcva_visitors_2025"),
                    "visitors_change_2024_to_2025": ("lvcva_visitors_2024", "lvcva_visitors_2025"),
                    "visitors_change_jan_sep_2025_to_2026": ("lvcva_visitors_jan_sep_2025", "lvcva_visitors_jan_sep_2026"),
                    "strip_gaming_revenue_change_jan_sep_2025_to_2026": ("lvcva_strip_gaming_revenue_jan_sep_2025",
                                                                         "lvcva_strip_gaming_revenue_jan_sep_2026"),
                    "visitors_who_gambled_change_2021_to_2025": ("lvcva_visitors_who_gambled_2021",
                                                                 "lvcva_visitors_who_gambled_2025")}.items():
    put(key, change(K[b], K[a]), "share", f"{b} / {a} - 1")
for key, line in (("revenue", "total_revenue"), ("profit", "net_income_before_federal_income_taxes"),
                  ("rooms_occupied", "rooms_occupied")):
    put(f"{key}_change_fy2019_to_fy2025", change(g(2025, line), g(2019, line)), "share", f"{line}, fiscal 2019 to 2025")

# 4. The series: what ate the profit
for y in SERIES:
    if y in (2022, 2023, 2024):
        total = sum(g(y, x) for x in REVENUE_LINES)
        check(f"fiscal {y}: gaming + rooms + food + beverage + other = total revenue", total == g(y, "total_revenue"),
              f"{total:.0f} vs {g(y, 'total_revenue'):.0f}")
        net = g(y, "departmental_income") - g(y, "total_general_and_administrative")
        check(f"fiscal {y}: departmental income - general and administrative = net income",
              net == g(y, "net_income_before_federal_income_taxes"),
              f"{net:.0f} vs {g(y, 'net_income_before_federal_income_taxes'):.0f}")
    income = g(y, "total_revenue") - g(y, "cost_of_sales") - g(y, "departmental_expenses")
    check(f"fiscal {y}: revenue - cost of sales - departmental expenses = departmental income",
          income == g(y, "departmental_income"), f"{income:.0f} vs {g(y, 'departmental_income'):.0f}")
    for d in DEPARTMENTS:
        items = sum(g(y, f"{d}_{i}") for i in (CASINO_ITEMS if d == "casino" else DEPT_ITEMS))
        check(f"fiscal {y}: {d} expense lines = {d} total departmental expenses",
              items == g(y, f"{d}_total_departmental_expenses"), f"{items:.0f} vs {g(y, f'{d}_total_departmental_expenses'):.0f}")
    depts = sum(g(y, f"{d}_total_departmental_expenses") for d in DEPARTMENTS)
    check(f"fiscal {y}: the five departments = published departmental expenses", depts == g(y, "departmental_expenses"),
          f"{depts:.0f} vs {g(y, 'departmental_expenses'):.0f}")
    nights = g(y, "rooms_occupied")
    payroll = sum(g(y, f"{d}_{p}") for d in DEPARTMENTS for p in PAYROLL) + sum(g(y, f"ga_{p}") for p in PAYROLL)
    put(f"payroll_per_night_fy{y}", payroll / nights, "usd per occupied room night",
        f"Fiscal {y}: payroll (taxes, benefits, officers, other employees) of the five departments and of general and "
        "administrative / rooms occupied")
    put(f"operating_cost_per_night_fy{y}", (g(y, "cost_of_sales") + g(y, "departmental_expenses")) / nights,
        "usd per occupied room night", f"Fiscal {y}: (cost of sales + departmental expenses) / rooms occupied")
    put(f"total_cost_per_night_fy{y}", (g(y, "total_revenue") - g(y, "net_income_before_federal_income_taxes")) / nights,
        "usd per occupied room night", f"Fiscal {y}: everything that went out (revenue - net income) / rooms occupied")
    if y in (2022, 2023, 2024):
        for name in ("revenue", "profit", "interest", "other_ga", "gaming", "rooms"):
            put(f"{name}_per_night_fy{y}", sum(g(y, x) for x in NIGHT_LINES[name]) / nights, "usd per occupied room night",
                f"Fiscal {y}: {' + '.join(NIGHT_LINES[name])} / rooms occupied")
for y in (2018, 2020):
    net = g(y, "departmental_income") - g(y, "total_general_and_administrative")
    check(f"fiscal {y}: departmental income - general and administrative = net income",
          net == g(y, "net_income_before_federal_income_taxes"), f"{net:.0f} vs {g(y, 'net_income_before_federal_income_taxes'):.0f}")
p25, p24, p23 = (g(y, "net_income_before_federal_income_taxes") for y in (2025, 2024, 2023))
check("Nevada Gaming Control Board press release: Strip net income -81.2% from fiscal 2024",
      abs(change(p25, p24) - K["ngcb_strip_profit_change_fy2024_to_fy2025"]) <= TOL_PRESS, f"{change(p25, p24):.4f}")
check("CDC Gaming Reports: Strip net income -40.4% in fiscal 2024",
      abs(change(p24, p23) - K["cdc_strip_profit_change_fy2023_to_fy2024"]) <= TOL_PRESS, f"{change(p24, p23):.4f}")

inflation22 = cpi[2025] / cpi[2022]
put("inflation_fy2022_to_fy2025", inflation22 - 1, "share", "CPI-U, fiscal 2025 average / fiscal 2022 average - 1")
for name in ("revenue", "operating_cost", "payroll", "interest", "other_ga", "profit", "total_cost"):
    before, after = out[f"{name}_per_night_fy2022"]["value"], out[f"{name}_per_night_fy2025"]["value"]
    put(f"{name}_per_night_difference_fy2022_to_fy2025", after - before, "usd per occupied room night",
        f"{name} per night, fiscal 2025 minus fiscal 2022 (dollars of each year)")
    put(f"{name}_per_night_change_fy2022_to_fy2025", after / before - 1, "share",
        f"{name} per night, fiscal 2022 to fiscal 2025 (dollars of each year)")
    put(f"{name}_per_night_fy2022_in_fy2025_dollars", before * inflation22, "usd per occupied room night",
        f"Fiscal 2022 {name} per night in fiscal 2025 dollars (CPI-U)")
    put(f"{name}_per_night_real_change_fy2022_to_fy2025", after / (before * inflation22) - 1, "share",
        f"Real change in {name} per night, fiscal 2022 to fiscal 2025")
cost_rise = out["total_cost_per_night_difference_fy2022_to_fy2025"]["value"]
for name in ("payroll", "interest", "other_ga"):
    put(f"{name}_share_of_cost_increase", out[f"{name}_per_night_difference_fy2022_to_fy2025"]["value"] / cost_rise,
        "share", f"Part of the rise in everything that went out per night (fiscal 2022 to 2025) that came from {name}")
put("payroll_share_of_new_revenue", out["payroll_per_night_difference_fy2022_to_fy2025"]["value"]
    / out["revenue_per_night_difference_fy2022_to_fy2025"]["value"], "share",
    "Rise in payroll per night as a share of the rise in revenue per night, fiscal 2022 to 2025")
for key, (a, b, line) in {"rooms_occupied_change_fy2022_to_fy2024": (2022, 2024, "rooms_occupied"),
                          "rooms_occupied_change_fy2022_to_fy2025": (2022, 2025, "rooms_occupied"),
                          "rooms_occupied_change_fy2024_to_fy2025": (2024, 2025, "rooms_occupied"),
                          "rooms_available_change_fy2024_to_fy2025": (2024, 2025, "rooms_available"),
                          "employees_change_fy2022_to_fy2025": (2022, 2025, "average_number_of_employees"),
                          "profit_change_fy2022_to_fy2024": (2022, 2024, "net_income_before_federal_income_taxes"),
                          "profit_change_fy2022_to_fy2025": (2022, 2025, "net_income_before_federal_income_taxes"),
                          "revenue_change_fy2022_to_fy2024": (2022, 2024, "total_revenue")}.items():
    put(key, change(g(b, line), g(a, line)), "share", f"{line}, fiscal {a} to {b}")
put("visitors_change_2022_to_2024", change(K["lvcva_visitors_2024"], K["lvcva_visitors_2022"]), "share",
    "lvcva_visitors_2024 / lvcva_visitors_2022 - 1")
check("from 2022 to 2024 the resorts filled more rooms and profit per night fell",
      out["rooms_occupied_change_fy2022_to_fy2024"]["value"] > 0
      and out["profit_per_night_fy2024"]["value"] < out["profit_per_night_fy2022"]["value"],
      f"rooms {out['rooms_occupied_change_fy2022_to_fy2024']['value']:+.4f}; profit per night "
      f"{out['profit_per_night_fy2022']['value']:.2f} -> {out['profit_per_night_fy2024']['value']:.2f}")
check("from 2022 to 2025, operating cost, interest and other G&A per night grew faster than revenue per night",
      all(out[f"{n}_per_night_change_fy2022_to_fy2025"]["value"] > out["revenue_per_night_change_fy2022_to_fy2025"]["value"]
          for n in ("operating_cost", "interest", "other_ga")),
      ", ".join(f"{n} {out[f'{n}_per_night_change_fy2022_to_fy2025']['value']:+.3f}"
                for n in ("revenue", "operating_cost", "interest", "other_ga")))

(HERE / "numbers.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
print(f"{len(out)} numbers written to numbers.json")

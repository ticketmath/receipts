"""Ticket Math #012 - Laughlin's casinos: where did the profit from each night with a guest go?

Recomputes every number in the video from the files in data/ and writes numbers.json.
Standard library only, no network: run `python calc.py` in this folder.

Method
1. Nevada Gaming Control Board, Gaming Abstract, group "Clark County - Laughlin Area, Gaming Revenue of $1,000,000 and
   over", fiscal 2019 to 2025. Fiscal years run July to June (fiscal 2025 = July 2024 to June 2025). Revenue by
   department, departmental income, the 17 general and administrative lines, net income before federal income taxes,
   occupancy, the rooms department, employees and long-term debt from the balance sheet.
2. Per occupied room night = the year's figure / the rooms occupied in the year (the same denominator as the abstract's
   "Per Room Per Day Statistics", checked against its published average room rate).
3. Inflation: BLS CPI-U (all items, U.S. city average), average of the 12 months of each fiscal year.
4. The building sales: VICI Properties (Harrah's Laughlin, closed July 20, 2020), GLPI (Tropicana Laughlin, October 1,
   2018) and Caesars' 2020 Form 10-K (the VICI and GLPI leases booked as financing obligations, with interest expense).
The abstract PDFs have no machine-readable tables: the lines in data/gaming_abstract.csv were read from them. The checks
below re-add the lines to the totals each abstract publishes, so a typo in one line would stop the script.
"""
import csv
import json
from pathlib import Path

HERE = Path(__file__).parent
YEARS = (2019, 2020, 2021, 2022, 2023, 2024, 2025)
REVENUE_LINES = ("gaming_revenue", "rooms_revenue", "food_revenue", "beverage_revenue", "other_revenue")
GA_LINES = ("ga_advertising_and_promotion", "ga_bad_debt_expense", "ga_depreciation_buildings",
            "ga_depreciation_and_amortization_other", "ga_energy_expense", "ga_equipment_rental_or_lease",
            "interest_expense", "ga_music_and_entertainment", "ga_payroll_taxes", "ga_payroll_employee_benefits",
            "ga_payroll_officers", "ga_payroll_other_employees", "rent_of_premises", "ga_taxes_real_estate",
            "ga_taxes_and_licenses_other", "ga_utilities", "other_general_and_administrative")
# per occupied room night: name -> abstract lines added together
PER_NIGHT = {"revenue": ("total_revenue",), "departmental_income": ("departmental_income",),
             "operating_cost": ("cost_of_sales", "departmental_expenses"), "interest": ("interest_expense",),
             "other_ga": ("other_general_and_administrative",),
             "depreciation": ("ga_depreciation_buildings", "ga_depreciation_and_amortization_other"),
             "profit": ("net_income_before_federal_income_taxes",), "gaming": ("gaming_revenue",),
             "rooms": ("rooms_revenue",),
             "profit_before_interest": ("net_income_before_federal_income_taxes", "interest_expense")}
MONTHS = 12
TOL_OCCUPANCY = 0.001   # occupancy published with 1 decimal in %
TOL_CENT = 0.01         # per-room statistics published with 2 decimals
TOL_LVCVA = 0.0005      # LVCVA changes published with 1 decimal in %
TOL_PRESS = 0.0005      # the board's press release, 1 decimal in %

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
    return value


def check(label, ok, detail):
    print(f"{'ok  ' if ok else 'FAIL'} {label}: {detail}")
    if not ok:
        raise SystemExit(1)


def g(year, line):
    return NG[(year, line)]


for r in abstract:
    put(f"fy{r['fiscal_year']}_{r['line']}", float(r["value"]), r["unit"],
        f"Gaming Abstract, fiscal {r['fiscal_year']}: {r['description']} (see data/gaming_abstract.csv)")
for r in published:
    put(r["key"], float(r["value"]), r["unit"], f"{r['description']} (see data/published_figures.csv)")

# 1. The lines add up to what each abstract publishes
for y in YEARS:
    total = sum(g(y, x) for x in REVENUE_LINES)
    check(f"fiscal {y}: gaming + rooms + food + beverage + other = total revenue", total == g(y, "total_revenue"),
          f"{total:.0f} vs {g(y, 'total_revenue'):.0f}")
    margin = g(y, "total_revenue") - g(y, "cost_of_sales")
    check(f"fiscal {y}: revenue - cost of sales = gross margin", margin == g(y, "gross_margin"),
          f"{margin:.0f} vs {g(y, 'gross_margin'):.0f}")
    dept = g(y, "gross_margin") - g(y, "departmental_expenses")
    check(f"fiscal {y}: gross margin - departmental expenses = departmental income", dept == g(y, "departmental_income"),
          f"{dept:.0f} vs {g(y, 'departmental_income'):.0f}")
    ga = sum(g(y, x) for x in GA_LINES)
    check(f"fiscal {y}: the 17 general and administrative lines = their published total",
          ga == g(y, "total_general_and_administrative"), f"{ga:.0f} vs {g(y, 'total_general_and_administrative'):.0f}")
    net = g(y, "departmental_income") - g(y, "total_general_and_administrative")
    check(f"fiscal {y}: departmental income - general and administrative = net income",
          net == g(y, "net_income_before_federal_income_taxes"),
          f"{net:.0f} vs {g(y, 'net_income_before_federal_income_taxes'):.0f}")
    occ = g(y, "rooms_occupied") / g(y, "rooms_available")
    check(f"fiscal {y}: rooms occupied / available = published occupancy",
          abs(occ - g(y, "occupancy_rate")) <= TOL_OCCUPANCY, f"{occ:.4f} vs {g(y, 'occupancy_rate')}")
    rooms = g(y, "rooms_room_sales") + g(y, "rooms_complimentary_room_sales") - g(y, "rooms_contra_revenue")
    check(f"fiscal {y}: paid rooms + complimentary rooms - contra = rooms revenue", rooms == g(y, "rooms_revenue"),
          f"{rooms:.0f} vs {g(y, 'rooms_revenue'):.0f}")
    rate = (g(y, "rooms_room_sales") + g(y, "rooms_complimentary_room_sales")) / g(y, "rooms_occupied")
    check(f"fiscal {y}: (paid + complimentary rooms) / rooms occupied = published average room rate",
          abs(rate - g(y, "average_room_rate_per_day")) <= TOL_CENT, f"{rate:.4f} vs {g(y, 'average_room_rate_per_day')}")

# 2. One night with a guest, year by year
for y in YEARS:
    nights = g(y, "rooms_occupied")
    for name, lines in PER_NIGHT.items():
        put(f"{name}_per_night_fy{y}", sum(g(y, x) for x in lines) / nights, "usd per occupied room night",
            f"Fiscal {y}: {' + '.join(lines)} / rooms occupied")
    put(f"comp_rooms_share_of_room_value_fy{y}", g(y, "rooms_complimentary_room_sales")
        / (g(y, "rooms_room_sales") + g(y, "rooms_complimentary_room_sales")), "share",
        f"Fiscal {y}: rooms given to players (list price) as a share of all room value")
    put(f"interest_share_of_departmental_income_fy{y}", g(y, "interest_expense") / g(y, "departmental_income"), "share",
        f"Fiscal {y}: interest as a share of departmental income")


def v(key):
    return out[key]["value"]


# 3. 2019 against 2025, 2022 against 2025 and the jumps in between
for key, (a, b) in {"rooms_occupied_change_fy2019_to_fy2025": ("fy2019_rooms_occupied", "fy2025_rooms_occupied"),
                    "rooms_available_change_fy2019_to_fy2025": ("fy2019_rooms_available", "fy2025_rooms_available"),
                    "rooms_occupied_change_fy2022_to_fy2025": ("fy2022_rooms_occupied", "fy2025_rooms_occupied"),
                    "departmental_income_change_fy2019_to_fy2025": ("fy2019_departmental_income", "fy2025_departmental_income"),
                    "revenue_change_fy2019_to_fy2025": ("fy2019_total_revenue", "fy2025_total_revenue"),
                    "interest_change_fy2019_to_fy2025": ("fy2019_interest_expense", "fy2025_interest_expense"),
                    "interest_change_fy2020_to_fy2021": ("fy2020_interest_expense", "fy2021_interest_expense"),
                    "long_term_debt_change_fy2020_to_fy2021": ("fy2020_total_long_term_debt", "fy2021_total_long_term_debt"),
                    "other_ga_change_fy2024_to_fy2025": ("fy2024_other_general_and_administrative",
                                                         "fy2025_other_general_and_administrative"),
                    "employees_change_fy2019_to_fy2025": ("fy2019_average_number_of_employees",
                                                          "fy2025_average_number_of_employees"),
                    "average_room_rate_change_fy2019_to_fy2025": ("fy2019_average_room_rate_per_day",
                                                                  "fy2025_average_room_rate_per_day"),
                    "slot_revenue_per_room_change_fy2019_to_fy2025": ("fy2019_slot_revenue_per_room_per_day",
                                                                      "fy2025_slot_revenue_per_room_per_day")}.items():
    put(key, v(b) / v(a) - 1, "share", f"{b} / {a} - 1")
for key, (a, b) in {"profit_difference_fy2019_to_fy2025": ("fy2019_net_income_before_federal_income_taxes",
                                                          "fy2025_net_income_before_federal_income_taxes"),
                    "interest_difference_fy2019_to_fy2025": ("fy2019_interest_expense", "fy2025_interest_expense"),
                    "other_ga_difference_fy2019_to_fy2025": ("fy2019_other_general_and_administrative",
                                                             "fy2025_other_general_and_administrative"),
                    "departmental_income_difference_fy2019_to_fy2025": ("fy2019_departmental_income",
                                                                        "fy2025_departmental_income"),
                    "profit_difference_fy2022_to_fy2025": ("fy2022_net_income_before_federal_income_taxes",
                                                          "fy2025_net_income_before_federal_income_taxes"),
                    "interest_difference_fy2022_to_fy2025": ("fy2022_interest_expense", "fy2025_interest_expense"),
                    "other_ga_difference_fy2022_to_fy2025": ("fy2022_other_general_and_administrative",
                                                             "fy2025_other_general_and_administrative"),
                    "departmental_income_difference_fy2022_to_fy2025": ("fy2022_departmental_income",
                                                                        "fy2025_departmental_income"),
                    "other_ga_difference_fy2024_to_fy2025": ("fy2024_other_general_and_administrative",
                                                             "fy2025_other_general_and_administrative"),
                    "interest_difference_fy2020_to_fy2021": ("fy2020_interest_expense", "fy2021_interest_expense"),
                    "contracts_debt_difference_fy2020_to_fy2021": ("fy2020_long_term_debt_contracts",
                                                                   "fy2021_long_term_debt_contracts")}.items():
    put(key, v(b) - v(a), "usd", f"{b} - {a}")
drop = -v("profit_difference_fy2019_to_fy2025")
for name, key in (("interest", "interest_difference_fy2019_to_fy2025"), ("other_ga", "other_ga_difference_fy2019_to_fy2025")):
    put(f"{name}_share_of_profit_drop", v(key) / drop, "share", f"{key} / (profit 2019 - profit 2025)")
for name in ("revenue", "departmental_income", "interest", "profit"):
    put(f"{name}_per_night_difference_fy2019_to_fy2025", v(f"{name}_per_night_fy2025") - v(f"{name}_per_night_fy2019"),
        "usd per occupied room night", f"{name} per night, fiscal 2025 - fiscal 2019 (dollars of each year)")
put("loss_per_night_fy2025", -v("profit_per_night_fy2025"), "usd per occupied room night",
    "Fiscal 2025: loss per occupied room night (profit per night with the sign flipped)")
put("rest_of_ga_per_night_fy2025", (g(2025, "total_general_and_administrative") - g(2025, "interest_expense")
                                    - g(2025, "other_general_and_administrative")) / g(2025, "rooms_occupied"),
    "usd per occupied room night", "Fiscal 2025: general and administrative minus interest and minus 'other G&A', per "
    "occupied room night (depreciation, office payroll, advertising, taxes, energy, rent and the rest)")
closes = v("departmental_income_per_night_fy2025") - v("interest_per_night_fy2025") - v("rest_of_ga_per_night_fy2025") \
    - v("other_ga_per_night_fy2025")
check("fiscal 2025: departmental income - interest - rest of G&A - other G&A = profit per night",
      abs(closes - v("profit_per_night_fy2025")) <= TOL_CENT, f"{closes:.4f} vs {v('profit_per_night_fy2025'):.4f}")
put("loss_fy2025", -g(2025, "net_income_before_federal_income_taxes"), "usd",
    "Fiscal 2025: the Laughlin casinos' loss for the year (net income with the sign flipped)")

# 4. In today's money (CPI-U, fiscal-year average)
cpi = {}
for y, values in cpi_months.items():
    check(f"BLS: {MONTHS} months of CPI-U in fiscal {y}", len(values) == MONTHS, f"{len(values)}")
    cpi[y] = sum(values) / len(values)
for y in (2019, 2022):
    infl = cpi[2025] / cpi[y]
    put(f"inflation_fy{y}_to_fy2025", infl - 1, "share", f"Average CPI-U, fiscal 2025 / fiscal {y} - 1")
    put(f"departmental_income_fy{y}_in_fy2025_dollars", g(y, "departmental_income") * infl, "usd",
        f"Fiscal {y} departmental income in fiscal 2025 dollars")
    put(f"departmental_income_real_change_fy{y}_to_fy2025", g(2025, "departmental_income")
        / (g(y, "departmental_income") * infl) - 1, "share", f"Departmental income, fiscal {y} to 2025, after inflation")
    for name in ("departmental_income", "profit", "revenue"):
        put(f"{name}_per_night_fy{y}_in_fy2025_dollars", v(f"{name}_per_night_fy{y}") * infl, "usd per occupied room night",
            f"Fiscal {y} {name} per night in fiscal 2025 dollars")

# 5. The thesis and the outside sources
check("thesis: fiscal 2025 departmental income within 1% of 2019 (the same money, in dollars of each year)",
      abs(v("departmental_income_change_fy2019_to_fy2025")) <= 0.01, f"{v('departmental_income_change_fy2019_to_fy2025'):.5f}")
check("thesis: at least 30% fewer occupied room nights than in 2019", v("rooms_occupied_change_fy2019_to_fy2025") <= -0.30,
      f"{v('rooms_occupied_change_fy2019_to_fy2025'):.4f}")
check("thesis: interest and other G&A add up to more than half of the profit drop from 2019 to 2025",
      v("interest_share_of_profit_drop") + v("other_ga_share_of_profit_drop") > 0.5,
      f"interest {v('interest_share_of_profit_drop'):.3f} + other {v('other_ga_share_of_profit_drop'):.3f}")
check("thesis: from 2022 to 2025 occupied room nights barely moved and profit turned into a loss",
      abs(v("rooms_occupied_change_fy2022_to_fy2025")) < 0.05
      and g(2025, "net_income_before_federal_income_taxes") < 0 < g(2022, "net_income_before_federal_income_taxes"),
      f"nights {v('rooms_occupied_change_fy2022_to_fy2025'):.4f}")
check("interest jumps in the same fiscal year the 'contracts' debt appears (fiscal 2020 to 2021); the new debt alone tops "
      "all of 2020's long-term debt", v("interest_change_fy2020_to_fy2021") > 1
      and g(2021, "long_term_debt_contracts") > g(2020, "total_long_term_debt"),
      f"interest {g(2020, 'interest_expense'):.0f} -> {g(2021, 'interest_expense'):.0f}")
for label, a, b, pub in (("visitors", "lvcva_laughlin_visitors_jan_sep_2025", "lvcva_laughlin_visitors_jan_sep_2026",
                          "lvcva_laughlin_visitors_change_jan_sep"),
                         ("gaming win", "lvcva_laughlin_gaming_win_jan_sep_2025", "lvcva_laughlin_gaming_win_jan_sep_2026",
                          "lvcva_laughlin_gaming_win_change_jan_sep")):
    chg = K[b] / K[a] - 1
    check(f"LVCVA: Laughlin {label}, January to September, change = the published one", abs(chg - K[pub]) <= TOL_LVCVA,
          f"{chg:.4f} vs {K[pub]}")
press = g(2025, "net_income_before_federal_income_taxes") / g(2024, "net_income_before_federal_income_taxes") - 1
check("the board's press release: Laughlin net income -758.6% from fiscal 2024",
      abs(press - K["ngcb_laughlin_net_income_change_fy2024_to_fy2025"]) <= TOL_PRESS, f"{press:.4f}")
three = K["vici_price_harrahs_laughlin"] + K["vici_price_harrahs_atlantic_city"] + K["vici_price_harrahs_new_orleans"]
put("harrahs_laughlin_share_of_three_property_price", K["vici_price_harrahs_laughlin"] / three, "share",
    "Harrah's Laughlin as a share of the price of the three buildings VICI bought")
put("harrahs_laughlin_rent_estimate", K["vici_rent_three_harrahs"] * K["vici_price_harrahs_laughlin"] / three,
    "usd per year", "Estimate, not published: Harrah's Laughlin's annual rent if the three-property rent splits by price")
put("vici_rent_yield_three_harrahs", K["vici_rent_three_harrahs"] / three, "share",
    "Annual rent of the three buildings as a share of what VICI paid")
for y in (2021, 2025):
    put(f"interest_to_long_term_debt_fy{y}", g(y, "interest_expense") / g(y, "total_long_term_debt"), "share",
        f"Fiscal {y}: interest as a share of the Laughlin casinos' long-term debt")

(HERE / "numbers.json").write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8")
print(f"numbers.json: {len(out)} numbers")

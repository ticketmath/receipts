"""Ticket Math #015 - UPS is shrinking on purpose: what does each package that stayed pay?

Recomputes every number in the video from the files in data/ and writes numbers.json.
Standard library only, no network: run `python calc.py` in this folder.

Method
1. UPS's U.S. Domestic Package segment table, from each 10-Q and 10-K: average daily package volume, average revenue
   per piece, operating days, revenue, operating expenses, operating profit, the adjusted operating profit UPS
   publishes (without transformation costs), and revenue by service, "Cargo and Other" included.
   Packages in a period = average daily volume x operating days. Per package = the line / packages.
   2024 figures are the ones UPS recast when U.S. air cargo moved into this segment (Q4 2024); they come from the
   comparison columns of the 2025 filings. Q4 = the full year minus the first nine months.
2. Before and after on the same quarter: July to September 2024 against July to September 2026, the first full quarter
   after UPS says its Amazon volume cut was done. Inflation: CPI-U (BLS), average of July to September.
3. Air cargo ("Cargo and Other"; UPS says its growth came from the U.S. Postal Service air cargo contract it took over
   in Q4 2024). UPS measures it by weight, so it is not in the package count or in revenue per piece, but it is in the
   segment's profit. Spread over packages = cargo revenue / packages. UPS does not publish its cost or profit.
4. For comparison: FedEx, Express U.S. Domestic segment, July to September 2025 and 2026.
5. Company statements (Amazon cut, jobs, buildings, program costs) and the driver buyout figures reported by the press.
"""
import csv
import json
from pathlib import Path

HERE = Path(__file__).parent
THOUSAND, MILLION = 1e3, 1e6
TOL_MILLION = 2         # sums in millions: each line is rounded to the million
TOL_PIECE = 0.003       # revenue per piece rebuilt from revenue and volume (volume rounded to the thousand)
TOL_PACKAGES = 0.002    # packages of three quarters against the nine months (daily volume rounded)
QUARTERS = [f"q{q}_{y}" for y in (2024, 2025) for q in (1, 2, 3, 4)] + [f"q{q}_2026" for q in (1, 2, 3)]
NINE = [f"9m_{y}" for y in (2024, 2025, 2026)]
YEARS = ["fy2024", "fy2025"]
SERVICES = ["next_day_air_revenue_millions", "deferred_revenue_millions", "ground_revenue_millions"]


def read(name):
    with open(HERE / "data" / name, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


T = {}
for r in read("ups_segment_tables.csv"):
    T.setdefault(r["period"], {})[r["metric"]] = float(r["value"])
FX = {}
for r in read("fedex_segment.csv"):
    FX.setdefault(r["period"], {})[r["metric"]] = float(r["value"])
CPI = {}
for r in read("bls_cpi_u_monthly.csv"):
    CPI.setdefault(int(r["year"]), []).append(float(r["value"]))
FIGURES = read("published_figures.csv")
K = {r["key"]: float(r["value"]) for r in FIGURES}
out = {}


def put(key, value, unit, description):
    out[key] = {"value": value, "unit": unit, "description": description}
    return value


def check(label, ok, detail):
    print(f"{'ok  ' if ok else 'FAIL'} {label}: {detail}")
    if not ok:
        raise SystemExit(1)


def name(p):
    if p.startswith("fy"):
        return f"full year {p[2:]}"
    if p.startswith("9m"):
        return f"January to September {p[3:]}"
    return f"Q{p[1]} {p[3:]}"


# 0. Published figures, as published
for r in FIGURES:
    if not r["key"].startswith("ups_consolidated_revenue_"):
        put(r["key"], float(r["value"]), r["unit"], f"{r['description']} ({r['source']})")

# 1. Each table adds up
for p, d in T.items():
    d["packages"] = d["avg_daily_packages_thousands"] * THOUSAND * d["operating_days"]
    total = sum(d[s] for s in SERVICES) + d["cargo_and_other_revenue_millions"]
    check(f"{p}: services + cargo = segment revenue", abs(total - d["revenue_millions"]) <= TOL_MILLION,
          f"{total:,.0f} and {d['revenue_millions']:,.0f}")
    check(f"{p}: revenue - expenses = operating profit (and adjusted)",
          abs(d["revenue_millions"] - d["operating_expenses_millions"] - d["operating_profit_millions"]) <= TOL_MILLION
          and abs(d["revenue_millions"] - d["adjusted_operating_expenses_millions"] - d["adjusted_operating_profit_millions"]) <= TOL_MILLION,
          f"profit {d['operating_profit_millions']:,.0f}; adjusted {d['adjusted_operating_profit_millions']:,.0f}")
    for label, rev in (("package revenue / packages", sum(d[s] for s in SERVICES)),
                       ("(segment revenue - cargo) / packages", d["revenue_millions"] - d["cargo_and_other_revenue_millions"])):
        rpp = rev * MILLION / d["packages"]
        check(f"{p}: {label} = published revenue per piece", abs(rpp / d["avg_revenue_per_piece_usd"] - 1) <= TOL_PIECE,
              f"{rpp:.3f} and {d['avg_revenue_per_piece_usd']:.2f}")
for y in (2024, 2025, 2026):
    qs, nm = [T[f"q{q}_{y}"] for q in (1, 2, 3)], T[f"9m_{y}"]
    check(f"{y}: days and profit of three quarters = nine months", sum(q["operating_days"] for q in qs) == nm["operating_days"]
          and abs(sum(q["operating_profit_millions"] for q in qs) - nm["operating_profit_millions"]) <= TOL_MILLION,
          f"{sum(q['operating_days'] for q in qs):.0f} and {nm['operating_days']:.0f} days")
    check(f"{y}: packages of three quarters = nine months", abs(sum(q["packages"] for q in qs) / nm["packages"] - 1) <= TOL_PACKAGES,
          f"{sum(q['packages'] for q in qs) / MILLION:,.1f}M and {nm['packages'] / MILLION:,.1f}M")

# Q4 = full year - nine months
FLOWS = ["operating_days", "revenue_millions", "operating_expenses_millions", "operating_profit_millions",
         "adjusted_operating_profit_millions", "transformation_strategy_costs_millions", "cargo_and_other_revenue_millions",
         "packages"] + SERVICES
for y in (2024, 2025):
    q4 = {m: T[f"fy{y}"][m] - T[f"9m_{y}"][m] for m in FLOWS}
    q4["avg_daily_packages_thousands"] = q4["packages"] / q4["operating_days"] / THOUSAND
    q4["avg_revenue_per_piece_usd"] = sum(q4[s] for s in SERVICES) * MILLION / q4["packages"]
    T[f"q4_{y}"] = q4

# 2. Per package, every period
for p in QUARTERS + NINE + YEARS:
    d, n = T[p], T[p]["packages"]
    put(f"op_profit_per_package_{p}", d["operating_profit_millions"] * MILLION / n, "usd", f"UPS, U.S.: operating profit per package, {name(p)}")
    put(f"adj_op_profit_per_package_{p}", d["adjusted_operating_profit_millions"] * MILLION / n, "usd",
        f"UPS, U.S.: adjusted operating profit per package (UPS's measure, without transformation costs), {name(p)}")
    put(f"revenue_per_package_{p}", d["avg_revenue_per_piece_usd"], "usd", f"UPS, U.S.: average revenue per piece, {name(p)}")
    put(f"packages_per_day_{p}", d["avg_daily_packages_thousands"] * THOUSAND, "packages a day", f"UPS, U.S.: average daily package volume, {name(p)}")
    put(f"transformation_costs_per_package_{p}", -d["transformation_strategy_costs_millions"] * MILLION / n, "usd",
        f"UPS, U.S.: transformation strategy costs (buyouts, consulting) per package, {name(p)}")
    put(f"cargo_revenue_{p}", d["cargo_and_other_revenue_millions"] * MILLION, "usd", f"UPS, U.S.: Cargo and Other revenue, {name(p)}")
    put(f"cargo_revenue_per_package_{p}", d["cargo_and_other_revenue_millions"] * MILLION / n, "usd",
        f"UPS, U.S.: Cargo and Other revenue spread over packages, {name(p)} (cargo is not packages)")
    check(f"{p}: segment revenue per package = revenue per piece + cargo per package",
          abs(d["revenue_millions"] * MILLION / n - d["avg_revenue_per_piece_usd"] - d["cargo_and_other_revenue_millions"] * MILLION / n)
          <= TOL_PIECE * d["avg_revenue_per_piece_usd"], f"{d['revenue_millions'] * MILLION / n:.3f}")
for p in ("q3_2024", "q3_2025", "q3_2026", "q2_2026", "9m_2024", "9m_2026", "fy2024", "fy2025"):
    d, n = T[p], T[p]["packages"]
    put(f"op_profit_{p}", d["operating_profit_millions"] * MILLION, "usd", f"UPS, U.S.: segment operating profit, {name(p)}")
    put(f"adj_op_profit_{p}", d["adjusted_operating_profit_millions"] * MILLION, "usd", f"UPS, U.S.: segment adjusted operating profit, {name(p)}")
    put(f"transformation_costs_{p}", -d["transformation_strategy_costs_millions"] * MILLION, "usd", f"UPS, U.S.: transformation strategy costs, {name(p)}")
    put(f"packages_{p}", n, "packages", f"UPS, U.S.: packages delivered, {name(p)}")
    put(f"opex_per_package_{p}", d["operating_expenses_millions"] * MILLION / n, "usd",
        f"UPS, U.S.: operating expenses per package, {name(p)} (air cargo included)")
    put(f"package_revenue_{p}", (d["revenue_millions"] - d["cargo_and_other_revenue_millions"]) * MILLION, "usd",
        f"UPS, U.S.: revenue from packages only, without air cargo, {name(p)}")
    put(f"segment_revenue_per_package_{p}", d["revenue_millions"] * MILLION / n, "usd",
        f"UPS, U.S.: segment revenue per package, air cargo included, {name(p)} (minus expenses per package = profit per package)")
    check(f"{p}: the receipt closes (segment revenue per package - expenses per package = profit per package)",
          abs((d["revenue_millions"] - d["operating_expenses_millions"]) * MILLION / n - d["operating_profit_millions"] * MILLION / n)
          <= TOL_MILLION * MILLION / n, f"{d['operating_profit_millions'] * MILLION / n:.3f}")

# 3. Before and after
WINDOWS = {"q3_2024_to_q3_2026": ("q3_2024", "q3_2026"), "9m_2024_to_9m_2026": ("9m_2024", "9m_2026"),
           "q3_2025_to_q3_2026": ("q3_2025", "q3_2026"), "q3_2024_to_q3_2025": ("q3_2024", "q3_2025"),
           "fy2024_to_fy2025": ("fy2024", "fy2025"), "q1_2024_to_q1_2025": ("q1_2024", "q1_2025")}
per = lambda p, line: T[p][line] * MILLION / T[p]["packages"]
for w in ("q3_2024_to_q3_2026", "9m_2024_to_9m_2026", "q3_2025_to_q3_2026", "q1_2024_to_q1_2025"):
    a, b = WINDOWS[w]
    da, db = T[a], T[b]
    lp0, lp1 = per(a, "operating_profit_millions"), per(b, "operating_profit_millions")
    la0, la1 = per(a, "adjusted_operating_profit_millions"), per(b, "adjusted_operating_profit_millions")
    label = f"{name(a)} to {name(b)}"
    put(f"change_op_profit_per_package_{w}", lp1 / lp0 - 1, "share", f"UPS, U.S.: change in operating profit per package, {label}")
    put(f"diff_op_profit_per_package_{w}", lp1 - lp0, "usd", f"UPS, U.S.: difference in operating profit per package, {label}")
    put(f"change_adj_op_profit_per_package_{w}", la1 / la0 - 1, "share", f"UPS, U.S.: change in adjusted operating profit per package, {label}")
    put(f"change_revenue_per_package_{w}", db["avg_revenue_per_piece_usd"] / da["avg_revenue_per_piece_usd"] - 1, "share",
        f"UPS, U.S.: change in revenue per piece, {label}")
    put(f"drop_packages_per_day_{w}", 1 - db["avg_daily_packages_thousands"] / da["avg_daily_packages_thousands"], "share",
        f"UPS, U.S.: drop in packages a day, {label}")
    put(f"fewer_packages_per_day_{w}", (da["avg_daily_packages_thousands"] - db["avg_daily_packages_thousands"]) * THOUSAND,
        "packages a day", f"UPS, U.S.: fewer packages a day, {label}")
    put(f"change_op_profit_{w}", db["operating_profit_millions"] / da["operating_profit_millions"] - 1, "share",
        f"UPS, U.S.: change in total segment operating profit, {label}")
for w, (a, b) in WINDOWS.items():
    da, db = T[a], T[b]
    label = f"{name(a)} to {name(b)}"
    put(f"diff_revenue_per_package_{w}", db["avg_revenue_per_piece_usd"] - da["avg_revenue_per_piece_usd"], "usd",
        f"UPS, U.S.: how much more UPS gets for each package (air cargo not included), {label}")
    put(f"diff_cargo_revenue_per_package_{w}",
        (db["cargo_and_other_revenue_millions"] / db["packages"] - da["cargo_and_other_revenue_millions"] / da["packages"]) * MILLION,
        "usd", f"UPS, U.S.: increase in cargo revenue spread over packages, {label}")
    put(f"diff_adj_op_profit_per_package_{w}",
        (db["adjusted_operating_profit_millions"] / db["packages"] - da["adjusted_operating_profit_millions"] / da["packages"]) * MILLION,
        "usd", f"UPS, U.S.: difference in adjusted operating profit per package, {label}")
    put(f"change_cargo_revenue_{w}", db["cargo_and_other_revenue_millions"] / da["cargo_and_other_revenue_millions"] - 1, "share",
        f"UPS, U.S.: change in Cargo and Other revenue, {label}")
    put(f"increase_cargo_revenue_{w}", (db["cargo_and_other_revenue_millions"] - da["cargo_and_other_revenue_millions"]) * MILLION,
        "usd", f"UPS, U.S.: more Cargo and Other revenue, {label}")

# 4. Inflation, July to September (CPI-U)
check("CPI: July to September published in 2024 and 2026", len(CPI[2024]) == 3 and len(CPI[2026]) == 3,
      f"{len(CPI[2024])} and {len(CPI[2026])} months")
infl = (sum(CPI[2026]) / len(CPI[2026])) / (sum(CPI[2024]) / len(CPI[2024]))
put("cpi_change_q3_2024_to_q3_2026", infl - 1, "share", "U.S. inflation (CPI-U), July-September 2024 average to July-September 2026 average")
q24, q26 = T["q3_2024"], T["q3_2026"]
lp24, lp26 = per("q3_2024", "operating_profit_millions"), per("q3_2026", "operating_profit_millions")
put("op_profit_per_package_q3_2024_in_2026_dollars", lp24 * infl, "usd", "UPS, U.S.: Q3 2024 operating profit per package in 2026 dollars")
put("real_change_op_profit_per_package_q3_2024_to_q3_2026", lp26 / (lp24 * infl) - 1, "share",
    "UPS, U.S.: change in operating profit per package after inflation, Q3 2024 to Q3 2026")
put("real_change_revenue_per_package_q3_2024_to_q3_2026",
    q26["avg_revenue_per_piece_usd"] / (q24["avg_revenue_per_piece_usd"] * infl) - 1, "share",
    "UPS, U.S.: change in revenue per piece after inflation, Q3 2024 to Q3 2026")
put("revenue_per_package_q3_2024_in_2026_dollars", q24["avg_revenue_per_piece_usd"] * infl, "usd",
    "UPS, U.S.: Q3 2024 revenue per piece in 2026 dollars")
put("real_diff_revenue_per_package_q3_2024_to_q3_2026", q26["avg_revenue_per_piece_usd"] - q24["avg_revenue_per_piece_usd"] * infl, "usd",
    "UPS, U.S.: how much more UPS gets for each package after inflation, Q3 2024 to Q3 2026")

# 5. Amazon, jobs and buildings
check("the Amazon cut announced and the one completed are the same", K["amazon_cut_announced"] == K["amazon_cut_completed"],
      f"more than {K['amazon_cut_announced']:.0%}")
for y in (2024, 2025):
    rev = put(f"ups_revenue_{y}", K[f"ups_consolidated_revenue_{y}"], "usd", f"UPS consolidated revenue in {y} (XBRL)")
    put(f"amazon_revenue_to_ups_{y}", rev * K[f"amazon_share_of_ups_revenue_{y}"], "usd",
        f"Revenue Amazon brought UPS in {y}, approximately: Amazon's share x consolidated revenue")
put("us_employees_fewer_2024_to_2025", K["us_employees_2024"] - K["us_employees_2025"], "employees",
    "UPS: fewer employees in the U.S., end of 2024 to end of 2025 (temporary seasonal employees excluded)")
put("buildings_closed_2025_to_sep_2026", K["buildings_daily_operations_closed_2025"] + K["buildings_closed_9m_2026"], "buildings",
    "UPS: buildings closed (2025: daily operations closed) from 2025 to September 2026")
put("buildings_permanently_closed_2025_to_sep_2026", K["buildings_permanently_closed_2025"] + K["buildings_permanently_closed_9m_2026"],
    "buildings", "UPS: buildings permanently closed from 2025 to September 2026")
check("order of magnitude: buyout cap x $150,000 fits in the Driver Choice cost UPS publishes",
      K["buyout_cap"] * K["driver_buyout_offer"] <= K["driver_choice_program_cost_2026"],
      f"{K['buyout_cap'] * K['driver_buyout_offer'] / 1e9:.2f}B and {K['driver_choice_program_cost_2026'] / 1e9:.1f}B")

# 6. FedEx, Express U.S. Domestic, July to September
for y in (2026, 2025):
    f = FX[f"jul_sep_{y}"]
    packages = f["avg_daily_packages_thousands"] * THOUSAND * f["operating_days"]
    check(f"FedEx {y}: package revenue / packages = published composite yield",
          abs(f["package_revenue_millions"] * MILLION / packages / f["composite_yield_usd"] - 1) <= TOL_PIECE,
          f"{f['package_revenue_millions'] * MILLION / packages:.3f} and {f['composite_yield_usd']:.2f}")
    check(f"FedEx {y}: packages + freight + other = revenue; revenue - expenses = operating income",
          abs(f["package_revenue_millions"] + f["us_freight_revenue_millions"] + f["other_revenue_millions"] - f["total_revenue_millions"]) <= TOL_MILLION
          and abs(f["total_revenue_millions"] - f["operating_expenses_millions"] - f["operating_income_millions"]) <= TOL_MILLION,
          f"operating income {f['operating_income_millions']:,.0f}")
    put(f"fedex_op_profit_per_package_q3_{y}", f["operating_income_millions"] * MILLION / packages, "usd",
        f"FedEx, U.S. (Express U.S. Domestic): operating income per package, July to September {y}")
    put(f"fedex_revenue_per_package_q3_{y}", f["composite_yield_usd"], "usd", f"FedEx, U.S.: composite revenue per package, July to September {y}")
    put(f"fedex_packages_per_day_q3_{y}", f["avg_daily_packages_thousands"] * THOUSAND, "packages a day",
        f"FedEx, U.S.: average daily packages, July to September {y}")
put("fedex_change_packages_per_day_q3_2025_to_q3_2026",
    FX["jul_sep_2026"]["avg_daily_packages_thousands"] / FX["jul_sep_2025"]["avg_daily_packages_thousands"] - 1, "share",
    "FedEx, U.S.: change in packages a day, July to September 2025 to 2026")

(HERE / "numbers.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
print(f"{len(out)} numbers written to numbers.json")

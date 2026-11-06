"""Ticket Math #010 - JetBlue: of every passenger it flew in the summer of 2026, how much came in, how much went out, and to whom?

Recomputes every number in the video from the files in data/ and writes numbers.json.
Standard library only, no network: run `python calc.py` in this folder.

Method
1. The receipt: the income statement of JetBlue's 10-Q for the third quarter of 2026 / revenue passengers. The same count
   for the third quarter of 2025 and for the nine months of 2026 and 2025.
2. Before: the same count from the 10-Ks of 2019 and 2025; net income from 2020 to 2025; retained earnings from the end
   of 2019 to September 30, 2026, checking that the losses close the fall in the balance.
3. The comparison: the 10-Qs for the same quarter of Delta, United, American, Southwest and Frontier (per $100 of revenue;
   per passenger only where the filing publishes passengers). Fuel price by airline from Form 41 (BTS, P-12(a)).
4. The debt: the 10-Q's debt, maturity and cash flow tables; the TrueBlue financing from the 8-K of September 3, 2024; the
   Spirit costs from the 10-Ks; Fort Lauderdale seats from the T-100 domestic segment data.
5. Market prices (notes, stock) and Carl Icahn's stake: press reports and Schedule 13D filings, in data/published_figures.csv.
"""
import csv
import json
from pathlib import Path

HERE = Path(__file__).parent
THOUSAND, MILLION, BILLION, HUNDRED = 1000, 1e6, 1e9, 100
PERIODS = ("q3_2026", "q3_2025", "nine_months_2026", "nine_months_2025")
LINES = ("fuel", "payroll", "airports", "depreciation", "aircraft_rent", "sales_and_marketing", "maintenance",
         "special_items", "other_expenses")
EMPLOYEE_GROUPS = ("pilots", "inflight", "airport_operations", "technicians", "reservation_agents", "management")
PEERS = ("delta", "united", "american", "southwest", "frontier")
CARRIERS = {"jetblue": "B6", "delta": "DL", "united": "UA", "american": "AA", "southwest": "WN", "frontier": "F9"}
LOSS_YEARS = range(2020, 2026)
Q2_MONTHS = (4, 5, 6)
TOL = 0.01              # published totals against the lines, as in the dossier
TOL_FARE = 0.005        # passenger revenue / passengers against the published average fare
TOL_LOYALTY = 0.03      # loyalty growth: published as a whole percent
TOL_BALANCE = 0.002     # retained earnings: rounded figures from several filings
TOL_T100 = 0.03         # passengers in the 10-K against the T-100


def read(name):
    with open(HERE / "data" / name, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


I = {r["key"]: float(r["value"]) for r in read("inputs.csv")}
K = {r["key"]: float(r["value"]) for r in read("published_figures.csv")}
UNITS = {r["key"]: r["unit"] for r in read("published_figures.csv")}
DESCRIPTIONS = {r["key"]: r["description"] for r in read("published_figures.csv")}
QUOTES = {r["key"]: r["quote"] for r in read("quotes.csv")}
FUEL = {(r["carrier"], int(r["month"])): (float(r["total_gallons"]), float(r["total_cost"])) for r in read("form41_fuel_2026.csv")}
SEATS = {}
for r in read("t100_fll_july_seats.csv"):
    SEATS.setdefault(int(r["year"]), {})[r["carrier"]] = float(r["seats"])
CPI = {}
for r in read("bls_cpi_u_monthly.csv"):
    CPI.setdefault(int(r["year"]), []).append(float(r["value"]))
out = {}


def put(key, value, unit, description):
    out[key] = {"value": value, "unit": unit, "description": description}


def check(label, ok, detail):
    print(f"{'ok  ' if ok else 'FAIL'} {label}: {detail}")
    if not ok:
        raise SystemExit(1)


def agrees(label, published, rebuilt, tolerance=TOL):
    check(label, abs(rebuilt - published) <= tolerance * abs(published), f"published {published:,.2f}; rebuilt {rebuilt:,.2f}")


for key in K:
    put(key, K[key], UNITS[key], f"{DESCRIPTIONS[key]} (see data/published_figures.csv)")

# 1. The receipt, third quarter and nine months
passengers = {p: I[f"passengers_{p}"] * THOUSAND for p in PERIODS}


def per_pax(amount_millions, period):
    return amount_millions * MILLION / passengers[period]


for p in PERIODS:
    lines = sum(I[f"{x}_{p}"] for x in LINES)
    agrees(f"10-Q, {p}: the expense lines add up to operating expenses", I[f"operating_expenses_{p}"], lines)
    agrees(f"10-Q, {p}: revenue - expenses = operating result", I[f"operating_result_{p}"], I[f"revenue_{p}"] - I[f"operating_expenses_{p}"])
    usd = "usd per passenger"
    put(f"passengers_{p}", passengers[p], "passengers", f"JetBlue: revenue passengers, {p}")
    put(f"revenue_per_passenger_{p}", per_pax(I[f"revenue_{p}"], p), usd, f"Operating revenue / passengers, {p}")
    put(f"cost_per_passenger_{p}", per_pax(I[f"operating_expenses_{p}"], p), usd, f"Operating expenses / passengers, {p}")
    put(f"operating_result_per_passenger_{p}", per_pax(I[f"operating_result_{p}"], p), usd, f"Operating result / passengers, {p}")
    put(f"interest_per_passenger_{p}", per_pax(I[f"interest_expense_{p}"], p), usd, f"Interest expense / passengers, {p}")
    put(f"pretax_result_per_passenger_{p}", per_pax(I[f"pretax_result_{p}"], p), usd, f"Result before income taxes / passengers, {p}")
    for x in LINES:
        put(f"{x}_per_passenger_{p}", per_pax(I[f"{x}_{p}"], p), usd, f"{x} / passengers, {p}")
for p, published in (("q3_2026", "average_fare_q3_2026"), ("q3_2025", "average_fare_q3_2025")):
    agrees(f"10-Q, {p}: passenger revenue / passengers = published average fare", I[published],
           I[f"passenger_revenue_{p}"] * MILLION / passengers[p], TOL_FARE)
fare, fare_before = I["average_fare_q3_2026"], I["average_fare_q3_2025"]
agrees("10-Q: the fare increase matches the published $ change column", I["average_fare_change_q3_published"], fare - fare_before)

loss, loss_before = -per_pax(I["net_result_q3_2026"], "q3_2026"), -per_pax(I["net_result_q3_2025"], "q3_2025")
put("operating_loss_per_passenger_q3_2026", -per_pax(I["operating_result_q3_2026"], "q3_2026"), "usd per passenger",
    "Loss from running the airline, before interest (as a positive amount), Q3 2026")
put("loss_per_passenger_q3_2026", loss, "usd per passenger", "Net loss / passengers, Q3 2026 (THE MAIN NUMBER)")
put("loss_per_passenger_q3_2025", loss_before, "usd per passenger", "Net loss / passengers, Q3 2025")
put("loss_per_passenger_increase_q3", loss - loss_before, "usd per passenger", "Net loss per passenger, Q3 2026 minus Q3 2025")
put("other_costs_per_passenger_q3_2026", per_pax(I["operating_expenses_q3_2026"] - I["payroll_q3_2026"] - I["fuel_q3_2026"], "q3_2026"),
    "usd per passenger", "(Operating expenses - payroll - fuel) / passengers, Q3 2026")
put("loss_per_passenger_nine_months_2026", -per_pax(I["net_result_nine_months_2026"], "nine_months_2026"), "usd per passenger",
    "Net loss / passengers, nine months of 2026")
put("loss_per_passenger_times_q3", loss / loss_before, "times", "Net loss per passenger, Q3 2026 / Q3 2025")
pretax, pretax_before = -per_pax(I["pretax_result_q3_2026"], "q3_2026"), -per_pax(I["pretax_result_q3_2025"], "q3_2025")
put("pretax_loss_per_passenger_change_q3", pretax / pretax_before - 1, "share", "Pretax loss per passenger, Q3 2026 / Q3 2025 - 1")
put("net_loss_q3_2026", -I["net_result_q3_2026"] * MILLION, "usd", "NET LOSS, Q3 2026")
put("net_loss_q3_2025", -I["net_result_q3_2025"] * MILLION, "usd", "NET LOSS, Q3 2025")
put("net_loss_nine_months_2026", -I["net_result_nine_months_2026"] * MILLION, "usd", "NET LOSS, nine months of 2026")
put("tax_benefit_q3_2026", I["tax_benefit_q3_2026"] * MILLION, "usd", "Income tax benefit, Q3 2026")
put("tax_benefit_q3_2025", I["tax_benefit_q3_2025"] * MILLION, "usd", "Income tax benefit, Q3 2025")
put("special_items_q3_2026", I["special_items_q3_2026"] * MILLION, "usd", "Special items, Q3 2026")
put("special_items_q3_2025", I["special_items_q3_2025"] * MILLION, "usd", "Special items, Q3 2025")
increase = -I["net_result_q3_2026"] + I["net_result_q3_2025"]
put("net_loss_increase_q3", increase * MILLION, "usd", "Net loss, Q3 2026 minus Q3 2025")
put("loss_increase_share_from_tax_and_special_items",
    ((I["tax_benefit_q3_2025"] - I["tax_benefit_q3_2026"]) + (I["special_items_q3_2026"] - I["special_items_q3_2025"])) / increase, "share",
    "(Fall in the tax benefit + rise in special items) / rise in the net loss, Q3")
for p in ("q3_2026", "q3_2025"):
    put(f"operating_result_ex_special_items_{p}", (I[f"operating_result_{p}"] + I[f"special_items_{p}"]) * MILLION, "usd",
        f"Operating result + special items, {p}")
put("operating_margin_q3_2026", I["operating_result_q3_2026"] / I["revenue_q3_2026"], "share", "Operating result / revenue, Q3 2026")
put("average_fare_q3_2026", fare, "usd per ticket", "Average fare (10-Q), Q3 2026")
put("average_fare_q3_2025", fare_before, "usd per ticket", "Average fare (10-Q), Q3 2025")
put("fare_change_q3", fare - fare_before, "usd per ticket", "Average fare, Q3 2026 minus Q3 2025")
put("fare_change_pct_q3", fare / fare_before - 1, "share", "Average fare, Q3 2026 / Q3 2025 - 1")
put("average_fare_nine_months_2026", I["average_fare_nine_months_2026"], "usd per ticket", "Average fare (10-Q), nine months of 2026")
revenue_change = out["revenue_per_passenger_q3_2026"]["value"] - out["revenue_per_passenger_q3_2025"]["value"]
cost_change = out["cost_per_passenger_q3_2026"]["value"] - out["cost_per_passenger_q3_2025"]["value"]
put("revenue_per_passenger_change_q3", revenue_change, "usd per passenger", "Revenue per passenger, Q3 2026 minus Q3 2025")
put("cost_per_passenger_change_q3", cost_change, "usd per passenger", "Cost per passenger, Q3 2026 minus Q3 2025")
total = 0
for x in LINES:
    change = out[f"{x}_per_passenger_q3_2026"]["value"] - out[f"{x}_per_passenger_q3_2025"]["value"]
    total += change
    put(f"{x}_per_passenger_change_q3", change, "usd per passenger", f"{x} per passenger, Q3 2026 minus Q3 2025")
agrees("the lines per passenger close the rise in cost per passenger", cost_change, total)
put("interest_income_q3_2026", I["interest_income_q3_2026"] * MILLION, "usd", "Interest income, Q3 2026")
put("interest_expense_q3_2026", I["interest_expense_q3_2026"] * MILLION, "usd", "Interest expense, Q3 2026")
revenue = I["revenue_q3_2026"]
put("jetblue_interest_per_100", I["interest_expense_q3_2026"] / revenue * HUNDRED, "usd of every $100 of revenue", "JetBlue: interest / revenue x 100, Q3 2026")
put("jetblue_fuel_per_100", I["fuel_q3_2026"] / revenue * HUNDRED, "usd of every $100 of revenue", "JetBlue: fuel / revenue x 100, Q3 2026")
put("jetblue_net_per_100", I["net_result_q3_2026"] / revenue * HUNDRED, "usd of every $100 of revenue", "JetBlue: net result / revenue x 100, Q3 2026")
put("jetblue_operating_per_100", I["operating_result_q3_2026"] / revenue * HUNDRED, "usd of every $100 of revenue", "JetBlue: operating result / revenue x 100, Q3 2026")
put("load_factor_q3_2026", I["load_factor_q3_2026"] / HUNDRED, "share", "Load factor (10-Q), Q3 2026")
put("load_factor_q3_2025", I["load_factor_q3_2025"] / HUNDRED, "share", "Load factor (10-Q), Q3 2025")

# The three quarters of 2026
quarters = -I["net_result_q3_2026"]
for q in ("q1", "q2"):
    net = -I[f"net_result_{q}_2026"]
    quarters += net
    put(f"net_loss_{q}_2026", net * MILLION, "usd", f"NET LOSS (10-Q), {q} 2026")
    put(f"loss_per_passenger_{q}_2026", net * MILLION / (I[f"passengers_{q}_2026"] * THOUSAND), "usd per passenger", f"Net loss / passengers, {q} 2026")
    put(f"average_fare_{q}_2026", I[f"average_fare_{q}_2026"], "usd per ticket", f"Average fare (10-Q), {q} 2026")
    put(f"fare_change_{q}_2026", I[f"fare_change_{q}_2026"], "usd per ticket", f"Average fare, $ change column (10-Q), {q} 2026")
agrees("the three quarters of 2026 add up to the nine-month net loss", -I["net_result_nine_months_2026"], quarters)

# October's release: fuel recaptured, the gallon, Fort Lauderdale, liquidity
put("fuel_recaptured_share", I["fuel_recaptured"] / HUNDRED, "share", "Share of higher fuel costs JetBlue says it recaptured, Q3 (8-K)")
put("fuel_per_gallon_q3_2026", I["fuel_per_gallon_q3_2026"], "usd per gallon", "Average fuel price, Q3 2026 (8-K)")
put("fuel_per_gallon_change_q3", I["fuel_per_gallon_change_q3"] / HUNDRED, "share", "Rise in the fuel price from a year earlier, Q3 (8-K)")
put("fuel_per_gallon_q4_2026_forecast", I["fuel_per_gallon_q4_2026_forecast"], "usd per gallon", "JetBlue's Q4 2026 fuel price estimate (8-K)")
put("fll_capacity_growth_q3", I["fll_capacity_growth_q3"] / HUNDRED, "share", "JetBlue's capacity growth at Fort Lauderdale, Q3, 'more than' (8-K)")
put("fll_rasm_growth_q3", I["fll_rasm_growth_q3"] / HUNDRED, "share", "Revenue per seat mile at Fort Lauderdale, Q3, 'nearly' (8-K)")
put("fll_seat_share_q4_forecast", I["fll_seat_share_q4_forecast"] / HUNDRED, "share", "JetBlue's expected seat share at Fort Lauderdale, Q4 (8-K)")
put("fll_seat_share_points_up", I["fll_seat_share_points_up"], "points", "Points that share is up from a year earlier (8-K)")
put("unencumbered_assets", I["unencumbered_assets"] * BILLION, "usd", "Unencumbered assets, approximate, per JetBlue (8-K)")
put("undrawn_credit_line", I["undrawn_credit_line"] * MILLION, "usd", "Undrawn credit facility (8-K)")
put("liquidity_september_30_2026", I["liquidity"] * BILLION, "usd", "Liquidity: cash, investment securities and the credit line (10-Q)")
put("cash_and_investments_september_30_2026", I["cash_and_investments"] * BILLION, "usd", "Unrestricted cash, equivalents and investment securities (10-Q)")

# January's plan against October's
check("January 2026 guidance said breakeven or better", "Breakeven or better" in QUOTES["january_guidance"], QUOTES["january_guidance"])
put("january_plan_fuel_per_gallon_low", I["january_plan_fuel_per_gallon_low"], "usd per gallon", "January 2026 guidance: fuel price for the year, low (8-K)")
put("january_plan_fuel_per_gallon_high", I["january_plan_fuel_per_gallon_high"], "usd per gallon", "January 2026 guidance: fuel price for the year, high (8-K)")
put("october_forecast_fuel_per_gallon_2026", I["october_forecast_fuel_per_gallon_2026"], "usd per gallon", "October 2026 guidance: fuel price for the year (8-K)")
put("october_forecast_margin_best", -I["october_forecast_margin_best_loss"] / HUNDRED, "share", "October 2026 guidance: adjusted operating margin for the year, best case (8-K)")
put("october_forecast_margin_worst", -I["october_forecast_margin_worst_loss"] / HUNDRED, "share", "October 2026 guidance: adjusted operating margin for the year, worst case (8-K)")
put("october_forecast_interest_2026", I["october_forecast_interest_2026"] * MILLION, "usd", "October 2026 guidance: interest expense for the year (8-K)")
put("jetforward_target_2027_low", I["jetforward_target_2027_low"] * MILLION, "usd", "JetForward: 2027 target, low (8-K)")
put("jetforward_target_2027_high", I["jetforward_target_2027_high"] * MILLION, "usd", "JetForward: 2027 target, high (8-K)")
put("jetforward_delivered_2025", I["jetforward_delivered_2025"] * MILLION, "usd", "JetForward: incremental EBIT delivered in 2025 (8-K)")
put("forecast_interest_vs_jetforward_high", I["october_forecast_interest_2026"] / I["jetforward_target_2027_high"], "share", "Interest forecast for 2026 / top of the JetForward target")
put("cash_and_investments_end_2025", I["cash_and_investments_end_2025"] * BILLION, "usd", "Liquidity at the end of 2025, without the credit line (8-K)")
check("the 10-Q says there were no fuel hedges", "fuel hedging" in QUOTES["no_fuel_hedges"], QUOTES["no_fuel_hedges"])
put("fuel_sensitivity_10_percent", I["fuel_sensitivity"] * MILLION, "usd a year", "Fuel expense over 12 months if the gallon rises 10% (10-Q, market risk)")

# Loyalty
loyalty, loyalty_before = I["loyalty_air_q3_2026"] + I["loyalty_related_q3_2026"], I["loyalty_air_q3_2025"] + I["loyalty_related_q3_2025"]
agrees("loyalty revenue: the rise matches the one JetBlue published", I["loyalty_revenue_growth_published"] / HUNDRED, loyalty / loyalty_before - 1, TOL_LOYALTY)
put("loyalty_total_revenue_q3_2026", loyalty * MILLION, "usd", "Loyalty revenue - air transportation + loyalty and related revenue, Q3 2026")
put("loyalty_total_revenue_per_passenger_q3_2026", per_pax(loyalty, "q3_2026"), "usd per passenger", "That / passengers, Q3 2026")
put("loyalty_total_revenue_change_q3", loyalty / loyalty_before - 1, "share", "That, Q3 2026 / Q3 2025 - 1")
put("loyalty_and_related_revenue_q3_2026", I["loyalty_related_q3_2026"] * MILLION, "usd", "Loyalty and related revenue, Q3 2026")
put("loyalty_and_related_per_passenger_q3_2026", per_pax(I["loyalty_related_q3_2026"], "q3_2026"), "usd per passenger", "Loyalty and related revenue / passengers, Q3 2026")

# 2. Before: 2019 against 2025
year = {}
for y in (2019, 2025):
    n = I[f"passengers_{y}"] * THOUSAND
    staff = sum(I[f"employees_{g}_{y}"] for g in EMPLOYEE_GROUPS)
    net = I[f"net_income_{y}"] / MILLION
    agrees(f"10-K {y}: the expense lines add up to operating expenses", I[f"operating_expenses_{y}"], sum(I[f"{x}_{y}"] for x in LINES))
    year[y] = {"n": n, "staff": staff, "net": net}
    usd = "usd per passenger"
    put(f"passengers_{y}", n, "passengers", f"Revenue passengers (10-K), {y}")
    put(f"average_fare_{y}", I[f"average_fare_{y}"], "usd per ticket", f"Average fare (10-K), {y}")
    put(f"stage_length_{y}", I[f"stage_length_{y}"], "miles", f"Average stage length (10-K), {y}")
    put(f"load_factor_{y}", I[f"load_factor_{y}"] / HUNDRED, "share", f"Load factor (10-K), {y}")
    put(f"employees_{y}", staff, "full-time equivalents", f"Sum of the employee groups (10-K), {y}")
    put(f"payroll_per_employee_{y}", I[f"payroll_{y}"] * MILLION / staff, "usd per employee", f"Salaries, wages and benefits / employees, {y}")
    put(f"passengers_per_employee_{y}", n / staff, "passengers per employee", f"Passengers / employees, {y}")
    put(f"revenue_per_passenger_{y}", I[f"revenue_{y}"] * MILLION / n, usd, f"Operating revenue / passengers, {y}")
    put(f"cost_per_passenger_{y}", I[f"operating_expenses_{y}"] * MILLION / n, usd, f"Operating expenses / passengers, {y}")
    put(f"interest_per_passenger_{y}", I[f"interest_expense_{y}"] * MILLION / n, usd, f"Interest expense / passengers, {y}")
    put(f"net_result_per_passenger_{y}", net * MILLION / n, usd, f"Net income / passengers, {y}")
    put(f"interest_expense_{y}", I[f"interest_expense_{y}"] * MILLION, "usd", f"Interest expense (10-K), {y}")
    put(f"net_income_{y}", net * MILLION, "usd", f"Net income (10-K), {y}")
    for x in LINES:
        put(f"{x}_per_passenger_{y}", I[f"{x}_{y}"] * MILLION / n, usd, f"{x} / passengers, {y}")
put("loss_per_passenger_2025", -out["net_result_per_passenger_2025"]["value"], "usd per passenger", "Net loss / passengers, 2025 (as a positive amount)")
put("interest_per_passenger_times_2019_to_2025", out["interest_per_passenger_2025"]["value"] / out["interest_per_passenger_2019"]["value"], "times", "Interest per passenger, 2025 / 2019")
for name, label in (("revenue", "Revenue"), ("cost", "Cost"), ("interest", "Interest")):
    put(f"{name}_per_passenger_change_2019_to_2025", out[f"{name}_per_passenger_2025"]["value"] - out[f"{name}_per_passenger_2019"]["value"],
        "usd per passenger", f"{label} per passenger, 2025 minus 2019")
for x in LINES:
    put(f"{x}_per_passenger_change_2019_to_2025", out[f"{x}_per_passenger_2025"]["value"] - out[f"{x}_per_passenger_2019"]["value"],
        "usd per passenger", f"{x} per passenger, 2025 minus 2019")
put("payroll_per_employee_change_2019_to_2025", (I["payroll_2025"] / year[2025]["staff"]) / (I["payroll_2019"] / year[2019]["staff"]) - 1, "share", "Payroll per employee, 2025 / 2019 - 1")
put("passengers_per_employee_change_2019_to_2025", (year[2025]["n"] / year[2025]["staff"]) / (year[2019]["n"] / year[2019]["staff"]) - 1, "share", "Passengers per employee, 2025 / 2019 - 1")
r1, r2, r3 = I["pilot_raise_march_2023"], I["pilot_raise_august_2023"], I["pilot_raise_august_2024"]
put("pilot_raise_march_2023", r1 / HUNDRED, "share", "Pilot contract of March 1, 2023: initial raise (10-K)")
put("pilot_raise_august_2023", r2 / HUNDRED, "share", "Pilot contract: raise of August 2023 (10-K)")
put("pilot_raise_august_2024", r3 / HUNDRED, "share", "Pilot contract: raise of August 2024 (10-K)")
put("pilot_raises_compounded", (1 + r1 / HUNDRED) * (1 + r2 / HUNDRED) * (1 + r3 / HUNDRED) - 1, "share", "The three raises, compounded")
put("stage_length_change_2019_to_2025", I["stage_length_2025"] / I["stage_length_2019"] - 1, "share", "Average stage length, 2025 / 2019 - 1")
check("BLS: 12 months of CPI-U in 2019", len(CPI[2019]) == 12, f"{len(CPI[2019])} months")
check("BLS: 11 months of CPI-U in 2025 (October 2025 was not collected)", len(CPI[2025]) == 11, f"{len(CPI[2025])} months")
put("inflation_2019_to_2025", (sum(CPI[2025]) / len(CPI[2025])) / (sum(CPI[2019]) / len(CPI[2019])) - 1, "share", "CPI-U, average of the published months of 2025 / of 2019 - 1")
put("average_fare_change_2019_to_2025", I["average_fare_2025"] / I["average_fare_2019"] - 1, "share", "Average fare, 2025 / 2019 - 1")

# The series of losses and retained earnings
series = {y: I[f"net_income_{y}"] / MILLION for y in LOSS_YEARS}
check("a loss in every year from 2020 to 2025", all(v < 0 for v in series.values()), ", ".join(f"{y}: {v:,.0f}" for y, v in series.items()))
put("loss_years_2020_to_2025", len(series), "years", "Years in a row with a net loss, 2020 to 2025")
losses = sum(series.values()) + I["net_result_nine_months_2026"]
put("losses_2020_to_september_2026", -losses * MILLION, "usd", "Sum of net losses, 2020 to September 30, 2026")
re_2019, re_2025 = I["retained_earnings_end_2019"], I["retained_earnings_december_31_2025"]
re_june, re_september = I["retained_earnings_june_30_2026"], I["retained_earnings_september_30_2026"]
put("retained_earnings_end_2019", re_2019 * MILLION, "usd", "Retained earnings, end of 2019 (10-K)")
put("retained_earnings_end_2025", re_2025 * MILLION, "usd", "Retained earnings, end of 2025 (10-Q)")
put("retained_earnings_june_30_2026", re_june * MILLION, "usd", "Retained earnings, June 30, 2026 (10-Q)")
put("retained_earnings_september_30_2026", re_september * MILLION, "usd", "Retained (deficit) earnings, September 30, 2026 (10-Q)")
put("retained_deficit_september_30_2026", -re_september * MILLION, "usd", "How far retained earnings were below zero, September 30, 2026")
check("the losses from 2020 to September 2026 close the fall in retained earnings",
      abs(re_2019 + losses - re_september) <= TOL_BALANCE * re_2019, f"{re_2019:,.0f} + {losses:,.0f} = {re_2019 + losses:,.0f}; published {re_september:,.0f}")
check("retained earnings: above zero in June 2026, below zero in September 2026", re_june > 0 > re_september, f"{re_june:,.0f} and {re_september:,.0f}")
check("10-Ks: JetBlue pays no dividends, so only results move the balance", "cash dividends" in QUOTES["no_dividends_2019"] and "cash dividends" in QUOTES["no_dividends_2025"], QUOTES["no_dividends_2025"])

# 3. The comparison: same quarter, same fuel market
base = {}
for c in PEERS:
    agrees(f"{c}: revenue - expenses = operating income", I[f"{c}_operating_income"], I[f"{c}_revenue"] - I[f"{c}_operating_expenses"])
    # Delta's refinery sales to third parties sit in both revenue and expenses: they stay out of the base
    rev = I[f"{c}_revenue"] - I.get(f"{c}_refinery_sales", 0)
    base[c] = rev
    u100 = "usd of every $100 of revenue"
    put(f"{c}_net_income_q3_2026", I[f"{c}_net_income"] * MILLION, "usd", f"{c}: net income, Q3 2026 (10-Q)")
    put(f"{c}_net_per_100", I[f"{c}_net_income"] / rev * HUNDRED, u100, f"{c}: net income / revenue x 100")
    put(f"{c}_interest_per_100", I[f"{c}_interest"] / rev * HUNDRED, u100, f"{c}: interest / revenue x 100")
    put(f"{c}_fuel_per_100", I[f"{c}_fuel"] / rev * HUNDRED, u100, f"{c}: fuel / revenue x 100")
    put(f"{c}_operating_per_100", I[f"{c}_operating_income"] / rev * HUNDRED, u100, f"{c}: operating income / revenue x 100")
    if f"{c}_passengers" in I:
        n = I[f"{c}_passengers"] * THOUSAND
        put(f"{c}_net_per_passenger", I[f"{c}_net_income"] * MILLION / n, "usd per passenger", f"{c}: net income / passengers")
        put(f"{c}_interest_per_passenger", I[f"{c}_interest"] * MILLION / n, "usd per passenger", f"{c}: interest / passengers")
put("frontier_loss_per_passenger", -out["frontier_net_per_passenger"]["value"], "usd per passenger", "Frontier: net loss / passengers (as a positive amount)")
amex = I["amex_paid_delta"] * BILLION
put("amex_paid_delta_q3_2026", amex, "usd", "Remuneration from American Express to Delta, Q3 2026 (10-Q)")
put("amex_vs_jetblue_revenue", amex / (revenue * MILLION), "share", "That / all of JetBlue's revenue in the same quarter")
jb_interest = I["interest_expense_q3_2026"] / revenue
check("none of the other airlines pays more interest per $100 of revenue than JetBlue",
      all(I[f"{c}_interest"] / base[c] < jb_interest for c in PEERS),
      ", ".join(f"{c}: {I[f'{c}_interest'] / base[c] * HUNDRED:.2f}" for c in PEERS) + f"; jetblue: {jb_interest * HUNDRED:.2f}")

# The gallon by airline: Form 41, P-12(a)
for c, code in CARRIERS.items():
    gallons, cost = (sum(FUEL[(code, m)][i] for m in Q2_MONTHS) for i in (0, 1))
    put(f"{c}_fuel_per_gallon_q2_2026", cost / gallons, "usd per gallon", f"{c}: total cost / total gallons, April to June 2026 (Form 41)")
for month, name in ((2, "february"), (4, "april")):
    put(f"jetblue_fuel_per_gallon_{name}_2026", FUEL[("B6", month)][1] / FUEL[("B6", month)][0], "usd per gallon", f"JetBlue: total cost / total gallons, {name} 2026 (Form 41)")

# 4. The debt and the breathing room
government = I["government_loan_cares"] + I["government_loan_extension"] + I["government_loan_arp"]
debt = I["current_debt"] + I["long_term_debt"]
agrees("balance sheet debt = total of the scheduled maturities", I["scheduled_maturities_total"], debt)
put("debt_september_30_2026", debt * MILLION, "usd", "Current + long-term debt and finance leases, balance sheet, September 30, 2026")
put("trueblue_debt", (I["trueblue_notes"] + I["trueblue_term_loan"]) * MILLION, "usd", "Debt backed by the TrueBlue collateral: the 2031 notes + the 2029 term loan")
put("trueblue_notes", I["trueblue_notes"] * MILLION, "usd", "2031 senior secured notes (10-Q)")
put("trueblue_term_loan", I["trueblue_term_loan"] * MILLION, "usd", "2029 senior secured term loan (10-Q)")
put("sale_leaseback_debt", I["sale_leaseback_debt"] * MILLION, "usd", "Aircraft failed sale-leaseback transactions (10-Q)")
put("government_loans", government * MILLION, "usd", "The three payroll support loans (10-Q)")
coupon = I["trueblue_notes_coupon"] / HUNDRED
put("trueblue_notes_coupon", coupon, "share", "Interest rate on the 2031 notes (8-K of September 3, 2024)")
put("trueblue_raised_2024", (I["trueblue_notes_issued"] + I["trueblue_term_loan_issued"]) * MILLION, "usd", "Notes + term loan issued in 2024 (8-K)")
coupon_year = I["trueblue_notes_issued"] * MILLION * coupon
put("trueblue_notes_interest_per_year", coupon_year, "usd a year", "Notes issued x interest rate")
put("trueblue_notes_interest_per_passenger", coupon_year / year[2025]["n"], "usd per passenger", "That / passengers of 2025")
check("the 8-K says the collateral is tied to the program", "certain collateral" in QUOTES["trueblue_collateral"], QUOTES["trueblue_collateral"])
debt_2019 = I["current_debt_end_2019"] + I["long_term_debt_end_2019"]
put("debt_end_2019", debt_2019 * MILLION, "usd", "Current + long-term debt and finance leases, end of 2019 (10-K)")
put("debt_times_2019_to_september_2026", debt / debt_2019, "times", "Debt on September 30, 2026 / at the end of 2019")
for y in ("2027", "2028", "2029", "total"):
    put(f"debt_due_{y}", I[f"debt_due_{y}"] * MILLION, "usd", f"Debt due, principal and interest, {y} (10-Q, contractual obligations)")
put("debt_repaid_nine_months_2026", -I["debt_repayment_nine_months_2026"] * MILLION, "usd", "Repayment of debt, nine months of 2026 (10-Q)")
put("new_debt_nine_months_2026", I["debt_proceeds_nine_months_2026"] * MILLION, "usd", "Proceeds from new debt, nine months of 2026 (10-Q)")
cash_flow, capex, deposits = I["operating_cash_flow_nine_months_2026"], I["capital_expenditures_nine_months_2026"], I["pre_delivery_deposits_nine_months_2026"]
burn = -(cash_flow + capex + deposits)
burn_month = burn * MILLION / 9
put("operating_cash_flow_nine_months_2026", cash_flow * MILLION, "usd", "Net cash used in operating activities, nine months of 2026 (10-Q)")
put("investments_nine_months_2026", -(capex + deposits) * MILLION, "usd", "Capital expenditures + pre-delivery deposits, nine months of 2026 (10-Q)")
put("cash_burn_per_month", burn_month, "usd a month", "(Operating cash flow + investments) / 9, before new loans or debt repayments")
put("months_of_liquidity", I["liquidity"] * BILLION / burn_month, "months", "Liquidity / cash burn per month: arithmetic, not a forecast")
put("unused_points_liability", I["unused_points_liability"] * MILLION, "usd", "Air traffic liability - loyalty program, September 30, 2026 (10-Q)")
shares = I["shares_outstanding"]
low, nov3 = K["stock_intraday_low_october_26_2026"], K["stock_close_november_3_2026"]
put("shares_outstanding", shares, "shares", "Shares outstanding (cover of the 10-Q)")
put("market_value_at_low", low * shares, "usd", "Intraday low of October 26, 2026 x shares")
put("market_value_november_3", nov3 * shares, "usd", "Close of November 3, 2026 x shares")
put("stock_rebound_low_to_november_3", nov3 / low - 1, "share", "Close of November 3 / low of October 26 - 1")
put("trueblue_debt_vs_market_value", (I["trueblue_notes"] + I["trueblue_term_loan"]) * MILLION / (low * shares), "times", "TrueBlue-backed debt / market value at the low")

# 5. Spirit
c24, c23, c22 = I["spirit_costs_2024"], I["spirit_costs_2023"], I["spirit_costs_2022"]
put("spirit_costs_2024", c24 * MILLION, "usd", "Spirit-related costs, 2024 (10-K of 2024)")
put("spirit_costs_2023", c23 * MILLION, "usd", "Spirit-related costs, 2023 (10-K of 2024)")
put("spirit_costs_2022", c22 * MILLION, "usd", "Spirit costs, 2022 (10-K of 2023)")
put("spirit_costs_total", (c24 + c23 + c22) * MILLION, "usd", "Spirit costs, 2022 to 2024")
put("spirit_prepayments", I["spirit_prepayments"] * MILLION, "usd", "Prepayments to Spirit shareholders by December 31, 2023 (10-K of 2023)")
put("laguardia_slots", I["laguardia_slots"], "slots", "Spirit's LaGuardia operating authorizations bought by JetBlue (10-Q)")
put("laguardia_slots_price", I["laguardia_slots_price"] * MILLION, "usd", "Aggregate purchase price of those slots (10-Q)")
deal = I["spirit_deal_value"] * BILLION
put("spirit_deal_value", deal, "usd", "Spirit deal: aggregate fully diluted equity value, July 2022 (8-K)")
put("spirit_deal_vs_market_value", deal / (low * shares), "times", "Spirit deal / JetBlue's market value at the October 2026 low")
put("spirit_breakup_fee", I["spirit_breakup_fee"] * MILLION, "usd", "What JetBlue paid Spirit on ending the deal, March 2024 (Spirit's 10-K)")

# Fort Lauderdale, domestic seats, July (T-100)
for y, seats in SEATS.items():
    all_seats = sum(seats.values())
    put(f"fll_jetblue_seat_share_july_{y}", seats["B6"] / all_seats, "share", f"JetBlue's seats / all domestic seats leaving FLL, July {y}")
    put(f"fll_spirit_seat_share_july_{y}", seats.get("NK", 0) / all_seats, "share", f"Spirit's seats / all domestic seats leaving FLL, July {y}")
    put(f"fll_domestic_seats_july_{y}", all_seats, "seats", f"All domestic seats leaving FLL, July {y}")
check("JetBlue 2025: passengers in the 10-K close to the T-100's", abs(I["t100_passengers_jetblue_2025"] - year[2025]["n"]) <= TOL_T100 * year[2025]["n"],
      f"10-K {year[2025]['n'] / MILLION:,.2f} million; T-100 {I['t100_passengers_jetblue_2025'] / MILLION:,.2f} million")
check("the 10-Q's statement on liquidity is in the filing", "next 12 months" in QUOTES["liquidity_statement"], QUOTES["liquidity_statement"])

(HERE / "numbers.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
print(f"{len(out)} numbers written to numbers.json")

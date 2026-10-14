"""Ticket Math #002 - How many rental days a month does a rental car need just to cover what it loses?

Recomputes every number in the video from the CSV files in data/ and writes numbers.json.
Standard library only, no network: run `python calc.py` from this folder.

Method
1. Hertz, Americas RAC segment (U.S. and the Americas), from the operating data table in its 2025 annual report
   (Form 10-K, SEC EDGAR; data/hertz_americas_kpis_2025.csv): fleet cost per car per month (Depreciation Per Unit
   Per Month: depreciation, rents for leased cars and the result of selling the cars, with the costs of selling)
   divided by revenue per rental day (Total RPD).
2. Car sales: cash received from selling cars against the year's revenue, and the gain or loss on those sales,
   for Hertz and Avis Budget as whole companies (data/xbrl_10k_2025.csv), with what that line includes according
   to the notes (data/notes_10k_2025.csv).
"""
import csv
import json
from pathlib import Path

HERE = Path(__file__).parent
YEAR, PRIOR = 2025, 2024
MILLION, THOUSAND = 1e6, 1e3
MONTHS = 12
TOLERANCE = 0.01  # accepted gap between a published figure and the one rebuilt from the same table


def read(name):
    with open(HERE / "data" / name, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def check(label, ok, detail):
    print(f"{'ok  ' if ok else 'FAIL'} {label}: {detail}")
    if not ok:
        raise SystemExit(1)


def main():
    kpi = {(r["metric"], int(r["year"])): float(r["value"]) for r in read(f"hertz_americas_kpis_{YEAR}.csv")}
    notes = {(r["company"], r["item"]): float(r["value"]) for r in read(f"notes_10k_{YEAR}.csv")}
    xbrl = {(r["company"], r["item"]): float(r["value_usd"]) for r in read(f"xbrl_10k_{YEAR}.csv")}
    out = {}

    def put(key, value, unit, label, formula):
        out[key] = {"value": value, "unit": unit, "label": label, "formula": formula}

    k = lambda metric, year=YEAR: kpi[(metric, year)]

    # 0. The published per-car figures come from the lines of the same table
    for year in (YEAR, PRIOR):
        rebuilt = k("fleet_cost_usd_millions", year) * MILLION / k("average_vehicles", year) / MONTHS
        check(f"fleet cost per car per month {year}", abs(rebuilt - k("fleet_cost_per_car_month", year)) <= TOLERANCE * rebuilt,
              f"published {k('fleet_cost_per_car_month', year):,.2f}, rebuilt {rebuilt:,.2f}")
        rebuilt = k("revenue_usd_millions", year) * MILLION / (k("transaction_days_thousands", year) * THOUSAND)
        check(f"revenue per rental day {year}", abs(rebuilt - k("revenue_per_rental_day", year)) <= TOLERANCE * rebuilt,
              f"published {k('revenue_per_rental_day', year):,.2f}, rebuilt {rebuilt:,.2f}")
    h = lambda item: notes[("hertz", item)]
    parts = h("depreciation_of_vehicles") + h("loss_on_disposal_of_vehicles") + h("rents_paid_for_vehicles_leased")
    check("fleet cost = depreciation + loss on disposal + rents for leased cars", abs(parts - h("fleet_cost_net")) <= TOLERANCE * parts,
          f"{parts:,.0f} vs {h('fleet_cost_net'):,.0f} million")

    # 1. Hertz Americas: the math per car
    put("days_to_cover", k("fleet_cost_per_car_month") / k("revenue_per_rental_day"), "count",
        "Rental days a month whose revenue covers what a Hertz car in the Americas loses in the month",
        "fleet cost per car per month / revenue per rental day")
    put("days_to_cover_2024", k("fleet_cost_per_car_month", PRIOR) / k("revenue_per_rental_day", PRIOR), "count",
        "The same in 2024, the year of the EV write-downs", "fleet cost per car per month / revenue per rental day")
    put("fleet_cost_per_car_month", k("fleet_cost_per_car_month"), "usd",
        "Fleet cost per car per month: depreciation, rents for leased cars and the result of selling the cars", "published")
    put("fleet_cost_per_car_month_2024", k("fleet_cost_per_car_month", PRIOR), "usd", "The same in 2024", "published")
    put("revenue_per_rental_day", k("revenue_per_rental_day"), "usd", "Revenue per rental day", "published")
    put("revenue_per_rental_day_2024", k("revenue_per_rental_day", PRIOR), "usd", "Revenue per rental day in 2024", "published")
    put("revenue_per_rentable_car_month", k("revenue_per_rentable_car_month"), "usd",
        "Revenue per rentable car per month (excludes cars held for sale)", "published")

    # Same base as the cost per car: the average fleet
    per_fleet_car = k("revenue_usd_millions") * MILLION / k("average_vehicles") / MONTHS
    put("revenue_per_fleet_car_month", per_fleet_car, "usd", "Revenue per fleet car per month", "revenue / average vehicles / 12")
    put("fleet_cost_share_of_car_revenue", k("fleet_cost_per_car_month") / per_fleet_car, "share",
        "Share of a fleet car's monthly revenue that goes to fleet cost", "fleet cost per car / revenue per fleet car")
    put("rented_days_per_car_month", k("transaction_days_thousands") * THOUSAND / k("average_vehicles") / MONTHS, "count",
        "Days a month a fleet car is out on rent, on average", "transaction days / average vehicles / 12")
    put("vehicle_utilization", k("vehicle_utilization_pct") / 100, "share", "Utilization of rentable cars", "published")
    put("average_vehicles", k("average_vehicles"), "count", "Hertz average fleet in the Americas", "published")
    put("months_in_fleet", h("months_in_fleet_of_cars_sold"), "count",
        "Months the cars sold in 2025 spent in the fleet, on average", "10-K text")
    put("program_vehicles_share", k("program_vehicles_pct") / 100, "share",
        "Share of the Americas fleet at year end with a buyback or guaranteed depreciation from the maker", "published")
    put("hertz_2024_vehicle_impairment", h("vehicle_impairment_2024") * MILLION, "usd",
        "Hertz 2024 write-down of fleet values (whole company), booked outside the fleet cost per car", "10-K note")

    # 2. Car sales: Hertz and Avis Budget (whole companies)
    for c in ("hertz", "avis"):
        x = lambda item: xbrl[(c, item)]
        put(f"{c}_revenue", x("revenue"), "usd", f"{c}: revenue for the year", "XBRL: Revenues")
        put(f"{c}_vehicle_sales", x("vehicle_sales"), "usd", f"{c}: cash received from selling fleet cars", "XBRL")
        put(f"{c}_sales_share_of_revenue", x("vehicle_sales") / x("revenue"), "share", f"{c}: car sales as a share of revenue",
            "car sales / revenue")
        put(f"{c}_gain_on_sale", x("gain_on_sale_of_vehicles"), "usd", f"{c}: gain (or loss) on selling the cars", "XBRL")
        put(f"{c}_net_income", x("net_income"), "usd", f"{c}: net income (or loss) for the year", "XBRL: NetIncomeLoss")
    check("Hertz: loss on disposal in the note = loss in XBRL",
          abs(h("loss_on_disposal_of_vehicles") * MILLION + xbrl[("hertz", "gain_on_sale_of_vehicles")])
          <= TOLERANCE * abs(xbrl[("hertz", "gain_on_sale_of_vehicles")]),
          f"note {h('loss_on_disposal_of_vehicles'):,.0f} million")

    selling = h("costs_of_selling_vehicles") * MILLION
    before = xbrl[("hertz", "gain_on_sale_of_vehicles")] + selling
    put("hertz_costs_of_selling", selling, "usd", "Hertz: costs of selling the cars, included in the result of the sale", "10-K note")
    put("hertz_gain_before_selling_costs", before, "usd", "Hertz: result of selling the cars before the costs of selling",
        "gain (loss) on sale + costs of selling")
    put("hertz_sales_share_returning_book_value", (xbrl[("hertz", "vehicle_sales")] - before) / xbrl[("hertz", "vehicle_sales")],
        "share", "Hertz: share of the sale cash that only gave back the cars' book value (approximate)",
        "(car sales - gain before costs of selling) / car sales")
    charges = notes[("avis", "fleet_disposal_charges")] * MILLION
    put("avis_fleet_charges", charges, "usd", "Avis Budget: charges for disposing of part of the Americas fleet, included in the loss",
        "10-K note")
    put("avis_gain_before_fleet_charges", xbrl[("avis", "gain_on_sale_of_vehicles")] + charges, "usd",
        "Avis Budget: result of selling the cars without those charges", "gain (loss) on sale + fleet charges")

    (HERE / "numbers.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    for key in ("days_to_cover", "fleet_cost_per_car_month", "hertz_sales_share_of_revenue", "hertz_gain_on_sale"):
        print(f"{key}: {out[key]['value']:.4f}")


if __name__ == "__main__":
    main()

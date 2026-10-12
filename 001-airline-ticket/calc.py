"""Ticket Math #001 - How much of a $400 airline ticket does the airline keep?

Recomputes every number in the video from the CSV files in data/ and writes numbers.json.
Standard library only, no network: run `python calc.py` from this folder.

Method
1. Federal taxes and the airport fee come out of the example fare first, using the published rates (data/inputs.csv).
2. What is left (the airline fare) is split in the same proportions as the combined costs of 7 major
   U.S. publicly traded airlines in their 2025 annual reports (Form 10-K, SEC EDGAR; data/airlines_10k_2025.csv).
3. Profit per boarding = combined net profit / passenger boardings reported to the BTS (T-100; data/t100_boardings_2025.csv).
"""
import csv
import json
from pathlib import Path

HERE = Path(__file__).parent
YEAR = 2025
SLICES = ["fuel", "labor", "regional", "airport_costs", "maintenance", "planes", "other_costs",
          "interest_and_other", "income_tax", "profit"]
LABELS = {"fuel": "Fuel", "labor": "Pilots, flight attendants and other employees", "regional": "Regional airline partners",
          "airport_costs": "Landing fees and airport rent", "maintenance": "Aircraft maintenance",
          "planes": "Depreciation (planes, ground equipment, buildings) and aircraft rent",
          "other_costs": "Other operating costs (not broken out in the 10-K)",
          "interest_and_other": "Interest and other non-operating items", "income_tax": "Income taxes", "profit": "Net profit"}


def read(name):
    with open(HERE / "data" / name, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main():
    inputs = {r["name"]: float(r["value"]) for r in read("inputs.csv")}
    out = {}

    def put(key, value, unit, label, formula):
        out[key] = {"value": value, "unit": unit, "label": label, "formula": formula}

    # 1. The ticket: government and airport first
    price, segments = inputs["price"], inputs["segments"]
    for k in ("price", "line", "federal_ticket_tax_rate", "segment_fee", "tsa_fee", "airport_fee_max"):
        unit = "share" if k in ("line", "federal_ticket_tax_rate") else "usd"
        put(k, inputs[k], unit, k.replace("_", " "), "input (data/inputs.csv)")
    segment_fees = segments * inputs["segment_fee"]
    tsa = segments * inputs["tsa_fee"]
    airport = segments * inputs["airport_fee_boardings_per_segment"] * inputs["airport_fee_max"]
    fare = (price - segment_fees - tsa - airport) / (1 + inputs["federal_ticket_tax_rate"])
    government = fare * inputs["federal_ticket_tax_rate"] + segment_fees + tsa
    put("ticket_government", government, "usd", "Federal taxes and fees on the ticket",
        "7.5% tax on the fare + segment fee x segments + TSA fee x segments")
    put("ticket_airport_fee", airport, "usd", "Airport fee on the ticket (PFC)", "PFC maximum x boardings")
    put("ticket_airline_fare", fare, "usd", "What the airline counts as revenue", "(price - fixed fees) / (1 + tax rate)")

    # 2. The airlines' annual reports
    rows = read(f"airlines_10k_{YEAR}.csv")
    books = {}
    for r in rows:
        books.setdefault(r["airline"], {})[r["line"]] = float(r["value_usd"])
    total = {k: 0.0 for k in SLICES}
    revenue = 0.0
    margins = {}
    for code, v in books.items():
        expenses = v.get("operating_expenses", v["revenue"] - v["operating_income"])
        profit = v["pretax_income"] - v["income_tax"]
        parts = {"fuel": v["fuel"], "labor": v["labor"], "regional": v.get("regional_capacity", 0.0),
                 "airport_costs": v["landing_fees_and_rent"], "maintenance": v["maintenance"],
                 "planes": v["depreciation"] + v.get("aircraft_rent", 0.0)}
        parts["other_costs"] = expenses - sum(parts.values())
        parts["interest_and_other"] = v["operating_income"] - v["pretax_income"]
        parts["income_tax"] = v["income_tax"]
        parts["profit"] = profit
        for k, x in parts.items():
            total[k] += x
        revenue += v["revenue"]
        margins[code] = profit / v["revenue"]
    put("group_revenue", revenue, "usd", "Combined revenue of the 7 airlines", "sum of 10-K revenues")

    # 3. The split inside the ticket
    for k in SLICES:
        put(f"share_{k}", total[k] / revenue, "share", f"{LABELS[k]}: share of every revenue dollar", f"sum of {k} / sum of revenue")
        put(f"ticket_{k}", fare * total[k] / revenue, "usd", f"{LABELS[k]}: dollars of the example ticket", f"airline fare x {k} / revenue")
    put("profit_share_of_price", fare * total["profit"] / revenue / price, "share",
        "Airline profit as a share of the full price paid", "profit on the ticket / price paid")

    # 4. Per boarding (10-K / T-100)
    boardings = sum(float(r["boardings"]) for r in read(f"t100_boardings_{YEAR}.csv"))
    put("group_boardings", boardings, "count", "Passenger boardings (the group and the regionals flying for it)", "sum of T-100 PASSENGERS")
    put("profit_per_boarding", total["profit"] / boardings, "usd", "Net profit per boarding", "combined net profit / boardings")
    put("revenue_per_boarding", revenue / boardings, "usd", "Revenue per boarding", "combined revenue / boardings")

    # 5. Scoreboard by airline
    for code, m in margins.items():
        c = code.lower()
        put(f"margin_{c}", m, "share", f"{code}: net profit per revenue dollar", "net profit / revenue")
        put(f"profit_share_of_price_{c}", fare * m / price, "share", f"{code}: profit as a share of the example ticket",
            "airline fare x margin / price paid")

    (HERE / "numbers.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    for k in ("ticket_profit", "profit_share_of_price", "profit_per_boarding"):
        print(f"{k}: {out[k]['value']:.4f}")


if __name__ == "__main__":
    main()

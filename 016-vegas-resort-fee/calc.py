"""Ticket Math #016 - The Las Vegas resort fee: how much of a night on the Strip is the room, and how much is the fee?

Recomputes every number in the video from the file in data/ and writes numbers.json.
Standard library only, no network: run `python calc.py` in this folder.

Method
1. Prices from the hotels' own booking sites, read on November 17, 2026, for the night of Tuesday, November 24, 2026,
   and for the weekend of November 20 to 22 at the Excalibur: 2 guests, the lowest rate of each room type, before tax.
   MGM Resorts (Excalibur, Luxor, Bellagio) and Caesars (Flamingo). Since the federal rule of May 12, 2025, the sites
   show the room rate, the resort fee and the total separately. The booking engines run in the browser, so the
   prices were read on screen; they are in data/published_figures.csv as shown.
2. Share of the night that is resort fee = resort fee / (room rate + resort fee), before tax.
3. Room tax on the Strip: 13.38% (Clark County), charged on the room rate and on the resort fee. The Flamingo's own
   price breakdown confirms it: its "Taxes" line is 13.38% of room rate + resort fee.
4. Context: the Strip's average daily room rate by month in 2026 (LVCVA) and by fiscal year (Gaming Abstract); the
   resort fee at the same hotel in 2010 (Las Vegas Sun) and MGM's resort fee revenue in 2009 and 2010 (10-K).
"""
import csv
import json
from pathlib import Path

HERE = Path(__file__).parent
TOL_CENT = 0.005           # the sites round to the cent
TAX_RANGE = (0.5, 2)       # the tax on the Excalibur fee alone is in the same range as the room rate itself


def read(name):
    with open(HERE / "data" / name, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


FIGURES = read("published_figures.csv")
K = {r["key"]: float(r["value"]) for r in FIGURES}
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

# 1. Room rate + resort fee = the total the site shows
for room, fee, total in (("excalibur_room_rate_nov24", "excalibur_resort_fee", "excalibur_total_nov24"),
                         ("excalibur_room_rate_weekend", "excalibur_resort_fee", "excalibur_total_weekend"),
                         ("luxor_room_rate_nov24", "luxor_resort_fee", "luxor_total_nov24"),
                         ("bellagio_room_rate_nov24", "bellagio_resort_fee", "bellagio_total_nov24")):
    check(f"{room} + {fee} = {total}", abs(K[room] + K[fee] - K[total]) <= TOL_CENT, f"{K[room] + K[fee]:.2f} against {K[total]}")
check("LVCVA: January to September sits between the cheapest and the priciest month",
      K["strip_adr_august_2026"] < K["strip_adr_jan_sep_2026"] < K["strip_adr_may_2026"],
      f"{K['strip_adr_august_2026']} < {K['strip_adr_jan_sep_2026']} < {K['strip_adr_may_2026']}")

# 2. Four nights at MGM hotels: what the fee is of the night
tax = K["strip_room_tax_rate"]
NIGHTS = (("excalibur_nov24", "excalibur_room_rate_nov24", "excalibur_resort_fee", "Excalibur, Tuesday November 24, 2026"),
          ("excalibur_weekend", "excalibur_room_rate_weekend", "excalibur_resort_fee", "Excalibur, November 20 to 22, 2026"),
          ("luxor_nov24", "luxor_room_rate_nov24", "luxor_resort_fee", "Luxor, Tuesday November 24, 2026"),
          ("bellagio_nov24", "bellagio_room_rate_nov24", "bellagio_resort_fee", "Bellagio, Tuesday November 24, 2026"))
for name, room, fee, label in NIGHTS:
    before = K[room] + K[fee]
    put(f"{name}_resort_fee_share_of_night", K[fee] / before, "share", f"{label}: resort fee / (room rate + resort fee), before tax")
    put(f"{name}_night_with_tax", before * (1 + tax), "usd a night", f"{label}: (room rate + resort fee) x (1 + room tax)")
    put(f"{name}_resort_fee_with_tax", K[fee] * (1 + tax), "usd a night", f"{label}: resort fee x (1 + room tax)")
    put(f"{name}_resort_fee_vs_room_rate_times", K[fee] / K[room], "times", f"{label}: resort fee / room rate")
put("excalibur_nov24_tax_on_resort_fee", K["excalibur_resort_fee"] * tax, "usd a night", "Excalibur: the room tax charged on the resort fee alone")
check("Excalibur, November 24: the tax on the fee alone is in the same range as the room rate",
      TAX_RANGE[0] < K["excalibur_resort_fee"] * tax / K["excalibur_room_rate_nov24"] < TAX_RANGE[1],
      f"{K['excalibur_resort_fee'] * tax:.2f} against {K['excalibur_room_rate_nov24']}")

# 3. The Flamingo's own receipt: the tax line is charged on room rate + resort fee
for room, taxes, total in (("flamingo_room_rate_nov24", "flamingo_taxes_nov24", "flamingo_total_nov24"),
                           ("flamingo_fab_room_rate_nov24", "flamingo_fab_room_taxes_nov24", "flamingo_fab_room_total_nov24")):
    base = K[room] + K["flamingo_resort_fee"]
    check(f"{room}: the published taxes are 13.38% of room rate + resort fee", abs(base * tax - K[taxes]) <= TOL_CENT,
          f"{base * tax:.4f} against {K[taxes]}")
    check(f"{room}: room rate + taxes + resort fee = published total",
          abs(K[room] + K[taxes] + K["flamingo_resort_fee"] - K[total]) <= TOL_CENT,
          f"{K[room] + K[taxes] + K['flamingo_resort_fee']:.2f} against {K[total]}")
room, fee, total = K["flamingo_room_rate_nov24"], K["flamingo_resort_fee"], K["flamingo_total_nov24"]
put("flamingo_nov24_resort_fee_share_of_night", fee / (room + fee), "share",
    "Flamingo, Tuesday November 24, 2026: resort fee / (room rate + resort fee), before tax")
put("flamingo_nov24_resort_fee_vs_room_rate_times", fee / room, "times", "Flamingo, November 24, 2026: resort fee / room rate")
put("flamingo_nov24_resort_fee_with_tax_share_of_total", (fee * (1 + tax)) / total, "share",
    "Flamingo, November 24, 2026: resort fee with its tax / published total")
discount = K["flamingo_room_rate_before_promos_nov24"] - room
put("flamingo_promo_discount", discount, "usd a night", "Flamingo: room rate before the promotions - room rate after ('You saved')")
put("flamingo_promo_discount_share_of_room_rate", discount / K["flamingo_room_rate_before_promos_nov24"], "share",
    "Flamingo: the discount / the room rate before the promotions")
# the discount also removes the tax that would have been charged on it (the tax is on room rate + resort fee)
discount_with_tax = discount * (1 + tax)
put("flamingo_promo_discount_share_of_full_night", discount_with_tax / (total + discount_with_tax), "share",
    "Flamingo: the discount with the tax it avoids / what the night would cost without the promotion (fee and tax included)")

# 4. The same hotel in 2010, and the year the fee spread
put("excalibur_2010_resort_fee_share_of_night", K["excalibur_resort_fee_2010"] / (K["excalibur_room_rate_2010"] + K["excalibur_resort_fee_2010"]),
    "share", "Excalibur, May 2010: resort fee / (room rate + resort fee)")
put("excalibur_resort_fee_2026_vs_2010_times", K["excalibur_resort_fee"] / K["excalibur_resort_fee_2010"], "times",
    "Excalibur resort fee in 2026 / in 2010")
put("mgm_resort_fee_revenue_2010_vs_2009_times", K["mgm_resort_fee_revenue_2010"] / K["mgm_resort_fee_revenue_2009"], "times",
    "MGM resort fee revenue, 2010 / 2009")

# 5. The whole Tuesday bill at the Excalibur, with the car
bill = (K["excalibur_room_rate_nov24"] + K["excalibur_resort_fee"]) * (1 + tax) + K["mgm_self_parking_per_day"]
put("excalibur_nov24_bill_with_parking", bill, "usd a night", "Excalibur, November 24, 2026: (room rate + resort fee) x (1 + room tax) + self-parking")
put("excalibur_nov24_room_rate_share_of_bill", K["excalibur_room_rate_nov24"] / bill, "share",
    "Excalibur, November 24, 2026: room rate / the whole bill with parking")
check("Excalibur, November 24: the fee's share is above the 20% the FTC cited",
      K["excalibur_resort_fee"] / (K["excalibur_room_rate_nov24"] + K["excalibur_resort_fee"]) > K["ftc_resort_fee_share_cited"],
      f"{K['excalibur_resort_fee'] / (K['excalibur_room_rate_nov24'] + K['excalibur_resort_fee']):.3f} > {K['ftc_resort_fee_share_cited']}")
put("aria_water_minibar_vs_starbucks_times", K["aria_minibar_water"] / K["aria_starbucks_water"], "times",
    "Minibar water at Aria / the same water at the Starbucks in the complex")

# 6. The same $45 fee on top of the Strip's average room rate, priciest and cheapest month of 2026
for month in ("may", "august"):
    put(f"resort_fee_45_on_strip_adr_{month}_2026", K["excalibur_resort_fee"] / K[f"strip_adr_{month}_2026"], "share",
        f"A $45 resort fee / the Strip's average daily room rate in {month.capitalize()} 2026 (LVCVA)")
put("strip_adr_change_fy2019_to_fy2025", K["strip_adr_fy2025"] / K["strip_adr_fy2019"] - 1, "share",
    "Strip average room rate, fiscal 2019 to fiscal 2025 (Gaming Abstract)")

(HERE / "numbers.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
print(f"{len(out)} numbers written to numbers.json")

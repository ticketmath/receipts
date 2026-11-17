"""Ticket Math #014 - Airbnb: who gets each part of a night?

Recomputes every number in the video from the files in data/ and writes numbers.json.
Standard library only, no network: run `python calc.py` in this folder.

Method
1. The night: Gross Booking Value (GBV: what the host gets, service fees, cleaning fees and taxes) / nights booked, from
   the key business metrics tables in Airbnb's 10-K filings (worldwide 2019 to 2025; North America 2020 to 2025; the
   10-K has no North America figures for 2019).
2. Airbnb's part: revenue / nights booked (worldwide revenue from the XBRL of each 10-K; revenue by region from the
   10-K table). The rest of the night (GBV - revenue) is the host's side, cleaning and taxes included.
3. Where Airbnb's part goes: each line of the income statement (cost of revenue, operations and support, product
   development, sales and marketing, general and administrative, profit) / nights, 2019 and 2025, worldwide.
4. For comparison: U.S. inflation (CPI-U, all items) and the price of lodging away from home (CPI-U), BLS.
5. The fees Airbnb says it charges (Help Center, read November 16, 2026): they check the share we compute.
"""
import csv
import json
from pathlib import Path

HERE = Path(__file__).parent
MILLION = 1e6
YEAR, BASE, BASE_NA, PEAK = 2025, 2019, 2021, 2024
YEARS = list(range(2019, 2026))
YEARS_NA = list(range(2020, 2026))
PANDEMIC = [2020, 2021]     # revenue (at check-in) and bookings (at booking) out of step: 2020 has the highest share
TOL_NIGHT = 0.002           # our GBV per night against the one written in the 2021 10-K (nights are rounded)
TOL_SUM = 0.0005            # costs + operating income against revenue
MAX_TAX = 0.20              # top tax rate on the subtotal, only for the range in the fee check
COSTS = ["cost_of_revenue", "operations_and_support", "product_development", "sales_and_marketing",
         "general_and_administrative", "operating_income"]
LINES = COSTS + ["net_income"]
LINE_NAMES = {"cost_of_revenue": "cost of revenue (payment processing, hosting the systems)",
              "operations_and_support": "operations and customer support",
              "product_development": "product development (engineering)", "sales_and_marketing": "sales and marketing",
              "general_and_administrative": "general and administrative", "operating_income": "operating income",
              "net_income": "net income"}


def read(name):
    with open(HERE / "data" / name, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


KBM = {(r["region"], r["metric"], int(r["year"])): float(r["value_millions"]) * MILLION for r in read("key_business_metrics.csv")}
CHECKS = {r["region"]: float(r["value"]) for r in read("published_checks.csv")}
IS = {(int(r["year"]), r["line"]): float(r["value_usd"]) for r in read("income_statement.csv")}
CPI = {}
for r in read("bls_cpi_u_monthly.csv"):
    CPI.setdefault((r["item"], int(r["year"])), []).append(float(r["value"]))
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


nights = {y: KBM[("world", "nights_booked", y)] for y in YEARS}
gbv = {y: KBM[("world", "gross_booking_value", y)] for y in YEARS}
revenue = {y: IS[(y, "revenue")] for y in YEARS}
na_n = {y: KBM[("north_america", "nights_booked", y)] for y in YEARS_NA}
na_g = {y: KBM[("north_america", "gross_booking_value", y)] for y in YEARS_NA}
na_r = {y: KBM[("north_america", "revenue", y)] for y in YEARS_NA}

# 0. Published figures, as published
for r in FIGURES:
    put(r["key"], float(r["value"]), r["unit"], f"{r['description']} ({r['source']})")

# 1. Our GBV per night against the one the 2021 10-K writes
for region, ours in (("world", gbv[BASE_NA] / nights[BASE_NA]), ("north_america", na_g[BASE_NA] / na_n[BASE_NA])):
    check(f"GBV per night in {BASE_NA} ({region}) = the one in the 10-K text", abs(ours / CHECKS[region] - 1) <= TOL_NIGHT,
          f"ours {ours:.2f}; published {CHECKS[region]:.2f}")


def per_night(y):
    return gbv[y] / nights[y], revenue[y] / nights[y]


# 2. The night, year by year
for y in YEARS:
    night, ab = per_night(y)
    put(f"world_average_night_{y}", night, "usd a night", f"Worldwide: average value of a night booked on Airbnb in {y} "
        "(fees, cleaning and taxes included): GBV / nights booked")
    put(f"world_airbnb_per_night_{y}", ab, "usd a night", f"Worldwide: what Airbnb keeps per night booked in {y}: revenue / nights booked")
    put(f"world_airbnb_share_{y}", ab / night, "share", f"Worldwide: Airbnb's share of the value of a night in {y}: revenue / GBV")
for y in YEARS_NA:
    night, ab = na_g[y] / na_n[y], na_r[y] / na_n[y]
    put(f"na_average_night_{y}", night, "usd a night", f"North America: average value of a night booked in {y}")
    put(f"na_airbnb_per_night_{y}", ab, "usd a night", f"North America: what Airbnb keeps per night in {y}")
    put(f"na_airbnb_share_{y}", ab / night, "share", f"North America: Airbnb's share of the value of a night in {y}")
put("na_host_side_per_night_2025", (na_g[YEAR] - na_r[YEAR]) / na_n[YEAR], "usd a night",
    f"North America: the host's side of a night in {YEAR} (what the host gets, cleaning and taxes): (GBV - revenue) / nights")
put("na_nights_booked_2025", na_n[YEAR], "nights", f"North America: nights and seats booked in {YEAR}")
put("world_nights_booked_2025", nights[YEAR], "nights", f"Worldwide: nights and seats booked in {YEAR}")
put("world_nights_booked_2019", nights[BASE], "nights", f"Worldwide: nights and experiences booked in {BASE}")
put("world_gbv_2025", gbv[YEAR], "usd", f"Worldwide: gross booking value in {YEAR}")
put("world_revenue_2025", revenue[YEAR], "usd", f"Airbnb's revenue in {YEAR}")

# 3. Who got the increase: since 2019 (worldwide) and since 2021 (North America)
(n19, a19), (n25, a25) = per_night(BASE), per_night(YEAR)
put("world_host_side_per_night_2019", n19 - a19, "usd a night", f"Worldwide: the host's side of a night in {BASE}")
put("world_host_side_per_night_2025", n25 - a25, "usd a night", f"Worldwide: the host's side of a night in {YEAR}")
put("world_night_increase_2019_2025", n25 - n19, "usd a night", f"Worldwide: how much more a night cost in {YEAR} than in {BASE}")
put("world_airbnb_increase_2019_2025", a25 - a19, "usd a night", f"Worldwide: how much of that went to Airbnb")
put("world_host_side_increase_2019_2025", (n25 - a25) - (n19 - a19), "usd a night", "Worldwide: how much went to the host's side")
put("world_airbnb_share_of_increase_2019_2025", (a25 - a19) / (n25 - n19), "share", "Worldwide: Airbnb's part of the increase")
put("world_night_change_2019_2025", n25 / n19 - 1, "share", f"Worldwide: change in the value of a night, {BASE} to {YEAR}")
put("world_airbnb_change_2019_2025", a25 / a19 - 1, "share", f"Worldwide: change in Airbnb's part per night, {BASE} to {YEAR}")
put("world_host_side_change_2019_2025", (n25 - a25) / (n19 - a19) - 1, "share",
    f"Worldwide: change in the host's side per night, {BASE} to {YEAR}")
nb, nbn = na_g[BASE_NA] / na_n[BASE_NA], na_g[YEAR] / na_n[YEAR]
nab, nan = na_r[BASE_NA] / na_n[BASE_NA], na_r[YEAR] / na_n[YEAR]
put("na_night_change_2021_2025", nbn / nb - 1, "share", f"North America: change in the value of a night, {BASE_NA} to {YEAR}")
put("na_night_increase_2021_2025", nbn - nb, "usd a night", f"North America: how much more a night cost, {BASE_NA} to {YEAR}")
put("na_airbnb_increase_2021_2025", nan - nab, "usd a night", f"North America: how much of that went to Airbnb")
outside = [y for y in YEARS if y not in PANDEMIC]
peak = max(outside, key=lambda y: per_night(y)[1] / per_night(y)[0])
check(f"outside the pandemic ({', '.join(map(str, PANDEMIC))}), Airbnb's highest worldwide share is in {PEAK}", peak == PEAK,
      f"highest share outside the pandemic in {peak}")

# 4. Where Airbnb's part goes (income statement / nights, worldwide)
for y in (BASE, YEAR):
    total = 0.0
    for line in LINES:
        v = IS[(y, line)]
        if line != "net_income":
            total += v
        put(f"world_{line}_per_night_{y}", v / nights[y], "usd a night", f"Worldwide: {LINE_NAMES[line]} per night booked in {y}")
    check(f"{y}: costs + operating income = revenue", abs(total / revenue[y] - 1) <= TOL_SUM,
          f"sum {total:,.0f}; revenue {revenue[y]:,.0f}")
    if y == BASE:   # a loss, said as a loss: the same value with the sign flipped
        put("world_net_loss_per_night_2019", -IS[(y, "net_income")] / nights[BASE], "usd a night",
            f"Worldwide: how much Airbnb lost per night booked in {BASE} (net income, sign flipped)")
        put("world_operating_loss_per_night_2019", -IS[(y, "operating_income")] / nights[BASE], "usd a night",
            f"Worldwide: operating loss per night booked in {BASE} (sign flipped)")
put("world_net_income_2025", IS[(YEAR, "net_income")], "usd", f"Airbnb's net income in {YEAR}")

# 5. Inflation and lodging (BLS, CPI-U, average of the months published; October 2025 was not collected)
avg = lambda item, y: sum(CPI[(item, y)]) / len(CPI[(item, y)])
check("CPI 2025: only October is missing (the BLS did not collect it)", len(CPI[("all_items", YEAR)]) == 11
      and len(CPI[("lodging_away_from_home", YEAR)]) == 11, f"{len(CPI[('all_items', YEAR)])} months")
for key, item, de, ate, name in (("cpi_all_items_change_2019_2025", "all_items", BASE, YEAR, "inflation (CPI-U, all items)"),
                                 ("cpi_lodging_change_2019_2025", "lodging_away_from_home", BASE, YEAR, "lodging away from home (CPI-U)"),
                                 ("cpi_lodging_change_2021_2025", "lodging_away_from_home", BASE_NA, YEAR, "lodging away from home (CPI-U)"),
                                 ("cpi_all_items_change_2021_2025", "all_items", BASE_NA, YEAR, "inflation (CPI-U, all items)")):
    put(key, avg(item, ate) / avg(item, de) - 1, "share", f"U.S.: change in {name}, {de} average to {ate} average")

# 6. The fees Airbnb says it charges, against the share we compute
host, gmin, gmax, single = (K[k] for k in ("split_fee_host_share", "split_fee_guest_share_low", "split_fee_guest_share_high",
                                           "single_fee_host_share"))
low = min(single / (1 + MAX_TAX), (host + gmin) / (1 + gmin + MAX_TAX))
high = max(single, (host + gmax) / (1 + gmax))
for region, share in (("worldwide", a25 / n25), ("North America", nan / nbn)):
    check(f"the {YEAR} share ({region}) fits what the published fees allow, with taxes from zero to {MAX_TAX:.0%}",
          low <= share <= high, f"share {share:.4f}; range {low:.4f} to {high:.4f}")

(HERE / "numbers.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
print(f"{len(out)} numbers written to numbers.json")

"""Ticket Math #004 - What does it cost to get goods from China to your door?

Recomputes every number in the video from data/inputs_2025.csv and writes numbers.json.
Standard library only, no network: run `python calc.py` from this folder.

Method (2025 data)
1. Ocean: US Census Bureau imports, goods that arrived by container ship. "Charges" (freight, insurance and other
   costs up to the first US port, tariff not included) / value of those goods = ocean cost per dollar of goods.
   For China, Vietnam and all countries; also per pound (charges / weight).
2. Tariff: Census calculated duty / value of imports for consumption, same countries. Checked against the tariffs
   the Treasury actually collected in the calendar year.
3. One container: Census value of containerized goods entering through the Port of Los Angeles / loaded import TEUs
   (port statistics). Checked against Hapag-Lloyd's published average freight rate per TEU.
4. Land: Union Pacific average revenue per intermodal load; UPS average revenue per US package; Amazon shipping
   costs / store sales (North America + International, without AWS).
"""
import csv
import json
from pathlib import Path

HERE = Path(__file__).parent
YEAR, PRIOR = 2025, 2024
THOUSAND, MILLION, BILLION = 1e3, 1e6, 1e9
TOLERANCE = 0.01          # published figure vs the one rebuilt from the same filing
TREASURY_TOLERANCE = 0.05  # Census calculated duty vs Treasury collections (timing and refunds differ)
FREIGHT_RANGE = (0.5, 3)   # Census charges per TEU between half and three times Hapag-Lloyd's average rate


def read(name):
    with open(HERE / "data" / name, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def check(label, ok, detail):
    print(f"{'ok  ' if ok else 'FAIL'} {label}: {detail}")
    if not ok:
        raise SystemExit(1)


def near(label, published, rebuilt, tolerance=TOLERANCE):
    check(label, abs(rebuilt - published) <= tolerance * abs(published), f"published {published:,.2f}, rebuilt {rebuilt:,.2f}")


def main():
    rows = read(f"inputs_{YEAR}.csv")
    data = {(r["source"], r["item"]): float(r["value"]) for r in rows}
    get = lambda source, item: data[(source, item)]
    out = {}

    def put(key, value, unit, label, formula):
        out[key] = {"value": value, "unit": unit, "label": label, "formula": formula}

    # ===== 1 and 2. Ocean and tariff, by country =====
    for country in ("china", "vietnam", "all_countries"):
        c = lambda field: get(f"census_{country}", field)
        check(f"{country}: container cargo fits inside vessel cargo, which fits inside the total",
              c("CNT_VAL_YR") <= c("VES_VAL_YR") <= c("GEN_VAL_YR") and c("CNT_CHA_YR") <= c("VES_CHA_YR"),
              f"container {c('CNT_VAL_YR') / BILLION:,.1f} bn <= vessel {c('VES_VAL_YR') / BILLION:,.1f} bn "
              f"<= total {c('GEN_VAL_YR') / BILLION:,.1f} bn")
        ocean = c("CNT_CHA_YR") / c("CNT_VAL_YR")
        tariff = c("CAL_DUT_YR") / c("CON_VAL_YR")
        put(f"{country}_imports", c("GEN_VAL_YR"), "usd", f"{country}: US imports in {YEAR} (general imports value)", "GEN_VAL_YR")
        put(f"{country}_ocean_share", ocean, "share", f"{country}: ocean freight, insurance and other charges per dollar of containerized goods",
            "CNT_CHA_YR / CNT_VAL_YR")
        put(f"{country}_tariff_share", tariff, "share", f"{country}: calculated duty per dollar of goods", "CAL_DUT_YR / CON_VAL_YR")
        put(f"{country}_tariff_vs_ocean", tariff / ocean, "count", f"{country}: tariff share / ocean share", "ratio")
        put(f"{country}_ocean_charges", c("CNT_CHA_YR"), "usd", f"{country}: charges on containerized goods for the year", "CNT_CHA_YR")
        put(f"{country}_tariff_total", c("CAL_DUT_YR"), "usd", f"{country}: calculated duty for the year", "CAL_DUT_YR")

    china = lambda field: get("census_china", field)
    pounds = china("CNT_WGT_YR") / get("constant", "kg_per_pound")
    put("china_ocean_per_pound", china("CNT_CHA_YR") / pounds, "usd", "China: ocean charges per pound of containerized goods",
        "CNT_CHA_YR / weight in pounds")
    put("china_value_per_pound", china("CNT_VAL_YR") / pounds, "usd", "China: value per pound of containerized goods",
        "CNT_VAL_YR / weight in pounds")

    months = sorted((item, value) for (source, item), value in data.items() if source == "treasury")
    collected = sum(v for _, v in months)
    near("tariffs calculated by Census close to tariffs collected by the Treasury", collected,
         get("census_all_countries", "CAL_DUT_YR"), TREASURY_TOLERANCE)
    put("tariffs_collected", collected, "usd", f"Tariffs collected by the US government in {YEAR} (calendar year)", "sum of 12 months")
    put("tariffs_collected_january", months[0][1], "usd", f"Tariffs collected in January {YEAR}", "Customs Duties, January")
    put("tariffs_collected_december", months[-1][1], "usd", f"Tariffs collected in December {YEAR}", "Customs Duties, December")

    box = get("assumption", "example_box_value")
    put("example_box_value", box, "usd", "Example: a box of goods from China worth $100 at customs", "assumption")
    put("example_box_ocean", box * out["china_ocean_share"]["value"], "usd", "Example: the ocean on that box", "box x china_ocean_share")
    put("example_box_tariff", box * out["china_tariff_share"]["value"], "usd", "Example: the tariff on that box", "box x china_tariff_share")
    put("thesis_threshold", get("assumption", "thesis_threshold"), "share", "Threshold chosen for the thesis: ocean below one tenth", "assumption")

    # ===== 3. One container through Los Angeles =====
    value_teu = get("census_port_los_angeles", "CNT_VAL_YR") / get("constant", "la_loaded_import_teu")
    teu_per_container = get("assumption", "teu_per_container")
    put("la_value_per_teu", value_teu, "usd", "Average value of goods in one loaded import TEU at Los Angeles", "port CNT_VAL_YR / loaded import TEU")
    put("teu_per_container", teu_per_container, "count", "TEU in a 40-foot container", "assumption")
    container = value_teu * teu_per_container
    put("la_value_per_container", container, "usd", "Average value of goods in a 40-foot container at Los Angeles", "value per TEU x 2")
    hapag = get("constant", "hapag_lloyd_rate_per_teu")
    put("hapag_lloyd_rate_per_teu", hapag, "usd", "Hapag-Lloyd average freight rate per TEU, all routes", "published")
    ratio = out["all_countries_ocean_share"]["value"] * value_teu / hapag
    check("Census charges per TEU in the same range as a carrier's published rate", FREIGHT_RANGE[0] <= ratio <= FREIGHT_RANGE[1],
          f"ratio {ratio:.2f} (charges include insurance and other costs; value per TEU is Los Angeles')")

    # ===== 4. Land =====
    up = lambda item: get("union_pacific", item)
    near("Union Pacific: intermodal revenue / loads = average revenue per load", up("intermodal_average_revenue_per_car"),
         up("intermodal_revenue_musd") * MILLION / (up("intermodal_carloads_thousands") * THOUSAND))
    put("union_pacific_revenue_per_container", up("intermodal_average_revenue_per_car"), "usd",
        "Union Pacific: average revenue per intermodal container or trailer", "published")
    put("train_share", up("intermodal_average_revenue_per_car") / container, "share",
        "Train per dollar of goods: revenue per container / value of a Los Angeles container", "ratio")

    ups = lambda item: get("ups", item)
    near("UPS Ground: revenue / (packages per day x days) = published revenue per package", ups("ground_revenue_per_piece"),
         ups("ground_revenue_musd") * MILLION / (ups("ground_daily_volume_thousands") * THOUSAND * ups("operating_days")))
    put("ups_revenue_per_package", ups("revenue_per_piece"), "usd", "UPS: average revenue per US domestic package", "published")
    put("ups_ground_revenue_per_package", ups("ground_revenue_per_piece"), "usd", "UPS: average revenue per Ground package", "published")
    put("ups_revenue_per_package_2024", ups(f"revenue_per_piece_{PRIOR}"), "usd", f"UPS: average revenue per US package, {PRIOR}", "published")

    amz = lambda item: get("amazon", item)
    near("Amazon: North America + International + AWS = consolidated sales", amz("consolidated_sales_musd"),
         amz("north_america_sales_musd") + amz("international_sales_musd") + amz("aws_sales_musd"))
    shipping = amz("shipping_costs_busd") * BILLION
    stores = (amz("north_america_sales_musd") + amz("international_sales_musd")) * MILLION
    put("amazon_shipping_costs", shipping, "usd", f"Amazon: shipping costs in {YEAR}", "10-K")
    put("amazon_shipping_share", shipping / stores, "share", "Amazon: shipping costs per dollar of store sales (rough)",
        "shipping costs / (North America + International sales)")

    (HERE / "numbers.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    for key in ("china_ocean_share", "china_tariff_share", "china_tariff_vs_ocean", "train_share", "amazon_shipping_share"):
        print(f"{key}: {out[key]['value']:.4f}")


if __name__ == "__main__":
    main()

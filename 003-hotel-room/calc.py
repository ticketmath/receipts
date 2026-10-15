"""Ticket Math #003 - Who makes money on a hotel room: the company that owns the building, or the brand on the door?

Recomputes every number in the video from the CSV files in data/ and writes numbers.json.
Standard library only, no network: run `python calc.py` from this folder.

Method
1. Owner: Host Hotels & Resorts, all consolidated hotels, 2025 annual report (Form 10-K, SEC EDGAR).
   Available room nights = rooms revenue / RevPAR; nights sold = rooms revenue / average daily rate (effective basis,
   all hotels for the period Host owned them). Every line of the income statement is divided by available room
   nights, and the lines add back up to total revenue.
2. Owner: Park Hotels & Resorts. Gross property cost / rooms of the consolidated hotels (Item 2 list); net result,
   write-down, debt.
3. Brands: Marriott, Hilton, Hyatt. Fees (franchise, base and incentive management) / (average system rooms x 365);
   net income / the same nights; return on total assets.
"""
import csv
import json
from pathlib import Path

HERE = Path(__file__).parent
YEAR, PRIOR = 2025, 2024
MILLION, DAYS, PCT = 1e6, 365, 100
TOLERANCE = 0.01  # accepted gap between a published figure and the one rebuilt from the same filing


def read(name):
    with open(HERE / "data" / name, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def check(label, ok, detail):
    print(f"{'ok  ' if ok else 'FAIL'} {label}: {detail}")
    if not ok:
        raise SystemExit(1)


def near(label, published, rebuilt):
    check(label, abs(rebuilt - published) <= TOLERANCE * abs(published), f"published {published:,.2f}, rebuilt {rebuilt:,.2f}")


def main():
    data = {(r["company"], r["item"]): float(r["value"]) for r in read(f"inputs_{YEAR}.csv")}
    park_list = read(f"park_hotels_{YEAR}.csv")
    out = {}

    def put(key, value, unit, label, formula):
        out[key] = {"value": value, "unit": unit, "label": label, "formula": formula}

    # ===== 1. Host Hotels & Resorts =====
    h = lambda item: data[("host", item)]
    m = lambda item: h(item) * MILLION
    revenue = h("revenue")
    near("Host: total revenues in the table = revenue in XBRL", revenue, m("total_revenues_musd"))
    nights = m("rooms_revenue_musd") / h("revpar")
    sold = m("rooms_revenue_musd") / h("adr")
    nights_prior = m("rooms_revenue_musd_2024") / h("revpar_2024")
    sold_prior = m("rooms_revenue_musd_2024") / h("adr_2024")
    near(f"Host {YEAR}: nights sold / available = published occupancy", h("occupancy_pct") / PCT, sold / nights)
    near(f"Host {PRIOR}: nights sold / available = published occupancy", h("occupancy_pct_2024") / PCT, sold_prior / nights_prior)
    near(f"Host {YEAR}: (revenue - condominium sales) / nights = published Total RevPAR", h("total_revpar"),
         (m("total_revenues_musd") - m("condominium_sales_musd")) / nights)
    near(f"Host {YEAR}: RevPAR = ADR x occupancy", h("revpar"), h("adr") * h("occupancy_pct") / PCT)
    near("Host: revenue - costs = operating income", h("operating_income"), revenue - h("costs_and_expenses"))
    near("Host: operating income - interest + other gains + interest income + equity income = income before tax",
         h("income_before_tax"), h("operating_income") - h("interest_expense") + h("other_gains") + h("interest_and_other_income")
         + h("equity_investments_income"))
    near("Host: income before tax - tax = net income", h("net_income"), h("income_before_tax") - h("income_tax"))
    hotel_lines = ["rooms_expense_musd", "food_beverage_expense_musd", "support_expense_musd", "management_fees_musd",
                   "other_property_expense_musd", "depreciation_musd"]
    near("Host: property-level expense lines add up to the table total", m("total_property_expenses_musd"),
         sum(m(x) for x in hotel_lines))
    near("Host: depreciation in the table = depreciation in XBRL", h("depreciation"), m("depreciation_musd"))
    outside = h("costs_and_expenses") - m("total_property_expenses_musd")
    near("Host: costs outside the hotels = corporate expenses + cost of condominiums sold - insurance gain", outside,
         h("general_and_administrative") + m("condominium_cost_musd") - h("insurance_gain"))

    slices = [
        ("host_rooms_cost_per_night", "Rooms expenses (staff, housekeeping, front desk)", m("rooms_expense_musd")),
        ("host_food_beverage_cost_per_night", "Food and beverage expenses", m("food_beverage_expense_musd")),
        ("host_support_cost_per_night", "Other departmental and support expenses", m("support_expense_musd")),
        ("host_property_cost_per_night", "Other property-level expenses", m("other_property_expense_musd")),
        ("host_management_fees_per_night", "Management fees paid to the companies that run the hotels", m("management_fees_musd")),
        ("host_depreciation_per_night", "Depreciation and amortization", m("depreciation_musd")),
        ("host_corporate_other_per_night", "Costs outside the hotels: corporate expenses and condominiums sold, less insurance gain",
         outside),
        ("host_interest_per_night", "Interest expense", h("interest_expense")),
        ("host_gains_other_income_per_night", "Gains outside operations (hotel sales, interest income, equity income), as a negative",
         -(h("other_gains") + h("interest_and_other_income") + h("equity_investments_income"))),
        ("host_income_tax_per_night", "Income tax", h("income_tax")),
        ("host_net_income_per_night", "Net income kept by the owner", h("net_income")),
    ]
    near("Host: the night's slices add back up to total revenue", revenue, sum(v for _, _, v in slices))
    put("host_revenue_per_night", revenue / nights, "usd", "Host: total revenue per available room night", "revenue / available nights")
    for key, label, value in slices:
        put(key, value / nights, "usd", f"Host: {label}, per available room night", "line / available nights")
    put("host_net_income_per_night_2024", h(f"net_income_{PRIOR}") / nights_prior, "usd", "Host: net income per available night, 2024",
        "net income / available nights")
    put("host_net_income_per_night_sold", h("net_income") / sold, "usd", "Host: net income per room night sold", "net income / nights sold")
    gain = m("gain_on_hotel_sales_musd")
    check("Host: gain on hotel sales is part of other gains", gain <= h("other_gains"), f"{gain:,.0f} <= {h('other_gains'):,.0f}")
    put("host_gain_on_hotel_sales", gain, "usd", "Host: gain on selling hotels in 2025", "10-K text")
    put("host_net_income_per_night_without_sales", (h("net_income") - gain) / nights, "usd",
        "Host: net income without the gain on hotel sales, per available night", "(net income - gain) / available nights")
    put("host_adr", h("adr"), "usd", "Host: average daily rate (all hotels, effective basis)", "published")
    put("host_adr_2024", h("adr_2024"), "usd", "Host: average daily rate, 2024", "published")
    put("host_revpar", h("revpar"), "usd", "Host: rooms revenue per available room night (RevPAR)", "published")
    put("host_occupancy", h("occupancy_pct") / PCT, "share", "Host: occupancy", "published")
    put("host_hotels", h("hotels"), "count", "Host: consolidated hotels at year end", "published")
    put("host_average_rooms", nights / DAYS, "count", "Host: rooms in operation, average for the year", "available nights / 365")
    put("host_available_room_nights", nights, "count", "Host: available room nights in the year", "rooms revenue / RevPAR")
    put("host_management_fees_share", m("management_fees_musd") / revenue, "share", "Host: management fees as a share of revenue",
        "management fees / revenue")

    comp_nights = h("comparable_rooms") * DAYS
    near("Host comparable hotels: revenue / (rooms x 365) = published Total RevPAR", h("comparable_total_revpar"),
         m("comparable_revenues_musd") / comp_nights)
    near("Host comparable hotels: EBITDA / revenue = published margin", h("comparable_ebitda_margin_pct") / PCT,
         h("comparable_ebitda_musd") / h("comparable_revenues_musd"))
    put("host_comparable_hotel_ebitda_per_night", m("comparable_ebitda_musd") / comp_nights, "usd",
        "Host: comparable hotels' EBITDA (before interest, depreciation and corporate costs), per available night",
        "comparable hotel EBITDA / (comparable rooms x 365)")

    ppe = h("gross_property")
    near("Host: land + buildings + fixtures + construction = gross property", ppe,
         h("land") + h("buildings") + h("fixtures") + h("construction_in_progress"))
    capex = -m("capex_musd")
    near("Host: capital expenditures in the cash flow = improvements + other assets in XBRL", capex,
         h("payments_capital_improvements") + h("payments_other_productive_assets"))
    rooms = nights / DAYS
    put("host_property_cost_per_room", ppe / rooms, "usd", "Host: gross property cost per room (historical cost on the balance sheet)",
        "gross property / average rooms")
    put("host_gross_property", ppe, "usd", "Host: gross property cost on the balance sheet", "XBRL")
    put("host_share_depreciated", h("accumulated_depreciation") / ppe, "share", "Host: share of the property cost already depreciated",
        "accumulated depreciation / gross property")
    put("host_average_hotel_age", h("average_hotel_age_years"), "count", "Host: average age of its hotels", "10-K text")
    put("host_debt_per_room", h("debt") / rooms, "usd", "Host: debt per room", "debt / average rooms")
    put("host_capex_per_night", capex / nights, "usd", "Host: capital expenditures per available night", "capex / available nights")
    put("host_net_income_on_gross_property", h("net_income") / ppe, "share", "Host: net income as a share of gross property cost",
        "net income / gross property")
    put("host_return_on_assets", h("net_income") / h("total_assets"), "share", "Host: net income as a share of total assets",
        "net income / total assets")
    put("host_years_of_profit_to_match_property", ppe / h("net_income"), "count",
        "Host: years of net income, at this year's pace, to match the gross property cost", "gross property / net income")

    total_price = total_rooms = 0
    for key in ("central_park", "nashville", "turtle_bay"):
        price, n = m(f"purchase_{key}_price_musd"), h(f"purchase_{key}_rooms")
        put(f"host_purchase_{key}_price_per_room", price / n, "usd", f"Host: price paid per room, 2024 purchase ({key})", "price / rooms")
        put(f"host_purchase_{key}_rooms", n, "count", f"Host: rooms, 2024 purchase ({key})", "10-K note")
        put(f"host_purchase_{key}_price", price, "usd", f"Host: price, 2024 purchase ({key})", "10-K note")
        total_price, total_rooms = total_price + price, total_rooms + n
    put("host_2024_purchases_price_per_room", total_price / total_rooms, "usd", "Host: average price per room of its 2024 purchases",
        "sum of prices / sum of rooms")
    key_money = m("marriott_key_money_musd")
    near("Host: Turtle Bay gross price - Marriott key money = net price in the note", m("purchase_turtle_bay_price_musd"),
         m("turtle_bay_gross_price_musd") - key_money)
    put("marriott_key_money_turtle_bay", key_money, "usd", "Marriott: key money paid to Host tied to the Ritz-Carlton conversion",
        "10-K text (Host)")
    put("marriott_key_money_per_room", key_money / h("purchase_turtle_bay_rooms"), "usd", "Marriott: key money per Turtle Bay room",
        "key money / rooms")

    # ===== 2. Park Hotels & Resorts =====
    p = lambda item: data[("park", item)]
    core = [float(r["rooms"]) for r in park_list if r["group"] == "core"]
    non_core = [float(r["rooms"]) for r in park_list if r["group"] == "non_core"]
    near("Park: core hotels' rooms add up to the list subtotal", p("core_rooms_subtotal"), sum(core))
    near("Park: non-core hotels' rooms add up to the list subtotal", p("non_core_rooms_subtotal"), sum(non_core))
    check("Park: hotels in the list = count in the text", len(core) == p("core_hotels") and len(non_core) == p("non_core_hotels"),
          f"{len(core)} core, {len(non_core)} non-core")
    park_rooms = sum(core) + sum(non_core)
    pppe = p("gross_property")
    near("Park: land + buildings + furniture + construction = gross property", pppe,
         p("land") + p("buildings") + p("furniture") + p("construction_in_progress"))
    put("park_property_cost_per_room", pppe / park_rooms, "usd", "Park: gross property cost per room of its consolidated hotels",
        "gross property / rooms (Item 2 list)")
    put("park_rooms", park_rooms, "count", "Park: rooms of its consolidated hotels", "sum of the Item 2 list")
    put("park_hotels", p("core_hotels") + p("non_core_hotels"), "count", "Park: consolidated hotels", "10-K text")
    put("park_net_income", p("net_income"), "usd", "Park: net income (loss), 2025", "XBRL: ProfitLoss")
    put("park_net_income_2024", p(f"net_income_{PRIOR}_musd") * MILLION, "usd", "Park: net income, 2024", "10-K reconciliation")
    put("park_impairment", p("impairment"), "usd", "Park: write-down of hotel values (impairment)", "XBRL")
    put("park_net_income_per_night", p("net_income") / (park_rooms * DAYS), "usd",
        "Park: net income (loss) per available room night (approximate)", "net income / (rooms x 365)")
    put("park_hotel_ebitda_per_night", p("hotel_adjusted_ebitda_musd") * MILLION / (park_rooms * DAYS), "usd",
        "Park: Hotel Adjusted EBITDA per available room night (approximate)", "Hotel Adjusted EBITDA / (rooms x 365)")
    put("park_debt_per_room", p("debt") / park_rooms, "usd", "Park: debt per room", "debt / rooms")
    put("park_net_income_on_gross_property", p("net_income") / pppe, "share", "Park: net income (loss) as a share of gross property",
        "net income / gross property")
    put("park_return_on_assets", p("net_income") / p("total_assets"), "share", "Park: net income (loss) as a share of total assets",
        "net income / total assets")
    put("park_management_fees_share", p("management_fees_musd") * MILLION / p("revenue"), "share",
        "Park: management fees as a share of revenue", "management fees / revenue")
    sf_rooms = p("sf_hilton_union_square_rooms") + p("sf_parc_55_rooms")
    put("park_sf_rooms", sf_rooms, "count", "Park: rooms of the two San Francisco hotels taken over by a receiver and sold in 2025",
        "10-K text")
    put("park_sf_loan", p("sf_loan_musd") * MILLION, "usd", "Park: loan on the San Francisco hotels, assumed by the buyer", "10-K text")
    put("park_sf_loan_per_room", p("sf_loan_musd") * MILLION / sf_rooms, "usd", "Park: San Francisco loan per room", "loan / rooms")

    # ===== 3. The brands =====
    property_per_room = {}
    for brand in ("marriott", "hilton", "hyatt"):
        b = lambda item: data[(brand, item)]
        if brand == "marriott":
            fees = b("gross_fees_musd") * MILLION
            near("Marriott: franchise + base + incentive = gross fees", fees,
                 (b("franchise_fees_musd") + b("base_management_fees_musd") + b("incentive_management_fees_musd")) * MILLION)
            near("Marriott: year-end 2024 rooms equal in the 2024 and 2025 10-Ks", b("rooms_2024_prior_10k"), b("rooms_2024"))
            put("marriott_cost_reimbursement_revenue", b("cost_reimbursement_revenue_musd") * MILLION, "usd",
                "Marriott: cost reimbursement revenue from the hotels it runs", "income statement")
        elif brand == "hilton":
            fees = (b("franchise_fees_musd") + b("base_management_fees_musd") + b("incentive_management_fees_musd")) * MILLION
            near("Hilton: base + incentive = published total management fees", b("total_management_fees_musd"),
                 b("base_management_fees_musd") + b("incentive_management_fees_musd"))
        else:
            fees = b("gross_fees_musd") * MILLION
            near("Hyatt: base + incentive + franchise = gross fees", fees,
                 (b("base_management_fees_musd") + b("incentive_management_fees_musd") + b("franchise_fees_musd")) * MILLION)
        check(f"{brand}: goodwill is larger than net property", b("goodwill") > b("net_property"),
              f"{b('goodwill') / MILLION:,.0f} vs {b('net_property') / MILLION:,.0f} million")
        nights_b = (b("rooms_2024") + b("rooms")) / 2 * DAYS
        put(f"{brand}_fees", fees, "usd", f"{brand}: fees for the year (franchise, management, incentive)", "10-K")
        put(f"{brand}_rooms", b("rooms"), "count", f"{brand}: system rooms at year end", "10-K text")
        put(f"{brand}_fees_per_night", fees / nights_b, "usd", f"{brand}: fees per system room night",
            "fees / (average of rooms at start and end of year x 365)")
        put(f"{brand}_net_income_per_night", b("net_income") / nights_b, "usd", f"{brand}: net income (loss) per system room night",
            "net income / (average rooms x 365)")
        put(f"{brand}_net_income", b("net_income"), "usd", f"{brand}: net income (loss) for the year", "XBRL: NetIncomeLoss")
        put(f"{brand}_net_income_on_fees", b("net_income") / fees, "share", f"{brand}: net income as a share of fees (not a margin)",
            "net income / fees")
        put(f"{brand}_return_on_assets", b("net_income") / b("total_assets"), "share", f"{brand}: net income as a share of total assets",
            "net income / total assets")
        put(f"{brand}_property_per_room", b("gross_property") / b("rooms"), "usd", f"{brand}: its own gross property per system room",
            "gross property / system rooms")
        property_per_room[brand] = b("gross_property") / b("rooms")
        if brand in ("marriott", "hilton"):
            near(f"{brand}: RevPAR = ADR x occupancy", b("revpar"), b("adr") * b("occupancy_pct") / PCT)
            put(f"{brand}_adr", b("adr"), "usd", f"{brand}: average daily rate, comparable system hotels, worldwide", "published")
            put(f"{brand}_fees_share_of_revpar", fees / nights_b / b("revpar"), "share", f"{brand}: fees per night as a share of RevPAR",
                "fees per night / RevPAR")
    put("host_vs_marriott_property_per_room", (ppe / rooms) / property_per_room["marriott"], "count",
        "How many times Host's property cost per room is Marriott's own property per system room", "ratio")

    (HERE / "numbers.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    for key in ("host_net_income_per_night", "marriott_net_income_per_night", "host_return_on_assets", "marriott_return_on_assets"):
        print(f"{key}: {out[key]['value']:.4f}")


if __name__ == "__main__":
    main()

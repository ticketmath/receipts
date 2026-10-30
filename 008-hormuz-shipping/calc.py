"""Ticket Math #008 - The Hormuz bypass: how much of the lost oil did the pipelines around the strait make up for?

Recomputes every number in the video from the files in data/ and writes numbers.json.
Standard library only, no network: run `python calc.py` in this folder.

Method
1. The main number (IEA, commentary of September 18, 2026, Kpler tanker-tracking data to September 12): the oil the
   higher flows through the bypass ports (Yanbu on the Red Sea, Fujairah on the Gulf of Oman) made up for since the war
   began, divided by the oil exports the strait lost over the same period. Both from the same publication.
2. Before the war: spare pipeline capacity from the EIA (June 2025) and the IEA factsheet (February 2026); Aramco's own
   account from its Q1 2026 earnings call; Gulf exports by month from the IEA Oil Market Report (April, July, October).
   Quarterly flows through the strait from the EIA's Short-Term Energy Outlook. No ratio mixes EIA and IEA figures.
3. Container ships: ships per day through the strait from IMF PortWatch (AIS signals), Q4 2025 against Q2 and Q3 2026;
   the Red Sea detour of 2024 (Bab el-Mandeb and the Cape of Good Hope, 2023 against 2024); Jebel Ali = DP World's group
   throughput minus its throughput without Jebel Ali (first half of 2026 against 2025); Maersk surcharges.
4. Prices (EIA): daily Brent around the start of the war; monthly Brent, U.S. regular gasoline and U.S. Gulf Coast jet
   fuel, February against September 2026. A calendar fact only: the EIA does not attribute the rise to Hormuz in numbers.
"""
import csv
import json
import statistics
from datetime import date
from pathlib import Path

HERE = Path(__file__).parent
WAR_STARTED = "2026-02-28"            # EIA: "military action in the Middle East on February 28"
IEA_DATA_TO = "2026-09-12"            # the IEA commentary's provisional data end here
QUARTERS = {"q4_2025": ("2025-10-01", "2025-12-31"), "q2_2026": ("2026-04-01", "2026-06-30"),
            "q3_2026": ("2026-07-01", "2026-09-30")}
RED_SEA = ("2023", "2024")            # before and after container lines left the Red Sea
MONTH_BEFORE, MONTH_AFTER = "2026-02", "2026-09"
FM1 = ("2026-10-17", "2026-11-16")    # Maersk FM1 relaunch notice (October 13, 2026): Qingdao departure, Khor Fakkan arrival
THOUSAND = 1000
MIN_DAYS = 90                         # a full quarter or year of daily data
TOLERANCE = 0.10                      # cross-checks between publications that define flows differently
DECIMALS = 6                          # rounding of the insurance multiples (0.03 / 0.0025 gives 12.000000000000002)

with open(HERE / "data" / "published_figures.csv", newline="", encoding="utf-8") as f:
    K = {r["key"]: float(r["value"]) for r in csv.DictReader(f)}
with open(HERE / "data" / "portwatch_daily.csv", newline="", encoding="utf-8") as f:
    ships = list(csv.DictReader(f))
with open(HERE / "data" / "eia_prices.csv", newline="", encoding="utf-8") as f:
    prices = {}
    for r in csv.DictReader(f):
        prices.setdefault(r["series"], {})[r["period"]] = float(r["value"])
out = {}


def put(key, value, unit, description):
    out[key] = {"value": value, "unit": unit, "description": description}


def check(label, ok, detail):
    print(f"{'ok  ' if ok else 'FAIL'} {label}: {detail}")
    if not ok:
        raise SystemExit(1)


def count(row, column):   # an empty cell counts as zero, as in the original count
    return int(row[column]) if row[column] != "" else 0


MBD = "million barrels per day"
for key, value in K.items():
    put(key, value, "as published", "published figure (see data/published_figures.csv)")

# 1. Oil: the bypass against the strait (IEA)
check("EIA: 2025 quarterly flows stay close to the 2024 flow (two EIA articles)",
      all(abs(K[f"strait_oil_q{q}_2025"] / K["strait_oil_2024"] - 1) <= TOLERANCE for q in (1, 2, 3, 4)),
      f"2024 {K['strait_oil_2024']}; 2025 {K['strait_oil_q1_2025']} to {K['strait_oil_q4_2025']}")
check("EIA: spare room is smaller than the pipelines' capacity", K["eia_spare_pipeline_capacity"] < K["east_west_capacity"]
      + K["uae_pipeline_capacity"], f"spare {K['eia_spare_pipeline_capacity']}")
check("IEA vs EIA: the IEA's 2025 flow is close to the EIA's Q4 2025",
      abs(K["iea_strait_exports_2025"] / K["strait_oil_q4_2025"] - 1) <= TOLERANCE,
      f"IEA {K['iea_strait_exports_2025']}; EIA {K['strait_oil_q4_2025']}")
put("bypass_share_of_strait_losses", K["bypass_offset"] / (K["strait_losses"] * THOUSAND), "share",
    "THE MAIN NUMBER: oil the higher bypass flows made up for, as a share of the oil exports the strait lost "
    "(late February to mid-September 2026)")
put("strait_losses_per_barrel_offset", K["strait_losses"] * THOUSAND / K["bypass_offset"], "barrels",
    "Barrels lost at the strait for every barrel the bypass made up for")
rise = K["bypass_exports_peak_jun_2026"] - K["bypass_exports_feb_2026"]
put("bypass_increase_to_peak", rise, MBD, "Rise in exports via Yanbu and Fujairah from February to the June peak")
put("bypass_peak_multiple", K["bypass_exports_peak_jun_2026"] / K["bypass_exports_feb_2026"], "times",
    "June peak exports via Yanbu and Fujairah, in multiples of February's")
check("IEA: at the peak, the bypass used the spare capacity estimated before the war",
      rise >= K["iea_spare_capacity_low"] - TOLERANCE, f"rise {rise:.1f}; range {K['iea_spare_capacity_low']}-{K['iea_spare_capacity_high']}")
check("IEA: the average daily offset is not above the rise at the peak", K["bypass_offset_per_day"] <= rise,
      f"average {K['bypass_offset_per_day']}; peak rise {rise:.1f}")
war_days = (date.fromisoformat(IEA_DATA_TO) - date.fromisoformat(WAR_STARTED)).days
prewar = K["strait_oil_aug_2026"] + K["strait_oil_aug_2026_below_prewar"]
check("IEA: the average daily loss sits between August's shortfall and the whole pre-war flow",
      K["strait_oil_aug_2026_below_prewar"] <= K["strait_losses"] * THOUSAND / war_days <= prewar,
      f"{K['strait_losses'] * THOUSAND / war_days:.1f} a day over {war_days} days")
put("strait_oil_prewar_iea", prewar, MBD, "Oil through the strait before the war (August + how far August was below)")
put("strait_oil_aug_2026_share_of_prewar", K["strait_oil_aug_2026"] / prewar, "share", "August 2026 flow as a share of pre-war")
check("IEA: August implied by the October report stays close to the September commentary's August",
      abs((K["strait_oil_sep_2026"] - K["strait_oil_rise_aug_to_sep_2026"]) / K["strait_oil_aug_2026"] - 1) <= TOLERANCE,
      f"{K['strait_oil_sep_2026'] - K['strait_oil_rise_aug_to_sep_2026']:.1f} vs {K['strait_oil_aug_2026']}")
put("strait_oil_sep_2026_share_of_prewar", K["strait_oil_sep_2026"] / prewar, "share",
    "September 2026 flow (October report) as a share of pre-war (September commentary)")
feb = K["gulf_exports_mar_2026"] + K["gulf_exports_drop_feb_to_mar_2026"]
check("IEA: February rebuilt from March + the drop is close to July's pre-war average",
      abs(feb / K["gulf_exports_prewar"] - 1) <= TOLERANCE, f"February {feb:.1f}; pre-war {K['gulf_exports_prewar']}")
put("gulf_exports_feb_2026", feb, MBD, "Gulf oil exports in February 2026 (March + the drop)")
put("gulf_exports_mar_2026_share_of_feb", K["gulf_exports_mar_2026"] / feb, "share", "March Gulf exports as a share of February's, bypass included")
put("gulf_exports_jun_2026_share_of_prewar", K["gulf_exports_jun_2026"] / K["gulf_exports_prewar"], "share",
    "June Gulf exports as a share of the pre-war average")
put("east_west_room_before_war", K["aramco_east_west_capacity"] - K["iea_east_west_in_use"], MBD,
    "East-West: Aramco's 7 minus what the IEA estimated in use in early 2026")

# 2. Oil: the EIA's quarterly view (no IEA figure in these ratios)
q4 = K["strait_oil_q4_2025"]
put("eia_spare_capacity_share", K["eia_spare_pipeline_capacity"] / q4, "share", "EIA spare pipeline room as a share of Q4 2025 flows")
put("strait_oil_without_pipeline_room_q4_2025", q4 - K["eia_spare_pipeline_capacity"], MBD, "Q4 2025 oil with no spare pipe to go around")
capacity = K["east_west_capacity"] + K["uae_pipeline_capacity"]
put("pipelines_combined_capacity", capacity, MBD, "East-West + UAE pipeline capacity")
put("pipelines_capacity_share", capacity / q4, "share", "That capacity as a share of Q4 2025 flows (if the pipes were empty, which they weren't)")
put("pipelines_max_capacity_share", (K["east_west_capacity_2019"] + K["uae_pipeline_capacity"]) / q4, "share",
    "The most ever used (East-West at 7 in 2019 + UAE) as a share of Q4 2025 flows")
for q in ("q1_2026", "q2_2026"):
    put(f"strait_oil_{q}_share_of_q4_2025", K[f"strait_oil_{q}"] / q4, "share", f"Oil through the strait, {q.upper()} as a share of Q4 2025")
put("strait_oil_lost_q2_2026", q4 - K["strait_oil_q2_2026"], MBD, "Oil that stopped going through the strait, Q2 2026 vs Q4 2025")
put("strait_lng_q2_2026_share_of_q4_2025", K["strait_lng_q2_2026"] / K["strait_lng_q4_2025"], "share", "LNG through the strait, Q2 2026 as a share of Q4 2025")

# 3. Container ships (IMF PortWatch)
hormuz = [r for r in ships if r["chokepoint"] == "Strait of Hormuz"]
mean = {}
for q, (start, end) in QUARTERS.items():
    days = [r for r in hormuz if start <= r["date"] <= end]
    check(f"PortWatch: {q} is complete", len(days) >= MIN_DAYS, f"{len(days)} days")
    for col in ("container_ships", "tankers", "all_ships"):
        mean[(q, col)] = statistics.fmean(count(r, col) for r in days)
    put(f"container_ships_per_day_{q}", mean[(q, "container_ships")], "ships per day", f"Container ships a day through Hormuz, {q} average")
    put(f"ships_per_day_{q}", mean[(q, "all_ships")], "ships per day", f"All ships a day through Hormuz, {q} average")
q3 = [r for r in hormuz if QUARTERS["q3_2026"][0] <= r["date"] <= QUARTERS["q3_2026"][1]]
zero = sum(1 for r in q3 if not count(r, "container_ships"))
put("days_without_container_ships_q3_2026", zero, "days", "Days in Q3 2026 with no container ship recorded in the strait")
put("days_without_container_ships_q3_2026_share", zero / len(q3), "share", "Share of Q3 2026 days with no container ship recorded")
for q in ("q2_2026", "q3_2026"):
    put(f"container_ships_{q}_share_of_q4_2025", mean[(q, "container_ships")] / mean[("q4_2025", "container_ships")], "share",
        f"Container ships through the strait, {q} as a share of Q4 2025")
put("tankers_q2_2026_share_of_q4_2025_ais", mean[("q2_2026", "tankers")] / mean[("q4_2025", "tankers")], "share",
    "Tankers through the strait, Q2 2026 as a share of Q4 2025, by AIS count (lower than the EIA flow: AIS undercounts in the crisis)")
check("Container ships fell further than oil (PortWatch vs EIA, Q2 2026)",
      mean[("q2_2026", "container_ships")] / mean[("q4_2025", "container_ships")] < K["strait_oil_q2_2026"] / q4,
      f"containers {mean[('q2_2026', 'container_ships')] / mean[('q4_2025', 'container_ships')]:.1%}; oil {K['strait_oil_q2_2026'] / q4:.1%}")
for name, key in (("Bab el-Mandeb Strait", "bab_el_mandeb"), ("Cape of Good Hope", "cape_of_good_hope")):
    for year in RED_SEA:
        days = [r for r in ships if r["chokepoint"] == name and r["date"].startswith(year)]
        check(f"PortWatch: {name} {year} is complete", len(days) >= MIN_DAYS, f"{len(days)} days")
        put(f"{key}_container_ships_per_day_{year}", statistics.fmean(count(r, "container_ships") for r in days), "ships per day",
            f"Container ships a day at {name}, {year} average")

# Jebel Ali (DP World) and the Maersk charges
ja = {h: K[f"dpworld_group_teu_{h}"] - K[f"dpworld_without_jebel_ali_teu_{h}"] for h in ("h1_2026", "h1_2025")}
check("DP World: the group total is above the total without Jebel Ali in both halves", all(x > 0 for x in ja.values()),
      f"Jebel Ali {ja['h1_2026']:.0f} vs {ja['h1_2025']:.0f} thousand TEU")
put("jebel_ali_teu_h1_2026", ja["h1_2026"] * THOUSAND, "TEU", "Jebel Ali throughput, first half of 2026")
put("jebel_ali_teu_h1_2025", ja["h1_2025"] * THOUSAND, "TEU", "Jebel Ali throughput, first half of 2025")
put("jebel_ali_h1_2026_share_of_h1_2025", ja["h1_2026"] / ja["h1_2025"], "share", "Jebel Ali, first half of 2026 as a share of 2025")
put("jebel_ali_teu_h1_2026_overland_included", ja["h1_2026"] * THOUSAND, "TEU",
    "Same count: DP World includes the boxes trucked in from Oman (Dubai Customs Notice 04/2026)")
put("maersk_40ft_extra_crossing_hormuz", K["maersk_emergency_increase_40ft"] + K["maersk_hormuz_transit_fee"], "usd per container",
    "Maersk: emergency increase for a 40-foot container to the Gulf plus the fee if its ship crosses Hormuz")
for side in ("low", "high"):
    put(f"war_risk_premium_multiple_{side}", round(K[f"war_risk_premium_july_{side}"] / K["war_risk_premium_before"], DECIMALS),
        "times", f"War-risk insurance in July 2026 ({side} end) in multiples of the pre-war rate")
put("maersk_fm1_days_qingdao_to_khor_fakkan", (date.fromisoformat(FM1[1]) - date.fromisoformat(FM1[0])).days, "days",
    "Maersk FM1 relaunch: Qingdao departure to Khor Fakkan arrival, outside the strait")

# 4. Prices (EIA)
brent = prices["PET.RBRTE.D"]
before = max(d for d in brent if d < WAR_STARTED)
after = {d: x for d, x in brent.items() if d >= WAR_STARTED}
peak = max(after, key=after.get)
check("EIA: daily Brent has data after the war began", len(after) > MIN_DAYS, f"{len(after)} days; latest {max(brent)}")
put("brent_last_day_before_war", brent[before], "usd per barrel", f"Brent on the last trading day before the war ({before})")
put("brent_peak_since_war", brent[peak], "usd per barrel", f"Highest daily Brent since the war began ({peak})")
put("brent_latest", brent[max(brent)], "usd per barrel", f"Brent on the latest day published ({max(brent)})")
for key, series, unit in (("brent_monthly", "PET.RBRTE.M", "usd per barrel"),
                          ("us_regular_gasoline", "PET.EMM_EPMR_PTE_NUS_DPG.M", "usd per gallon"),
                          ("us_gulf_coast_jet_fuel", "PET.EER_EPJK_PF4_RGC_DPG.M", "usd per gallon")):
    s = prices[series]
    check(f"EIA: {key} has {MONTH_BEFORE} and {MONTH_AFTER}", MONTH_BEFORE in s and MONTH_AFTER in s, f"{s.get(MONTH_BEFORE)}; {s.get(MONTH_AFTER)}")
    put(f"{key}_2026_02", s[MONTH_BEFORE], unit, f"{key.replace('_', ' ')}, monthly average, {MONTH_BEFORE}")
    put(f"{key}_2026_09", s[MONTH_AFTER], unit, f"{key.replace('_', ' ')}, monthly average, {MONTH_AFTER}")
    put(f"{key}_rise", s[MONTH_AFTER] - s[MONTH_BEFORE], unit, f"{key.replace('_', ' ')}, {MONTH_AFTER} minus {MONTH_BEFORE}")

(HERE / "numbers.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
print(f"{len(out)} numbers written to numbers.json")

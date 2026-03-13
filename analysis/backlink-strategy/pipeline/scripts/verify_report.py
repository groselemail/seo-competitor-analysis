#!/usr/bin/env python3
"""
Автоматическая верификация отчёта backlink-strategy.md
Проверяет числовые утверждения против JSON-агрегатов.
"""

import json
import re
import statistics
from pathlib import Path

BASE = Path("/mnt/c/freesoft")
INTER = BASE / "analysis/backlink-strategy/pipeline/intermediate"
REPORT = BASE / "reports/backlink-strategy.md"

# ── Load data ──────────────────────────────────────────────────
with open(INTER / "inventory.json") as f:
    inventory = json.load(f)
with open(INTER / "r1_language_links.json") as f:
    r1 = json.load(f)
with open(INTER / "r2_pbn_signals.json") as f:
    r2 = json.load(f)
with open(INTER / "r3_intersections.json") as f:
    r3 = json.load(f)
with open(INTER / "r4_link_profiles.json") as f:
    r4 = json.load(f)

report_text = REPORT.read_text(encoding="utf-8")

# ── Helpers ────────────────────────────────────────────────────
results = []

def check(name, report_val, json_val, tolerance=0.05):
    """Compare two values and record result."""
    if report_val is None or json_val is None:
        results.append({
            "check": name,
            "report_value": report_val,
            "json_value": json_val,
            "status": "SKIP",
            "severity": "info",
            "note": "Value not found"
        })
        return

    try:
        rv = float(report_val)
        jv = float(json_val)
    except (ValueError, TypeError):
        results.append({
            "check": name,
            "report_value": report_val,
            "json_value": json_val,
            "status": "SKIP",
            "severity": "info",
            "note": "Non-numeric comparison"
        })
        return

    delta = abs(rv - jv)

    if jv == 0:
        if rv == 0:
            status = "PASS"
            severity = "ok"
        elif delta <= 0.15:
            status = "PASS"
            severity = "rounding"
        else:
            status = "FAIL"
            severity = "critical"
    else:
        pct_diff = delta / abs(jv) * 100
        if delta <= 0.05:
            status = "PASS"
            severity = "ok"
        elif pct_diff <= 1.0:
            status = "PASS"
            severity = "rounding"
        elif pct_diff <= 5.0:
            status = "WARN"
            severity = "minor"
        elif pct_diff <= 20.0:
            status = "FAIL"
            severity = "major"
        else:
            status = "FAIL"
            severity = "critical"

    results.append({
        "check": name,
        "report_value": rv,
        "json_value": jv,
        "status": status,
        "delta": round(delta, 4),
        "severity": severity
    })

def compute_median(values):
    """Compute median from a list of values."""
    s = sorted(values)
    n = len(s)
    if n % 2 == 1:
        return s[n // 2]
    else:
        return (s[n // 2 - 1] + s[n // 2]) / 2

# ── All domains ────────────────────────────────────────────────
OUR_DOMAINS = ["freesoft.net", "freesoft.ru", "frees0ft.fr"]
COMPETITORS = ["softonic.com", "uptodown.com", "malavida.com", "softonic.ru",
               "trashbox.ru", "filehippo.com", "clubic.com", "01net.com", "commentcamarche.net"]
ALL_DOMAINS = OUR_DOMAINS + COMPETITORS

# ══════════════════════════════════════════════════════════════
# CHECK 1: INVENTORY
# ══════════════════════════════════════════════════════════════
print("CHECK 1: Inventory...")

# Report header: "~670K (659 669 после фильтрации gambling/adult)"
check("inventory.total_rows_raw", 669569, inventory["total_rows_raw"])
check("inventory.total_rows_after_gambling_filter", 659669, inventory["total_rows_after_gambling_filter"])
check("inventory.gambling_filtered_rows", 9900, inventory["gambling_filtered_rows"])

# Per-domain A_rows, B_rows, C_rows from report Appendix B table
appendix_b = {
    "freesoft.net": {"A": 3864, "B": 20361, "C": 3810},
    "freesoft.ru": {"A": 3257, "B": 5227, "C": 2852},
    "frees0ft.fr": {"A": 478, "B": 19, "C": 465},
    "softonic.com": {"A": 29904, "B": 28912, "C": 29518},
    "uptodown.com": {"A": 29888, "B": 29242, "C": 28335},
    "malavida.com": {"A": 13431, "B": None, "C": 12907},
    "softonic.ru": {"A": 4964, "B": None, "C": 4290},
    "trashbox.ru": {"A": 5322, "B": 16362, "C": 5125},
    "filehippo.com": {"A": 17715, "B": None, "C": 16924},
    "clubic.com": {"A": 17373, "B": None, "C": 17081},
    "01net.com": {"A": 20991, "B": None, "C": 19569},
    "commentcamarche.net": {"A": 13676, "B": None, "C": 13368},
}

for domain, vals in appendix_b.items():
    inv = inventory["per_domain_summary"].get(domain, {})
    if vals["A"] is not None:
        check(f"inventory.{domain}.A_rows", vals["A"], inv.get("A_rows"))
    if vals["B"] is not None:
        check(f"inventory.{domain}.B_rows", vals["B"], inv.get("B_rows"))
    if vals["C"] is not None:
        check(f"inventory.{domain}.C_rows", vals["C"], inv.get("C_rows"))

# Ahrefs limit files count
check("inventory.ahrefs_limit_files_count", 14, len(inventory["ahrefs_limit_files"]))

# ══════════════════════════════════════════════════════════════
# CHECK 2: R4 LINK PROFILES
# ══════════════════════════════════════════════════════════════
print("CHECK 2: R4 Link Profiles...")

# --- Per-domain overview ---
r4_report_overview = {
    "freesoft.net": {"dr": 51, "ref_domains": 3864},
    "freesoft.ru": {"dr": 59, "ref_domains": 3257},
    "frees0ft.fr": {"dr": 23, "ref_domains": 478},
    "softonic.com": {"dr": 86, "ref_domains": 29904},
    "uptodown.com": {"dr": 83, "ref_domains": 29888},
    "malavida.com": {"dr": 74, "ref_domains": 13431},
    "softonic.ru": {"dr": 37, "ref_domains": 4964},
    "trashbox.ru": {"dr": 45, "ref_domains": 5322},
    "filehippo.com": {"dr": 75, "ref_domains": 17715},
    "clubic.com": {"dr": 76, "ref_domains": 17373},
    "01net.com": {"dr": 79, "ref_domains": 20991},
    "commentcamarche.net": {"dr": 81, "ref_domains": 13676},
}

for domain, vals in r4_report_overview.items():
    r4d = r4["domains"][domain]
    check(f"r4.{domain}.dr", vals["dr"], r4d["overview"]["dr"])
    check(f"r4.{domain}.ref_domains", vals["ref_domains"], r4d["overview"]["total_ref_domains"])

# --- DR distribution ---
r4_report_dr = {
    "softonic.com": [26.2, 17.0, 15.3, 12.0, 8.0, 7.0, 5.1, 6.3, 2.2, 0.7],
    "uptodown.com": [54.4, 12.6, 9.5, 6.9, 5.5, 3.7, 2.6, 3.2, 1.2, 0.4],
    "malavida.com": [71.3, 7.8, 6.5, 3.9, 2.9, 2.6, 1.8, 2.0, 0.8, 0.4],
    "softonic.ru": [85.0, 5.4, 4.0, 2.0, 1.2, 0.9, 0.8, 0.4, 0.1, 0.2],
    "trashbox.ru": [76.8, 5.8, 5.8, 3.4, 2.3, 2.1, 1.8, 1.3, 0.4, 0.3],
    "filehippo.com": [62.0, 8.8, 8.1, 6.1, 4.0, 3.9, 2.6, 2.9, 1.1, 0.4],
    "clubic.com": [52.4, 11.0, 10.7, 7.9, 5.4, 4.1, 3.1, 3.6, 1.3, 0.5],
    "01net.com": [57.2, 9.8, 9.3, 7.1, 4.7, 4.0, 2.9, 3.4, 1.3, 0.4],
    "commentcamarche.net": [48.4, 12.0, 11.2, 8.9, 5.5, 4.9, 3.4, 3.7, 1.6, 0.5],
    "freesoft.net": [91.9, 3.5, 2.4, 0.6, 0.5, 0.6, 0.1, 0.2, 0.1, 0.1],
    "freesoft.ru": [58.9, 13.4, 11.5, 5.4, 3.0, 3.3, 2.0, 1.7, 0.5, 0.3],
    "frees0ft.fr": [74.9, 10.9, 7.9, 3.1, 1.0, 1.3, 0.6, 0.0, 0.0, 0.2],
}

dr_buckets = ["0-10", "11-20", "21-30", "31-40", "41-50", "51-60", "61-70", "71-80", "81-90", "91-100"]

for domain, vals in r4_report_dr.items():
    r4d = r4["domains"][domain]["dr_distribution"]["buckets"]
    for i, bucket in enumerate(dr_buckets):
        check(f"r4.{domain}.dr_bucket.{bucket}", vals[i], r4d[bucket]["pct"])

# --- DR stats (mean, median) ---
r4_report_stats = {
    "freesoft.net": {"mean": 3.2, "median": 0},
    "freesoft.ru": {"mean": 15.2, "median": 7},
    "frees0ft.fr": {"mean": 9.1, "median": 6},
}

for domain, vals in r4_report_stats.items():
    r4d = r4["domains"][domain]["dr_distribution"]["stats"]
    check(f"r4.{domain}.dr_mean", vals["mean"], r4d["mean"])
    check(f"r4.{domain}.dr_median", vals["median"], r4d["median"])

# --- Follow ratio ---
r4_report_follow = {
    "softonic.com": {"dofollow": 72.0, "nofollow": 28.0, "ugc": 5.1, "sponsored": 0.2},
    "uptodown.com": {"dofollow": 66.1, "nofollow": 33.9, "ugc": 7.9, "sponsored": 0.1},
    "commentcamarche.net": {"dofollow": 76.8, "nofollow": 23.2, "ugc": 4.4, "sponsored": 0.0},
    "01net.com": {"dofollow": 81.7, "nofollow": 18.3, "ugc": 2.2, "sponsored": 0.0},
    "clubic.com": {"dofollow": 79.4, "nofollow": 20.6, "ugc": 2.9, "sponsored": 0.0},
    "filehippo.com": {"dofollow": 70.2, "nofollow": 29.8, "ugc": 4.6, "sponsored": 0.0},
    "malavida.com": {"dofollow": 70.3, "nofollow": 29.7, "ugc": 1.9, "sponsored": 0.0},
    "trashbox.ru": {"dofollow": 70.3, "nofollow": 29.7, "ugc": 2.6, "sponsored": 0.0},
    "softonic.ru": {"dofollow": 70.7, "nofollow": 29.3, "ugc": 0.2, "sponsored": 0.0},
    "freesoft.net": {"dofollow": 74.9, "nofollow": 25.1, "ugc": 0.1, "sponsored": 0.0},
    "freesoft.ru": {"dofollow": 35.5, "nofollow": 64.5, "ugc": 13.3, "sponsored": 0.1},
    "frees0ft.fr": {"dofollow": 4.3, "nofollow": 95.7, "ugc": 0.0, "sponsored": 0.0},
}

for domain, vals in r4_report_follow.items():
    r4d = r4["domains"][domain]["follow_ratio"]
    check(f"r4.{domain}.dofollow_pct", vals["dofollow"], r4d["dofollow"]["pct"])
    check(f"r4.{domain}.nofollow_pct", vals["nofollow"], r4d["nofollow"]["pct"])
    check(f"r4.{domain}.ugc_pct", vals["ugc"], r4d["ugc"]["pct"])
    check(f"r4.{domain}.sponsored_pct", vals["sponsored"], r4d["sponsored"]["pct"])

# --- Link types ---
r4_report_ltypes = {
    "softonic.com": {"text": 96.1, "image": 3.7},
    "uptodown.com": {"text": 94.5, "image": 4.7},
    "malavida.com": {"text": 81.4, "image": 18.5},
    "softonic.ru": {"text": 99.3, "image": 0.7},
    "trashbox.ru": {"text": 90.7, "image": 9.1},
    "filehippo.com": {"text": 96.6, "image": 3.2},
    "clubic.com": {"text": 90.5, "image": 9.0},
    "01net.com": {"text": 87.2, "image": 12.1},
    "commentcamarche.net": {"text": 96.1, "image": 3.5},
    "freesoft.net": {"text": 99.6, "image": 0.4},
    "freesoft.ru": {"text": 96.2, "image": 3.5},
    "frees0ft.fr": {"text": 98.5, "image": 1.5},
}

for domain, vals in r4_report_ltypes.items():
    r4d = r4["domains"][domain]["link_types"]
    check(f"r4.{domain}.text_pct", vals["text"], r4d["text"]["pct"])
    check(f"r4.{domain}.image_pct", vals["image"], r4d["image"]["pct"])

# --- Anchor profile ---
r4_report_anchors = {
    "softonic.com": {"branded": 16.6, "exact_match": 31.6, "url": 2.5, "generic": 0.3, "other": 49.0},
    "uptodown.com": {"branded": 20.9, "exact_match": 2.9, "url": 2.0, "generic": 0.5, "other": 73.7},
    "malavida.com": {"branded": 8.8, "exact_match": 6.3, "url": 4.2, "generic": 0.3, "other": 80.5},
    "softonic.ru": {"branded": 3.7, "exact_match": 95.4, "url": 0.3, "generic": 0.0, "other": 0.6},
    "trashbox.ru": {"branded": 4.3, "exact_match": 1.6, "url": 7.7, "generic": 0.2, "other": 86.2},
    "filehippo.com": {"branded": 4.9, "exact_match": 61.2, "url": 7.7, "generic": 0.6, "other": 25.7},
    "clubic.com": {"branded": 13.6, "exact_match": 1.1, "url": 31.5, "generic": 1.4, "other": 52.5},
    "01net.com": {"branded": 8.4, "exact_match": 1.7, "url": 27.4, "generic": 1.3, "other": 61.1},
    "commentcamarche.net": {"branded": 10.4, "exact_match": 1.8, "url": 26.6, "generic": 1.1, "other": 60.1},
    "freesoft.net": {"branded": 1.4, "exact_match": 1.0, "url": 1.1, "generic": 0.0, "other": 96.5},
    "freesoft.ru": {"branded": 7.2, "exact_match": 8.6, "url": 20.6, "generic": 0.6, "other": 63.0},
    "frees0ft.fr": {"branded": 0.2, "exact_match": 0.0, "url": 20.0, "generic": 0.0, "other": 79.9},
}

for domain, vals in r4_report_anchors.items():
    r4d = r4["domains"][domain]["anchor_profile"]["type_distribution"]
    for atype, rval in vals.items():
        json_val = r4d.get(atype, {}).get("pct", 0.0)
        check(f"r4.{domain}.anchor.{atype}", rval, json_val)

# --- Spam ratio ---
r4_report_spam = {
    "softonic.com": {"count": 6425, "pct": 21.5},
    "commentcamarche.net": {"count": 3381, "pct": 24.7},
    "clubic.com": {"count": 4619, "pct": 26.6},
    "01net.com": {"count": 6703, "pct": 31.9},
    "uptodown.com": {"count": 12668, "pct": 42.4},
    "filehippo.com": {"count": 7664, "pct": 43.3},
    "malavida.com": {"count": 8065, "pct": 60.1},
    "trashbox.ru": {"count": 3856, "pct": 72.5},
    "softonic.ru": {"count": 4056, "pct": 81.7},
    "freesoft.ru": {"count": 2274, "pct": 69.8},
    "frees0ft.fr": {"count": 425, "pct": 88.9},
    "freesoft.net": {"count": 3452, "pct": 89.3},
}

for domain, vals in r4_report_spam.items():
    r4d = r4["domains"][domain]["spam_ratio"]
    check(f"r4.{domain}.spam_count", vals["count"], r4d["count"])
    check(f"r4.{domain}.spam_pct", vals["pct"], r4d["pct"])

# --- Link age ---
r4_report_age = {
    "softonic.com": {"<1y": 28.4, "1-3y": 28.6, "3-5y": 17.4, ">5y": 25.7, "growth": 8489},
    "uptodown.com": {"<1y": 45.4, "1-3y": 28.1, "3-5y": 14.3, ">5y": 12.2, "growth": 13573},
    "malavida.com": {"<1y": 66.3, "1-3y": 18.1, "3-5y": 8.5, ">5y": 7.1, "growth": 8892},
    "softonic.ru": {"<1y": 88.1, "1-3y": 9.9, "3-5y": 0.9, ">5y": 1.1, "growth": 4375},
    "trashbox.ru": {"<1y": 80.6, "1-3y": 10.7, "3-5y": 4.2, ">5y": 4.4, "growth": 4290},
    "filehippo.com": {"<1y": 46.4, "1-3y": 18.2, "3-5y": 12.8, ">5y": 22.6, "growth": 8219},
    "clubic.com": {"<1y": 40.6, "1-3y": 21.3, "3-5y": 12.6, ">5y": 25.4, "growth": 7056},
    "01net.com": {"<1y": 44.9, "1-3y": 19.3, "3-5y": 11.9, ">5y": 23.9, "growth": 9421},
    "commentcamarche.net": {"<1y": 30.0, "1-3y": 23.3, "3-5y": 15.8, ">5y": 30.9, "growth": 4096},
    "freesoft.net": {"<1y": 97.3, "1-3y": 2.7, "3-5y": 0.0, ">5y": 0.0, "growth": 3761},
    "freesoft.ru": {"<1y": 51.2, "1-3y": 29.7, "3-5y": 5.7, ">5y": 13.4, "growth": 1667},
    "frees0ft.fr": {"<1y": 97.7, "1-3y": 1.5, "3-5y": 0.8, ">5y": 0.0, "growth": 467},
}

for domain, vals in r4_report_age.items():
    r4d = r4["domains"][domain]["link_age"]
    buckets = r4d["buckets"]
    total = sum(buckets.values())
    if total > 0:
        for age_key in ["<1y", "1-3y", "3-5y", ">5y"]:
            json_pct = round(buckets[age_key] / total * 100, 1)
            check(f"r4.{domain}.age.{age_key}_pct", vals[age_key], json_pct)
    check(f"r4.{domain}.growth_12m", vals["growth"], r4d["growth_last_12m"])

# ══════════════════════════════════════════════════════════════
# CHECK 2b: BENCHMARK MEDIANS (recalculated from 9 competitors)
# ══════════════════════════════════════════════════════════════
print("CHECK 2b: Benchmark medians...")

# Recalculate medians from 9 competitors
comp_dr = [r4["domains"][d]["overview"]["dr"] for d in COMPETITORS]
comp_ref = [r4["domains"][d]["overview"]["total_ref_domains"] for d in COMPETITORS]
comp_dofollow = [r4["domains"][d]["follow_ratio"]["dofollow"]["pct"] for d in COMPETITORS]
comp_nofollow = [r4["domains"][d]["follow_ratio"]["nofollow"]["pct"] for d in COMPETITORS]
comp_text = [r4["domains"][d]["link_types"]["text"]["pct"] for d in COMPETITORS]
comp_image = [r4["domains"][d]["link_types"]["image"]["pct"] for d in COMPETITORS]
comp_branded = [r4["domains"][d]["anchor_profile"]["type_distribution"]["branded"]["pct"] for d in COMPETITORS]
comp_exact = [r4["domains"][d]["anchor_profile"]["type_distribution"].get("exact_match", {}).get("pct", 0.0) for d in COMPETITORS]
comp_url = [r4["domains"][d]["anchor_profile"]["type_distribution"].get("url", {}).get("pct", 0.0) for d in COMPETITORS]
comp_other = [r4["domains"][d]["anchor_profile"]["type_distribution"].get("other", {}).get("pct", 0.0) for d in COMPETITORS]
comp_generic = [r4["domains"][d]["anchor_profile"]["type_distribution"].get("generic", {}).get("pct", 0.0) for d in COMPETITORS]
comp_spam = [r4["domains"][d]["spam_ratio"]["pct"] for d in COMPETITORS]
comp_dr_mean = [r4["domains"][d]["dr_distribution"]["stats"]["mean"] for d in COMPETITORS]
comp_dr_median = [r4["domains"][d]["dr_distribution"]["stats"]["median"] for d in COMPETITORS]
comp_growth = [r4["domains"][d]["link_age"]["growth_last_12m"] for d in COMPETITORS]

# Link age >5y pcts
comp_age_5y = []
for d in COMPETITORS:
    buckets = r4["domains"][d]["link_age"]["buckets"]
    total = sum(buckets.values())
    comp_age_5y.append(round(buckets[">5y"] / total * 100, 1) if total > 0 else 0)

# Report benchmark values from the main benchmark table
benchmark_report = {
    "DR": 76,
    "Ref.domains": 17373,
    "Dofollow%": 70.7,
    "Nofollow%": 29.3,
    "Text%": 94.5,
    "Image%": 4.7,
    "Branded%": 8.8,
    "Exact%": 2.9,
    "URL%": 7.7,
    "Other%": 60.1,
    "Generic%": 0.5,
    "Spam%": 42.4,
    "DR_mean": 17.8,
    "DR_median": 6,
    "Growth_12m": 8219,
    "Age_5y%": 22.6,
}

calc_medians = {
    "DR": compute_median(comp_dr),
    "Ref.domains": compute_median(comp_ref),
    "Dofollow%": compute_median(comp_dofollow),
    "Nofollow%": compute_median(comp_nofollow),
    "Text%": compute_median(comp_text),
    "Image%": compute_median(comp_image),
    "Branded%": compute_median(comp_branded),
    "Exact%": compute_median(comp_exact),
    "URL%": compute_median(comp_url),
    "Other%": compute_median(comp_other),
    "Generic%": compute_median(comp_generic),
    "Spam%": compute_median(comp_spam),
    "DR_mean": compute_median(comp_dr_mean),
    "DR_median": compute_median(comp_dr_median),
    "Growth_12m": compute_median(comp_growth),
    "Age_5y%": compute_median(comp_age_5y),
}

for metric, report_val in benchmark_report.items():
    calc_val = calc_medians[metric]
    check(f"benchmark.median.{metric}", report_val, round(calc_val, 1))

# DR bucket medians
dr_bucket_medians_report = [57.2, 9.8, 9.3, 6.9, 4.7, 3.9, 2.6, 3.2, 1.1, 0.4]
for i, bucket in enumerate(dr_buckets):
    comp_vals = [r4["domains"][d]["dr_distribution"]["buckets"][bucket]["pct"] for d in COMPETITORS]
    calc_med = compute_median(comp_vals)
    check(f"benchmark.dr_bucket_median.{bucket}", dr_bucket_medians_report[i], round(calc_med, 1))

# ══════════════════════════════════════════════════════════════
# CHECK 3: R2 PBN SIGNALS
# ══════════════════════════════════════════════════════════════
print("CHECK 3: R2 PBN signals...")

r2_report = {
    "freesoft.net": {"spam": 89.3, "low_dr": 89.5, "susp_tld": 71.6, "exclusive": 31, "spikes": 4, "score": 73.5, "ref": 3864},
    "softonic.ru": {"spam": 81.7, "low_dr": 82.1, "susp_tld": 57.5, "exclusive": 129, "spikes": 7, "score": 67.0, "ref": 4964},
    "trashbox.ru": {"spam": 72.5, "low_dr": 73.9, "susp_tld": 46.1, "exclusive": 890, "spikes": 16, "score": 63.4, "ref": 5322},
    "frees0ft.fr": {"spam": 88.9, "low_dr": 64.0, "susp_tld": 27.8, "exclusive": 1, "spikes": 2, "score": 55.1, "ref": 478},
    "malavida.com": {"spam": 60.1, "low_dr": 69.9, "susp_tld": 26.4, "exclusive": 2456, "spikes": 19, "score": 54.6, "ref": 13431},
    "freesoft.ru": {"spam": 69.8, "low_dr": 53.3, "susp_tld": 11.1, "exclusive": 908, "spikes": 19, "score": 50.0, "ref": 3257},
    "filehippo.com": {"spam": 43.3, "low_dr": 60.8, "susp_tld": 20.6, "exclusive": 6403, "spikes": 17, "score": 44.0, "ref": 17715},
    "01net.com": {"spam": 31.9, "low_dr": 56.1, "susp_tld": 15.0, "exclusive": 7100, "spikes": 31, "score": 44.0, "ref": 20991},
    "uptodown.com": {"spam": 42.4, "low_dr": 53.6, "susp_tld": 10.8, "exclusive": 15034, "spikes": 25, "score": 43.4, "ref": 29888},
    "clubic.com": {"spam": 26.6, "low_dr": 51.1, "susp_tld": 8.6, "exclusive": 5649, "spikes": 28, "score": 38.2, "ref": 17373},
    "commentcamarche.net": {"spam": 24.7, "low_dr": 46.8, "susp_tld": 5.2, "exclusive": 5660, "spikes": 30, "score": 36.7, "ref": 13676},
    "softonic.com": {"spam": 21.5, "low_dr": 25.5, "susp_tld": 1.7, "exclusive": 17262, "spikes": 27, "score": 27.8, "ref": 29904},
}

for domain, vals in r2_report.items():
    r2d = r2["domains"][domain]["summary"]
    check(f"r2.{domain}.spam_pct", vals["spam"], r2d["spam_pct"])
    check(f"r2.{domain}.low_dr_pct", vals["low_dr"], r2d["low_dr_pct"])
    check(f"r2.{domain}.susp_tld_pct", vals["susp_tld"], r2d["suspicious_tld_pct"])
    check(f"r2.{domain}.exclusive_count", vals["exclusive"], r2d["exclusive_domains_count"])
    check(f"r2.{domain}.spikes_count", vals["spikes"], r2d["temporal_spikes_count"])
    check(f"r2.{domain}.ref_domains", vals["ref"], r2d["total_ref_domains"])

# Verify composite scores using formula: spam*0.35 + low_dr*0.25 + susp_tld*0.25 + norm_spikes*0.15
# We need to check what normalized_spikes means
# Max spikes = 31 (01net.com), so norm = spikes/31*100
max_spikes = max(r2["domains"][d]["summary"]["temporal_spikes_count"] for d in ALL_DOMAINS)
for domain, vals in r2_report.items():
    r2d = r2["domains"][domain]["summary"]
    spam = r2d["spam_pct"]
    low_dr = r2d["low_dr_pct"]
    susp_tld = r2d["suspicious_tld_pct"]
    spikes = r2d["temporal_spikes_count"]
    norm_spikes = (spikes / max_spikes) * 100 if max_spikes > 0 else 0
    calc_score = spam * 0.35 + low_dr * 0.25 + susp_tld * 0.25 + norm_spikes * 0.15
    check(f"r2.{domain}.composite_score_verify", vals["score"], round(calc_score, 1))

# ══════════════════════════════════════════════════════════════
# CHECK 4: R3 INTERSECTIONS - JACCARD
# ══════════════════════════════════════════════════════════════
print("CHECK 4: R3 Jaccard matrix...")

r3_domains = r3["overlap_matrix"]["domains"]
r3_counts = r3["overlap_matrix"]["counts"]

# Report Jaccard values (from the matrix table)
report_jaccard = {
    ("freesoft.net", "freesoft.ru"): 0.14,
    ("freesoft.net", "frees0ft.fr"): 0.11,
    ("freesoft.net", "softonic.com"): 0.02,
    ("freesoft.net", "uptodown.com"): 0.10,
    ("freesoft.net", "malavida.com"): 0.28,
    ("freesoft.net", "softonic.ru"): 0.58,
    ("freesoft.net", "trashbox.ru"): 0.44,
    ("freesoft.net", "filehippo.com"): 0.21,
    ("freesoft.net", "clubic.com"): 0.09,
    ("freesoft.net", "01net.com"): 0.14,
    ("freesoft.net", "commentcamarche.net"): 0.06,
    ("freesoft.ru", "frees0ft.fr"): 0.13,
    ("freesoft.ru", "softonic.com"): 0.04,
    ("freesoft.ru", "uptodown.com"): 0.06,
    ("freesoft.ru", "malavida.com"): 0.12,
    ("freesoft.ru", "softonic.ru"): 0.23,
    ("freesoft.ru", "trashbox.ru"): 0.19,
    ("freesoft.ru", "filehippo.com"): 0.08,
    ("freesoft.ru", "clubic.com"): 0.06,
    ("freesoft.ru", "01net.com"): 0.05,
    ("freesoft.ru", "commentcamarche.net"): 0.06,
    ("frees0ft.fr", "softonic.com"): 0.01,
    ("frees0ft.fr", "uptodown.com"): 0.02,
    ("frees0ft.fr", "malavida.com"): 0.03,
    ("frees0ft.fr", "softonic.ru"): 0.09,
    ("frees0ft.fr", "trashbox.ru"): 0.07,
    ("frees0ft.fr", "filehippo.com"): 0.03,
    ("frees0ft.fr", "clubic.com"): 0.02,
    ("frees0ft.fr", "01net.com"): 0.02,
    ("frees0ft.fr", "commentcamarche.net"): 0.03,
    ("softonic.com", "uptodown.com"): 0.16,
    ("softonic.com", "filehippo.com"): 0.13,
    ("softonic.com", "clubic.com"): 0.07,
    ("softonic.com", "01net.com"): 0.06,
    ("softonic.com", "commentcamarche.net"): 0.07,
    ("uptodown.com", "malavida.com"): 0.22,
    ("uptodown.com", "filehippo.com"): 0.19,
    ("uptodown.com", "clubic.com"): 0.09,
    ("uptodown.com", "01net.com"): 0.11,
    ("malavida.com", "softonic.ru"): 0.33,
    ("malavida.com", "trashbox.ru"): 0.27,
    ("malavida.com", "filehippo.com"): 0.28,
    ("malavida.com", "clubic.com"): 0.15,
    ("malavida.com", "01net.com"): 0.21,
    ("softonic.ru", "trashbox.ru"): 0.50,
    ("softonic.ru", "filehippo.com"): 0.22,
    ("softonic.ru", "clubic.com"): 0.10,
    ("softonic.ru", "01net.com"): 0.17,
    ("trashbox.ru", "filehippo.com"): 0.19,
    ("trashbox.ru", "clubic.com"): 0.11,
    ("trashbox.ru", "01net.com"): 0.16,
    ("clubic.com", "01net.com"): 0.32,
    ("clubic.com", "commentcamarche.net"): 0.22,
    ("01net.com", "commentcamarche.net"): 0.20,
}

for (d1, d2), report_val in report_jaccard.items():
    i = r3_domains.index(d1)
    j = r3_domains.index(d2)
    inter = r3_counts[i][j]
    union = r3_counts[i][i] + r3_counts[j][j] - inter
    calc_jacc = round(inter / union, 2) if union > 0 else 0
    check(f"r3.jaccard.{d1}_x_{d2}", report_val, calc_jacc)

# ══════════════════════════════════════════════════════════════
# CHECK 5: R3 MULTI-COMPETITOR DOMAINS
# ══════════════════════════════════════════════════════════════
print("CHECK 5: R3 multi-competitor domains...")

mcd = r3["multi_competitor_domains"]
p3_count = mcd["3_plus_competitors"]["count"]
e2_count = mcd["exactly_2_competitors"]["count"]
total_2plus = p3_count + e2_count

# Report says "28 178 доменов ссылаются на 2+ конкурентов"
check("r3.multi_competitor.2plus_total", 28178, total_2plus)
check("r3.multi_competitor.3plus_count", 14517, p3_count)
check("r3.multi_competitor.exactly_2_count", 13661, e2_count)

# ══════════════════════════════════════════════════════════════
# CHECK 6: GAP ANALYSIS ARITHMETIC
# ══════════════════════════════════════════════════════════════
print("CHECK 6: Gap analysis arithmetic...")

gap_report = {
    "freesoft.net": {
        "DR": (-25, 76, 51),
        "Ref.domains": (-13509, 17373, 3864),
        "Dofollow%": (4.2, 70.7, 74.9),
        "Spam%": (46.9, 42.4, 89.3),
        "Branded%": (-7.4, 8.8, 1.4),
        "DR_mean": (-14.6, 17.8, 3.2),
        "Age_5y%": (-22.6, 22.6, 0.0),
        "Growth": (-4458, 8219, 3761),
        "Other%": (36.4, 60.1, 96.5),
    },
    "freesoft.ru": {
        "DR": (-17, 76, 59),
        "Ref.domains": (-14116, 17373, 3257),
        "Dofollow%": (-35.2, 70.7, 35.5),
        "Spam%": (27.4, 42.4, 69.8),
        "Branded%": (-1.6, 8.8, 7.2),
        "DR_mean": (-2.6, 17.8, 15.2),
        "Age_5y%": (-9.2, 22.6, 13.4),
        "Growth": (-6552, 8219, 1667),
        "Other%": (2.9, 60.1, 63.0),
    },
    "frees0ft.fr": {
        "DR": (-53, 76, 23),
        "Ref.domains": (-16895, 17373, 478),
        "Dofollow%": (-66.4, 70.7, 4.3),
        "Spam%": (46.5, 42.4, 88.9),
        "Branded%": (-8.6, 8.8, 0.2),
        "DR_mean": (-8.7, 17.8, 9.1),
        "Age_5y%": (-22.6, 22.6, 0.0),
        "Growth": (-7752, 8219, 467),
        "Other%": (19.8, 60.1, 79.9),
    },
}

for domain, gaps in gap_report.items():
    for metric, (gap, benchmark, actual) in gaps.items():
        calc_gap = round(actual - benchmark, 1)
        check(f"gap.{domain}.{metric}", gap, calc_gap)

# ══════════════════════════════════════════════════════════════
# CHECK 7: PERCENTAGE SUMS
# ══════════════════════════════════════════════════════════════
print("CHECK 7: Percentage sums...")

for domain in ALL_DOMAINS:
    r4d = r4["domains"][domain]

    # DR buckets should sum to ~100%
    dr_sum = sum(r4d["dr_distribution"]["buckets"][b]["pct"] for b in dr_buckets)
    check(f"pct_sum.{domain}.dr_buckets", 100.0, dr_sum)

    # Anchor types should sum to ~100%
    anch = r4d["anchor_profile"]["type_distribution"]
    anch_sum = sum(anch.get(t, {}).get("pct", 0.0) for t in ["branded", "exact_match", "url", "generic", "other"])
    check(f"pct_sum.{domain}.anchor_types", 100.0, anch_sum)

    # Dofollow + nofollow should be ~100%
    fr = r4d["follow_ratio"]
    follow_sum = fr["dofollow"]["pct"] + fr["nofollow"]["pct"]
    check(f"pct_sum.{domain}.follow_ratio", 100.0, follow_sum)

# ══════════════════════════════════════════════════════════════
# CHECK 8: CROSS-CONSISTENCY (same number in different places)
# ══════════════════════════════════════════════════════════════
print("CHECK 8: Cross-consistency...")

# freesoft.net spam% appears in exec summary (89.3%), R4 section (89.3%), R2 section (89.3%)
# All should match r4 and r2 JSON values
for domain in OUR_DOMAINS:
    r4_spam = r4["domains"][domain]["spam_ratio"]["pct"]
    r2_spam = r2["domains"][domain]["summary"]["spam_pct"]
    check(f"cross.{domain}.spam_r4_vs_r2", round(r4_spam, 1), round(r2_spam, 1))

# ref_domains should be same in r4 overview and r2 summary and inventory
for domain in ALL_DOMAINS:
    r4_ref = r4["domains"][domain]["overview"]["total_ref_domains"]
    r2_ref = r2["domains"][domain]["summary"]["total_ref_domains"]
    inv_ref = inventory["per_domain_summary"].get(domain, {}).get("A_rows")
    check(f"cross.{domain}.ref_r4_vs_r2", r4_ref, r2_ref)
    check(f"cross.{domain}.ref_r4_vs_inv", r4_ref, inv_ref)

# ══════════════════════════════════════════════════════════════
# CHECK 9: R1 LANGUAGE LINKS (key numbers)
# ══════════════════════════════════════════════════════════════
print("CHECK 9: R1 language links...")

# Extract key numbers from R1 JSON
r1_domains = r1.get("domains", {})

# Report says: softonic.com 29,518 backlinks, 17.3% non-EN
r1_softonic = r1_domains.get("softonic.com", {})
if r1_softonic:
    total_bl = r1_softonic.get("total_backlinks", 0)
    check("r1.softonic.com.total_backlinks", 29518, total_bl)

# Report says: uptodown.com 28,335 backlinks
r1_uptodown = r1_domains.get("uptodown.com", {})
if r1_uptodown:
    total_bl = r1_uptodown.get("total_backlinks", 0)
    check("r1.uptodown.com.total_backlinks", 28335, total_bl)

# Report says: frees0ft.fr 465 backlinks, 4.4% FR
r1_freesoft_fr = r1_domains.get("frees0ft.fr", {})
if r1_freesoft_fr:
    total_bl = r1_freesoft_fr.get("total_backlinks", 0)
    check("r1.frees0ft.fr.total_backlinks", 465, total_bl)

# Report says: freesoft.ru 2,852 backlinks, 35.6% RU
r1_freesoft_ru = r1_domains.get("freesoft.ru", {})
if r1_freesoft_ru:
    total_bl = r1_freesoft_ru.get("total_backlinks", 0)
    check("r1.freesoft.ru.total_backlinks", 2852, total_bl)

# Report says: freesoft.net 3,810 backlinks
r1_freesoft_net = r1_domains.get("freesoft.net", {})
if r1_freesoft_net:
    total_bl = r1_freesoft_net.get("total_backlinks", 0)
    check("r1.freesoft.net.total_backlinks", 3810, total_bl)

# ══════════════════════════════════════════════════════════════
# SUMMARY AND OUTPUT
# ══════════════════════════════════════════════════════════════
total_checks = len(results)
passed = sum(1 for r in results if r["status"] == "PASS")
failed = sum(1 for r in results if r["status"] == "FAIL")
warned = sum(1 for r in results if r["status"] == "WARN")
skipped = sum(1 for r in results if r["status"] == "SKIP")

print(f"\n{'='*60}")
print(f"VERIFICATION COMPLETE")
print(f"{'='*60}")
print(f"Total checks: {total_checks}")
print(f"Passed:       {passed} ({passed/total_checks*100:.1f}%)")
print(f"Failed:       {failed} ({failed/total_checks*100:.1f}%)")
print(f"Warnings:     {warned} ({warned/total_checks*100:.1f}%)")
print(f"Skipped:      {skipped}")

# Print failures
if failed > 0:
    print(f"\n{'='*60}")
    print("FAILURES:")
    print(f"{'='*60}")
    for r in results:
        if r["status"] == "FAIL":
            print(f"  [{r['severity'].upper()}] {r['check']}: report={r['report_value']}, json={r['json_value']}, delta={r.get('delta', 'N/A')}")

# Print warnings
if warned > 0:
    print(f"\n{'='*60}")
    print("WARNINGS:")
    print(f"{'='*60}")
    for r in results:
        if r["status"] == "WARN":
            print(f"  [{r['severity'].upper()}] {r['check']}: report={r['report_value']}, json={r['json_value']}, delta={r.get('delta', 'N/A')}")

# Save full results
output = {
    "total_checks": total_checks,
    "passed": passed,
    "failed": failed,
    "warnings": warned,
    "skipped": skipped,
    "details": results
}

output_path = INTER / "verification_results.json"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"\nFull results saved to: {output_path}")

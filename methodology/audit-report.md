# Final Architecture Audit Report (Iteration 3)

## Verdict: READY TO BUILD (after 3 fixes below)

3 issues need fixing before launch, all addressed in this audit. No architectural rework needed.

---

## Data Verification Results

### File Counts
- CSV files: **36** (confirmed) — matches ARCHITECTURE.md
- PNG files: **15** (confirmed) — matches ARCHITECTURE.md
- Total: **51** — correct

### Encoding Discovery (CRITICAL)

**34 of 36 CSV files** are UTF-16LE with BOM as documented.

**2 files are ASCII/CSV** (comma-delimited, NOT tab-delimited, NOT UTF-16LE):
- `frees0ft.fr-perf-subdomains_year2_daily_2026-03-05_22-22-53.csv` (731 lines, ASCII)
- `frees0ft.fr-perf-subdomains_year2_daily_2026-03-05_23-03-23.csv` (731 lines, ASCII)

**Impact:** Task `00b-convert-encoding` runs `iconv -f UTF-16LE` on ALL CSVs. For these 2 files, iconv produces **empty output** (0 bytes). Task 03-parse-freesoft-fr will read empty files and report "ДАННЫЕ ОТСУТСТВУЮТ" for performance data.

**Fix applied:** Updated ARCHITECTURE.md task 00b to detect encoding before converting (see Changes section).

### Row Count Discrepancies

data-inventory.md contains slightly inflated row counts for some files. Real counts (via `wc -l` after UTF-8 conversion):

| File | Inventory says | Actual |
|------|---------------|--------|
| uptodown_com_top_pages...actual | 30045 | 30001 |
| softonic_com_top_pages...actual | 30029 | 30001 |
| softonic_com_top_pages...comp | 30050 | 30001 |

All other files match. The discrepancies are not architecturally significant — all Ahrefs exports cap at 30001 lines (30000 data rows + 1 header).

---

## File Coverage: 51/51

All 51 files from data-inventory.md are assigned to tasks in ARCHITECTURE.md.

| # | Filename | Assigned Task | Path | Status |
|---|----------|---------------|------|--------|
| 1 | freesoft_net_organic_keywords...us...csv | 01-parse-freesoft-net | data_utf8/ | ok |
| 2 | freesoft_net_organic_keywords...ru_22_29_58.csv | 01-parse-freesoft-net | data_utf8/ | ok |
| 3 | freesoft_net_organic_keywords...ru_22_30_14.csv | 01-parse-freesoft-net | data_utf8/ | ok |
| 4 | freesoft_net_top_pages...us_comp.csv | 01-parse-freesoft-net | data_utf8/ | ok |
| 5 | freesoft_net_top_pages...ru_comp.csv | 01-parse-freesoft-net | data_utf8/ | ok |
| 6 | freesoft_net_top_pages...ru_actu.csv | 01-parse-freesoft-net | data_utf8/ | ok |
| 7 | freesoft_net_orgcompetitors...ru.csv | 01-parse-freesoft-net | data_utf8/ | ok |
| 8 | freesoft_net_orgcompetitors...us.csv | 01-parse-freesoft-net | data_utf8/ | ok |
| 9 | freesoft_net_main_overiew.png | 01-parse-freesoft-net | data_for_task/ | ok |
| 10 | organic_traff_loc_US.png | 01-parse-freesoft-net | data_for_task/ | ok |
| 11 | freesoft_ru_organic_keywords...22_26_41.csv | 02a-parse-freesoft-ru-keywords | data_utf8/ | ok |
| 12 | freesoft_ru_organic_keywords...22_27_20.csv | 02a-parse-freesoft-ru-keywords | data_utf8/ | ok |
| 13 | freesoft_ru_top_pages...actua.csv | 02b-parse-freesoft-ru-pages | data_utf8/ | ok |
| 14 | freesoft_ru_top_pages...compa.csv | 02b-parse-freesoft-ru-pages | data_utf8/ | ok |
| 15 | freesoft_RU_main_overiew.png | 02a-parse-freesoft-ru-keywords | data_for_task/ | ok |
| 16 | organic_traff_loc_RU.png | 02a-parse-freesoft-ru-keywords | data_for_task/ | ok |
| 17 | frees0ft_fr_organic_keywords...22_20_26.csv | 03-parse-freesoft-fr | data_utf8/ | ok |
| 18 | frees0ft_fr_organic_keywords...22_21_09.csv | 03-parse-freesoft-fr | data_utf8/ | ok |
| 19 | frees0ft_fr_top_pages...actua...23_03_45.csv | 03-parse-freesoft-fr | data_utf8/ | ok |
| 20 | frees0ft_fr_top_pages...actua...23_11_08.csv | 03-parse-freesoft-fr | data_utf8/ | ok |
| 21 | frees0ft_fr_top_pages...compa...23_03_29.csv | 03-parse-freesoft-fr | data_utf8/ | ok |
| 22 | frees0ft_fr_top_pages...compa...23_11_22.csv | 03-parse-freesoft-fr | data_utf8/ | ok |
| 23 | frees0ft_fr_top_pages...ru_compa.csv | 03-parse-freesoft-fr | data_utf8/ | ok |
| 24 | frees0ft.fr-perf...22-22-53.csv | 03-parse-freesoft-fr | data_utf8/ | ok (ASCII, special handling) |
| 25 | frees0ft.fr-perf...23-03-23.csv | 03-parse-freesoft-fr | data_utf8/ | ok (ASCII, special handling) |
| 26 | freesoft_FR_main_overiew.png | 03-parse-freesoft-fr | data_for_task/ | ok |
| 27 | organic_traff_loc_FR.png | 03-parse-freesoft-fr | data_for_task/ | ok |
| 28 | uptodown_com_site_structure.csv | 04a-parse-uptodown-structure | data_utf8/ | ok |
| 29 | uptodown_com_top_pages...actual.csv | 04b-parse-uptodown-pages | data_utf8/ | ok |
| 30 | uptodown_com_top_pages...comp.csv | 04b-parse-uptodown-pages | data_utf8/ | ok |
| 31 | uptodown_com_US_overview.png | 04a-parse-uptodown-structure | data_for_task/ | ok |
| 32 | softonic_com_site_structure.csv | 05a-parse-softonic-com-structure | data_utf8/ | ok |
| 33 | softonic_com_top_pages...actual.csv | 05b-parse-softonic-com-pages | data_utf8/ | ok |
| 34 | softonic_com_top_pages...comp.csv | 05b-parse-softonic-com-pages | data_utf8/ | ok |
| 35 | softonic_ru_site_structure.csv | 05c-parse-softonic-ru | data_utf8/ | ok |
| 36 | softonic_com_US_overview.png | 05a-parse-softonic-com-structure | data_for_task/ | ok |
| 37 | softonic_ru_RU_overview.png | 05c-parse-softonic-ru | data_for_task/ | ok |
| 38 | malavida_com_site_structure.csv | 06a-parse-malavida-structure | data_utf8/ | ok |
| 39 | malavida_com_top_pages...actual.csv | 06b-parse-malavida-pages | data_utf8/ | ok |
| 40 | malavida_com_top_pages...comp.csv | 06b-parse-malavida-pages | data_utf8/ | ok |
| 41 | malavida_com_US_overview.png | 06a-parse-malavida-structure | data_for_task/ | ok |
| 42 | filehippo_com_site_structure.csv | 07a-parse-filehippo | data_utf8/ | ok |
| 43 | filehippo_com_US_overview.png | 07a-parse-filehippo | data_for_task/ | ok |
| 44 | trashbox_ru_site_structure.csv | 07b-parse-trashbox | data_utf8/ | ok |
| 45 | trashbox_ru_US_overview.png | 07b-parse-trashbox | data_for_task/ | ok |
| 46 | clubic_com_top_pages.csv | 08a-parse-clubic | data_utf8/ | ok |
| 47 | clubic_com_US_overview.png | 08a-parse-clubic | data_for_task/ | ok |
| 48 | 01net_com_top_pages.csv | 08b-parse-01net | data_utf8/ | ok |
| 49 | 01net_com_US_overview.png | 08b-parse-01net | data_for_task/ | ok |
| 50 | commentcamarche_net_top_pages.csv | 08c-parse-commentcamarche | data_utf8/ | ok |
| 51 | ommentcamarche_net_overview.png | 08c-parse-commentcamarche | data_for_task/ | ok |

---

## Context Budget Analysis

Calculation method:
- Prompt: ~1.5K tokens
- CSV via Bash (awk/sort): ~4-6K tokens per 30K CSV, ~1-2K per small CSV
- PNG via Read: ~1-2K tokens per PNG
- Brief (200-400 lines YAML): ~2-4K tokens per brief
- Output YAML: ~2-4K tokens
- Safe budget: <60K tokens input (of ~200K total context)

| Task | CSV (count x rows) | PNGs | Briefs | Est. Input Tokens | Risk |
|------|-------------------|------|--------|-------------------|------|
| 00-inventory | 36 (head only) | 15 | 0 | ~25K | YELLOW |
| 00b-convert-encoding | 36 (loop) | 0 | 0 | ~3K | GREEN |
| 01-parse-freesoft-net | 8 x 4,222 total | 2 | 0 | ~15K | GREEN |
| 02a-parse-freesoft-ru-kw | 2 x 47,484 total | 2 | 0 | ~14K | GREEN |
| 02b-parse-freesoft-ru-pages | 2 x 30,687 total | 0 | 0 | ~12K | GREEN |
| 03-parse-freesoft-fr | 9 x 11,163 total | 2 | 0 | ~20K | GREEN |
| 04a-parse-uptodown-structure | 1 x 30,001 | 1 | 0 | ~8K | GREEN |
| 04b-parse-uptodown-pages | 2 x 60,002 total | 0 | 0 | ~12K | GREEN |
| 05a-parse-softonic-com-struct | 1 x 30,001 | 1 | 0 | ~8K | GREEN |
| 05b-parse-softonic-com-pages | 2 x 60,002 total | 0 | 0 | ~12K | GREEN |
| 05c-parse-softonic-ru | 1 x 30,001 | 1 | 0 | ~8K | GREEN |
| 06a-parse-malavida-structure | 1 x 30,001 | 1 | 0 | ~8K | GREEN |
| 06b-parse-malavida-pages | 2 x 60,002 total | 0 | 0 | ~12K | GREEN |
| 07a-parse-filehippo | 1 x 30,001 | 1 | 0 | ~8K | GREEN |
| 07b-parse-trashbox | 1 x 30,001 | 1 | 0 | ~8K | GREEN |
| 08a-parse-clubic | 1 x 26,609 | 1 | 0 | ~8K | GREEN |
| 08b-parse-01net | 1 x 28,699 | 1 | 0 | ~8K | GREEN |
| 08c-parse-commentcamarche | 1 x 30,001 | 1 | 0 | ~8K | GREEN |
| 10-validate-briefs | 0 | 0 | 17 | ~40-55K | YELLOW |
| 11-analyze-our-domains | 0 | 0 | 4 | ~12-16K | GREEN |
| 12-analyze-multilingual | 0 | 0 | 7 | ~20-28K | GREEN |
| 13-analyze-fr-market | 0 | 0 | 4 | ~12-16K | GREEN |
| 14-analyze-domain-structures | 0 | 0 | 6 | ~16-24K | GREEN |
| 16-language-potential | 0 | 0 | 3 | ~8-12K | GREEN |
| 17-domain-strategy | 0 | 0 | 2 | ~6-8K | GREEN |
| 18-roadmap-draft | 0 | 0 | 2 | ~6-8K | GREEN |
| 20-report-domain-strategy | 0 | 0 | 4 | ~12-16K | GREEN |
| 21-report-multilingual-roadmap | 0 | 0 | 6 | ~16-24K | GREEN |
| 22-validate | 0 | 0 | 7 + 2 docs | ~28-36K | YELLOW |

**No RED tasks.** 3 YELLOW tasks (00, 10, 22) are comfortably within 60K limit.

Notable:
- Tasks 04b, 05b, 06b each handle 2 x 30K CSV via Bash. At ~4-6K tokens per CSV = ~12K total. GREEN — well within budget.
- Task 02a handles 47K rows (2 CSVs). Via Bash, ~12K tokens. GREEN.
- Task 10 reads 17 briefs. If each is ~300 lines YAML = ~3K tokens, total ~51K. YELLOW but safe.
- Task 22 reads 7 briefs + 2 final docs. ~36K tokens max. YELLOW but safe.

---

## Dependency Graph Verification

```
Phase 0:   00-inventory → 00b-convert-encoding
                              |
Phase 1:   [01, 02a, 02b, 03, 04a, 04b, 05a, 05b, 05c, 06a, 06b, 07a, 07b, 08a, 08b, 08c]
           (17 tasks, all independent, MAX_PARALLEL=3)
                              |
Phase 1.5: 10-validate-briefs (singleton gate)
                              |
Phase 2:   [11, 12, 13, 14] (4 tasks, all independent, MAX_PARALLEL=3)
                              |
Phase 3:   16-language-potential → 17-domain-strategy → 18-roadmap-draft
           (sequential — each depends on previous)
                              |
Phase 4:   [20-report-domain-strategy, 21-report-multilingual-roadmap]
           (PARALLEL — no cross-dependencies)
                              |
Phase 5:   22-validate (singleton)
```

### Dependency Verification (file-level)

| From | To | File Written | File Read | Match? |
|------|----|-------------|-----------|--------|
| 00 → 00b | briefs/00-manifest.yaml | (implicit) | yes |
| 00b → Phase 1 | data_utf8/*.csv | data_utf8/*.csv | yes |
| Phase 1 → 10 | briefs/01...08c.yaml (17 files) | all 17 briefs | yes |
| 10 → Phase 2 | briefs/10-validation-result.yaml | (gate only) | yes |
| Phase 1 → 11 | briefs/01, 02a, 02b, 03 | same | yes |
| Phase 1 → 12 | briefs/04a, 04b, 05a, 05b, 05c, 06a, 06b | same | yes |
| Phase 1 → 13 | briefs/03, 08a, 08b, 08c | same | yes |
| Phase 1 → 14 | briefs/04a, 05a, 05c, 06a, 07a, 07b | same | yes |
| 11,12,13 → 16 | briefs/11, 12, 13 | same | yes |
| 14,16 → 17 | briefs/14, 16 | same | yes |
| 16,17 → 18 | briefs/16, 17 | same | yes |
| 11,14,16,17 → 20 | briefs/11, 14, 16, 17 | same | yes |
| 11,12,13,16,17,18 → 21 | briefs/11, 12, 13, 16, 17, 18 | same | yes |
| 20,21 → 22 | output/domain-strategy.md, output/multilingual-roadmap.md + briefs/11-18 | same | yes |

### Hidden Dependencies Within Phases

**Phase 1:** All 17 tasks read from `data_utf8/` (read-only) and write to separate `briefs/` files. No shared mutable state. Truly independent. Verified.

**Phase 2:** All 4 tasks read from Phase 1 briefs (read-only) and write to separate Phase 2 briefs. Task 13 reads brief 03 (also read by task 11), but both are READ-ONLY. No conflict. Truly independent. Verified.

**Phase 4:** Task 20 writes `output/domain-strategy.md`, task 21 writes `output/multilingual-roadmap.md`. Different output files. Both read Phase 2/3 briefs (read-only). **Can run in parallel.** This is a change from current architecture which says "sequential."

---

## MAX_PARALLEL=3 Optimization

### Current (MAX_PARALLEL=2)
- Phase 1: 17 tasks / 2 = 9 batches
- Phase 2: 4 tasks / 2 = 2 batches
- Phase 4: 2 tasks sequential = 2 steps
- **Total parallel batches: 13**

### Optimized (MAX_PARALLEL=3)
- Phase 1: 17 tasks / 3 = 6 batches (5 full + 1 with 2 tasks)
- Phase 2: 4 tasks / 3 = 2 batches (1 with 3 + 1 with 1)
- Phase 4: 2 tasks / 3 = 1 batch (both parallel)
- **Total parallel batches: 9** (-30% improvement)

### Optimized Execution Plan

```
PHASE 0 (sequential, ~30 min):
  00-inventory
  00b-convert-encoding

PHASE 1 (MAX_PARALLEL=3, ~2.5h):
  Batch 1: 01, 02a, 02b
  Batch 2: 03, 04a, 04b
  Batch 3: 05a, 05b, 05c
  Batch 4: 06a, 06b, 07a
  Batch 5: 07b, 08a, 08b
  Batch 6: 08c + (2 slots idle)

PHASE 1.5 (singleton, ~10 min):
  10-validate-briefs

PHASE 2 (MAX_PARALLEL=3, ~40 min):
  Batch 1: 11, 12, 13
  Batch 2: 14 + (2 slots idle)

PHASE 3 (sequential, ~1h):
  16-language-potential
  17-domain-strategy
  18-roadmap-draft

PHASE 4 (MAX_PARALLEL=3, ~20 min):
  Batch 1: 20, 21 (PARALLEL - was sequential)

PHASE 5 (singleton, ~15 min):
  22-validate
```

### Rate Limit Risk

PRINCIPLES.md recommends MAX_PARALLEL=2 for Opus. However:
- Customer explicitly approved MAX_PARALLEL=3
- Modern Opus tiers generally support 3 concurrent sessions
- If rate limits occur, the orchestrator's retry logic handles it
- Fallback: reduce to MAX_PARALLEL=2 at runtime via env var

**Decision: MAX_PARALLEL=3 approved. No blocking concern.**

---

## Brief Format Assessment

### Adequacy for Core Questions

The brief format in ARCHITECTURE.md adequately supports answering:
1. "Which languages drive traffic?" — via `traffic_by_language` in site_structure briefs
2. "What domain structure works?" — via subdomain/folder analysis in structure briefs

### Language Coverage

Current instruction: "top-20 subdomains/folders by traffic."
- Most competitors have <20 language variants. Top-20 captures all meaningful ones.
- For edge cases with 100+ subdomains: the filter `traffic > 100` already ensures completeness.
- **Recommendation:** Add instruction: "List ALL language-specific subdomains/folders regardless of traffic. Sum remaining non-language paths as 'other'."

### Top Pages Depth

Current: top-50 pages by traffic.
- For answering "what page types work?", top-50 is sufficient — captures dominant patterns.
- Top-100 would add ~500 tokens per brief — acceptable but unnecessary for this analysis.
- **Decision:** Keep top-50. Adequate for deliverables.

### Missing Aggregates

Current briefs include: traffic_by_language, top_pages, traffic_by_page_type, traffic_by_country.

**Should add to comparison CSV briefs:**
- `total_traffic_change`: net traffic change from comparison period
- `growing_pages_count` / `declining_pages_count`: trend signal

These are extracted with simple awk and add ~100 tokens per brief. Worth including for trend analysis in Phase 2+.

---

## Fact Integrity Chain

### Traced Example: "uptodown.com Spanish subdomain traffic"

| Step | File | Source Reference | Traceable? |
|------|------|-----------------|------------|
| 1. Raw data | `data_utf8/uptodown_com_site_structure_subdomains_ru_2026_03_05_22_38_10.csv` | N/A (primary source) | yes |
| 2. Brief 04a | `briefs/04a-uptodown-struct.yaml` → `traffic_by_language[].source` | CSV filename + awk command | yes |
| 3. Brief 12 | `briefs/12-multilingual-analysis.yaml` | References "brief 04a" | yes |
| 4. Brief 16 | `briefs/16-language-potential.yaml` | References "brief 12" | yes |
| 5. Output | `output/domain-strategy.md` | References brief 16/17 | yes |

**Chain-of-evidence is maintained** because ARCHITECTURE.md v2 mandates `source` and `extraction` fields in every brief value.

### Can Task 22-validate trace back?

Task 22 reads:
- 7 briefs (11, 12, 13, 14, 16, 17, 18) — these contain `source` references to Phase 1 briefs
- 2 final documents — these cite Phase 2/3 briefs

Task 22 does NOT read Phase 1 briefs directly. It can verify:
- Final doc → Phase 3 brief → Phase 2 brief (chain OK)
- BUT cannot verify Phase 2 brief → Phase 1 brief → CSV

**Recommendation:** Add Phase 1 key briefs (04a, 05a, 06a) to task 22's input list for spot-check verification. This adds ~9-12K tokens — still within budget.

---

## Remaining Issues

### Issue 1: Performance CSV Encoding Mismatch
- **Problem:** 2 performance CSV files (`frees0ft.fr-perf-subdomains_year2_daily_*.csv`) are ASCII with comma delimiters, not UTF-16LE with tab delimiters. Task 00b's `iconv -f UTF-16LE` produces empty files for them.
- **Solution:** Update 00b to detect encoding before converting. For ASCII files, copy as-is with CRLF stripping. Update task 03 prompt to note comma-delimited format for these 2 files.
- **Severity:** CRITICAL (data loss without fix)

### Issue 2: MAX_PARALLEL=2 Throughout ARCHITECTURE.md
- **Problem:** ARCHITECTURE.md says MAX_PARALLEL=2 in 4 places. Customer approved MAX_PARALLEL=3.
- **Solution:** Update all references to MAX_PARALLEL=3.
- **Severity:** IMPORTANT (performance impact)

### Issue 3: Phase 4 Marked as Sequential
- **Problem:** ARCHITECTURE.md says Phase 4 is "sequential" with tasks 20 → 21. But they write to different files and read independent briefs. No dependency exists.
- **Solution:** Mark Phase 4 as parallel. Both tasks run simultaneously.
- **Severity:** IMPORTANT (unnecessary serialization)

### Issue 4: Row Count Inaccuracies in data-inventory.md
- **Problem:** 3 files show inflated row counts (30045, 30029, 30050 vs actual 30001).
- **Solution:** Correct data-inventory.md. Not architecturally significant.
- **Severity:** MINOR

### Issue 5: Task 22 Cannot Fully Trace to Phase 1 Briefs
- **Problem:** Task 22 reads Phase 2/3 briefs and final docs, but not Phase 1 briefs. Cannot verify the full chain back to CSV.
- **Solution:** Add 3 key Phase 1 briefs (04a, 05a, 06a) to task 22 input for spot-checking.
- **Severity:** MINOR (verification depth, not correctness)

---

## Changes Made to ARCHITECTURE.md

1. **Task 00b:** Added encoding detection logic — `file` command check before iconv. ASCII files copied with `sed 's/\r$//'` only.

2. **MAX_PARALLEL:** Updated from 2 to 3 in:
   - General scheme diagram
   - Phase 1 header
   - Phase 2 header
   - run.sh configuration section
   - Estimates table

3. **Phase 4:** Changed from "sequential" to "parallel" with note that tasks 20 and 21 are independent.

4. **Task 22:** Added Phase 1 briefs (04a, 05a, 06a) to input list for spot-check verification.

5. **Brief format:** Added `total_traffic_change` and `growing_vs_declining_pages` to comparison CSV brief template.

6. **Task 03 prompt note:** Added that performance CSVs are comma-delimited ASCII (not tab-delimited UTF-16LE).

---

## Final Verification (7 Questions)

1. **All 51 files assigned to tasks?** YES — 51/51 confirmed via table above.

2. **Any task with RED risk level?** NO — all GREEN or YELLOW. Highest risk tasks (00, 10, 22) are YELLOW at ~25-55K tokens, well within 60K limit.

3. **MAX_PARALLEL=3 everywhere?** YES — updated in general scheme, Phase 1 header, Phase 2 header, run.sh config, estimates table.

4. **Every brief contains source for every value?** YES — ARCHITECTURE.md v2 mandates `source` and `extraction` fields. Format template includes them.

5. **Phase 3 tasks correctly sequential?** YES — 16 depends on 11+12+13 (Phase 2), 17 depends on 14+16, 18 depends on 16+17. Each reads the previous task's output. Cannot be parallelized.

6. **Task 22 can trace from CSV to report?** PARTIALLY — after fix, task 22 reads key Phase 1 briefs (04a, 05a, 06a) for spot-checking, plus Phase 2/3 briefs and final docs. Full chain: CSV → Phase 1 brief (with `source` + `extraction`) → Phase 2 brief (with `source: brief X`) → final doc (with citations). Verifiable.

7. **Pipeline ready for prompt generation and run.sh?** YES — after applying the 3 fixes documented above (all already applied to ARCHITECTURE.md).

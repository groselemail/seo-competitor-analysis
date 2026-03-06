# Architecture Review Report

## Summary

**Overall Assessment: Major Rework**

Architecture has a solid phased structure but contains 5 critical issues that will cause pipeline failures: UTF-16 CSV encoding not handled, incorrect file counts per task, tasks too large for context, missing files in task assignments, and no chain-of-evidence in briefs.

---

## Critical Issues (block launch)

### Issue 1: UTF-16LE CSV Encoding — Pipeline Will Crash

- **Problem:** ALL CSV files are UTF-16LE with BOM (byte order mark). Standard Unix tools (`awk`, `sort`, `head`, `cut`, `wc -l`) will produce garbage or errors on UTF-16 input. Architecture assumes UTF-8 compatible CSVs.
- **Evidence:** `head -1` output shows wide-spaced characters with BOM: `"\xef\xbf\xbd" U R L "` instead of `"URL"`.
- **Impact:** Every Phase 1 task will fail or produce incorrect data. `wc -l` will report wrong line counts. `awk` field splitting will not work.
- **Solution:** Add a mandatory UTF-8 conversion step. Either:
  - (A) Add a Phase 0.5 pre-processing task that converts all CSVs: `iconv -f UTF-16LE -t UTF-8 < input.csv | sed 's/\r$//' > input_utf8.csv`
  - (B) Include conversion in every Phase 1 prompt as the first Bash step.
  - Recommendation: Option (A) — single task `00b-convert-encoding` after inventory. Creates `data_for_task_utf8/` directory with clean files. All subsequent tasks read from `data_for_task_utf8/`.

### Issue 2: Incorrect File Counts Per Task

- **Problem:** Architecture lists wrong file counts for most tasks. This means prompts will reference wrong number of files, potentially missing some.
- **Evidence:**
  - Task 01 says "4 CSV" but freesoft.net has **8 CSV** (2 keywords RU + 1 keywords US + 3 top_pages + 2 competitors)
  - Task 02 says "3 CSV" but freesoft.ru has **4 CSV** (2 keywords + 2 top_pages)
  - Task 03 says "5 CSV" but frees0ft.fr has **9 CSV** (2 keywords + 4 top_pages + 1 ru_comparison + 2 performance_daily)
  - Task 05 says "3 CSV" but softonic has **4 CSV** (softonic.com: 3 + softonic.ru: 1)
  - Task 07 says "3 CSV" but filehippo+trashbox have only **2 CSV**
- **Impact:** Tasks will miss input files, producing incomplete briefs.
- **Solution:** Recount all files per task using data-inventory.md as ground truth. Update architecture table.

### Issue 3: Tasks Too Large for Context (>60K CSV Rows)

- **Problem:** Multiple tasks try to process 60K-120K CSV rows in a single session. Even with Bash pre-processing, this is too many operations for one agent.
- **Evidence:**
  - Task 04 (uptodown): 30K + 30K + 30K = **90K rows**
  - Task 05 (softonic.com + softonic.ru): 30K + 30K + 30K + 30K = **120K rows**
  - Task 06 (malavida): 30K + 30K + 30K = **90K rows**
  - Task 08 (fr-market): 27K + 29K + 30K = **85K rows** + 3 PNGs
  - Task 02 (freesoft.ru): 17K + 30K + 8K + 22K = **77K rows**
- **Impact:** Context degradation, missed data, potential "prompt too long" errors. Agent may not complete within 150 turns.
- **Solution:** Split heavy tasks:
  - Task 05 → 05a (softonic.com) + 05b (softonic.ru)
  - Task 04 → 04a (uptodown site_structure) + 04b (uptodown top_pages)
  - Task 06 → 06a (malavida site_structure) + 06b (malavida top_pages)
  - Task 08 → 08a (clubic) + 08b (01net) + 08c (commentcamarche)
  - Task 02 → 02a (freesoft.ru keywords) + 02b (freesoft.ru top_pages)

### Issue 4: Missing Competitor Files in Architecture Table

- **Problem:** Architecture's "Входные данные" table is incomplete and sometimes wrong.
- **Evidence:**
  - `freesoft_net_orgcompetitors` (2 CSV) — listed in table header but not assigned to any task
  - `frees0ft.fr-perf-subdomains_year2_daily` (2 CSV) — mentioned as "performance daily" but not assigned
  - `frees0ft_fr_top_pages_subdomains_ru_compa` — not mentioned at all (cross-language comparison)
  - Duplicate frees0ft.fr CSVs (4 files at 2 timestamps) — not mentioned
  - `ommentcamarche_net_overview.png` — architecture says "Screenshot_1.png" but actual filename different (and has typo)
  - `organic_traff_loc_*.png` — 3 PNGs for traffic by location, ambiguously assigned
- **Impact:** Data loss — important files will be ignored by the pipeline.
- **Solution:** Create explicit file→task mapping in architecture. Every file must be named.

### Issue 5: No Chain-of-Evidence in Brief Format

- **Problem:** Brief format examples show data without source references. When a brief says `traffic: 983000`, there's no way to verify which file/field this came from.
- **Impact:** Validation task (22-validate) cannot actually verify facts against sources. Hallucinated numbers will pass validation.
- **Solution:** Every data point in briefs must include source:
  ```yaml
  total_organic_traffic:
    value: 983000
    source: "uptodown_com_US_overview.png"
    note: "Read from Ahrefs overview screenshot"
  ```

---

## Important Issues (don't block, but degrade quality)

### Issue 6: MAX_PARALLEL Mismatch

- **Problem:** ARCHITECTURE.md says `MAX_PARALLEL=2`. REVIEW_PROMPT.md says `MAX_PARALLEL=3`. PRINCIPLES.md recommends Opus=2.
- **Impact:** If run with 3, rate limit errors. If run with 2, architecture already accounts for it.
- **Solution:** Standardize on `MAX_PARALLEL=2` for Opus as per PRINCIPLES.md.

### Issue 7: Task 02 (freesoft.ru) Has 77K Rows

- **Problem:** freesoft.ru has the largest dataset among our domains: 17K keywords (actual) + 30K keywords (comparison) + 8K top_pages (actual) + 22K top_pages (comparison).
- **Impact:** Single task processing 77K rows will degrade in quality toward the end.
- **Solution:** Split into 02a (keywords, 47K rows) and 02b (top_pages, 30K rows). Both write sub-briefs that get merged.

### Issue 8: Task 05 Combines Two Separate Domains

- **Problem:** softonic.com and softonic.ru are treated as one entity, but they're separate domains with different DR (86 vs 50), different traffic (88.5K vs 335K), and different language focus.
- **Impact:** Analysis will conflate two distinct strategies.
- **Solution:** Split into 05a (softonic.com: 3 CSV + 1 PNG) and 05b (softonic.ru: 1 CSV + 1 PNG).

### Issue 9: Duplicate frees0ft.fr Files

- **Problem:** 4 frees0ft.fr CSV files appear in pairs at different timestamps (23:03 and 23:11). Same row counts suggest duplicates.
  - `frees0ft_fr_top_pages...fr_actua...23_03_45.csv` (488) and `...23_11_08.csv` (488)
  - `frees0ft_fr_top_pages...fr_compa...23_03_29.csv` (1931) and `...23_11_22.csv` (1931)
- **Impact:** If truly duplicates, wasted processing. If different snapshots, both should be analyzed.
- **Solution:** Phase 0 (inventory) should diff these files. If identical, mark one as "skip". If different, note timestamps.

### Issue 10: No Validation Between Phase 1 and Phase 2

- **Problem:** If a Phase 1 brief is malformed or empty, Phase 2 tasks will silently produce wrong analysis.
- **Impact:** Garbage-in-garbage-out propagation.
- **Solution:** Add `10-validate-briefs` task between Phase 1 and Phase 2. Checks: all briefs exist, non-empty, valid YAML, contain required fields. Quick task (~30 turns).

### Issue 11: Phase 2 Task 14 Reads 4 Briefs Including Minor Competitors

- **Problem:** Task 14 (domain structures) reads briefs 04 + 05 + 06 + 07. If after splitting these become 8 briefs, that's a lot of input.
- **Impact:** Moderate context pressure, but briefs are compressed so likely OK.
- **Solution:** Keep as-is but ensure each brief stays under 300 lines YAML.

### Issue 12: freesoft.net Overview Screenshot Shows RU Filter

- **Problem:** freesoft_net_main_overiew.png shows "Russian Federation" filter. freesoft.net is an English domain — RU traffic is only 89 per month. The US filter data is not in any PNG.
- **Impact:** Task 01 will see misleadingly low traffic numbers for freesoft.net.
- **Solution:** Note in prompt that this PNG shows RU-filtered data. Real US traffic data is in `organic_traff_loc_US.png` (India 14.2K, US 2.1K — total ~34.6K). Mention this discrepancy explicitly.

---

## Minor Issues (nice to have)

### Issue 13: Filename Typo — ommentcamarche

- **Problem:** `ommentcamarche_net_overview.png` is missing leading 'c'. Architecture refers to "Screenshot_1.png".
- **Solution:** Reference actual filename in prompts. Consider renaming file.

### Issue 14: Architecture Numbering Gap (15, 19)

- **Problem:** Task numbers jump from 14 to 16 (Phase 3), and from 18 to 20 (Phase 4). Numbers 15 and 19 are unused.
- **Impact:** Cosmetic, but confusing. Should reserve for split tasks or explicitly note they're intentionally skipped.
- **Solution:** Use 15 for validation-briefs task. Or renumber.

### Issue 15: Phased Pipeline vs Chain-Based

- **Problem:** Architecture declares "Level 2 — Phased Pipeline" but also defines CHAINS in run.sh config. This is a hybrid that doesn't match either pattern cleanly.
- **Impact:** The CHAINS definition suggests chain-based execution, but the actual dependency graph is phased (Phase 1 fully completes before Phase 2).
- **Solution:** Clarify: this IS a phased pipeline. The chains in config are just for Phase 1→2 dependency tracking, not true end-to-end chains. Update description.

### Issue 16: No Meta-Prompt Pattern for 19+ Prompts

- **Problem:** Pipeline has 19 tasks = 19 prompts. META_PROMPTS.md recommends meta-prompts for 15+ tasks to avoid context degradation when writing prompts.
- **Solution:** Use 4 meta-prompts: meta-phase1 (8 prompts), meta-phase2 (4), meta-phase3 (3), meta-phase4-5 (4).

---

## Data Coverage Matrix

| # | File | Assigned Task |
|---|------|--------------|
| 1 | freesoft_net_organic_keywords...us.csv | 01-parse-freesoft-net |
| 2 | freesoft_net_organic_keywords...ru_22_29_58.csv | 01-parse-freesoft-net |
| 3 | freesoft_net_organic_keywords...ru_22_30_14.csv | 01-parse-freesoft-net |
| 4 | freesoft_net_top_pages...us_comp.csv | 01-parse-freesoft-net |
| 5 | freesoft_net_top_pages...ru_comp.csv | 01-parse-freesoft-net |
| 6 | freesoft_net_top_pages...ru_actu.csv | 01-parse-freesoft-net |
| 7 | freesoft_net_orgcompetitors...ru.csv | 01-parse-freesoft-net |
| 8 | freesoft_net_orgcompetitors...us.csv | 01-parse-freesoft-net |
| 9 | freesoft_net_main_overiew.png | 01-parse-freesoft-net |
| 10 | organic_traff_loc_US.png | 01-parse-freesoft-net |
| 11 | freesoft_ru_organic_keywords...22_26_41.csv | 02a-parse-freesoft-ru-keywords |
| 12 | freesoft_ru_organic_keywords...22_27_20.csv | 02a-parse-freesoft-ru-keywords |
| 13 | freesoft_ru_top_pages...actual.csv | 02b-parse-freesoft-ru-pages |
| 14 | freesoft_ru_top_pages...compa.csv | 02b-parse-freesoft-ru-pages |
| 15 | freesoft_RU_main_overiew.png | 02a-parse-freesoft-ru-keywords |
| 16 | organic_traff_loc_RU.png | 02a-parse-freesoft-ru-keywords |
| 17 | frees0ft_fr_organic_keywords...22_20_26.csv | 03-parse-freesoft-fr |
| 18 | frees0ft_fr_organic_keywords...22_21_09.csv | 03-parse-freesoft-fr |
| 19 | frees0ft_fr_top_pages...actual...23_03_45.csv | 03-parse-freesoft-fr |
| 20 | frees0ft_fr_top_pages...actual...23_11_08.csv | 03-parse-freesoft-fr |
| 21 | frees0ft_fr_top_pages...compa...23_03_29.csv | 03-parse-freesoft-fr |
| 22 | frees0ft_fr_top_pages...compa...23_11_22.csv | 03-parse-freesoft-fr |
| 23 | frees0ft_fr_top_pages...ru_compa.csv | 03-parse-freesoft-fr |
| 24 | frees0ft.fr-perf...22-22-53.csv (RU) | 03-parse-freesoft-fr |
| 25 | frees0ft.fr-perf...23-03-23.csv (FR) | 03-parse-freesoft-fr |
| 26 | freesoft_FR_main_overiew.png | 03-parse-freesoft-fr |
| 27 | organic_traff_loc_FR.png | 03-parse-freesoft-fr |
| 28 | uptodown_com_site_structure.csv | 04a-parse-uptodown-structure |
| 29 | uptodown_com_top_pages...actual.csv | 04b-parse-uptodown-pages |
| 30 | uptodown_com_top_pages...comp.csv | 04b-parse-uptodown-pages |
| 31 | uptodown_com_US_overview.png | 04a-parse-uptodown-structure |
| 32 | softonic_com_site_structure.csv | 05a-parse-softonic-com |
| 33 | softonic_com_top_pages...actual.csv | 05a-parse-softonic-com |
| 34 | softonic_com_top_pages...comp.csv | 05a-parse-softonic-com |
| 35 | softonic_ru_site_structure.csv | 05b-parse-softonic-ru |
| 36 | softonic_com_US_overview.png | 05a-parse-softonic-com |
| 37 | softonic_ru_RU_overview.png | 05b-parse-softonic-ru |
| 38 | malavida_com_site_structure.csv | 06a-parse-malavida-structure |
| 39 | malavida_com_top_pages...actual.csv | 06b-parse-malavida-pages |
| 40 | malavida_com_top_pages...comp.csv | 06b-parse-malavida-pages |
| 41 | malavida_com_US_overview.png | 06a-parse-malavida-structure |
| 42 | filehippo_com_site_structure.csv | 07a-parse-filehippo |
| 43 | filehippo_com_US_overview.png | 07a-parse-filehippo |
| 44 | trashbox_ru_site_structure.csv | 07b-parse-trashbox |
| 45 | trashbox_ru_US_overview.png | 07b-parse-trashbox |
| 46 | clubic_com_top_pages.csv | 08a-parse-clubic |
| 47 | clubic_com_US_overview.png | 08a-parse-clubic |
| 48 | 01net_com_top_pages.csv | 08b-parse-01net |
| 49 | 01net_com_US_overview.png | 08b-parse-01net |
| 50 | commentcamarche_net_top_pages.csv | 08c-parse-commentcamarche |
| 51 | ommentcamarche_net_overview.png | 08c-parse-commentcamarche |

**Coverage: 51/51 files mapped.**

---

## Context Budget Estimates (after proposed splits)

| Task | CSV Rows | PNGs | Briefs Read | Risk Level | Notes |
|------|----------|------|-------------|------------|-------|
| 00-inventory | 0 (head only) | 15 | 0 | MEDIUM | 15 PNGs is a lot; consider splitting into sub-batches |
| 00b-convert-encoding | 0 | 0 | 0 | LOW | Pure Bash: iconv loop |
| 01-parse-freesoft-net | ~4,222 | 2 | 0 | LOW | Small CSVs, manageable |
| 02a-parse-freesoft-ru-kw | ~47,484 | 2 | 0 | HIGH | 30K comparison CSV; MUST use Bash preprocessing |
| 02b-parse-freesoft-ru-pages | ~30,687 | 0 | 0 | HIGH | 22K comparison CSV; MUST use Bash |
| 03-parse-freesoft-fr | ~11,163 | 2 | 0 | MEDIUM | Many small files; duplicates inflate count |
| 04a-parse-uptodown-structure | ~30,001 | 1 | 0 | HIGH | Single 30K CSV; Bash for language extraction |
| 04b-parse-uptodown-pages | ~60,046 | 0 | 0 | HIGH | Two 30K CSVs; MUST use Bash |
| 05a-parse-softonic-com | ~90,080 | 1 | 0 | CRITICAL | Three 30K CSVs; split further or aggressive Bash |
| 05b-parse-softonic-ru | ~30,001 | 1 | 0 | HIGH | Single 30K CSV |
| 06a-parse-malavida-structure | ~30,001 | 1 | 0 | HIGH | Single 30K CSV |
| 06b-parse-malavida-pages | ~60,002 | 0 | 0 | HIGH | Two 30K CSVs |
| 07a-parse-filehippo | ~30,001 | 1 | 0 | HIGH | Single 30K CSV |
| 07b-parse-trashbox | ~30,001 | 1 | 0 | HIGH | Single 30K CSV |
| 08a-parse-clubic | ~26,609 | 1 | 0 | HIGH | Near-30K CSV |
| 08b-parse-01net | ~28,699 | 1 | 0 | HIGH | Near-30K CSV |
| 08c-parse-commentcamarche | ~30,001 | 1 | 0 | HIGH | 30K CSV |
| 10-validate-briefs | 0 | 0 | ~15 | LOW | Quick YAML validation |
| 11-analyze-our-domains | 0 | 0 | 3 | LOW | Briefs only |
| 12-analyze-multilingual | 0 | 0 | 4 | LOW | Briefs only |
| 13-analyze-fr-market | 0 | 0 | 4 | LOW | Briefs only |
| 14-analyze-domain-structures | 0 | 0 | 5 | LOW | Briefs only |
| 16-language-potential | 0 | 0 | 3 | LOW | Briefs only |
| 17-domain-strategy | 0 | 0 | 2 | LOW | Briefs only |
| 18-roadmap-draft | 0 | 0 | 2 | LOW | Briefs only |
| 20-report-domain-strategy | 0 | 0 | 4 | LOW | Briefs only |
| 21-report-multilingual-roadmap | 0 | 0 | 6 | MEDIUM | Most briefs; watch size |
| 22-validate | 0 | 0 | ~10+2 docs | MEDIUM | All briefs + 2 final docs |

---

## Recommendations

1. **Add encoding conversion task (00b)** as first priority. Without this, the entire pipeline is non-functional.

2. **Split heavy Phase 1 tasks** as described in Issue 3. This increases task count from 19 to ~28 but dramatically improves reliability.

3. **Add chain-of-evidence to brief format.** Every numeric value must cite `source_file` and `extraction_method` (Bash command or PNG visual).

4. **Add Phase 1.5 brief validation task (10-validate-briefs).** Quick YAML schema check before Phase 2 starts.

5. **Fix all file counts and create explicit file-to-task mapping** in architecture. No more "4 CSV" — list actual filenames.

6. **Standardize MAX_PARALLEL=2** for Opus model. Update all references.

7. **Use meta-prompts** to generate the 28 prompt files (4 meta-prompts, one per phase).

8. **Handle duplicate frees0ft.fr files** — inventory task should detect and mark duplicates.

9. **Task 05a (softonic.com) still has 90K rows** even after split. Consider further splitting into 05a-structure (30K) and 05a-pages (60K), or use aggressive Bash reduction (top-100 pages only).

10. **Note freesoft.net overview PNG limitation** — it shows RU filter with traffic=89, not representative. US traffic data is only in organic_traff_loc_US.png.

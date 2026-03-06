# Review Report: Phase 0 + Phase 1 + Phase 1.5 Prompts

**Reviewer:** Claude Opus 4.6 (automated QA)
**Date:** 2026-03-06
**Source of truth:** `pipeline-seo/ARCHITECTURE.md` (rev 2026-03-05)

## Summary

- **Files reviewed:** 19
- **Files with issues:** 0 (critical), 0 (requiring fixes)
- **Total fixes applied:** 0
- **Status: PASS**

All 19 prompts are well-constructed, consistent with ARCHITECTURE.md, and follow the PROMPT_ENGINEERING.md template. No blocking or functional issues found. Minor observations noted below.

---

## Per-File Results

### 00-inventory.md
- [x] Check 1: File paths — OK (correctly reads from `data_for_task/` as this is pre-conversion)
- [x] Check 2: Output path — OK (`pipeline-seo/briefs/00-manifest.yaml`)
- [x] Check 3: Self-contained — OK (references `data-inventory.md` and `ARCHITECTURE.md`)
- [x] Check 4: Verification — OK (7 checks)
- [x] Check 5: Gambling filter — N/A (Phase 0)
- [x] Check 6: CSV via Bash — OK (uses Bash for all CSV metadata)
- [x] Check 7: Performance CSV comma — N/A (catalogs only, no parsing)
- [x] Check 8: Chain-of-evidence — N/A (Phase 0, no brief metrics)
- [x] Check 9: max-turns — NOTE: not mentioned (expected: 100)
- [x] Check 10: No hardcoded data — OK (template values are reference targets)
- **Issues found:** None
- **Fixes applied:** None

### 00b-convert-encoding.md
- [x] Check 1: File paths — OK (reads `data_for_task/*.csv`, writes `data_utf8/`)
- [x] Check 2: Output path — OK (36 CSV files in `data_utf8/`)
- [x] Check 3: Self-contained — OK (references `00-manifest.yaml`)
- [x] Check 4: Verification — OK (6 checks including ASCII perf CSV validation)
- [x] Check 5: Gambling filter — N/A (Phase 0)
- [x] Check 6: CSV via Bash — OK (all Bash)
- [x] Check 7: Performance CSV comma — OK (handles ASCII files separately)
- [x] Check 8: Chain-of-evidence — N/A (no brief output)
- [x] Check 9: max-turns — NOTE: not mentioned (expected: 50)
- [x] Check 10: No hardcoded data — OK
- **Issues found:** None
- **Fixes applied:** None

### 01-parse-freesoft-net.md
- [x] Check 1: File paths — OK (8 CSV from `data_utf8/`, 2 PNG from `data_for_task/`, all filenames match ARCHITECTURE.md)
- [x] Check 2: Output path — OK (`briefs/01-freesoft-net.yaml`)
- [x] Check 3: Self-contained — OK
- [x] Check 4: Verification — OK (5 checks)
- [x] Check 5: Gambling filter — OK (regex present in IMPORTANT section and awk examples)
- [x] Check 6: CSV via Bash — OK (Bash examples shown, Read allowed for <200-row files)
- [x] Check 7: Performance CSV comma — N/A
- [x] Check 8: Chain-of-evidence — OK ("Every numeric value must include `source` and `extraction`")
- [x] Check 9: max-turns — NOTE: not mentioned (expected: 150)
- [x] Check 10: No hardcoded data — OK (template values in output format section)
- **Issues found:** None
- **Fixes applied:** None

### 02a-parse-freesoft-ru-keywords.md
- [x] Check 1: File paths — OK (2 CSV + 2 PNG, all match ARCHITECTURE.md)
- [x] Check 2: Output path — OK (`briefs/02a-freesoft-ru-kw.yaml`)
- [x] Check 3: Self-contained — OK
- [x] Check 4: Verification — OK (5 checks)
- [x] Check 5: Gambling filter — OK
- [x] Check 6: CSV via Bash — OK (explicit "LARGE FILES — Bash only" instruction)
- [x] Check 7: Performance CSV comma — N/A
- [x] Check 8: Chain-of-evidence — OK
- [x] Check 9: max-turns — NOTE: not mentioned (expected: 150)
- [x] Check 10: No hardcoded data — OK
- **Issues found:** None
- **Fixes applied:** None

### 02b-parse-freesoft-ru-pages.md
- [x] Check 1: File paths — OK (2 CSV, no PNG, matches ARCHITECTURE.md)
- [x] Check 2: Output path — OK (`briefs/02b-freesoft-ru-pages.yaml`)
- [x] Check 3: Self-contained — OK
- [x] Check 4: Verification — OK (5 checks)
- [x] Check 5: Gambling filter — OK
- [x] Check 6: CSV via Bash — OK
- [x] Check 7: Performance CSV comma — N/A
- [x] Check 8: Chain-of-evidence — OK
- [x] Check 9: max-turns — NOTE: not mentioned (expected: 150)
- [x] Check 10: No hardcoded data — OK
- **Issues found:** None
- **Fixes applied:** None

### 03-parse-freesoft-fr.md
- [x] Check 1: File paths — OK (9 CSV + 2 PNG, all filenames match ARCHITECTURE.md including duplicates and perf CSVs)
- [x] Check 2: Output path — OK (`briefs/03-freesoft-fr.yaml`)
- [x] Check 3: Self-contained — OK
- [x] Check 4: Verification — OK (7 checks including performance CSV validation)
- [x] Check 5: Gambling filter — OK
- [x] Check 6: CSV via Bash — OK
- [x] Check 7: Performance CSV comma — **OK** (explicitly states "COMMA vs TAB delimiters", `awk -F','` examples, multiple warnings)
- [x] Check 8: Chain-of-evidence — OK
- [x] Check 9: max-turns — NOTE: not mentioned (expected: 150)
- [x] Check 10: No hardcoded data — OK
- **Issues found:** None
- **Fixes applied:** None

### 04a-parse-uptodown-structure.md
- [x] Check 1: File paths — OK (1 CSV + 1 PNG, matches ARCHITECTURE.md)
- [x] Check 2: Output path — OK (`briefs/04a-uptodown-struct.yaml`)
- [x] Check 3: Self-contained — OK
- [x] Check 4: Verification — OK (5 checks)
- [x] Check 5: Gambling filter — OK
- [x] Check 6: CSV via Bash — OK
- [x] Check 7: Performance CSV comma — N/A
- [x] Check 8: Chain-of-evidence — OK
- [x] Check 9: max-turns — NOTE: not mentioned (expected: 150)
- [x] Check 10: No hardcoded data — OK
- **Issues found:** None
- **Fixes applied:** None
- **Note:** Edge cases covered: empty CSV check, 500+ subdomains filter, language_structure detection

### 04b-parse-uptodown-pages.md
- [x] Check 1: File paths — OK (2 CSV, filenames match ARCHITECTURE.md)
- [x] Check 2: Output path — OK (`briefs/04b-uptodown-pages.yaml`)
- [x] Check 3: Self-contained — OK
- [x] Check 4: Verification — OK (6 checks)
- [x] Check 5: Gambling filter — OK
- [x] Check 6: CSV via Bash — OK
- [x] Check 7: Performance CSV comma — N/A
- [x] Check 8: Chain-of-evidence — OK
- [x] Check 9: max-turns — NOTE: not mentioned (expected: 200)
- [x] Check 10: No hardcoded data — OK
- **Issues found:** None
- **Fixes applied:** None
- **Note:** Prompt says "30,001" rows for actual CSV; ARCHITECTURE says 30045. Informational only — agent verifies with `wc -l`.

### 05a-parse-softonic-com-structure.md
- [x] Check 1: File paths — OK (1 CSV + 1 PNG, matches ARCHITECTURE.md)
- [x] Check 2: Output path — OK (`briefs/05a-softonic-com-struct.yaml`)
- [x] Check 3: Self-contained — OK
- [x] Check 4: Verification — OK (5 checks)
- [x] Check 5: Gambling filter — OK
- [x] Check 6: CSV via Bash — OK
- [x] Check 7: Performance CSV comma — N/A
- [x] Check 8: Chain-of-evidence — OK
- [x] Check 9: max-turns — NOTE: not mentioned (expected: 150)
- [x] Check 10: No hardcoded data — OK
- **Issues found:** None
- **Fixes applied:** None
- **Note:** Correctly documents RU filter caveat on PNG

### 05b-parse-softonic-com-pages.md
- [x] Check 1: File paths — OK (2 CSV, filenames match ARCHITECTURE.md)
- [x] Check 2: Output path — OK (`briefs/05b-softonic-com-pages.yaml`)
- [x] Check 3: Self-contained — OK
- [x] Check 4: Verification — OK (6 checks)
- [x] Check 5: Gambling filter — OK
- [x] Check 6: CSV via Bash — OK
- [x] Check 7: Performance CSV comma — N/A
- [x] Check 8: Chain-of-evidence — OK
- [x] Check 9: max-turns — NOTE: not mentioned (expected: 200)
- [x] Check 10: No hardcoded data — OK
- **Issues found:** None
- **Fixes applied:** None
- **Note:** Prompt says "30,001" rows for both CSVs; ARCHITECTURE says 30029 and 30050. Informational only.

### 05c-parse-softonic-ru.md
- [x] Check 1: File paths — OK (1 CSV + 1 PNG, matches ARCHITECTURE.md)
- [x] Check 2: Output path — OK (`briefs/05c-softonic-ru.yaml`)
- [x] Check 3: Self-contained — OK
- [x] Check 4: Verification — OK (5 checks)
- [x] Check 5: Gambling filter — OK
- [x] Check 6: CSV via Bash — OK
- [x] Check 7: Performance CSV comma — N/A
- [x] Check 8: Chain-of-evidence — OK
- [x] Check 9: max-turns — NOTE: not mentioned (expected: 150)
- [x] Check 10: No hardcoded data — OK
- **Issues found:** None
- **Fixes applied:** None
- **Note:** Correctly identifies "separate_domain" strategy and references softonic.com comparison

### 06a-parse-malavida-structure.md
- [x] Check 1: File paths — OK (1 CSV + 1 PNG, matches ARCHITECTURE.md)
- [x] Check 2: Output path — OK (`briefs/06a-malavida-struct.yaml`)
- [x] Check 3: Self-contained — OK
- [x] Check 4: Verification — OK (6 checks)
- [x] Check 5: Gambling filter — OK
- [x] Check 6: CSV via Bash — OK
- [x] Check 7: Performance CSV comma — N/A
- [x] Check 8: Chain-of-evidence — OK
- [x] Check 9: max-turns — NOTE: not mentioned (expected: 150)
- [x] Check 10: No hardcoded data — OK
- **Issues found:** None
- **Fixes applied:** None

### 06b-parse-malavida-pages.md
- [x] Check 1: File paths — OK (2 CSV, filenames match ARCHITECTURE.md)
- [x] Check 2: Output path — OK (`briefs/06b-malavida-pages.yaml`)
- [x] Check 3: Self-contained — OK
- [x] Check 4: Verification — OK (6 checks)
- [x] Check 5: Gambling filter — OK
- [x] Check 6: CSV via Bash — OK
- [x] Check 7: Performance CSV comma — N/A
- [x] Check 8: Chain-of-evidence — OK
- [x] Check 9: max-turns — NOTE: not mentioned (expected: 200)
- [x] Check 10: No hardcoded data — OK
- **Issues found:** None
- **Fixes applied:** None

### 07a-parse-filehippo.md
- [x] Check 1: File paths — OK (1 CSV + 1 PNG, matches ARCHITECTURE.md)
- [x] Check 2: Output path — OK (`briefs/07a-filehippo.yaml`)
- [x] Check 3: Self-contained — OK
- [x] Check 4: Verification — OK (5 checks)
- [x] Check 5: Gambling filter — OK
- [x] Check 6: CSV via Bash — OK
- [x] Check 7: Performance CSV comma — N/A
- [x] Check 8: Chain-of-evidence — OK
- [x] Check 9: max-turns — NOTE: not mentioned (expected: 150)
- [x] Check 10: No hardcoded data — OK
- **Issues found:** None
- **Fixes applied:** None
- **Note:** Correctly handles single-language control case

### 07b-parse-trashbox.md
- [x] Check 1: File paths — OK (1 CSV + 1 PNG, matches ARCHITECTURE.md)
- [x] Check 2: Output path — OK (`briefs/07b-trashbox.yaml`)
- [x] Check 3: Self-contained — OK
- [x] Check 4: Verification — OK (6 checks including decline metrics)
- [x] Check 5: Gambling filter — OK
- [x] Check 6: CSV via Bash — OK
- [x] Check 7: Performance CSV comma — N/A
- [x] Check 8: Chain-of-evidence — OK
- [x] Check 9: max-turns — NOTE: not mentioned (expected: 150)
- [x] Check 10: No hardcoded data — OK
- **Issues found:** None
- **Fixes applied:** None
- **Note:** Good: correctly separates content subdomains from language subdomains

### 08a-parse-clubic.md
- [x] Check 1: File paths — OK (1 CSV + 1 PNG, matches ARCHITECTURE.md)
- [x] Check 2: Output path — OK (`briefs/08a-clubic.yaml`)
- [x] Check 3: Self-contained — OK
- [x] Check 4: Verification — OK (5 checks)
- [x] Check 5: Gambling filter — OK
- [x] Check 6: CSV via Bash — OK
- [x] Check 7: Performance CSV comma — N/A
- [x] Check 8: Chain-of-evidence — OK
- [x] Check 9: max-turns — NOTE: not mentioned (expected: 150)
- [x] Check 10: No hardcoded data — OK
- **Issues found:** None
- **Fixes applied:** None
- **Note:** Good: includes deep analysis of download pages and French URL patterns

### 08b-parse-01net.md
- [x] Check 1: File paths — OK (1 CSV + 1 PNG, matches ARCHITECTURE.md)
- [x] Check 2: Output path — OK (`briefs/08b-01net.yaml`)
- [x] Check 3: Self-contained — OK
- [x] Check 4: Verification — OK (6 checks)
- [x] Check 5: Gambling filter — OK
- [x] Check 6: CSV via Bash — OK
- [x] Check 7: Performance CSV comma — N/A
- [x] Check 8: Chain-of-evidence — OK
- [x] Check 9: max-turns — NOTE: not mentioned (expected: 150)
- [x] Check 10: No hardcoded data — OK
- **Issues found:** None
- **Fixes applied:** None
- **Note:** Correctly documents massive decline (-2.2M traffic, -925K keywords)

### 08c-parse-commentcamarche.md
- [x] Check 1: File paths — OK (1 CSV + 1 PNG with typo `ommentcamarche_net_overview.png`, correctly documented)
- [x] Check 2: Output path — OK (`briefs/08c-commentcamarche.yaml`)
- [x] Check 3: Self-contained — OK
- [x] Check 4: Verification — OK (7 checks including PNG filename typo check)
- [x] Check 5: Gambling filter — OK
- [x] Check 6: CSV via Bash — OK
- [x] Check 7: Performance CSV comma — N/A
- [x] Check 8: Chain-of-evidence — OK
- [x] Check 9: max-turns — NOTE: not mentioned (expected: 150)
- [x] Check 10: No hardcoded data — OK
- **Issues found:** None
- **Fixes applied:** None
- **Note:** PNG filename typo correctly handled — uses actual filename `ommentcamarche_net_overview.png` with explanatory note

### 10-validate-briefs.md
- [x] Check 1: File paths — OK (lists all 16 expected brief files)
- [x] Check 2: Output path — OK (`briefs/10-validation-result.yaml`)
- [x] Check 3: Self-contained — OK (references ARCHITECTURE.md for brief formats)
- [x] Check 4: Verification — OK (4 checks)
- [x] Check 5: Gambling filter — OK (correctly states "No gambling filter needed")
- [x] Check 6: CSV via Bash — N/A (reads YAML briefs, not CSV)
- [x] Check 7: Performance CSV comma — N/A
- [x] Check 8: Chain-of-evidence — OK (validates chain-of-evidence in briefs via spot-check)
- [x] Check 9: max-turns — NOTE: not mentioned (expected: 50)
- [x] Check 10: No hardcoded data — OK
- **Issues found:** None
- **Fixes applied:** None
- **Note:** Correctly validates 16 briefs (ARCHITECTURE.md says "17 файлов" in the Phase 1.5 description, but actual Phase 1 task count is 16 — this is a minor error in ARCHITECTURE.md, not in the prompt). Correctly handles frees0ft.fr special case (very low traffic is not an error).

---

## Cross-Cutting Observations

### 1. max-turns Not Mentioned in Any Prompt (non-critical)

None of the 19 prompts mention the expected max-turns budget. ARCHITECTURE.md specifies:

| Task | Expected max-turns |
|------|--------------------|
| 00-inventory | 100 |
| 00b-convert-encoding | 50 |
| 01, 02a, 02b, 03 | 150 |
| 04a, 05a, 05c, 06a | 150 |
| 04b, 05b, 06b | 200 |
| 07a, 07b | 150 |
| 08a, 08b, 08c | 150 |
| 10-validate-briefs | 50 |

**Assessment:** Non-critical. The max-turns value is set by the orchestrator (`run.sh`) via `--max-turns` flag to `claude -p`. The agent doesn't strictly need to know its budget. However, adding it as context in the prompt could help the agent pace itself on complex tasks.

**Recommendation:** Consider adding a one-liner like `**Turn budget:** 150 max-turns` to each prompt's Context section. Not required for pipeline to function.

### 2. Minor Row Count Approximations (informational)

Three prompts use approximate row counts that differ slightly from ARCHITECTURE.md:

| Prompt | File | Prompt says | ARCHITECTURE says |
|--------|------|-------------|-------------------|
| 04b | `uptodown_com_top_pages...all_act...csv` | 30,001 | 30,045 |
| 05b | `softonic_com_top_pages...all_act...csv` | 30,001 | 30,029 |
| 05b | `softonic_com_top_pages...all_com...csv` | 30,001 | 30,050 |

**Assessment:** Non-functional. All three prompts instruct the agent to verify row count with `wc -l`. The approximate values are informational context only and don't affect extraction logic.

### 3. ARCHITECTURE.md Minor Inconsistency (not a prompt issue)

ARCHITECTURE.md states "17 tasks" for Phase 1 (line 15) and "17 файлов" for Phase 1.5 validation (line 398), but the actual Phase 1 task count is **16**. The 10-validate-briefs.md prompt correctly uses 16. This is an error in ARCHITECTURE.md itself, not in the prompts.

### 4. All Edge Cases Properly Covered

Every Phase 1 prompt includes the required edge case handling from ARCHITECTURE.md section "Обработка edge cases":

| Edge Case | Coverage |
|-----------|----------|
| Empty/corrupted CSV (`wc -l < file; if <2...`) | Structure tasks (04a, 05a, 05c, 06a, 07a, 07b) — explicit check |
| Unreadable PNG ("НЕ ВИДНО НА СКРИНШОТЕ") | All prompts with PNG — covered |
| No language data ("single_language") | Structure tasks — covered |
| 500+ subdomains filter (traffic > 100) | Structure tasks — covered |
| Gambling/adult content (regex filter) | All Phase 1 prompts — covered |

### 5. Prompt Quality Assessment

All 19 prompts follow the PROMPT_ENGINEERING.md template:
- ✅ Role + one-sentence goal
- ✅ Context section
- ✅ "Before You Start — Read These Files" section
- ✅ Task section with input file tables
- ✅ Tools section with examples
- ✅ Numbered Steps
- ✅ Output Format with YAML template
- ✅ Verification section
- ✅ IMPORTANT section with constraints

Average prompt length: ~250 lines (~1500 words) — within the recommended sweet spot.

---

## Verification of This Review

1. ✅ All 19 prompt files exist and were read in full
2. ✅ This review report exists at `pipeline-seo/meta/review-1-report.md`
3. ✅ No Phase 1 prompt references `data_for_task/` for CSV files (only `data_utf8/`)
4. ✅ All 16 Phase 1 prompts contain the gambling regex
5. ✅ Task 10 correctly omits the gambling filter
6. ✅ Task 00 correctly reads from `data_for_task/` (pre-conversion)

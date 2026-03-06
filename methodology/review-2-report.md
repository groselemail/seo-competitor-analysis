# Review Report: Phase 2 + Phase 3 + Phase 4 + Phase 5 Prompts

> Reviewed: 2026-03-06
> Reviewer: QA Engineer (automated)
> Source of truth: `pipeline-seo/ARCHITECTURE.md`

## Summary

- **Files reviewed:** 10
- **Files with issues:** 7 (minor — missing max-turns only)
- **Total fixes applied:** 7
- **Status:** PASS

All 10 prompts are structurally correct with proper input/output paths, self-contained context, verification sections, chain-of-evidence instructions, and no raw data references. The only issue was missing `max-turns` declarations in 7 Phase 2/3 prompts, now fixed.

## Per-File Results

### 11-analyze-our-domains.md
- [x] Check 1: Input briefs — OK (4 briefs: 01, 02a, 02b, 03 — all with `pipeline-seo/` prefix)
- [x] Check 2: Output path — OK (`pipeline-seo/briefs/11-our-state.yaml`)
- [x] Check 3: Self-contained — OK (no "continue from", no cross-prompt refs)
- [x] Check 4: Verification section — OK (line 200)
- [x] Check 5: No raw CSV/PNG — OK (says "Do NOT read raw CSV or PNG files")
- [x] Check 6: Chain-of-evidence — OK (instructs citing `source: "briefs/XX.yaml"`)
- [x] Check 7: No hardcoded data — OK (context hints present, instructs to use brief values)
- [x] Check 8: max-turns — **FIXED** (added `max-turns: 200`)
- [x] Check 9: N/A (Phase 2 — parallel, no sequential deps)
- [x] Check 10: N/A (not a report task)

### 12-analyze-multilingual-competitors.md
- [x] Check 1: Input briefs — OK (7 briefs: 04a, 04b, 05a, 05b, 05c, 06a, 06b)
- [x] Check 2: Output path — OK (`pipeline-seo/briefs/12-multilingual-analysis.yaml`)
- [x] Check 3: Self-contained — OK
- [x] Check 4: Verification section — OK (line 221)
- [x] Check 5: No raw CSV/PNG — OK
- [x] Check 6: Chain-of-evidence — OK
- [x] Check 7: No hardcoded data — OK
- [x] Check 8: max-turns — **FIXED** (added `max-turns: 200`)
- [x] Check 9: N/A (Phase 2)
- [x] Check 10: N/A

### 13-analyze-fr-market.md
- [x] Check 1: Input briefs — OK (4 briefs: 03, 08a, 08b, 08c)
- [x] Check 2: Output path — OK (`pipeline-seo/briefs/13-fr-market-analysis.yaml`)
- [x] Check 3: Self-contained — OK
- [x] Check 4: Verification section — OK (line 248)
- [x] Check 5: No raw CSV/PNG — OK
- [x] Check 6: Chain-of-evidence — OK
- [x] Check 7: No hardcoded data — OK (frees0ft.fr ~21.6K hint, but says use brief values)
- [x] Check 8: max-turns — **FIXED** (added `max-turns: 200`)
- [x] Check 9: N/A (Phase 2)
- [x] Check 10: N/A

### 14-analyze-domain-structures.md
- [x] Check 1: Input briefs — OK (6 briefs: 04a, 05a, 05c, 06a, 07a, 07b)
- [x] Check 2: Output path — OK (`pipeline-seo/briefs/14-domain-structures.yaml`)
- [x] Check 3: Self-contained — OK
- [x] Check 4: Verification section — OK (line 269)
- [x] Check 5: No raw CSV/PNG — OK
- [x] Check 6: Chain-of-evidence — OK
- [x] Check 7: No hardcoded data — OK
- [x] Check 8: max-turns — **FIXED** (added `max-turns: 200`)
- [x] Check 9: N/A (Phase 2)
- [x] Check 10: N/A

### 16-language-potential.md
- [x] Check 1: Input briefs — OK (3 briefs: 11, 12, 13 — Phase 2 outputs)
- [x] Check 2: Output path — OK (`pipeline-seo/briefs/16-language-potential.yaml`)
- [x] Check 3: Self-contained — OK
- [x] Check 4: Verification section — OK (line 233)
- [x] Check 5: No raw CSV/PNG — OK
- [x] Check 6: Chain-of-evidence — OK
- [x] Check 7: No hardcoded data — OK (context hints like "168K" but instructs reading briefs)
- [x] Check 8: max-turns — **FIXED** (added `max-turns: 200`)
- [x] Check 9: Sequential deps — OK (reads briefs 11+12+13, all Phase 2 = done before Phase 3)
- [x] Check 10: N/A

### 17-domain-strategy.md
- [x] Check 1: Input briefs — OK (2 briefs: 14, 16)
- [x] Check 2: Output path — OK (`pipeline-seo/briefs/17-domain-strategy.yaml`)
- [x] Check 3: Self-contained — OK
- [x] Check 4: Verification section — OK (line 275)
- [x] Check 5: No raw CSV/PNG — OK
- [x] Check 6: Chain-of-evidence — OK
- [x] Check 7: No hardcoded data — OK (context values for current state, but reads from briefs)
- [x] Check 8: max-turns — **FIXED** (added `max-turns: 200`)
- [x] Check 9: Sequential deps — OK (reads brief 14 from Phase 2 + brief 16 just completed)
- [x] Check 10: N/A

### 18-roadmap-draft.md
- [x] Check 1: Input briefs — OK (2 briefs: 16, 17)
- [x] Check 2: Output path — OK (`pipeline-seo/briefs/18-roadmap-draft.yaml`)
- [x] Check 3: Self-contained — OK
- [x] Check 4: Verification section — OK (line 330)
- [x] Check 5: No raw CSV/PNG — OK
- [x] Check 6: Chain-of-evidence — OK
- [x] Check 7: No hardcoded data — OK
- [x] Check 8: max-turns — **FIXED** (added `max-turns: 200`)
- [x] Check 9: Sequential deps — OK (reads brief 16 + brief 17 just completed)
- [x] Check 10: N/A

### 20-report-domain-strategy.md
- [x] Check 1: Input briefs — OK (4 briefs: 11, 14, 16, 17)
- [x] Check 2: Output path — OK (`pipeline-seo/output/domain-strategy.md`)
- [x] Check 3: Self-contained — OK
- [x] Check 4: Verification section — OK (line 222)
- [x] Check 5: No raw CSV/PNG — OK
- [x] Check 6: Chain-of-evidence — OK (inline citations `(brief 11)` etc.)
- [x] Check 7: No hardcoded data — OK
- [x] Check 8: max-turns — OK (150, line 292)
- [x] Check 9: N/A (Phase 4 — parallel)
- [x] Check 10: Russian language — OK ("Language: Russian", line 276)

### 21-report-multilingual-roadmap.md
- [x] Check 1: Input briefs — OK (6 briefs: 11, 12, 13, 16, 17, 18)
- [x] Check 2: Output path — OK (`pipeline-seo/output/multilingual-roadmap.md`)
- [x] Check 3: Self-contained — OK
- [x] Check 4: Verification section — OK (line 266)
- [x] Check 5: No raw CSV/PNG — OK
- [x] Check 6: Chain-of-evidence — OK
- [x] Check 7: No hardcoded data — OK
- [x] Check 8: max-turns — OK (150, line 352)
- [x] Check 9: N/A (Phase 4)
- [x] Check 10: Russian language — OK ("Language: Russian", line 332)

### 22-validate.md
- [x] Check 1: Input briefs — OK (12 files: 2 reports + 7 Phase 2/3 briefs + 3 Phase 1 spot-check briefs)
- [x] Check 2: Output path — OK (`pipeline-seo/output/validation-report.md`)
- [x] Check 3: Self-contained — OK
- [x] Check 4: Verification section — OK (line 275)
- [x] Check 5: No raw CSV/PNG — OK (references Phase 1 briefs for spot-check, not raw CSVs)
- [x] Check 6: Chain-of-evidence — OK (traces from report → Phase 2/3 brief → Phase 1 brief)
- [x] Check 7: No hardcoded data — OK
- [x] Check 8: max-turns — OK (150, line 343)
- [x] Check 9: N/A (Phase 5)
- [x] Check 10: N/A (validation report, language flexible)

## Cross-Cutting Issues

### Issue 1: Missing max-turns (FIXED)

7 of 10 prompts (all Phase 2 and Phase 3 tasks) were missing `max-turns` declarations. Tasks 20, 21, 22 had them. Fixed by adding `- **max-turns:** 200` to the IMPORTANT section of each affected prompt, matching the style used in tasks 20/21/22.

| Task | Expected | Before | After |
|------|----------|--------|-------|
| 11 | 200 | missing | 200 |
| 12 | 200 | missing | 200 |
| 13 | 200 | missing | 200 |
| 14 | 200 | missing | 200 |
| 16 | 200 | missing | 200 |
| 17 | 200 | missing | 200 |
| 18 | 200 | missing | 200 |
| 20 | 150 | 150 | 150 |
| 21 | 150 | 150 | 150 |
| 22 | 150 | 150 | 150 |

### No Other Issues Found

All other checks passed cleanly across all 10 files:

- **Input brief paths:** All match ARCHITECTURE.md exactly, all prefixed with `pipeline-seo/`
- **Output paths:** All match ARCHITECTURE.md exactly
- **Self-contained:** No prompt references another prompt's content or says "continue"
- **Verification sections:** All 10 prompts have `## Verification` with Bash checks
- **No raw CSV/PNG:** All Phase 2+ prompts explicitly say "Do NOT read raw CSV or PNG files"
- **Chain-of-evidence:** All prompts instruct citing `source: "briefs/XX.yaml"`
- **No hardcoded data:** Context hints present (e.g., "168K traffic") but all prompts instruct reading briefs
- **Phase 3 dependencies:** Correct chain: 16 reads {11,12,13} → 17 reads {14,16} → 18 reads {16,17}
- **Russian output:** Tasks 20/21 explicitly instruct "Language: Russian"
- **Gambling filter:** Tasks 20/21/22 include gambling filter checks in verification

## Verification

1. All 10 prompt files exist and are non-empty: verified
2. This review report exists: yes
3. No Phase 2+ prompt references `data_utf8/` or `data_for_task/`: confirmed
4. Phase 3 dependency chain: 16←{11,12,13}, 17←{14,16}, 18←{16,17}: correct
5. Tasks 20/21 instruct Russian language output: confirmed
6. Task 22 reads both output reports + 7 Phase 2/3 briefs + 3 Phase 1 spot-check briefs: confirmed

# SEO Competitor Analysis: Multilingual Expansion for freesoft.net

## Executive Summary (RU)

Проведён комплексный SEO-анализ конкурентов в нише скачивания софта на основе 51 файла данных Ahrefs по 9 конкурентам. Портфель freesoft состоит из трёх доменов с суммарным трафиком ~222 000 визитов/мес., при этом 75,7% трафика сконцентрировано на одном русскоязычном домене freesoft.ru (168 000, DR 59). Анализ показал критическую зависимость от одного языка и рынка: монолингвальные .ru-сайты демонстрируют системное падение (trashbox.ru: −47%, softonic.ru: −578K). Все три ведущих конкурента (softonic.com, uptodown.com, malavida.com) используют мультиязычные поддомены на 9–14 языках. Рекомендуется гибридная стратегия: сохранить freesoft.ru для русского рынка, консолидировать остальные языки на поддоменах freesoft.net. Потенциал роста — с ~222K до 500K–880K трафика (2,3–4,0x) за 6–18 месяцев через запуск 5 новых языков (ES, AR, PT, ID, VI). Все ~180 числовых утверждений верифицированы против первичных источников Ahrefs: 0 критических расхождений.

## Executive Summary (EN)

A comprehensive SEO competitor analysis of the software download niche based on 51 Ahrefs data files covering 9 competitors. The freesoft portfolio generates ~222K monthly organic visits across three domains, with 75.7% concentrated on a single Russian-language domain (freesoft.ru). A hybrid domain strategy is recommended: retain freesoft.ru for the Russian market while consolidating all other languages on freesoft.net subdomains (es/ar/pt/id/vi.freesoft.net). The projected growth is 2.3–4.0x (to 500K–880K visits) over 6–18 months. All numerical claims have been verified against primary Ahrefs sources with zero critical discrepancies.

## Key Findings

| Language / Market | Traffic Potential | Priority | Source |
|---|---|---|---|
| Spanish (ES) | +134K (TAM 9.9M) | #1 new language | [language-potential.yaml](analysis/cross-analysis/language-potential.yaml) |
| English (EN) | +132K (optimization gap) | #1 existing | [our-state.yaml](analysis/cross-analysis/our-state.yaml) |
| Arabic (AR) | +93.5K (TAM 3.5M, 1 competitor) | #2 new language | [language-potential.yaml](analysis/cross-analysis/language-potential.yaml) |
| French (FR) | +65K (migration + growth) | Existing, migrate | [french-market.yaml](analysis/cross-analysis/french-market.yaml) |
| Russian (RU) | +55K (optimization) | Existing, protect | [our-state.yaml](analysis/cross-analysis/our-state.yaml) |
| Brazilian PT | +53K (TAM 2.9M) | #3 new language | [language-potential.yaml](analysis/cross-analysis/language-potential.yaml) |
| Indonesian (ID) | +43K (TAM 1.6M) | #4 new language | [language-potential.yaml](analysis/cross-analysis/language-potential.yaml) |
| Vietnamese (VI) | +31K (TAM 1.7M) | #5 new language | [language-potential.yaml](analysis/cross-analysis/language-potential.yaml) |

## Recommended Strategy

Hybrid approach (Option D): retain freesoft.ru as a standalone domain for the Russian market (168K traffic, DR 59 — zero migration risk) and consolidate everything else on freesoft.net subdomains. This mirrors the proven subdomain model used by all three leading competitors (softonic.com, uptodown.com, malavida.com) while protecting the primary traffic asset. The only migration — frees0ft.fr to fr.freesoft.net — carries low risk (DR 23, 24 followed referring domains). The strategy is reversible: full consolidation onto freesoft.net can be evaluated once its DR surpasses freesoft.ru.

## Repository Structure

```
seo-competitor-analysis/
├── reports/             — Final client-facing reports
├── analysis/
│   ├── competitors/     — Per-competitor YAML analysis
│   ├── cross-analysis/  — Cross-competitor synthesis
│   └── our-domains/     — freesoft.net / .ru / .fr analysis
├── validation/          — Fact-checking and chain of evidence
├── methodology/         — Pipeline architecture and audit logs
└── raw-data/            — Description of source Ahrefs exports
```

## Quick Navigation

- **Start here:** [Executive Summary](reports/executive-summary.md)
- **Strategy:** [Domain Strategy](reports/domain-strategy.md)
- **Roadmap:** [Multilingual Roadmap](reports/multilingual-roadmap.md)
- **Fact-checking:** [How to verify](validation/README.md)
- **Methodology:** [Pipeline architecture](methodology/architecture.md)

## Methodology

The analysis was executed as a pipeline of 29 tasks processing 51 Ahrefs data files across 9 competitors using Claude Opus. Each task produced structured YAML artifacts that feed into cross-analysis and final reports. For details see [methodology/](methodology/README.md).

## How to Verify

1. Pick any numerical claim from the reports (e.g., "freesoft.ru DR 59")
2. Find the source reference (e.g., "brief 11")
3. Trace it through [chain-of-evidence.md](validation/chain-of-evidence.md) to the original Ahrefs data
4. Cross-check against the validation results in [validation-report.md](validation/validation-report.md)

## Data Sources

All data originates from Ahrefs exports (organic traffic, keywords, backlinks, domain ratings) collected in March 2026. For the full inventory of 51 source files and their mapping to analysis tasks, see [data-sources.md](methodology/data-sources.md).

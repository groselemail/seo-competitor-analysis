# SEO Competitor Analysis: Multilingual Expansion for freesoft.net

## Executive Summary (RU)

Проведён комплексный SEO-анализ конкурентов в нише скачивания софта на основе 51 файла данных Ahrefs по 9 конкурентам. Портфель freesoft состоит из трёх доменов с суммарным трафиком ~222 000 визитов/мес., при этом 75,7% трафика сконцентрировано на одном русскоязычном домене freesoft.ru (168 000, DR 59). Анализ показал критическую зависимость от одного языка и рынка: монолингвальные .ru-сайты демонстрируют системное падение (trashbox.ru: −47%, softonic.ru: −578K). Все три ведущих конкурента (softonic.com, uptodown.com, malavida.com) используют мультиязычные поддомены на 9–14 языках (7–8 с измеримым трафиком). Рекомендуется гибридная стратегия: сохранить freesoft.ru для русского рынка, консолидировать остальные языки на поддоменах freesoft.net. Потенциал роста — с ~222K до 500K–880K трафика (2,3–4,0x) за 6–18 месяцев через запуск 5 новых языков (ES, AR, PT, ID, VI). Все ~180 числовых утверждений верифицированы против первичных источников Ahrefs: 0 критических расхождений.

### Ссылочный анализ (Phase 2)

Проведён комплексный анализ ссылочных профилей 12 доменов на основе 39 CSV-файлов Ahrefs (~660 000 строк). 4 исследования: ссылочный ландшафт ниши, языковые стратегии конкурентов, PBN-детекция, пересечения доменов.

**Ключевые находки:**
- **freesoft.net (DR 51):** Критическое загрязнение спамом — 89.3% (медиана ниши — 42%). Необходим disavow ~3 000 доменов
- **freesoft.ru (DR 59):** Сильнейший домен, но низкий dofollow (35.5% vs медиана 68.1%)
- **frees0ft.fr (DR 23):** Нулевая ссылочная ценность (95.7% nofollow, 88.9% спам) — подтверждает необходимость миграции
- **5 099 EN-targets** — домены, ссылающиеся на конкурентов, но не на нас
- **662 автоматические проверки**, 99.4% pass rate — данные верифицированы

Подробнее: [reports/backlink-strategy/](reports/backlink-strategy/INDEX.md)

## Ключевые находки

| Язык / Рынок | Потенциал трафика | Приоритет | Источник |
|---|---|---|---|
| Испанский (ES) | +134K (TAM 9.9M) | #1 новый язык | [language-potential.yaml](analysis/cross-analysis/language-potential.yaml) |
| Английский (EN) | +132K (optimization gap) | #1 существующий | [our-state.yaml](analysis/cross-analysis/our-state.yaml) |
| Арабский (AR) | +93.5K (TAM 3.5M, 1 конкурент) | #2 новый язык | [language-potential.yaml](analysis/cross-analysis/language-potential.yaml) |
| Французский (FR) | +65K (миграция + рост) | Существующий, миграция | [french-market.yaml](analysis/cross-analysis/french-market.yaml) |
| Русский (RU) | +55K (оптимизация) | Существующий, защита | [our-state.yaml](analysis/cross-analysis/our-state.yaml) |
| Бразильский PT | +53K (TAM 2.9M) | #3 новый язык | [language-potential.yaml](analysis/cross-analysis/language-potential.yaml) |
| Индонезийский (ID) | +43K (TAM 1.6M) | #4 новый язык | [language-potential.yaml](analysis/cross-analysis/language-potential.yaml) |
| Вьетнамский (VI) | +31K (TAM 1.7M) | #5 новый язык | [language-potential.yaml](analysis/cross-analysis/language-potential.yaml) |

## Рекомендованная стратегия

Гибридный подход (Option D): сохранить freesoft.ru как отдельный домен для русского рынка (168K трафика, DR 59 — нулевой риск миграции) и консолидировать все остальные языки на поддоменах freesoft.net. Это повторяет проверенную модель поддоменов, которую используют все три ведущих конкурента (softonic.com, uptodown.com, malavida.com), при этом защищая основной трафиковый актив. Единственная миграция — frees0ft.fr на fr.freesoft.net — несёт низкий риск (DR 23, 24 followed referring domains). Стратегия обратима: полную консолидацию на freesoft.net можно рассмотреть, когда его DR превысит DR freesoft.ru.

## Структура репозитория

```
seo-competitor-analysis/
├── reports/
│   ├── executive-summary.md      — Executive Summary (Phase 1)
│   ├── domain-strategy.md        — Доменная стратегия (Phase 1)
│   ├── multilingual-roadmap.md   — Мультиязычный roadmap (Phase 1)
│   └── backlink-strategy/        — Ссылочный анализ (Phase 2, 9 файлов)
├── analysis/
│   ├── competitors/              — YAML-аналитика по конкурентам (Phase 1)
│   ├── cross-analysis/           — Кросс-анализ и синтез (Phase 1)
│   ├── our-domains/              — Анализ freesoft.net / .ru / .fr (Phase 1)
│   └── backlink-strategy/        — Pipeline ссылочного анализа (Phase 2)
│       └── pipeline/             — JSON-агрегаты, секции R1-R4, Python-скрипты
├── validation/                   — Fact-checking и цепочка доказательств
├── methodology/                  — Архитектура pipeline и отчёты аудита
└── raw-data/                     — Описание исходных выгрузок Ahrefs
```

## Быстрая навигация

### Органический анализ (Phase 1)

- **Начните здесь:** [Executive Summary](reports/executive-summary.md)
- **Стратегия:** [Domain Strategy](reports/domain-strategy.md)
- **Roadmap:** [Multilingual Roadmap](reports/multilingual-roadmap.md)
- **Fact-checking:** [Как верифицировать](validation/README.md)
- **Методология:** [Архитектура pipeline](methodology/architecture.md)

### Ссылочный анализ (Phase 2)

| Документ | Описание |
|----------|----------|
| [Краткая сводка](reports/backlink-strategy/01-executive-brief.md) | 1-2 страницы для руководства |
| [Полный отчёт](reports/backlink-strategy/02-full-report.md) | R1-R4, кросс-анализ, стратегия |
| [Целевые домены](reports/backlink-strategy/03-target-domains.md) | 5 099 EN + 49 RU + 4 369 FR targets |
| [План disavow](reports/backlink-strategy/04-disavow-plan.md) | Паттерны, шаблоны, мониторинг |
| [Roadmap внедрения](reports/backlink-strategy/05-implementation-roadmap.md) | Чек-листы по неделям/месяцам |
| [Карточки конкурентов](reports/backlink-strategy/06-competitor-cards.md) | 9 карточек с метриками |

### Навигация по ролям

| Роль | Органический анализ (Phase 1) | Ссылочный анализ (Phase 2) |
|------|-------------------------------|----------------------------|
| PM / руководство | [Executive Summary](reports/executive-summary.md) | [Краткая сводка](reports/backlink-strategy/01-executive-brief.md) |
| SEO-стратег | [Доменная стратегия](reports/domain-strategy.md), [Roadmap](reports/multilingual-roadmap.md) | [Полный отчёт](reports/backlink-strategy/02-full-report.md), [Targets](reports/backlink-strategy/03-target-domains.md) |
| SEO-исполнитель | — | [Roadmap внедрения](reports/backlink-strategy/05-implementation-roadmap.md), [Карточки конкурентов](reports/backlink-strategy/06-competitor-cards.md) |
| Аудит / QA | [Валидация](validation/) | [Audit report](reports/backlink-strategy/07-audit-report.md) |
| Tech Lead | [Методология](methodology/) | [Методология](reports/backlink-strategy/08-methodology.md), [Pipeline](analysis/backlink-strategy/) |

## Методология

**Phase 1 (органический анализ):** Pipeline из 29 задач, обработавший 51 файл данных Ahrefs по 9 конкурентам с помощью Claude Opus. Каждая задача произвела структурированные YAML-артефакты, которые агрегируются в кросс-анализ и финальные отчёты. Подробнее: [methodology/](methodology/README.md).

**Phase 2 (ссылочный анализ):** Pipeline из 3 этапов: Python/pandas нормализация 39 CSV → JSON-агрегация → 4 параллельных исследования Claude AI (R1-R4) → синтез → автоматическая верификация (662 проверки). Подробнее: [reports/backlink-strategy/08-methodology.md](reports/backlink-strategy/08-methodology.md).

## Как верифицировать данные

**Phase 1 (органический анализ):**
1. Выберите любое числовое утверждение из отчётов (например, "freesoft.ru DR 59")
2. Найдите ссылку на источник (например, "brief 11")
3. Проследите цепочку через [chain-of-evidence.md](validation/chain-of-evidence.md) до исходных данных Ahrefs
4. Сверьте с результатами валидации в [validation-report.md](validation/validation-report.md)

**Phase 2 (ссылочный анализ):**
1. Найдите число в отчёте (например, «89.3% spam у freesoft.net»)
2. Найдите соответствующее поле в JSON-агрегате (`r2_pbn_signals.json` → `domains.freesoft.net.summary.spam_pct`)
3. (Опционально) Запустите `verify_report.py` для автоматической проверки 662 утверждений
4. Подробнее: [07-audit-report.md](reports/backlink-strategy/07-audit-report.md)

## Источники данных

**Phase 1:** 51 файл Ahrefs (36 CSV + 15 PNG) — органический трафик, ключевые слова, Domain Rating. Инвентаризация: [data-sources.md](methodology/data-sources.md).

**Phase 2:** 39 CSV из Ahrefs (ссылочные отчёты), экспорт 2026-03-13, ~660 000 строк, 12 доменов. 4 типа отчётов: referring domains, anchors, backlinks one per domain, link intersect. Подробнее: [08-methodology.md](reports/backlink-strategy/08-methodology.md).

## Верификация

**Phase 1:** ~180 data points, CONDITIONAL PASS. Подробнее: [validation/](validation/README.md).

**Phase 2:** 662 автоматических проверки, 99.4% pass rate (PASS WITH WARNINGS). Подробнее: [audit report](reports/backlink-strategy/07-audit-report.md).

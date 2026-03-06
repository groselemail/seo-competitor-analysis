# SEO Competitor Analysis: Multilingual Expansion for freesoft.net

## Executive Summary (RU)

Проведён комплексный SEO-анализ конкурентов в нише скачивания софта на основе 51 файла данных Ahrefs по 9 конкурентам. Портфель freesoft состоит из трёх доменов с суммарным трафиком ~222 000 визитов/мес., при этом 75,7% трафика сконцентрировано на одном русскоязычном домене freesoft.ru (168 000, DR 59). Анализ показал критическую зависимость от одного языка и рынка: монолингвальные .ru-сайты демонстрируют системное падение (trashbox.ru: −47%, softonic.ru: −578K). Все три ведущих конкурента (softonic.com, uptodown.com, malavida.com) используют мультиязычные поддомены на 9–14 языках (7–8 с измеримым трафиком). Рекомендуется гибридная стратегия: сохранить freesoft.ru для русского рынка, консолидировать остальные языки на поддоменах freesoft.net. Потенциал роста — с ~222K до 500K–880K трафика (2,3–4,0x) за 6–18 месяцев через запуск 5 новых языков (ES, AR, PT, ID, VI). Все ~180 числовых утверждений верифицированы против первичных источников Ahrefs: 0 критических расхождений.

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
├── reports/             — Финальные отчёты для клиента
├── analysis/
│   ├── competitors/     — Аналитика по каждому конкуренту (YAML)
│   ├── cross-analysis/  — Кросс-анализ и синтез
│   └── our-domains/     — Анализ freesoft.net / .ru / .fr
├── validation/          — Fact-checking и цепочка доказательств
├── methodology/         — Архитектура pipeline и отчёты аудита
└── raw-data/            — Описание исходных выгрузок Ahrefs
```

## Быстрая навигация

- **Начните здесь:** [Executive Summary](reports/executive-summary.md)
- **Стратегия:** [Domain Strategy](reports/domain-strategy.md)
- **Roadmap:** [Multilingual Roadmap](reports/multilingual-roadmap.md)
- **Fact-checking:** [Как верифицировать](validation/README.md)
- **Методология:** [Архитектура pipeline](methodology/architecture.md)

## Методология

Анализ выполнен как pipeline из 29 задач, обработавший 51 файл данных Ahrefs по 9 конкурентам с помощью Claude Opus. Каждая задача произвела структурированные YAML-артефакты, которые агрегируются в кросс-анализ и финальные отчёты. Подробнее: [methodology/](methodology/README.md).

## Как верифицировать данные

1. Выберите любое числовое утверждение из отчётов (например, "freesoft.ru DR 59")
2. Найдите ссылку на источник (например, "brief 11")
3. Проследите цепочку через [chain-of-evidence.md](validation/chain-of-evidence.md) до исходных данных Ahrefs
4. Сверьте с результатами валидации в [validation-report.md](validation/validation-report.md)

## Источники данных

Все данные получены из выгрузок Ahrefs (органический трафик, ключевые слова, бэклинки, Domain Rating), собранных в марте 2026. Полная инвентаризация 51 исходного файла и их маппировка на задачи анализа: [data-sources.md](methodology/data-sources.md).

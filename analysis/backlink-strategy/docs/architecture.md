# Архитектура документации: Ссылочная стратегия freesoft.net

> **Версия:** 1.0
> **Дата:** 2026-03-13
> **Назначение:** Спецификация пакета документов по результатам ссылочного анализа

---

## Принцип организации

4 уровня глубины по аудитории:

| Уровень | Аудитория | Вопрос | Документы |
|---------|-----------|--------|-----------|
| 1. Решения | PM, руководство | «Что делать?» | 01-executive-brief |
| 2. Стратегия | SEO-стратег | «Почему и куда?» | 02-full-report, 03-target-domains, 04-disavow-plan |
| 3. Исполнение | SEO-исполнитель | «Как именно?» | 05-implementation-roadmap, 06-competitor-cards |
| 4. Обоснование | Аудит, техн. команда | «Можно ли доверять?» | 07-audit-report, 08-methodology |

---

## Структура файлов

```
reports/backlink-strategy/
├── INDEX.md                         # Точка входа, навигация, быстрый старт по ролям
│
├── 01-executive-brief.md            # Уровень 1: 1-2 стр., ключевые решения
├── 02-full-report.md                # Уровень 2: полный аналитический отчёт
├── 03-target-domains.md             # Уровень 2: приоритизированные цели линкбилдинга
├── 04-disavow-plan.md               # Уровень 2: план disavow по доменам freesoft
├── 05-implementation-roadmap.md     # Уровень 3: пошаговые чек-листы
├── 06-competitor-cards.md           # Уровень 3: карточки 9 конкурентов
├── 07-audit-report.md               # Уровень 4: верификация данных
└── 08-methodology.md                # Уровень 4: методология и ограничения
```

---

## Спецификация документов

### INDEX.md — Навигационный хаб

- Описание пакета (что, когда, на каких данных)
- Быстрый старт по ролям (PM → 01, SEO-стратег → 02+03, исполнитель → 05+06)
- Таблица документов с описаниями и статусами
- Ссылки: относительные пути

### 01-executive-brief.md — Краткая сводка для руководства

- **Объём:** Максимум 60-80 строк (1-2 страницы)
- **Формат:** Без детальных таблиц — только ключевые числа в тексте
- **Структура:**
  1. Контекст (2-3 предложения)
  2. Позиция freesoft (DR vs конкуренты, ref domains, gaps)
  3. 5 ключевых находок (по 1-2 предложения, конкретные числа)
  4. Критическая проблема (spam → disavow)
  5. Top-3 приоритетных действия + ожидаемый результат
  6. Ресурсы и сроки
- **Источник:** синтез из 02-full-report.md

### 02-full-report.md — Полный аналитический отчёт

- **Действие:** ПЕРЕМЕСТИТЬ из `reports/backlink-strategy.md`
- Без изменений содержания

### 03-target-domains.md — Целевые домены для линкбилдинга

- **Структура:**
  - EN-targets: таблица (домен, DR, traffic, intersect, тип контента, подход, приоритет)
  - RU-targets: аналогично
  - FR-targets: аналогично + пометка про миграцию frees0ft.fr
  - Multi-competitor domains (3+ конкурентов) — выделены
  - Для каждого: рекомендованный формат outreach
- **Формат:** Чистые таблицы, готовые к копированию в таск-трекер
- **Источник:** `r3_intersections.json` + `r3_domain_intersections.md`

### 04-disavow-plan.md — План очистки ссылочного профиля

- **Структура:**
  - **freesoft.net:** ~3 000 доменов, паттерны, приоритет
  - **freesoft.ru:** ~500-600 доменов, паттерны
  - **frees0ft.fr:** оценка необходимости при миграции
  - Формат disavow-файла для Google Search Console
  - Порядок действий
  - Мониторинг эффекта
- **Источник:** `r2_pbn_signals.json` + `r2_pbn_detection.md`

### 05-implementation-roadmap.md — Пошаговый план внедрения

- **Структура:**
  - Неделя 1-2: Quick wins (конкретные домены из 03)
  - Месяц 1: Disavow (по плану из 04) + первый outreach
  - Месяц 2-3: Языковой линкбилдинг (EN/RU/FR)
  - Месяц 3-6: Стратегические targets DR 60+
  - Месяц 6-12: Брендовые анкоры, рост DR
- **Формат:** Markdown `[ ]` checkboxes, конкретные домены, критерии завершения
- **Источник:** 02-full-report.md (roadmap) + 03 + 04

### 06-competitor-cards.md — Карточки конкурентов

- 9 карточек: softonic.com, uptodown.com, malavida.com, softonic.ru, trashbox.ru, filehippo.com, clubic.com, 01net.com, commentcamarche.net
- Каждая карточка (~25-30 строк):
  - Метрики: DR, ref domains, dofollow%, spam%, growth 12m
  - Языковая стратегия (из R1)
  - PBN-риск (из R2)
  - Пересечение с freesoft (Jaccard, из R3)
  - Что копировать / чего избегать
- Сводная таблица сравнения в конце
- **Источник:** секции R1-R4

### 07-audit-report.md — Верификация данных

- **Действие:** ПЕРЕМЕСТИТЬ из `reports/AUDIT_REPORT.md`
- Без изменений содержания

### 08-methodology.md — Методология и ограничения

- **Структура:**
  1. Источник данных (Ahrefs, дата, 39 CSV, 12 доменов)
  2. Датасет (total rows, gambling-фильтр)
  3. Пайплайн обработки (нормализация → агрегация → анализ)
  4. 4 исследования (R1-R4: краткое описание каждого)
  5. Ограничения данных (Ahrefs 30K лимит, PBN-детекция, gambling-фильтр, exclusive domains, дата актуальности)
  6. Верификация (662 проверки, 99.4% — ссылка на 07)
  7. Воспроизводимость (3 сессии, промпты, команды запуска)
  8. Карта файлов pipeline
- **Источник:** `PIPELINE_ARCHITECTURE.md` + `inventory.json` + промпты сессий

---

## Разбивка по сессиям

### Сессия 4 — Документация, часть 1

**Создаёт:** INDEX.md, 01, 02 (move), 06, 07 (move), 08

**Читает:**
- `reports/backlink-strategy.md`
- `reports/AUDIT_REPORT.md`
- `analysis/backlink-strategy/PIPELINE_ARCHITECTURE.md`
- `analysis/backlink-strategy/pipeline/intermediate/inventory.json`
- `analysis/backlink-strategy/pipeline/sections/r1_language_strategy.md`
- `analysis/backlink-strategy/pipeline/sections/r2_pbn_detection.md`
- `analysis/backlink-strategy/pipeline/sections/r3_domain_intersections.md`
- `analysis/backlink-strategy/pipeline/sections/r4_link_profile_analysis.md`

### Сессия 5 — Документация, часть 2

**Создаёт:** 03, 04, 05. Обновляет INDEX.md.

**Читает:**
- `analysis/backlink-strategy/DOCS_ARCHITECTURE.md`
- `reports/backlink-strategy/02-full-report.md`
- `analysis/backlink-strategy/pipeline/intermediate/r2_pbn_signals.json` (через Python-скрипт)
- `analysis/backlink-strategy/pipeline/intermediate/r3_intersections.json` (через Python-скрипт)
- `analysis/backlink-strategy/pipeline/sections/r2_pbn_detection.md`
- `analysis/backlink-strategy/pipeline/sections/r3_domain_intersections.md`

---

## Правила

1. **Без имён.** Нигде в документах не упоминаются имена людей. Только роли.
2. **Числа из данных.** Каждое число — из JSON-агрегатов или проверенного отчёта. Не выдумывать.
3. **Gambling-фильтр.** Не рекомендовать gambling/adult домены.
4. **Миграция frees0ft.fr.** Учитывать во всех FR-рекомендациях.
5. **Формат:** Чистый markdown, читаемый без специальных инструментов.
6. **Кросс-ссылки.** Документы ссылаются друг на друга где релевантно.
7. **Компактность.** Executive brief ≤ 2 стр. Карточка конкурента ≤ 30 строк.

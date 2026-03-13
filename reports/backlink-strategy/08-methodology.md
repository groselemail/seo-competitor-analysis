# Методология и ограничения

## 1. Источник данных

Все данные экспортированы из Ahrefs 2026-03-13. Формат: CSV (UTF-16LE TSV, некоторые файлы link_intersect — UTF-8). Всего 39 файлов в 4 категориях.

## 2. Датасет

| Показатель | Значение |
|-----------|----------|
| Всего CSV-файлов | 39 |
| Типы отчётов | 4 (A: referring_domains, B: anchors, C: backlinks_one_per_domain, D: link_intersect) |
| Доменов | 12 (3 наших + 9 конкурентов) |
| Строк до фильтрации | 669 569 |
| Gambling/adult отфильтровано | 9 900 |
| Строк после фильтрации | 659 669 |

Файлы, упёршиеся в лимит Ahrefs 30K строк (14 шт.):

| Файл | Домен |
|------|-------|
| referring_domains | softonic.com, uptodown.com |
| anchors | softonic.com, uptodown.com, malavida.com, softonic.ru, filehippo.com, clubic.com, 01net.com, commentcamarche.net |
| backlinks_one_per_domain | softonic.com, uptodown.com |
| link_intersect | D1_EN, D3_FR |

## 3. Пайплайн обработки

Обработка выполнена в 3 этапа:

**Этап 1 — Нормализация:** Конвертация 39 CSV-файлов из UTF-16LE в UTF-8 TSV. Стандартизация колонок через маппинг (COLUMN_MAP_A/B/C/D). Применение gambling/adult фильтра (strict + loose regex) с логированием отфильтрованных строк. Инструменты: Python 3 + pandas.

**Этап 2 — Агрегация:** Создание 4 JSON-агрегатов (R1–R4) из нормализованных TSV-файлов. Каждый агрегат содержит сводные метрики для всех 12 доменов. Суммарный размер агрегатов ~61K токенов. Инструменты: Python 3 + pandas + numpy.

**Этап 3 — Анализ:** 4 параллельных исследования (R1–R4), каждое в собственном контексте Claude AI. Каждое исследование получает JSON-агрегат и пишет markdown-секцию. Финальный синтез объединяет 4 секции в единый отчёт с кросс-анализом. Инструменты: Claude Code CLI.

## 4. Исследования

| ID | Название | Вопрос | Источники данных |
|----|---------|--------|-----------------|
| R1 | Языковые стратегии | Как конкуренты строят мультиязычный линкбилдинг? | A + C |
| R2 | PBN-детекция | Кто использует PBN/сателлиты? | A + C |
| R3 | Пересечения доменов | Где общие источники ссылок? | A + D |
| R4 | Ссылочные профили | Каков бенчмарк ниши? | A + B + C |

## 5. Ограничения данных

- **Ahrefs 30K лимит:** 14 файлов усечены (полный список — см. таблицу в секции 2). Для softonic.com и uptodown.com реальное количество referring domains значительно выше 30K. Все количественные выводы по ним помечены как «в рамках доступных данных».

- **PBN-детекция:** Выявляет только очевидные паттерны — шаблонные домены (seo-anomaly-\*, bhs-links-\*), массовый .xyz-спам, аномальные temporal spikes, Ahrefs spam-флаг. Профессиональные PBN (DR 30+, уникальный контент, разнесённые по IP) не детектируются. Для полной детекции необходимы: IP/AS-кластеризация, WHOIS-анализ, контент-анализ.

- **Gambling/adult фильтр:** Применены два паттерна — strict (с word boundaries) и loose. 9 900 строк отфильтровано. Возможны false negatives (неочевидный gambling-контент).

- **Exclusive domains (R2, Детектор 3):** Ограничение датасета из 12 доменов. Домен, «эксклюзивно» ссылающийся на 1 из 12, может ссылаться на тысячи других сайтов за пределами выборки. Высокое число exclusive domains ≠ доказательство PBN.

- **Anchor type classification:** Анкоры «01net» и «Comment ca marche» классифицированы как «other», а не branded. Реальная доля branded-анкоров у конкурентов может быть на 3–10% выше.

- **Данные актуальны на дату экспорта** (2026-03-13). Ссылочные профили меняются ежедневно.

## 6. Верификация

Проведено **662 автоматических проверки** числовых утверждений отчёта против исходных JSON-агрегатов. Результат: **99.4% pass rate** (658 пройдено, 1 минорная ошибка, 3 предупреждения).

Единственная обнаруженная ошибка: медиана DR-бакета 81–90 — 1.1% в отчёте вместо корректного 1.2%. Влияние минимально, бакет не упоминается в выводах.

3 предупреждения: расхождения в композитных PBN-scores (дельта 0.4–0.5 балла) из-за различий в нормализации temporal_spikes_count. Ранжирование доменов не меняется.

Выдуманных данных, фабрикованных доменов или систематических ошибок **не обнаружено**. Все 34 проверенных target-домена найдены в JSON с корректными DR и intersect.

Подробный отчёт аудита: [07-audit-report.md](07-audit-report.md)

## 7. Воспроизводимость

Анализ выполнен в 3 сессиях Claude Code CLI:

| Сессия | Задача | Время |
|--------|--------|-------|
| Сессия 1 | Нормализация + 4 параллельных исследования (R1–R4) | ~44 мин |
| Сессия 2 | Синтез финального отчёта | ~18 мин |
| Сессия 3 | Аудит и верификация | ~20 мин |

Промпты сессий сохранены:
- `analysis/backlink-strategy/PROMPT_SESSION_1.md`
- `analysis/backlink-strategy/PROMPT_SESSION_2.md`
- `analysis/backlink-strategy/PROMPT_SESSION_3_AUDIT.md`

Команда запуска:
```bash
claude --dangerously-skip-permissions --max-turns 300 "$(sed -n '/^## ПРОМПТ$/,$ p' <prompt_file>)"
```

## 8. Карта файлов

| Файл | Назначение |
|------|-----------|
| pipeline/intermediate/inventory.json | Инвентаризация датасета |
| pipeline/intermediate/r1_language_links.json | Агрегат R1 |
| pipeline/intermediate/r2_pbn_signals.json | Агрегат R2 |
| pipeline/intermediate/r3_intersections.json | Агрегат R3 |
| pipeline/intermediate/r4_link_profiles.json | Агрегат R4 |
| pipeline/intermediate/validation_report.json | Валидация 39 файлов |
| pipeline/intermediate/gambling_filter_log.json | Лог gambling-фильтра |
| pipeline/intermediate/verification_results.json | Результат автоматической верификации |
| pipeline/sections/r1_language_strategy.md | Секция R1 |
| pipeline/sections/r2_pbn_detection.md | Секция R2 |
| pipeline/sections/r3_domain_intersections.md | Секция R3 |
| pipeline/sections/r4_link_profile_analysis.md | Секция R4 |
| pipeline/scripts/verify_report.py | Скрипт верификации |

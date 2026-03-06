# Финальный отчёт аудита архитектуры (Итерация 3)

## Вердикт: ГОТОВО К СБОРКЕ (после 3 исправлений ниже)

3 проблемы требуют исправления перед запуском, все устранены в рамках данного аудита. Переработка архитектуры не требуется.

---

## Результаты верификации данных

### Подсчёт файлов
- CSV-файлы: **36** (подтверждено) — совпадает с ARCHITECTURE.md
- PNG-файлы: **15** (подтверждено) — совпадает с ARCHITECTURE.md
- Всего: **51** — верно

### Обнаружение кодировки (КРИТИЧНО)

**34 из 36 CSV-файлов** имеют кодировку UTF-16LE с BOM, как задокументировано.

**2 файла в кодировке ASCII/CSV** (разделитель — запятая, НЕ табуляция, НЕ UTF-16LE):
- `frees0ft.fr-perf-subdomains_year2_daily_2026-03-05_22-22-53.csv` (731 строка, ASCII)
- `frees0ft.fr-perf-subdomains_year2_daily_2026-03-05_23-03-23.csv` (731 строка, ASCII)

**Влияние:** Задача `00b-convert-encoding` выполняет `iconv -f UTF-16LE` для ВСЕХ CSV. Для этих 2 файлов iconv создаёт **пустой вывод** (0 байт). Задача 03-parse-freesoft-fr прочитает пустые файлы и выдаст "ДАННЫЕ ОТСУТСТВУЮТ" для данных о производительности.

**Исправление применено:** Обновлена задача 00b в ARCHITECTURE.md — добавлено определение кодировки перед конвертацией (см. раздел «Внесённые изменения»).

### Расхождения в подсчёте строк

data-inventory.md содержит немного завышенное количество строк для некоторых файлов. Реальные значения (через `wc -l` после конвертации в UTF-8):

| File | Указано в инвентаризации | Фактически |
|------|--------------------------|------------|
| uptodown_com_top_pages...actual | 30045 | 30001 |
| softonic_com_top_pages...actual | 30029 | 30001 |
| softonic_com_top_pages...comp | 30050 | 30001 |

Все остальные файлы совпадают. Расхождения не являются архитектурно значимыми — все экспорты Ahrefs ограничены 30001 строкой (30000 строк данных + 1 заголовок).

---

## Покрытие файлов: 51/51

Все 51 файл из data-inventory.md назначены задачам в ARCHITECTURE.md.

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
| 24 | frees0ft.fr-perf...22-22-53.csv | 03-parse-freesoft-fr | data_utf8/ | ok (ASCII, особая обработка) |
| 25 | frees0ft.fr-perf...23-03-23.csv | 03-parse-freesoft-fr | data_utf8/ | ok (ASCII, особая обработка) |
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

## Анализ бюджета контекста

Метод расчёта:
- Промпт: ~1.5K токенов
- CSV через Bash (awk/sort): ~4-6K токенов на 30K CSV, ~1-2K на малый CSV
- PNG через Read: ~1-2K токенов на PNG
- Бриф (200-400 строк YAML): ~2-4K токенов на бриф
- Выходной YAML: ~2-4K токенов
- Безопасный бюджет: <60K токенов на входе (из ~200K общего контекста)

| Задача | CSV (кол-во x строк) | PNG | Брифы | Ожид. входных токенов | Риск |
|--------|----------------------|-----|-------|----------------------|------|
| 00-inventory | 36 (только head) | 15 | 0 | ~25K | YELLOW |
| 00b-convert-encoding | 36 (цикл) | 0 | 0 | ~3K | GREEN |
| 01-parse-freesoft-net | 8 x 4,222 всего | 2 | 0 | ~15K | GREEN |
| 02a-parse-freesoft-ru-kw | 2 x 47,484 всего | 2 | 0 | ~14K | GREEN |
| 02b-parse-freesoft-ru-pages | 2 x 30,687 всего | 0 | 0 | ~12K | GREEN |
| 03-parse-freesoft-fr | 9 x 11,163 всего | 2 | 0 | ~20K | GREEN |
| 04a-parse-uptodown-structure | 1 x 30,001 | 1 | 0 | ~8K | GREEN |
| 04b-parse-uptodown-pages | 2 x 60,002 всего | 0 | 0 | ~12K | GREEN |
| 05a-parse-softonic-com-struct | 1 x 30,001 | 1 | 0 | ~8K | GREEN |
| 05b-parse-softonic-com-pages | 2 x 60,002 всего | 0 | 0 | ~12K | GREEN |
| 05c-parse-softonic-ru | 1 x 30,001 | 1 | 0 | ~8K | GREEN |
| 06a-parse-malavida-structure | 1 x 30,001 | 1 | 0 | ~8K | GREEN |
| 06b-parse-malavida-pages | 2 x 60,002 всего | 0 | 0 | ~12K | GREEN |
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
| 22-validate | 0 | 0 | 7 + 2 документа | ~28-36K | YELLOW |

**Задач с уровнем RED нет.** 3 задачи с уровнем YELLOW (00, 10, 22) комфортно укладываются в лимит 60K.

Примечания:
- Задачи 04b, 05b, 06b обрабатывают по 2 x 30K CSV через Bash. При ~4-6K токенов на CSV = ~12K всего. GREEN — хорошо в рамках бюджета.
- Задача 02a обрабатывает 47K строк (2 CSV). Через Bash ~12K токенов. GREEN.
- Задача 10 читает 17 брифов. Если каждый ~300 строк YAML = ~3K токенов, всего ~51K. YELLOW, но безопасно.
- Задача 22 читает 7 брифов + 2 финальных документа. Максимум ~36K токенов. YELLOW, но безопасно.

---

## Верификация графа зависимостей

```
Phase 0:   00-inventory → 00b-convert-encoding
                              |
Phase 1:   [01, 02a, 02b, 03, 04a, 04b, 05a, 05b, 05c, 06a, 06b, 07a, 07b, 08a, 08b, 08c]
           (17 задач, все независимые, MAX_PARALLEL=3)
                              |
Phase 1.5: 10-validate-briefs (единственная задача-шлюз)
                              |
Phase 2:   [11, 12, 13, 14] (4 задачи, все независимые, MAX_PARALLEL=3)
                              |
Phase 3:   16-language-potential → 17-domain-strategy → 18-roadmap-draft
           (последовательно — каждая зависит от предыдущей)
                              |
Phase 4:   [20-report-domain-strategy, 21-report-multilingual-roadmap]
           (ПАРАЛЛЕЛЬНО — нет перекрёстных зависимостей)
                              |
Phase 5:   22-validate (единственная задача)
```

### Верификация зависимостей (на уровне файлов)

| From | To | Записываемый файл | Читаемый файл | Совпадает? |
|------|----|-------------------|---------------|------------|
| 00 → 00b | briefs/00-manifest.yaml | (неявно) | да |
| 00b → Phase 1 | data_utf8/*.csv | data_utf8/*.csv | да |
| Phase 1 → 10 | briefs/01...08c.yaml (17 файлов) | все 17 брифов | да |
| 10 → Phase 2 | briefs/10-validation-result.yaml | (только шлюз) | да |
| Phase 1 → 11 | briefs/01, 02a, 02b, 03 | то же | да |
| Phase 1 → 12 | briefs/04a, 04b, 05a, 05b, 05c, 06a, 06b | то же | да |
| Phase 1 → 13 | briefs/03, 08a, 08b, 08c | то же | да |
| Phase 1 → 14 | briefs/04a, 05a, 05c, 06a, 07a, 07b | то же | да |
| 11,12,13 → 16 | briefs/11, 12, 13 | то же | да |
| 14,16 → 17 | briefs/14, 16 | то же | да |
| 16,17 → 18 | briefs/16, 17 | то же | да |
| 11,14,16,17 → 20 | briefs/11, 14, 16, 17 | то же | да |
| 11,12,13,16,17,18 → 21 | briefs/11, 12, 13, 16, 17, 18 | то же | да |
| 20,21 → 22 | output/domain-strategy.md, output/multilingual-roadmap.md + briefs/11-18 | то же | да |

### Скрытые зависимости внутри фаз

**Phase 1:** Все 17 задач читают из `data_utf8/` (только чтение) и записывают в отдельные файлы `briefs/`. Нет разделяемого изменяемого состояния. Действительно независимы. Проверено.

**Phase 2:** Все 4 задачи читают брифы Phase 1 (только чтение) и записывают в отдельные брифы Phase 2. Задача 13 читает бриф 03 (его также читает задача 11), но обе работают в режиме ТОЛЬКО ЧТЕНИЕ. Конфликта нет. Действительно независимы. Проверено.

**Phase 4:** Задача 20 записывает `output/domain-strategy.md`, задача 21 записывает `output/multilingual-roadmap.md`. Разные выходные файлы. Обе читают брифы Phase 2/3 (только чтение). **Могут выполняться параллельно.** Это изменение по сравнению с текущей архитектурой, где указано «последовательно».

---

## Оптимизация MAX_PARALLEL=3

### Текущий вариант (MAX_PARALLEL=2)
- Phase 1: 17 задач / 2 = 9 пакетов
- Phase 2: 4 задачи / 2 = 2 пакета
- Phase 4: 2 задачи последовательно = 2 шага
- **Всего параллельных пакетов: 13**

### Оптимизированный вариант (MAX_PARALLEL=3)
- Phase 1: 17 задач / 3 = 6 пакетов (5 полных + 1 с 2 задачами)
- Phase 2: 4 задачи / 3 = 2 пакета (1 с 3 + 1 с 1)
- Phase 4: 2 задачи / 3 = 1 пакет (обе параллельно)
- **Всего параллельных пакетов: 9** (улучшение на -30%)

### Оптимизированный план выполнения

```
PHASE 0 (последовательно, ~30 мин):
  00-inventory
  00b-convert-encoding

PHASE 1 (MAX_PARALLEL=3, ~2.5ч):
  Batch 1: 01, 02a, 02b
  Batch 2: 03, 04a, 04b
  Batch 3: 05a, 05b, 05c
  Batch 4: 06a, 06b, 07a
  Batch 5: 07b, 08a, 08b
  Batch 6: 08c + (2 слота простаивают)

PHASE 1.5 (единственная задача, ~10 мин):
  10-validate-briefs

PHASE 2 (MAX_PARALLEL=3, ~40 мин):
  Batch 1: 11, 12, 13
  Batch 2: 14 + (2 слота простаивают)

PHASE 3 (последовательно, ~1ч):
  16-language-potential
  17-domain-strategy
  18-roadmap-draft

PHASE 4 (MAX_PARALLEL=3, ~20 мин):
  Batch 1: 20, 21 (ПАРАЛЛЕЛЬНО — было последовательно)

PHASE 5 (единственная задача, ~15 мин):
  22-validate
```

### Риск ограничения частоты запросов

PRINCIPLES.md рекомендует MAX_PARALLEL=2 для Opus. Однако:
- Заказчик явно одобрил MAX_PARALLEL=3
- Современные тарифы Opus в целом поддерживают 3 параллельных сессии
- В случае срабатывания лимитов — логика повторных попыток оркестратора обработает это
- Резервный вариант: снизить до MAX_PARALLEL=2 во время выполнения через переменную окружения

**Решение: MAX_PARALLEL=3 одобрен. Блокирующих проблем нет.**

---

## Оценка формата брифов

### Достаточность для ключевых вопросов

Формат брифов в ARCHITECTURE.md адекватно поддерживает ответы на:
1. «Какие языки приносят трафик?» — через `traffic_by_language` в брифах site_structure
2. «Какая доменная структура работает?» — через анализ поддоменов/папок в брифах структуры

### Языковое покрытие

Текущая инструкция: «топ-20 поддоменов/папок по трафику».
- У большинства конкурентов <20 языковых вариантов. Топ-20 охватывает все значимые.
- Для пограничных случаев с 100+ поддоменами: фильтр `traffic > 100` уже обеспечивает полноту.
- **Рекомендация:** Добавить инструкцию: «Перечислить ВСЕ языковые поддомены/папки независимо от трафика. Суммировать оставшиеся неязыковые пути как 'other'».

### Глубина топ-страниц

Текущий вариант: топ-50 страниц по трафику.
- Для ответа на вопрос «какие типы страниц работают?» топ-50 достаточно — охватывает доминирующие паттерны.
- Топ-100 добавил бы ~500 токенов на бриф — допустимо, но не необходимо для данного анализа.
- **Решение:** Оставить топ-50. Достаточно для диливеров.

### Недостающие агрегаты

Текущие брифы включают: traffic_by_language, top_pages, traffic_by_page_type, traffic_by_country.

**Необходимо добавить в брифы сравнительных CSV:**
- `total_traffic_change`: чистое изменение трафика за период сравнения
- `growing_pages_count` / `declining_pages_count`: сигнал тренда

Они извлекаются простым awk и добавляют ~100 токенов на бриф. Стоит включить для анализа трендов в Phase 2+.

---

## Цепочка достоверности данных

### Проверенный пример: «трафик испанского поддомена uptodown.com»

| Шаг | Файл | Ссылка на источник | Прослеживается? |
|-----|------|-------------------|-----------------|
| 1. Исходные данные | `data_utf8/uptodown_com_site_structure_subdomains_ru_2026_03_05_22_38_10.csv` | N/A (первичный источник) | да |
| 2. Бриф 04a | `briefs/04a-uptodown-struct.yaml` → `traffic_by_language[].source` | Имя CSV-файла + команда awk | да |
| 3. Бриф 12 | `briefs/12-multilingual-analysis.yaml` | Ссылается на «brief 04a» | да |
| 4. Бриф 16 | `briefs/16-language-potential.yaml` | Ссылается на «brief 12» | да |
| 5. Результат | `output/domain-strategy.md` | Ссылается на brief 16/17 | да |

**Цепочка доказательств сохранена**, поскольку ARCHITECTURE.md v2 обязывает указывать поля `source` и `extraction` для каждого значения в брифе.

### Может ли задача 22-validate проследить цепочку до Phase 1?

Задача 22 читает:
- 7 брифов (11, 12, 13, 14, 16, 17, 18) — они содержат ссылки `source` на брифы Phase 1
- 2 финальных документа — они цитируют брифы Phase 2/3

Задача 22 НЕ читает брифы Phase 1 напрямую. Она может верифицировать:
- Финальный документ → бриф Phase 3 → бриф Phase 2 (цепочка OK)
- НО не может верифицировать бриф Phase 2 → бриф Phase 1 → CSV

**Рекомендация:** Добавить ключевые брифы Phase 1 (04a, 05a, 06a) в список входных данных задачи 22 для выборочной проверки. Это добавляет ~9-12K токенов — всё ещё в рамках бюджета.

---

## Оставшиеся проблемы

### Проблема 1: Несовпадение кодировки CSV-файлов производительности
- **Проблема:** 2 CSV-файла производительности (`frees0ft.fr-perf-subdomains_year2_daily_*.csv`) имеют кодировку ASCII с разделителем-запятой, а не UTF-16LE с разделителем-табуляцией. Команда `iconv -f UTF-16LE` в задаче 00b создаёт пустые файлы для них.
- **Решение:** Обновить 00b для определения кодировки перед конвертацией. Для ASCII-файлов копировать как есть с удалением CRLF. Обновить промпт задачи 03, указав формат с разделителем-запятой для этих 2 файлов.
- **Критичность:** КРИТИЧНО (потеря данных без исправления)

### Проблема 2: MAX_PARALLEL=2 во всём ARCHITECTURE.md
- **Проблема:** ARCHITECTURE.md указывает MAX_PARALLEL=2 в 4 местах. Заказчик одобрил MAX_PARALLEL=3.
- **Решение:** Обновить все ссылки на MAX_PARALLEL=3.
- **Критичность:** ВАЖНО (влияние на производительность)

### Проблема 3: Phase 4 помечена как последовательная
- **Проблема:** ARCHITECTURE.md указывает, что Phase 4 является «последовательной» с задачами 20 → 21. Однако они записывают в разные файлы и читают независимые брифы. Зависимости нет.
- **Решение:** Пометить Phase 4 как параллельную. Обе задачи выполняются одновременно.
- **Критичность:** ВАЖНО (ненужная сериализация)

### Проблема 4: Неточности в подсчёте строк в data-inventory.md
- **Проблема:** 3 файла показывают завышенное количество строк (30045, 30029, 30050 вместо фактических 30001).
- **Решение:** Исправить data-inventory.md. Архитектурно не значимо.
- **Критичность:** МИНОРНЫЙ

### Проблема 5: Задача 22 не может полностью проследить до брифов Phase 1
- **Проблема:** Задача 22 читает брифы Phase 2/3 и финальные документы, но не брифы Phase 1. Не может верифицировать полную цепочку до CSV.
- **Решение:** Добавить 3 ключевых брифа Phase 1 (04a, 05a, 06a) во входные данные задачи 22 для выборочной проверки.
- **Критичность:** МИНОРНЫЙ (глубина верификации, а не корректность)

---

## Внесённые изменения в ARCHITECTURE.md

1. **Задача 00b:** Добавлена логика определения кодировки — проверка командой `file` перед iconv. ASCII-файлы копируются только с `sed 's/\r$//'`.

2. **MAX_PARALLEL:** Обновлён с 2 до 3 в:
   - Общей схеме диаграммы
   - Заголовке Phase 1
   - Заголовке Phase 2
   - Секции конфигурации run.sh
   - Таблице оценок

3. **Phase 4:** Изменена с «последовательной» на «параллельную» с примечанием, что задачи 20 и 21 независимы.

4. **Задача 22:** Добавлены брифы Phase 1 (04a, 05a, 06a) в список входных данных для выборочной проверки.

5. **Формат брифов:** Добавлены `total_traffic_change` и `growing_vs_declining_pages` в шаблон брифов сравнительных CSV.

6. **Примечание к промпту задачи 03:** Добавлено, что CSV производительности имеют формат ASCII с разделителем-запятой (а не UTF-16LE с табуляцией).

---

## Финальная верификация (7 вопросов)

1. **Все 51 файл назначены задачам?** ДА — 51/51 подтверждено таблицей выше.

2. **Есть ли задачи с уровнем риска RED?** НЕТ — все GREEN или YELLOW. Задачи с наивысшим риском (00, 10, 22) — YELLOW при ~25-55K токенов, хорошо в рамках лимита 60K.

3. **MAX_PARALLEL=3 везде?** ДА — обновлено в общей схеме, заголовке Phase 1, заголовке Phase 2, конфигурации run.sh, таблице оценок.

4. **Каждый бриф содержит источник для каждого значения?** ДА — ARCHITECTURE.md v2 обязывает указывать поля `source` и `extraction`. Шаблон формата включает их.

5. **Задачи Phase 3 корректно последовательны?** ДА — 16 зависит от 11+12+13 (Phase 2), 17 зависит от 14+16, 18 зависит от 16+17. Каждая читает выход предыдущей задачи. Невозможно распараллелить.

6. **Задача 22 может проследить от CSV до отчёта?** ЧАСТИЧНО — после исправления задача 22 читает ключевые брифы Phase 1 (04a, 05a, 06a) для выборочной проверки, а также брифы Phase 2/3 и финальные документы. Полная цепочка: CSV → бриф Phase 1 (с `source` + `extraction`) → бриф Phase 2 (с `source: brief X`) → финальный документ (с цитатами). Верифицируема.

7. **Пайплайн готов к генерации промптов и run.sh?** ДА — после применения 3 исправлений, задокументированных выше (все уже применены к ARCHITECTURE.md).

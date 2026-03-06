# Pipeline Architecture: SEO Competitor Analysis for Multilingual Expansion

> **Задача:** Анализ конкурентов для ответа на вопрос "даст ли языковое расширение рост трафика и на сколько?"
> **Deliverables:** (1) Рекомендация по доменной стратегии + план миграции, (2) Мультиязычный roadmap
> **Дата создания:** 2026-03-05
> **Ревизия:** 2026-03-05 (post-review)

---

## Общая схема

```
Phase 0: Inventory + Encoding (2 singletons, sequential)
        |
Phase 1: Parse & Extract (parallel, 17 tasks, MAX_PARALLEL=3)
        |
Phase 1.5: Validate Briefs (singleton)
        |
Phase 2: Deep Analysis (parallel, 4 tasks, MAX_PARALLEL=3)
        |
Phase 3: Cross-Analysis (sequential, 3 tasks)
        |
Phase 4: Deliverables (parallel, 2 tasks — independent outputs)
        |
Phase 5: Validation (singleton)
```

**Паттерн:** Level 2 — Phased Pipeline (Fan-Out / Fan-In) из playbooks/pipeline/ARCHITECTURE.md

**Ключевые проблемы и решения:**

1. **CSV до 30K строк не влезают в контекст.** Решение: Phase 1 использует Bash (awk/sort/head) для извлечения метрик в компактные YAML briefs. Phase 2+ работает только с briefs.

2. **CSV в кодировке UTF-16LE с BOM.** Решение: Phase 0 (task 00b) конвертирует все CSV в UTF-8 перед обработкой. Без этого `awk`/`sort`/`head` дают мусор.

3. **Задачи с >60K строк ненадежны.** Решение: тяжелые задачи разбиты на атомарные (1 CSV 30K = 1 task).

---

## КРИТИЧНО: Кодировка CSV

Все CSV файлы в `data_for_task/` имеют кодировку **UTF-16LE с BOM**.

Стандартные Unix-инструменты (`awk`, `sort`, `head`, `wc -l`) **не работают** с UTF-16.

Обязательная конвертация перед любой обработкой:
```bash
iconv -f UTF-16LE -t UTF-8 < input.csv | sed 's/\r$//' > output_utf8.csv
```

Task `00b-convert-encoding` создает `data_utf8/` с конвертированными файлами. Все последующие tasks читают **только** из `data_utf8/`.

---

## Входные данные

51 файл в `data_for_task/` (36 CSV + 15 PNG).

Полная инвентаризация: [data-inventory.md](../analysis/data-inventory.md)

### Наши домены

| Домен | Overview PNG | Keywords CSV | Top Pages CSV | Traffic Location PNG | Competitors CSV | Performance CSV |
|-------|-------------|-------------|--------------|---------------------|----------------|----------------|
| freesoft.net | `freesoft_net_main_overiew.png` (DR 51, RU filter) | 3 файла: US comp (149), RU comp (2617), RU actual (139) | 3 файла: US comp (17), RU comp (1170), RU actual (88) | `organic_traff_loc_US.png` | 2 файла: RU (21), US (21) | — |
| freesoft.ru | `freesoft_RU_main_overiew.png` (DR 59) | 2 файла: RU actual (17483), RU comp (30001) | 2 файла: RU actual (8439), RU comp (22248) | `organic_traff_loc_RU.png` | — | — |
| frees0ft.fr | `freesoft_FR_main_overiew.png` (DR 23, RU filter!) | 2 файла: FR actual (733), FR comp (3967) | 5 файлов: FR actual x2 (488), FR comp x2 (1931), RU comp (164) | `organic_traff_loc_FR.png` | — | 2 файла: RU daily (731), FR daily (731) |

**Примечание:** freesoft_net overview PNG показывает фильтр "Russian Federation" — трафик всего 89. Реальный US трафик (India 14.2K, US 2.1K) виден только в `organic_traff_loc_US.png`.

**Примечание:** frees0ft.fr имеет 2 пары дубликатов CSV (разные timestamps: 23:03 vs 23:11). Task 00-inventory должен сверить и пометить.

### Конкуренты

| Конкурент | Overview PNG | Site Structure CSV | Top Pages CSV |
|-----------|-------------|-------------------|--------------|
| uptodown.com | `uptodown_com_US_overview.png` (DR 83, ~983K traffic) | 1: subdomains RU (30001) | 2: all actual (30045), RU comp (30001) |
| softonic.com | `softonic_com_US_overview.png` (DR 86, ~88.5K traffic) | 1: subdomains RU (30001) | 2: all actual (30029), all comp (30050) |
| softonic.ru | `softonic_ru_RU_overview.png` (DR 50, ~335K traffic) | 1: subdomains RU (30001) | — |
| malavida.com | `malavida_com_US_overview.png` (DR ~87, ~526K traffic) | 1: subdomains RU (30001) | 2: all actual (30001), all comp (30001) |
| filehippo.com | `filehippo_com_US_overview.png` (DR 77, ~526 traffic) | 1: subdomains RU (30001) | — |
| trashbox.ru | `trashbox_ru_US_overview.png` (DR 54, ~991K traffic) | 1: subdomains RU (30001) | — |
| clubic.com | `clubic_com_US_overview.png` (DR ~91, small traffic) | — | 1: all actual (26609) |
| 01net.com | `01net_com_US_overview.png` (DR 81, ~1.5M traffic) | — | 1: all actual (28699) |
| commentcamarche.net | `ommentcamarche_net_overview.png` (DR 80, ~227K traffic) | — | 1: all actual (30001) |

**Примечание:** PNG commentcamarche имеет опечатку в имени файла (пропущена 'c' в начале).

---

## Phase 0: Inventory + Encoding (2 singletons, sequential)

### Task `00-inventory`

**Цель:** Каталогизация всех файлов, проверка структуры, обнаружение дубликатов, создание манифеста.
**max-turns:** 100

Действия:
1. Для каждого CSV: `head -3` через iconv (для UTF-16) + `wc -c` (размер файла) + определить кодировку
2. Для каждого PNG (Read — Claude видит картинки) — извлечь ключевые цифры (DR, traffic, keywords)
3. Сравнить дубликаты frees0ft.fr (diff первые 10 строк)
4. Записать манифест в `pipeline-seo/briefs/00-manifest.yaml`

Формат манифеста:
```yaml
encoding: "UTF-16LE"  # обнаруженная кодировка CSV
files:
  - name: "uptodown_com_site_structure_subdomains_ru_2026_03_05_22_38_10.csv"
    type: csv
    rows: 30001
    columns: [Path, Ref. pages, Ref. domains, Organic traffic, ...]
    domain: uptodown.com
    report_type: site_structure
    filter_country: RU
    assigned_task: "04a-parse-uptodown-structure"
    is_duplicate_of: null
  # ... все 51 файл

our_domains:
  - domain: freesoft.net
    dr: 51
    organic_traffic: 89  # NOTE: RU filter, real total ~34.6K (from organic_traff_loc_US.png)
    organic_keywords: 138
    source: "freesoft_net_main_overiew.png"
  - domain: freesoft.ru
    dr: 59
    organic_traffic: 168000
    organic_keywords: 17500
    source: "freesoft_RU_main_overiew.png"
  - domain: frees0ft.fr
    dr: 23
    organic_traffic: 4  # NOTE: RU filter, real FR traffic ~21.6K (from organic_traff_loc_FR.png)
    organic_keywords: 11
    source: "freesoft_FR_main_overiew.png"

duplicates:
  - files: ["frees0ft_fr_top_pages...23_03_45.csv", "frees0ft_fr_top_pages...23_11_08.csv"]
    identical: true/false  # определяется diff
  - files: ["frees0ft_fr_top_pages...23_03_29.csv", "frees0ft_fr_top_pages...23_11_22.csv"]
    identical: true/false
```

### Task `00b-convert-encoding`

**Цель:** Конвертировать все CSV из UTF-16LE в UTF-8 для корректной работы Unix-инструментов.
**max-turns:** 50
**Зависимость:** после `00-inventory`

Действия:
```bash
mkdir -p data_utf8
for f in data_for_task/*.csv; do
  base=$(basename "$f")
  encoding=$(file -b "$f" | grep -o 'UTF-16\|ASCII\|UTF-8')
  if [ "$encoding" = "UTF-16" ]; then
    iconv -f UTF-16LE -t UTF-8 < "$f" | sed 's/\r$//' > "data_utf8/$base"
  else
    # ASCII/UTF-8 files (e.g., performance CSVs) — just strip CRLF
    sed 's/\r$//' < "$f" > "data_utf8/$base"
  fi
done
```

**ВАЖНО:** 2 файла performance (`frees0ft.fr-perf-subdomains_year2_daily_*.csv`) имеют кодировку **ASCII** с разделителем-запятой (не UTF-16LE, не табуляция). Скрипт выше обрабатывает это автоматически.

Верификация:
- Все 36 CSV файлов созданы в `data_utf8/`
- `head -1 data_utf8/uptodown*.csv` показывает нормальные ASCII-заголовки
- `wc -l` дает корректные числа
- `wc -l data_utf8/frees0ft.fr-perf*.csv` показывает 731 строку (не 0!)

---

## Phase 1: Parse & Extract (параллельно, MAX_PARALLEL=3)

Каждая задача берет конвертированные CSV из `data_utf8/`, обрабатывает через Bash (awk/sort/cut), записывает компактный YAML brief.

**ВАЖНО:** Все CSV пути — через `data_utf8/`, НЕ `data_for_task/`. PNG по-прежнему из `data_for_task/`.

### Tasks (17 задач)

#### Наши домены

| Task | Что делает | Входные файлы | CSV строк | Выходной brief |
|------|-----------|---------------|-----------|----------------|
| `01-parse-freesoft-net` | Keywords + top pages + competitors freesoft.net | 8 CSV + 2 PNG | ~4,222 | `briefs/01-freesoft-net.yaml` |
| `02a-parse-freesoft-ru-keywords` | Keywords freesoft.ru: actual + comparison | 2 CSV + 2 PNG | ~47,484 | `briefs/02a-freesoft-ru-kw.yaml` |
| `02b-parse-freesoft-ru-pages` | Top pages freesoft.ru: actual + comparison | 2 CSV | ~30,687 | `briefs/02b-freesoft-ru-pages.yaml` |
| `03-parse-freesoft-fr` | Keywords + top pages + performance frees0ft.fr | 9 CSV + 2 PNG | ~11,163 | `briefs/03-freesoft-fr.yaml` |

#### Конкуренты — мультиязычные

| Task | Что делает | Входные файлы | CSV строк | Выходной brief |
|------|-----------|---------------|-----------|----------------|
| `04a-parse-uptodown-structure` | Site structure uptodown — языки/поддомены | 1 CSV + 1 PNG | ~30,001 | `briefs/04a-uptodown-struct.yaml` |
| `04b-parse-uptodown-pages` | Top pages uptodown — actual + comparison | 2 CSV | ~60,046 | `briefs/04b-uptodown-pages.yaml` |
| `05a-parse-softonic-com-structure` | Site structure softonic.com | 1 CSV + 1 PNG | ~30,001 | `briefs/05a-softonic-com-struct.yaml` |
| `05b-parse-softonic-com-pages` | Top pages softonic.com — actual + comparison | 2 CSV | ~60,079 | `briefs/05b-softonic-com-pages.yaml` |
| `05c-parse-softonic-ru` | Site structure softonic.ru | 1 CSV + 1 PNG | ~30,001 | `briefs/05c-softonic-ru.yaml` |
| `06a-parse-malavida-structure` | Site structure malavida — языки | 1 CSV + 1 PNG | ~30,001 | `briefs/06a-malavida-struct.yaml` |
| `06b-parse-malavida-pages` | Top pages malavida — actual + comparison | 2 CSV | ~60,002 | `briefs/06b-malavida-pages.yaml` |

#### Конкуренты — одноязычные

| Task | Что делает | Входные файлы | CSV строк | Выходной brief |
|------|-----------|---------------|-----------|----------------|
| `07a-parse-filehippo` | Site structure filehippo | 1 CSV + 1 PNG | ~30,001 | `briefs/07a-filehippo.yaml` |
| `07b-parse-trashbox` | Site structure trashbox.ru | 1 CSV + 1 PNG | ~30,001 | `briefs/07b-trashbox.yaml` |

#### Конкуренты — французский рынок

| Task | Что делает | Входные файлы | CSV строк | Выходной brief |
|------|-----------|---------------|-----------|----------------|
| `08a-parse-clubic` | Top pages clubic.com | 1 CSV + 1 PNG | ~26,609 | `briefs/08a-clubic.yaml` |
| `08b-parse-01net` | Top pages 01net.com | 1 CSV + 1 PNG | ~28,699 | `briefs/08b-01net.yaml` |
| `08c-parse-commentcamarche` | Top pages commentcamarche.net | 1 CSV + 1 PNG | ~30,001 | `briefs/08c-commentcamarche.yaml` |

### Подробная маппировка файлов

#### Task 01-parse-freesoft-net (8 CSV + 2 PNG → ~4,222 строк)

CSV (из `data_utf8/`):
1. `freesoft_net_organic_keywords_subdomains_us_2026_01_19_12_02_04.csv` (149 строк, keywords US comparison)
2. `freesoft_net_organic_keywords_subdomains_ru_2026_03_05_22_29_58.csv` (2617 строк, keywords RU comparison)
3. `freesoft_net_organic_keywords_subdomains_ru_2026_03_05_22_30_14.csv` (139 строк, keywords RU actual)
4. `freesoft_net_top_pages_subdomains_us_comp_2026_01_19_12_04_24.csv` (17 строк, top pages US comparison)
5. `freesoft_net_top_pages_subdomains_ru_comp_2026_03_05_22_30_46.csv` (1170 строк, top pages RU comparison)
6. `freesoft_net_top_pages_subdomains_ru_actu_2026_03_05_22_31_09.csv` (88 строк, top pages RU actual)
7. `freesoft_net_orgcompetitors_subdomains_ru_2026_01_19_12_38_49.csv` (21 строк, competitors RU)
8. `freesoft_net_orgcompetitors_subdomains_us_2026_01_19_12_41_12.csv` (21 строк, competitors US)

PNG (из `data_for_task/`):
1. `freesoft_net_main_overiew.png` (DR 51, Traffic 89 — RU filter!)
2. `organic_traff_loc_US.png` (India 14.2K, Bangladesh 5.4K, US 2.1K)

#### Task 02a-parse-freesoft-ru-keywords (2 CSV + 2 PNG → ~47,484 строк)

CSV:
1. `freesoft_ru_organic_keywords_subdomains_ru_2026_03_05_22_26_41.csv` (17483, actual)
2. `freesoft_ru_organic_keywords_subdomains_ru_2026_03_05_22_27_20.csv` (30001, comparison)

PNG:
1. `freesoft_RU_main_overiew.png` (DR 59, Traffic 168K)
2. `organic_traff_loc_RU.png` (Russia 168K, Kazakhstan 28.7K)

#### Task 02b-parse-freesoft-ru-pages (2 CSV → ~30,687 строк)

CSV:
1. `freesoft_ru_top_pages_subdomains_ru_actua_2026_03_05_22_28_10.csv` (8439, actual)
2. `freesoft_ru_top_pages_subdomains_ru_compa_2026_03_05_22_28_29.csv` (22248, comparison)

#### Task 03-parse-freesoft-fr (9 CSV + 2 PNG → ~11,163 строк)

CSV:
1. `frees0ft_fr_organic_keywords_subdomains_fr_2026_03_05_22_20_26.csv` (733, actual)
2. `frees0ft_fr_organic_keywords_subdomains_fr_2026_03_05_22_21_09.csv` (3967, comparison)
3. `frees0ft_fr_top_pages_subdomains_fr_actua_2026_03_05_23_03_45.csv` (488, actual)
4. `frees0ft_fr_top_pages_subdomains_fr_actua_2026_03_05_23_11_08.csv` (488, actual duplicate?)
5. `frees0ft_fr_top_pages_subdomains_fr_compa_2026_03_05_23_03_29.csv` (1931, comparison)
6. `frees0ft_fr_top_pages_subdomains_fr_compa_2026_03_05_23_11_22.csv` (1931, comparison duplicate?)
7. `frees0ft_fr_top_pages_subdomains_ru_compa_2026_03_05_22_22_00.csv` (164, RU comparison)
8. `frees0ft.fr-perf-subdomains_year2_daily_2026-03-05_22-22-53.csv` (731, performance RU) **ВНИМАНИЕ: ASCII, comma-delimited (не tab)**
9. `frees0ft.fr-perf-subdomains_year2_daily_2026-03-05_23-03-23.csv` (731, performance FR) **ВНИМАНИЕ: ASCII, comma-delimited (не tab)**

PNG:
1. `freesoft_FR_main_overiew.png` (DR 23, Traffic 4 — RU filter!)
2. `organic_traff_loc_FR.png` (France 12.7K, Senegal 6.1K)

#### Tasks 04a/04b (uptodown)

04a: `uptodown_com_site_structure_subdomains_ru_2026_03_05_22_38_10.csv` (30001) + `uptodown_com_US_overview.png`
04b: `uptodown_com_top_pages_subdomains_all_act_2026_03_05_23_03_05.csv` (30045) + `uptodown_com_top_pages_subdomains_ru_comp_2026_03_05_23_02_25.csv` (30001)

#### Tasks 05a/05b/05c (softonic)

05a: `softonic_com_site_structure_subdomains_ru_2026_03_05_22_48_04.csv` (30001) + `softonic_com_US_overview.png`
05b: `softonic_com_top_pages_subdomains_all_act_2026_03_05_23_04_55.csv` (30029) + `softonic_com_top_pages_subdomains_all_com_2026_03_05_23_04_30.csv` (30050)
05c: `softonic_ru_site_structure_subdomains_ru_2026_03_05_22_40_52.csv` (30001) + `softonic_ru_RU_overview.png`

#### Tasks 06a/06b (malavida)

06a: `malavida_com_site_structure_subdomains_ru_2026_03_05_22_46_42.csv` (30001) + `malavida_com_US_overview.png`
06b: `malavida_com_top_pages_subdomains_all_act_2026_03_05_23_05_50.csv` (30001) + `malavida_com_top_pages_subdomains_all_com_2026_03_05_23_05_32.csv` (30001)

#### Tasks 07a/07b (minor competitors)

07a: `filehippo_com_site_structure_subdomains_ru_2026_03_05_22_49_10.csv` (30001) + `filehippo_com_US_overview.png`
07b: `trashbox_ru_site_structure_subdomains_ru_2026_03_05_22_44_22.csv` (30001) + `trashbox_ru_US_overview.png`

#### Tasks 08a/08b/08c (FR market)

08a: `clubic_com_top_pages_subdomains_all_actua_2026_03_05_23_06_47.csv` (26609) + `clubic_com_US_overview.png`
08b: `01net_com_top_pages_subdomains_all_actual_2026_03_05_23_06_59.csv` (28699) + `01net_com_US_overview.png`
08c: `commentcamarche_net_top_pages_subdomains_al_2026_03_05_23_07_08.csv` (30001) + `ommentcamarche_net_overview.png`

### Формат выходного brief (с chain-of-evidence)

Каждый brief ОБЯЗАН содержать `source` для каждого значения:

```yaml
domain: uptodown.com
dr:
  value: 83
  source: "uptodown_com_US_overview.png"
total_organic_traffic:
  value: 983000
  source: "uptodown_com_US_overview.png"
  note: "Approximated from screenshot"
total_keywords:
  value: 95800
  source: "uptodown_com_US_overview.png"

# Из site_structure CSV — распределение по языкам
traffic_by_language:
  - subdomain_or_folder: "en.uptodown.com"
    traffic: 234000
    share_pct: 23.8
    keywords: 45000
    source: "uptodown_com_site_structure_subdomains_ru_2026_03_05_22_38_10.csv"
    extraction: "awk -F'\\t' 'NR>1 {print $1,$4,$6}' | sort -t$'\\t' -k2 -rn | head -20"

# Из top_pages CSV — топ-50 страниц по трафику
top_pages:
  - url: "/android/..."
    traffic: 12500
    keywords: 340
    source: "uptodown_com_top_pages_subdomains_all_act_2026_03_05_23_03_05.csv"

# Агрегаты по типам страниц
traffic_by_page_type:
  app_pages:
    value: 650000
    source: "uptodown_com_top_pages...csv"
    extraction: "awk filter on URL patterns /android|windows|mac/"

# Топ-10 стран по трафику
traffic_by_country:
  - country: India
    traffic: 6800000
    share_pct: 21.5
    source: "uptodown_com_US_overview.png"
```

### Формат для наших доменов (с chain-of-evidence)

```yaml
domain: freesoft.ru
dr:
  value: 59
  source: "freesoft_RU_main_overiew.png"
total_organic_traffic:
  value: 168000
  source: "freesoft_RU_main_overiew.png"

# Текущее распределение по странам
traffic_by_country:
  - country: Russia
    traffic: 168000
    share_pct: 71.9
    source: "organic_traff_loc_RU.png"

# Топ-50 keywords по трафику (из CSV через Bash)
top_keywords:
  - keyword: "..."
    volume: XX
    position: XX
    traffic: XX
    url: "..."
    source: "freesoft_ru_organic_keywords_subdomains_ru_2026_03_05_22_26_41.csv"

# Тренд
trend:
  direction: "growing"
  change_pct: XX
  source: "freesoft_ru_organic_keywords_subdomains_ru_2026_03_05_22_27_20.csv (comparison)"

# Конкурентное окружение (только для freesoft.net)
competitors:
  - domain: "example.com"
    common_keywords: XX
    share: XX
    source: "freesoft_net_orgcompetitors_subdomains_ru_2026_01_19_12_38_49.csv"
```

**max-turns:** 150 (для задач с 1 CSV ≤30K строк), 200 (для задач с 2 CSV, как 04b/05b/06b)

---

## Phase 1.5: Validate Briefs (singleton)

### Task `10-validate-briefs`

**Цель:** Проверить что все Phase 1 briefs корректны перед запуском Phase 2.
**max-turns:** 50
**Зависимость:** после ВСЕХ Phase 1 задач

Проверки:
1. Все ожидаемые brief-файлы существуют (17 файлов)
2. Каждый brief не пустой и содержит валидный YAML
3. Обязательные поля присутствуют: `domain`, `dr`, `total_organic_traffic`, `source`
4. Для мультиязычных конкурентов: `traffic_by_language` содержит минимум 3 языка
5. Для наших доменов: `top_keywords` содержит минимум 20 записей
6. Числовые значения > 0 (кроме frees0ft.fr где трафик может быть малым)

Выход: `briefs/10-validation-result.yaml`
```yaml
status: "PASS" | "FAIL"
briefs_checked: 17
briefs_ok: [list]
briefs_failed:
  - file: "briefs/04b-uptodown-pages.yaml"
    issue: "Missing top_pages field"
```

Если FAIL — pipeline останавливается. Оператор проверяет и перезапускает проблемные Phase 1 задачи.

---

## Phase 2: Deep Analysis (параллельно, MAX_PARALLEL=3)

Работает ТОЛЬКО с briefs из Phase 1. Чистый анализ, без обработки сырых CSV.

| Chain | Task | Что анализирует | Входные briefs | Выход |
|-------|------|----------------|---------------|-------|
| A | `11-analyze-our-domains` | Сравнение 3 доменов freesoft: состояние, тренды, сильные/слабые стороны | 01, 02a, 02b, 03 | `briefs/11-our-state.yaml` |
| B | `12-analyze-multilingual-competitors` | Языковые стратегии uptodown/softonic/malavida: какие языки, сколько трафика дает каждый | 04a, 04b, 05a, 05b, 05c, 06a, 06b | `briefs/12-multilingual-analysis.yaml` |
| C | `13-analyze-fr-market` | Глубина французского рынка, уровень конкуренции, позиция frees0ft.fr | 03, 08a, 08b, 08c | `briefs/13-fr-market-analysis.yaml` |
| D | `14-analyze-domain-structures` | Как конкуренты организуют языки: поддомены vs папки vs отдельные домены | 04a, 05a, 05c, 06a, 07a, 07b | `briefs/14-domain-structures.yaml` |

**Примечание:** Task 12 читает 7 briefs. Каждый brief ~200-400 строк YAML = суммарно ~2000-2800 строк. Безопасно.

**max-turns:** 200

---

## Phase 3: Cross-Analysis (последовательно)

Задачи зависят друг от друга. Каждая читает предыдущие + briefs из Phase 2.

| Task | Что делает | Входные briefs | Выход |
|------|-----------|---------------|-------|
| `16-language-potential` | Потенциал каждого языка: TAM/SAM, сколько трафика получают конкуренты, какую долю мог бы забрать freesoft | 11 + 12 + 13 | `briefs/16-language-potential.yaml` |
| `17-domain-strategy` | Рекомендация: домены vs папки vs поддомены. Плюсы/минусы/риски миграции. На основе данных конкурентов | 14 + 16 | `briefs/17-domain-strategy.yaml` |
| `18-roadmap-draft` | Черновик roadmap: языки, порядок, шаблоны страниц, KPI | 16 + 17 | `briefs/18-roadmap-draft.yaml` |

**max-turns:** 200

---

## Phase 4: Deliverables (параллельно — задачи независимы)

Финальные документы для клиента. Каждый читает нужные briefs. Задачи 20 и 21 пишут в разные файлы и не зависят друг от друга — запускаются параллельно.

| Task | Что делает | Входные briefs | Выход |
|------|-----------|---------------|-------|
| `20-report-domain-strategy` | Итоговый документ: рекомендация по доменной стратегии + план миграции | 11 + 14 + 16 + 17 | `output/domain-strategy.md` |
| `21-report-multilingual-roadmap` | Итоговый документ: мультиязычный roadmap с приоритетами, шаблонами, KPI | 11 + 12 + 13 + 16 + 17 + 18 | `output/multilingual-roadmap.md` |

**max-turns:** 150

---

## Phase 5: Validation (singleton)

| Task | Что делает |
|------|-----------|
| `22-validate` | Читает оба финальных документа + ключевые briefs (11, 12, 13, 14, 16, 17, 18) + Phase 1 briefs для spot-check (04a, 05a, 06a). Проверяет: (1) каждая цифра в отчете подтверждена `source` из briefs, (2) каждый вывод логически следует из фактов, (3) нет выдуманных данных, (4) нет пропущенных языков/конкурентов, (5) gambling/betting/adult контент отфильтрован, (6) chain-of-evidence прослеживается от Phase 1 brief до финального документа. Записывает `output/validation-report.md` |

**max-turns:** 150

---

## Обработка edge cases (во ВСЕХ промптах Phase 1)

1. **Пустой или поврежденный CSV:**
   ```
   Перед обработкой проверь: wc -l < file.csv. Если <2 строк — пиши "ФАЙЛ ПУСТ" в brief и продолжай.
   ```

2. **PNG нечитаемый / низкое качество:**
   ```
   Если не можешь прочитать цифру на скриншоте — пиши "НЕ ВИДНО НА СКРИНШОТЕ" вместо числа. НЕ угадывай.
   ```

3. **Нет данных по языку у конкурента:**
   ```
   Если site_structure не содержит языковых поддоменов/папок — запиши: language_structure: "single_language". Не выдумывай.
   ```

4. **site_structure показывает 500+ поддоменов:**
   ```
   Фильтруй: оставляй только поддомены/папки с traffic > 100. Для остальных — суммируй в "other".
   ```

5. **Gambling/betting/adult контент в данных:**
   ```
   Фильтруй URL и keywords по regex: (?i)(casino|gambling|slots|betting|poker|roulette|jackpot|porn|xxx|adult|nsfw|1xbet|juwa|rummy)
   Исключай из top_pages, top_keywords, traffic_by_page_type.
   ```

---

## Структура файлов

```
pipeline-seo/
|-- ARCHITECTURE.md            # Этот документ
|-- REVIEW_REPORT.md           # Отчет ревью архитектуры
|-- data-inventory.md          # Полная инвентаризация входных файлов
|-- run.sh                     # Оркестратор
|-- prompts/
|   |-- 00-inventory.md
|   |-- 00b-convert-encoding.md
|   |-- 01-parse-freesoft-net.md
|   |-- 02a-parse-freesoft-ru-keywords.md
|   |-- 02b-parse-freesoft-ru-pages.md
|   |-- 03-parse-freesoft-fr.md
|   |-- 04a-parse-uptodown-structure.md
|   |-- 04b-parse-uptodown-pages.md
|   |-- 05a-parse-softonic-com-structure.md
|   |-- 05b-parse-softonic-com-pages.md
|   |-- 05c-parse-softonic-ru.md
|   |-- 06a-parse-malavida-structure.md
|   |-- 06b-parse-malavida-pages.md
|   |-- 07a-parse-filehippo.md
|   |-- 07b-parse-trashbox.md
|   |-- 08a-parse-clubic.md
|   |-- 08b-parse-01net.md
|   |-- 08c-parse-commentcamarche.md
|   |-- 10-validate-briefs.md
|   |-- 11-analyze-our-domains.md
|   |-- 12-analyze-multilingual-competitors.md
|   |-- 13-analyze-fr-market.md
|   |-- 14-analyze-domain-structures.md
|   |-- 16-language-potential.md
|   |-- 17-domain-strategy.md
|   |-- 18-roadmap-draft.md
|   |-- 20-report-domain-strategy.md
|   |-- 21-report-multilingual-roadmap.md
|   |-- 22-validate.md
|-- briefs/                    # Промежуточные данные (gitignore)
|   |-- 00-manifest.yaml
|   |-- 01-freesoft-net.yaml
|   |-- 02a-freesoft-ru-kw.yaml
|   |-- 02b-freesoft-ru-pages.yaml
|   |-- 03-freesoft-fr.yaml
|   |-- 04a-uptodown-struct.yaml
|   |-- 04b-uptodown-pages.yaml
|   |-- 05a-softonic-com-struct.yaml
|   |-- 05b-softonic-com-pages.yaml
|   |-- 05c-softonic-ru.yaml
|   |-- 06a-malavida-struct.yaml
|   |-- 06b-malavida-pages.yaml
|   |-- 07a-filehippo.yaml
|   |-- 07b-trashbox.yaml
|   |-- 08a-clubic.yaml
|   |-- 08b-01net.yaml
|   |-- 08c-commentcamarche.yaml
|   |-- 10-validation-result.yaml
|   |-- 11-our-state.yaml
|   |-- 12-multilingual-analysis.yaml
|   |-- 13-fr-market-analysis.yaml
|   |-- 14-domain-structures.yaml
|   |-- 16-language-potential.yaml
|   |-- 17-domain-strategy.yaml
|   |-- 18-roadmap-draft.yaml
|-- output/                    # Финальные документы
|   |-- domain-strategy.md
|   |-- multilingual-roadmap.md
|   |-- validation-report.md
|-- data_utf8/                 # Конвертированные CSV (gitignore)
|-- .done/                     # Маркеры выполнения (gitignore)
|-- logs/                      # Логи выполнения (gitignore)
```

---

## Конфигурация run.sh

```bash
CLAUDE_MODEL=opus
MAX_PARALLEL=3
ALLOWED_TOOLS=Read,Write,Edit,Glob,Grep,Bash

TASKS=(
  # Phase 0
  "00-inventory"
  "00b-convert-encoding"
  # Phase 1 — наши домены
  "01-parse-freesoft-net"
  "02a-parse-freesoft-ru-keywords"
  "02b-parse-freesoft-ru-pages"
  "03-parse-freesoft-fr"
  # Phase 1 — мультиязычные конкуренты
  "04a-parse-uptodown-structure"
  "04b-parse-uptodown-pages"
  "05a-parse-softonic-com-structure"
  "05b-parse-softonic-com-pages"
  "05c-parse-softonic-ru"
  "06a-parse-malavida-structure"
  "06b-parse-malavida-pages"
  # Phase 1 — одноязычные конкуренты
  "07a-parse-filehippo"
  "07b-parse-trashbox"
  # Phase 1 — FR market
  "08a-parse-clubic"
  "08b-parse-01net"
  "08c-parse-commentcamarche"
  # Phase 1.5
  "10-validate-briefs"
  # Phase 2
  "11-analyze-our-domains"
  "12-analyze-multilingual-competitors"
  "13-analyze-fr-market"
  "14-analyze-domain-structures"
  # Phase 3
  "16-language-potential"
  "17-domain-strategy"
  "18-roadmap-draft"
  # Phase 4
  "20-report-domain-strategy"
  "21-report-multilingual-roadmap"
  # Phase 5
  "22-validate"
)

# Phase execution order (оркестратор выполняет фазы последовательно, внутри фаз — параллельно)
PHASE_0=("00-inventory" "00b-convert-encoding")  # sequential singletons
PHASE_1=(
  "01-parse-freesoft-net"
  "02a-parse-freesoft-ru-keywords" "02b-parse-freesoft-ru-pages"
  "03-parse-freesoft-fr"
  "04a-parse-uptodown-structure" "04b-parse-uptodown-pages"
  "05a-parse-softonic-com-structure" "05b-parse-softonic-com-pages" "05c-parse-softonic-ru"
  "06a-parse-malavida-structure" "06b-parse-malavida-pages"
  "07a-parse-filehippo" "07b-parse-trashbox"
  "08a-parse-clubic" "08b-parse-01net" "08c-parse-commentcamarche"
)
PHASE_1_5=("10-validate-briefs")  # singleton gate
PHASE_2=("11-analyze-our-domains" "12-analyze-multilingual-competitors" "13-analyze-fr-market" "14-analyze-domain-structures")
PHASE_3=("16-language-potential" "17-domain-strategy" "18-roadmap-draft")  # sequential
PHASE_4=("20-report-domain-strategy" "21-report-multilingual-roadmap")  # PARALLEL (independent outputs)
PHASE_5=("22-validate")  # singleton
```

**Примечание:** Внутри Phase 1 все 17 задач независимы — читают из `data_utf8/` (read-only), пишут в разные brief-файлы. Оркестратор запускает партиями по MAX_PARALLEL=3. При 17 задачах = 6 батчей (5 по 3 + 1 остаток).

---

## Критические правила (во ВСЕХ промптах)

1. **ЗАПРЕЩЕНО выдумывать данные.** Каждая цифра берется из файлов. Если данных нет — писать "ДАННЫЕ ОТСУТСТВУЮТ".
2. **Chain of evidence обязателен.** Каждое числовое значение в brief содержит `source` (имя файла) и `extraction` (Bash-команда или "visual from PNG").
3. **Фильтрация контента:** исключать gambling/betting/adult (regex из CLAUDE.md).
4. **CSV пути:** `data_utf8/filename.csv` (НЕ `data_for_task/`). PNG пути: `data_for_task/filename.png`.
5. **Для больших CSV (>1000 строк) — использовать Bash:** `awk`, `sort`, `head`, `cut`, `wc`. НЕ пытаться прочитать через Read.
6. **Каждый prompt самодостаточен:** никаких "продолжи", всё нужное — в prompt или в referenced файлах.
7. **Верификация в конце каждого task:** проверить что выходной файл существует, не пустой, содержит все обязательные поля.
8. **UTF-8 only:** все CSV читаются из `data_utf8/`. Если агент видит BOM или wide chars — это ошибка, значит читает из `data_for_task/`.

---

## Оценки

| Метрика | Значение |
|---------|----------|
| Всего tasks | 29 |
| Phase 0 (sequential) | 2 |
| Phase 1 (parallel) | 17 |
| Phase 1.5 (singleton) | 1 |
| Phase 2 (parallel) | 4 |
| Phase 3 (sequential) | 3 |
| Phase 4 (parallel) | 2 |
| Phase 5 (singleton) | 1 |
| MAX_PARALLEL | 3 (утверждено заказчиком) |
| Примерное время | 4-5 часов |
| Рестартуемость | Да (.done/ маркеры) |
| Meta-prompts для генерации | Рекомендовано: 4 meta-prompts (Phase 1: 17, Phase 2: 4, Phase 3-4: 5, Phase 5: 1+1) |

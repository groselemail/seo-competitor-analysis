# Источники данных

> Дата документа: 2026-03-06
> Источники: `analysis/data-inventory.md`, `analysis/cross-analysis/manifest.yaml`

---

## Ahrefs

Ahrefs — SEO-платформа для анализа поисковой видимости сайтов. В рамках данного проекта используется для:

- Анализа органических ключевых слов и позиций в поиске
- Оценки трафика и его динамики по страницам
- Изучения структуры сайтов конкурентов
- Выявления органических конкурентов по пересечению семантики
- Отслеживания исторической динамики (performance)
- Оценки авторитетности доменов (DR, UR) и ссылочного профиля

---

## Типы отчётов

В выгрузке представлены следующие типы отчётов Ahrefs:

| Тип отчёта | Описание | Подтипы | Ключевые колонки |
|------------|----------|---------|------------------|
| **organic_keywords** | Органические ключевые слова домена | actual, comparison | Keyword, Volume, KD, Position, Traffic, Position change |
| **top_pages** | Топ страницы по органическому трафику | actual, comparison | URL, Traffic, Keywords, Top keyword, Traffic change |
| **site_structure** | Структура сайта по URL-путям | — | Path, Organic traffic, Organic keywords, Organic pages, Ref. domains |
| **competitors** | Органические конкуренты по пересечению ключей | actual, comparison | Domain, Common keywords, Share, DR, Traffic |
| **performance_daily** | Ежедневная динамика трафика и страниц | — | Date, Organic pages, Organic traffic |
| **overview** | Общий обзор домена (скриншоты) | — | DR, UR, Keywords, Traffic, Backlinks, Ref. domains |
| **traffic_by_location** | Распределение трафика по странам (скриншоты) | — | Country, Traffic, Share, Keywords |

**Подтипы:**
- **actual** — текущий срез данных (позиции, трафик на момент выгрузки)
- **comparison** — сравнительный отчёт (изменения позиций и трафика между двумя датами)

---

## Анализируемые сайты

### Наши домены

| Домен | DR | Трафик (фильтр) | CSV | PNG | Типы отчётов |
|-------|----|------------------|-----|-----|--------------|
| freesoft.net | 51 | 89 (RU) | 8 | 2 | organic_keywords, top_pages, competitors, overview, traffic_by_location |
| freesoft.ru | 59 | 168K (RU) | 4 | 2 | organic_keywords, top_pages, overview, traffic_by_location |
| frees0ft.fr | 23 | ~21.6K (FR) | 9 | 2 | organic_keywords, top_pages, performance_daily, overview, traffic_by_location |

### Конкуренты

| Домен | DR | Трафик (фильтр) | CSV | PNG | Типы отчётов |
|-------|----|------------------|-----|-----|--------------|
| uptodown.com | 83 | 983K (US) | 3 | 1 | site_structure, top_pages (actual + comparison), overview |
| softonic.com | 86 | 88.5K (RU) | 3 | 1 | site_structure, top_pages (actual + comparison), overview |
| softonic.ru | 50 | 335K (RU) | 1 | 1 | site_structure, overview |
| malavida.com | 73 | 526K (US) | 3 | 1 | site_structure, top_pages (actual + comparison), overview |
| filehippo.com | 77 | 526 (RU) | 1 | 1 | site_structure, overview |
| trashbox.ru | 54 | 991K (RU) | 1 | 1 | site_structure, overview |
| clubic.com | 81 | 186 (RU) | 1 | 1 | top_pages (actual), overview |
| 01net.com | 81 | 1.5M (ALL) | 1 | 1 | top_pages (actual), overview |
| commentcamarche.net | 80 | 227K (ALL) | 1 | 1 | top_pages (actual), overview |

---

## Параметры выгрузки

| Параметр | Значение |
|----------|----------|
| Период выгрузки | Январь — март 2026 (основная часть: 5 марта 2026) |
| Кодировка CSV | UTF-16LE с BOM (требуется конвертация в UTF-8 перед обработкой) |
| Исключение | 2 файла performance_daily (frees0ft.fr) — ASCII, разделитель запятая |
| Разделитель полей | Tab (основные CSV), запятая (performance CSV) |
| Лимит строк | ~30 000 строк на отчёт (ограничение Ahrefs) |
| Фильтры по стране | RU, US, FR, ALL — в зависимости от домена и отчёта |

---

## Статистика

| Метрика | Значение |
|---------|----------|
| Всего файлов | 51 |
| CSV файлов | 36 |
| PNG файлов (скриншоты) | 15 |
| Общее количество строк в CSV | ~548 917 |
| CSV, достигших лимита 30K строк | 16 из 36 (44%) |
| Дублирующихся пар CSV | 2 пары (4 файла, все frees0ft.fr) |

### Распределение CSV по размеру

| Диапазон строк | Количество файлов |
|----------------|-------------------|
| < 100 | 5 |
| 100–1 000 | 7 |
| 1 000–10 000 | 6 |
| 10 000–30 000 | 4 |
| 30 000 (лимит) | 14 |

---

## Ограничения и caveats

### Лимит выгрузки Ahrefs

16 из 36 CSV-файлов содержат ровно 30 001 строку — это потолок экспорта Ahrefs. Данные в этих файлах **неполные**: отсечены записи с наименьшим трафиком / позициями. Это касается:
- Всех отчётов site_structure (5 файлов конкурентов)
- organic_keywords comparison для freesoft.ru (30 001 строка из потенциально большего набора)
- top_pages для крупных конкурентов (uptodown, softonic, malavida, commentcamarche)

### Фильтры по странам

Обзорные скриншоты (overview PNG) сняты с разными фильтрами по странам, что влияет на отображаемые метрики:
- freesoft.net и frees0ft.fr: overview с фильтром «Russian Federation» — трафик занижен (89 и 4 соответственно), реальный суммарный трафик значительно выше
- softonic.com: overview с фильтром RU — трафик 88.5K, реальный глобальный трафик значительно выше
- clubic.com: фильтр RU — трафик 186, реальный FR-трафик 635.5K
- uptodown.com: фильтр US — показан только US-срез
- 01net.com, commentcamarche.net: фильтр «All locations» — данные глобальные

При сравнении метрик между доменами необходимо учитывать различие фильтров.

### Кодировка

Все основные CSV-файлы имеют кодировку UTF-16LE с BOM. Перед обработкой утилитами (awk, sort, head, grep) требуется конвертация в UTF-8 через `iconv`. Два файла performance_daily являются исключением — они в ASCII с разделителем-запятой.

### Дубликаты

В выгрузке frees0ft.fr присутствуют 2 пары побайтово идентичных файлов (подтверждено MD5). Используются файлы с более ранней меткой времени:
- `frees0ft_fr_top_pages_subdomains_fr_actua_2026_03_05_23_03_45.csv` (вместо 23_11_08)
- `frees0ft_fr_top_pages_subdomains_fr_compa_2026_03_05_23_03_29.csv` (вместо 23_11_22)

### Точность метрик Ahrefs

- Трафик Ahrefs — оценочная метрика, не фактический трафик. Основана на модели CTR по позициям и объёмам запросов
- Keyword Difficulty (KD) — собственная шкала Ahrefs (0–100), не сопоставима напрямую с другими инструментами
- Domain Rating (DR) — метрика силы ссылочного профиля домена; не является фактором ранжирования Google
- Расхождения в количестве строк: некоторые файлы в data-inventory.md указаны с количеством 30 029 / 30 045 / 30 050, но фактический подсчёт через `iconv | wc -l` даёт 30 001

---

## Phase 2: Ссылочные данные (Backlink Analysis)

**Источник:** Ahrefs, экспорт 2026-03-13.

**39 CSV-файлов, 4 типа отчётов:**

| Тип отчёта | Файлов | Описание |
|-----------|--------|----------|
| Referring Domains (A) | 12 | Ссылающиеся домены по каждому из 12 доменов |
| Anchors (B) | 12 | Анкорные тексты ссылок |
| Backlinks One Per Domain (C) | 12 | По одной ссылке с каждого домена |
| Link Intersect (D) | 3 | Пересечения: EN, RU, FR группы |

**Объём:** ~660 000 строк после gambling/adult фильтрации (9 900 строк отфильтровано).

**Ограничение Ahrefs:** 14 файлов достигли лимита 30K строк (softonic.com, uptodown.com и др.). Реальные значения для крупных конкурентов выше.

Подробнее: [08-methodology.md](../reports/backlink-strategy/08-methodology.md)

### Данные filehippo.com

В overview-скриншоте filehippo.com данные Backlinks и Ref. domains не загрузились (ошибка Ahrefs). Ссылочные метрики для этого домена отсутствуют.

### HTTP-статус malavida.com

Overview malavida.com фиксирует HTTP 301 redirect — домен может использовать перенаправления, что влияет на интерпретацию ссылочных метрик.

### Опечатка в имени файла

Файл `ommentcamarche_net_overview.png` — пропущена первая буква «c» (корректно: commentcamarche.net).

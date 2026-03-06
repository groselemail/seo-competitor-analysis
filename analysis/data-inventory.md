# Инвентаризация данных: data_for_task/

> Создано: 2026-03-05
> Всего файлов: 51 (36 CSV + 15 PNG)
> ПРЕДУПРЕЖДЕНИЕ О КОДИРОВКЕ: Все CSV-файлы в кодировке UTF-16LE с BOM. Необходимо конвертировать в UTF-8 перед обработкой через awk/sort/head.

---

## Наши домены

### freesoft.net (8 CSV + 2 PNG)

| # | File | Type | Rows | Report Type | Country | Key Columns |
|---|------|------|------|-------------|---------|-------------|
| 1 | freesoft_net_organic_keywords_subdomains_us_2026_01_19_12_02_04.csv | CSV | 149 | organic_keywords (comparison) | US | Keyword, Volume, KD, Position change, Traffic change |
| 2 | freesoft_net_organic_keywords_subdomains_ru_2026_03_05_22_29_58.csv | CSV | 2617 | organic_keywords (comparison) | RU | Keyword, Volume, KD, Position change, Traffic change |
| 3 | freesoft_net_organic_keywords_subdomains_ru_2026_03_05_22_30_14.csv | CSV | 139 | organic_keywords (actual) | RU | Keyword, Volume, KD, Position, Traffic |
| 4 | freesoft_net_top_pages_subdomains_us_comp_2026_01_19_12_04_24.csv | CSV | 17 | top_pages (comparison) | US | URL, Traffic change, Keywords change |
| 5 | freesoft_net_top_pages_subdomains_ru_comp_2026_03_05_22_30_46.csv | CSV | 1170 | top_pages (comparison) | RU | URL, Traffic change, Keywords change |
| 6 | freesoft_net_top_pages_subdomains_ru_actu_2026_03_05_22_31_09.csv | CSV | 88 | top_pages (actual) | RU | URL, Traffic, Keywords, Top keyword |
| 7 | freesoft_net_orgcompetitors_subdomains_ru_2026_01_19_12_38_49.csv | CSV | 21 | competitors | RU | Domain, Common keywords, Share, DR, Traffic |
| 8 | freesoft_net_orgcompetitors_subdomains_us_2026_01_19_12_41_12.csv | CSV | 21 | competitors | US | Domain, Common keywords, Share, DR, Traffic |

| # | File | Ключевые метрики со скриншота |
|---|------|-------------------------------|
| 9 | freesoft_net_main_overiew.png | DR 51, UR 27, Keywords 138 (-2.1K), Traffic 89 (-196), Backlinks 191K, Ref domains 3.7K. Фильтр: Russian Federation |
| 10 | organic_traff_loc_US.png | Всего ключевых слов 137. India 14.2K (41%), Bangladesh 5.4K (15.6%), Somalia 2.1K (6.1%), Myanmar 2.1K (6%), US 2.1K (5.9%) |

### freesoft.ru (4 CSV + 2 PNG)

| # | File | Type | Rows | Report Type | Country |
|---|------|------|------|-------------|---------|
| 11 | freesoft_ru_organic_keywords_subdomains_ru_2026_03_05_22_26_41.csv | CSV | 17483 | organic_keywords (actual) | RU |
| 12 | freesoft_ru_organic_keywords_subdomains_ru_2026_03_05_22_27_20.csv | CSV | 30001 | organic_keywords (comparison) | RU |
| 13 | freesoft_ru_top_pages_subdomains_ru_actua_2026_03_05_22_28_10.csv | CSV | 8439 | top_pages (actual) | RU |
| 14 | freesoft_ru_top_pages_subdomains_ru_compa_2026_03_05_22_28_29.csv | CSV | 22248 | top_pages (comparison) | RU |

| # | File | Ключевые метрики со скриншота |
|---|------|-------------------------------|
| 15 | freesoft_RU_main_overiew.png | DR 59, UR 33, Keywords 17.5K (-85.5K), Traffic 168K (+95.9K), Backlinks 170K, Ref domains 3.3K. Фильтр: Russian Federation |
| 16 | organic_traff_loc_RU.png | Всего 91 локация. Russia 168K (71.9%), Kazakhstan 28.7K (12.3%), Ukraine 14.8K (6.3%), Belarus 7.8K (3.3%) |

### frees0ft.fr (9 CSV + 2 PNG)

| # | File | Type | Rows | Report Type | Country |
|---|------|------|------|-------------|---------|
| 17 | frees0ft_fr_organic_keywords_subdomains_fr_2026_03_05_22_20_26.csv | CSV | 733 | organic_keywords (actual) | FR |
| 18 | frees0ft_fr_organic_keywords_subdomains_fr_2026_03_05_22_21_09.csv | CSV | 3967 | organic_keywords (comparison) | FR |
| 19 | frees0ft_fr_top_pages_subdomains_fr_actua_2026_03_05_23_03_45.csv | CSV | 488 | top_pages (actual) | FR |
| 20 | frees0ft_fr_top_pages_subdomains_fr_actua_2026_03_05_23_11_08.csv | CSV | 488 | top_pages (actual, дубликат?) | FR |
| 21 | frees0ft_fr_top_pages_subdomains_fr_compa_2026_03_05_23_03_29.csv | CSV | 1931 | top_pages (comparison) | FR |
| 22 | frees0ft_fr_top_pages_subdomains_fr_compa_2026_03_05_23_11_22.csv | CSV | 1931 | top_pages (comparison, дубликат?) | FR |
| 23 | frees0ft_fr_top_pages_subdomains_ru_compa_2026_03_05_22_22_00.csv | CSV | 164 | top_pages (comparison) | RU |
| 24 | frees0ft.fr-perf-subdomains_year2_daily_2026-03-05_22-22-53.csv | CSV | 731 | performance_daily | RU |
| 25 | frees0ft.fr-perf-subdomains_year2_daily_2026-03-05_23-03-23.csv | CSV | 731 | performance_daily | FR |

| # | File | Ключевые метрики со скриншота |
|---|------|-------------------------------|
| 26 | freesoft_FR_main_overiew.png | DR 23, UR 38, Keywords 11 (-171), Traffic 4 (+2), Backlinks 117K, Ref domains 488. Фильтр: Russian Federation (ПРИМЕЧАНИЕ: низкий трафик из-за фильтра RU) |
| 27 | organic_traff_loc_FR.png | Всего 56 локаций. France 12.7K (58.7%), Senegal 6.1K (28.3%), Cameroon 704 (3.2%), Algeria 362 (1.7%) |

---

## Конкуренты

### uptodown.com (3 CSV + 1 PNG)

| # | File | Rows | Report Type | Country |
|---|------|------|-------------|---------|
| 28 | uptodown_com_site_structure_subdomains_ru_2026_03_05_22_38_10.csv | 30001 | site_structure | RU |
| 29 | uptodown_com_top_pages_subdomains_all_act_2026_03_05_23_03_05.csv | 30045 | top_pages (actual) | ALL |
| 30 | uptodown_com_top_pages_subdomains_ru_comp_2026_03_05_23_02_25.csv | 30001 | top_pages (comparison) | RU |

| 31 | uptodown_com_US_overview.png | DR 83, Keywords ~95.8K, Traffic ~983K (маленький скриншот, точные значения трудно прочитать) |

### softonic.com + softonic.ru (4 CSV + 2 PNG)

| # | File | Rows | Report Type | Domain | Country |
|---|------|------|-------------|--------|---------|
| 32 | softonic_com_site_structure_subdomains_ru_2026_03_05_22_48_04.csv | 30001 | site_structure | softonic.com | RU |
| 33 | softonic_com_top_pages_subdomains_all_act_2026_03_05_23_04_55.csv | 30029 | top_pages (actual) | softonic.com | ALL |
| 34 | softonic_com_top_pages_subdomains_all_com_2026_03_05_23_04_30.csv | 30050 | top_pages (comparison) | softonic.com | ALL |
| 35 | softonic_ru_site_structure_subdomains_ru_2026_03_05_22_40_52.csv | 30001 | site_structure | softonic.ru | RU |

| 36 | softonic_com_US_overview.png | DR 86, UR 19, Keywords ~20.8K, Traffic ~88.5K. Фильтр: Russian Federation |
| 37 | softonic_ru_RU_overview.png | DR 50, Keywords ~65.7K, Traffic ~335K. Фильтр: Russian Federation |

### malavida.com (3 CSV + 1 PNG)

| # | File | Rows | Report Type | Country |
|---|------|------|-------------|---------|
| 38 | malavida_com_site_structure_subdomains_ru_2026_03_05_22_46_42.csv | 30001 | site_structure | RU |
| 39 | malavida_com_top_pages_subdomains_all_act_2026_03_05_23_05_50.csv | 30001 | top_pages (actual) | ALL |
| 40 | malavida_com_top_pages_subdomains_all_com_2026_03_05_23_05_32.csv | 30001 | top_pages (comparison) | ALL |

| 41 | malavida_com_US_overview.png | DR ~87, Keywords ~54.1K, Traffic ~526K |

### filehippo.com (1 CSV + 1 PNG)

| # | File | Rows | Report Type | Country |
|---|------|------|-------------|---------|
| 42 | filehippo_com_site_structure_subdomains_ru_2026_03_05_22_49_10.csv | 30001 | site_structure | RU |

| 43 | filehippo_com_US_overview.png | DR 77, UR 37, Keywords ~1.3K, Traffic ~526 |

### trashbox.ru (1 CSV + 1 PNG)

| # | File | Rows | Report Type | Country |
|---|------|------|-------------|---------|
| 44 | trashbox_ru_site_structure_subdomains_ru_2026_03_05_22_44_22.csv | 30001 | site_structure | RU |

| 45 | trashbox_ru_US_overview.png | DR 54, Keywords 64.4K (-323K), Traffic 991K (-893K). Фильтр: Russian Federation |

### clubic.com (1 CSV + 1 PNG)

| # | File | Rows | Report Type | Country |
|---|------|------|-------------|---------|
| 46 | clubic_com_top_pages_subdomains_all_actua_2026_03_05_23_06_47.csv | 26609 | top_pages (actual) | ALL |

| 47 | clubic_com_US_overview.png | DR ~91, Keywords ~596, Traffic ~186. Фильтр: Russian Federation (очень мало) |

### 01net.com (1 CSV + 1 PNG)

| # | File | Rows | Report Type | Country |
|---|------|------|-------------|---------|
| 48 | 01net_com_top_pages_subdomains_all_actual_2026_03_05_23_06_59.csv | 28699 | top_pages (actual) | ALL |

| 49 | 01net_com_US_overview.png | DR 81, Keywords 141K (-925K), Traffic 1.5M (-2.2M). Фильтр: All locations. France 823K (56.5%) |

### commentcamarche.net (1 CSV + 1 PNG)

| # | File | Rows | Report Type | Country |
|---|------|------|-------------|---------|
| 50 | commentcamarche_net_top_pages_subdomains_al_2026_03_05_23_07_08.csv | 30001 | top_pages (actual) | ALL |

| 51 | ommentcamarche_net_overview.png | DR 80, Keywords 71.7K (-990K), Traffic 227K (-440K). Фильтр: All locations. France 178.4K (78.6%) |

ПРИМЕЧАНИЕ: В имени PNG-файла опечатка — отсутствует первая буква 'c' (должно быть commentcamarche, а записано ommentcamarche).

---

## Сводная статистика

| Метрика | Значение |
|---------|----------|
| Всего файлов | 51 |
| CSV-файлов | 36 |
| PNG-файлов | 15 |
| Всего строк в CSV | ~548,917 |
| CSV-файлов с 30K строк (максимум экспорта Ahrefs) | 16 |
| Кодировка CSV | UTF-16LE с BOM |
| Дублирующиеся пары CSV (frees0ft.fr) | 2 пары (4 файла) |

### Распределение CSV по размеру

| Диапазон | Кол-во | Файлы |
|----------|--------|-------|
| <100 строк | 5 | freesoft_net keywords_ru actual (139), freesoft_net keywords_us (149), freesoft_net top_pages_us (17), freesoft_net competitors RU (21), freesoft_net competitors US (21) |
| 100-1000 строк | 7 | frees0ft.fr keywords actual (733), perf RU (731), perf FR (731), top_pages_fr actual x2 (488), frees0ft_fr ru_compa (164), freesoft_net top_pages_ru actual (88) |
| 1K-10K строк | 6 | frees0ft.fr keywords comp (3967), frees0ft.fr top_pages compa x2 (1931), freesoft_net keywords_ru comp (2617), freesoft_ru top_pages actual (8439), freesoft_net top_pages_ru comp (1170) |
| 10K-30K строк | 4 | freesoft_ru keywords actual (17483), freesoft_ru top_pages comp (22248), clubic top_pages (26609), 01net top_pages (28699) |
| 30K строк (лимит) | 14 | freesoft_ru keywords comp, все site_structures (5), все competitor top_pages actual/comp для uptodown/softonic/malavida, commentcamarche top_pages, softonic_com top_pages x2 |

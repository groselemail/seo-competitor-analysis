# Отчёт по ревью архитектуры

## Сводка

**Общая оценка: Требуется существенная переработка**

Архитектура имеет продуманную фазовую структуру, но содержит 5 критических проблем, которые приведут к сбоям пайплайна: не обрабатывается кодировка UTF-16 в CSV, неверное количество файлов на задачу, задачи слишком большие для контекста, отсутствующие файлы в назначениях задач и отсутствие цепочки доказательств в брифах.

---

## Критические проблемы (блокируют запуск)

### Проблема 1: Кодировка UTF-16LE в CSV — пайплайн упадёт

- **Проблема:** ВСЕ CSV-файлы имеют кодировку UTF-16LE с BOM (byte order mark). Стандартные Unix-утилиты (`awk`, `sort`, `head`, `cut`, `wc -l`) выдадут мусор или ошибки на UTF-16 входе. Архитектура предполагает UTF-8-совместимые CSV.
- **Доказательство:** Вывод `head -1` показывает символы с широкими интервалами и BOM: `"\xef\xbf\xbd" U R L "` вместо `"URL"`.
- **Влияние:** Каждая задача Фазы 1 завершится ошибкой или выдаст некорректные данные. `wc -l` покажет неверное количество строк. Разбивка полей в `awk` не сработает.
- **Решение:** Добавить обязательный шаг конвертации в UTF-8. Варианты:
  - (A) Добавить задачу предобработки Фазы 0.5, которая конвертирует все CSV: `iconv -f UTF-16LE -t UTF-8 < input.csv | sed 's/\r$//' > input_utf8.csv`
  - (B) Включить конвертацию в каждый промпт Фазы 1 как первый шаг Bash.
  - Рекомендация: Вариант (A) — отдельная задача `00b-convert-encoding` после инвентаризации. Создаёт директорию `data_for_task_utf8/` с чистыми файлами. Все последующие задачи читают из `data_for_task_utf8/`.

### Проблема 2: Неверное количество файлов на задачу

- **Проблема:** Архитектура указывает неверное количество файлов для большинства задач. Это означает, что промпты будут ссылаться на неправильное число файлов, потенциально пропуская некоторые.
- **Доказательство:**
  - Задача 01 указывает «4 CSV», но у freesoft.net **8 CSV** (2 keywords RU + 1 keywords US + 3 top_pages + 2 competitors)
  - Задача 02 указывает «3 CSV», но у freesoft.ru **4 CSV** (2 keywords + 2 top_pages)
  - Задача 03 указывает «5 CSV», но у frees0ft.fr **9 CSV** (2 keywords + 4 top_pages + 1 ru_comparison + 2 performance_daily)
  - Задача 05 указывает «3 CSV», но у softonic **4 CSV** (softonic.com: 3 + softonic.ru: 1)
  - Задача 07 указывает «3 CSV», но у filehippo+trashbox только **2 CSV**
- **Влияние:** Задачи пропустят входные файлы, создавая неполные брифы.
- **Решение:** Пересчитать все файлы по задачам, используя data-inventory.md как источник истины. Обновить таблицу архитектуры.

### Проблема 3: Задачи слишком большие для контекста (>60K строк CSV)

- **Проблема:** Несколько задач пытаются обработать 60K-120K строк CSV за одну сессию. Даже с предобработкой в Bash это слишком много операций для одного агента.
- **Доказательство:**
  - Задача 04 (uptodown): 30K + 30K + 30K = **90K строк**
  - Задача 05 (softonic.com + softonic.ru): 30K + 30K + 30K + 30K = **120K строк**
  - Задача 06 (malavida): 30K + 30K + 30K = **90K строк**
  - Задача 08 (fr-market): 27K + 29K + 30K = **85K строк** + 3 PNG
  - Задача 02 (freesoft.ru): 17K + 30K + 8K + 22K = **77K строк**
- **Влияние:** Деградация контекста, пропуск данных, возможные ошибки «prompt too long». Агент может не уложиться в 150 ходов.
- **Решение:** Разделить тяжёлые задачи:
  - Задача 05 → 05a (softonic.com) + 05b (softonic.ru)
  - Задача 04 → 04a (uptodown site_structure) + 04b (uptodown top_pages)
  - Задача 06 → 06a (malavida site_structure) + 06b (malavida top_pages)
  - Задача 08 → 08a (clubic) + 08b (01net) + 08c (commentcamarche)
  - Задача 02 → 02a (freesoft.ru keywords) + 02b (freesoft.ru top_pages)

### Проблема 4: Отсутствующие файлы конкурентов в таблице архитектуры

- **Проблема:** Таблица «Входные данные» в архитектуре неполная и местами ошибочная.
- **Доказательство:**
  - `freesoft_net_orgcompetitors` (2 CSV) — указаны в заголовке таблицы, но не назначены ни на одну задачу
  - `frees0ft.fr-perf-subdomains_year2_daily` (2 CSV) — упомянуты как «performance daily», но не назначены
  - `frees0ft_fr_top_pages_subdomains_ru_compa` — вообще не упомянут (кросс-языковое сравнение)
  - Дублирующиеся CSV frees0ft.fr (4 файла с 2 временными метками) — не упомянуты
  - `ommentcamarche_net_overview.png` — архитектура указывает «Screenshot_1.png», но реальное имя файла другое (и содержит опечатку)
  - `organic_traff_loc_*.png` — 3 PNG для трафика по локациям, неоднозначно назначены
- **Влияние:** Потеря данных — важные файлы будут проигнорированы пайплайном.
- **Решение:** Создать явное сопоставление файл→задача в архитектуре. Каждый файл должен быть указан по имени.

### Проблема 5: Отсутствие цепочки доказательств в формате брифов

- **Проблема:** Примеры формата брифов содержат данные без ссылок на источники. Когда бриф указывает `traffic: 983000`, невозможно проверить, из какого файла/поля это значение получено.
- **Влияние:** Задача валидации (22-validate) не сможет реально проверить факты по источникам. Галлюцинированные числа пройдут валидацию.
- **Решение:** Каждая точка данных в брифах должна содержать источник:
  ```yaml
  total_organic_traffic:
    value: 983000
    source: "uptodown_com_US_overview.png"
    note: "Read from Ahrefs overview screenshot"
  ```

---

## Важные проблемы (не блокируют, но снижают качество)

### Проблема 6: Несоответствие MAX_PARALLEL

- **Проблема:** ARCHITECTURE.md указывает `MAX_PARALLEL=2`. REVIEW_PROMPT.md указывает `MAX_PARALLEL=3`. PRINCIPLES.md рекомендует Opus=2.
- **Влияние:** При запуске с 3 — ошибки rate limit. При запуске с 2 — архитектура уже это учитывает.
- **Решение:** Стандартизировать `MAX_PARALLEL=2` для модели Opus согласно PRINCIPLES.md.

### Проблема 7: Задача 02 (freesoft.ru) содержит 77K строк

- **Проблема:** freesoft.ru имеет наибольший датасет среди наших доменов: 17K keywords (актуальные) + 30K keywords (сравнение) + 8K top_pages (актуальные) + 22K top_pages (сравнение).
- **Влияние:** Обработка 77K строк одной задачей приведёт к снижению качества к концу.
- **Решение:** Разделить на 02a (keywords, 47K строк) и 02b (top_pages, 30K строк). Обе задачи создают суб-брифы, которые затем объединяются.

### Проблема 8: Задача 05 объединяет два отдельных домена

- **Проблема:** softonic.com и softonic.ru рассматриваются как одна сущность, но это отдельные домены с разным DR (86 vs 50), разным трафиком (88.5K vs 335K) и разным языковым фокусом.
- **Влияние:** Анализ смешает две различные стратегии.
- **Решение:** Разделить на 05a (softonic.com: 3 CSV + 1 PNG) и 05b (softonic.ru: 1 CSV + 1 PNG).

### Проблема 9: Дублирующиеся файлы frees0ft.fr

- **Проблема:** 4 CSV-файла frees0ft.fr встречаются парами с разными временными метками (23:03 и 23:11). Одинаковое количество строк предполагает дубликаты.
  - `frees0ft_fr_top_pages...fr_actua...23_03_45.csv` (488) и `...23_11_08.csv` (488)
  - `frees0ft_fr_top_pages...fr_compa...23_03_29.csv` (1931) и `...23_11_22.csv` (1931)
- **Влияние:** Если это действительно дубликаты — впустую потраченные ресурсы. Если разные снапшоты — оба должны быть проанализированы.
- **Решение:** Фаза 0 (инвентаризация) должна сравнить эти файлы. Если идентичны — пометить один как «skip». Если различаются — отметить временные метки.

### Проблема 10: Нет валидации между Фазой 1 и Фазой 2

- **Проблема:** Если бриф Фазы 1 имеет неверный формат или пуст, задачи Фазы 2 молча выдадут неправильный анализ.
- **Влияние:** Распространение ошибок по принципу «мусор на входе — мусор на выходе».
- **Решение:** Добавить задачу `10-validate-briefs` между Фазой 1 и Фазой 2. Проверки: все брифы существуют, не пусты, валидный YAML, содержат обязательные поля. Быстрая задача (~30 ходов).

### Проблема 11: Задача 14 Фазы 2 читает 4 брифа включая минорных конкурентов

- **Проблема:** Задача 14 (структуры доменов) читает брифы 04 + 05 + 06 + 07. Если после разделения их станет 8, это большой объём входных данных.
- **Влияние:** Умеренное давление на контекст, но брифы сжатые, поэтому скорее всего OK.
- **Решение:** Оставить как есть, но убедиться, что каждый бриф не превышает 300 строк YAML.

### Проблема 12: Скриншот обзора freesoft.net показывает фильтр RU

- **Проблема:** freesoft_net_main_overiew.png показывает фильтр «Russian Federation». freesoft.net — англоязычный домен — RU-трафик составляет всего 89 в месяц. Данные по US-фильтру отсутствуют в PNG.
- **Влияние:** Задача 01 увидит обманчиво низкие показатели трафика для freesoft.net.
- **Решение:** Указать в промпте, что этот PNG показывает данные с RU-фильтром. Реальные данные по US-трафику находятся в `organic_traff_loc_US.png` (India 14.2K, US 2.1K — всего ~34.6K). Явно упомянуть это расхождение.

---

## Минорные проблемы (желательно исправить)

### Проблема 13: Опечатка в имени файла — ommentcamarche

- **Проблема:** В `ommentcamarche_net_overview.png` пропущена начальная буква 'c'. Архитектура ссылается на «Screenshot_1.png».
- **Решение:** Использовать реальное имя файла в промптах. Рассмотреть переименование файла.

### Проблема 14: Пропуски в нумерации архитектуры (15, 19)

- **Проблема:** Номера задач перескакивают с 14 на 16 (Фаза 3) и с 18 на 20 (Фаза 4). Номера 15 и 19 не используются.
- **Влияние:** Косметическая проблема, но вносит путаницу. Следует зарезервировать для разделённых задач или явно указать, что они намеренно пропущены.
- **Решение:** Использовать 15 для задачи валидации брифов. Или перенумеровать.

### Проблема 15: Фазовый пайплайн vs цепочечный

- **Проблема:** Архитектура объявляет «Level 2 — Phased Pipeline», но также определяет CHAINS в конфигурации run.sh. Это гибрид, который не соответствует ни одному паттерну чисто.
- **Влияние:** Определение CHAINS предполагает цепочечное выполнение, но фактический граф зависимостей — фазовый (Фаза 1 полностью завершается перед Фазой 2).
- **Решение:** Уточнить: это ФАЗОВЫЙ пайплайн. Цепочки в конфигурации используются только для отслеживания зависимостей Фаза 1→2, а не для сквозных цепочек. Обновить описание.

### Проблема 16: Нет мета-промптов для 19+ промптов

- **Проблема:** Пайплайн содержит 19 задач = 19 промптов. META_PROMPTS.md рекомендует мета-промпты для 15+ задач, чтобы избежать деградации контекста при написании промптов.
- **Решение:** Использовать 4 мета-промпта: meta-phase1 (8 промптов), meta-phase2 (4), meta-phase3 (3), meta-phase4-5 (4).

---

## Матрица покрытия данных

| # | Файл | Назначенная задача |
|---|------|--------------|
| 1 | freesoft_net_organic_keywords...us.csv | 01-parse-freesoft-net |
| 2 | freesoft_net_organic_keywords...ru_22_29_58.csv | 01-parse-freesoft-net |
| 3 | freesoft_net_organic_keywords...ru_22_30_14.csv | 01-parse-freesoft-net |
| 4 | freesoft_net_top_pages...us_comp.csv | 01-parse-freesoft-net |
| 5 | freesoft_net_top_pages...ru_comp.csv | 01-parse-freesoft-net |
| 6 | freesoft_net_top_pages...ru_actu.csv | 01-parse-freesoft-net |
| 7 | freesoft_net_orgcompetitors...ru.csv | 01-parse-freesoft-net |
| 8 | freesoft_net_orgcompetitors...us.csv | 01-parse-freesoft-net |
| 9 | freesoft_net_main_overiew.png | 01-parse-freesoft-net |
| 10 | organic_traff_loc_US.png | 01-parse-freesoft-net |
| 11 | freesoft_ru_organic_keywords...22_26_41.csv | 02a-parse-freesoft-ru-keywords |
| 12 | freesoft_ru_organic_keywords...22_27_20.csv | 02a-parse-freesoft-ru-keywords |
| 13 | freesoft_ru_top_pages...actual.csv | 02b-parse-freesoft-ru-pages |
| 14 | freesoft_ru_top_pages...compa.csv | 02b-parse-freesoft-ru-pages |
| 15 | freesoft_RU_main_overiew.png | 02a-parse-freesoft-ru-keywords |
| 16 | organic_traff_loc_RU.png | 02a-parse-freesoft-ru-keywords |
| 17 | frees0ft_fr_organic_keywords...22_20_26.csv | 03-parse-freesoft-fr |
| 18 | frees0ft_fr_organic_keywords...22_21_09.csv | 03-parse-freesoft-fr |
| 19 | frees0ft_fr_top_pages...actual...23_03_45.csv | 03-parse-freesoft-fr |
| 20 | frees0ft_fr_top_pages...actual...23_11_08.csv | 03-parse-freesoft-fr |
| 21 | frees0ft_fr_top_pages...compa...23_03_29.csv | 03-parse-freesoft-fr |
| 22 | frees0ft_fr_top_pages...compa...23_11_22.csv | 03-parse-freesoft-fr |
| 23 | frees0ft_fr_top_pages...ru_compa.csv | 03-parse-freesoft-fr |
| 24 | frees0ft.fr-perf...22-22-53.csv (RU) | 03-parse-freesoft-fr |
| 25 | frees0ft.fr-perf...23-03-23.csv (FR) | 03-parse-freesoft-fr |
| 26 | freesoft_FR_main_overiew.png | 03-parse-freesoft-fr |
| 27 | organic_traff_loc_FR.png | 03-parse-freesoft-fr |
| 28 | uptodown_com_site_structure.csv | 04a-parse-uptodown-structure |
| 29 | uptodown_com_top_pages...actual.csv | 04b-parse-uptodown-pages |
| 30 | uptodown_com_top_pages...comp.csv | 04b-parse-uptodown-pages |
| 31 | uptodown_com_US_overview.png | 04a-parse-uptodown-structure |
| 32 | softonic_com_site_structure.csv | 05a-parse-softonic-com |
| 33 | softonic_com_top_pages...actual.csv | 05a-parse-softonic-com |
| 34 | softonic_com_top_pages...comp.csv | 05a-parse-softonic-com |
| 35 | softonic_ru_site_structure.csv | 05b-parse-softonic-ru |
| 36 | softonic_com_US_overview.png | 05a-parse-softonic-com |
| 37 | softonic_ru_RU_overview.png | 05b-parse-softonic-ru |
| 38 | malavida_com_site_structure.csv | 06a-parse-malavida-structure |
| 39 | malavida_com_top_pages...actual.csv | 06b-parse-malavida-pages |
| 40 | malavida_com_top_pages...comp.csv | 06b-parse-malavida-pages |
| 41 | malavida_com_US_overview.png | 06a-parse-malavida-structure |
| 42 | filehippo_com_site_structure.csv | 07a-parse-filehippo |
| 43 | filehippo_com_US_overview.png | 07a-parse-filehippo |
| 44 | trashbox_ru_site_structure.csv | 07b-parse-trashbox |
| 45 | trashbox_ru_US_overview.png | 07b-parse-trashbox |
| 46 | clubic_com_top_pages.csv | 08a-parse-clubic |
| 47 | clubic_com_US_overview.png | 08a-parse-clubic |
| 48 | 01net_com_top_pages.csv | 08b-parse-01net |
| 49 | 01net_com_US_overview.png | 08b-parse-01net |
| 50 | commentcamarche_net_top_pages.csv | 08c-parse-commentcamarche |
| 51 | ommentcamarche_net_overview.png | 08c-parse-commentcamarche |

**Покрытие: 51/51 файлов сопоставлено.**

---

## Оценка бюджета контекста (после предложенных разделений)

| Задача | Строк CSV | PNG | Брифов на чтение | Уровень риска | Примечания |
|------|----------|------|-------------|------------|-------|
| 00-inventory | 0 (только head) | 15 | 0 | MEDIUM | 15 PNG — много; рассмотреть разбивку на подгруппы |
| 00b-convert-encoding | 0 | 0 | 0 | LOW | Чистый Bash: цикл iconv |
| 01-parse-freesoft-net | ~4,222 | 2 | 0 | LOW | Небольшие CSV, управляемый объём |
| 02a-parse-freesoft-ru-kw | ~47,484 | 2 | 0 | HIGH | 30K CSV сравнения; ОБЯЗАТЕЛЬНО использовать предобработку Bash |
| 02b-parse-freesoft-ru-pages | ~30,687 | 0 | 0 | HIGH | 22K CSV сравнения; ОБЯЗАТЕЛЬНО использовать Bash |
| 03-parse-freesoft-fr | ~11,163 | 2 | 0 | MEDIUM | Много мелких файлов; дубликаты завышают счёт |
| 04a-parse-uptodown-structure | ~30,001 | 1 | 0 | HIGH | Один CSV на 30K; Bash для извлечения языков |
| 04b-parse-uptodown-pages | ~60,046 | 0 | 0 | HIGH | Два CSV по 30K; ОБЯЗАТЕЛЬНО использовать Bash |
| 05a-parse-softonic-com | ~90,080 | 1 | 0 | CRITICAL | Три CSV по 30K; разделить ещё или агрессивный Bash |
| 05b-parse-softonic-ru | ~30,001 | 1 | 0 | HIGH | Один CSV на 30K |
| 06a-parse-malavida-structure | ~30,001 | 1 | 0 | HIGH | Один CSV на 30K |
| 06b-parse-malavida-pages | ~60,002 | 0 | 0 | HIGH | Два CSV по 30K |
| 07a-parse-filehippo | ~30,001 | 1 | 0 | HIGH | Один CSV на 30K |
| 07b-parse-trashbox | ~30,001 | 1 | 0 | HIGH | Один CSV на 30K |
| 08a-parse-clubic | ~26,609 | 1 | 0 | HIGH | Почти 30K CSV |
| 08b-parse-01net | ~28,699 | 1 | 0 | HIGH | Почти 30K CSV |
| 08c-parse-commentcamarche | ~30,001 | 1 | 0 | HIGH | 30K CSV |
| 10-validate-briefs | 0 | 0 | ~15 | LOW | Быстрая валидация YAML |
| 11-analyze-our-domains | 0 | 0 | 3 | LOW | Только брифы |
| 12-analyze-multilingual | 0 | 0 | 4 | LOW | Только брифы |
| 13-analyze-fr-market | 0 | 0 | 4 | LOW | Только брифы |
| 14-analyze-domain-structures | 0 | 0 | 5 | LOW | Только брифы |
| 16-language-potential | 0 | 0 | 3 | LOW | Только брифы |
| 17-domain-strategy | 0 | 0 | 2 | LOW | Только брифы |
| 18-roadmap-draft | 0 | 0 | 2 | LOW | Только брифы |
| 20-report-domain-strategy | 0 | 0 | 4 | LOW | Только брифы |
| 21-report-multilingual-roadmap | 0 | 0 | 6 | MEDIUM | Наибольшее число брифов; следить за размером |
| 22-validate | 0 | 0 | ~10+2 документа | MEDIUM | Все брифы + 2 финальных документа |

---

## Рекомендации

1. **Добавить задачу конвертации кодировки (00b)** как первый приоритет. Без этого весь пайплайн неработоспособен.

2. **Разделить тяжёлые задачи Фазы 1** как описано в Проблеме 3. Это увеличивает количество задач с 19 до ~28, но кардинально повышает надёжность.

3. **Добавить цепочку доказательств в формат брифов.** Каждое числовое значение должно содержать ссылку на `source_file` и `extraction_method` (команда Bash или визуальное чтение PNG).

4. **Добавить задачу валидации брифов Фазы 1.5 (10-validate-briefs).** Быстрая проверка YAML-схемы перед началом Фазы 2.

5. **Исправить все количества файлов и создать явное сопоставление файл→задача** в архитектуре. Больше никаких «4 CSV» — указывать реальные имена файлов.

6. **Стандартизировать MAX_PARALLEL=2** для модели Opus. Обновить все упоминания.

7. **Использовать мета-промпты** для генерации 28 файлов промптов (4 мета-промпта, по одному на фазу).

8. **Обработать дублирующиеся файлы frees0ft.fr** — задача инвентаризации должна обнаруживать и помечать дубликаты.

9. **Задача 05a (softonic.com) по-прежнему содержит 90K строк** даже после разделения. Рассмотреть дальнейшее разделение на 05a-structure (30K) и 05a-pages (60K), или использовать агрессивное сокращение через Bash (только top-100 страниц).

10. **Указать ограничение PNG обзора freesoft.net** — он показывает RU-фильтр с трафиком=89, что нерепрезентативно. Данные по US-трафику есть только в organic_traff_loc_US.png.

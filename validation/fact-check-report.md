# Independent Fact-Check Report — QA Audit

> Auditor: Independent QA (Claude Opus 4.6)
> Date: 2026-03-06
> Scope: 3 reports × 7 briefs × 40+ CSV files
> Methodology: Three-level verification (Reports→Briefs→CSV)

---

## Сводка (Executive Summary)

| Метрика | Результат |
|---------|-----------|
| Проверено утверждений | ~220 |
| VERIFIED (отчёт = бриф) | ~195 |
| MINOR (округление, ±1%) | 7 |
| NOT_IN_AHREFS (красная зона) | **8** |
| INFERENCE (моделирование, не данные) | **26+** |
| CSV MISMATCH (бриф ≠ CSV) | **4** |
| FABRICATION | **0** прямых выдумок |

### Вердикт: CONDITIONAL PASS

Числовые данные из Ahrefs корректно переносятся по цепочке CSV → briefs → reports. Однако существуют **8 утверждений** в красной зоне (hreflang, технические детали), которые не могут быть получены из Ahrefs, и **4 расхождения** между briefs и CSV. Также **26+ утверждений** являются моделированием/проекцией, а не фактами из данных — они должны быть явно маркированы как таковые.

---

## 1. Критические находки (Critical Findings)

### CF-1: hreflang — все утверждения вне зоны Ahrefs

**Где:** domain-strategy.md:69, executive-summary.md:30, multilingual-roadmap.md:514

**Утверждение:** "hreflang реализован частично. Между тремя доменами настроены hreflang-теги (x-default → freesoft.ru, fr → frees0ft.fr, en → freesoft.net)"

**Проблема:**
- Brief 14 (domain-structures.yaml) ЯВНО указывает: *"Ahrefs data does not include hreflang information"*
- Отчёт сам признаёт: *"данные Ahrefs не содержат информации о hreflang-разметке"* (domain-strategy.md:69)
- НО затем делает конкретные утверждения о реализации hreflang (какие теги, какие маппинги)
- Источник этих утверждений **НЕИЗВЕСТЕН** — не Ahrefs, не CSV, не briefs

**Масштаб проблемы:**
- domain-strategy.md: линии 69, 181, 192, 215, 284, 331-349 (XML пример)
- executive-summary.md: линия 30
- multilingual-roadmap.md: линии 155, 189, 232, 344, 424, 430, 514

**Оценка:** НЕ фабрикация (утверждение может быть верным), но **НЕ ВЕРИФИЦИРУЕМО** из данных пайплайна. Это та же категория проблемы, что и ранее найденная "отсутствие hreflang" — утверждение о hreflang не имеет источника в данных Ahrefs.

**Рекомендация:** Все hreflang-утверждения должны быть маркированы как `[требует ручной верификации — не из Ahrefs]`. Либо провести ручной аудит сайта и зафиксировать источник.

---

### CF-2: Validation-report.md — неполный scope + самореференция

**Где:** executive-summary.md:102

**Утверждение:** "~180 числовых утверждений проверены против первичных источников (briefs Ahrefs). Результат: PASS"

**Проблема:**
1. validation-report.md проверяет **только 2 отчёта** (domain-strategy.md + multilingual-roadmap.md), но **НЕ executive-summary.md**
2. validation-report.md проверяет **только Level 1** (отчёт vs briefs), но **НЕ проверяет:**
   - briefs vs CSV (Level 2)
   - технические/нефактуальные утверждения (Level 3)
   - hreflang-утверждения (красная зона)
3. executive-summary.md ссылается на validation-report как доказательство своей верифицированности — **самореференция** (validation-report не проверял executive-summary)

**Рекомендация:** Уточнить scope: "~180 утверждений в 2 отчётах проверены против briefs (Level 1). CSV-верификация и технический аудит не проводились."

---

## 2. CSV Spot-Check Results (Level 2)

### Методология

Проверены 14 ключевых цифр из briefs напрямую против CSV-файлов в `pipeline-seo/data_utf8/`. CSV-файлы — прямой экспорт из Ahrefs.

**Важное ограничение:** Некоторые CSV ограничены 30,000 строк (Ahrefs cap). Трафик в top_pages CSV = сумма по страницам, а не overview-метрика Ahrefs. Site_structure CSV = RU-фильтр для конкурентов.

### Таблица верификации

| # | Показатель | Brief значение | CSV значение | CSV файл | Результат | Комментарий |
|---|-----------|---------------|-------------|----------|-----------|-------------|
| 1 | freesoft.ru трафик | 168,000 | 160,642 (sum top_pages) | freesoft_ru_top_pages_ru_actua | ОБЪЯСНИМО | Brief = Ahrefs overview; CSV = сумма страниц (8,438 стр., без cap). Разница 4.4% — стандартное расхождение overview vs page sum |
| 2 | freesoft.net трафик | 32,252 | 98 (sum top_pages) | freesoft_net_top_pages_ru_actu | N/A | CSV = RU-фильтр; brief = ALL locations. .net трафик из India (41%), нет в RU-CSV |
| 3 | frees0ft.fr трафик | 21,575 | 14,013 (sum top_pages) | frees0ft_fr_top_pages_fr_actua | N/A | CSV = FR-фильтр; brief = ALL locations. Разница = трафик из Senegal/Cameroon (не в FR-CSV) |
| 4 | **trashbox.ru трафик** | **991,000** | **1,009,540** (site_structure root) | trashbox_ru_site_structure_ru | **MISMATCH** | Расхождение 18,540 (+1.9%). Brief 14 использует округлённое значение или другой Ahrefs отчёт |
| 5 | uptodown.com поддомены | 12,735 | 12,735 | uptodown_com_site_structure_ru | **✓ MATCH** | Точное совпадение |
| 6 | uptodown трафик >100 | 936 | 936 | uptodown_com_site_structure_ru | **✓ MATCH** | Точное совпадение |
| 7 | softonic.ru поддомены | 15,014 | 15,014 | softonic_ru_site_structure_ru | **✓ MATCH** | Точное совпадение |
| 8 | **softonic.ru трафик >100** | **568** | **378** | softonic_ru_site_structure_ru | **MISMATCH** | Расхождение 190 (33.4%). Brief 14 → brief 05a → возможно другой Ahrefs snapshot |
| 9 | **malavida.com поддомены** | **9,880** | **8,891** | malavida_com_site_structure_ru | **MISMATCH** | Расхождение 989 (10.0%). Brief 14 → brief 06a; CSV = RU filter, возможно brief использует ALL |
| 10 | **malavida трафик >100** | **1,014** | **620** | malavida_com_site_structure_ru | **MISMATCH** | Расхождение 394 (38.9%). Значительное — требует исследования |
| 11 | uptodown ALL трафик | ~30.4M (brief 12) | 31,008,012 (30K cap) | uptodown_com_top_pages_all_act | CONSISTENT | CSV capped at 30K rows; sum close to brief |
| 12 | softonic.com ALL трафик | ~38.4M (brief 12) | 38,889,564 (30K cap) | softonic_com_top_pages_all_act | CONSISTENT | Close match |
| 13 | malavida ALL трафик | ~6.5M (brief 12) | 6,510,998 (30K cap) | malavida_com_top_pages_all_act | **✓ MATCH** | Very close match |
| 14 | freesoft.ru тренд | +36,431 (brief 11) | +22,063 (comparison CSV sum) | freesoft_ru_top_pages_ru_compa | ОБЪЯСНИМО | Comparison CSV = сумма по отдельным страницам; brief = overview net change (включает новые страницы) |

### Итог CSV-проверки

- **3 точных совпадения** (#5, #6, #7)
- **4 MISMATCH** (#4, #8, #9, #10) — все связаны с site_structure данными
- **4 объяснимых расхождения** — разница overview vs page sum, или разные location-фильтры
- **3 consistent** — совпадают в пределах погрешности export cap

**Гипотеза о причине MISMATCH #8-#10:** Briefs 14 → 05a/06a были обработаны из Ahrefs-экспортов с другой даты или другим фильтром (ALL vs RU). CSV-файлы в `data_utf8/` имеют дату 2026-03-05, а source briefs (04a, 05a, 06a) могли обрабатывать более ранние экспорты. **Это не фабрикация, но data provenance gap.**

**Рекомендация:** Зафиксировать точные даты/фильтры Ahrefs-экспортов для каждого brief. Расхождения #8–#10 между brief 14 и CSV нужно расследовать.

---

## 3. Inference/Projection Registry (Level 3)

Следующие утверждения в отчётах являются **моделированием, проекциями или экспертными оценками**, а НЕ фактами из данных Ahrefs. Все они присутствуют в briefs (17, 18), поэтому цепочка report→brief корректна, но читатель может ошибочно воспринять их как данные.

### 3.1. Бюджет и стоимость (RED ZONE)

| Утверждение | Отчёт | Линия | Brief | Категория |
|-------------|-------|-------|-------|-----------|
| $15–27K на язык | domain-strategy.md, multilingual-roadmap.md, executive-summary.md | 76, 394, 76 | 18 | INFERENCE — модель стоимости |
| $75–135K итого | executive-summary.md, multilingual-roadmap.md | 76, 457 | 18 | INFERENCE — 5 × $15-27K |
| ~9,000 новых страниц | executive-summary.md, multilingual-roadmap.md | 76, 385 | 18 | INFERENCE — план |
| $10K–15K за топ-100 стр. | multilingual-roadmap.md | 391 | 18 | INFERENCE — оценка |
| $5K–10K за топ-1000 стр. | multilingual-roadmap.md | 392 | 18 | INFERENCE — оценка |
| $500–2K API-перевод | multilingual-roadmap.md | 393 | 18 | INFERENCE — оценка |

### 3.2. Таймлайны и сроки

| Утверждение | Brief | Категория |
|-------------|-------|-----------|
| Все длительности фаз (1–3 мес., 3–6 мес., 6–12 мес., 12–18 мес.) | 17, 18 | INFERENCE — план проекта |
| Сроки вариантов стратегии (2–3 мес. до 8–12 мес.) | 17 | INFERENCE — экспертная оценка |
| "3–6 месяцев восстановления" после миграции | 17 | INFERENCE — industry rule of thumb |

### 3.3. Миграционные риски

| Утверждение | Отчёт | Линия | Brief | Категория |
|-------------|-------|-------|-------|-----------|
| "20–40% потери трафика на 3–6 месяцев" | domain-strategy.md | 150, 170 | 17 | INFERENCE — industry rule of thumb, не из Ahrefs |
| "33K–67K визитов под угрозой" | domain-strategy.md | 150, 264 | 17 | INFERENCE — 20-40% от 168K |
| "Даже при потере 50% = -11K, восстановимо" | domain-strategy.md | 268 | 17 | INFERENCE |

### 3.4. TAM/SAM/Achievable модель

Все TAM/SAM/Achievable цифры (brief 16) — это **моделирование на основе данных Ahrefs**, а не прямые данные:

- TAM = сумма трафика конкурентов по языку из brief 12 → **VERIFIED** (это данные)
- SAM = TAM × 0.9 → **INFERENCE** (коэффициент 90% — экспертная оценка)
- Achievable = SAM × capture rate (0.4%–3.0%) → **INFERENCE** (capture rates — экспертная оценка)
- Capture rates не обоснованы данными — почему 1.5% для ES, но 3.0% для AR?

**Вердикт:** TAM цифры верифицированы (это суммы из brief 12 = суммы из CSV). SAM и Achievable — моделирование.

### 3.5. Технические утверждения без источника в данных

| Утверждение | Категория |
|-------------|-----------|
| Яндекс предпочитает .ru ccTLD | INFERENCE — общее SEO-знание |
| "Тройные затраты на поддержку" (3 домена) | INFERENCE — техническое допущение |
| ".ru ccTLD серьёзно препятствует международному таргетингу" | INFERENCE — SEO best practice |
| "Google sandbox эффект" для новых субдоменов | INFERENCE — спорное SEO-мнение |
| "Screaming Frog / Sitebulb для hreflang-аудита" | INFERENCE — рекомендация инструмента |
| Content pipeline подход (LLM + human review) | INFERENCE — рекомендация процесса |

### 3.6. KPI-таргеты

ВСЕ целевые значения (brief 18) — проекции:

| KPI | Значение | Категория |
|-----|----------|-----------|
| EN 37,000 за 3 мес. | INFERENCE — проекция |
| RU 178,000 за 3 мес. | INFERENCE — проекция |
| FR 25,000 за 3 мес. | INFERENCE — проекция |
| ES 15,000 за 6 мес. | INFERENCE — проекция |
| AR 10,000 за 6 мес. | INFERENCE — проекция |
| DR 58+ за 12 мес. | INFERENCE — проекция |
| 500,000 общий за 12 мес. | INFERENCE — проекция |
| 700,000+ за 18 мес. | INFERENCE — проекция |

### 3.7. Интерпретация конкурентных стратегий

| Утверждение | Категория |
|-------------|-----------|
| "softonic.ru в спаде из-за стагнации контента, а не структуры" | INFERENCE — причинно-следственная интерпретация |
| "trashbox показывает риски монолингвальной модели" | INFERENCE — корреляция ≠ причинность |
| "filehippo провалился из-за низкого качества локализации" | INFERENCE — причина не подтверждена данными |
| "Все конкуренты используют поддомены → поддомены = правильный подход" | INFERENCE — survival bias |

---

## 4. Level 1: Full Verification Tables

### 4.1. executive-summary.md (lines 1–105)

| # | Утверждение | Отчёт | Brief | Статус |
|---|-------------|-------|-------|--------|
| 1 | freesoft.ru DR 59 | 16 | 11 | VERIFIED |
| 2 | freesoft.ru трафик 168,000 | 16 | 11 | VERIFIED |
| 3 | freesoft.ru доля 75.7% | 16 | 11 | VERIFIED |
| 4 | freesoft.net DR 51 | 17 | 11 | VERIFIED |
| 5 | freesoft.net трафик ~32,252 | 17 | 11 | VERIFIED |
| 6 | freesoft.net доля 14.5% | 17 | 11 | VERIFIED |
| 7 | frees0ft.fr DR 23 | 18 | 11 | VERIFIED |
| 8 | frees0ft.fr трафик ~21,575 | 18 | 11 | VERIFIED |
| 9 | frees0ft.fr доля 9.7% | 18 | 11 | VERIFIED |
| 10 | Итого ~222,000 | 19 | 11 (221,827) | VERIFIED |
| 11 | trashbox.ru −893K (−47%) | 25 | 14 | VERIFIED |
| 12 | softonic.ru −578K | 25 | 14 | VERIFIED |
| 13 | 24 followed RD (frees0ft.fr) | 29 | 11 | VERIFIED |
| 14 | **hreflang реализован** | **30** | **14 (корр.)** | **NOT_IN_AHREFS** |
| 15 | 75.2 млн на 17+ языках | 34 | 12 | VERIFIED |
| 16 | softonic 9 языков, DR 86 | 38 | 14 | VERIFIED |
| 17 | uptodown 14 языков | 39 | 14 | VERIFIED |
| 18 | malavida 14 языков, DR 73 | 40 | 14 | VERIFIED |
| 19 | ~660K дополнительного трафика | 44 | 16 | VERIFIED (model output) |
| 20 | ES TAM 9.9M, захват 134K | 45 | 16 | VERIFIED (TAM) / INFERENCE (захват) |
| 21 | EN TAM 45.7M, рост +132K | 46 | 16 | VERIFIED (TAM) / INFERENCE (рост) |
| 22 | AR TAM 3.5M, 1 конкурент, 93.5K | 47 | 12, 16 | VERIFIED (TAM+конкурент) / INFERENCE (93.5K) |
| 23 | Вариант D гибрид | 53 | 17 | VERIFIED |
| 24 | 2.3–4.0× рост | 72 | 17 | INFERENCE |
| 25 | 500K–880K | 72 | 17, 16 | INFERENCE |
| 26 | $15–27K на язык | 76 | 18 | INFERENCE |
| 27 | $75–135K на 5 языков | 76 | 18 | INFERENCE |
| 28 | ~9,000 новых страниц | 76 | 18 | INFERENCE |
| 29 | ~180 утверждений проверены, PASS | 102 | validation-report.md | VERIFIED (но scope неполный — см. CF-2) |

### 4.2. domain-strategy.md

Полная верификация ~120 утверждений выполнена validation-report.md (Task 22). Мой аудит подтверждает:

- **Все числовые утверждения из Ahrefs** (DR, трафик, ключевые слова, бэклинки, доли стран, тренды) корректно переносятся из brief 11 и brief 14.
- **5 minor issues** зафиксированы validation-report.md (округления):
  - M1: 75.6% vs 75.7% (оба корректны)
  - M2: EN +132,748 vs +132,245 (ошибка округления промежуточного значения)
  - M3: "60% реализации" = на самом деле 56.7%
  - M4/M5: таймлайны фаз различаются между отчётами (разные source briefs)

**Дополнительные находки моего аудита (не в validation-report):**

| Линия | Утверждение | Статус |
|-------|-------------|--------|
| 69 | "hreflang реализован частично" + детали маппинга | NOT_IN_AHREFS (см. CF-1) |
| 101 | "Яндекс... локальные сигналы доверия" | INFERENCE (общее SEO-знание) |
| 150 | "20–40% потери при миграции" | INFERENCE (industry rule of thumb) |
| 75 | "Тройные затраты на поддержку" | INFERENCE (техническое допущение) |
| 109 | filehippo провалился из-за качества локализации | INFERENCE (причина не подтверждена) |
| 339–349 | XML sitemap пример кода | CONSTRUCTED (иллюстрация, не из данных) |
| 401 | "500K = 60% оценок" (на самом деле 56.7%) | MINOR — неточное округление |

### 4.3. multilingual-roadmap.md

Полная верификация ~60 числовых утверждений по TAM/SAM/Achievable подтверждена validation-report.md. Все TAM значения точно совпадают с brief 16. Все KPI, бюджеты, abort criteria точно совпадают с brief 18.

**Дополнительные находки:**

| Линия | Утверждение | Статус |
|-------|-------------|--------|
| 134 | "uptodown (17 языков)" | **DISCREPANCY** — brief 12 = 17, brief 14 = 14 (RU filter). Тот же отчёт на линии 119 показывает данные только по ~11 языкам |
| 134 | "softonic (7 языков)" | **DISCREPANCY** — brief 12 = 7 (measurable), brief 14 = 9 (all). Отчёт использует оба числа в разных местах |
| 134 | "malavida (8–14 языков)" | OK — отчёт корректно указывает диапазон |
| 514 | "Кросс-доменный hreflang через XML sitemaps" | NOT_IN_AHREFS — рекомендация, не данные |
| 469 | "LLM-перевод (выше качество, чем NMT)" | INFERENCE — спорное утверждение |

---

## 5. NOT_IN_AHREFS Complete List

Все утверждения, которые НЕВОЗМОЖНО получить из данных Ahrefs:

| # | Утверждение | Отчёт(ы) | Brief(ы) | Источник |
|---|-------------|----------|----------|----------|
| 1 | hreflang реализован между доменами | domain-strategy, executive-summary | 14, 17 | НЕИЗВЕСТЕН — ручная проверка сайта? |
| 2 | x-default → freesoft.ru | domain-strategy | 17 | НЕИЗВЕСТЕН |
| 3 | hreflang fr → frees0ft.fr | domain-strategy | 17 | НЕИЗВЕСТЕН |
| 4 | hreflang en → freesoft.net | domain-strategy | 17 | НЕИЗВЕСТЕН |
| 5 | XML sitemap = надёжнейший метод hreflang | domain-strategy, multilingual-roadmap | 17, 18 | SEO best practice (не Ahrefs) |
| 6 | Написание frees0ft (ноль вместо «o») — проблема доверия | domain-strategy | 17 | Человеческое наблюдение (не Ahrefs) |
| 7 | frees0ft.fr трафик 90% от одной страницы | domain-strategy, multilingual-roadmap | 11, 13 | Возможно из CSV (нужно верифицировать top_pages) |
| 8 | Кросс-доменный hreflang сложнее одно-доменного | domain-strategy | 17 | SEO-знание (не Ahrefs) |

**Примечание к #7:** Проверка frees0ft.fr top_pages CSV подтверждает: null's brawl pages = 10,854 + 1,108 = 11,962 из 14,013 FR-трафика = **85.3%** (не 90%). Утверждение "90%" — приближение, слегка завышено.

---

## 6. Language Count Discrepancies

Количество языков конкурентов варьируется в зависимости от source brief и метода подсчёта:

| Конкурент | Brief 12 (ALL locations, >0 traffic) | Brief 14 (RU filter, all subdomains) | CSV RU-filter (unique lang codes >10 entries) | Используется в отчётах |
|-----------|--------------------------------------|--------------------------------------|-----------------------------------------------|----------------------|
| uptodown | 17 | 14 | ~11 (ru, en, ar, br, tr, fr, cn, kr, vi, th, it) | 14 (domain-strategy), 17 (multilingual-roadmap:134) |
| softonic.com | 7 (measurable) | 9 (incl. zero-traffic) | ~5 (en, fr, de, it, vi) | 9 (domain-strategy), 7 (multilingual-roadmap:134) |
| malavida | 8 (with traffic >0) | 14 (all subdomains) | ~13 (ru, fr, en, it, de, ro, jp, nl, br, dk, se, pl, pt) | 14 (domain-strategy), 8-14 (multilingual-roadmap) |

**Проблема:** Отчёты используют разные числа для одних и тех же конкурентов без объяснения почему. Читатель видит "softonic — 9 языков" в одном месте и "softonic — 7 языков" в другом.

**Рекомендация:** Унифицировать и добавить сноску: "N языков (из них M с измеримым трафиком)".

---

## 7. Minor Issues Registry

| # | Отчёт | Линия | Описание | Severity |
|---|-------|-------|----------|----------|
| M1 | domain-strategy.md | 10 vs 59 | Portfolio share: 75.6% (text) vs 75.7% (table). Both = valid roundings of 75.74% | Minor |
| M2 | domain-strategy.md | 389 | EN growth +132,748 vs brief 16 +132,245. Rounding of intermediate 165,000 | Minor |
| M3 | domain-strategy.md | 401 | "60% реализации" = actually 56.7% (500K/882K). Brief 17 uses same "~60%" | Minor |
| M4 | Both reports | phases | domain-strategy: Phase 1 M1-2, Phase 2 M2-4. Roadmap: Phase 1 M1-3, Phase 2 M3-6. Different source briefs (17 vs 18) | Minor |
| M5 | Both reports | Phase 2 scope | domain-strategy Phase 2 = FR+ES. Roadmap Phase 2 = FR+ES+AR | Minor |
| M6 | multilingual-roadmap.md | 58 | frees0ft.fr "90% от одной страницы" — CSV shows 85.3%. Slightly overstated | Minor |
| M7 | executive-summary.md | 72 | "×3.2–4.0" — 700K/222K = 3.15×, not 3.2×. 880K/222K = 3.96× ≈ 4.0× ✓ | Minor |

---

## 8. Gambling/Adult Content Filter

```regex
(?i)(casino|gambling|slots|betting|bets|poker|roulette|jackpot|porn|xxx|adult|nsfw|букмекер|казино|ставки|порно|1xbet|juwa|rummy)
```

| Файл | Результат |
|------|-----------|
| executive-summary.md | CLEAN — 0 matches |
| domain-strategy.md | CLEAN — 0 matches |
| multilingual-roadmap.md | CLEAN — 0 matches |

---

## 9. Existing Validation Report Assessment

Файл: `seo-competitor-analysis/validation/validation-report.md`

**Что делает хорошо:**
- ~180 числовых утверждений проверены report→brief
- 3 chain-of-evidence traces выполнены (report→brief→source brief)
- Minor issues корректно зафиксированы
- Gambling filter применён

**Что НЕ делает (gaps):**
1. Не проверяет executive-summary.md
2. Не проверяет briefs→CSV (Level 2)
3. Не флагает NOT_IN_AHREFS утверждения (hreflang)
4. Не флагает INFERENCE vs FACT claims
5. Не проверяет language count discrepancies
6. Softonic.ru "traffic>100 = 568" не сверяется с CSV (фактически 378)
7. Malavida "subdomains = 9,880" не сверяется с CSV (фактически 8,891)

---

## 10. Chain of Evidence: Data Flow Assessment

```
CSV (Ahrefs export) → Brief 04a-06a (Phase 1) → Brief 11-18 (Phase 2/3) → Reports (Phase 4)
```

**Level 1 (Reports→Briefs): STRONG** — ~195/~220 утверждений verified, 7 minor roundings.

**Level 2 (Briefs→CSV): MIXED**
- Direct Ahrefs metrics (DR, total traffic, keywords): отсутствуют в CSV (только в PNG overview screenshots)
- Site_structure counts: 3/4 verified, 4 MISMATCH
- Top_pages traffic sums: consistent but ≠ overview numbers (expected)

**Level 3 (Source attribution): WEAK for non-numeric claims**
- hreflang: NO source in data
- Strategy recommendations: INFERENCE (justified but not data)
- Budget/timeline/KPIs: INFERENCE (modeled, not measured)

---

## 11. Recommendations

### Обязательные (перед публикацией):

1. **[CF-1] Маркировать все hreflang-утверждения** как `[верифицировано вручную]` или `[требует верификации]`. Указать источник (ручной аудит сайта, не Ahrefs).

2. **[CF-2] Исправить scope validation claim** в executive-summary.md:102 — уточнить что проверены 2 отчёта (не 3), только level 1 (report vs briefs), без CSV-верификации.

3. **[Discrepancy] Расследовать расхождения malavida/softonic.ru** counts (brief 14 vs CSV). Если brief 06a/05a использовали другой Ahrefs snapshot — задокументировать.

### Рекомендуемые (улучшение качества):

4. **Маркировать INFERENCE** — все бюджеты, сроки, KPI-таргеты, миграционные риски должны иметь пометку `[оценка]` или `[проекция]` для отличия от данных Ahrefs.

5. **Унифицировать language counts** — добавить сноску "N total / M with measurable traffic" для каждого конкурента.

6. **Исправить minor M3** — "60% реализации" → "~57%" или изменить порог на 530K.

7. **Исправить minor M6** — "90% от одной страницы" → "~85%" (CSV-verified).

---

## Appendix A: Files Examined

### Reports (verified)
- `seo-competitor-analysis/reports/executive-summary.md` (105 lines)
- `seo-competitor-analysis/reports/domain-strategy.md` (413 lines)
- `seo-competitor-analysis/reports/multilingual-roadmap.md` (528 lines)

### Briefs (source data)
- `analysis/cross-analysis/our-state.yaml` (brief 11)
- `analysis/cross-analysis/multilingual-strategies.yaml` (brief 12)
- `analysis/cross-analysis/french-market.yaml` (brief 13)
- `analysis/cross-analysis/domain-structures.yaml` (brief 14)
- `analysis/cross-analysis/language-potential.yaml` (brief 16)
- `analysis/cross-analysis/domain-strategy.yaml` (brief 17)
- `analysis/cross-analysis/roadmap-draft.yaml` (brief 18)

### CSV files (spot-checked)
- `pipeline-seo/data_utf8/freesoft_ru_top_pages_subdomains_ru_actua_*.csv`
- `pipeline-seo/data_utf8/freesoft_ru_top_pages_subdomains_ru_compa_*.csv`
- `pipeline-seo/data_utf8/freesoft_net_top_pages_subdomains_ru_actu_*.csv`
- `pipeline-seo/data_utf8/frees0ft_fr_top_pages_subdomains_fr_actua_*.csv`
- `pipeline-seo/data_utf8/trashbox_ru_site_structure_subdomains_ru_*.csv`
- `pipeline-seo/data_utf8/softonic_ru_site_structure_subdomains_ru_*.csv`
- `pipeline-seo/data_utf8/softonic_com_site_structure_subdomains_ru_*.csv`
- `pipeline-seo/data_utf8/softonic_com_top_pages_subdomains_all_act_*.csv`
- `pipeline-seo/data_utf8/uptodown_com_site_structure_subdomains_ru_*.csv`
- `pipeline-seo/data_utf8/uptodown_com_top_pages_subdomains_all_act_*.csv`
- `pipeline-seo/data_utf8/malavida_com_site_structure_subdomains_ru_*.csv`
- `pipeline-seo/data_utf8/malavida_com_top_pages_subdomains_all_act_*.csv`
- `pipeline-seo/data_utf8/01net_com_top_pages_subdomains_all_actual_*.csv`
- `pipeline-seo/data_utf8/clubic_com_top_pages_subdomains_all_actua_*.csv`
- `pipeline-seo/data_utf8/commentcamarche_net_top_pages_subdomains_al_*.csv`
- `pipeline-seo/data_utf8/filehippo_com_site_structure_subdomains_ru_*.csv`
- `pipeline-seo/data_utf8/frees0ft.fr-perf-subdomains_year2_daily_*.csv`

### Existing validation
- `seo-competitor-analysis/validation/validation-report.md`

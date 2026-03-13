# План Disavow — Очистка ссылочного профиля freesoft

> **Дата:** 2026-03-13 | **Источник:** Ahrefs + R2 PBN-анализ
> **Данные:** `r2_pbn_signals.json`, [02-full-report.md](02-full-report.md) секция R2
> **Инструмент:** Google Search Console → Disavow Links Tool

---

## Зачем нужен disavow

Все три домена freesoft имеют spam% значительно выше медианы ниши (42.4%): freesoft.net — 89.3%, frees0ft.fr — 88.9%, freesoft.ru — 69.8%. Такой уровень спама размывает ссылочный профиль и может негативно влиять на ранжирование. Обнаружены две организованные спам-сети (seo-anomaly-\*, bhs-links-\*), атакующие наши домены. Disavow — обязательный первый шаг перед линкбилдингом.

---

## freesoft.net (DR 51) — СРОЧНО

### Масштаб проблемы

| Метрика | freesoft.net | Медиана ниши | Отклонение |
|---------|:-----------:|:------------:|:----------:|
| Spam % | **89.3%** | 42.4% | +47 п.п. |
| Low DR % | **89.5%** | 57.2% | +32 п.п. |
| Suspicious TLD % | **71.6%** | 15.0% | +57 п.п. |
| Ref. domains | 3 864 | 17 373 | 4.5x меньше |
| Spam-флаг Ahrefs | 3 452 доменов | — | 89.3% профиля |

### Паттерны для disavow

| # | Паттерн | Кол-во доменов | Avg DR | Пример | Приоритет |
|---|---------|:--------------:|:------:|--------|:---------:|
| 1 | `domain:*.xyz` | 1 950 | 0.3 | playlord.xyz, kurumsalwebsitesi.xyz | 1 — ПЕРВЫЙ |
| 2 | `domain:*.info` | 602 | 0.5 | alberghino.info, i2eo1e0px.info | 2 |
| 3 | `domain:*.asia` | 224 | 0.4 | u29o4g.asia, rjy5l6.asia | 3 |
| 4 | `domain:seo-anomaly-*.site` | 106 | 3.4 | seo-anomaly-authority.site | 4 |
| 5 | `domain:seo-anomaly-*.space` | 104 | 3.2 | seo-anomaly-organic.space | 4 |
| 6 | `domain:seo-anomaly-*.online` | 104 | 3.0 | seo-anomaly-indexing.online | 4 |
| 7 | `domain:seo-anomaly-*.website` | 98 | 3.1 | seo-anomaly-alttext.website | 4 |
| 8 | `domain:*.top` | 3 | — | — | 5 |

**Примечание:** Сеть seo-anomaly-\* использует SEO-терминологию в именах доменов (authority, bounce, crawling, keydensity, linkbuilding и т.д.) и присутствует во ВСЕХ 12 анализируемых доменах. Это массовый link-спам, атакующий всю нишу software downloads.

### Итого к disavow: ~3 000 доменов

- Suspicious TLDs (.xyz, .info, .asia, .site, .space, .online, .website, .top): 2 765 доменов
- Дополнительные spam-флаг домены (low DR .com и др.): ~200–300 доменов
- **После disavow останется: ~800–900 «чистых» referring domains**
- Это соответствует реальному масштабу домена DR 51

---

## freesoft.ru (DR 59) — ТОЧЕЧНО

### Масштаб проблемы

| Метрика | freesoft.ru | Медиана ниши | Отклонение |
|---------|:----------:|:------------:|:----------:|
| Spam % | **69.8%** | 42.4% | +27 п.п. |
| Low DR % | **53.3%** | 57.2% | -4 п.п. (норма) |
| Suspicious TLD % | **11.1%** | 15.0% | -4 п.п. (норма) |
| Ref. domains | 3 257 | 17 373 | 5.3x меньше |
| Spam-флаг Ahrefs | 2 274 доменов | — | 69.8% профиля |

### Паттерны для disavow

| # | Паттерн | Кол-во доменов | Avg DR | Пример | Приоритет |
|---|---------|:--------------:|:------:|--------|:---------:|
| 1 | `domain:seo-anomaly-*.site` | ~135 | 2.8 | seo-anomaly-authority.site | 1 — ПЕРВЫЙ |
| 2 | `domain:seo-anomaly-*.space` | ~130 | 2.6 | seo-anomaly-organic.space | 1 |
| 3 | `domain:seo-anomaly-*.online` | ~126 | 2.6 | seo-anomaly-indexing.online | 1 |
| 4 | `domain:seo-anomaly-*.website` | ~121 | 2.5 | seo-anomaly-alttext.website | 1 |
| 5 | `domain:*-links-bhs.xyz` | ~9 | 0.3 | o-links-bhs.xyz, t-links-bhs.xyz | 2 |
| 6 | `domain:*.xyz` (остальные) | ~36 | 0.3 | arabtheme.xyz | 3 |
| 7 | `domain:*.info` | 28 | 3.0 | — | 4 |
| 8 | `domain:*.top` | 4 | — | — | 5 |
| 9 | `domain:*.click` | 1 | — | — | 5 |
| 10 | `domain:*.work` | 1 | — | — | 5 |

**Примечание:** У freesoft.ru low DR % (53.3%) и suspicious TLD % (11.1%) находятся на уровне медианы ниши — это значит, что основная проблема не в TLD-кластерах, а в сети seo-anomaly-\* на «нормальных» TLD (.site, .space, .online, .website). Также обнаружена сеть bhs-links через \*-links-bhs.xyz.

**Особенность:** Временные спайки показывают два паттерна:
- 2024-W18..2025-W43: avg DR 9–20 — возможно органические ссылки
- 2026-W04..W10: avg DR 1.8–2.9 — чисто спамовые

Рекомендуется мониторить спайки 2026 года; если продолжатся — расширить disavow.

### Итого к disavow: ~500–600 доменов

- Сеть seo-anomaly-\* (4 TLD): ~512 доменов
- Сеть bhs-links (xyz): ~9 доменов
- Остальные suspicious TLDs: ~40 доменов
- **После disavow останется: ~2 600–2 700 referring domains**
- Dofollow % должен вырасти с текущих 35.5%

---

## frees0ft.fr (DR 23) — СРОЧНО + МИГРАЦИЯ

### Масштаб проблемы

| Метрика | frees0ft.fr | Медиана ниши | Отклонение |
|---------|:----------:|:------------:|:----------:|
| Spam % | **88.9%** | 42.4% | +47 п.п. |
| Low DR % | **64.0%** | 57.2% | +7 п.п. |
| Suspicious TLD % | **27.8%** | 15.0% | +13 п.п. |
| Ref. domains | 478 | 17 373 | 36x меньше |
| Spam-флаг Ahrefs | 425 доменов | — | 88.9% профиля |

### Паттерны для disavow

| # | Паттерн | Кол-во доменов | Avg DR | Пример | Приоритет |
|---|---------|:--------------:|:------:|--------|:---------:|
| 1 | `domain:bhs-links-*.site` | 55 | 3.4 | bhs-links-poseidon.site, bhs-links-apollo.site | 1 — ПЕРВЫЙ |
| 2 | `domain:bhs-links-*.space` | 51 | 3.0 | bhs-links-rhea.space, bhs-links-zeus.space | 1 |
| 3 | `domain:bhs-links-*.online` | 46 | 2.7 | bhs-links-ares.online, bhs-links-gaia.online | 1 |
| 4 | `domain:bhs-links-*.website` | 43 | 2.8 | bhs-links-ares.website, bhs-links-zeus.website | 1 |
| 5 | `domain:*-links-bhs.xyz` | ~8 | 0.3 | o-links-bhs.xyz, t-links-bhs.xyz | 2 |
| 6 | `domain:seo-anomaly-*.xyz` | ~6 | 0.3 | seo-anomaly-6.xyz, seo-anomaly-2.xyz | 2 |
| 7 | `domain:seo-anomaly-*.online` | — | — | seo-anomaly-sao-paulo.online | 3 |
| 8 | `domain:seo-anomaly-*.space` | — | — | seo-anomaly-tokyo.space | 3 |
| 9 | `domain:seo-anomaly-*.site` | — | — | seo-anomaly-jakarta.site | 3 |
| 10 | `domain:seo-anomaly-*.website` | — | — | seo-anomaly-mexico.website | 3 |

**Сеть bhs-links-\*: 221 домен из 478 (46% всего ссылочного профиля)**

Сеть использует мифологические имена (Zeus, Hades, Apollo, Athena, Poseidon, Rhea, Morpheus, Persephone, Ares, Gaia, Selene, Eros, Uranus, Cronus, Hephaestus, Nyx, Thanatos, Hestia, Helios, Dionysus, Aphrodite, Artemis, Hera) на 5 TLD (.site, .space, .online, .website, .xyz). Также обнаружены субдомены `sparta.bhs-links-*.website`, `corinth.bhs-links-*.online` — города-государства.

Это явный шаблонный генератор. Может быть как негативное SEO, так и заказанный link-спам.

### Итого к disavow: ~230 доменов

- Сеть bhs-links-\* (5 TLD): ~203 домена
- Сеть seo-anomaly-\* (включая xyz): ~20 доменов
- Дополнительные подозрительные: ~7 доменов
- **После disavow останется: ~248 referring domains**
- Профиль останется слабым (DR 23), но чистым

---

## Шаблон disavow-файла

### freesoft.net

```
# Disavow file for freesoft.net
# Generated: 2026-03-13
# Source: Ahrefs R2 PBN analysis
# Estimated domains: ~3 000

# === Priority 1: TLD clusters (mass spam) ===

# .xyz cluster — 1 950 domains, avg DR 0.3
domain:*.xyz

# === Priority 2: .info cluster ===

# .info cluster — 602 domains, avg DR 0.5
domain:*.info

# === Priority 3: .asia cluster ===

# .asia cluster — 224 domains, avg DR 0.4
domain:*.asia

# === Priority 4: seo-anomaly-* network ===

# seo-anomaly network on .site — 106 domains
domain:seo-anomaly-authority.site
domain:seo-anomaly-linkbuilding.site
domain:seo-anomaly-bounce.site
domain:seo-anomaly-black.site
domain:seo-anomaly-serp.site
domain:seo-anomaly-conversion.site
domain:seo-anomaly-engagement.site
domain:seo-anomaly-master.site
domain:seo-anomaly-crawling.site
domain:seo-anomaly-keydensity.site
# ... (остальные ~96 доменов — полный список из Ahrefs экспорта)

# seo-anomaly network on .space — 104 domains
domain:seo-anomaly-organic.space
domain:seo-anomaly-dofollow.space
domain:seo-anomaly-domain.space
domain:seo-anomaly-serp.space
domain:seo-anomaly-sitemap.space
domain:seo-anomaly-metadata.space
domain:seo-anomaly-seoaudit.space
domain:seo-anomaly-hreflang.space
domain:seo-anomaly-crawlbudget.space
domain:seo-anomaly-snippet.space
# ... (остальные ~94 домена)

# seo-anomaly network on .online — 104 domains
domain:seo-anomaly-indexing.online
domain:seo-anomaly-alttext.online
domain:seo-anomaly-conversion.online
domain:seo-anomaly-canonical.online
domain:seo-anomaly-engagement.online
domain:seo-anomaly-crawlbudget.online
domain:seo-anomaly-metadata.online
domain:seo-anomaly-keydensity.online
domain:seo-anomaly-seoaudit.online
domain:seo-anomaly-linkbuilding.online
# ... (остальные ~94 домена)

# seo-anomaly network on .website — 98 domains
domain:seo-anomaly-alttext.website
domain:seo-anomaly-hreflang.website
domain:seo-anomaly-seoaudit.website
domain:seo-anomaly-crawling.website
domain:seo-anomaly-anchor.website
domain:seo-anomaly-linkbuilding.website
domain:seo-anomaly-engagement.website
domain:seo-anomaly-conversion.website
domain:seo-anomaly-snippet.website
domain:seo-anomaly-bounce.website
# ... (остальные ~88 доменов)

# === Priority 5: remaining suspicious TLDs ===
domain:*.top
```

### freesoft.ru

```
# Disavow file for freesoft.ru
# Generated: 2026-03-13
# Source: Ahrefs R2 PBN analysis
# Estimated domains: ~500-600

# === Priority 1: seo-anomaly-* network ===

# seo-anomaly on .site — ~135 domains
domain:seo-anomaly-authority.site
domain:seo-anomaly-linkbuilding.site
domain:seo-anomaly-bounce.site
domain:seo-anomaly-black.site
domain:seo-anomaly-serp.site
domain:seo-anomaly-conversion.site
domain:seo-anomaly-engagement.site
domain:seo-anomaly-master.site
domain:seo-anomaly-crawling.site
domain:seo-anomaly-keydensity.site
# ... (остальные домены — полный список из Ahrefs экспорта)

# seo-anomaly on .space — ~130 domains
domain:seo-anomaly-organic.space
domain:seo-anomaly-dofollow.space
domain:seo-anomaly-domain.space
# ... (полный список из Ahrefs)

# seo-anomaly on .online — ~126 domains
domain:seo-anomaly-indexing.online
domain:seo-anomaly-alttext.online
domain:seo-anomaly-conversion.online
# ... (полный список из Ahrefs)

# seo-anomaly on .website — ~121 domains
domain:seo-anomaly-alttext.website
domain:seo-anomaly-hreflang.website
domain:seo-anomaly-seoaudit.website
# ... (полный список из Ahrefs)

# === Priority 2: bhs-links network (xyz) ===
domain:o-links-bhs.xyz
domain:t-links-bhs.xyz
domain:r-links-bhs.xyz
domain:w-links-bhs.xyz
domain:u-links-bhs.xyz
domain:q-links-bhs.xyz
domain:i-links-bhs.xyz
domain:y-links-bhs.xyz
domain:p-links-bhs.xyz

# === Priority 3: remaining suspicious TLDs ===
# .xyz (excluding bhs-links, ~36 domains — review individually)
# .info — 28 domains
# .top — 4 domains
# .click — 1 domain
# .work — 1 domain
```

### frees0ft.fr

```
# Disavow file for frees0ft.fr
# Generated: 2026-03-13
# Source: Ahrefs R2 PBN analysis
# Estimated domains: ~230

# === Priority 1: bhs-links-* network ===

# bhs-links on .site — 55 domains
domain:bhs-links-poseidon.site
domain:bhs-links-apollo.site
domain:bhs-links-nyx.site
domain:bhs-links-uranus.site
domain:bhs-links-rhea.site
domain:bhs-links-zeus.site
domain:bhs-links-morpheus.site
domain:bhs-links-hades.site
domain:bhs-links-ares.site
domain:bhs-links-persephone.site
# ... (остальные ~45 доменов)

# bhs-links on .space — 51 domain
domain:bhs-links-rhea.space
domain:bhs-links-cronus.space
domain:bhs-links-hephaestus.space
domain:bhs-links-poseidon.space
domain:bhs-links-zeus.space
domain:bhs-links-persephone.space
domain:bhs-links-athena.space
domain:bhs-links-gaia.space
domain:bhs-links-selene.space
domain:bhs-links-eros.space
# ... (остальные ~41 домен)

# bhs-links on .online — 46 domains
domain:bhs-links-ares.online
domain:bhs-links-gaia.online
domain:bhs-links-artemis.online
domain:bhs-links-zeus.online
domain:bhs-links-hades.online
domain:bhs-links-hera.online
domain:bhs-links-hestia.online
domain:bhs-links-helios.online
domain:bhs-links-dionysus.online
domain:bhs-links-aphrodite.online
# ... (остальные ~36 доменов)

# bhs-links on .website — 43 domains
domain:bhs-links-ares.website
domain:bhs-links-selene.website
domain:bhs-links-zeus.website
domain:bhs-links-apollo.website
domain:bhs-links-uranus.website
domain:bhs-links-thanatos.website
domain:bhs-links-nyx.website
domain:bhs-links-rhea.website
domain:bhs-links-hestia.website
domain:bhs-links-morpheus.website
# ... (остальные ~33 домена)

# === Priority 2: bhs-links and seo-anomaly on .xyz ===
domain:o-links-bhs.xyz
domain:t-links-bhs.xyz
domain:r-links-bhs.xyz
domain:w-links-bhs.xyz
domain:u-links-bhs.xyz
domain:q-links-bhs.xyz
domain:y-links-bhs.xyz
domain:p-links-bhs.xyz
domain:seo-anomaly-6.xyz
domain:seo-anomaly-2.xyz

# === Priority 3: seo-anomaly-* (geo pattern) ===
domain:seo-anomaly-sao-paulo.online
domain:seo-anomaly-tokyo.space
domain:seo-anomaly-jakarta.site
domain:seo-anomaly-mexico.website
# ... (остальные из данной сети)
```

**Формат:** Google Search Console Disavow Tool принимает текстовый файл (.txt), одна строка = один паттерн. Префикс `domain:` означает все URL с данного домена.

**Важно:** Полный список доменов необходимо извлечь из Ahrefs экспорта (файлы A1, A2, A3 из `data_for_task/backlinks/referring_domains/`). Шаблоны выше содержат паттерны и примеры; для генерации финального файла — отфильтровать домены по указанным паттернам.

---

## Порядок действий

1. [ ] Скачать текущий disavow-файл из Google Search Console (если есть) для каждого из 3 доменов
2. [ ] Экспортировать полный список referring domains из Ahrefs для каждого домена
3. [ ] Применить фильтры по паттернам из таблиц выше (скрипт или ручная фильтрация)
4. [ ] Составить disavow-файлы по шаблонам
5. [ ] Объединить с существующим disavow-файлом (если был)
6. [ ] Загрузить в Google Search Console для каждого домена **отдельно**
7. [ ] Зафиксировать дату загрузки и количество доменов в disavow
8. [ ] Дождаться переиндексации (2–4 недели)
9. [ ] Через 30 дней: проверить spam% в Ahrefs
10. [ ] Через 90 дней: повторная оценка и корректировка

---

## Мониторинг после disavow

### freesoft.net

| Метрика | Текущее | Целевое (30 дней) | Целевое (90 дней) |
|---------|:-------:|:-----------------:|:-----------------:|
| Spam % | 89.3% | 50–60% | 40–50% |
| Ref. domains | 3 864 | 800–900 | 1 000–1 200 |
| DR | 51 | 51 | 52–54 |
| Suspicious TLD % | 71.6% | <15% | <10% |

### freesoft.ru

| Метрика | Текущее | Целевое (30 дней) | Целевое (90 дней) |
|---------|:-------:|:-----------------:|:-----------------:|
| Spam % | 69.8% | 55–60% | 45–55% |
| Ref. domains | 3 257 | 2 600–2 700 | 2 800–3 000 |
| DR | 59 | 59 | 60–61 |
| Dofollow % | 35.5% | 38–40% | 42–45% |

### frees0ft.fr

| Метрика | Текущее | Целевое (30 дней) | Целевое (90 дней) |
|---------|:-------:|:-----------------:|:-----------------:|
| Spam % | 88.9% | 40–50% | 30–40% |
| Ref. domains | 478 | ~248 | 250–270 |
| DR | 23 | 23 | 23 |
| bhs-links % | 46% | 0% | 0% |

---

## Для frees0ft.fr: миграция + disavow

### Специальные рекомендации

1. **Disavow сейчас (на текущем домене frees0ft.fr):**
   - Загрузить disavow-файл с bhs-links-\* + seo-anomaly-\* в GSC
   - Цель: очистить профиль перед миграцией
   - Чистый профиль = лучший «стартовый капитал» для 301-redirect

2. **При миграции (301-redirect на новый домен):**
   - 301-redirect с frees0ft.fr на новый домен
   - **Disavow НЕ переносится автоматически при 301-redirect**
   - Необходимо заново добавить disavow-файл в GSC для нового домена (если спам-ссылки начнут «перетекать»)

3. **После миграции (мониторинг):**
   - Через 2 недели: проверить, появились ли спам-ссылки на новом домене
   - Если bhs-links-\* начнут ссылаться на новый домен — немедленно disavow
   - Вероятнее всего, спам-сеть не будет автоматически обновлять ссылки на новый домен

4. **hreflang после миграции:**
   - Связать новый FR-домен с freesoft.net и freesoft.ru через hreflang
   - Это укрепит ссылочный профиль всей группы доменов

### Порядок: миграция + disavow

```
Сейчас:     disavow на frees0ft.fr → GSC → ждать 2-4 недели
Миграция:   301-redirect frees0ft.fr → новый.домен
+1 неделя:  проверить ref. domains нового домена в Ahrefs
+2 недели:  если спам перетёк → disavow на новом домене в GSC
+1 месяц:   полная проверка spam% на обоих доменах
+3 месяца:  закрыть старый домен (если 301 стабилен)
```

---

## Связанные документы

- [02-full-report.md](02-full-report.md) — полный отчёт (R2 секция: PBN-детекция)
- [03-target-domains.md](03-target-domains.md) — куда направить линкбилдинг после очистки
- [05-implementation-roadmap.md](05-implementation-roadmap.md) — disavow как первый шаг roadmap
- [07-audit-report.md](07-audit-report.md) — верификация данных

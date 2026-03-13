## 4. Opportunities — пересекающиеся домены (R3)

### Ключевые находки

- **28 178 доменов** ссылаются на 2+ наших конкурентов, но НЕ на нас: 14 517 ссылаются на 3+ конкурентов, 13 661 — ровно на 2. Это огромный пул target-доменов для outreach.
- **freesoft.net неожиданно близок к русским конкурентам:** Jaccard-similarity с softonic.ru = 0.58, с trashbox.ru = 0.44 — ссылочный профиль freesoft.net «русскоязычный», а не «англоязычный». Overlap с softonic.com всего 0.02 — колоссальный gap.
- **EN-группа — самый большой потенциал роста:** 5 099 доменов (DR 20+, intersect 2+) ссылаются на англоязычных конкурентов и не на freesoft.net. Текущий overlap с softonic.com (Jaccard 0.02) означает, что 97% ссылочного профиля softonic.com — terra incognita для freesoft.net.
- **FR-группа зажата внутри тесного кластера:** clubic+01net (Jaccard 0.32), clubic+ccm (0.22), 01net+ccm (0.20). Три конкурента активно делят одну «подушку» из 4 369 target-доменов. frees0ft.fr (478 ref domains) стоит в стороне с Jaccard < 0.03 ко всем трём.
- **RU-группа — самая скудная Link Intersect:** всего 49 доменов (DR 20+) ссылаются на оба конкурента (softonic.ru и trashbox.ru), но не на freesoft.ru. Причина: ниша «софт-скачивания» в рунете узкая, softonic.ru и trashbox.ru сами невелики (DR 57 и 55).

---

### Матрица пересечений (Jaccard Similarity)

Матрица 12x12 показывает долю общих referring domains между каждой парой сайтов. Значение 1.0 = полное совпадение, 0.0 = нет общих доноров. Диагональ = 1.0 (сам с собой). Ниже — «тепловая карта»:

| | fs.net | fs.ru | fs0.fr | soft.com | upto. | malav. | soft.ru | trash. | fileh. | clubic | 01net | ccm |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **freesoft.net** | **1.00** | .14 | .11 | **.02** | .10 | .28 | **.58** | **.44** | .21 | .09 | .14 | .06 |
| **freesoft.ru** | .14 | **1.00** | .13 | .04 | .06 | .12 | **.23** | **.19** | .08 | .06 | .05 | .06 |
| **frees0ft.fr** | .11 | .13 | **1.00** | **.01** | **.02** | .03 | .09 | .07 | .03 | **.02** | **.02** | **.03** |
| softonic.com | .02 | .04 | .01 | **1.00** | **.16** | .10 | .04 | .03 | **.13** | .07 | .06 | .07 |
| uptodown.com | .10 | .06 | .02 | .16 | **1.00** | **.22** | .12 | .10 | **.19** | .09 | .11 | .07 |
| malavida.com | .28 | .12 | .03 | .10 | .22 | **1.00** | **.33** | **.27** | **.28** | .15 | **.21** | .09 |
| softonic.ru | .58 | .23 | .09 | .04 | .12 | .33 | **1.00** | **.50** | .22 | .10 | .17 | .06 |
| trashbox.ru | .44 | .19 | .07 | .03 | .10 | .27 | .50 | **1.00** | .19 | .11 | .16 | .06 |
| filehippo.com | .21 | .08 | .03 | .13 | .19 | .28 | .22 | .19 | **1.00** | .12 | .16 | .08 |
| clubic.com | .09 | .06 | .02 | .07 | .09 | .15 | .10 | .11 | .12 | **1.00** | **.32** | **.22** |
| 01net.com | .14 | .05 | .02 | .06 | .11 | .21 | .17 | .16 | .16 | .32 | **1.00** | **.20** |
| ccm.net | .06 | .06 | .03 | .07 | .07 | .09 | .06 | .06 | .08 | .22 | .20 | **1.00** |

#### Кластеры и выводы

**Кластер 1 — «Русскоязычный пул»** (Jaccard 0.23-0.58):
- freesoft.net + softonic.ru (0.58) + trashbox.ru (0.44) + freesoft.ru (0.14)
- Ядро: softonic.ru <-> trashbox.ru (0.50), freesoft.net <-> softonic.ru (0.58)
- **Вывод:** freesoft.net делит больше доноров с softonic.ru и trashbox.ru, чем с любым EN-конкурентом. Это означает, что ссылочный профиль freesoft.net исторически формировался из RU-источников, несмотря на EN-домен.

**Кластер 2 — «Англоязычный mainstream»** (Jaccard 0.13-0.22):
- softonic.com + uptodown.com (0.16) + filehippo.com (0.13-0.19) + malavida.com (0.10-0.28)
- malavida.com — «мост» между кластерами: высокий overlap и с softonic.ru (0.33), и с uptodown (0.22), и с filehippo (0.28)
- **Вывод:** freesoft.net overlap с этим кластером крайне низок (softonic.com = 0.02, uptodown = 0.10). Здесь самый большой потенциал для наращивания EN-ссылок.

**Кластер 3 — «Французский»** (Jaccard 0.20-0.32):
- clubic.com + 01net.com (0.32) + commentcamarche.net (0.20-0.22)
- Тесный внутренний overlap, но все три изолированы от англоязычного кластера
- **Вывод:** frees0ft.fr (Jaccard < 0.03 ко всем трём) — полный аутсайдер. Но FR-конкуренты сильно связаны через общие ресурсы (ок. 9 300 общих доменов у clubic+01net). Именно этот пул — target для frees0ft.fr.

---

### Targets по языковым группам

> **Примечание к данным:** EN и FR Link Intersect-файлы усечены лимитом Ahrefs (30K доменов). Реальное количество target-доменов может быть выше. RU-группа — полные данные (5 042 домена).

#### EN Group — targets для freesoft.net

**Контекст:** 5 099 доменов (DR 20+, intersect 2+) не ссылаются на freesoft.net. Ниже top-20 из Ahrefs Link Intersect (softonic.com + uptodown.com + malavida.com vs freesoft.net), отсортированные по DR и intersect.

| # | Домен | DR | Traffic | Int. | Ссылается на | Тип ресурса | Приоритет |
|---|---|---|---|---|---|---|---|
| 1 | youtube.com | 99 | 2.41B | 3 | softonic(486), uptodown(1878), malavida(110) | Видеоплатформа (UGC) | Long Shot |
| 2 | wikipedia.org | 97 | 4.06B | 3 | softonic(161), uptodown(102), malavida(16) | Энциклопедия (wiki) | Стратегический |
| 3 | t.me | 96 | 17.6M | 3 | softonic(13), uptodown(153), malavida(4) | Мессенджер (UGC) | Quick Win |
| 4 | github.com | 96 | 40.4M | 3 | softonic(57), uptodown(108), malavida(18) | Dev-платформа (UGC) | Quick Win |
| 5 | microsoft.com | 96 | 307M | 2 | softonic(5), uptodown(26) | Вендор ПО | Стратегический |
| 6 | medium.com | 94 | 23.7M | 3 | softonic(55), uptodown(27), malavida(4) | Блог-платформа (UGC) | Quick Win |
| 7 | github.io | 94 | 10.8M | 3 | softonic(107), uptodown(70), malavida(7) | Dev-сайты (UGC) | Quick Win |
| 8 | wixsite.com | 94 | 1.8M | 3 | softonic(61), uptodown(27), malavida(1) | Бесплатные сайты (UGC) | Quick Win |
| 9 | bing.com | 93 | 14.2M | 3 | softonic(29820), uptodown(420), malavida(3409) | Поисковик | Long Shot |
| 10 | vercel.app | 93 | 2.3M | 3 | softonic(2), uptodown(9), malavida(15) | Dev-хостинг (UGC) | Quick Win |
| 11 | wikimedia.org | 93 | 3.1M | 3 | softonic(18), uptodown(2), malavida(1) | Wiki-ресурсы | Стратегический |
| 12 | springer.com | 93 | 1.8M | 3 | softonic(8), uptodown(1), malavida(4) | Академия | Long Shot |
| 13 | googleapis.com | 93 | 410K | 3 | softonic(7), uptodown(4), malavida(3) | Google-инфраструктура | N/A (тех.) |
| 14 | yahoo.co.jp | 93 | 209M | 3 | softonic(2), uptodown(5), malavida(1) | Портал (JP) | Long Shot |
| 15 | telegram.me | 93 | 568K | 3 | softonic(5), uptodown(115), malavida(1) | Мессенджер (UGC) | Quick Win |
| 16 | nih.gov | 95 | 109M | 3 | softonic(44), uptodown(5), malavida(3) | Гос. здравоохранение | Long Shot |
| 17 | stackoverflow.com | 92 | 8.2M | 3 | softonic(37), uptodown(22), malavida(7) | Dev-форум | Quick Win |
| 18 | fandom.com | 92 | 188M | 3 | softonic(23), uptodown(49), malavida(2) | Wiki-игры (UGC) | Quick Win |
| 19 | mail.ru | 92 | 29.0M | 3 | softonic(1), uptodown(11), malavida(1) | RU портал | Quick Win |
| 20 | mdpi.com | 92 | 1.2M | 3 | softonic(51), uptodown(7), malavida(11) | Академия (Open Access) | Стратегический |

**Комментарии по EN-targets:**

- **UGC-платформы (github.com, medium.com, github.io, wixsite.com, vercel.app, t.me, telegram.me, stackoverflow.com, fandom.com)** — самые доступные. Ссылки появляются через пользовательский контент: README-файлы, статьи, посты на форумах. Для freesoft.net стратегия: создание полезного контента (обзоры, гайды, инструменты), который пользователи будут ссылать.
- **wikipedia.org, wikimedia.org** — высочайший авторитет. Нужен notability-критерий. Вариант: если есть страницы про ПО, где упоминаются source-ссылки, можно предложить freesoft.net как альтернативный источник.
- **microsoft.com** — вендор, напрямую не получить. Но партнерские/аффилиатные программы Microsoft могут дать ссылку.
- **bing.com** — 29 820 ссылок на softonic (SEO-индексация). Скорее индикатор SEO-видимости, чем actionable target.
- **mail.ru** — интересный кросс-языковой target. Уже ссылается на softonic и uptodown; учитывая RU-roots freesoft.net, может быть доступным.

#### RU Group — targets для freesoft.ru

**Контекст:** Всего 49 доменов (DR 20+, intersect 2) — самая узкая группа. softonic.ru и trashbox.ru сами относительно небольшие (DR 57 и 55), поэтому пересечений мало. Данные полные, не усечены.

| # | Домен | DR | Traffic | Int. | Ссылается на | Тип ресурса | Приоритет |
|---|---|---|---|---|---|---|---|
| 1 | t.me | 96 | 17.6M | 2 | softonic.ru(1), trashbox(341) | Мессенджер (UGC) | Quick Win |
| 2 | github.com | 96 | 40.4M | 2 | softonic.ru(1), trashbox(5) | Dev-платформа (UGC) | Quick Win |
| 3 | telegram.me | 93 | 568K | 2 | softonic.ru(2), trashbox(67) | Мессенджер (UGC) | Quick Win |
| 4 | fandom.com | 92 | 188M | 2 | softonic.ru(1), trashbox(4) | Wiki-игры (UGC) | Quick Win |
| 5 | teletype.in | 82 | 2.6K | 2 | softonic.ru(19), trashbox(17) | RU блог-платформа | Quick Win |
| 6 | ixbt.com | 78 | 482K | 2 | softonic.ru(2), trashbox(27) | Tech-медиа (RU) | **Quick Win / High Value** |
| 7 | pr-cy.ru | 75 | 1.9M | 2 | softonic.ru(2), trashbox(1) | SEO-инструмент (RU) | Quick Win |
| 8 | partnerkin.com | 68 | 29.8K | 2 | softonic.ru(3), trashbox(2) | Маркетинг-медиа (RU) | Quick Win |
| 9 | skillfactory.ru | 67 | 261K | 2 | softonic.ru(2), trashbox(2) | EdTech (RU) | Стратегический |
| 10 | kokoc.com | 59 | 145K | 2 | softonic.ru(2), trashbox(1) | Digital-агентство (RU) | Quick Win |
| 11 | seosprint.net | 54 | 8.2K | 2 | softonic.ru(1), trashbox(1) | Заработок онлайн | Long Shot |
| 12 | linkingdirectory.com | 51 | 0 | 2 | softonic.ru(2), trashbox(2) | Каталог ссылок | Quick Win |
| 13 | worldofplayers.ru | 35 | 580 | 2 | softonic.ru(1), trashbox(12) | Игровой форум (RU) | Quick Win |
| 14 | trashexpert.ru | 34 | 12K | 2 | softonic.ru(1), trashbox(1) | Tech-блог (RU) | Quick Win |
| 15 | seosprint.run | 32 | 10.4K | 2 | softonic.ru(3), trashbox(3) | Заработок онлайн | Long Shot |
| 16 | dxdy.ru | 31 | 5.8K | 2 | softonic.ru(1), trashbox(1) | Научный форум (RU) | Стратегический |
| 17 | crestbook.com | 40 | 203 | 2 | softonic.ru(1), trashbox(1) | Шахматный сайт (RU) | Long Shot |
| 18 | gmd.live | 36 | 17.3K | 2 | softonic.ru(1), trashbox(1) | Игровой ресурс | Quick Win |
| 19 | microlinksite.com | 65 | 0 | 2 | softonic.ru(4), trashbox(4) | Сервис ссылок | Quick Win |
| 20 | ryba.team | 61 | 644 | 2 | softonic.ru(3), trashbox(4) | Digital-студия (RU) | Quick Win |

**Комментарии по RU-targets:**

- **ixbt.com (DR 78)** — главная находка. Крупнейшее tech-медиа в рунете, пишет обзоры софта и гаджетов. Trashbox имеет 27 ссылок оттуда. Для freesoft.ru это идеальный target: предложить экспертный комментарий, гостевую статью или данные для обзора.
- **t.me / telegram.me** — Telegram-каналы. Trashbox имеет 341 ссылку с t.me — значит, его активно цитируют в каналах. freesoft.ru нужен Telegram-канал с полезным контентом.
- **teletype.in (DR 82)** — русскоязычная блог-платформа, аналог Medium. И softonic.ru (19), и trashbox (17) хорошо представлены. Легко создать контент-хаб.
- **pr-cy.ru (DR 75)** — SEO-инструмент с каталогом сайтов. Можно зарегистрировать freesoft.ru.
- **partnerkin.com (DR 68)** — медиа о партнерском маркетинге и монетизации трафика. Релевантно для нашей ниши.
- **Спам-домены** (analyticshaven.top, creativeposts.top, byteshort.xyz, metamagic.top, screenshots.wiki и др. с DR 49-50 и traffic=0) — это сеть SEO-каталогов/PBN. Ссылки с них малоценны и не рекомендуются для outreach.

#### FR Group — targets для frees0ft.fr

**Контекст:** 4 369 доменов (DR 20+, intersect 2+) ссылаются на FR-конкурентов, но не на frees0ft.fr. frees0ft.fr имеет всего 478 referring domains (DR 23). Планируется миграция домена.

| # | Домен | DR | Traffic | Int. | Ссылается на | Тип ресурса | Приоритет |
|---|---|---|---|---|---|---|---|
| 1 | youtube.com | 99 | 2.41B | 3 | clubic(207), 01net(289), ccm(24) | Видеоплатформа (UGC) | Quick Win |
| 2 | google.com | 99 | 1.30B | 3 | clubic(2), 01net(1), ccm(3) | Поисковик | Long Shot |
| 3 | wikipedia.org | 97 | 4.06B | 3 | clubic(580), 01net(738), ccm(86) | Энциклопедия | Стратегический |
| 4 | github.com | 96 | 40.4M | 3 | clubic(7), 01net(5), ccm(6) | Dev-платформа (UGC) | Quick Win |
| 5 | t.me | 96 | 17.6M | 3 | clubic(34), 01net(13), ccm(2) | Мессенджер (UGC) | Quick Win |
| 6 | microsoft.com | 96 | 307M | 3 | clubic(1), 01net(2), ccm(12) | Вендор ПО | Стратегический |
| 7 | bsky.app | 94 | 1.2M | 3 | clubic(125), 01net(154), ccm(10) | Соцсеть (UGC) | Quick Win |
| 8 | github.io | 94 | 10.8M | 3 | clubic(5), 01net(30), ccm(15) | Dev-сайты (UGC) | Quick Win |
| 9 | medium.com | 94 | 23.7M | 3 | clubic(9), 01net(3), ccm(4) | Блог-платформа (UGC) | Quick Win |
| 10 | wixsite.com | 94 | 1.8M | 3 | clubic(6), 01net(5), ccm(4) | Бесплатные сайты (UGC) | Quick Win |
| 11 | weebly.com | 94 | 4.0M | 3 | clubic(3), 01net(2), ccm(1) | Бесплатные сайты (UGC) | Quick Win |
| 12 | substack.com | 93 | 7.5M | 3 | clubic(57), 01net(46), ccm(1) | Блог-платформа (UGC) | Quick Win |
| 13 | archive.org | 93 | 8.0M | 3 | clubic(13), 01net(3), ccm(3) | Web-архив | Quick Win |
| 14 | bing.com | 93 | 14.2M | 3 | clubic(631), 01net(353), ccm(207) | Поисковик | Long Shot |
| 15 | wikimedia.org | 93 | 3.1M | 3 | clubic(45), 01net(23), ccm(5) | Wiki-ресурсы | Стратегический |
| 16 | googleapis.com | 93 | 410K | 3 | clubic(494), 01net(424), ccm(83) | Google-инфра | N/A (тех.) |
| 17 | hatena.ne.jp | 93 | 1.1M | 3 | clubic(11), 01net(2), ccm(2) | JP блог-платформа | Long Shot |
| 18 | techcrunch.com | 92 | 747K | 3 | clubic(6), 01net(4), ccm(1) | Tech-медиа (EN/FR) | **Стратегический / High Value** |
| 19 | samsung.com | 92 | 77.6M | 3 | clubic(29), 01net(13), ccm(1) | Вендор | Стратегический |
| 20 | jimdofree.com | 92 | 3.1M | 3 | clubic(167), 01net(149), ccm(73) | Бесплатные сайты (UGC) | Quick Win |

**Дополнительные FR-specific targets (из top-50):**

| # | Домен | DR | Traffic | Int. | Ссылается на | Тип ресурса | Приоритет |
|---|---|---|---|---|---|---|---|
| 21 | ovhcloud.com | 92 | 1.4M | 3 | clubic(7), 01net(3), ccm(1) | FR хостинг-провайдер | **Quick Win / High Value** |
| 22 | cnil.fr | 94 | 232K | 2 | clubic(2), 01net(4) | Гос. регулятор (FR) | Стратегический |
| 23 | sourceforge.net | 92 | 2.1M | 2 | 01net(1), ccm(5) | Каталог ПО | **Quick Win / High Value** |
| 24 | fandom.com | 92 | 188M | 3 | clubic(3), 01net(14), ccm(2) | Wiki-игры (UGC) | Quick Win |
| 25 | notion.site | 92 | 62K | 3 | clubic(1), 01net(1), ccm(1) | Docs-платформа (UGC) | Quick Win |
| 26 | google.fr | 93 | 2.0M | 2 | clubic(2), ccm(2) | Поисковик (FR) | Long Shot |
| 27 | w3.org | 94 | 330K | 2 | clubic(153), 01net(447) | Web-стандарты | Long Shot |

**Комментарии по FR-targets:**

- **bsky.app** — неожиданная находка. clubic (125 ссылок) и 01net (154) очень активны в Bluesky. Значит, FR tech-комьюнити мигрировало туда. Создание присутствия в Bluesky может дать естественные ссылки.
- **jimdofree.com** — самый «насыщенный» UGC-target: 167+149+73 = 389 ссылок от FR-конкурентов. Это сайты на бесплатном хостинге, которые ссылаются на clubic/01net как на источники скачивания. Аналогичные сайты будут ссылаться на frees0ft.fr, если мы появимся в их поле зрения.
- **techcrunch.com (DR 92)** — все три FR-конкурента получают упоминания. Для frees0ft.fr важен TechCrunch France (если есть FR-редакция) или PR-релизы.
- **ovhcloud.com** — ключевой FR-хостинг. Партнерская программа или упоминание в маркетплейсе OVH может дать ссылку.
- **sourceforge.net (DR 92)** — прямой конкурент-каталог ПО, но также — площадка для размещения. Если freesoft.net/frees0ft.fr зарегистрирует проект, получит ссылку.
- **cnil.fr** — государственный регулятор данных (Франция). Ссылки появляются в контексте privacy-policy. Если frees0ft.fr корректно оформит политику приватности и GDPR — может быть процитирован.

**ВАЖНО для FR: учёт миграции домена frees0ft.fr**
- Все outreach-усилия должны идти с нового домена (после миграции), чтобы ссылки не «сгорели» при редиректе.
- Рекомендация: завершить миграцию ДО начала активного outreach. Если миграция ожидается в ближайшие 1-2 месяца, сейчас стоит только создавать UGC-ссылки (они легко обновляемы), а серьёзный outreach (медиа, партнёрства) отложить до постмиграции.
- При outreach после миграции — обязательно упоминать, что сайт переехал, и просить обновить ссылку, если она вела на старый домен.

---

### Отраслевые ресурсы (3+ конкурентов)

14 517 доменов ссылаются на 3+ из 9 конкурентов. Ниже — «must have» ресурсы, на которые ссылается максимум конкурентов. Это подтверждает, что данный ресурс — стандарт в нише.

| Домен | DR | На скольких конкур. | Тип ресурса | Actionable? |
|---|---|---|---|---|
| youtube.com | 99 | 9/9 | UGC видеоплатформа | Да — YouTube-канал, обзоры ПО |
| t.me | 96 | 9/9 | UGC мессенджер | Да — Telegram-каналы |
| github.com | 96 | 9/9 | UGC dev-платформа | Да — open-source проекты |
| bing.com | 93 | 9/9 | Поисковик (автолинки) | Нет — SEO-индексация |
| pages.dev | 93 | 9/9 | Cloudflare Pages (UGC) | Да — создание микросайтов |
| wikipedia.org | 97 | 8/9 | Энциклопедия | Да — редактирование статей (notability) |
| github.io | 94 | 8/9 | Dev-сайты (UGC) | Да — GitHub Pages проекты |
| wixsite.com | 94 | 8/9 | UGC сайтбилдер | Частично — спамный канал |
| medium.com | 94 | 8/9 | UGC блог-платформа | Да — экспертные статьи |
| telegram.me | 93 | 8/9 | UGC мессенджер | Да — Telegram-каналы |
| jimdofree.com | 92 | 8/9 | UGC сайтбилдер | Частично — спамный канал |
| goo.gl | 97 | 7/9 | URL-shortener (устарел) | Нет — сервис закрыт |
| weebly.com | 94 | 7/9 | UGC сайтбилдер | Частично |
| wikimedia.org | 93 | 7/9 | Wiki-ресурсы | Да — Wikimedia Commons/Wikidata |
| hatena.ne.jp | 93 | 7/9 | JP блог-платформа | Нет — не целевой язык |
| google.com | 99 | 6/9 | Поисковик | Нет — автолинки |
| microsoft.com | 96 | 6/9 | Вендор ПО | Да — партнёрская программа |
| nih.gov | 95 | 6/9 | Гос. здравоохранение | Нет — нерелевантно |
| substack.com | 93 | 6/9 | UGC блог-платформа | Да — экспертные рассылки |
| googleapis.com | 93 | 6/9 | Google-инфра | Нет — техническое |
| freshdesk.com | 92 | 6/9 | Help-desk платформа | Нет — внутренние ссылки компаний |
| mozilla.org | 96 | 5/9 | Вендор браузера | Да — партнёрства, аддоны |
| blogspot.com | 95 | 5/9 | UGC блоги | Да — блог-контент |
| bsky.app | 94 | 5/9 | Соцсеть (UGC) | Да — Bluesky-аккаунт |
| zendesk.com | 93 | 5/9 | Help-desk платформа | Нет — внутренние ссылки |
| theguardian.com | 93 | 5/9 | Медиа (EN) | Да — PR/комментарии |
| archive.org | 93 | 5/9 | Web-архив | Да — Wayback Machine |
| notion.site | 92 | 5/9 | UGC docs-платформа | Да — базы знаний |

**Паттерн:** Верхние позиции заняты UGC-платформами (youtube, github, t.me, medium и т.д.), а не тематическими медиа. Это значит, что ссылки конкурентов массово генерируются пользователями, а не через outreach. Для freesoft стратегия «community presence» (YouTube-канал, Telegram-канал, GitHub-проекты) даст мультипликативный эффект: одно усилие — ссылки с множества доменов.

---

### Матрица приоритетов

#### Quick Wins (высокая доступность + хороший DR)

Домены, где получить ссылку проще всего — UGC-платформы, каталоги, форумы. Ссылка зависит только от наших действий.

| # | Домен | DR | Языки | Действие | Est. усилие |
|---|---|---|---|---|---|
| 1 | **github.com** | 96 | EN,RU,FR | Создать open-source инструмент/скрипт со ссылкой на freesoft | 1-2 дня |
| 2 | **t.me / telegram.me** | 96/93 | EN,RU,FR | Создать Telegram-каналы для каждого языка с обзорами софта | 1 день + постоянно |
| 3 | **medium.com** | 94 | EN,FR | Публиковать экспертные статьи «Best apps for X» со ссылками | 2-3 часа/статья |
| 4 | **stackoverflow.com** | 92 | EN | Отвечать на вопросы о ПО со ссылками на freesoft (осторожно: модерация!) | Постоянно |
| 5 | **fandom.com** | 92 | EN,RU,FR | Добавить ссылки в wiki-статьи об играх/приложениях | 1 день |
| 6 | **bsky.app** | 94 | FR | Создать аккаунт в Bluesky (особенно для FR: clubic=125, 01net=154 ссылок) | 1 день + постоянно |
| 7 | **substack.com** | 93 | EN,FR | Запустить рассылку о новинках ПО со ссылками | 1 день + постоянно |
| 8 | **archive.org** | 93 | EN,FR | Зарегистрировать коллекцию/проект с обзорами ПО | 1 день |
| 9 | **teletype.in** | 82 | RU | Публиковать статьи-обзоры на RU блог-платформе | 2-3 часа/статья |
| 10 | **sourceforge.net** | 92 | EN,FR | Зарегистрировать проект, получить профиль со ссылкой | 1 час |

#### Стратегические targets (высокий DR, требуют усилий, но реалистичны)

Домены, где нужен outreach или создание значимого контента.

| # | Домен | DR | Языки | Действие | Est. усилие |
|---|---|---|---|---|---|
| 1 | **wikipedia.org** | 97 | EN,FR | Добавить freesoft как источник в статьях о ПО (нужна notability) | 2-4 недели |
| 2 | **microsoft.com** | 96 | EN,FR | Партнёрская программа Microsoft, App Source | 1-2 месяца |
| 3 | **ixbt.com** | 78 | RU | Предложить экспертный комментарий или данные для обзора | 1-2 недели |
| 4 | **techcrunch.com** | 92 | FR | PR-релиз или питч об интересных данных о рынке ПО | 1-3 месяца |
| 5 | **ovhcloud.com** | 92 | FR | Партнёрская/технологическая интеграция | 1-2 месяца |
| 6 | **pr-cy.ru** | 75 | RU | Зарегистрировать сайт в каталоге, попасть в обзоры | 1-2 дня |
| 7 | **partnerkin.com** | 68 | RU | Экспертная статья о монетизации софт-каталогов | 1-2 недели |
| 8 | **mozilla.org** | 96 | EN,FR | Партнёрство по дистрибуции Firefox, аддоны | 1-3 месяца |
| 9 | **mdpi.com** | 92 | EN | Академическая публикация с упоминанием freesoft (если есть данные) | 3-6 месяцев |
| 10 | **cnil.fr** | 94 | FR | GDPR-compliance → упоминание как пример правильной политики | 3-6 месяцев |

#### Long Shots (очень высокий DR, мало шансов на прямую ссылку)

| # | Домен | DR | Почему Long Shot |
|---|---|---|---|
| 1 | google.com | 99 | Автоматические ссылки из SERP, не контролируемые |
| 2 | bing.com | 93 | Аналогично — индексация |
| 3 | apple.com | 97 | Только для App Store-листингов, freesoft не вендор |
| 4 | spotify.com | 95 | Нерелевантная ниша |
| 5 | yahoo.co.jp | 93 | Японский рынок, нецелевой |
| 6 | springer.com | 93 | Только через академическую публикацию |
| 7 | nih.gov | 95 | Здравоохранение, не наша ниша |
| 8 | nytimes.com | 94 | Нужен значимый инфоповод |

---

### Рекомендации

#### 1. [Quick Win — все языки] Запустить «Presence Pack» на UGC-платформах
**Действие:** Создать аккаунты/каналы на: GitHub, Telegram (t.me), Medium, Bluesky (bsky.app), Substack, Teletype.in (RU), SourceForge, Fandom (для популярных игр). Каждый профиль — со ссылкой на freesoft.net/freesoft.ru/frees0ft.fr.
**Почему:** 9 из 9 конкурентов имеют ссылки с GitHub, Telegram и YouTube. Это «стандарт отрасли». Отсутствие freesoft на этих платформах — аномалия.
**Ожидаемый результат:** 8-12 новых referring domains (DR 82-96) за 1-2 недели.

#### 2. [Quick Win — EN] Создать GitHub-проект с утилитой для скачивания/проверки ПО
**Действие:** Open-source инструмент (CLI/скрипт) для проверки APK, сравнения версий, или API для каталога freesoft. В README — ссылки на freesoft.net.
**Почему:** GitHub.com (DR 96) ссылается на 9/9 конкурентов. softonic имеет 57 ссылок, uptodown — 108. GitHub-ссылки — самый ценный тип UGC-ссылок (tech-аудитория, высокий DR).
**Ожидаемый результат:** 1-3 backlinks с github.com, потенциал для github.io упоминаний.

#### 3. [Quick Win — RU] Активная работа с ixbt.com и teletype.in
**Действие:** (a) Написать в редакцию ixbt.com предложение экспертного комментария о трендах в мобильных приложениях. (b) Начать регулярные публикации на teletype.in — обзоры ПО, сравнения, гайды.
**Почему:** ixbt.com (DR 78) — крупнейшее tech-медиа в рунете с 482K трафика. Trashbox.ru имеет 27 ссылок оттуда. Teletype.in (DR 82) — обе конкурента активны (softonic.ru: 19, trashbox: 17). Для freesoft.ru с DR 59 — идеальный уровень.
**Ожидаемый результат:** 2-5 backlinks за 1-2 месяца.

#### 4. [Среднесрочный — EN] Outreach к Wikipedia для добавления freesoft.net как источника
**Действие:** Идентифицировать статьи Википедии о популярном ПО (VPN, антивирусы, мессенджеры), где softonic.com уже указан как источник (161 ссылка). Предложить freesoft.net как альтернативный/дополнительный источник.
**Почему:** wikipedia.org (DR 97) ссылается на 8/9 конкурентов — это самая ценная ссылка в нише. Softonic имеет 161, uptodown — 102. Ссылки с Wikipedia дают и авторитет, и реферальный трафик.
**Ожидаемый результат:** 1-5 ссылок за 1-3 месяца (зависит от notability-политики).

#### 5. [Среднесрочный — FR] Bluesky + Substack стратегия для frees0ft.fr / нового FR-домена
**Действие:** Создать Bluesky-аккаунт (clubic=125, 01net=154 ссылок!) и Substack-рассылку на французском языке с обзорами ПО. Контент: «Les meilleures applications de la semaine», «Guide: comment choisir un VPN».
**Почему:** FR tech-сообщество массово на Bluesky (289 совокупных ссылок от конкурентов). Substack (57+46+1=104 ссылки) — второй по «плотности». Это самые быстрорастущие каналы FR-конкурентов.
**Ожидаемый результат:** 2-4 backlinks за 1-2 месяца, растущее community.
**ВАЖНО:** Запускать на новом домене ПОСЛЕ миграции. Если миграция не завершена — зарезервировать брендовые аккаунты с новым именем, но контент пока вести минимально.

#### 6. [Стратегический — EN] Закрыть gap с softonic.com (Jaccard 0.02)
**Действие:** Провести отдельный deep-dive в ссылочный профиль softonic.com (29 904 referring domains) и выявить «средний пояс» доменов (DR 30-70), которые ссылаются на softonic, но не на freesoft.net. Это вторичная задача после Quick Wins.
**Почему:** Jaccard 0.02 = 98% ссылочного профиля softonic.com — это «неосвоенная территория» для freesoft.net. Даже 5% penetration даст ~1 500 новых доменов.
**Ожидаемый результат:** Список из 100-200 actionable targets для постепенного outreach.

#### 7. [Стратегический — FR, постмиграция] Партнёрства с FR tech-экосистемой
**Действие:** После миграции домена — outreach к: (a) ovhcloud.com — технологическое партнёрство, (b) cnil.fr — попасть в каталог GDPR-compliant ресурсов, (c) techcrunch.com — FR-PR.
**Почему:** Все три FR-конкурента получают ссылки от этих ресурсов. Для нового домена важно сразу попасть в «правильный» контекст (tech, privacy, reviews), а не набирать спамные ссылки.
**Ожидаемый результат:** 3-5 high-authority backlinks за 3-6 месяцев.

---

### Методология и ограничения

- **Источники данных:** Ahrefs Referring Domains (отчёты A1-A12), Ahrefs Link Intersect (D1-D3).
- **Лимит Ahrefs:** EN и FR Link Intersect усечены на 30K доменов. Реальное количество target-доменов в EN и FR группах выше.
- **Gambling-фильтр:** Применён на этапе инвентаризации (9 900 строк отфильтровано). В настоящем отчёте gambling/adult-домены отсутствуют.
- **Jaccard Similarity** вычислена как |A intersect B| / |A union B| на основе referring domains каждого сайта.
- **Intersect count** из Link Intersect: количество конкурентов из группы, на которых ссылается данный домен (от 2 до числа конкурентов в группе).
- **Дата сбора данных:** 2026-03-13.

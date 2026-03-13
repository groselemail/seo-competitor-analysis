# Raw Data

Сырые данные Ahrefs (36 CSV + 15 PNG) не включены в репозиторий из-за размера.

## Как получить доступ

Файлы находятся в `pipeline-seo/data_for_task/` основного проекта:
- **36 CSV-файлов** (UTF-16LE с BOM, до 30K строк каждый)
- **15 PNG-скриншотов** (скриншоты дашбордов Ahrefs)

Полный перечень файлов: [data-inventory.md](../analysis/data-inventory.md)

## Конвертация CSV

CSV-файлы требуют конвертации из UTF-16LE в UTF-8 перед обработкой:
```bash
iconv -f UTF-16LE -t UTF-8 < input.csv | sed 's/\r$//' > output.csv
```

## Воспроизведение анализа

Для воспроизведения pipeline целиком:
1. Поместите CSV/PNG файлы в `data_for_task/`
2. См. [architecture.md](../methodology/architecture.md) — описание всех 29 задач
3. См. [pipeline-run.log](../methodology/pipeline-run.log) — лог оригинального запуска

---

## Phase 2: Ссылочные данные

**39 CSV-файлов Ahrefs** (ссылочные отчёты по 12 доменам, экспорт 2026-03-13).

Формат: UTF-16LE TSV (referring domains, anchors, backlinks) и UTF-8 CSV (link intersect).

**Нормализованные TSV-файлы** (~109 МБ) хранятся локально (не включены в репозиторий из-за размера). Для воспроизведения: скрипт нормализации в `analysis/backlink-strategy/pipeline/scripts/run_pipeline.py`.

**JSON-агрегаты** (результат агрегации, ~2.8 МБ) включены в репозиторий: `analysis/backlink-strategy/pipeline/intermediate/`.

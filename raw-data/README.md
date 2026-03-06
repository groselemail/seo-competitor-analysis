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

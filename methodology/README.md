# Методология

Как проведён анализ: 29 автоматических задач, 51 входной файл, Claude Opus.

## Файлы

| Файл | Описание |
|------|----------|
| [architecture.md](architecture.md) | Архитектура пайплайна анализа |
| [data-sources.md](data-sources.md) | Перечень источников данных |
| [pipeline-run.log](pipeline-run.log) | Лог выполнения пайплайна |
| [audit-report.md](audit-report.md) | Аудит качества результатов |
| [review-report.md](review-report.md) | Ревью результатов анализа |
| [review-1-report.md](review-1-report.md) | Ревью — раунд 1 |
| [review-2-report.md](review-2-report.md) | Ревью — раунд 2 |

---

## Ссылочный анализ (Phase 2)

- **Методология:** [reports/backlink-strategy/08-methodology.md](../reports/backlink-strategy/08-methodology.md)
- **Архитектура pipeline:** [analysis/backlink-strategy/docs/architecture.md](../analysis/backlink-strategy/docs/architecture.md)
- **Pipeline:** [analysis/backlink-strategy/pipeline/](../analysis/backlink-strategy/pipeline/)
- **Данные:** 39 CSV Ahrefs → Python/pandas → JSON-агрегаты → Claude AI → отчёты
- **Верификация:** 662 проверки, 99.4% pass rate

---

## Воспроизведение

Для воспроизведения анализа см. [raw-data](../raw-data/README.md) — исходные данные и инструкции.

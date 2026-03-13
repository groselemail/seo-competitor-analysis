# Проверка качества данных

Как убедиться, что выводы в отчётах основаны на реальных данных, а не на галлюцинациях модели.

## Файлы

| Файл | Описание |
|------|----------|
| [validation-report.md](validation-report.md) | Отчёт валидации: какие данные проверены, какие расхождения найдены |
| [briefs-validation.yaml](briefs-validation.yaml) | Проверка соответствия брифов исходным данным |
| [chain-of-evidence.md](chain-of-evidence.md) | Цепочка доказательств: от исходных данных до выводов в отчётах |

---

## Ссылочный анализ (Phase 2) — верификация

- **Автоматическая верификация:** 662 проверки числовых утверждений против JSON-агрегатов. 99.4% pass rate.
- **Audit report:** [reports/backlink-strategy/07-audit-report.md](../reports/backlink-strategy/07-audit-report.md)
- **Скрипт верификации:** [analysis/backlink-strategy/pipeline/scripts/verify_report.py](../analysis/backlink-strategy/pipeline/scripts/verify_report.py)
- **Результат:** PASS WITH WARNINGS (1 минорная ошибка исправлена, 3 предупреждения по PBN-scores)

---

## Как провести fact-check за 5 минут

1. Откройте [chain-of-evidence.md](chain-of-evidence.md) — найдите интересующий вывод и проследите ссылку до исходных данных.
2. Проверьте конкретную цифру в [briefs-validation.yaml](briefs-validation.yaml) — каждый brief сопоставлен с первоисточником.
3. Просмотрите [validation-report.md](validation-report.md) — в нём перечислены все найденные расхождения и их статус.
4. При необходимости сверьтесь с сырыми данными в [raw-data/](../raw-data/README.md).

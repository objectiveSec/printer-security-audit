# hp-joblog-parser

Небольшой скрипт для проверки экспортов HP Job Log.

Сделал его после случая, когда офисный HP-принтер начал печатать большое количество мусорных страниц.
В логах принтера было много заданий от `Guest` с `source_IP=0.0.0.0`.

Этот скрипт не ищет хакеров или что-то подобное.
Он просто помогает быстро проверить сохранённый/export-файл логов принтера и посчитать подозрительно выглядящие print jobs.

## Что проверяет

- jobs from `Guest`
- jobs with `source_IP=0.0.0.0`
- repeated users
- repeated source IPs
- total number of print jobs

## Example

```bash
python hp_joblog_parser.py examples/sample_log.txt
```

Example output:

```text
total jobs: 5
guest jobs: 4
0.0.0.0 jobs: 4

top users:
Guest: 4
petrov: 1

top source IPs:
0.0.0.0: 4
10.10.12.44: 1
```

## Для чего нужен

Когда принтер начинает печатать мусорные страницы, вручную разбирать Job Log неудобно.
Скрипт быстро показывает краткую статистику и помогает заметить большое количество заданий от `Guest` или `0.0.0.0`.

В моём случае это, скорее всего, было связано с direct printing, RAW/9100, зависшей очередью печати или проблемным драйвером.

## Files

```text
hp-joblog-parser/
├── README.md
├── hp_joblog_parser.py
└── examples/
    └── sample_log.txt
```

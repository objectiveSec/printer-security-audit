# hp-joblog-parser

Небольшой скрипт для проверки экспортов HP Job Log.

Сделал его после реального случая, когда офисный HP-принтер начал печатать большое количество мусорных страниц.
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

## Why this can be useful

When a printer starts printing garbage, the log can be hard to read manually.  
This script gives a quick summary, so it is easier to notice if many jobs come from `Guest` or `0.0.0.0`.

In my case this was probably related to direct printing, RAW/9100, a stuck print queue, or a broken driver.

## Files

```text
hp-joblog-parser/
├── README.md
├── hp_joblog_parser.py
└── examples/
    └── sample_log.txt
```

# hp-joblog-parser

Небольшой скрипт для проверки экспортов HP Job Log.

Сделал его после случая, когда офисный HP-принтер начал печатать большое количество мусорных страниц.
В логах принтера было много заданий от `Guest` с `source_IP=0.0.0.0`.

Этот скрипт помогает быстро проверить сохранённый/export-файл логов принтера и посчитать подозрительно выглядящие print jobs.

## Checks

- jobs from `Guest`
- jobs with `source_IP=0.0.0.0`
- repeated users
- repeated source IPs
- total number of print jobs

## Example

```bash
python hp_joblog_parser.py examples/sample_log.txt
```

Пример вывода:

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

## Application

Когда принтер начинает печатать мусорные страницы, вручную разбирать Job Log неудобно.
Скрипт быстро показывает краткую статистику и помогает заметить большое количество заданий от `Guest` или `0.0.0.0`.

В моём случае это было связано с direct printing, RAW/9100, зависшей очередью печати.

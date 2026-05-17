# hp-joblog-parser

Small script for checking HP printer Job Log exports.

I made this after a real case where an office HP printer started printing a lot of junk pages.  
In the printer logs there were many jobs from `Guest` with `source_IP=0.0.0.0`.

This script does not detect hackers or anything like that.  
It just helps to quickly check a saved/exported printer log and count suspicious-looking print jobs.

## What it checks

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

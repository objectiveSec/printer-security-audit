#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

USER_RE = re.compile(r'user[=:]"?([^",\s}]+)', re.IGNORECASE)
SOURCE_IP_RE = re.compile(r'source_IP[=:]"?([0-9a-fA-F:.]+)', re.IGNORECASE)
JOB_NAME_RE = re.compile(r'job_name[=:]"?([^",}]+)', re.IGNORECASE)
TIME_RE = re.compile(r'time[=:]"?([^",}]+)', re.IGNORECASE)

@dataclass
class PrintEvent:
    raw: str
    user: str
    source_ip: str
    job_name: str
    time: str

def find_value(pattern: re.Pattern[str], text: str, default: str = "unknown") -> str:
    match = pattern.search(text)
    if not match:
        return default
    value = match.group(1).strip().strip('"').strip("\\")
    return value if value else default

def parse_log(text: str) -> list[PrintEvent]:
    parts = re.split(r'(?=syslogMessage|Print job|user=|user")', text)
    events: list[PrintEvent] = []

    for part in parts:
        part = part.strip()
        if not part:
            continue

        lower = part.lower()
        if "print" not in lower and "job" not in lower:
            continue

        events.append(PrintEvent(
            raw=part,
            user=find_value(USER_RE, part),
            source_ip=find_value(SOURCE_IP_RE, part),
            job_name=find_value(JOB_NAME_RE, part),
            time=find_value(TIME_RE, part),
        ))

    return events

def risk_level(events: list[PrintEvent]) -> tuple[str, list[str]]:
    notes = []

    guest_jobs = sum(1 for event in events if event.user.lower() == "guest")
    zero_ip_jobs = sum(1 for event in events if event.source_ip == "0.0.0.0")
    empty_names = sum(1 for event in events if event.job_name in {"unknown", "\\", ""})

    if guest_jobs:
        notes.append(f"jobs from Guest: {guest_jobs}")
    if zero_ip_jobs:
        notes.append(f"jobs with source_IP=0.0.0.0: {zero_ip_jobs}")
    if empty_names:
        notes.append(f"jobs with empty or unknown name: {empty_names}")
    if len(events) >= 20:
        notes.append(f"many print-related events: {len(events)}")

    if zero_ip_jobs >= 5 or guest_jobs >= 10 or len(events) >= 50:
        return "high", notes
    if guest_jobs or zero_ip_jobs or len(events) >= 20:
        return "medium", notes
    return "low", notes

def make_report(events: list[PrintEvent]) -> str:
    level, notes = risk_level(events)

    users = Counter(event.user for event in events)
    ips = Counter(event.source_ip for event in events)
    jobs = Counter(event.job_name for event in events)

    out = []
    out.append("# Printer log report")
    out.append("")
    out.append(f"Risk level: **{level}**")
    out.append("")
    out.append("## Summary")
    out.append("")
    out.append(f"- parsed print events: {len(events)}")
    out.append(f"- Guest jobs: {sum(count for user, count in users.items() if user.lower() == 'guest')}")
    out.append(f"- source_IP=0.0.0.0: {ips.get('0.0.0.0', 0)}")
    out.append("")
    out.append("## Notes")
    out.append("")

    if notes:
        for note in notes:
            out.append(f"- {note}")
    else:
        out.append("- no obvious indicators in this sample")

    out.append("")
    out.append("## Users")
    out.append("")
    for user, count in users.most_common(10):
        out.append(f"- `{user}`: {count}")

    out.append("")
    out.append("## Source IPs")
    out.append("")
    for ip, count in ips.most_common(10):
        out.append(f"- `{ip}`: {count}")

    out.append("")
    out.append("## Job names")
    out.append("")
    for job, count in jobs.most_common(10):
        out.append(f"- `{job}`: {count}")

    out.append("")
    out.append("## What this probably means")
    out.append("")
    out.append("Guest and 0.0.0.0 do not prove domain compromise.")
    out.append("In many HP printer cases it points to direct printing, RAW/9100, a broken driver, a stuck spooler, or malformed print data.")
    out.append("")
    out.append("## Recommended next steps")
    out.append("")
    out.append("1. Save printer logs before clearing anything.")
    out.append("2. Check if Port 9100 / RAW printing is enabled.")
    out.append("3. Check print queues on workstations and print server.")
    out.append("4. If possible, allow print jobs only from the print server.")
    out.append("5. Disable direct IP printing where it is not needed.")
    out.append("6. Limit printer access with firewall or ACL rules.")
    out.append("")

    return "\n".join(out)

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("logfile")
    parser.add_argument("--out", default="printer_report.md")
    args = parser.parse_args()

    log_path = Path(args.logfile)
    if not log_path.exists():
        raise SystemExit(f"file not found: {log_path}")

    text = log_path.read_text(encoding="utf-8", errors="replace")
    events = parse_log(text)

    report = make_report(events)
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(report, encoding="utf-8")

    print(f"events parsed: {len(events)}")
    print(f"report saved: {out_path}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

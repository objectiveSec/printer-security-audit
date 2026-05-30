#!/usr/bin/env python
import re
import sys
from collections import Counter
from pathlib import Path

USER_RE = re.compile(r'user[=:]"?([^",\s}]+)', re.IGNORECASE)
SOURCE_IP_RE = re.compile(r'source_IP[=:]"?([0-9a-fA-F:.]+)', re.IGNORECASE)

def find_value(pattern, text, default="unknown"):
    match = pattern.search(text)
    if not match:
        return default
    return match.group(1).strip().strip('"').strip("\\")

def parse_log(text):
    jobs = []

    for line in text.splitlines():
        if "print" not in line.lower() and "job" not in line.lower():
            continue

        user = find_value(USER_RE, line)
        source_ip = find_value(SOURCE_IP_RE, line)

        jobs.append({
            "user": user,
            "source_ip": source_ip,
            "raw": line.strip()
        })

    return jobs

def main():
    if len(sys.argv) != 2:
        print("usage: python hp_joblog_parser.py <log_file>")
        return 1

    log_path = Path(sys.argv[1])

    if not log_path.exists():
        print(f"file not found: {log_path}")
        return 1

    text = log_path.read_text(encoding="utf-8", errors="replace")
    jobs = parse_log(text)

    users = Counter(job["user"] for job in jobs)
    source_ips = Counter(job["source_ip"] for job in jobs)

    guest_jobs = sum(1 for job in jobs if job["user"].lower() == "guest")
    zero_ip_jobs = sum(1 for job in jobs if job["source_ip"] == "0.0.0.0")

    print(f"total jobs: {len(jobs)}")
    print(f"guest jobs: {guest_jobs}")
    print(f"0.0.0.0 jobs: {zero_ip_jobs}")

    print("\ntop users:")
    for user, count in users.most_common(10):
        print(f"{user}: {count}")

    print("\ntop source IPs:")
    for ip, count in source_ips.most_common(10):
        print(f"{ip}: {count}")

    if guest_jobs or zero_ip_jobs:
        print("\nnote:")
        print("Guest or 0.0.0.0 in printer logs does not prove a compromise.")
        print("It may point to direct printing, RAW/9100, a stuck queue, or a broken driver.")

    return 0

if __name__ == "__main__":
    raise SystemExit(main())

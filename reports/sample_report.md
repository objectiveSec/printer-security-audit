# Printer log report

Risk level: **low**

## Summary

- parsed print events: 5
- Guest jobs: 0
- source_IP=0.0.0.0: 0

## Notes

- jobs with empty or unknown name: 4

## Users

- `unknown`: 5

## Source IPs

- `unknown`: 5

## Job names

- `unknown`: 4
- `invoice.pdf`: 1

## What this probably means

Guest and 0.0.0.0 do not prove domain compromise.
In many HP printer cases it points to direct printing, RAW/9100, a broken driver, a stuck spooler, or malformed print data.

## Recommended next steps

1. Save printer logs before clearing anything.
2. Check if Port 9100 / RAW printing is enabled.
3. Check print queues on workstations and print server.
4. If possible, allow print jobs only from the print server.
5. Disable direct IP printing where it is not needed.
6. Limit printer access with firewall or ACL rules.

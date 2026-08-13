# `datetime`

## 1. Core truth

The `datetime` module helps you represent dates and times.
It is useful for logs, reports, schedules, and automation tasks.

```python
from datetime import date

today = date(2026, 8, 9)
print(today.isoformat())
```

Output:

```text
2026-08-09
```

`isoformat()` converts the date to the standard `YYYY-MM-DD` format.

## 2. Date and time foundations

### Date values

```python
from datetime import date

day = date(2026, 8, 9)
print(day.year)
print(day.isoformat())
```

Output:

```text
2026
2026-08-09
```

### Time differences

```python
from datetime import timedelta

delta = timedelta(days=2, hours=3)
print(delta)
```

Output:

```text
2 days, 3:00:00
```

### Datetime arithmetic

```python
from datetime import datetime, timedelta

start = datetime(2026, 8, 9, 10, 0)
end = start + timedelta(hours=2, minutes=30)
print(end.isoformat(sep=" "))
```

Output:

```text
2026-08-09 12:30:00
```

## 3. Date and time APIs

- `date(...)`
- `time(...)`
- `datetime(...)`
- `timedelta(...)`
- `isoformat()`
- `strftime()`

```python
from datetime import date

day = date(2026, 8, 9)
print(day.strftime("%Y/%m/%d"))
```

Output:

```text
2026/08/09
```

## 4. Practical date processing

### Example 1: Print a date

```python
from datetime import date

print(date(2026, 8, 9).isoformat())
```

Output:

```text
2026-08-09
```

### Example 2: Add a duration

```python
from datetime import datetime, timedelta

start = datetime(2026, 8, 9, 9, 0)
print((start + timedelta(hours=1)).isoformat(sep=" "))
```

Output:

```text
2026-08-09 10:00:00
```

### Example 3: Format a date

```python
from datetime import date

day = date(2026, 8, 9)
print(day.strftime("%d-%m-%Y"))
```

Output:

```text
09-08-2026
```

- scheduled jobs and reminders;
- file naming with dates;
- time-based reports;
- measuring or shifting dates in automation scripts.

## 5. Date and time mistakes

### Mistake 1: Using current time when a fixed value is better for tests

### Mistake 2: Confusing `date` and `datetime`

### Mistake 3: Ignoring timezone issues in real systems

## 6. Type decision guide

| Need | Best choice | Why |
| --- | --- | --- |
| Calendar day only | `date` | simple and clear |
| Time of day only | `time` | no date attached |
| Date and time together | `datetime` | general scheduling |
| Duration | `timedelta` | arithmetic on time values |

## 7. Correctness and maintainability

- use fixed dates in examples and tests when possible;
- be explicit about timezone handling in real systems;
- format dates intentionally for humans or machines.

## 8. Advanced time behavior

- timezone-aware datetimes;
- parsing text into datetime objects;
- ISO 8601 formatting.

## 9. Mental model

| Concept | Remember |
| --- | --- |
| `date` | calendar day |
| `time` | clock time |
| `datetime` | both together |
| `timedelta` | duration |
| `strftime` | formatting |

## 10. Naive and aware datetimes

A naive `datetime` has no UTC offset. An aware `datetime` has a `tzinfo` that
can produce one. Do not compare or subtract a naive value and an aware value.

```python
from datetime import datetime, timezone

naive = datetime(2026, 1, 1, 12, 0)
aware = datetime(2026, 1, 1, 12, 0, tzinfo=timezone.utc)

try:
    print(aware - naive)
except TypeError as error:
    print(type(error).__name__)
```

Output:

```text
TypeError
```

Use aware UTC values for storage and interchange. Convert to a named local zone
only for display or rules that explicitly depend on civil time.

## 11. Named zones and DST ambiguity

`zoneinfo.ZoneInfo` uses IANA time-zone rules. Local clock times can be missing
during a forward transition or occur twice during a backward transition; the
`fold` attribute distinguishes the two repeated instants.

Time-zone data changes politically. Pin and update the `tzdata` package when the
operating system does not provide a suitable database, and test rules near
transitions.

## 12. Parsing, serialization, and elapsed time

```python
from datetime import datetime, timezone

instant = datetime(2026, 8, 13, 10, 30, tzinfo=timezone.utc)
encoded = instant.isoformat().replace("+00:00", "Z")
decoded = datetime.fromisoformat(encoded.replace("Z", "+00:00"))

print(encoded)
print(decoded == instant)
```

Output:

```text
2026-08-13T10:30:00Z
True
```

Use `time.monotonic()` or `time.perf_counter()` for elapsed durations and
deadlines. Wall-clock time can move because of synchronization or manual changes.

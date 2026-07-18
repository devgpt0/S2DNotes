# 07 - Date and Time API

## 1) Choose the Correct Type

- `Instant`: a machine timestamp in UTC.
- `LocalDate`: a date without time or zone.
- `LocalTime`: a time without date or zone.
- `LocalDateTime`: date and time without zone.
- `ZonedDateTime`: date and time in a region-based zone.
- `Duration`: time-based amount.
- `Period`: date-based amount.

```java
LocalDate date = LocalDate.of(2026, 7, 18);
System.out.println(date.plusDays(10));
// Output: 2026-07-28
```

## 2) Inject `Clock`

Code using the current time becomes deterministic in tests when it receives a `Clock`.

```java
Clock clock = Clock.fixed(Instant.parse("2026-07-18T10:15:30Z"), ZoneOffset.UTC);
System.out.println(Instant.now(clock));
// Output: 2026-07-18T10:15:30Z
```

## 3) Formatting and Strict Parsing

```java
DateTimeFormatter formatter = DateTimeFormatter
        .ofPattern("uuuu-MM-dd")
        .withResolverStyle(ResolverStyle.STRICT);
System.out.println(LocalDate.parse("2024-02-29", formatter));
// Output: 2024-02-29
```

Strict parsing rejects impossible dates instead of adjusting them.

## 4) Time Zones and Daylight Saving

```java
Instant instant = Instant.parse("2026-01-01T00:00:00Z");
ZonedDateTime india = instant.atZone(ZoneId.of("Asia/Kolkata"));
System.out.println(india.toLocalTime());
// Output: 05:30
```

Store timestamps as `Instant`; convert to a user’s zone for presentation.

## 5) Duration vs Period

```java
System.out.println(Duration.between(Instant.EPOCH, Instant.EPOCH.plusSeconds(90)).toSeconds());
System.out.println(Period.between(LocalDate.of(2026, 1, 1), LocalDate.of(2026, 2, 1)).getMonths());
// Output:
// 90
// 1
```

Never represent calendar months as a fixed number of seconds.

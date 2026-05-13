# Project 07: API Access Log Audit Tool

## Estimated Time
4 to 6 hours

## Goal
Build an audit tool for API access logs (common backend operation in Java services).

## Functional Requirements
- Parse API access logs:
  - timestamp
  - user/API key
  - endpoint
  - status code
- Generate audit reports:
  - top callers
  - top failing endpoints
  - 4xx/5xx counts
- Export report to JSON/text.

## Non-Functional Requirements
- Skip malformed lines safely.
- Provide total processed vs invalid lines.

## Concepts Practiced
- `Map<String, Integer>` counters
- nested map (`endpoint -> status -> count`)
- sorting map entries

## HLD
- `AccessLogParser`
- `AuditMetricsService`
- `ReportWriter`
- `Main`

## LLD
- `parseLine(line): Optional<AccessRecord>`
- `readAll(path): ParseResult`
- `topCallers(records, n): List<Entry<String,Integer>>`
- `topFailingEndpoints(records, n): List<Entry<String,Integer>>`
- `statusBucketCounts(records): Map<String, Integer>`

## Passing Criteria
- Report counts are correct.
- Invalid line handling works.
- Top lists are sorted properly.

## Implementation Roadmap
1. Build parser.
2. Build counters.
3. Build ranking outputs.
4. Write final report.

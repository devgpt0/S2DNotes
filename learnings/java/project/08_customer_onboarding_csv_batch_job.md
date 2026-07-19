# Project 08: Customer Onboarding CSV Batch Job

## Estimated Time
5 to 8 hours

## Goal
Create a batch onboarding process used in enterprise systems for bulk customer import.

## Functional Requirements
- Read customer CSV.
- Validate required fields (name, email, phone, country).
- Normalize values (trim, lowercase email).
- Detect duplicates by email/phone.
- Produce:
  - accepted customers file
  - rejected customers file with reasons
  - batch summary

## Non-Functional Requirements
- Must continue after row validation failure.
- Should report per-row errors.

## Concepts Practiced
- `List<CustomerRow>`
- `Set<String>` dedupe keys
- pipeline style row processing

## HLD
- `BatchReader`
- `ValidationService`
- `DedupService`
- `BatchWriter`
- `SummaryService`

## LLD
- `readCsv(path): List<Map<String,String>>`
- `validateRow(row): List<String>`
- `normalizeRow(row): Map<String,String>`
- `isDuplicate(row, seenEmail, seenPhone): boolean`
- `splitAcceptedRejected(rows): BatchResult`
- `writeOutputs(result): void`

## Passing Criteria
- Invalid rows captured with reasons.
- Duplicate rows detected correctly.
- Summary totals match input.

## Implementation Roadmap
1. Build CSV read logic.
2. Add row validators.
3. Add dedupe checks.
4. Build output files and summary.

# Project 10: Notification Queue Dispatcher

## Estimated Time
4 to 6 hours

## Goal
Build a notification dispatch module using queue processing (email/SMS/push simulation).

## Functional Requirements
- Enqueue notifications with type, target, message.
- Process queue in FIFO order.
- Retry failed dispatch up to N attempts.
- Move permanently failed items to dead-letter list.
- Generate dispatch summary.

## Non-Functional Requirements
- Queue operations must be reliable for edge cases.
- Processing should continue even if one item fails.

## Concepts Practiced
- `Queue<NotificationRecord>` (`LinkedList`)
- `List<NotificationRecord>` dead-letter
- `Map<String, Integer>` delivery stats

## HLD
- `QueueService`
- `DispatcherService`
- `RetryPolicyService`
- `ReportService`

## LLD
- `enqueue(queue, notification): void`
- `dispatchOne(notification): boolean`
- `processQueue(queue, deadLetter, stats): void`
- `retryOrDeadLetter(notification, maxRetries): void`
- `buildSummary(stats, deadLetter): Map<String, Object>`

## Passing Criteria
- FIFO processing validated.
- Retry count respected.
- Failed messages moved to dead-letter.
- Summary counts accurate.

## Implementation Roadmap
1. Build queue and models.
2. Add dispatch simulation.
3. Add retry + dead-letter handling.
4. Add summary report and test cases.

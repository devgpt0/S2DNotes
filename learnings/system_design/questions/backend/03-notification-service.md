# Design a Notification Service

> **Difficulty:** Medium  
> **Main focus:** fan-out, preferences, retries

## Interview prompt

Design a platform that sends push, email, SMS, and in-app notifications.

## 1. Clarify the scope

**What I would say first:** The core contract is accepted-for-delivery, not instantly delivered. I will separate durable intent from provider-specific attempts.

### Functional requirements

- Accept transactional and bulk notification requests.
- Respect user channel preferences, quiet hours, locale, and unsubscribe rules.
- Render versioned templates and send through multiple providers.
- Track accepted, sent, delivered, failed, and suppressed states.

### Out of scope for the first version

- A visual campaign editor and marketing segmentation engine are separate systems.

## 2. Estimate the scale

These are interview assumptions, not claims about a specific company:

- Assume 500 million notification intents per day with campaign spikes.
- Provider throughput and user-level frequency limits are the main bottlenecks.
- Payloads stay small; attempt history and retention dominate storage.

## 3. API and data model

### Main contracts

- POST /v1/notifications {recipientId, templateId, channels, variables, scheduleAt}
- GET /v1/notifications/{id}
- PUT /v1/users/{id}/preferences

### Important data

- Notification(id, recipient_id, template_version, status, scheduled_at, idempotency_key)
- Preference(user_id, channel, topic, enabled, quiet_hours, locale)
- DeliveryAttempt(notification_id, channel, provider, attempt, status, provider_message_id)

## 4. High-level design

```text
producer -> notification API -> intent database -> outbox -> scheduler/queue
                                                        |
user prefs + templates -> orchestrator -> channel queues
                                      -> email/SMS/push adapters -> providers
provider callbacks -> status API -> attempt store -> analytics
```

## 5. Critical request flow

1. Validate the template variables and persist one idempotent notification intent.
2. Outbox publishing guarantees the queue event follows the database commit.
3. At send time, re-check preferences, consent, quiet hours, and frequency caps.
4. Render the localized template, choose a healthy provider, and create an attempt.
5. Process provider callbacks idempotently and update delivery status.

## 6. Deep dive

- Use separate queues per channel and priority so a bulk email campaign cannot block password-reset SMS.
- Retry only transient failures with exponential backoff and jitter; permanent failures go to a reviewable dead-letter flow.
- Provider adapters translate a stable internal contract to vendor-specific APIs.
- Deduplicate at intent creation and again using provider idempotency when supported.

## 7. Scaling, failures, and observability

- Pause a failing provider with a circuit breaker and route to a secondary provider when allowed.
- Expired transactional messages are dropped instead of delivered late.
- Queue age, send latency, provider error rate, suppression rate, and delivery rate define operations.
- Reconciliation jobs compare provider callbacks with unresolved attempts.

## 8. Security and privacy

- Encrypt contact endpoints and restrict template variables containing personal data.
- Honor unsubscribe and deletion requirements before every send.
- Prevent template injection and never place secrets in notification bodies or logs.

## 9. Trade-offs

| Choice | Consequence |
|---|---|
| At-least-once queue | Reliable delivery intent but requires idempotent workers. |
| Exactly-once claim | Misleading across external providers; use deduplication instead. |
| Immediate preference snapshot | Fast, but may send after a later unsubscribe. |
| Send-time preference check | Safer compliance with an extra read. |

## 10. 60-second interview summary

I persist an idempotent notification intent, publish it through an outbox, then use priority channel queues and provider adapters. Preferences and consent are checked at send time, retries are bounded, and status callbacks are idempotent.

## Likely follow-up questions

- What breaks first at ten times the assumed traffic?
- Which operation needs strong consistency, and why?
- What happens when the main dependency times out after completing its work?
- Which metric best reflects the user's experience?


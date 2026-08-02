# Design a Ticket Booking System

> **Difficulty:** Hard  
> **Main focus:** high contention, holds, fairness

## Interview prompt

Design seat selection and purchase for concerts or travel during extreme demand.

## 1. Clarify the scope

**What I would say first:** The invariant is one confirmed ticket per seat. I will use short expiring holds and an atomic seat state transition.

### Functional requirements

- Browse events and seat availability.
- Hold selected seats briefly and complete payment.
- Prevent overselling under extreme contention.
- Expire abandoned holds and provide fair admission during spikes.

### Out of scope for the first version

- Event discovery and resale marketplace rules are separate designs.

## 2. Estimate the scale

These are interview assumptions, not claims about a specific company:

- Normal reads are moderate, but popular onsales create millions of users for a small seat set.
- Seat-map reads can be cached; final hold and confirmation cannot trust cache.
- A waiting room protects the transactional core.

## 3. API and data model

### Main contracts

- POST /v1/events/{id}/holds {seatIds} with Idempotency-Key
- POST /v1/holds/{id}/confirm {paymentToken}
- GET /v1/events/{id}/availability?section=...

### Important data

- Seat(event_id, seat_id, state, hold_id, hold_expires_at, version)
- Hold(hold_id, user_id, event_id, state, expires_at)
- Ticket(ticket_id, event_id, seat_id, owner_id, order_id)

## 4. High-level design

```text
users -> waiting room -> booking API -> seat partition owner -> seat database
                                       |                |
                                       |                +-> expiry queue
                                       +-> payment service
                                       +-> ticket/order database

seat snapshots -> cache/CDN -> browse clients
```

## 5. Critical request flow

1. Waiting room grants signed admission tokens at a controlled rate.
2. Hold request atomically changes every requested seat from available to held or fails as a unit.
3. Payment runs while the hold is valid.
4. Confirmation atomically verifies hold ownership and creates tickets.
5. Expiry worker releases only seats whose hold ID and expiry still match.

## 6. Deep dive

- Partition by event or section so one owner serializes contentious seat transitions.
- General-admission inventory uses atomic counters or numbered inventory tokens.
- Cache availability is advisory; the hold response is authoritative.
- Fairness policy may use a randomized queue rather than arrival order vulnerable to network advantage.

## 7. Scaling, failures, and observability

- If payment result is unknown, query the provider before releasing the hold.
- A late expiry message cannot release a seat held by a newer hold because it checks hold ID.
- Protect hot events with admission control, bounded queues, and bot mitigation.
- Monitor hold conflict, confirmation latency, expiry lag, payment unknowns, and queue wait.

## 8. Security and privacy

- Bind admission and hold tokens to authenticated users; rate-limit accounts and devices.
- Use server prices, signed tickets, audited transfers, and payment tokenization.
- Detect automation while maintaining accessibility paths.

## 9. Trade-offs

| Choice | Consequence |
|---|---|
| Database locks | Straightforward for moderate contention, limited at massive onsales. |
| Partition owner/queue | Predictable serialization with added architecture. |
| Long holds | Better user completion but worse inventory utilization. |
| Short holds | Fairer turnover with more checkout pressure. |

## 10. 60-second interview summary

Browse uses cached seat snapshots, but a seat-partition owner performs atomic expiring holds. Payment confirmation checks the same hold identity, expiry is idempotent, and a signed waiting room protects fairness and capacity during onsales.

## Likely follow-up questions

- What breaks first at ten times the assumed traffic?
- Which operation needs strong consistency, and why?
- How would you test recovery from a dependency timeout?
- Which metric best reflects the user's experience?


# Design E-commerce Inventory and Orders

> **Difficulty:** Hard  
> **Main focus:** reservations, sagas, overselling

## Interview prompt

Design checkout, inventory reservation, order state, payment, and fulfillment.

## 1. Clarify the scope

**What I would say first:** The key invariant is that confirmed reservations never exceed sellable stock. I will use a saga because inventory, payment, and fulfillment cannot share one database transaction.

### Functional requirements

- Create carts and submit idempotent checkout.
- Reserve limited inventory for a bounded time.
- Authorize payment and confirm an order.
- Release stock on timeout or failure and expose truthful order status.

### Out of scope for the first version

- Catalog search and recommendation ranking are separate systems.

## 2. Estimate the scale

These are interview assumptions, not claims about a specific company:

- Assume 100 thousand checkout attempts per second during major sales.
- Most products are ordinary; a few flash-sale SKUs become severe hot keys.
- Order history is write-once state transitions plus read-heavy customer queries.

## 3. API and data model

### Main contracts

- POST /v1/orders {cartId, addressId, paymentToken} with Idempotency-Key
- GET /v1/orders/{orderId}
- POST /v1/orders/{orderId}/cancel

### Important data

- Stock(sku_id, location_id, on_hand, reserved, version)
- Reservation(reservation_id, order_id, sku_id, quantity, expires_at, state)
- Order(order_id, user_id, total_minor, state, idempotency_key)

## 4. High-level design

```text
client -> checkout API -> order orchestrator -> order database
                                |             |
                                |             +-> inventory service -> stock database
                                |             +-> payment service
                                |             +-> fulfillment service
                                |
                                +-> durable workflow/events -> expiry workers
```

## 5. Critical request flow

1. Create one pending order using the idempotency key.
2. Reserve every SKU with an atomic conditional update: available stock must be sufficient.
3. Authorize payment only after all reservations succeed.
4. Confirm reservations and the order, then publish fulfillment work.
5. On any failure, compensate completed steps: void payment and release reservations.

## 6. Deep dive

- Use short reservation TTLs and an explicit state transition so expiration and confirmation cannot both win.
- For hot SKUs, serialize commands by SKU partition or pre-allocate stock tokens to shards.
- Never derive availability from a stale cache during the final reservation.
- A saga log records completed actions and makes compensation restartable.

## 7. Scaling, failures, and observability

- Payment timeout becomes pending reconciliation, not an immediate retry with a new key.
- Expiry workers are idempotent and re-scan overdue active reservations.
- Serve order reads from replicas only when state staleness is acceptable.
- Monitor oversell invariant, reservation age, checkout completion, compensation failures, and hot partitions.

## 8. Security and privacy

- Authorize carts and orders, validate prices on the server, and tokenize payment data.
- Rate-limit bots during scarce releases and maintain auditable admin adjustments.
- Protect addresses and order history as personal data.

## 9. Trade-offs

| Choice | Consequence |
|---|---|
| Pessimistic row locking | Simple correctness but poor hot-SKU throughput. |
| Optimistic version check | Scales normal traffic but retries under contention. |
| Queue per hot SKU | Predictable correctness with extra latency. |
| No reservations | Simpler, but payment may succeed after stock disappears. |

## 10. 60-second interview summary

Checkout is an idempotent saga. Inventory uses atomic expiring reservations, payment follows successful reservation, and every completed step has an idempotent compensation. Hot products move to serialized SKU partitions or token allocation.

## Likely follow-up questions

- What breaks first at ten times the assumed traffic?
- Which operation needs strong consistency, and why?
- How would you test recovery from a dependency timeout?
- Which metric best reflects the user's experience?


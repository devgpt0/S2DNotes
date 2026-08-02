# Design a Payment and Ledger System

> **Difficulty:** Hard  
> **Main focus:** money correctness, idempotency, reconciliation

## Interview prompt

Design a payment service that charges customers and records an auditable ledger.

## 1. Clarify the scope

**What I would say first:** The ledger is the source of financial truth. Every external payment call and internal command must be idempotent; balances are derived from immutable entries.

### Functional requirements

- Authorize, capture, refund, and query payments.
- Record balanced ledger entries in one atomic transaction.
- Prevent duplicate charges during retries.
- Reconcile internal records with payment processors and bank settlement.

### Out of scope for the first version

- Fraud model design is separate, but the payment flow must call its decision service.

## 2. Estimate the scale

These are interview assumptions, not claims about a specific company:

- Assume thousands of transactions per second with much higher read traffic.
- Correctness and auditability matter more than shaving a few milliseconds.
- Partitioning must preserve atomicity for accounts touched by one transaction.

## 3. API and data model

### Main contracts

- POST /v1/payments {merchantId, amountMinor, currency, paymentMethodToken} with Idempotency-Key
- POST /v1/payments/{id}/capture
- POST /v1/payments/{id}/refund {amountMinor}
- GET /v1/payments/{id}

### Important data

- Payment(payment_id, merchant_id, amount_minor, currency, state, idempotency_key, processor_ref)
- LedgerTransaction(transaction_id, type, effective_at, reference)
- LedgerEntry(transaction_id, account_id, direction, amount_minor, currency)

## 4. High-level design

```text
client -> payment API -> payment orchestrator -> payment database
                         |                 |
                         |                 +-> risk decision
                         |                 +-> processor adapter -> external processor
                         |
                         +-> atomic double-entry ledger

processor webhooks -> verified inbox -> state machine
settlement files -> reconciliation jobs -> exception queue
```

## 5. Critical request flow

1. Authenticate the merchant, validate integer minor units, and reserve the idempotency key.
2. Persist a payment state machine record before calling the processor.
3. Call the processor using its idempotency key; handle timeout as unknown, not failed.
4. On confirmed capture, atomically write equal debit and credit ledger entries.
5. Consume signed webhooks idempotently and reconcile later with settlement files.

## 6. Deep dive

- Ledger transactions are append-only; corrections use compensating entries.
- The sum of entries in each currency for one transaction must be zero.
- Store raw processor responses securely for investigation but expose a stable internal state machine.
- An unknown processor result is resolved by query or webhook before another charge attempt.

## 7. Scaling, failures, and observability

- Use an inbox table for webhooks so verification and processing survive restarts.
- Reconciliation reports missing, duplicated, and amount-mismatched records for controlled resolution.
- Back up and restore the ledger with point-in-time guarantees and regularly test recovery.
- Alert on invariant violations, unknown states, webhook lag, and reconciliation breaks.

## 8. Security and privacy

- Tokenize payment methods; keep card data out of application storage where possible.
- Use least privilege, dual control for sensitive operations, immutable audit logs, and encrypted fields.
- Do not log personal payment data or secrets; verify every processor webhook.

## 9. Trade-offs

| Choice | Consequence |
|---|---|
| Mutable balance only | Fast but weak auditability and difficult correction. |
| Double-entry ledger | More writes but clear invariants and history. |
| Synchronous processor call | Immediate result but timeout can be ambiguous. |
| Asynchronous completion | More resilient but product must display pending states. |

## 10. 60-second interview summary

I model payments as an idempotent state machine and keep an append-only double-entry ledger as the financial source of truth. Processor timeouts become unknown states, webhooks are durably ingested, and reconciliation catches every external mismatch.

## Likely follow-up questions

- What breaks first at ten times the assumed traffic?
- Which operation needs strong consistency, and why?
- What happens when the main dependency times out after completing its work?
- Which metric best reflects the user's experience?


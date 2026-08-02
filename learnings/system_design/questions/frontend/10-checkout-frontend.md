# Design a Resilient Checkout Frontend

> **Difficulty:** Medium  
> **Main focus:** state machine, idempotency, payment safety

## Interview prompt

Design a multi-step e-commerce checkout that remains correct under retries and partial failures.

## 1. Clarify the experience

**What I would say first:** Checkout is a server-backed state machine. The browser never calculates the authoritative price and never retries a payment with a new identity.

### Functional requirements

- Collect address, delivery, promotion, and tokenized payment details.
- Show authoritative price and inventory changes.
- Submit once safely despite double-clicks, refreshes, and timeouts.
- Resume pending checkout and display truthful final status.

### Browser and product constraints

- Payment and inventory can fail independently.
- Browser navigation or refresh may happen after the server commits.
- Third-party payment UI must be isolated and accessible.

## 2. State and API contracts

- POST /v1/checkout-sessions {cartId} -> session, version, priced summary
- PATCH /v1/checkout-sessions/{id} with expectedVersion
- POST /v1/orders {checkoutSessionId, paymentMethodToken} with Idempotency-Key
- GET /v1/orders/by-idempotency-key/{key}

## 3. Frontend architecture

```text
checkout route -> server-session query cache
      |
step state machine -> validated forms -> address/shipping APIs
      |
payment provider iframe/SDK -> payment token
      |
single submit controller -> order API -> pending/success/failure route
local storage keeps only safe resume identifiers
```

## 4. Critical user flow

1. Create or restore a server checkout session and render its authoritative summary.
2. Validate each step locally for usability and on the server for truth.
3. Tokenize payment data through the provider without storing raw card details.
4. Generate one idempotency key, disable duplicate submission, and persist the key safely for resume.
5. If the result times out, query by the same key and show pending until truth is known.

## 5. Deep dive

- The URL may represent the current step, while sensitive form values stay in component or secure provider state.
- Version checks detect price, stock, or shipping changes and return a deliberate review step.
- Do not optimistically show order success before the server confirms it.
- Route guards prevent losing entered data but never trap users with inaccessible dialogs.

## 6. Performance, resilience, and observability

- Preload the next step's small code and data without loading every payment integration upfront.
- Use field-level validation without rerendering the entire form per keystroke.
- Preserve safe session state across refresh; never persist payment secrets.
- Track checkout step drop-off, validation errors, price-change reviews, unknown submissions, and INP.

## 7. Security and accessibility

- Use hosted/tokenized payment fields, strong CSP, CSRF defenses, and server-side price validation.
- Mask personal data in telemetry and expire abandoned sessions.
- Provide explicit labels, error summaries, focus movement, autofill semantics, and screen-reader status updates.

## 8. Trade-offs

| Choice | Consequence |
|---|---|
| Client-only checkout state | Fast prototype but fragile across refresh and price changes. |
| Server checkout session | Resumable and authoritative with more API work. |
| Optimistic success | Feels fast but can lie about payment. |
| Pending state | Truthful under ambiguity but requires careful UX. |

## 9. 60-second interview summary

Checkout uses a versioned server session and explicit frontend state machine. Payment data is tokenized, one persisted idempotency key protects submission, and ambiguous timeouts become a resumable pending state rather than a duplicate order.

## Likely follow-up questions

- What state belongs in the URL, local UI, server cache, or durable local storage?
- What happens on a slow device with a flaky network?
- How do loading, empty, stale, partial-error, and retry states appear?
- Which Core Web Vital or product metric would reveal a bad release?


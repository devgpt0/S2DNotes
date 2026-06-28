# OOP and Clean Code Interview Case Studies

## 1) Case Study: Payment Processing

Problem:
- multiple payment providers
- retries
- logging
- notification on success/failure

Strong design:
- `PaymentGateway` abstraction
- provider-specific adapters
- `PaymentService` orchestration
- policy for retry/timeouts
- injected notifier/logger

Interview highlights:
- OCP for adding providers
- DIP via abstraction dependencies
- testability with fake gateways

## 2) Case Study: Notification System

Problem:
- email/sms/push channels
- per-user preferences
- fallback rules

Design:
- `Notifier` interface
- channel strategies
- preference resolver
- dispatcher coordinating channel selection

## 3) Case Study: Inventory Domain

Problem:
- reserve/release/ship flows
- state transitions
- concurrency concerns

Design:
- explicit domain methods (`reserve`, `release`, `ship`)
- invariants validated centrally
- repository abstraction for persistence

## 4) Case Study: Legacy God Class Refactor

Symptoms:
- one giant class with DB + business + API + formatting

Refactor steps:
1. add tests around current behavior
2. extract pure domain logic
3. extract data access adapter
4. extract formatting/presentation layer
5. wire with dependency injection

## 5) Case Study: Replace Conditionals with Polymorphism

Before:
- long `if order_type == ...` chains.

After:
- strategy class per order type implementing same contract.

Tradeoff:
- better extensibility
- slightly more classes; acceptable when behavior variations are real and stable.

## 6) Behavioral Interview Framing

When asked "design this system":
1. clarify invariants and boundaries
2. identify variation points
3. pick composition-first abstractions
4. explain failure-handling and test strategy
5. mention incremental evolution path

## 7) Quick Answer Templates

1. "I separate domain logic from infrastructure adapters to reduce coupling."
2. "I inject dependencies to keep services testable and replaceable."
3. "I prefer composition and strategy before inheritance unless subtype semantics are stable."
4. "I use contract tests to guarantee substitutability across implementations."

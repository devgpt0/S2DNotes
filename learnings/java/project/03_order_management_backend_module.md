# Project 03: Order Management Backend Module

## Estimated Time
5 to 7 hours

## Goal
Build backend order lifecycle logic used in e-commerce systems.

## Functional Requirements
- Create order with multiple line items.
- Order states:
  - `CREATED`
  - `CONFIRMED`
  - `PACKED`
  - `SHIPPED`
  - `DELIVERED`
  - `CANCELLED`
- Validate state transitions.
- Calculate total order value.
- Search orders by customer and status.

## Non-Functional Requirements
- Invalid transitions must be blocked.
- Keep audit trail of status changes.

## Concepts Practiced
- `Map<String, OrderRecord>`
- `List<OrderItem>`
- `List<String>` status history

## HLD
- `OrderService`
- `OrderStateMachine`
- `SearchService`
- `StorageService`

## LLD
- `createOrder(orderMap, order): String`
- `changeStatus(orderMap, orderId, newStatus): boolean`
- `isValidTransition(from, to): boolean`
- `calculateTotal(order): double`
- `findByStatus(orderMap, status): List<OrderRecord>`
- `findByCustomer(orderMap, customerId): List<OrderRecord>`

## Passing Criteria
- Status transitions enforce rules.
- Total value equals item sums.
- Search returns expected orders.

## Implementation Roadmap
1. Define order and item records.
2. Add create and total methods.
3. Add transition rules.
4. Add search and persistence.

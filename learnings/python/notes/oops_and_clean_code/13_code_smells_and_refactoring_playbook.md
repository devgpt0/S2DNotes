# Code Smells and Refactoring Playbook

## 1) High-Value OOP Smells

1. God class (too many responsibilities)
2. Long method with mixed concerns
3. Shotgun surgery (one change touches many classes)
4. Primitive obsession (no domain types)
5. Feature envy (method uses another object's data too much)
6. Deep inheritance tree without clear contract

## 2) Refactoring Principles

- preserve behavior while improving structure
- small safe steps
- tests first or in parallel

## 3) Practical Refactor Moves

1. Extract method
2. Extract class
3. Replace conditional with strategy/polymorphism
4. Introduce parameter object/value object
5. Introduce abstraction interface
6. Move method to more cohesive class

## 4) Safety Workflow

1. capture baseline behavior with tests
2. rename for clarity
3. split responsibilities
4. run tests each small step
5. stop when code is clearly simpler

## 5) Refactoring Example Pattern

Before:
- one `OrderManager` does validation, pricing, persistence, notifications.

After:
- `OrderValidator`
- `PricingService`
- `OrderRepository`
- `Notifier`
- orchestrating `OrderService`

## 6) Metrics to Watch (Signals, Not Absolute Rules)

- very long methods/classes
- high cyclomatic complexity
- high fan-in/fan-out coupling
- duplicate logic across modules

## 7) When Not to Refactor Immediately

- unstable requirements where abstraction likely to change tomorrow
- no test safety net for high-risk wide changes
- low-value internal code not on active paths

## 8) Interview Questions

1. How do you refactor safely in production?
2. How to detect over-abstraction?
3. When to replace if/elif chains with polymorphism?
4. What smells indicate SRP violation?

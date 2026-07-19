# 12 - Case Studies, Interview Questions, and Practice

## 1) Case Study: Discount Rules

```java
interface DiscountPolicy {
    int discountFor(int total);
}

record PercentageDiscount(int percent) implements DiscountPolicy {
    PercentageDiscount {
        if (percent < 0 || percent > 100) {
            throw new IllegalArgumentException("percent must be between 0 and 100");
        }
    }

    public int discountFor(int total) {
        return total * percent / 100;
    }
}

DiscountPolicy policy = new PercentageDiscount(10);
System.out.println(policy.discountFor(500));
// Output: 50
```

This design keeps validation with the value and pricing variation behind one small contract.

## 2) Case Study: Order State

```java
enum OrderStatus { CREATED, PAID, SHIPPED }

record Order(OrderStatus status) {
    Order pay() {
        if (status != OrderStatus.CREATED) {
            throw new IllegalStateException("only created orders can be paid");
        }
        return new Order(OrderStatus.PAID);
    }
}

System.out.println(new Order(OrderStatus.CREATED).pay().status());
// Output: PAID
```

The transition method prevents invalid lifecycle changes.

## 3) Interview Quick Answers

- Encapsulation protects invariants; private fields alone are insufficient.
- Abstraction hides irrelevant implementation details behind a useful contract.
- Polymorphism lets different implementations honor the same contract.
- Inheritance is appropriate only for true substitutability.
- Composition makes behavior independently replaceable.
- SOLID principles are design heuristics, not interface-count targets.
- An entity has identity; a value object is defined by its values.
- Constructor injection exposes required dependencies and improves testability.

## 4) Practice Tasks

1. Design an immutable `Money` value object with currency validation.
2. Refactor a payment type switch into strategies.
3. Split a report class that queries data, formats HTML, and sends email.
4. Demonstrate an LSP violation and redesign the abstraction.
5. Inject `Clock` into a subscription expiry service and test it deterministically.
6. Model an order lifecycle so invalid transitions fail immediately.

## 5) Review Checklist

- every class has one cohesive responsibility
- constructors establish valid objects
- mutable state is not exposed
- dependencies are explicit
- abstractions correspond to real variation or boundaries
- errors are deterministic and actionable
- names communicate domain intent
- no pattern or layer exists without a current need

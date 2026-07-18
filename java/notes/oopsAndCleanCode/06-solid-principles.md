# 06 - SOLID Principles

SOLID is a set of design signals, not a requirement to create an interface for every class.

Read SOLID as five questions, not five rules to apply everywhere:

1. Does this class have one cohesive job?
2. Can a real variation be added without repeatedly editing stable policy?
3. Can every subtype safely replace its parent contract?
4. Does a caller depend only on operations it needs?
5. Does high-level policy depend on replaceable boundaries rather than concrete infrastructure?

## 1) Single Responsibility

A class should have one cohesive reason to change.

```java
record Order(int amount) {}

final class TaxCalculator {
    int tax(Order order) {
        return order.amount() * 18 / 100;
    }
}

System.out.println(new TaxCalculator().tax(new Order(1000)));
// Output: 180
```

## 2) Open/Closed

Extend behavior through a stable contract when variants are genuinely expected.

```java
interface PricingRule {
    int price(int basePrice);
}

PricingRule regular = basePrice -> basePrice;
PricingRule sale = basePrice -> basePrice * 90 / 100;
System.out.println(regular.price(100) + ", " + sale.price(100));
// Output: 100, 90
```

## 3) Liskov Substitution

Implementations must preserve the abstraction’s contract. A subtype that rejects valid parent operations is a design warning.

## 4) Interface Segregation

```java
interface Printable {
    String print();
}

record Receipt(int total) implements Printable {
    public String print() {
        return "total=" + total;
    }
}

System.out.println(new Receipt(250).print());
// Output: total=250
```

Clients depend only on capabilities they use.

## 5) Dependency Inversion

High-level policy depends on an abstraction supplied from outside.

```java
interface AuditSink {
    void record(String event);
}

final class LoginService {
    private final AuditSink auditSink;

    LoginService(AuditSink auditSink) {
        this.auditSink = auditSink;
    }

    void login(String user) {
        auditSink.record("login:" + user);
    }
}

LoginService service = new LoginService(System.out::println);
service.login("Asha");
// Output: login:Asha
```

Add abstraction at a boundary where replacement or isolation is valuable, not by habit.

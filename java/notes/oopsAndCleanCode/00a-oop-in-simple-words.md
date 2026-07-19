# OOP and Clean Code in Simple Words

Read this before the detailed OOP chapters.

## Why Does OOP Exist?

A large program has data and rules that belong together.

For a bank account:

- data: owner and balance
- rules: deposit must be positive; withdrawal cannot exceed the balance

OOP lets one object protect that data and provide safe operations.

## First Object

```java
final class BankAccount {
    private int balance;

    BankAccount(int openingBalance) {
        if (openingBalance < 0) {
            throw new IllegalArgumentException("opening balance cannot be negative");
        }
        balance = openingBalance;
    }

    void deposit(int amount) {
        if (amount <= 0) {
            throw new IllegalArgumentException("deposit must be positive");
        }
        balance += amount;
    }

    int balance() {
        return balance;
    }
}

BankAccount account = new BankAccount(100);
account.deposit(50);
System.out.println(account.balance());
// Output: 150
```

## Read It in Simple Language

- `class`: defines a kind of object
- `object`: one value created from a class
- `private`: outside code cannot directly change the field
- `constructor`: creates a valid object
- `method`: operation the object allows
- `throw`: stop the current operation because input is invalid

The important design idea is not “put everything in classes.” It is: keep data close to the rules that protect it.

## Encapsulation

Encapsulation means an object protects its valid state.

Bad design would let any code write a negative balance. Better design keeps `balance` private and exposes operations that check the rules.

The rule that must always remain true is called an **invariant**.

## Composition

Composition means one object uses another object.

```java
final class CheckoutService {
    private final PaymentGateway paymentGateway;

    CheckoutService(PaymentGateway paymentGateway) {
        this.paymentGateway = paymentGateway;
    }
}
```

Read it as: “Checkout has a payment gateway.”

Composition is usually easier to change and test than a deep inheritance tree.

## Inheritance and Polymorphism

Inheritance means one type is a more specific version of another type.

```java
interface Shape {
    double area();
}

record Circle(double radius) implements Shape {
    public double area() {
        return Math.PI * radius * radius;
    }
}
```

A `Circle` can be used wherever the program expects a `Shape`. That is polymorphism: the caller uses one contract while different objects provide the behavior.

Use inheritance for a real “is-a” contract, not only to reuse code.

## Abstraction

Abstraction shows what a caller needs and hides unnecessary detail.

A `PaymentGateway.charge(...)` method should explain the operation. The caller should not need to know socket, JSON, or retry details.

Good abstraction reduces what a reader must hold in their head.

## Clean Code

Clean code is code whose purpose and rules are easy to see.

Prefer:

- names that explain meaning
- small methods that do one job
- early validation
- explicit control flow
- few dependencies
- tests around behavior

Avoid creating an interface, factory, base class, or pattern until it solves a real problem.

## SOLID Without Memorizing First

- **S:** one class has one clear reason to change
- **O:** new behavior can be added without editing stable decision code everywhere
- **L:** a subtype keeps the promises of its parent contract
- **I:** callers depend on small contracts they actually use
- **D:** important policy depends on a contract, not a replaceable detail

Learn the examples in the SOLID chapter before memorizing the names.

## Patterns

A design pattern is a named solution shape for a repeated design problem.

Do not start with “Which pattern can I add?” Start with:

1. What is changing?
2. What must remain stable?
3. Which object owns each rule?
4. Is a pattern simpler than direct code?

## Beginner to Expert Path

1. **Beginner:** create classes and valid objects.
2. **Developer:** protect invariants, prefer composition, and test behavior.
3. **Senior:** design small contracts and clear dependency direction.
4. **Expert:** recognize coupling, choose patterns only when useful, and evolve systems safely.

You are ready for the detailed notes when you can explain why `balance` is private, why invalid deposits throw, and why `CheckoutService` receives its gateway through the constructor.

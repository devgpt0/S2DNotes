# 03 - Inheritance and Composition

## 1) Inheritance Models an Is-A Relationship

```java
abstract class Shape {
    abstract double area();
}

final class Circle extends Shape {
    private final double radius;

    Circle(double radius) {
        if (radius <= 0) {
            throw new IllegalArgumentException("radius must be positive");
        }
        this.radius = radius;
    }

    @Override
    double area() {
        return Math.PI * radius * radius;
    }
}

System.out.printf("%.2f%n", new Circle(2).area());
// Output: 12.57
```

Subclasses must honor every promise made by the base type.

## 2) Composition Models Has-A Behavior

```java
interface Discount {
    int apply(int price);
}

final class Checkout {
    private final Discount discount;

    Checkout(Discount discount) {
        this.discount = Objects.requireNonNull(discount);
    }

    int total(int price) {
        return discount.apply(price);
    }
}

Checkout checkout = new Checkout(price -> price - 10);
System.out.println(checkout.total(100));
// Output: 90
```

Composition makes behavior replaceable without inheriting implementation details.

## 3) Prefer Composition When

- behavior must vary independently
- only part of another class is needed
- inheritance would expose unwanted methods
- subclass behavior might violate parent assumptions
- runtime replacement improves testing or configuration

## 4) Use Inheritance When

- the subtype truly is substitutable for the parent
- the base contract is stable and intentionally designed for extension
- shared polymorphism matters more than code reuse

Do not inherit solely to reuse a few lines of code. Extract a focused collaborator instead.

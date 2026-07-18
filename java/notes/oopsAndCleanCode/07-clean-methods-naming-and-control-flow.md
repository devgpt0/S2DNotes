# 07 - Clean Methods, Naming, and Control Flow

## 1) Use Intention-Revealing Names

```java
static boolean isEligibleForDiscount(int completedOrders) {
    return completedOrders >= 10;
}

System.out.println(isEligibleForDiscount(12));
// Output: true
```

`isEligibleForDiscount` communicates more than `check` or `process`.

## 2) Fail Fast with Guard Clauses

```java
static int divide(int dividend, int divisor) {
    if (divisor == 0) {
        throw new IllegalArgumentException("divisor must not be zero");
    }
    return dividend / divisor;
}

System.out.println(divide(10, 2));
// Output: 5
```

Guard clauses keep the valid path unindented and obvious.

## 3) One Level of Abstraction

```java
static int checkoutTotal(List<Integer> prices) {
    if (prices.isEmpty()) {
        return 0;
    }
    return prices.stream().mapToInt(Integer::intValue).sum();
}

System.out.println(checkoutTotal(List.of(20, 30)));
// Output: 50
```

A method should have a focused purpose. Extract code when it names a distinct idea, removes meaningful duplication, or makes testing easier.

## 4) Avoid Boolean Mystery Arguments

```java
enum DeliverySpeed { STANDARD, EXPRESS }

static int deliveryDays(DeliverySpeed speed) {
    return switch (speed) {
        case STANDARD -> 5;
        case EXPRESS -> 1;
    };
}

System.out.println(deliveryDays(DeliverySpeed.EXPRESS));
// Output: 1
```

The enum makes the call self-explanatory.

## 5) Clean Code Checklist

- names express domain intent
- methods are small and cohesive
- invalid input is rejected immediately
- no hidden mutation or surprising side effects
- constants replace unexplained magic values
- comments explain why, not what obvious code does
- duplication is removed only when the shared concept is stable

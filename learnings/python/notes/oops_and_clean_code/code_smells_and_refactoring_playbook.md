# Code Smells and Refactoring Playbook
## 1. Core truth

A code smell is a sign that code may be harder to understand, test, or change than it should be.
It is not always a bug, but it is often a warning.

```python
def shipping_cost(weight_kg: float) -> float:
    if weight_kg <= 1:
        return 5.0
    return 5.0 + (weight_kg - 1) * 2.0

print(shipping_cost(3.0))
```

Output:

```text
9.0
```

The first kilogram costs `5.0`, and the extra `2.0` kilograms cost `2.0 * 2.0 = 4.0`.

## 2. Refactoring foundations

### Refactor behavior, not guesses

Do not change structure just because it looks different.
Change structure because it clearly helps readability, testability, or maintainability.

### Use tests as safety rails

If the behavior is important, capture it before changing structure.

### Prefer small steps

One rename, one extraction, one responsibility split at a time is easier to verify.

## 3. Refactoring operations

### Extract method

Use when one function contains a clearly named subtask.

### Extract class

Use when one class is doing too much.

### Replace conditional with strategy

Use when one `if/elif` chain represents several real behaviors.

### Introduce value object or parameter object

Use when primitive values are hiding important domain meaning.

### Move method

Use when a method mostly uses another object's data and belongs there.

### Introduce abstraction

Use when multiple implementations need the same contract.

## 4. Practical refactoring workflow

### Example 1: Extract a method from a long function

```python
def format_total(price: float, tax_rate: float) -> str:
    tax = price * tax_rate
    total = price + tax
    return f"total={total:.2f}"

print(format_total(100.0, 0.1))
```

Output:

```text
total=110.00
```

### Example 2: Replace a conditional with strategy behavior

```python
class StandardShipping:
    def cost(self, weight_kg: float) -> float:
        return 5.0 + max(0.0, weight_kg - 1) * 2.0

class ExpressShipping:
    def cost(self, weight_kg: float) -> float:
        return 12.0 + max(0.0, weight_kg - 1) * 3.0

print(StandardShipping().cost(3.0))
print(ExpressShipping().cost(3.0))
```

Output:

```text
9.0
18.0
```

### Example 3: Replace primitive obsession with a value object

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Money:
    amount: float
    currency: str

money = Money(10.0, "USD")
print(money)
```

Output:

```text
Money(amount=10.0, currency='USD')
```

- Split validation, persistence, and notification into separate classes.
- Replace repeated conditionals with clearer behavior objects.
- Introduce domain types for money, ids, dates, and quantities.
- Keep the public API stable while improving internals.

## 5. Refactoring mistakes

### Mistake 1: Refactoring without tests

You may break behavior and not notice.

### Mistake 2: Over-abstracting too early

Not every `if` statement needs a strategy class.

### Mistake 3: Refactoring unstable code too aggressively

If requirements are still moving, keep the design simple.

### Mistake 4: Treating smell detection as a rigid formula

Smells are signals. Judgment still matters.

## 6. Refactoring decision guide

| Smell | Likely fix | Why | Avoid when |
| --- | --- | --- | --- |
| God class | extract class | reduces responsibility load | the class is still small |
| Long method | extract method | easier to read and test | the method is already clear |
| Shotgun surgery | move behavior closer to data | reduces spread | the change is truly rare |
| Primitive obsession | value object | adds domain meaning | the value is truly trivial |
| Feature envy | move method | improves cohesion | the dependency is temporary |

Selection rule:

- If a code change keeps touching many places, look for a design split.
- If a function is too long, look for named substeps.
- If plain primitives hide domain meaning, consider a value object.

## 7. Safety and maintainability

- Refactoring should preserve behavior.
- Small changes are easier to review and safer to deploy.
- Do not rename or split code in ways that make it harder to follow.
- Keep the refactoring aligned with actual usage, not theoretical elegance.

Best practices:

- Add tests before risky structural changes.
- Keep the public API stable if possible.
- Stop when the code is clearly simpler, not when it is maximally abstract.

## 8. Advanced refactoring boundaries

### Behavioral versus structural change

Refactoring changes structure.
Feature work changes behavior.
Keep those concerns separate when possible.

### Incremental refactoring

Large improvements should be broken into small reviewable steps.

## 9. Mental model

| Smell | Refactor move |
| --- | --- |
| God class | extract class |
| Long method | extract method |
| Shotgun surgery | move behavior / split responsibility |
| Primitive obsession | introduce value object |
| Feature envy | move method |
| Repeated conditionals | strategy or polymorphism |

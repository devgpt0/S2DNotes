# 12 - Practice Problems (With Direction)

Solve in order. Try first, then verify output manually.

## Beginner

1. Create `Predicate<Integer>` to test even numbers.
2. Create `Function<String, Integer>` to return string length.
3. Use `Consumer<String>` to print uppercase text.
4. Replace anonymous `Runnable` with lambda.

## Intermediate

1. Sort list of employees by salary descending using lambda.
2. Use `removeIf` to remove all short strings from list.
3. Build word frequency map using `merge`.
4. Convert list of names to uppercase using streams.
5. Group strings by first character using collectors.

## Advanced

1. Build reusable validator chain using predicate composition.
2. Implement `withRetry` utility accepting lambda and retry count.
3. Write wrapper to convert checked exception lambda to unchecked.
4. Build mini rule engine: list of predicates and actions.
5. Create cache decorator around `Function<T, R>` with `ConcurrentHashMap`.

## Expert Challenge

Given a list of transactions:

- filter only successful transactions
- group by user
- find total amount per user
- return top 3 users by total amount

Use stream + lambda only (no manual loops).


# Probability and Expected Value

## Idea

Probabilities of disjoint outcomes add; independent event probabilities
multiply. Expected value is linear even when variables are not independent:

```text
E[X + Y] = E[X] + E[Y]
```

## Visual model

For independent biased coins, DP stores the probability of exactly `k` heads
after processing some coins.

## Classroom board: two fair coins

```text
after first: P(0 heads)=1/2, P(1)=1/2
after second:
P(0)=1/4
P(1)=1/4 + 1/4 = 1/2
P(2)=1/4
```

Each old state branches into tail and head outcomes.

## Steps

1. Start with probability `1` of zero heads.
2. For each coin with head probability `p`, create a fresh distribution.
3. Add `old[k] * (1-p)` to `new[k]`.
4. Add `old[k] * p` to `new[k+1]`.

## First-principles derivation

Probability adds over mutually exclusive outcomes. Expected value is a weighted
average and, crucially, expectations add even when variables are dependent.

Indicator variables turn “how many events happen?” into a sum of simple
zero-or-one variables.

## Classroom board: expected heads in two tosses

```text
outcome  probability  heads
HH       1/4          2
HT       1/4          1
TH       1/4          1
TT       1/4          0

E[heads] = (2 + 1 + 1 + 0) / 4 = 1
```

Indicator view:

```text
E[first is head] + E[second is head]
= 1/2 + 1/2
= 1
```

## Pattern recognition

Use probability DP when random steps create a small state. Use indicator
variables and linearity when the answer is a sum of events.

## Implementation: distribution of the number of heads

### C++

```cpp
std::vector<double> headDistribution(const std::vector<double>& probability) {
    std::vector<double> distribution(probability.size() + 1, 0.0);
    distribution[0] = 1.0;
    int processed = 0;
    for (double heads : probability) {
        std::vector<double> next(probability.size() + 1, 0.0);
        for (int count = 0; count <= processed; ++count) {
            next[count] += distribution[count] * (1.0 - heads);
            next[count + 1] += distribution[count] * heads;
        }
        distribution = std::move(next);
        ++processed;
    }
    return distribution;
}
```

### Python

```python
def head_distribution(probability: list[float]) -> list[float]:
    distribution = [1.0] + [0.0] * len(probability)
    for processed, heads in enumerate(probability):
        next_distribution = [0.0] * (len(probability) + 1)
        for count in range(processed + 1):
            next_distribution[count] += distribution[count] * (1.0 - heads)
            next_distribution[count + 1] += distribution[count] * heads
        distribution = next_distribution
    return distribution
```

### Java

```java
static double[] headDistribution(double[] probability) {
    double[] distribution = new double[probability.length + 1];
    distribution[0] = 1.0;
    for (int processed = 0; processed < probability.length; processed++) {
        double[] next = new double[probability.length + 1];
        for (int count = 0; count <= processed; count++) {
            next[count] += distribution[count] * (1.0 - probability[processed]);
            next[count + 1] += distribution[count] * probability[processed];
        }
        distribution = next;
    }
    return distribution;
}
```

## Why it works

The last coin is either tail or head; these outcomes are disjoint and cover all
possibilities. Multiplication applies because each coin is independent.

## Complexity

Time is `O(n^2)` and space is `O(n)`.

## Common mistakes

- Adding probabilities of overlapping events.
- Multiplying probabilities without independence.
- Comparing floating-point answers for exact equality.
- Forgetting expected time equations often include the current step itself.

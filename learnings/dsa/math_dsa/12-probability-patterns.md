# Probability and Expectation Patterns: Worked Contest Questions

Use this note after [probability and games](08-probability-games.md). Keep
probabilities as exact fractions while reasoning; convert to a prime modulus
only when the statement explicitly asks for it.

## 1. Uniform sample space

**Question.** Two fair six-sided dice are rolled. What is the probability that
their sum is 7?

**Solution.** There are 6 * 6 = 36 equally likely ordered outcomes. The six
favorable outcomes are (1,6) through (6,1), so probability is 6/36 = 1/6.

Do not use favorable divided by total unless all elementary outcomes truly have
equal probability.

## 2. At least one: count the complement

**Question.** Roll a fair die four times. What is the probability of at least
one 6?

**Solution.** No roll is 6 with probability (5/6)^4. Therefore the answer is
1 - (5/6)^4 = 671/1296.

For independent trials, multiply the complement probabilities. Without
independence, this shortcut is invalid.

## 3. Conditional probability

**Question.** Two fair dice are rolled. Given that their sum is even, what is
the probability that both values are equal?

**Solution.** There are 18 even-sum outcomes: both dice odd or both even. The
favorable equal outcomes are (1,1), (2,2), through (6,6), so the conditional
probability is 6/18 = 1/3.

Use P(A given B) = P(A and B) / P(B), with P(B) > 0. Restrict both numerator
and denominator to the condition; do not divide by the original sample size.

## 4. Sampling without replacement

**Question.** A bag has 3 red and 2 blue balls. Draw 2 without replacement.
What is the probability that both are red?

**Solution.** Choose the two red balls from the three red balls and divide by
all unordered two-ball selections: C(3,2) / C(5,2) = 3/10.

Sequential multiplication gives the same answer: (3/5) * (2/4). Unlike
replacement, the second draw probability changes after the first draw.

## 5. Binomial distribution: fixed number of successes

**Question.** A fair coin is flipped 3 times. What is the probability of
exactly 2 heads?

**Solution.** Choose the two head positions, then multiply one sequence's
probability: C(3,2) * (1/2)^2 * (1/2)^1 = 3/8.

~~~python
from fractions import Fraction
from math import comb


def exactly_successes(trials: int, successes: int, success_probability: Fraction) -> Fraction:
    if trials < 0 or successes < 0 or successes > trials or not 0 <= success_probability <= 1:
        raise ValueError("invalid trial count, success count, or probability")
    return (
        comb(trials, successes)
        * success_probability**successes
        * (1 - success_probability) ** (trials - successes)
    )


print(exactly_successes(3, 2, Fraction(1, 2)))
~~~

Output:

~~~text
3/8
~~~

The binomial formula requires independent trials with the same success
probability. Otherwise use state DP.

## 6. Total probability and Bayes

**Question.** One of two coins is chosen uniformly. Coin A has head probability
1/2; Coin B has head probability 3/4. A flip is heads. What is the probability
Coin B was chosen?

**Solution.** P(heads) = (1/2)(1/2) + (1/2)(3/4) = 5/8. Thus
P(B given heads) = ((1/2)(3/4)) / (5/8) = 3/5.

Partition the hidden cause first, then sum its contributions. Bayes reverses a
conditional probability; it is not the same as P(heads given B).

## 7. Geometric expectation

**Question.** Repeatedly roll a fair die until a 6 appears. What is the
expected number of rolls?

**Solution.** Every independent roll succeeds with probability p = 1/6, so the
expected trial count is 1/p = 6. This includes the successful roll.

If probability changes with state, derive E[state] = 1 + sum(P(next) * E[next])
instead. A geometric formula cannot model changing probabilities.

## 8. Linearity of expectation and indicators

**Question.** A uniformly random permutation of 5 values is formed. What is
the expected number of inversions?

**Solution.** For each of the C(5,2) = 10 pairs, make an indicator that is one
when the pair is inverted. Each has expectation 1/2, so the expected total is
10 * 1/2 = 5. Pair indicators are dependent, but linearity still applies.

~~~python
from fractions import Fraction


def expected_inversions(size: int) -> Fraction:
    if size < 0:
        raise ValueError("size must be non-negative")
    return Fraction(size * (size - 1), 4)


print(expected_inversions(5))
~~~

Output:

~~~text
5
~~~

This pattern also counts expected matching positions, occupied bins, and
successful events: sum the probability of each indicator being one.

## 9. Probability DP

**Question.** A fair coin is flipped 3 times. What is the probability of ending
with exactly 2 heads if the number of flips is the DP state?

**Solution.** Let dp[h] be the probability of h heads after the current number
of flips. Each flip sends half of dp[h] to h and half to h + 1. The final value
is 3/8.

~~~python
from fractions import Fraction


def head_distribution(flips: int) -> list[Fraction]:
    if flips < 0:
        raise ValueError("flips must be non-negative")
    distribution = [Fraction(1)]
    for _ in range(flips):
        next_distribution = [Fraction(0)] * (len(distribution) + 1)
        for heads, probability in enumerate(distribution):
            next_distribution[heads] += probability / 2
            next_distribution[heads + 1] += probability / 2
        distribution = next_distribution
    return distribution


print(head_distribution(3)[2])
~~~

Output:

~~~text
3/8
~~~

Use DP when next probability, allowed transitions, or stopping condition depends
on state. For a prime-modulus answer, replace fractions with modular inverses
only after every denominator is known to be invertible.

## 10. Expected time on a finite state graph

For an absorbing process, set E[terminal] = 0. Every other state satisfies
E[state] = 1 + sum(P(state -> next) * E[next]). If transitions only move
forward, evaluate backward with DP. If they can cycle, solve simultaneous
linear equations with [Gaussian elimination](10-linear-algebra-transforms.md).

## Pattern checklist

- Equal elementary outcomes: favorable divided by total.
- At least one: usually complement; verify independence before multiplying.
- Given information: condition both numerator and denominator.
- Without replacement: probabilities change; combinations often simplify it.
- Fixed success count: binomial only for identical independent trials.
- Expected total: introduce indicators and use linearity.
- State-dependent randomness or cycles: probability/expectation DP or equations.


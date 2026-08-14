# PnC Patterns: Worked Contest Questions

Use this note after [combinatorics](04-combinatorics.md). Each section is a
recurring contest pattern: identify the objects first, then apply its count.

## 1. Sum rule versus product rule

**Question.** A code is either one uppercase letter or one digit. How many
valid one-character codes exist?

**Solution.** The alternatives cannot both occur, so add: 26 + 10 = 36.
For consecutive independent choices, multiply instead. A letter followed by a
digit has 26 * 10 = 260 choices.

Use a sum for disjoint cases and a product for a sequence of choices. If cases
overlap, make them disjoint or use inclusion-exclusion.

## 2. Choose versus arrange

**Question.** Choose a captain and vice-captain from 8 students.

**Solution.** Roles make order matter: 8 * 7 = 56. Choosing an unordered
two-person committee would be C(8, 2) = 28.

| Wording | Count |
| --- | --- |
| team, subset, pair | C(n, r) |
| rank, position, ordered sequence | n! / (n-r)! |

## 3. Repeated objects (multinomial)

**Question.** How many distinct strings can be made from BANANA?

**Solution.** There are 6 positions, with three identical A values and two
identical N values: 6! / (3! * 2!) = 60. Divide once for every group of
indistinguishable objects.

## 4. Adjacent items: make a block

**Question.** In how many ways can A, B, C, D be arranged with A and B
adjacent?

**Solution.** Treat AB as one block. The block can be AB or BA, and there
are 3! ways to arrange that block with C and D: 2 * 3! = 12.

Use a block only when the items must be consecutive. For not adjacent, count
all arrangements and subtract the adjacent arrangements when that complement is
simpler.

## 5. No adjacency: use gaps

**Question.** Place 3 identical A values and 2 identical B values so no two A
values are adjacent. How many strings exist?

**Solution.** Put the B values first: _ B _ B _. Choose all 3 gaps for the A
values, so the answer is C(3, 3) = 1: ABABA.

More generally, place the unrestricted type first. If it creates g gaps and
the restricted identical type has r copies, the count is C(g, r) when each gap
holds at most one copy.

## 6. Stars and bars

**Question.** Distribute 8 identical candies to 3 distinct children, each
receiving at least one.

**Solution.** Reserve one candy for every child. The remaining equation is
x1 + x2 + x3 = 5 with non-negative values, so the answer is
C(5 + 3 - 1, 3 - 1) = C(7, 2) = 21.

| Equation | Number of solutions |
| --- | --- |
| x1 + ... + xk = total, xi >= 0 | C(total + k - 1, k - 1) |
| x1 + ... + xk = total, xi >= 1 | C(total - 1, k - 1) |

This requires identical items and distinct labeled boxes. It is not a formula
for distributing distinct objects.

## 7. Upper bounds: stars and bars plus inclusion-exclusion

**Question.** How many non-negative solutions satisfy x1 + x2 + x3 = 7 and
every xi <= 3?

**Solution.** Without upper bounds there are C(9, 2) = 36. If one chosen
variable is at least 4, subtract 4 and distribute 3: C(5, 2) = 10 choices.
There are 3 choices for the violating variable, and two variables cannot both
be at least 4. Answer: 36 - 3 * 10 = 6.

~~~python
from math import comb


def bounded_solutions(total: int, variables: int, upper_bound: int) -> int:
    if total < 0 or variables <= 0 or upper_bound < 0:
        raise ValueError("total and upper_bound must be non-negative; variables must be positive")
    answer = 0
    for chosen in range(variables + 1):
        remaining = total - chosen * (upper_bound + 1)
        if remaining < 0:
            break
        term = comb(variables, chosen) * comb(remaining + variables - 1, variables - 1)
        answer += term if chosen % 2 == 0 else -term
    return answer


print(bounded_solutions(7, 3, 3))
~~~

Output:

~~~text
6
~~~

The loop has O(variables) terms; use precomputed modular combinations for large
repeated queries under a prime modulus.

## 8. Derangements: nobody gets their own item

**Question.** Four people return four distinct gifts uniformly at random. How
many assignments give nobody their original gift?

**Solution.** The derangement recurrence is D(n) = (n-1)(D(n-1)+D(n-2)), with
D(0) = 1 and D(1) = 0. Thus D(4) = 9.

~~~python
def derangements(count: int) -> int:
    if count < 0:
        raise ValueError("count must be non-negative")
    previous_two, previous_one = 1, 0
    for value in range(2, count + 1):
        previous_two, previous_one = previous_one, (value - 1) * (previous_one + previous_two)
    return previous_two if count == 0 else previous_one


print(derangements(4))
~~~

Output:

~~~text
9
~~~

For exactly k fixed points, choose those fixed people and derange the remaining
n-k: C(n, k) * D(n-k).

## 9. Catalan: valid brackets and non-crossing structures

**Question.** How many correct bracket sequences contain 3 pairs of brackets?

**Solution.** The answer is the third Catalan number:
C(6, 3) / 4 = 5. Catalan numbers also count non-crossing matchings,
triangulations, and BST shapes.

~~~python
from math import comb


def catalan(pairs: int) -> int:
    if pairs < 0:
        raise ValueError("pairs must be non-negative")
    return comb(2 * pairs, pairs) // (pairs + 1)


print(catalan(3))
~~~

Output:

~~~text
5
~~~

Modulo a prime, use factorials and the inverse of pairs + 1; check the
preconditions in [modular arithmetic](02-modular-arithmetic.md).

## 10. Circular arrangements and rotations

**Question.** Seat 5 distinct people at a round table, considering rotations
identical. How many seatings exist?

**Solution.** Fix one person to remove rotational symmetry; arrange the other
four. The answer is (5 - 1)! = 24. Reflections are still different unless the
statement says a mirror image is identical.

For repeated colors under rotations, do not divide by n blindly. Use Burnside's
lemma when different rotations can fix different arrangements.

## Pattern checklist

- Alternatives: sum. Consecutive independent choices: product.
- Roles/order matter: permutation. Only membership matters: combination.
- Identical objects: divide duplicate permutations or use stars and bars.
- Adjacency: block; non-adjacency: gaps or complement.
- Lower bounds: reserve first. Upper bounds: inclusion-exclusion.
- No fixed points: derangements. Balanced non-crossing objects: Catalan.


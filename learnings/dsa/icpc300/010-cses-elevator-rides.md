# ICPC300 010: CSES - Elevator Rides

**Source:** [CSES - Elevator Rides](https://cses.fi/problemset/task/1653/)  
**Pattern:** bitmask dynamic programming  
**Goal:** Put everyone into the fewest elevator rides without any ride
exceeding the weight capacity.

## 1. First principles

A subset mask records exactly which people are already placed. Merely storing
the fewest rides for a mask loses information: two arrangements can use the
same number of rides but leave different loads in the current ride.

Store the lexicographically smallest pair:

```text
(number of rides used, load in the last ride)
```

Fewer rides is always better. For the same ride count, a lighter last ride is
always at least as useful for adding another person.

## 2. Cases that decide correctness

| Case | Required behavior |
| --- | --- |
| No people | Return `0`. |
| One person at capacity | Return `1`. |
| A person's weight exceeds capacity | Reject the input. |
| New person exactly fills the last ride | Keep the same ride count. |
| Same minimum rides, different last loads | Keep the lighter last load. |

## 3. Brute force: assign people to rides

Place people from heaviest to lightest into every fitting existing ride or a
new ride. Equal current loads are symmetric, so try only one of them.

```python
def elevator_rides_brute(weights: list[int], capacity: int) -> int:
    if capacity <= 0:
        raise ValueError("capacity must be positive")
    if any(weight <= 0 or weight > capacity for weight in weights):
        raise ValueError("every weight must be in [1, capacity]")
    if not weights:
        return 0

    ordered_weights = sorted(weights, reverse=True)
    ride_loads: list[int] = []
    best = len(weights)

    def assign(person: int) -> None:
        nonlocal best
        if len(ride_loads) >= best:
            return
        if person == len(ordered_weights):
            best = len(ride_loads)
            return

        weight = ordered_weights[person]
        tried_loads: set[int] = set()
        for ride in range(len(ride_loads)):
            current_load = ride_loads[ride]
            if current_load in tried_loads:
                continue
            tried_loads.add(current_load)
            if current_load + weight <= capacity:
                ride_loads[ride] += weight
                assign(person + 1)
                ride_loads[ride] -= weight

        ride_loads.append(weight)
        assign(person + 1)
        ride_loads.pop()

    assign(0)
    return best
```

**Complexity:** exponential time in the number of people and `O(n)` recursion
space.

## 4. Better: partition into feasible subsets

Precompute each subset's total weight. For a remaining mask, choose one
capacity-fitting submask as the next ride. Requiring it to contain one fixed
person removes equivalent ride orderings.

```python
def elevator_rides_subset_dp(weights: list[int], capacity: int) -> int:
    if capacity <= 0:
        raise ValueError("capacity must be positive")
    if any(weight <= 0 or weight > capacity for weight in weights):
        raise ValueError("every weight must be in [1, capacity]")
    if not weights:
        return 0

    state_count = 1 << len(weights)
    subset_weight = [0] * state_count
    for mask in range(1, state_count):
        lowest_bit = mask & -mask
        person = lowest_bit.bit_length() - 1
        subset_weight[mask] = subset_weight[mask ^ lowest_bit] + weights[person]

    infinity = len(weights) + 1
    minimum_rides = [infinity] * state_count
    minimum_rides[0] = 0

    for mask in range(1, state_count):
        required_person = mask & -mask
        submask = mask
        while submask:
            if submask & required_person and subset_weight[submask] <= capacity:
                minimum_rides[mask] = min(
                    minimum_rides[mask],
                    1 + minimum_rides[mask ^ submask],
                )
            submask = (submask - 1) & mask

    return minimum_rides[-1]
```

**Complexity:** `O(3^n)` time and `O(2^n)` space.

## 5. Expert solution: lexicographic bitmask DP

For every nonempty mask, choose one included person as the last addition. Put
that person into the current ride if possible; otherwise start one new ride.

```python
def elevator_rides_bitmask_dp(weights: list[int], capacity: int) -> int:
    if capacity <= 0:
        raise ValueError("capacity must be positive")
    if any(weight <= 0 or weight > capacity for weight in weights):
        raise ValueError("every weight must be in [1, capacity]")
    if not weights:
        return 0

    state_count = 1 << len(weights)
    impossible = (len(weights) + 1, 0)
    best: list[tuple[int, int]] = [impossible] * state_count
    best[0] = (0, 0)

    for mask in range(1, state_count):
        for person, weight in enumerate(weights):
            person_bit = 1 << person
            if mask & person_bit == 0:
                continue

            rides, last_load = best[mask ^ person_bit]
            if rides == 0 or last_load + weight > capacity:
                candidate = (rides + 1, weight)
            else:
                candidate = (rides, last_load + weight)
            if candidate < best[mask]:
                best[mask] = candidate

    return best[-1][0]
```

### Why the expert code is correct

- Removing one selected person reaches a smaller mask whose optimal state is
  already known.
- Adding that person either fits the last ride or necessarily opens one new
  ride for that ordering.
- Trying every possible last person covers every ordering. Lexicographic
  minimization keeps the fewest rides and, among ties, the most reusable last
  ride.

**Complexity:** `O(n 2^n)` time and `O(2^n)` space, which fits `n <= 20`.

## 6. What to remember

```text
mask alone is not enough
state(mask) = minimum (rides, last_ride_load)
compare states lexicographically
```

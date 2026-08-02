# Game Theory and Nim

## Idea

In normal-play impartial games, a state is losing if every move goes to a
winning state; it is winning if at least one move goes to a losing state.

For Nim, the position is losing exactly when the XOR of heap sizes is zero.

## Visual model

```text
heap XOR = 0     -> every move makes XOR nonzero
heap XOR != 0    -> one move can make XOR zero
```

## Classroom board: Nim heaps `[1,2,3]`

```text
1 XOR 2 XOR 3 = 0
any one-heap move makes XOR nonzero
with perfect play, the current player is in a losing state
```

## Steps

1. XOR all heap sizes.
2. Zero means the current player loses with perfect play.
3. Nonzero means the current player can force a win.

## First-principles derivation

In an impartial normal-play game, a state is losing when every move reaches a
winning state; it is winning when at least one move reaches a losing state.

For Nim, the XOR of heap sizes summarizes this recursion: XOR zero is losing,
and nonzero always has a move to XOR zero.

## Classroom board: make Nim XOR zero

Heaps are `[3,4,5]`.

```text
3 XOR 4 XOR 5 = 2, so the state is winning

choose heap 3:
new size = 3 XOR 2 = 1, which is smaller

new heaps [1,4,5]
1 XOR 4 XOR 5 = 0
```

Whatever the opponent changes from a zero-XOR state makes XOR nonzero again,
allowing the invariant to be restored.

## Pattern recognition

Use Nim for multiple heaps where a move removes any positive number from one
heap. For other impartial games, compute Grundy numbers: `mex` of reachable
states, then XOR independent components.

## Implementation

### C++

```cpp
bool firstPlayerWins(const std::vector<long long>& heaps) {
    long long nimSum = 0;
    for (long long heap : heaps) nimSum ^= heap;
    return nimSum != 0;
}
```

### Python

```python
def first_player_wins(heaps: list[int]) -> bool:
    nim_sum = 0
    for heap in heaps:
        nim_sum ^= heap
    return nim_sum != 0
```

### Java

```java
static boolean firstPlayerWins(long[] heaps) {
    long nimSum = 0;
    for (long heap : heaps) nimSum ^= heap;
    return nimSum != 0;
}
```

## Why it works

From XOR zero, changing one heap changes the highest affected bit and cannot
leave XOR zero. From nonzero, reduce a heap containing the highest set bit so
the total XOR becomes zero.

## Complexity

Time is `O(number of heaps)` and space is `O(1)`.

## Common mistakes

- Applying normal Nim to misere play, where taking the last object loses.
- Adding heap sizes instead of XORing them.
- Assuming every take-away game is plain Nim without checking move rules.

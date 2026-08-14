# ICPC300 061: CSES - Word Combinations

**Source:** [CSES - Word Combinations](https://cses.fi/problemset/task/1731/)  
**Pattern:** trie-guided prefix dynamic programming  
**Goal:** Count, modulo `1_000_000_007`, the ways to form the target string by
concatenating words from the given dictionary.

## 1. Problem in plain words

Dictionary words may be reused. Two constructions are different when their
sequences of chosen words differ. For target `aaaa` and words `a`, `aa`, the
five constructions correspond to the five compositions of length four using
parts one and two.

The target must be consumed exactly: a word cannot extend past its end.

## 2. First principles

Let `dp[i]` be the number of constructions of target prefix `target[:i]`.
Initially `dp[0] = 1`. From every reachable position `i`, each dictionary word
matching at `i` contributes `dp[i]` to the state after that word.

Testing every word at every position repeats prefix comparisons. Store all
dictionary words in a trie. Starting at position `i`, follow target characters
through the trie and update DP whenever a terminal trie node is reached. Stop
at the first missing trie edge.

## 3. Cases that decide correctness

| Case | Required behavior |
| --- | --- |
| Whole target is one dictionary word | Count that construction. |
| One word is a prefix of another | Both terminal positions may contribute. |
| Dictionary word is never used | It changes no DP state. |
| No complete construction | Return `0`. |
| Number of constructions is large | Reduce every addition modulo the source modulus. |

## 4. Brute force: try every next dictionary word

```python
MODULO = 1_000_000_007


def count_word_combinations_brute_force(target: str, words: list[str]) -> int:
    if not target or any(not word for word in words):
        raise ValueError("target and dictionary words must be nonempty")
    if len(set(words)) != len(words):
        raise ValueError("dictionary words must be distinct")

    def search(position: int) -> int:
        if position == len(target):
            return 1
        return (
            sum(
                search(position + len(word))
                for word in words
                if target.startswith(word, position)
            )
            % MODULO
        )

    return search(0)
```

**Complexity:** exponential in the number of chosen words, with recursion depth
up to the target length.

## 5. Better: position DP with direct word tests

Memoization collapses all partial constructions ending at the same target
position into one state. This is polynomial, but it still checks every
dictionary word at every reachable position.

```python
MODULO = 1_000_000_007


def count_word_combinations_dp(target: str, words: list[str]) -> int:
    if not target or any(not word for word in words):
        raise ValueError("target and dictionary words must be nonempty")
    if len(set(words)) != len(words):
        raise ValueError("dictionary words must be distinct")

    dp = [0] * (len(target) + 1)
    dp[0] = 1
    for position in range(len(target)):
        if dp[position] == 0:
            continue
        for word in words:
            if target.startswith(word, position):
                end = position + len(word)
                dp[end] = (dp[end] + dp[position]) % MODULO
    return dp[-1]
```

**Complexity:** `O(n * total_dictionary_characters)` worst-case comparison time
and `O(n)` DP memory.

## 6. Expert solution: trie-guided DP transitions

```python
MODULO = 1_000_000_007


def count_word_combinations(target: str, words: list[str]) -> int:
    if not target or any(not word for word in words):
        raise ValueError("target and dictionary words must be nonempty")
    if len(set(words)) != len(words):
        raise ValueError("dictionary words must be distinct")

    children: list[dict[str, int]] = [{}]
    terminal = [False]
    for word in words:
        node = 0
        for character in word:
            if character not in children[node]:
                children[node][character] = len(children)
                children.append({})
                terminal.append(False)
            node = children[node][character]
        terminal[node] = True

    dp = [0] * (len(target) + 1)
    dp[0] = 1
    for start in range(len(target)):
        if dp[start] == 0:
            continue
        node = 0
        for end in range(start, len(target)):
            character = target[end]
            if character not in children[node]:
                break
            node = children[node][character]
            if terminal[node]:
                dp[end + 1] = (dp[end + 1] + dp[start]) % MODULO
    return dp[-1]
```

### Why the expert code is correct

- `dp[start]` represents every valid word sequence ending exactly at `start`.
- A trie path from `start` spells exactly the dictionary prefixes matching that
  target position.
- Each terminal reached appends one complete dictionary word and contributes
  every construction counted by `dp[start]` once.
- Every complete target construction has a unique previous word boundary, so
  these transitions cover it without duplication.

**Complexity:** `O(total_dictionary_characters + nL)` time and corresponding
trie memory, where `L` is the maximum dictionary-word length.

## 7. What to remember

Use DP for word boundaries and a trie for all words that can begin at one
boundary. The trie shares their prefix comparisons.

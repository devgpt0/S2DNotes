# Focus300 130: LeetCode 839 - Similar String Groups

**Source:** [LeetCode 839](https://leetcode.com/problems/similar-string-groups/)  
**Difficulty:** Hard  
**Pattern:** connected components under a one-swap relation

## Exact contract

All input strings have equal length, contain lowercase ASCII letters, and are
anagrams of one another. Two strings are similar when they are equal or one can
become the other by swapping two positions. Similarity groups are connected
components under this direct relation. Return the number of groups.

## First principles

Direct similarity is not transitive, but group membership is its transitive
closure. Two anagrams are directly similar exactly when they differ at zero
positions or at two cross-matching positions. Build those graph edges and count
components with union-find.

## Cases that decide correctness

- Strings connected through intermediates belong to one group.
- Equal strings are directly similar without a swap.
- One mismatch cannot occur between anagrams.
- More than two mismatches is not one-swap similarity.
- Repeated letters can generate the same swapped string many times.

## Brute force: generate every one-swap neighbor

```python
def similar_groups_brute(words: list[str]) -> int:
    if type(words) is not list or not 1 <= len(words) <= 300:
        raise ValueError("words must contain between 1 and 300 strings")
    if any(
        type(word) is not str
        or not 1 <= len(word) <= 300
        or any(not "a" <= character <= "z" for character in word)
        for word in words
    ):
        raise ValueError("words must be nonempty lowercase ASCII strings")
    signature = sorted(words[0])
    if any(len(word) != len(words[0]) or sorted(word) != signature for word in words):
        raise ValueError("all words must have equal length and be anagrams")

    unvisited = set(words)
    groups = 0
    while unvisited:
        groups += 1
        stack = [unvisited.pop()]
        while stack:
            word = stack.pop()
            characters = list(word)
            for first in range(len(characters)):
                for second in range(first + 1, len(characters)):
                    if characters[first] == characters[second]:
                        continue
                    characters[first], characters[second] = (
                        characters[second],
                        characters[first],
                    )
                    candidate = "".join(characters)
                    characters[first], characters[second] = (
                        characters[second],
                        characters[first],
                    )
                    if candidate in unvisited:
                        unvisited.remove(candidate)
                        stack.append(candidate)
    return groups
```

Generating `O(m^2)` strings of length `m` per reached word costs
`O(n*m^3)` time in the worst case.

## Better insight: compare the at most 300 provided strings directly

There is no need to construct neighbors absent from the input. Stop comparing a
pair as soon as its third mismatch appears, and union every similar pair.

## Expert solution: pairwise similarity plus union-find

```python
def similar_groups(words: list[str]) -> int:
    if type(words) is not list or not 1 <= len(words) <= 300:
        raise ValueError("words must contain between 1 and 300 strings")
    if any(
        type(word) is not str
        or not 1 <= len(word) <= 300
        or any(not "a" <= character <= "z" for character in word)
        for word in words
    ):
        raise ValueError("words must be nonempty lowercase ASCII strings")
    signature = sorted(words[0])
    if any(len(word) != len(words[0]) or sorted(word) != signature for word in words):
        raise ValueError("all words must have equal length and be anagrams")

    parent = list(range(len(words)))
    component_size = [1] * len(words)

    def find(index: int) -> int:
        while parent[index] != index:
            parent[index] = parent[parent[index]]
            index = parent[index]
        return index

    def union(first: int, second: int) -> None:
        first_root = find(first)
        second_root = find(second)
        if first_root == second_root:
            return
        if component_size[first_root] < component_size[second_root]:
            first_root, second_root = second_root, first_root
        parent[second_root] = first_root
        component_size[first_root] += component_size[second_root]

    def directly_similar(first: str, second: str) -> bool:
        differences: list[tuple[str, str]] = []
        for first_character, second_character in zip(first, second, strict=True):
            if first_character != second_character:
                differences.append((first_character, second_character))
                if len(differences) > 2:
                    return False
        return not differences or (
            len(differences) == 2
            and differences[0] == (differences[1][1], differences[1][0])
        )

    for first in range(len(words)):
        for second in range(first + 1, len(words)):
            if directly_similar(words[first], words[second]):
                union(first, second)
    return sum(find(index) == index for index in range(len(words)))
```

Union-find computes the transitive closure while each pair test enforces the
source's exact one-swap relation.

**Complexity:** `O(n^2*m + n*alpha(n))` time and `O(n)` space.

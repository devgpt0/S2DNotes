# Deque

## Idea

A deque (double-ended queue) supports adding and removing at both ends in
`O(1)`.

## Visual model

```text
add/remove <- [ front ........ back ] -> add/remove
```

## Classroom board: both ends are useful

```text
characters: [r, a, c, e, c, a, r]
compare r/r -> equal; remove both
compare a/a -> equal; remove both
compare c/c -> equal; remove both
one e remains -> palindrome
```

A normal queue removes only the front; a deque lets this example remove both
ends in constant time.

## Steps

The exact steps depend on the problem: choose the front for urgent/small-cost
work and the back for normal/larger-cost work.

## First-principles derivation

A stack exposes one end and a queue uses opposite ends. Some algorithms need
both choices, so a deque supports insertion and removal at either boundary.

The algorithm must still define what each end represents; a deque is a tool,
not the invariant by itself.

## Pattern recognition

Use a deque when both ends matter: 0-1 BFS, sliding-window maxima, palindrome
checks, or simulations with front and back operations.

## Implementation: palindrome check

### C++

```cpp
bool isPalindrome(const std::string& text) {
    std::deque<char> characters(text.begin(), text.end());
    while (characters.size() > 1) {
        if (characters.front() != characters.back()) return false;
        characters.pop_front();
        characters.pop_back();
    }
    return true;
}
```

### Python

```python
from collections import deque


def is_palindrome(text: str) -> bool:
    characters = deque(text)
    while len(characters) > 1:
        if characters.popleft() != characters.pop():
            return False
    return True
```

### Java

```java
static boolean isPalindrome(String text) {
    Deque<Character> characters = new ArrayDeque<>();
    for (char character : text.toCharArray()) characters.addLast(character);
    while (characters.size() > 1) {
        if (!characters.removeFirst().equals(characters.removeLast())) return false;
    }
    return true;
}
```

## Why it works

A string is a palindrome exactly when matching outside characters are equal at
every step; removing them leaves the same smaller problem.

## Complexity

Time and space are `O(n)`. A two-pointer palindrome check uses only `O(1)`
extra space, but this example makes deque operations visible.

## Common mistakes

- Using a structure whose front removal is linear.
- Confusing a deque with a priority queue; a deque does not sort values.
- Removing from an empty deque.

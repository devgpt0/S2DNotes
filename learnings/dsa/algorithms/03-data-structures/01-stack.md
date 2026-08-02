# Stack

## Idea

A stack stores values in **last in, first out** order. The last value pushed is
the first value popped.

## Visual model

```text
push 3       top -> 3       pop -> 3
push 2              2              2
push 1              1              1
```

## Classroom board: balanced `([{}])`

```text
read (  -> stack [(]
read [  -> stack [(,[]
read {  -> stack [(,[,{]
read }  -> matches top {; pop
read ]  -> matches top [; pop
read )  -> matches top (; pop
empty stack -> balanced
```

A closing bracket must match the most recent unclosed bracket, so LIFO is the
exact order we need.

## Steps

1. Push when an item starts or must be remembered.
2. Read the top when only the most recent unfinished item matters.
3. Pop when that item is finished.

## First-principles derivation

Some unfinished work must be resolved in reverse order: the newest opening
bracket closes first, and the newest function call returns first.

A stack stores exactly this last-in, first-out frontier; its top is the only
item that can be completed next.

## Pattern recognition

Use a stack for nested structures, undo operations, DFS, expression parsing,
or “nearest previous/next” problems.

## Implementation: balanced brackets

### C++

```cpp
bool isBalanced(const std::string& text) {
    std::vector<char> stack;
    const std::unordered_map<char, char> opening{{')', '('}, {']', '['}, {'}', '{'}};
    for (char character : text) {
        if (character == '(' || character == '[' || character == '{') {
            stack.push_back(character);
        } else if (opening.find(character) != opening.end()) {
            if (stack.empty() || stack.back() != opening.at(character)) return false;
            stack.pop_back();
        }
    }
    return stack.empty();
}
```

### Python

```python
def is_balanced(text: str) -> bool:
    opening = {')': '(', ']': '[', '}': '{'}
    stack: list[str] = []
    for character in text:
        if character in '([{':
            stack.append(character)
        elif character in opening:
            if not stack or stack[-1] != opening[character]:
                return False
            stack.pop()
    return not stack
```

### Java

```java
static boolean isBalanced(String text) {
    Deque<Character> stack = new ArrayDeque<>();
    Map<Character, Character> opening = Map.of(')', '(', ']', '[', '}', '{');
    for (char character : text.toCharArray()) {
        if (character == '(' || character == '[' || character == '{') {
            stack.addLast(character);
        } else if (opening.containsKey(character)) {
            if (stack.isEmpty() || stack.removeLast() != opening.get(character)) return false;
        }
    }
    return stack.isEmpty();
}
```

## Why it works

The top always holds the most recent opening bracket that has not been closed.
A closing bracket must match exactly that bracket.

## Complexity

Time is `O(n)` and space is `O(n)` in the worst case.

## Common mistakes

- Popping before checking whether the stack is empty.
- Returning true before checking for leftover opening brackets.
- Using a queue when the most recent item must be handled first.

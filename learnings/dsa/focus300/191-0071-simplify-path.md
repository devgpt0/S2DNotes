# Focus300 191: LeetCode 71 - Simplify Path

**Source:** [LeetCode 71](https://leetcode.com/problems/simplify-path/)  
**Difficulty:** Medium  
**Pattern:** stack reduction of path components

## Exact contract

Given an absolute Unix-style path, return its canonical form. Treat repeated
slashes as one separator, `.` as the current directory, and `..` as moving to
the parent without going above root. Any other nonempty component—including
names containing extra periods—is a literal directory name.

## First principles

Splitting on `/` exposes a sequence of navigation commands. Literal components
push one directory, `..` pops one when possible, and empty or `.` components do
nothing. The stack after each component is exactly the canonical location of
the processed prefix.


## Classroom board: keep only the useful unfinished work

```text
a stack stores the part of the state that can still matter after the next step.
```



## Step-by-step transformation

1. Load the current candidates into a stack, queue, heap, or window.
2. Push or pop the structure while the current element keeps the invariant true.
3. Drop stale candidates and keep only the ones that can still affect the answer.
4. Read the final top, window score, or popped order as the output.

These problems transform the input by keeping just the active frontier of candidates instead of rescanning the whole array every time.


## Diagram: active frontier only

```text

            scan left to right
                |
                v
            keep active candidates
                |
                v
            pop stale work
                |
                v
            current best answer
```

These notes keep only the active frontier of useful candidates instead of rescanning the whole input.

## Cases that decide correctness

- Leading `..` commands remain at root.
- Repeated and trailing slashes disappear.
- `...` and `.hidden` are ordinary names, not navigation commands.
- The result begins with one slash and has no trailing slash unless it is root.
- The input is absolute and begins with `/`.

## Brute force: rebuild an immutable path after each component

```python
def simplify_path_brute(path: str) -> str:
    if (
        type(path) is not str
        or not 1 <= len(path) <= 3_000
        or not path.startswith("/")
        or any(
            not character.isascii()
            or not (character.isalnum() or character in "._/")
            for character in path
        )
    ):
        raise ValueError("path must be an absolute source-valid Unix path")

    canonical = "/"
    for component in path.split("/"):
        if not component or component == ".":
            continue
        if component == "..":
            if canonical != "/":
                canonical = canonical.rsplit("/", 1)[0] or "/"
        elif canonical == "/":
            canonical += component
        else:
            canonical += "/" + component
    return canonical
```

Repeated immutable-string rebuilding can make this `O(n^2)` in total path
length.

## Better insight: directory components are the natural mutable state

A list supports constant-time append and pop. Join it once after processing all
navigation commands.

## Expert solution: component stack

```python
def simplify_path(path: str) -> str:
    if (
        type(path) is not str
        or not 1 <= len(path) <= 3_000
        or not path.startswith("/")
        or any(
            not character.isascii()
            or not (character.isalnum() or character in "._/")
            for character in path
        )
    ):
        raise ValueError("path must be an absolute source-valid Unix path")

    directories: list[str] = []
    for component in path.split("/"):
        if not component or component == ".":
            continue
        if component == "..":
            if directories:
                directories.pop()
        else:
            directories.append(component)
    return "/" + "/".join(directories)
```

The stack invariant represents the canonical directory sequence after every
component, so the final join produces the unique canonical path.

**Complexity:** `O(n)` time and `O(n)` space.

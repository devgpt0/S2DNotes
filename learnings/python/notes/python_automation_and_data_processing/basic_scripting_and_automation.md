# Basic Scripting and Automation

## 1. Core truth

A script is a small program that performs a repeatable task.
Automation means using code to reduce manual effort and repeated mistakes.

```python
def normalize_names(names: list[str]) -> list[str]:
    return [name.strip().title() for name in names]

print(normalize_names(["  ana", "raj  ", "mia"]))
```

Output:

```text
['Ana', 'Raj', 'Mia']
```

The function trims spaces and converts each name into title case.

## 2. Script foundations

### Keep logic in functions

```python
def normalize_names(names: list[str]) -> list[str]:
    return [name.strip().title() for name in names]

print(normalize_names(["  ana", "raj  ", "mia"]))
```

Output:

```text
['Ana', 'Raj', 'Mia']
```

### Add a clear entry point

```python
def main() -> None:
    print("ready")

main()
```

Output:

```text
ready
```

### Make automation deterministic

```python
def count_items(items: list[str]) -> int:
    return len(items)

print(count_items(["a", "b", "c"]))
```

Output:

```text
3
```

## 3. Script building blocks

- break work into functions;
- use `main()` for orchestration;
- validate inputs before changing anything;
- print or return a clear result;
- keep side effects controlled.

## 4. Practical automation

### Example 1: Normalize values

```python
def normalize_names(names: list[str]) -> list[str]:
    return [name.strip().title() for name in names]

print(normalize_names(["  ana", "raj  "]))
```

Output:

```text
['Ana', 'Raj']
```

### Example 2: Summarize a small input

```python
def count_names(names: list[str]) -> int:
    return len(names)

print(count_names(["Ana", "Raj", "Mia"]))
```

Output:

```text
3
```

### Example 3: Safe script shape

```python
def main() -> None:
    names = ["ana", "raj"]
    print([name.title() for name in names])

main()
```

Output:

```text
['Ana', 'Raj']
```

- cleanup scripts;
- report generation;
- file renaming;
- simple imports and exports;
- scheduled maintenance tasks.

## 5. Automation mistakes

### Mistake 1: Mixing too much logic with top-level code

Keep reusable logic in functions.

### Mistake 2: Automating unsafe changes without a dry run

Preview the effect before deleting or renaming data.

### Mistake 3: Making scripts hard to rerun

Prefer idempotent operations when possible.

## 6. Automation decision guide

| Need | Best choice | Why |
| --- | --- | --- |
| Small repeatable task | script | simple and direct |
| Complex multi-step system | application | needs more structure |
| One-off manual step | manual action | no repetition yet |

## 7. Safety and maintainability

- keep scripts small and explicit;
- validate inputs before acting;
- avoid destructive operations without confirmation;
- log or print results clearly when useful.

## 8. Advanced automation

- command-line arguments;
- dry-run mode;
- batch processing;
- scheduling.

## 9. Mental model

| Concept | Remember |
| --- | --- |
| Script | small repeatable program |
| Automation | reduce manual work |
| `main()` | clear entry point |
| Dry run | preview before changing |
| Idempotent | safe to rerun |

## 10. Reliable command-line boundaries

Parse command-line values once and validate them before doing work. `argparse`
rejects missing values and unsupported choices instead of silently guessing.

```python
import argparse


def parse_args(arguments: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("dry-run", "apply"), required=True)
    return parser.parse_args(arguments)


print(parse_args(["--mode", "dry-run"]).mode)
```

Output:

```text
dry-run
```

Return explicit exit codes from `main()`: `0` for success and a documented
nonzero code for an expected operational failure. Let unexpected programming
errors propagate with their traceback.

## 11. Safe process execution

Pass arguments as a sequence and keep `shell=False`, the default. This avoids
shell parsing and command injection.

```python
import sys

command = [sys.executable, "-c", "print(6 * 7)"]
print(command[1:])
```

Output:

```text
['-c', 'print(6 * 7)']
```

Pass this sequence to `subprocess.run()` with `check=True`, a timeout, and the
minimum environment needed. Never place secrets in command arguments because
process listings may expose them.

## 12. Atomic and repeatable changes

- Make repeated runs converge on the same state.
- Write a complete temporary file in the destination directory, flush it when
  durability matters, then replace the destination atomically with `os.replace()`.
- Keep dry-run and apply modes on the same planning path.
- Record which item failed and stop when continuing could corrupt later work.
- Use a lock or transactional store when multiple script instances may modify
  the same resource.

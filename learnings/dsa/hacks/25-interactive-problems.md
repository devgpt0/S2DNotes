# Interactive-Problem Discipline

## First principles

An interactive program and judge alternate messages under a strict protocol.
A correct algorithm can still fail if it sends an invalid query, exceeds the
query budget, forgets to flush, or continues after an error response.

## Why it matters

Interactive programs exchange queries and replies with a judge. Buffering,
invalid queries, or exceeding the query budget can fail a correct strategy.

## Technique

Print every query with flushing, then read and validate the reply.

```python
import sys


def ask(left: int, right: int) -> int:
    print('?', left, right, flush=True)
    reply = int(sys.stdin.buffer.readline())
    if reply == -1:
        raise RuntimeError('judge reported an invalid query')
    return reply


def answer(value: int) -> None:
    print('!', value, flush=True)
```

## Steps

1. Derive a strategy within the stated query limit.
2. Centralize query formatting and count queries.
3. Flush after every query and final answer.
4. Stop immediately on the judge's failure sentinel.
5. Never print diagnostics to standard output.

## Pattern recognition

Interactive statements explicitly describe a protocol, allowed queries,
reply meanings, and a maximum query count.

## Local testing

Separate strategy from I/O by injecting an `ask` function. A local mock can
then answer from a hidden value and assert every query is valid.

```python
def make_mock(hidden: int):
    def ask(left: int, right: int) -> int:
        assert left <= right
        return int(left <= hidden <= right)
    return ask
```

## Visual worked example: one safe exchange

```text
your program                    judge
print("? 1 5", flush=True)  ->
                            <-  "3"
parse exactly one integer
update search interval
print("? 4 5", flush=True)  ->
                            <-  "-1" means protocol failure
terminate immediately; send nothing else

final:
print("! 4", flush=True)
```

Track the number and meaning of queries as part of the algorithm's state, and
test locally with a deterministic mock judge.

## Traps

- Using whole-file input; replies arrive only after queries.
- Forgetting `flush=True`.
- Continuing after a `-1` error reply.
- Testing by printing extra messages to standard output.
- Assuming ordinary custom testing behaves like an interactive judge.

# How to Learn from a Classroom Note

## The classroom rule

Do not begin with code. Imagine the teacher has only an array and a marker on
the board.

```text
1. What is the slow obvious method?
2. Which work does it repeat?
3. What small fact can we remember?
4. What stays true after every step?
5. Only now: write code.
```

This is the first-principles loop used throughout the course:

```text
obvious correct method
        |
        v
find repeated work or a structural guarantee
        |
        v
store, skip, or combine work safely
        |
        v
state the invariant
        |
        v
trace one complete example before coding
```

Do not memorize the finished optimization without the middle steps. Those
steps are what let you recognize a disguised problem later.

## How to read every note

### 1. Read the prerequisite

If a word is unfamiliar, use the [glossary](00-simple-glossary.md). Do not let
three unknown words hide one simple idea.

### 2. Copy the board example by hand

For each row, say why a pointer, total, queue, stack, or DP value changes.

```text
input: [2, 1, 3]

step        remembered total
start       0
read 2      2
read 1      3
read 3      6
```

For every trace, mark four things:

1. **State:** what information is remembered now?
2. **Choice:** what can the algorithm do next?
3. **Invariant:** what must remain true after the choice?
4. **Progress:** why does the algorithm move closer to stopping?

### 3. Say the idea in one sentence

Example: “A prefix sum remembers the total before every position, so a range
sum is one subtraction.” If you need a paragraph, the idea is not clear yet.

### 4. Hide the note and reproduce it

Write:

- when the pattern works;
- the numbered steps;
- the invariant;
- time and space complexity;
- one case where it fails.

### 5. Implement in one language first

Use your main contest language. Read the other languages only after you can
write the algorithm without copying. The three versions express the same
steps, not three different algorithms.

## How to use a first-principles derivation

Cover the section and answer these questions yourself:

```text
What would brute force do?
Which work would brute force repeat?
Which fact makes some work unnecessary?
What information is the smallest sufficient state?
Which counterexample breaks the method's assumptions?
```

Then compare your reasoning with the note. A different solution is fine when
you can prove it and its complexity fits.

## The three-problem ladder

For every concept solve:

1. **Direct:** the statement almost names the pattern.
2. **Disguised:** the same pattern is hidden in a story.
3. **Combined:** the pattern works with another concept.

## When you are ready to move on

You are ready only when you can teach the board example to someone else,
implement it from memory, and explain a counterexample to a tempting wrong
approach.

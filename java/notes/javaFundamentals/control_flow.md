# JAVA - CONTROL FLOW

## 1. Core Mental Model

Control flow questions test whether you can predict exactly which statement executes next.

Think in this order:
1. Condition evaluation
2. Branch/loop selection
3. Jump statements (break, continue, return, throw)
4. finally execution guarantees

## 2. Boolean Operators and Short-Circuit

Short-circuit operators:
- && : if left is false, right is not evaluated.
- || : if left is true, right is not evaluated.

Non-short-circuit operators:
- & and | with booleans evaluate both sides.

This matters for division-by-zero and side effects inside conditions.

## 3. if Conditions and Assignment Trap

In Java, if condition must be boolean.
- if (a = 10) does not compile because assignment expression is int, not boolean.

## 4. switch Statement (Classic)

Classic switch behavior:
- Matching case starts execution.
- Without break, fall-through continues into next cases.
- default runs when no case matches (or after fall-through if reached).

String switch notes:
- Compiler typically uses hash-based dispatch plus equals check.
- Hash collision does not break correctness because equals is still checked.

## 5. Enhanced switch (Expression and Arrow Cases)

Modern switch supports:
- Arrow labels: case X -> ...
- Expression form that returns a value.

Rules:
- No fall-through with arrow syntax.
- Switch expressions must be exhaustive.
- Use yield in block cases when returning a value from switch expression.

## 6. Loops and Scope

for/while/do-while fundamentals:
- for init variable scope is limited to loop block.
- do-while body executes at least once.
- Infinite loops occur when condition never becomes false.

Evaluation order in for loop:
- init -> condition -> body -> update -> condition -> ...

## 7. break, continue, and labels

break:
- Exits nearest loop/switch by default.
- Labelled break exits the named outer loop.

continue:
- Skips remaining body and goes to next iteration.
- Labelled continue jumps to next iteration of named outer loop.

## 8. Ternary Operator (?:)

Ternary is right-associative:
- a ? b : c ? d : e means a ? b : (c ? d : e)

Type selection rules can promote operands to common type.
In mixed numeric wrappers, result may be a promoted numeric type rather than one operand's exact wrapper.

## 9. Dead Code and Compile-Time Checks

Compile-time unreachable examples:
- while(false) { ... } is a compile-time error.

Reason:
- Compiler detects definitely unreachable statements for constant-false loops.

## 10. try/finally in Control Flow

finally executes even when:
- return runs in try/catch
- break/continue occurs
- exception is thrown

If finally returns, it overrides earlier return values and can suppress exceptions.

## 11. for-each and Mutation Semantics

for-each loop variable is a copy of each element reference/value for that iteration.
- Reassigning loop variable does not modify collection contents.
- To modify mutable element state, mutate the object itself.
- To replace elements, use index-based update or list iterator (if mutable collection).

## 12. Java 21 Pattern Matching for switch

Pattern switch supports:
- Type patterns (case Integer i -> ...)
- Guarded patterns (case Integer i when i > 0 -> ...)
- case null handling
- Record patterns

Important rules:
- Order matters; broader patterns can dominate narrower ones.
- Dominated case labels cause compile-time error.
- Exhaustiveness is required for switch expressions, especially with sealed hierarchies.
- Pattern variables exist only in their matching case scope.

## 13. Control Flow Quality Patterns

Good style:
- Prefer guard clauses over deep nesting.
- Replace magic numbers with enums/constants.
- Use multiple early returns when clarity improves.
- Do not use exceptions for normal control flow in hot paths.
- Choose loop vs stream based on readability and performance context.

## 14. Interview Solve Template

For any control-flow snippet:
1. Mark entry point and initial variable values.
2. Evaluate conditions in exact order.
3. Track loop iteration boundaries.
4. Apply break/continue/return labels precisely.
5. Apply finally execution before method exit.
6. For switch, verify matching, fall-through (if classic), and exhaustiveness (if expression).
7. For pattern switch, check dominance, guards, and null handling.

## 15. Worksheet Concept Coverage Checklist

- && vs & and side effects
- Assignment-in-condition compile errors
- Classic switch fall-through
- String switch collision understanding
- Loop termination and scope
- Labelled break and continue
- do-while execution guarantee
- Ternary associativity and type selection
- Dead code detection
- try/finally return override
- for-each modification behavior
- Enhanced switch and yield
- Java 21 pattern matching: guards, dominance, exhaustiveness, sealed types, record patterns, null

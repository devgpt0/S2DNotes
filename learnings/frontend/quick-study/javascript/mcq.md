# JavaScript interview MCQs with explanations

Answer each question before reading the explanation.

## 1. Which declaration should be the default for an unchanged binding?

- A. `var`
- B. `let`
- C. `const`
- D. `static`

**Answer: C — `const`.** It prevents accidental reassignment and clearly communicates intent. Use `let` only when the variable must be reassigned.

## 2. Which equality operator avoids type coercion?

- A. `==`
- B. `===`
- C. `=`
- D. `=>`

**Answer: B — `===`.** Strict equality compares both type and value. Loose equality first performs conversion, which can create surprising matches such as `0 == false`.

## 3. What does `typeof null` return?

- A. `"null"`
- B. `"undefined"`
- C. `"object"`
- D. `"number"`

**Answer: C — `"object"`.** This is a historical JavaScript behavior. Check for null explicitly with `value === null`.

## 4. Which value is truthy?

- A. `0`
- B. `""`
- C. `[]`
- D. `null`

**Answer: C — `[]`.** Arrays and objects are truthy even when empty. Zero, an empty string, null, undefined, false, and `NaN` are falsy.

## 5. When does `left ?? right` return `right`?

- A. When `left` is any falsy value
- B. When `left` is null or undefined
- C. When `left` is zero
- D. When `left` is an empty array

**Answer: B — When the left side is nullish.** Unlike `||`, nullish coalescing preserves meaningful falsy values such as `0`, `false`, and `""`.

## 6. What does optional chaining do?

- A. Creates a missing property
- B. Returns undefined when an accessed receiver is nullish
- C. Validates property types
- D. Deep-copies an object

**Answer: B — It stops on null or undefined.** For example, `user.address?.city` avoids an error when `address` is nullish, but it does not validate any value.

## 7. What kind of copy does object or array spread create?

- A. Deep copy
- B. Shallow copy
- C. Frozen copy
- D. Prototype-free copy

**Answer: B — Shallow copy.** Only the outer container is new. Nested objects and arrays still refer to the same underlying values.

## 8. Which array method transforms every item into a new array?

- A. `filter`
- B. `find`
- C. `map`
- D. `some`

**Answer: C — `map`.** It calls a function for every item and collects each returned value in a new array of the same length.

## 9. Which method returns the first matching item?

- A. `find`
- B. `filter`
- C. `every`
- D. `reduce`

**Answer: A — `find`.** It stops at the first match and returns that value, or `undefined` when no item matches. `filter` returns every match in an array.

## 10. What does `forEach` return?

- A. A new array
- B. The last item
- C. `undefined`
- D. An iterator

**Answer: C — `undefined`.** `forEach` is intended for side effects. Use `map`, `filter`, or `reduce` when you need a produced value.

## 11. What is a closure?

- A. A closed browser tab
- B. A function retaining access to its lexical variables
- C. A private class only
- D. A completed Promise

**Answer: B — A function plus its lexical environment.** The remembered variables remain accessible after the outer function finishes, enabling private state and callbacks.

## 12. Where does an arrow function get `this`?

- A. Its call site
- B. Its enclosing lexical scope
- C. Its first argument
- D. Always the global object

**Answer: B — The enclosing scope.** Arrow functions do not create their own `this`, so `call`, `apply`, and method-style invocation do not rebind it.

## 13. What scope do `let` and `const` use?

- A. Function scope only
- B. Block scope
- C. File-system scope
- D. Class scope only

**Answer: B — Block scope.** A binding declared inside braces is unavailable outside that block, which reduces accidental leakage compared with `var`.

## 14. What is the temporal dead zone?

- A. Time before a timer fires
- B. The region where a lexical binding exists but is not initialized
- C. The garbage-collection phase
- D. A rejected Promise state

**Answer: B — The pre-initialization region.** Reading a `let`, `const`, or class binding before its declaration executes throws a `ReferenceError`.

## 15. What inheritance mechanism supports JavaScript classes?

- A. Value copying
- B. The prototype chain
- C. Interfaces
- D. Multiple class inheritance

**Answer: B — The prototype chain.** `class` is cleaner syntax over JavaScript's prototype-based object model.

## 16. What does an `async` function always return?

- A. An iterator
- B. A Promise
- C. A number
- D. A callback

**Answer: B — A Promise.** A returned value becomes a fulfilled Promise, while a thrown error becomes a rejected Promise.

## 17. Which callback runs first after synchronous code finishes?

- A. `setTimeout(callback, 0)`
- B. A resolved Promise's handler
- C. Every animation callback
- D. Every network callback

**Answer: B — The Promise handler.** Promise handlers are microtasks. The event loop drains microtasks before running the next task, such as a timer.

## 18. Does `fetch` reject automatically for an HTTP 404 response?

- A. Yes
- B. No
- C. Only inside modules
- D. Only when used with `await`

**Answer: B — No.** `fetch` resolves when an HTTP response arrives, even for 404 or 500. Check `response.ok` or `response.status` yourself.

## 19. Which method combines independent Promises and rejects when one fails?

- A. `Promise.all`
- B. `Promise.resolve`
- C. `forEach`
- D. `JSON.parse`

**Answer: A — `Promise.all`.** It fulfills with ordered results when every input fulfills and rejects when any input rejects.

## 20. Which method waits for every Promise regardless of rejection?

- A. `Promise.resolve`
- B. `Promise.allSettled`
- C. `Promise.reject`
- D. `Promise.race`

**Answer: B — `Promise.allSettled`.** It returns a status object for every input, making it appropriate when both successes and failures must be reported.

## 21. Why is `array.forEach(async item => ...)` often incorrect?

- A. Async callbacks are invalid
- B. `forEach` does not wait for returned Promises
- C. It is always sequential
- D. It mutates the array

**Answer: B — `forEach` ignores returned Promises.** Use `Promise.all(items.map(...))` for concurrent work or `for...of` with `await` for sequential work.

## 22. What is event bubbling?

- A. An event travels from its target through ancestors
- B. An event travels only to children
- C. A timer enters the task queue
- D. The browser parses DOM nodes

**Answer: A — Target-to-ancestor propagation.** Bubbling lets a parent observe events that began on descendants and enables event delegation.

## 23. What does `event.preventDefault()` stop?

- A. Event bubbling
- B. The browser's default action
- C. Other listeners
- D. Rendering

**Answer: B — The default action.** It can prevent form submission or link navigation. It does not stop propagation; that requires `stopPropagation()`.

## 24. Where does event delegation place the listener?

- A. On every descendant
- B. On a common ancestor
- C. Only on `window`
- D. In a CSS rule

**Answer: B — On a common ancestor.** The listener inspects the bubbled event target, reducing listener count and supporting dynamically added children.

## 25. Which property safely inserts untrusted plain text?

- A. `innerHTML`
- B. `textContent`
- C. `eval`
- D. `document.write`

**Answer: B — `textContent`.** The browser treats the value as text rather than parsing it as markup, preventing injected tags or scripts from executing.

## 26. Which collection stores unique values?

- A. Array
- B. Set
- C. Map
- D. Plain object

**Answer: B — Set.** Adding an already-present value has no effect, making Set useful for uniqueness and membership checks.

## 27. Which collection directly supports objects as keys?

- A. Map
- B. JSON
- C. String
- D. Array

**Answer: A — Map.** Map keys retain their actual identity and type. Plain object property keys are strings or symbols.

## 28. What does numeric `array.sort()` require for ascending order?

- A. `JSON.stringify`
- B. A comparator such as `(a, b) => a - b`
- C. `parseInt` only
- D. Nothing

**Answer: B — A numeric comparator.** The default sort compares string representations, so `[2, 10]` can be ordered incorrectly for numeric intent. `sort` also mutates the array.

## 29. What does `function.bind(value)` return?

- A. A new function with fixed `this`
- B. The original function's result
- C. A Promise
- D. A class

**Answer: A — A new bound function.** Calling `bind` does not execute the original function. It creates a wrapper with fixed `this` and optionally pre-filled arguments.

## 30. What should be the first step in performance optimization?

- A. Memoize everything
- B. Measure the actual bottleneck
- C. Rewrite in WebAssembly
- D. Remove functions

**Answer: B — Measure first.** Profiling shows where time and memory are actually spent, preventing complicated changes that do not improve real performance.

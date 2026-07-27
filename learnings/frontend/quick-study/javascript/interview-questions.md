# JavaScript: 10 most-asked interview questions

## 1. What is the difference between `var`, `let`, and `const`?

`var` is function-scoped, can be redeclared, and initializes as `undefined` during hoisting. `let` and `const` are block-scoped and stay in the temporal dead zone until initialized. `const` prevents rebinding, not mutation of the referenced object.

## 2. What is a closure?

A closure is a function together with access to the lexical environment where it was created. It enables private state, factories, callbacks, and memoization. Retained variables stay alive as long as the closure is reachable.

## 3. Explain hoisting and the temporal dead zone.

Declarations are processed before execution. Function declarations are callable early; `var` reads early as `undefined`. `let`, `const`, and class bindings exist but cannot be accessed before initialization—the temporal dead zone.

## 4. How does `this` work?

For normal functions, `this` depends on the call: method receiver, constructor instance, explicit `call`/`apply`/`bind`, or `undefined` in strict plain calls. Arrow functions capture `this` lexically and cannot be constructors.

## 5. What is the difference between `==` and `===`?

`==` performs type coercion before comparison, creating cases such as `0 == false`. `===` compares without coercing types. Use strict equality unless a carefully documented coercive comparison is intentional.

## 6. Explain the event loop.

Synchronous code runs on the call stack. After it finishes, queued microtasks such as Promise handlers run before the next task such as a timer or input event. Long synchronous work blocks rendering and interaction.

## 7. Promises versus `async`/`await`?

They use the same Promise model. `async`/`await` gives sequential-looking syntax and normal `try`/`catch`; promise chaining can be useful for direct composition. An async function always returns a Promise, and independent work should usually start together.

## 8. What is event delegation?

One ancestor listener handles events from many descendants through bubbling, typically using `closest` to find a matching target. It reduces listeners and supports dynamically added items. Check that the match belongs to the intended container.

## 9. Shallow copy versus deep copy?

Spread, `Object.assign`, and array spread copy only the outer container; nested references remain shared. `structuredClone` deeply clones supported values, but not every value. Often the cleanest design copies only the changed path.

## 10. Debounce versus throttle?

Debounce waits until calls stop, useful for search input. Throttle allows at most one call per interval, useful for continuous scroll/resize updates. Both must preserve needed arguments/context and clean up timers when ownership ends.

# 12 - JavaScript Practical Activities and Interview Answers

## Activity 1: Accessible Todo Application

Build add, complete, filter, and delete behavior.

Requirements:

- semantic form and list
- validation without silent trimming/coercion
- event delegation
- immutable state updates
- localStorage persistence with schema checking
- keyboard focus after add/delete
- live-region status
- unit tests for state functions

### Example State Function

```javascript
function addTodo(todos, text) {
  if (typeof text !== "string" || text.length === 0) throw new TypeError("text is required");
  return [...todos, { id: crypto.randomUUID(), text, completed: false }];
}
const todos = addTodo([], "Learn JavaScript");
console.log(todos[0].text, todos.length);
// Console output: Learn JavaScript 1
```

## Activity 2: Search with Cancellation

Create a search input that debounces requests, aborts the previous request, shows loading/error/empty states, validates JSON, and ignores obsolete responses.

## Activity 3: Performance Lab

Render 5,000 rows, record performance, then implement pagination or virtualization. Compare DOM nodes, scripting, layout, memory, and interaction responsiveness.

## Interview Questions with Answers

### 1. `var`, `let`, `const`?

`var` is function-scoped and hoisted with undefined initialization. `let`/`const` are block-scoped and have a temporal dead zone. `const` prevents reassignment.

### 2. `==` vs `===`?

Loose equality performs type coercion. Strict equality compares without that coercion and is the normal choice.

### 3. What is closure?

A function retaining access to variables from its creation scope, even after the outer function returns.

### 4. What is event delegation?

Listen on an ancestor and identify a bubbled event's matching descendant. It reduces listeners and handles dynamically added children.

### 5. Explain the event loop output order.

Current synchronous stack finishes first, then queued microtasks such as Promise reactions, then a later task such as a timer.

### 6. Promise vs async/await?

Async/await is syntax built on Promises. It makes sequential asynchronous control flow read more like synchronous code; it does not create threads.

### 7. Shallow vs deep copy?

Spread/Object.assign copy the outer container; nested objects remain shared. Deep cloning requires supported structured cloning or explicit domain copying.

### 8. Prototype vs class?

JavaScript inheritance is prototype delegation. Class syntax provides a clearer constructor/method/private-field interface over that model.

### 9. How do you prevent XSS?

Keep untrusted data as text, avoid unsafe HTML/script sinks, encode for the output context, sanitize permitted rich HTML, enforce CSP, and validate URLs.

### 10. How do you improve JavaScript performance?

Measure first; reduce shipped/executed code, split by useful journeys, avoid long tasks/layout thrashing, optimize algorithms/DOM size, use caching/workers appropriately, and retest real devices.

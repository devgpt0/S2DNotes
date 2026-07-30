# JavaScript MCQs: predict values, order, and behavior

There are 50 questions: 30 code-snippet questions and 20 theory questions. Predict first, then read the answer.

## Part A: code-snippet MCQs (1-30)

### 1. What does this print?

```js
const user = { name: "Asha" };
user.name = "Priya";
console.log(user.name);
```

- A. Throws because `const` forbids property changes
- B. `Asha`
- C. `Priya`
- D. `undefined`

**Answer: C.** `const` prevents reassignment of `user`, not mutation of its object.

### 2. What does this expression evaluate to?

```js
0 === false;
```

- A. `true`
- B. `false`
- C. `0`
- D. It throws

**Answer: B.** Strict equality compares both type and value.

### 3. What does this print?

```js
console.log(typeof null);
```

- A. `"null"`
- B. `"undefined"`
- C. `"object"`
- D. `"boolean"`

**Answer: C.** This is a historical JavaScript behavior; use `value === null` to test for null.

### 4. What value is assigned to `withOr`?

```js
const retries = 0;
const withOr = retries || 3;
```

- A. `0`
- B. `3`
- C. `null`
- D. It throws

**Answer: B.** `||` falls back for any falsy value, including zero.

### 5. What value is assigned to `withNullish`?

```js
const retries = 0;
const withNullish = retries ?? 3;
```

- A. `0`
- B. `3`
- C. `undefined`
- D. It throws

**Answer: A.** `??` falls back only for `null` or `undefined`.

### 6. What does optional chaining return here?

```js
const user = { name: "Asha" };
const city = user.address?.city;
```

- A. An error
- B. `null`
- C. `undefined`
- D. An empty string

**Answer: C.** Optional chaining stops when `address` is nullish.

### 7. What is the value of `doubled`?

```js
const numbers = [1, 2, 3];
const doubled = numbers.map((number) => number * 2);
```

- A. `[1, 2, 3]`
- B. `[2, 4, 6]`
- C. `6`
- D. `undefined`

**Answer: B.** `map` transforms every item into a new array.

### 8. What does `find` return here?

```js
const scores = [40, 70, 90];
const result = scores.find((score) => score >= 60);
```

- A. `[70, 90]`
- B. `40`
- C. `70`
- D. `true`

**Answer: C.** `find` returns the first matching item, not an array of all matches.

### 9. What is `total`?

```js
const scores = [10, 20, 30];
const total = scores.reduce((sum, score) => sum + score, 0);
```

- A. `0`
- B. `30`
- C. `60`
- D. `[10, 20, 30]`

**Answer: C.** The accumulator starts at zero and adds every score.

### 10. What does `forEach` return?

```js
const result = [1, 2].forEach((number) => number * 2);
```

- A. `[2, 4]`
- B. `2`
- C. `undefined`
- D. A Promise

**Answer: C.** `forEach` is for side effects; it does not create an output array.

### 11. What does this print?

```js
const original = { settings: { theme: "light" } };
const copy = { ...original };
copy.settings.theme = "dark";
console.log(original.settings.theme);
```

- A. `light`
- B. `dark`
- C. `undefined`
- D. It throws

**Answer: B.** Object spread is shallow, so the nested `settings` object is shared.

### 12. What does this print?

```js
const numbers = [10, 2, 1];
numbers.sort();
console.log(numbers);
```

- A. `[1, 2, 10]`
- B. `[10, 2, 1]`
- C. `[1, 10, 2]`
- D. It throws

**Answer: C.** Without a comparator, `sort()` compares string representations.

### 13. Which code creates a numeric sorted copy without changing `numbers`?

```js
const numbers = [10, 2, 1];
```

- A. `numbers.sort()`
- B. `numbers.toSorted((a, b) => a - b)`
- C. `numbers.map((a, b) => a - b)`
- D. `numbers.filter((a, b) => a - b)`

**Answer: B.** `toSorted` returns a new array and the comparator orders numbers.

### 14. What does this closure remember?

```js
function createCounter() {
  let count = 0;
  return () => ++count;
}

const next = createCounter();
console.log(next(), next());
```

- A. `0 0`
- B. `1 1`
- C. `1 2`
- D. It throws

**Answer: C.** The returned function closes over the same `count` variable.

### 15. What happens here?

```js
console.log(score);
const score = 90;
```

- A. Logs `undefined`
- B. Logs `90`
- C. Throws a ReferenceError
- D. Logs `null`

**Answer: C.** `const` exists in the temporal dead zone until initialized.

### 16. What does this method call return?

```js
const learner = {
  name: "Asha",
  greeting() {
    return this.name;
  },
};

console.log(learner.greeting());
```

- A. `Asha`
- B. `undefined`
- C. `this`
- D. A function

**Answer: A.** The method call gives the normal function `this === learner`.

### 17. What is true about this field?

```js
class Account {
  #balance = 0;
}
```

- A. Any caller can read `account.#balance`
- B. It is a runtime private class field
- C. It is a public property named `balance`
- D. It is a CSS selector

**Answer: B.** `#` fields are accessible only from the class body.

### 18. What does this module export?

```js
export function add(left, right) {
  return left + right;
}
```

- A. A default value only
- B. A named export called `add`
- C. Nothing until HTML imports it
- D. A global function

**Answer: B.** Another module can import it with `import { add } from "./math.js"`.

### 19. In what order are messages printed?

```js
console.log("start");
Promise.resolve().then(() => console.log("promise"));
setTimeout(() => console.log("timer"), 0);
console.log("end");
```

- A. start, promise, end, timer
- B. start, end, promise, timer
- C. timer, promise, start, end
- D. start, end, timer, promise

**Answer: B.** Synchronous code finishes, microtasks run, then timer tasks run.

### 20. What does every `async` function return?

```js
async function answer() {
  return 42;
}
```

- A. A number directly
- B. A Promise fulfilled with `42`
- C. `undefined`
- D. A callback

**Answer: B.** `async` wraps returned values in a Promise.

### 21. Why is this check needed?

```js
const response = await fetch("/api/user");
if (!response.ok) {
  throw new Error(`Request failed: ${response.status}`);
}
```

- A. `fetch` rejects for every HTTP 404/500 automatically
- B. HTTP error responses can resolve, so code must check status success
- C. `response.ok` encrypts the response
- D. It makes JSON parse faster

**Answer: B.** `fetch` usually rejects only for network-level failures.

### 22. What does `Promise.all` do if one required request rejects?

```js
await Promise.all([loadProfile(), loadCourses()]);
```

- A. It always returns both values
- B. It resolves with an error value
- C. It rejects
- D. It retries automatically

**Answer: C.** `Promise.all` fails when any input Promise rejects.

### 23. What should replace `innerHTML` for untrusted text?

```js
const message = "<img src=x onerror=alert(1)>";
```

- A. `element.innerHTML = message`
- B. `element.textContent = message`
- C. `eval(message)`
- D. `document.write(message)`

**Answer: B.** `textContent` inserts text without parsing it as HTML.

### 24. What value can this call return?

```js
const saveButton = document.querySelector("#save");
```

- A. Always an element
- B. An element or `null`
- C. A string ID
- D. A NodeList

**Answer: B.** Check the result before using it when the element is required.

### 25. What does this prevent?

```js
form.addEventListener("submit", (event) => {
  event.preventDefault();
});
```

- A. The event from reaching a parent
- B. The form's normal submit/navigation action
- C. All JavaScript errors
- D. Browser focus

**Answer: B.** `preventDefault` stops the default action; it does not stop propagation.

### 26. Why can one listener serve buttons added later?

```js
list.addEventListener("click", (event) => {
  const target = event.target;
  if (!(target instanceof Element)) return;
  const button = target.closest("button[data-id]");
  if (!button || !list.contains(button)) return;
  removeItem(button.dataset.id);
});
```

- A. All buttons share the same ID
- B. Click events bubble to the parent list
- C. `closest` adds a click listener to every button
- D. `dataset` prevents bubbling

**Answer: B.** This is event delegation: a parent reacts to bubbled child events.

### 27. What must happen before storing this object in `localStorage`?

```js
const preferences = { theme: "dark" };
```

- A. Convert it with `JSON.stringify`
- B. Call `toSorted`
- C. Add an event listener
- D. Use `innerHTML`

**Answer: A.** Web Storage stores string key/value pairs.

### 28. What does this expression safely handle?

```js
const preferences = JSON.parse(localStorage.getItem("preferences") ?? "{}");
```

- A. A missing storage key
- B. Invalid JSON text
- C. Network errors
- D. A server redirect

**Answer: A.** `?? "{}"` supplies valid fallback text only when the item is absent; invalid stored JSON would still throw.

### 29. What collection is produced?

```js
const tags = [...new Set(["js", "css", "js"])];
```

- A. `["js", "css", "js"]`
- B. `["js", "css"]`
- C. A Map with two entries
- D. A string

**Answer: B.** A Set keeps unique values, and spread returns them in an array.

### 30. What does this cancellation setup enable?

```js
const controller = new AbortController();
fetch("/api/search?q=css", { signal: controller.signal });
controller.abort();
```

- A. It converts the response to JSON
- B. It requests cancellation of the in-flight fetch
- C. It retries the request
- D. It prevents every network request on the page

**Answer: B.** AbortController lets obsolete work be cancelled.

## Part B: theory MCQs (31-50)

### 31. Which declaration should be the default for a binding that will not be reassigned?

- A. `var`
- B. `let`
- C. `const`
- D. `static`

**Answer: C.** Use `let` only when the binding itself must change.

### 32. What is a closure?

- A. A syntax error
- B. A function retaining access to variables from where it was created
- C. A closed browser tab
- D. A private class only

**Answer: B.** Closures enable callbacks, private state, and factory functions.

### 33. When should `for...of` normally be used?

- A. To iterate values in an array or other iterable
- B. To iterate CSS selectors
- C. To make a deep copy
- D. To catch errors

**Answer: A.** `for...in` instead iterates enumerable property keys.

### 34. Which array operation mutates its original array?

- A. `map`
- B. `filter`
- C. `sort`
- D. `toSorted`

**Answer: C.** `sort` changes the input array in place.

### 35. When is `Map` often clearer than a plain object?

- A. When keys may be any value, including objects
- B. When CSS needs a selector
- C. When the data must be JSON only
- D. When a webpage needs a heading

**Answer: A.** Maps support keys of any type and provide explicit map operations.

### 36. What does an arrow function *not* create?

- A. A return value
- B. Its own `this`
- C. A function value
- D. A lexical scope

**Answer: B.** It captures the surrounding `this` instead.

### 37. Why use ES modules?

- A. To make all values global
- B. To declare dependencies and exports explicitly
- C. To replace all functions
- D. To avoid strict mode

**Answer: B.** Modules have their own scope and make code organization clearer.

### 38. What runs before the next timer task after synchronous code completes?

- A. Promise microtasks
- B. A random event listener
- C. Page navigation only
- D. CSS parsing only

**Answer: A.** Promise callbacks run in the microtask queue.

### 39. When should `Promise.allSettled` be considered instead of `Promise.all`?

- A. When every result matters even if some operations fail
- B. When only the first result matters
- C. When code must be synchronous
- D. When values are CSS colors

**Answer: A.** It reports every fulfilled or rejected outcome.

### 40. Why should browser code check `response.ok` after `fetch`?

- A. It checks whether a network request was made
- B. HTTP 4xx/5xx responses may not reject the fetch Promise
- C. It validates the response JSON schema
- D. It prevents XSS automatically

**Answer: B.** Status failures need explicit handling.

### 41. What is the safest DOM API for displaying arbitrary user text?

- A. `innerHTML`
- B. `textContent`
- C. `eval`
- D. `outerHTML`

**Answer: B.** It avoids interpreting the supplied string as markup.

### 42. What is event delegation?

- A. Removing all event listeners
- B. A parent listener handling bubbled events from matching descendants
- C. Adding a listener to every new item manually
- D. Preventing default browser behavior

**Answer: B.** It is especially helpful for dynamic lists.

### 43. When should an error be caught?

- A. Always, with an empty catch block
- B. Only when code can recover, add useful context, or clean up
- C. Never
- D. Only inside a loop

**Answer: B.** Unhandled errors should otherwise propagate to an appropriate boundary.

### 44. Why should secrets not be stored in `localStorage`?

- A. It only stores strings
- B. Same-origin JavaScript can read it, including injected script in an XSS attack
- C. It deletes all data on refresh
- D. It is asynchronous

**Answer: B.** Security-sensitive session design commonly uses secure, HttpOnly cookies instead.

### 45. What is a shallow copy?

- A. A copy with no own properties
- B. A new outer container that still shares nested references
- C. A frozen object
- D. A serialized JSON document

**Answer: B.** Object/array spread copies only one level.

### 46. Why validate external data at boundaries?

- A. Dynamic typing means input may not match the code's expected shape
- B. It makes arrays faster
- C. It removes the DOM
- D. It changes strict equality

**Answer: A.** Validate API data, form values, storage data, and other untrusted inputs before relying on them.

### 47. What should be measured before performance changes are made?

- A. A real bottleneck, such as a long task or slow operation
- B. Only code length
- C. The number of semicolons
- D. The page title

**Answer: A.** Profiling avoids needless complexity and targets actual problems.

### 48. What is a common use for debounce?

- A. Run a search after rapid typing settles
- B. Run every scroll event immediately
- C. Deep-copy an object
- D. Encrypt a request

**Answer: A.** Debounce delays repeated work until calls pause.

### 49. What must be cleaned up when a component or page feature is destroyed?

- A. Only variables declared with `const`
- B. Owned listeners, timers, observers, and subscriptions
- C. Every HTML element on the page
- D. All browser cookies

**Answer: B.** Cleanup prevents unwanted work and retained memory.

### 50. What is the best default response to a surprising JavaScript result?

- A. Add type coercion until it works
- B. Inspect values and types, then make the intended conversion or check explicit
- C. Replace every `const` with `var`
- D. Suppress the error

**Answer: B.** Explicit data handling produces code that is easier to debug and maintain.

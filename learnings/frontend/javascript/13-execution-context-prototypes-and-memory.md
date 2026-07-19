# 13 - Execution Contexts, Hoisting, Prototypes, and Memory

This chapter explains the runtime ideas behind scope, closures, objects, and common interview questions. Learn the visible behavior first; use the formal terms to explain it precisely later.

## How a Function Call Runs

Each active function call gets execution state containing its parameters, local bindings, current instruction, and access to outer lexical environments.

```javascript
const multiply = (left, right) => {
  const result = left * right;
  return result;
};

const total = multiply(4, 5);
console.log(total);
// Output: 20
```

Simplified call flow:

1. global/module code calls `multiply`
2. a new call frame stores `left = 4`, `right = 5`, and `result`
3. the frame returns `20`
4. the frame leaves the call stack

The **call stack** is the last-in, first-out stack of active calls.

## Stack Overflow

Recursion needs a stopping condition:

```javascript
const countdown = (value) => {
  if (value <= 0) return;
  countdown(value - 1);
};

countdown(3);
console.log("finished");
// Output: finished
```

Unbounded recursion eventually throws a range error because calls keep occupying the stack.

## Lexical Environments

A lexical environment connects names to values for a scope. Functions remember the environment where they were created.

```javascript
const createCourseLabel = (prefix) => {
  return (title) => `${prefix}: ${title}`;
};

const lessonLabel = createCourseLabel("Lesson");
console.log(lessonLabel("Closures"));
// Output: Lesson: Closures
```

The returned function keeps access to `prefix`. That retained relationship is closure behavior.

## Hoisting in Plain Language

Before executing a scope, JavaScript creates its bindings. Different declarations become usable at different times.

### Function Declaration

```javascript
console.log(declared());
function declared() {
  return "ready";
}
// Output: ready
```

The function binding is initialized before that source line executes.

### `var`

```javascript
console.log(oldValue);
var oldValue = 10;
// Output: undefined
```

The binding exists early and starts as `undefined`. This behavior is one reason modern code avoids `var`.

### `let`, `const`, and `class`

```javascript
// console.log(course); // ReferenceError
const course = "JavaScript";
console.log(course);
// Output: JavaScript
```

The binding exists but cannot be accessed before initialization. This period is the **temporal dead zone**.

## Why Arrow Variables Improve Reading Order

```javascript
const parseCourse = (value) => {
  // validation
  return value;
};
```

The function becomes usable at its initialization line. A reader can follow setup top to bottom instead of searching for a hoisted implementation.

## Objects and Property Lookup

An object has its own properties and an internal link to a prototype.

```javascript
const baseCourse = { category: "programming" };
const course = Object.create(baseCourse);
course.title = "JavaScript";

console.log(course.title);
console.log(course.category);
console.log(Object.hasOwn(course, "category"));
// Output:
// JavaScript
// programming
// false
```

Lookup checks `course` first, then follows its prototype chain.

Use `Object.hasOwn` when the question is specifically about the object's own data.

## Constructor Functions and `new`

Arrow functions cannot be constructors. This traditional constructor function is shown to explain `new`:

```javascript
function Course(title) {
  this.title = title;
}

Course.prototype.label = function label() {
  return `Course: ${this.title}`;
};

const course = new Course("JavaScript");
console.log(course.label());
// Output: Course: JavaScript
```

Simplified `new` behavior:

1. create a new object
2. connect it to `Course.prototype`
3. call `Course` with the new object as `this`
4. return the object unless the constructor explicitly returns another object

Modern `class` syntax expresses this relationship more clearly, but it still uses prototypes at runtime.

## Class Fields and Arrow Fields

```javascript
class Counter {
  count = 0;

  increment = () => {
    this.count += 1;
    return this.count;
  };
}

const counter = new Counter();
const increment = counter.increment;
console.log(increment());
// Output: 1
```

The arrow field captures the instance `this`, which is useful when passing the callback. It also creates a function per instance. A prototype method is shared and should be preferred when binding is not needed.

## Property Descriptors

Properties have behavior flags:

```javascript
const course = {};
Object.defineProperty(course, "id", {
  value: "js",
  writable: false,
  enumerable: true,
  configurable: false,
});

console.log(Object.getOwnPropertyDescriptor(course, "id"));
// Output describes value and the three flags.
```

- writable: value can be assigned
- enumerable: appears in common enumeration
- configurable: descriptor can be changed or property deleted

Modules and ordinary domain objects rarely need custom descriptors, but frameworks and libraries use them.

## Equality and Identity

Objects compare by identity:

```javascript
console.log({ id: 1 } === { id: 1 });
const first = { id: 1 };
const second = first;
console.log(first === second);
// Output:
// false
// true
```

For value equality, compare validated fields or use a domain-specific equality function.

## Garbage Collection

JavaScript engines reclaim memory for values no longer reachable from live roots.

```javascript
let course = { largeData: new Array(10_000).fill("x") };
course = null;
```

After reassignment, the old object may become unreachable and eligible for collection. Collection time is controlled by the engine.

## Common Retention Causes

- an event listener still references a closure
- an interval is never cleared
- a cache grows without a bound
- a detached DOM node remains in an array or map
- a subscription keeps its callback
- a pending task retains large captured data

Use explicit ownership and cleanup:

```javascript
const mount = (button) => {
  const controller = new AbortController();
  button.addEventListener("click", () => console.log("clicked"), {
    signal: controller.signal,
  });
  return () => controller.abort();
};
```

## Weak References

`WeakMap` keys and `WeakSet` values do not keep their object keys alive by themselves.

```javascript
const metadata = new WeakMap();
const element = document.createElement("button");
metadata.set(element, { mountedAt: performance.now() });
console.log(metadata.has(element));
// Output: true
```

Weak collections are not enumerable because garbage collection is intentionally not observable in that way. Do not use them as ordinary application stores.

## Module Evaluation

ES modules are loaded, linked, then evaluated. Imports are live bindings, not copied snapshots.

```javascript
// counter.js
export let count = 0;
export const increment = () => { count += 1; };
```

```javascript
// app.js
import { count, increment } from "./counter.js";
increment();
console.log(count);
// Output: 1
```

Circular runtime dependencies can expose bindings before initialization. Break cycles through ownership and dependency direction rather than relying on fragile execution order.

## Expert Checklist

- explain scope using lexical environments, not “the function remembers everything”
- distinguish binding creation from initialization
- distinguish own properties from prototype lookup
- choose prototype methods vs per-instance arrow fields deliberately
- treat memory as reachability and lifecycle, not manual freeing
- review module cycles as architecture problems

## Final Rule

Use runtime internals to explain observed behavior. Do not optimize based on engine folklore; profile real code on supported environments.

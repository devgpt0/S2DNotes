# 01 - JavaScript Runtime, Variables, Values, and Types

## Where JavaScript Runs

In a browser, an engine executes JavaScript while browser Web APIs provide DOM, timers, Fetch, storage, and other capabilities. JavaScript itself and browser APIs are related but not identical.

```html
<script type="module" src="app.js"></script>
<!-- Browser behavior: downloads app.js without blocking parsing and executes it as a strict module after parsing. -->
```

## `const` and `let`

```javascript
const course = "JavaScript";
let completedLessons = 0;
completedLessons += 1;
console.log(course, completedLessons);
// Console output: JavaScript 1
```

Use `const` unless the variable must be reassigned. Avoid `var` in modern code because function scope and hoisting behavior cause avoidable mistakes.

`const` prevents reassignment, not object mutation.

```javascript
const student = { name: "Asha" };
student.name = "Anu";
console.log(student.name);
// Console output: Anu
```

## Primitive Types

- string
- number
- bigint
- boolean
- undefined
- symbol
- null (historical `typeof` reports `object`)

Objects and functions are non-primitive values.

```javascript
console.log(typeof "hello");
console.log(typeof 42);
console.log(typeof true);
console.log(typeof undefined);
console.log(typeof null);
// Console output:
// string
// number
// boolean
// undefined
// object
```

## `undefined` vs `null`

`undefined` usually means no value has been assigned/provided. `null` is an intentional “no object/value” marker chosen by code or an API.

## Numbers

JavaScript `number` is IEEE-754 floating point, including integers within a safe range.

```javascript
console.log(0.1 + 0.2);
console.log(Number.isSafeInteger(9_007_199_254_740_991));
// Console output:
// 0.30000000000000004
// true
```

Use integer minor units or a decimal library for exact money. Use `bigint` for integers beyond safe number range when compatible with APIs/serialization.

```javascript
console.log(10n + 20n);
// Console output: 30n
// Mixing bigint and number arithmetic throws TypeError.
```

## Value vs Reference Behavior

```javascript
const first = { score: 1 };
const second = first;
second.score = 2;
console.log(first.score);
// Console output: 2
```

Both variables reference the same object. JavaScript passes arguments by value; for objects, that copied value is a reference.

## Template Literals

```javascript
const name = "Asha";
console.log(`Hello ${name}`);
// Console output: Hello Asha
```

Tagged templates can process template parts, but they do not automatically make HTML or SQL safe.

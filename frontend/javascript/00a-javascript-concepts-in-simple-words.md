# JavaScript Concepts in Simple Words

Read this before chapter 01 if JavaScript is new to you.

## What JavaScript Does

HTML gives a page structure. CSS controls presentation. JavaScript reads values, makes decisions, reacts to events, requests data, and changes the page.

```html
<button id="greet">Greet</button>
<p id="message"></p>
<script type="module" src="app.js"></script>
```

```javascript
const button = document.querySelector("#greet");
const message = document.querySelector("#message");

if (!(button instanceof HTMLButtonElement)
  || !(message instanceof HTMLParagraphElement)) {
  throw new Error("required elements are missing");
}

button.addEventListener("click", () => {
  message.textContent = "Hello, learner";
});
// Browser result: clicking the button shows "Hello, learner".
```

## JavaScript Runs Instructions in Order

```javascript
const price = 100;
const quantity = 2;
const total = price * quantity;
console.log(total);
// Output: 200
```

1. create `price`
2. create `quantity`
3. multiply them
4. store the result
5. print it

## Values and Variables

Common values:

```javascript
const title = "JavaScript"; // string
const lessons = 12;         // number
const published = true;     // boolean
const selected = null;      // intentional empty value
let result;                 // undefined until assigned
```

Use `const` when the variable will not be reassigned. Use `let` when reassignment is part of the logic.

## Functions

A function stores behavior.

```javascript
const doubleNumber = (number) => number * 2;
console.log(doubleNumber(5));
// Output: 10
```

- `doubleNumber`: variable holding the function
- `number`: input parameter
- `number * 2`: returned result

These notes use arrow functions assigned to `const` for standalone behavior. Object/class methods and generators use their correct language syntax when needed.

## Conditions

```javascript
const score = 80;
if (score >= 70) {
  console.log("Passed");
} else {
  console.log("Try again");
}
// Output: Passed
```

A condition chooses one path.

## Arrays

An array stores ordered values:

```javascript
const courses = ["HTML", "CSS", "JavaScript"];
console.log(courses[0]);
console.log(courses.length);
// Output:
// HTML
// 3
```

Array positions start at zero.

## Objects

An object groups named values:

```javascript
const course = {
  id: "js",
  title: "JavaScript",
};
console.log(course.title);
// Output: JavaScript
```

Arrays answer “which position?” Objects answer “which property name?”

## Loops and Array Methods

```javascript
for (const course of ["HTML", "CSS"]) {
  console.log(course);
}
// Output:
// HTML
// CSS
```

Transform a list:

```javascript
const lengths = ["HTML", "CSS"].map((course) => course.length);
console.log(lengths);
// Output: [4, 3]
```

Use the version that makes the work easiest to understand.

## Errors

Invalid input should fail clearly:

```javascript
const divide = (left, right) => {
  if (right === 0) throw new RangeError("right cannot be zero");
  return left / right;
};
console.log(divide(10, 2));
// Output: 5
```

Catch an error only where you can recover, translate it, retry safely, or show useful feedback.

## DOM

The DOM is the browser's object representation of the document.

```javascript
const heading = document.querySelector("h1");
if (!(heading instanceof HTMLHeadingElement)) throw new Error("heading is missing");
heading.textContent = "JavaScript Foundations";
```

Use `textContent` for untrusted plain text. Do not place user data into `innerHTML`.

## Events

Events tell your code something happened:

```javascript
button.addEventListener("click", () => {
  console.log("button clicked");
});
// Output after click: button clicked
```

Examples include click, input, submit, keyboard, network completion, and messages.

## Async Work

Some results arrive later:

```javascript
const loadCourse = async () => {
  const response = await fetch("/api/course");
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  return response.json();
};
```

An async function returns a Promise. `await` pauses only that async function, not the whole browser.

## Modules

Modules split code into explicit files:

```javascript
// math.js
export const add = (left, right) => left + right;
```

```javascript
// app.js
import { add } from "./math.js";
console.log(add(2, 3));
// Output: 5
```

## Browser Storage

Not every value should be saved.

- memory: current UI state
- URL: shareable filters/navigation
- sessionStorage: small one-tab temporary data
- localStorage: small non-sensitive preference
- IndexedDB: structured offline data
- server: authoritative shared data

Read the complete browser storage guide before choosing.

## Security Basics

- validate external data
- render text safely
- validate URLs
- keep secrets out of frontend bundles
- enforce authorization on the server
- do not trust storage or API JSON automatically

## Beginner to Expert Path

1. values, variables, conditions, loops, functions
2. arrays, objects, errors, modules
3. DOM, events, forms, async Fetch
4. prototypes, iterators, workers, streams
5. architecture, security, performance, memory

## Ready to Continue?

Explain this without running it:

```javascript
const values = [1, 2, 3];
const result = values.filter((value) => value > 1).map((value) => value * 10);
console.log(result);
// Output: [20, 30]
```

The filter keeps `2` and `3`; map changes them to `20` and `30`.

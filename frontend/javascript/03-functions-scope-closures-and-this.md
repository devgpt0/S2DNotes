# 03 - Functions, Scope, Closures, and `this`

## Start with the Main Idea

A function stores reusable behavior.

These notes use an arrow function assigned to a `const` by default:

```javascript
const add = (left, right) => left + right;
console.log(add(2, 3));
// Output: 5
```

Read it as: create a constant variable named `add`; its value is a function that receives two inputs and returns their sum.

## Why `const name = () => {}` Is the Default Here

- the name cannot be reassigned accidentally
- the function is created where the variable is initialized
- arrow functions do not create a surprising dynamic `this`
- callbacks and small transformations use the same readable form
- it is easy to distinguish a standalone function value from a class/object method

This is a project convention, not a claim that `function` declarations are invalid.

## Expression Body and Block Body

One expression is returned automatically:

```javascript
const doubleNumber = (number) => number * 2;
console.log(doubleNumber(6));
// Output: 12
```

Use braces for several statements, and write `return` when a value must come back:

```javascript
const calculateTotal = (price, quantity) => {
  if (!Number.isFinite(price) || !Number.isSafeInteger(quantity) || quantity < 0) {
    throw new TypeError("price and quantity are invalid");
  }
  const total = price * quantity;
  return total;
};

console.log(calculateTotal(99.5, 2));
// Output: 199
```

## Parameters and Arguments

- **parameter:** input name in the function definition
- **argument:** actual value passed during a call

```javascript
const greet = (name = "Guest") => `Hello, ${name}`;
console.log(greet());
console.log(greet("Asha"));
// Output:
// Hello, Guest
// Hello, Asha
```

Rest parameters collect remaining arguments into an array:

```javascript
const sum = (...values) => values.reduce((total, value) => total + value, 0);
console.log(sum(10, 20, 30));
// Output: 60
```

JavaScript does not validate argument types for you. Validate values at external or domain boundaries.

## Functions Are Values

A function can be stored, passed, and returned:

```javascript
const applyTwice = (operation, value) => operation(operation(value));
const addOne = (number) => number + 1;

console.log(applyTwice(addOne, 5));
// Output: 7
```

A function that accepts or returns another function is called a **higher-order function**.

## Scope

Scope answers: “Where can this name be used?”

```javascript
const course = "JavaScript"; // module/global scope for this file

const printLesson = () => {
  const lesson = "Closures"; // function scope
  if (lesson.length > 0) {
    const message = `${course}: ${lesson}`; // block scope
    console.log(message);
  }
  // console.log(message); // ReferenceError: message is outside its block.
};

printLesson();
// Output: JavaScript: Closures
```

`const` and `let` are block-scoped. Prefer the smallest scope that contains every required use.

## Lexical Scope

JavaScript resolves names from where a function was **written**, not from where it is called.

```javascript
const label = "outer";

const createReader = () => {
  const label = "inside createReader";
  return () => label;
};

const readLabel = createReader();
console.log(readLabel());
// Output: inside createReader
```

The caller's location does not change which `label` the returned function uses.

## Closure

A closure is a function together with access to names from its lexical environment.

```javascript
const createCounter = () => {
  let count = 0;
  return () => {
    count += 1;
    return count;
  };
};

const nextCount = createCounter();
console.log(nextCount());
console.log(nextCount());
// Output:
// 1
// 2
```

Step by step:

1. `createCounter` creates one private `count` variable.
2. It returns an arrow function.
3. The returned function keeps access to that `count`.
4. Each call changes the same retained value.

Closures power callbacks, module privacy, memoization, and event handlers. They can also retain memory longer than intended when a listener, timer, or cache outlives its owner.

## Arrow Functions and `this`

Arrow functions do not create their own `this`. They use `this` from the surrounding lexical scope.

That makes them excellent callbacks:

```javascript
const course = {
  title: "JavaScript",
  lessons: ["Scope", "Closure"],
  printLessons() {
    this.lessons.forEach((lesson) => {
      console.log(`${this.title}: ${lesson}`);
    });
  },
};

course.printLessons();
// Output:
// JavaScript: Scope
// JavaScript: Closure
```

`printLessons` is a real object method because it needs the receiving object as `this`. The inner callback is an arrow so it uses the method's `this`.

## Do Not Use an Arrow as a Dynamic-`this` Method

```javascript
const brokenCourse = {
  title: "JavaScript",
  printTitle: () => console.log(this.title),
};

brokenCourse.printTitle();
// Output is not "JavaScript" because the arrow does not receive brokenCourse as this.
```

Use method syntax when the operation intentionally depends on the receiver:

```javascript
const workingCourse = {
  title: "JavaScript",
  printTitle() {
    console.log(this.title);
  },
};

workingCourse.printTitle();
// Output: JavaScript
```

## `call`, `apply`, and `bind`

These APIs can set `this` for ordinary functions and methods. They cannot replace lexical `this` inside an arrow.

```javascript
const learner = { name: "Asha" };

function greeting(prefix) {
  return `${prefix} ${this.name}`;
}

console.log(greeting.call(learner, "Hello"));
console.log(greeting.apply(learner, ["Welcome"]));
const boundGreeting = greeting.bind(learner, "Hi");
console.log(boundGreeting());
// Output:
// Hello Asha
// Welcome Asha
// Hi Asha
```

This deliberate ordinary function demonstrates dynamic `this`. In most application code, explicit parameters are simpler:

```javascript
const greetingFor = (person, prefix) => `${prefix} ${person.name}`;
console.log(greetingFor(learner, "Hello"));
// Output: Hello Asha
```

## Hoisting and the Temporal Dead Zone

A function declaration can be called before its source line because its binding is initialized during environment setup:

```javascript
console.log(declared());
function declared() {
  return "available early";
}
// Output: available early
```

An arrow assigned to `const` cannot be used before initialization:

```javascript
// console.log(arrow()); // ReferenceError
const arrow = () => "available after this line";
console.log(arrow());
// Output: available after this line
```

This predictable top-to-bottom availability is one reason these notes prefer `const` arrows.

## Cases Where Arrow Functions Cannot Replace Other Syntax

- constructors called with `new`
- generators written with `function*`
- object/class methods that require dynamic receiver `this`
- APIs or demonstrations specifically about `arguments`
- some TypeScript overload implementations, unless a call-signature type is used

Use the correct language feature rather than forcing one style everywhere.

## Pure and Impure Functions

A pure function returns the same result for the same inputs and does not change outside state:

```javascript
const calculateTax = (amount, rate) => amount * rate;
console.log(calculateTax(1_000, 0.18));
// Output: 180
```

An impure function can still be required:

```javascript
const showMessage = (element, message) => {
  element.textContent = message;
};
```

Keep calculations pure when practical. Keep necessary side effects at clear boundaries.

## Beginner to Expert Checklist

- beginner: parameters, return values, expression/block arrows
- developer: callbacks, higher-order functions, scope, closure
- senior: lifecycle of captured data, pure boundaries, explicit dependencies
- expert: lexical vs dynamic `this`, hoisting, callability/constructability, memory retention, engine optimization based on evidence

## Practice

Create a multiplier factory:

```javascript
const createMultiplier = (factor) => (value) => value * factor;
const triple = createMultiplier(3);
console.log(triple(7));
// Output: 21
```

Explain which value the closure remembers and why `factor` remains available after `createMultiplier` returns.

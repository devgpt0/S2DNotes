# 03 - Functions, Scope, Closures, and `this`

## Function Forms

```javascript
function add(left, right) { return left + right; }
const multiply = function (left, right) { return left * right; };
const square = value => value * value;
console.log(add(2, 3), multiply(2, 3), square(4));
// Console output: 5 6 16
```

Function declarations are hoisted with their body. Function expressions follow the initialization rules of their variable.

## Parameters

```javascript
function greet(name = "Guest") { return `Hello ${name}`; }
function sum(...values) { return values.reduce((total, value) => total + value, 0); }
console.log(greet(), sum(1, 2, 3));
// Console output: Hello Guest 6
```

Rest collects values. Spread expands an iterable or object properties in supported positions.

## Scope

`let` and `const` are block scoped. Functions create function scope. Modules create module scope.

```javascript
const outside = "visible";
if (true) {
  const inside = "block only";
  console.log(outside, inside);
}
// Console output: visible block only
// Accessing inside after the block throws ReferenceError.
```

## Closure

A closure is a function together with access to variables from where it was created.

```javascript
function createCounter() {
  let count = 0;
  return () => ++count;
}
const next = createCounter();
console.log(next(), next());
// Console output: 1 2
```

Closures support private state, callbacks, and factories, but can retain large objects longer than intended.

## `this`

For normal functions, `this` depends on how the function is called. Arrow functions capture lexical `this` and do not create their own.

```javascript
const user = {
  name: "Asha",
  greet() { return `Hello ${this.name}`; },
};
console.log(user.greet());
// Console output: Hello Asha
```

```javascript
const detached = user.greet;
try { console.log(detached()); } catch (error) { console.log(error.name); }
// Module console output: TypeError
```

Use `bind`, call through the object, or design a function that accepts dependencies explicitly.

## Call, Apply, Bind

```javascript
function greeting(prefix) { return `${prefix} ${this.name}`; }
console.log(greeting.call({ name: "Ravi" }, "Hello"));
console.log(greeting.bind({ name: "Anu" })("Hi"));
// Console output:
// Hello Ravi
// Hi Anu
```

## Higher-Order Functions

A higher-order function receives or returns a function.

```javascript
const withTax = rate => price => price * (1 + rate);
console.log(withTax(0.18)(100));
// Console output: 118
```

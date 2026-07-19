# 08 - Prototypes, Classes, Iterators, and Generators

## Prototype Chain

Objects can delegate missing property lookup to a prototype.

```javascript
const animal = { speak() { return "sound"; } };
const dog = Object.create(animal);
dog.name = "Milo";
console.log(dog.speak(), Object.hasOwn(dog, "speak"));
// Console output: sound false
```

## Classes

Class syntax is a clearer layer over prototypes.

```javascript
class Counter {
  #value = 0;
  increment() { this.#value += 1; }
  get value() { return this.#value; }
}
const counter = new Counter();
counter.increment();
console.log(counter.value);
// Console output: 1
```

Private fields use `#` and are enforced by the language.

## Inheritance vs Composition

Use inheritance only for a true substitutable relationship. Prefer composing small objects/functions for flexible behavior.

## Iterator Protocol

An iterator has `next()` returning `{ value, done }`. An iterable exposes `Symbol.iterator`.

```javascript
const iterator = ["A", "B"][Symbol.iterator]();
console.log(iterator.next());
console.log(iterator.next());
// Console output:
// {value: "A", done: false}
// {value: "B", done: false}
```

Console formatting varies slightly by browser.

## Generator

```javascript
function* ids() {
  yield 1;
  yield 2;
}
console.log([...ids()]);
// Console output: [1, 2]
```

Generators create iterators and pause at `yield`. They are useful for lazy sequences and protocol adapters.

## Async Iteration

```javascript
async function* messages() {
  yield "first";
  yield "second";
}
for await (const message of messages()) console.log(message);
// Module console output:
// first
// second
```

Async iterables model values arriving over time, such as streams or paginated requests.

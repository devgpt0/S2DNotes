# JavaScript Concepts in Simple Words

## The One-Sentence Idea

JavaScript runs instructions, stores values, calls functions, reacts to events, and coordinates asynchronous browser work.

## Runtime Picture

```text
call stack runs JavaScript
browser APIs handle timers/network/DOM
event loop schedules queued work when stack is free
# Result: JavaScript stays responsive only when main-thread tasks remain short.
```

## Core Concepts

| Concept | Simple meaning |
|---|---|
| value/type | data and its allowed operations |
| variable | name holding a value |
| function | reusable behavior and scope |
| object | keyed values/behavior |
| array | ordered values |
| closure | function retains creation-scope variables |
| DOM | browser object tree for HTML |
| event | notification that something happened |
| Promise | handle for a future success/failure |
| module | file with explicit imports/exports |

## Data Flow Example

```javascript
const courses = [{ title: "HTML", active: true }, { title: "Old CSS", active: false }];
const titles = courses.filter(course => course.active).map(course => course.title);
console.log(titles);
// Console output: ["HTML"]
```

Read it left to right: take courses -> keep active -> extract title -> print result.

## DOM Flow Example

```javascript
const button = document.querySelector("button");
if (!button) throw new Error("button is required");
button.addEventListener("click", () => console.log("clicked"));
// Console output after user activates button: clicked
```

## Async Flow Example

```javascript
console.log("start");
Promise.resolve().then(() => console.log("later"));
console.log("end");
// Console output:
// start
// end
// later
```

## Learning Order

Values -> conditions/loops -> functions/scope -> arrays/objects -> errors/modules -> DOM/events -> Promise/async -> browser APIs/performance -> architecture/testing.

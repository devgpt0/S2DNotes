# 04 - Arrays, Objects, Map, Set, JSON, and Immutability

## Arrays

```javascript
const values = [3, 1, 2];
console.log(values.length, values[0]);
// Console output: 3 3
```

Common methods:

```javascript
const numbers = [1, 2, 3, 4];
const result = numbers.filter(value => value % 2 === 0).map(value => value * 10);
console.log(result);
console.log(numbers);
// Console output:
// [20, 40]
// [1, 2, 3, 4]
```

`map`, `filter`, `slice`, `toSorted`, and spread can create new arrays. `push`, `pop`, `splice`, `sort`, and `reverse` mutate the array.

## Reduce

```javascript
const total = [10, 20, 30].reduce((sum, value) => sum + value, 0);
console.log(total);
// Console output: 60
```

Use a loop when it explains complex accumulation more clearly.

## Objects and Destructuring

```javascript
const course = { title: "HTML", price: 500 };
const { title, price: coursePrice } = course;
console.log(title, coursePrice);
// Console output: HTML 500
```

## Spread Is Shallow

```javascript
const original = { profile: { name: "Asha" } };
const copy = { ...original };
copy.profile.name = "Anu";
console.log(original.profile.name);
// Console output: Anu
// Nested profile is still shared.
```

Use `structuredClone` for supported data when a deep copy is genuinely needed; functions and some platform objects are not cloneable.

## Map and Set

```javascript
const scores = new Map([["Asha", 90]]);
scores.set("Ravi", 80);
console.log(scores.get("Asha"));

const unique = new Set([1, 2, 2, 3]);
console.log([...unique]);
// Console output:
// 90
// [1, 2, 3]
```

Map supports keys of any value and explicit size/iteration APIs. Set stores unique values using SameValueZero equality.

## JSON

```javascript
const text = JSON.stringify({ name: "Asha", active: true });
console.log(text);
console.log(JSON.parse(text).name);
// Console output:
// {"name":"Asha","active":true}
// Asha
```

JSON does not preserve functions, undefined object properties, BigInt, prototypes, Map, Set, or Date type. Parse external JSON and validate its schema before use.

## Property Tools

Use `Object.keys/values/entries`, `Object.hasOwn`, optional chaining, and nullish coalescing. Avoid prototype-pollution-prone merging of untrusted keys.

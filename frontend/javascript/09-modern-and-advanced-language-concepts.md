# 09 - Modern and Advanced JavaScript Concepts

## Symbol

Symbols are unique primitive keys.

```javascript
const id = Symbol("id");
const user = { [id]: 7 };
console.log(user[id], String(id));
// Console output: 7 Symbol(id)
```

Well-known symbols customize protocols such as iteration.

## Property Descriptors

```javascript
const object = {};
Object.defineProperty(object, "id", { value: 7, writable: false, enumerable: true });
console.log(object.id, Object.keys(object));
// Console output: 7 ["id"]
```

In modules/strict mode, assigning to the non-writable property throws.

## Proxy and Reflect

```javascript
const target = { name: "Asha" };
const proxy = new Proxy(target, {
  get(object, property, receiver) {
    console.log(`read ${String(property)}`);
    return Reflect.get(object, property, receiver);
  },
});
console.log(proxy.name);
// Console output:
// read name
// Asha
```

Proxies power some reactive systems but can complicate identity, debugging, and performance.

## Regular Expressions

```javascript
const match = /^(?<prefix>[A-Z]+)-(?<id>\d+)$/.exec("ORD-42");
console.log(match?.groups);
// Console output: {prefix: "ORD", id: "42"} (format varies by console).
```

Avoid catastrophic backtracking and limit untrusted input length.

## Date and Intl

```javascript
const date = new Date("2026-07-18T00:00:00Z");
console.log(new Intl.DateTimeFormat("en-IN", { dateStyle: "medium", timeZone: "UTC" }).format(date));
// Console output: 18 Jul 2026
```

Use explicit time zones and locale-aware formatting. Do not parse ambiguous date strings.

## Functional Concepts

- pure function: same input gives same output and no external side effect
- immutability: create updated values rather than mutating shared state
- composition: build behavior by combining functions
- memoization: cache a pure expensive result with bounded ownership

## WeakMap and WeakSet

They hold object keys weakly and are useful for object-associated metadata. They are not iterable because garbage collection is nondeterministic.

## Typed Arrays

`ArrayBuffer`, `Uint8Array`, and related views represent binary data for files, graphics, audio, and protocols. They have fixed byte-oriented storage unlike normal arrays.

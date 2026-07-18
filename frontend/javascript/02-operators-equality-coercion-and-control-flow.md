# 02 - Operators, Equality, Coercion, and Control Flow

## Strict Equality

Prefer `===` and `!==` because they do not perform broad type coercion.

```javascript
console.log(5 === "5");
console.log(5 == "5");
// Console output:
// false
// true
```

Use loose equality only with a deliberate documented reason.

## Truthy and Falsy

Falsy values: `false`, `0`, `-0`, `0n`, `""`, `null`, `undefined`, and `NaN`. Arrays and objects are truthy even when empty.

```javascript
console.log(Boolean([]));
console.log(Boolean(""));
// Console output:
// true
// false
```

## Nullish Coalescing

`??` uses fallback only for `null` or `undefined`; `||` also treats `0`, false, and empty string as missing.

```javascript
const count = 0;
console.log(count ?? 10);
console.log(count || 10);
// Console output:
// 0
// 10
```

## Optional Chaining

```javascript
const user = { profile: { name: "Asha" } };
console.log(user.profile?.name);
console.log(user.address?.city ?? "Unknown");
// Console output:
// Asha
// Unknown
```

Optional chaining handles absence; it should not hide a value that the schema requires.

## Conditions and Switch

```javascript
const role = "admin";
if (role === "admin") console.log("full access");

const label = role === "admin" ? "Administrator" : "User";
console.log(label);
// Console output:
// full access
// Administrator
```

```javascript
switch (role) {
  case "admin": console.log("manage"); break;
  case "user": console.log("read"); break;
  default: throw new Error("Unknown role");
}
// Console output: manage
```

## Loops

```javascript
for (const value of [10, 20, 30]) console.log(value);
// Console output:
// 10
// 20
// 30
```

- `for...of`: iterable values
- `for...in`: enumerable property keys; rarely correct for arrays
- `while`: repeat while condition remains true
- array methods: declarative transformations

## NaN

```javascript
const value = Number("not a number");
console.log(Number.isNaN(value));
console.log(value === value);
// Console output:
// true
// false
```

Use `Number.isNaN`, not global coercing `isNaN`, for precise checks.

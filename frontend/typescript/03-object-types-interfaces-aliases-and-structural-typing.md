# 03 - Object Types, Interfaces, Aliases, and Structural Typing

## Object Type

```typescript
type Course = {
  readonly id: string;
  title: string;
  description?: string;
};
const course: Course = { id: "html", title: "HTML" };
console.log(course.title);
// Console output: HTML
```

`readonly` prevents assignment through this type at compile time; it does not freeze the runtime object.

With `exactOptionalPropertyTypes`, missing `description` differs from explicitly assigning undefined unless undefined is included.

## Interface

```typescript
interface Priced {
  price: number;
}
interface Product extends Priced {
  name: string;
}
const product: Product = { name: "Course", price: 500 };
console.log(product.price);
// Console output: 500
```

Interfaces can merge declarations and are convenient for extensible object contracts. Type aliases can express unions, primitives, tuples, mapped/conditional types, and objects.

## Structural Typing

```typescript
interface Named { name: string }
const user = { name: "Asha", age: 25 };
const named: Named = user;
console.log(named.name);
// Console output: Asha
```

Compatibility is based on required shape, not declared class/interface name.

## Excess Property Check

Fresh object literals receive extra checking, but extra properties may still exist through another variable. Do not treat TypeScript object types as runtime exact schemas.

## Index Signatures and Records

```typescript
const scores: Record<string, number> = { Asha: 90, Ravi: 80 };
console.log(scores.Asha);
// Console output: 90
```

With `noUncheckedIndexedAccess`, unknown key reads may be undefined and must be handled.

## Tuples

```typescript
const entry: readonly [string, number] = ["Asha", 90];
console.log(entry[0], entry[1]);
// Console output: Asha 90
```

Use tuples for small fixed positional contracts. Prefer objects when field names improve clarity.

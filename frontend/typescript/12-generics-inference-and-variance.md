# 12 - Generics, Inference, and Variance

## Why Generics Exist

Generics preserve a relationship between types without copying the implementation.

```typescript
const first = <T>(values: readonly T[]): T | undefined => values[0];

const firstNumber = first([10, 20]); // number | undefined
const firstTitle = first(["HTML", "CSS"]); // string | undefined
console.log(firstNumber, firstTitle);
// Console output: 10 HTML
```

`T` means: “Choose one type for this call and use it consistently.”

## Generic vs `any`

```typescript
const unsafeFirst = (values: any[]): any => values[0];
const value = unsafeFirst([10, 20]);
value.notARealMethod(); // allowed by TypeScript, fails at runtime
```

The generic version preserves the element type. `any` discards it.

## Type Inference

Usually callers do not write the type argument:

```typescript
const result = first([true, false]); // T is inferred as boolean
console.log(result);
// Console output: true
```

Write an explicit type argument only when inference lacks information or a broader intended type must be stated:

```typescript
const empty = first<string>([]); // string | undefined
console.log(empty ?? "No title");
// Console output: No title
```

## Preserve Relationships

```typescript
const pair = <Left, Right>(left: Left, right: Right): readonly [Left, Right] => {
  return [left, right];
};

const course = pair("TypeScript", 14);
console.log(course[0], course[1]);
// Console output: TypeScript 14
```

The result keeps the exact relationship: first position is `Left`, second is `Right`.

## Generic Constraints

A constraint states the minimum capability needed:

```typescript
type HasLength = { readonly length: number };

const longer = <T extends HasLength>(left: T, right: T): T => {
  return left.length >= right.length ? left : right;
};

console.log(longer("TypeScript", "JS"));
// Console output: TypeScript
```

The function can read `.length`, but it preserves the caller's more specific type.

Do not constrain to a large domain type when the algorithm only needs one property.

## `keyof` Relationships

```typescript
const getProperty = <ObjectType, Key extends keyof ObjectType>(
  object: ObjectType,
  key: Key,
): ObjectType[Key] => object[key];

const course = { id: "ts", lessons: 14, published: true };
console.log(getProperty(course, "lessons"));
// Console output: 14
// getProperty(course, "missing") is a compile-time error.
```

`Key` must be a key of the actual object type, and the result matches that property's type.

## Generic Object Types

```typescript
type ApiResult<T> =
  | { ok: true; data: T }
  | { ok: false; error: string };

type Course = { id: string; title: string };
const result: ApiResult<Course> = {
  ok: true,
  data: { id: "ts", title: "TypeScript" },
};
console.log(result.ok ? result.data.title : result.error);
// Console output: TypeScript
```

The state model remains the same while the success data changes by use case.

## Generic Interfaces for Capabilities

```typescript
interface Repository<Entity, Id> {
  findById: (id: Id) => Promise<Entity | undefined>;
  save: (entity: Entity) => Promise<void>;
}
```

Do not create a generic repository automatically for every domain. Use it only when several implementations genuinely share the same useful contract.

## Generic Defaults

```typescript
type Page<T, Metadata = undefined> = {
  readonly items: readonly T[];
  readonly metadata: Metadata;
};

type SimplePage = Page<string>;
type CountedPage = Page<string, { total: number }>;
```

Defaults reduce noise when one type argument has a common meaning. Required parameters should come before defaulted ones.

## `const` Type Parameters

Modern TypeScript can preserve literal information for generic inputs:

```typescript
const defineRoutes = <const Routes extends readonly string[]>(routes: Routes): Routes => routes;
const routes = defineRoutes(["/", "/courses"]);
// type is readonly ["/", "/courses"]
console.log(routes[1]);
// Console output: /courses
```

Use this for configuration-building APIs where literal values matter. Avoid it when callers need ordinary mutable widened values.

## Generics vs Unions

Use a union when the function accepts several independent possibilities:

```typescript
const printId = (id: string | number): void => console.log(id);
```

Use a generic when input and output types must stay related:

```typescript
const identity = <T>(value: T): T => value;
```

A useless generic appears only once:

```typescript
// Unnecessary relationship:
const logValue = <T>(value: T): void => console.log(value);

// Simpler:
const logUnknown = (value: unknown): void => console.log(value);
```

## Variance: The Easy Mental Model

Variance asks whether a generic type relationship follows, reverses, or rejects the relationship between its type arguments.

Start with two types:

```typescript
type Animal = { name: string };
type Dog = Animal & { bark: () => void };
```

Every `Dog` is an `Animal`, but not every `Animal` is a `Dog`.

## Read-Only Producers Are Covariant

```typescript
const dogs: readonly Dog[] = [
  { name: "Milo", bark: () => console.log("woof") },
];
const animals: readonly Animal[] = dogs;
console.log(animals[0]?.name);
// Console output: Milo
```

Reading a Dog as an Animal is safe. No code can insert a plain Animal through the readonly reference.

## Consumers Are Contravariant Under Strict Function Checking

```typescript
type Handler<T> = (value: T) => void;

const handleAnimal: Handler<Animal> = (animal) => console.log(animal.name);
const handleDog: Handler<Dog> = handleAnimal;
handleDog({ name: "Milo", bark: () => console.log("woof") });
// Console output: Milo
```

A handler that accepts every Animal can safely handle a Dog. The reverse is unsafe because a dog-only handler might call `bark` on a plain Animal.

## Mutable Containers Need More Caution

If a type both reads and writes `T`, treating it as freely covariant can be unsafe.

Prefer readonly inputs at API boundaries:

```typescript
const printAnimals = (values: readonly Animal[]): void => {
  values.forEach((animal) => console.log(animal.name));
};
printAnimals(dogs);
// Console output: Milo
```

## Method Parameter Bivariance Caveat

TypeScript preserves some more-permissive method checking for compatibility. Function properties under `strictFunctionTypes` are usually safer for callback contracts:

```typescript
type Listener<T> = {
  onValue: (value: T) => void;
};
```

Do not rely on variance vocabulary alone. Test whether values flow into, out of, or both through the API.

## Inference Failure and API Design

If callers repeatedly need assertions or explicit type arguments, the API may not expose a clear inference relationship.

Improve it by:

- moving the value that determines `T` earlier
- separating unrelated type parameters
- using a discriminated union
- using overload call signatures for genuinely different calls
- returning a builder only when staged inference is actually required

## Expert Checklist

- every type parameter represents a real relationship
- constraints describe minimum required capability
- readonly inputs improve safe substitution
- callback parameter direction is reviewed under strict checking
- public generic order and defaults are stable API decisions
- recursive or conditional generic work is measured for compiler complexity

## Final Rule

Use generics to preserve information, not to make code look advanced. If removing the type parameter loses no useful relationship, remove it.

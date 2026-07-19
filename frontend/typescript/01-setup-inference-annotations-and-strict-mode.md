# 01 - TypeScript Setup, Inference, Annotations, and Strict Mode

## Install and Check

```powershell
npm install --save-dev typescript
npx tsc --init
npx tsc --noEmit
# Result: creates configuration, then type-checks without writing JavaScript files.
```

## Strict Configuration

```json
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true,
    "useUnknownInCatchVariables": true,
    "noEmit": true
  }
}
```

Result: TypeScript reports more possible null/undefined/index/error-shape mistakes before runtime.

## Type Inference

```typescript
const course = "TypeScript";
let completed = 0;
completed += 1;
console.log(course, completed);
// Console output: TypeScript 1
// Inferred types: course is "TypeScript"/string-compatible constant; completed is number.
```

Let TypeScript infer obvious local types. Add annotations at public boundaries, empty containers, complex returns, or where intent is otherwise unclear.

## Annotations

```typescript
const total = (price: number, quantity: number): number => {
  return price * quantity;
};
console.log(total(250, 2));
// Console output: 500
// total("250", 2) fails type checking.
```

## Type Erasure

```typescript
const count: number = 3;
console.log(count);
// Emitted JavaScript behaves like: const count = 3;
// Console output: 3
```

## Avoid `any`

`any` disables useful checking and spreads through code. Use `unknown` for values whose type is not yet proven, then narrow it.

## Nullability

```typescript
const length = (value: string | null): number => {
  return value === null ? 0 : value.length;
};
console.log(length(null), length("Java"));
// Console output: 0 4
```

Do not use non-null assertions (`!`) merely to silence a real uncertainty.

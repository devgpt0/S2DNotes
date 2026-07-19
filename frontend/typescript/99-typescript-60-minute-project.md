# TypeScript 60-Minute Project - Typed Expense Tracker

## Goal

Build a small expense tracker using strict TypeScript, discriminated UI state, runtime storage validation, typed DOM events, immutable updates, generics/utility types, and tests.

## Time Box

- 0-8 min: Vite TS setup and strict config
- 8-20 min: domain types and validator
- 20-35 min: state functions and rendering
- 35-47 min: form/events/storage
- 47-55 min: filters/summary
- 55-60 min: tests and type audit

## Step 1: Types

```typescript
type Category = "food" | "travel" | "learning";
type Expense = Readonly<{ id: string; description: string; amountMinor: number; category: Category }>;
type AppState =
  | { status: "ready"; expenses: readonly Expense[] }
  | { status: "error"; message: string };
console.log(({ status: "ready", expenses: [] } satisfies AppState).status);
// Console output: ready
```

Store money as integer minor units.

## Step 2: Runtime Validator

```typescript
function isExpense(value: unknown): value is Expense {
  if (typeof value !== "object" || value === null) return false;
  const item = value as Record<string, unknown>;
  return typeof item.id === "string"
    && typeof item.description === "string"
    && Number.isSafeInteger(item.amountMinor)
    && (item.amountMinor as number) > 0
    && ["food", "travel", "learning"].includes(item.category as string);
}
console.log(isExpense({ id: "1", description: "Book", amountMinor: 50000, category: "learning" }));
// Console output: true
```

The narrow assertions are local to a validator that checks every property before trusted use.

## Step 3: Pure Updates

```typescript
function addExpense(expenses: readonly Expense[], expense: Expense): readonly Expense[] {
  return [...expenses, expense];
}
function total(expenses: readonly Expense[]): number {
  return expenses.reduce((sum, expense) => sum + expense.amountMinor, 0);
}
const expenses = addExpense([], { id: "1", description: "Book", amountMinor: 50000, category: "learning" });
console.log(total(expenses));
// Console output: 50000
```

## Step 4: Typed Form

```typescript
const form = document.querySelector<HTMLFormElement>("#expense-form");
if (!form) throw new Error("expense form is required");
form.addEventListener("submit", event => {
  event.preventDefault();
  const data = new FormData(form);
  const description = data.get("description");
  const amount = data.get("amount");
  if (typeof description !== "string" || typeof amount !== "string") throw new TypeError("invalid form fields");
  const amountMinor = Math.round(Number(amount) * 100);
  if (!Number.isSafeInteger(amountMinor) || amountMinor <= 0) throw new RangeError("invalid amount");
  console.log(description, amountMinor);
});
// Console output on valid submit: description and integer minor-unit amount.
```

## Step 5: Safe Storage

Parse localStorage to `unknown`, verify it is an array and every item satisfies `isExpense`; otherwise show an error rather than silently accepting/coercing corrupted data.

## Step 6: Test

```typescript
import { expect, test } from "vitest";
test("totals minor units", () => {
  const value: Expense = { id: "1", description: "Book", amountMinor: 50000, category: "learning" };
  expect(total([value])).toBe(50000);
});
// Test output: passes with exact integer total.
```

## Interview Review

Explain inference vs annotation, union narrowing, readonly ownership, type guard, unknown vs any, compile-time erasure, runtime validation, `satisfies`, safe money modeling, typed DOM nullable queries, and why assertions do not validate.

## Completion Definition

Strict check passes, no `any`, storage is validated, impossible UI states excluded, money uses safe integers, DOM nulls handled, updates immutable, and tests cover validator/total.

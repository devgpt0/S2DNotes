# 99 - Build a Strict Expense Tracker in 60 Minutes

## Project Overview

Build a browser expense tracker with strict TypeScript. Users add an expense, filter by category, see an exact total, and reload validated data from local storage.

The project treats DOM input and stored JSON as untrusted runtime data. TypeScript describes trusted application values; explicit validation is what allows external values to enter that trusted model.

## What You Will Learn

- strict compiler configuration and modern ES modules
- literal unions, readonly domain types, and exhaustive checks
- runtime validation and `unknown` narrowing without `any`
- exact money storage in integer minor units
- typed DOM dependencies and events
- immutable updates and derived totals
- focused tests for validation and domain calculations

## Time Plan

| Minutes | Work |
|---:|---|
| 0-10 | Create the Vite and strict TypeScript files |
| 10-24 | Define the domain model and runtime validator |
| 24-34 | Implement pure updates and tests |
| 34-52 | Build typed DOM behavior and storage |
| 52-60 | Run checks and test invalid boundary values |

## Folder Structure

```text
typescript-expense-tracker/
|-- index.html
|-- package.json
|-- styles.css
|-- tsconfig.json
|-- src/
|   |-- domain.ts
|   `-- main.ts
`-- tests/
    `-- domain.test.ts
```

Generated dependencies, lockfiles, and `dist` output are intentionally omitted from the hand-written tree.

## File: `package.json`

```json
{
  "name": "typescript-expense-tracker",
  "private": true,
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc --noEmit && vite build",
    "test": "vitest run"
  },
  "devDependencies": {
    "typescript": "^5.8.0",
    "vite": "^7.0.0",
    "vitest": "^3.2.0"
  }
}
```

Concepts learned from this file:

- the build first performs a strict type check, then creates production assets.
- development dependencies are tools, not code shipped as direct application dependencies.
- `private` protects the learning project from accidental package publication.

## File: `tsconfig.json`

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "useDefineForClassFields": true,
    "module": "ESNext",
    "moduleResolution": "Bundler",
    "lib": ["ES2022", "DOM", "DOM.Iterable"],
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true,
    "noImplicitOverride": true,
    "noFallthroughCasesInSwitch": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "isolatedModules": true,
    "verbatimModuleSyntax": true,
    "noEmit": true
  },
  "include": ["src", "tests"]
}
```

Concepts learned from this file:

- `strict` enables the core soundness checks rather than hiding null and inference mistakes.
- unchecked indexes and optional properties receive precise treatment.
- bundler module resolution matches Vite while `noEmit` leaves emission to the bundler.
- unused and fallthrough checks keep the small codebase intentional.

## File: `index.html`

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="A strict TypeScript expense tracker.">
    <title>Expense Tracker</title>
    <link rel="stylesheet" href="/styles.css">
  </head>
  <body>
    <main class="shell">
      <header>
        <p class="eyebrow">Strict TypeScript project</p>
        <h1>Expense tracker</h1>
        <p>Amounts are stored as integer paise to keep totals exact.</p>
      </header>

      <form id="expense-form" class="expense-form">
        <div>
          <label for="description">Description</label>
          <input id="description" name="description" required maxlength="80">
        </div>
        <div>
          <label for="amount">Amount in rupees</label>
          <input id="amount" name="amount" inputmode="decimal" placeholder="499.00" required>
        </div>
        <div>
          <label for="category">Category</label>
          <select id="category" name="category" required>
            <option value="">Choose one</option>
            <option value="food">Food</option>
            <option value="travel">Travel</option>
            <option value="learning">Learning</option>
          </select>
        </div>
        <button type="submit">Add expense</button>
      </form>

      <section aria-labelledby="expenses-heading">
        <div class="toolbar">
          <h2 id="expenses-heading">Expenses</h2>
          <label for="filter">Filter</label>
          <select id="filter">
            <option value="all">All categories</option>
            <option value="food">Food</option>
            <option value="travel">Travel</option>
            <option value="learning">Learning</option>
          </select>
        </div>
        <p id="status" role="status"></p>
        <p id="error" role="alert" hidden></p>
        <ul id="expense-list" class="expense-list"></ul>
        <p class="total">Total: <output id="total">₹0.00</output></p>
      </section>
    </main>
    <script type="module" src="/src/main.ts"></script>
  </body>
</html>
```

Concepts learned from this file:

- the input remains text because the application enforces an exact decimal grammar.
- `output` represents a calculated result.
- status and error messages have separate announcement urgency.
- the DOM provides raw strings; TypeScript cannot make those values valid automatically.

## File: `styles.css`

```css
*, *::before, *::after { box-sizing: border-box; }
:root { color-scheme: light dark; font-family: ui-sans-serif, system-ui, sans-serif; line-height: 1.5; --brand: #5b45d6; --border: color-mix(in srgb, currentColor 22%, transparent); }
body { margin: 0; min-block-size: 100dvh; }
button, input, select { min-block-size: 2.75rem; font: inherit; }
input, select { inline-size: 100%; padding-inline: 0.7rem; }
button { padding-inline: 1rem; cursor: pointer; }
:focus-visible { outline: 0.2rem solid var(--brand); outline-offset: 0.2rem; }
.shell { inline-size: min(100% - 2rem, 60rem); margin-inline: auto; padding-block: 3rem; }
.shell > * + * { margin-block-start: 2.5rem; }
.eyebrow { color: var(--brand); font-weight: 800; text-transform: uppercase; }
.expense-form { display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 12rem), 1fr)); align-items: end; gap: 1rem; }
.expense-form label { display: block; margin-block-end: 0.25rem; }
.toolbar { display: flex; flex-wrap: wrap; align-items: center; gap: 0.75rem; }
.toolbar h2 { margin-inline-end: auto; }
.toolbar select { inline-size: auto; max-inline-size: 100%; }
.expense-list { display: grid; gap: 0.75rem; padding: 0; list-style: none; }
.expense-list li { display: grid; grid-template-columns: minmax(0, 1fr) auto; gap: 0.5rem 1rem; padding: 1rem; border: 1px solid var(--border); border-radius: 0.75rem; }
.expense-list small { text-transform: capitalize; }
.total { font-size: 1.25rem; font-weight: 800; text-align: end; }
```

Concepts learned from this file:

- auto-fit Grid adapts the form without device-specific breakpoint names.
- `min(100%, 12rem)` prevents a minimum track from overflowing a narrow viewport.
- logical properties support different writing directions.
- the list keeps descriptions flexible while the amount column remains content-sized.

## File: `src/domain.ts`

```typescript
export const CATEGORIES = ["food", "travel", "learning"] as const;
export type Category = (typeof CATEGORIES)[number];
export type CategoryFilter = Category | "all";

export type Expense = Readonly<{
  id: string;
  description: string;
  amountMinor: number;
  category: Category;
}>;

export const isCategory = (value: unknown): value is Category => {
  return typeof value === "string"
    && CATEGORIES.some((category) => category === value);
};

export const isExpense = (value: unknown): value is Expense => {
  return typeof value === "object"
    && value !== null
    && "id" in value
    && typeof value.id === "string"
    && value.id.length > 0
    && "description" in value
    && typeof value.description === "string"
    && value.description.length > 0
    && "amountMinor" in value
    && typeof value.amountMinor === "number"
    && Number.isSafeInteger(value.amountMinor)
    && value.amountMinor > 0
    && "category" in value
    && isCategory(value.category);
};

export const parseExpenses = (serialized: string): readonly Expense[] => {
  const value: unknown = JSON.parse(serialized);
  if (!Array.isArray(value) || !value.every(isExpense)) {
    throw new TypeError("stored expenses do not match the expense schema");
  }
  return value;
};

export const parseAmountMinor = (value: string): number => {
  if (!/^(?:0|[1-9]\d*)(?:\.\d{1,2})?$/.test(value)) {
    throw new TypeError("amount must be a positive decimal with at most two places");
  }

  const [rupees, paise = ""] = value.split(".");
  const amountMinor = Number(rupees) * 100 + Number(paise.padEnd(2, "0"));
  if (!Number.isSafeInteger(amountMinor) || amountMinor <= 0) {
    throw new RangeError("amount is outside the supported range");
  }
  return amountMinor;
};

export const addExpense = (
  expenses: readonly Expense[],
  expense: Expense,
): readonly Expense[] => {
  if (!isExpense(expense)) throw new TypeError("expense is invalid");
  return [...expenses, expense];
};

export const filterExpenses = (
  expenses: readonly Expense[],
  filter: CategoryFilter,
): readonly Expense[] => {
  return filter === "all"
    ? expenses
    : expenses.filter((expense) => expense.category === filter);
};

export const totalMinor = (expenses: readonly Expense[]): number => {
  const total = expenses.reduce((sum, expense) => sum + expense.amountMinor, 0);
  if (!Number.isSafeInteger(total)) throw new RangeError("expense total is unsafe");
  return total;
};
```

Concepts learned from this file:

- `as const` derives a literal union from one canonical category list.
- validators narrow `unknown` only after checking every required property.
- amount parsing validates a decimal grammar before explicit conversion; it does not accept partial or coerced values.
- readonly inputs plus new arrays make ownership and mutation rules clear.
- money remains exact because calculations use integer minor units.

## File: `src/main.ts`

```typescript
import {
  addExpense,
  filterExpenses,
  isCategory,
  isExpense,
  parseAmountMinor,
  parseExpenses,
  totalMinor,
  type CategoryFilter,
  type Expense,
} from "./domain";

const STORAGE_KEY = "typescript-expense-tracker.expenses";
const money = new Intl.NumberFormat("en-IN", {
  style: "currency",
  currency: "INR",
});

const requiredElement = <T extends Element>(selector: string, type: new () => T): T => {
  const element = document.querySelector(selector);
  if (!(element instanceof type)) throw new Error(`missing required element: ${selector}`);
  return element;
};

const form = requiredElement("#expense-form", HTMLFormElement);
const descriptionInput = requiredElement("#description", HTMLInputElement);
const amountInput = requiredElement("#amount", HTMLInputElement);
const categoryInput = requiredElement("#category", HTMLSelectElement);
const filterInput = requiredElement("#filter", HTMLSelectElement);
const list = requiredElement("#expense-list", HTMLUListElement);
const status = requiredElement("#status", HTMLParagraphElement);
const error = requiredElement("#error", HTMLParagraphElement);
const total = requiredElement("#total", HTMLOutputElement);

let expenses: readonly Expense[];
let filter: CategoryFilter = "all";

const loadExpenses = (): readonly Expense[] => {
  const serialized = localStorage.getItem(STORAGE_KEY);
  return serialized === null ? [] : parseExpenses(serialized);
};

const expenseElement = (expense: Expense): HTMLLIElement => {
  const item = document.createElement("li");
  const details = document.createElement("span");
  const description = document.createElement("strong");
  const category = document.createElement("small");
  const amount = document.createElement("span");

  description.textContent = expense.description;
  category.textContent = expense.category;
  amount.textContent = money.format(expense.amountMinor / 100);
  details.append(description, document.createElement("br"), category);
  item.append(details, amount);
  return item;
};

const render = (): void => {
  const visible = filterExpenses(expenses, filter);
  list.replaceChildren(...visible.map(expenseElement));
  status.textContent = `${visible.length} of ${expenses.length} expenses shown`;
  total.value = money.format(totalMinor(visible) / 100);
};

const start = (): void => {
  expenses = loadExpenses();
  render();

  form.addEventListener("submit", (event) => {
    event.preventDefault();
    if (!form.reportValidity()) return;

    const category: unknown = categoryInput.value;
    if (!isCategory(category)) throw new TypeError("category is invalid");

    const expense: Expense = {
      id: crypto.randomUUID(),
      description: descriptionInput.value.trim(),
      amountMinor: parseAmountMinor(amountInput.value),
      category,
    };
    if (!isExpense(expense)) throw new TypeError("expense fields are invalid");

    const nextExpenses = addExpense(expenses, expense);
    localStorage.setItem(STORAGE_KEY, JSON.stringify(nextExpenses));
    expenses = nextExpenses;
    form.reset();
    descriptionInput.focus();
    render();
  });

  filterInput.addEventListener("change", () => {
    const value: unknown = filterInput.value;
    if (value !== "all" && !isCategory(value)) throw new TypeError("filter is invalid");
    filter = value;
    render();
  });
};

try {
  start();
} catch (caught: unknown) {
  error.hidden = false;
  error.textContent = caught instanceof Error
    ? `Expense tracker could not start: ${caught.message}`
    : "Expense tracker could not start.";
  form.inert = true;
  filterInput.disabled = true;
}
```

Concepts learned from this file:

- a generic dependency function centralizes one repeated DOM invariant.
- type-only imports disappear from runtime output.
- `Intl.NumberFormat` owns display formatting while domain code owns integer calculations.
- values enter the trusted model only after runtime checks.
- persistence happens before in-memory commit, preventing state divergence on storage failure.

## File: `tests/domain.test.ts`

```typescript
import { describe, expect, test } from "vitest";
import {
  addExpense,
  parseAmountMinor,
  parseExpenses,
  totalMinor,
  type Expense,
} from "../src/domain";

const book: Expense = {
  id: "expense-1",
  description: "TypeScript book",
  amountMinor: 49900,
  category: "learning",
};

describe("expense domain", () => {
  test("parses exact minor units", () => {
    expect(parseAmountMinor("499")).toBe(49900);
    expect(parseAmountMinor("499.5")).toBe(49950);
    expect(() => parseAmountMinor("499.999")).toThrow(TypeError);
  });

  test("rejects invalid stored data without coercion", () => {
    expect(() => parseExpenses('[{"amountMinor":"49900"}]')).toThrow(TypeError);
  });

  test("adds immutably and totals safely", () => {
    const before: readonly Expense[] = [];
    const after = addExpense(before, book);

    expect(before).toEqual([]);
    expect(totalMinor(after)).toBe(49900);
  });
});
```

Concepts learned from this file:

- tests cover valid values, boundary syntax, wrong runtime types, and immutability.
- a numeric-looking string is rejected instead of converted into a number.
- domain tests run without DOM rendering or browser event setup.

## Run the Project

```powershell
npm install
npm run test
npm run build
npm run dev
# Test result: 3 tests pass.
# Build result: TypeScript check and Vite production build succeed.
```

## Expected Behavior

1. Valid descriptions, amounts, and categories create expenses.
2. `499`, `499.5`, and `499.50` are accepted; partial, negative, exponent, and three-decimal values are rejected.
3. Category filtering recalculates the visible list and total.
4. Reload restores only schema-valid stored expenses.
5. Corrupted stored data produces a visible fatal error and disables interaction.

## Verification Checklist

- run the strict build with no `any`, suppressions, or unchecked boundary assertions
- inspect local storage and change `amountMinor` from a number to a string
- test very large amounts and confirm unsafe integers fail
- test keyboard use, 320px width, 200% zoom, and long descriptions
- use the Coverage panel to identify code paths not exercised by tests

## Interview Review

### Why does `Expense` not validate JSON by itself?

TypeScript types are erased during compilation. Runtime data remains `unknown` until executable checks establish the contract.

### Why store money as integer minor units?

Binary floating-point cannot exactly represent many decimal fractions. Integer paise makes addition deterministic while formatting remains a presentation concern.

### Why use a literal union for categories?

It creates a finite domain that supports autocomplete and exhaustive reasoning while the validator enforces the same set at runtime.

### Why is a type assertion not validation?

An assertion changes what the compiler believes. It performs no runtime inspection and cannot make invalid data valid.

## Completion Definition

The project is complete when strict type-checking, tests, and production build pass; invalid external values fail explicitly; totals remain exact; responsive and keyboard flows work; and every file's concept section can be explained from memory.

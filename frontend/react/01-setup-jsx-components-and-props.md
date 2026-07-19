# 01 - React Setup, JSX, Components, and Props

## Create a TypeScript Project

```powershell
npm create vite@latest course-app -- --template react-ts
cd course-app
npm install
npm run dev
# Result: Vite starts a React TypeScript development server and prints its local URL.
```

## Root Render

```tsx
import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { App } from "./App";

createRoot(document.getElementById("root")!).render(<StrictMode><App /></StrictMode>);
// Browser result: App renders inside #root; development StrictMode helps reveal unsafe logic/effect cleanup.
```

Validate the root instead of asserting in production code if the HTML shell can vary.

## JSX Rules

- return one parent/root expression
- close every element
- use `className`, `htmlFor`, camelCase DOM properties/events
- JavaScript expressions go inside braces
- component names begin uppercase
- values are escaped when rendered as text

```tsx
function CourseCard() {
  const title = "HTML Basics";
  return <article className="card"><h2>{title}</h2><p>{2 + 3} lessons</p></article>;
}
// Browser result: card showing "HTML Basics" and "5 lessons".
```

## Props

Props are read-only inputs.

```tsx
type CourseCardProps = {
  title: string;
  price: number;
  featured?: boolean;
};

function CourseCard({ title, price, featured = false }: CourseCardProps) {
  return <article><h2>{title}</h2><p>₹{price}</p>{featured && <strong>Featured</strong>}</article>;
}
// Browser result for title="React", price=999, featured: title, ₹999, and Featured label.
```

Never modify a prop. Ask the parent to provide new data through an event callback.

## Component Purity

During render, components should calculate JSX from props/state/context without changing outside state, making network requests, setting state, or manipulating the DOM.

## Children Composition

```tsx
type PanelProps = { title: string; children: ReactNode };
function Panel({ title, children }: PanelProps) {
  return <section aria-labelledby={`${title}-heading`}><h2 id={`${title}-heading`}>{title}</h2>{children}</section>;
}
// Browser result: reusable titled section containing caller-provided children.
```

Prefer composition over giant components with dozens of configuration flags.

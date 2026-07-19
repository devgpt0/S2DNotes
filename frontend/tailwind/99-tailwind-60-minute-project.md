# 99 - Build a Responsive Pricing Page in 60 Minutes

## Project Overview

Build a semantic pricing and signup page with Tailwind CSS 4. The page uses CSS-first theme tokens, an intrinsic responsive grid, dark mode, accessible states, and a small production build.

## What You Will Learn

- Tailwind 4 Vite setup and source detection
- CSS-first theme tokens
- mobile-first utilities and intrinsic Grid
- responsive, dark, focus, invalid, and motion variants
- semantic HTML beneath utility classes
- production CSS inspection and dynamic-class pitfalls

## Folder Structure

```text
tailwind-pricing-page/
|-- index.html
|-- package.json
|-- vite.config.js
`-- src/
    |-- input.css
    `-- main.js
```

Vite output, installed packages, and the lockfile are generated.

## File: `package.json`

```json
{
  "name": "tailwind-pricing-page",
  "private": true,
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "devDependencies": {
    "@tailwindcss/vite": "^4.1.0",
    "tailwindcss": "^4.1.0",
    "vite": "^7.0.0"
  }
}
```

Concepts learned from this file:

- Tailwind's Vite plugin participates in development and production builds.
- no JavaScript Tailwind configuration is required for this CSS-first project.
- the preview command checks the actual production output.

## File: `vite.config.js`

```javascript
import tailwindcss from "@tailwindcss/vite";
import { defineConfig } from "vite";

export default defineConfig({
  plugins: [tailwindcss()],
});
```

Concepts learned from this file:

- the Tailwind plugin transforms the CSS import during Vite builds.
- the configuration contains only a demonstrated requirement; theme values remain in CSS.

## File: `src/input.css`

```css
@import "tailwindcss";

@theme {
  --color-brand-500: oklch(58% 0.2 260);
  --color-brand-700: oklch(45% 0.2 260);
  --font-sans: Inter, ui-sans-serif, system-ui, sans-serif;
}

@layer base {
  :focus-visible {
    outline: 0.2rem solid var(--color-brand-500);
    outline-offset: 0.2rem;
  }
}
```

Concepts learned from this file:

- `@import "tailwindcss"` loads Tailwind's layers.
- `@theme` creates both design tokens and matching utilities such as `bg-brand-700`.
- a base focus rule provides a dependable fallback even when a component forgets a focus utility.

## File: `src/main.js`

```javascript
import "./input.css";

const form = document.querySelector("#signup");
const status = document.querySelector("#status");

if (!(form instanceof HTMLFormElement)
  || !(status instanceof HTMLParagraphElement)) {
  throw new Error("required signup elements are missing");
}

form.addEventListener("submit", (event) => {
  event.preventDefault();
  if (!form.reportValidity()) return;
  status.textContent = "Your learning account is ready.";
  form.reset();
});
```

Concepts learned from this file:

- JavaScript imports the CSS entry so Vite processes it.
- required DOM dependencies are checked before listeners are attached.
- native validation remains the first validation layer.
- Tailwind styles the behavior but does not replace JavaScript or semantic HTML.

## File: `index.html`

```html
<!doctype html>
<html lang="en" class="scheme-light dark:scheme-dark">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="Compare frontend learning plans.">
    <title>Learning Plans</title>
  </head>
  <body class="min-h-dvh bg-slate-50 font-sans text-slate-950 dark:bg-slate-950 dark:text-slate-50">
    <main class="mx-auto w-full max-w-6xl px-4 py-12 sm:px-6 lg:px-8">
      <header class="mx-auto max-w-2xl text-center">
        <p class="font-bold uppercase tracking-wider text-brand-700 dark:text-brand-500">Frontend learning</p>
        <h1 class="mt-3 text-balance text-4xl font-bold tracking-tight sm:text-5xl">Choose your learning plan</h1>
        <p class="mt-4 text-pretty text-slate-600 dark:text-slate-300">Start free, then add feedback when guided projects become useful.</p>
      </header>

      <section aria-label="Pricing plans" class="mt-10 grid grid-cols-[repeat(auto-fit,minmax(min(100%,17rem),1fr))] gap-5">
        <article class="flex flex-col rounded-2xl border border-slate-200 bg-white p-6 shadow-sm dark:border-slate-700 dark:bg-slate-900">
          <h2 class="text-xl font-semibold">Starter</h2>
          <p class="mt-2 text-3xl font-bold">₹0</p>
          <p class="mt-2 text-slate-600 dark:text-slate-300">Build the foundation at your pace.</p>
          <ul class="my-6 space-y-2" role="list">
            <li>Core notes</li>
            <li>Practice checkpoints</li>
          </ul>
          <a class="mt-auto min-h-11 rounded-lg bg-brand-700 px-4 py-3 text-center font-semibold text-white hover:bg-brand-500" href="#signup">Start learning</a>
        </article>

        <article class="flex flex-col rounded-2xl border-2 border-brand-500 bg-white p-6 shadow-sm dark:bg-slate-900">
          <p class="w-fit rounded-full bg-brand-700 px-3 py-1 text-sm font-bold text-white">Most popular</p>
          <h2 class="mt-4 text-xl font-semibold">Guided</h2>
          <p class="mt-2 text-3xl font-bold">₹999</p>
          <p class="mt-2 text-slate-600 dark:text-slate-300">Add reviews and project feedback.</p>
          <ul class="my-6 space-y-2" role="list">
            <li>Everything in Starter</li>
            <li>Weekly code review</li>
          </ul>
          <a class="mt-auto min-h-11 rounded-lg bg-brand-700 px-4 py-3 text-center font-semibold text-white hover:bg-brand-500" href="#signup">Choose Guided</a>
        </article>

        <article class="flex flex-col rounded-2xl border border-slate-200 bg-white p-6 shadow-sm dark:border-slate-700 dark:bg-slate-900">
          <h2 class="text-xl font-semibold">Team</h2>
          <p class="mt-2 text-3xl font-bold">Custom</p>
          <p class="mt-2 text-slate-600 dark:text-slate-300">Create a shared learning path.</p>
          <ul class="my-6 space-y-2" role="list">
            <li>Progress dashboard</li>
            <li>Team workshops</li>
          </ul>
          <a class="mt-auto min-h-11 rounded-lg border border-slate-400 px-4 py-3 text-center font-semibold hover:bg-slate-100 dark:hover:bg-slate-800" href="mailto:team@example.com">Contact us</a>
        </article>
      </section>

      <section class="mx-auto mt-16 max-w-xl" aria-labelledby="signup-heading">
        <h2 id="signup-heading" class="text-2xl font-bold">Create a Starter account</h2>
        <form id="signup" class="mt-5 space-y-4 rounded-xl border border-slate-300 bg-white p-6 dark:border-slate-700 dark:bg-slate-900">
          <div>
            <label class="block font-medium" for="email">Email address</label>
            <input class="mt-1 min-h-11 w-full rounded-md border border-slate-400 bg-transparent px-3 invalid:not-placeholder-shown:border-red-600" id="email" name="email" type="email" autocomplete="email" placeholder="you@example.com" required>
          </div>
          <label class="flex items-start gap-2">
            <input class="mt-1 size-4 accent-brand-700" type="checkbox" required>
            <span>I accept the learning terms.</span>
          </label>
          <button class="min-h-11 w-full rounded-md bg-brand-700 px-4 font-semibold text-white hover:bg-brand-500 motion-safe:transition-colors disabled:cursor-not-allowed disabled:opacity-50" type="submit">Create account</button>
          <p id="status" class="text-sm font-medium" role="status"></p>
        </form>
      </section>
    </main>
    <script type="module" src="/src/main.js"></script>
  </body>
</html>
```

Concepts learned from this file:

- semantic elements and native controls provide meaning before utilities are applied.
- the arbitrary grid value creates responsive columns from available space, not device names.
- `min(100%, 17rem)` prevents the minimum card width from causing overflow.
- complete static class names are discoverable during the production build.
- dark, hover, invalid, and motion-safe variants express real UI states.

## Run and Verify

```powershell
npm install
npm run dev
npm run build
npm run preview
# Result: Vite prints local URLs and creates a production dist folder.
```

Test 320px to wide screens, 200% zoom, keyboard focus, dark mode, reduced motion, long translated text, invalid email behavior, and the generated CSS size. Search the production CSS for one used and one unused utility to understand source detection.

## Avoid This Dynamic-Class Bug

```javascript
// Avoid: `bg-${color}-700` may not be found as a complete class.
const styles = {
  primary: "bg-brand-700 text-white",
  secondary: "border border-slate-400",
};
```

Map finite variants to complete class strings.

## Completion Definition

Every listed file exists, the production build succeeds, all classes are statically discoverable, the page has no narrow-screen overflow, keyboard and dark-mode states work, and every file's concept section is understood.

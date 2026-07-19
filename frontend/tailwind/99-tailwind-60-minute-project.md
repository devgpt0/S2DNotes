# Tailwind 60-Minute Project - Responsive Pricing and Signup Page

## Goal

Build a semantic pricing page using Tailwind 4 theme tokens, mobile-first Grid, states, dark mode, container queries, accessible signup form, and production-output inspection.

## Time Box

- 0-8 min: Vite/Tailwind setup and theme
- 8-18 min: header and hero
- 18-35 min: pricing cards
- 35-48 min: signup form and interaction states
- 48-55 min: dark/reduced motion/responsive audit
- 55-60 min: production build inspection

## Step 1: Theme

```css
@import "tailwindcss";
@theme {
  --color-brand-500: oklch(58% .2 260);
  --color-brand-700: oklch(45% .2 260);
  --font-sans: Inter, ui-sans-serif, system-ui, sans-serif;
}
/* Result: brand color and font utilities become available. */
```

## Step 2: Shell and Hero

```html
<main class="mx-auto w-full max-w-6xl px-4 py-10 sm:px-6 lg:px-8">
  <header class="mx-auto max-w-2xl text-center">
    <h1 class="text-balance text-4xl font-bold tracking-tight sm:text-5xl">Choose your learning plan</h1>
    <p class="mt-4 text-pretty text-slate-600 dark:text-slate-300">Start free and upgrade when you need guided projects.</p>
  </header>
</main>
<!-- Browser result: centered responsive hero with readable wrapping. -->
```

## Step 3: Pricing Grid

```html
<section aria-label="Pricing plans" class="mt-10 grid grid-cols-[repeat(auto-fit,minmax(min(100%,17rem),1fr))] gap-5">
  <article class="flex flex-col rounded-2xl border border-slate-200 bg-white p-6 shadow-sm dark:border-slate-700 dark:bg-slate-900">
    <h2 class="text-xl font-semibold">Starter</h2><p class="mt-2 text-3xl font-bold">₹0</p>
    <ul class="my-6 space-y-2"><li>✓ Core notes</li><li>✓ Practice tasks</li></ul>
    <a class="mt-auto rounded-lg bg-brand-700 px-4 py-3 text-center font-semibold text-white hover:bg-brand-500 focus-visible:outline-2 focus-visible:outline-offset-2" href="#signup">Start learning</a>
  </article>
</section>
<!-- Browser result: intrinsic responsive pricing grid and equal-height action placement. -->
```

Duplicate the article for Pro and Team, mapping variants to complete class strings if using JSX.

## Step 4: Signup Form

```html
<form id="signup" class="mx-auto mt-12 max-w-xl space-y-4 rounded-xl border p-6">
  <div><label class="block font-medium" for="email">Email</label><input class="mt-1 w-full rounded border px-3 py-2 invalid:border-red-600 focus-visible:outline-2" id="email" name="email" type="email" required></div>
  <label class="flex gap-2"><input type="checkbox" required> <span>I accept the terms</span></label>
  <button class="min-h-11 w-full rounded bg-brand-700 px-4 text-white disabled:opacity-50" type="submit">Create account</button>
</form>
<!-- Browser result: responsive labelled form with native validation and visible states. -->
```

## Step 5: Expert Audit

Test 320px/200% zoom, long plan names, keyboard focus, dark/reduced-motion/forced-colors, and production generated CSS. Confirm no dynamic class fragments or huge safelist.

## Interview Review

Explain utility-first, source detection, CSS-first theme, mobile variants, container variants, arbitrary values, class conflict order, `@apply` tradeoffs, accessibility, and why Tailwind does not replace CSS knowledge.

## Completion Definition

Semantic controls, no narrow-screen overflow, token-based colors, visible focus, accessible form, dark mode, static class detection, and recorded production CSS size.

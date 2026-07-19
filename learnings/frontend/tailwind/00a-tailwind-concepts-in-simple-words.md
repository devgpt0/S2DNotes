# Tailwind CSS Concepts in Simple Words

## The One-Sentence Idea

Tailwind scans source files for utility class names and generates normal CSS for those classes.

```text
HTML/JSX class tokens -> Tailwind build -> CSS utilities -> browser
# Result: the browser sees CSS; Tailwind does not run as a layout engine in the page.
```

## Read a Utility

```html
<button class="rounded-md bg-blue-700 px-4 py-2 text-white hover:bg-blue-600 md:px-6">
  Save
</button>
<!-- Browser result: styled button; wider padding from the md breakpoint upward. -->
```

- property/value utility: `bg-blue-700`
- spacing scale: `px-4`
- state variant: `hover:`
- responsive variant: `md:`
- theme token: `blue-700`

## What Tailwind Does Not Replace

You still need HTML semantics, cascade, box model, Flexbox, Grid, responsive design, accessibility, browser compatibility, and performance knowledge.

## Component Rule

Extract repeated **markup and behavior** into a React/component function. Do not automatically replace every repeated class list with `@apply`.

## Detection Rule

Class names must normally appear as complete tokens in scanned source. Map variants to complete strings instead of assembling fragments.

```typescript
const variants = { success: "bg-green-600", danger: "bg-red-700" } as const;
console.log(variants.success);
// Console output: bg-green-600
```

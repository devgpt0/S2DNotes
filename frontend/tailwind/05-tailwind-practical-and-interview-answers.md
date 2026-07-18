# 05 - Tailwind Practical Activities and Interview Answers

## Activity: Responsive Course Landing Page

Build header, hero, responsive course grid, pricing section, form, and footer.

Requirements:

- semantic HTML before utilities
- mobile-first layout
- keyboard focus and error states
- dark mode
- reduced motion
- theme tokens for brand colors
- no dynamically assembled class fragments
- inspect production CSS output

### Example Card

```html
<article class="overflow-hidden rounded-xl border border-slate-200 bg-white shadow-sm dark:border-slate-700 dark:bg-slate-900">
  <img class="aspect-video w-full object-cover" src="course.jpg" width="640" height="360" alt="Student coding">
  <div class="space-y-3 p-4"><h2 class="text-xl font-semibold">HTML Course</h2><button class="rounded bg-blue-700 px-4 py-2 text-white focus-visible:outline-2">Enroll</button></div>
</article>
<!-- Browser result: responsive theme-aware course card with visible focus and stable image ratio. -->
```

## Interview Questions with Answers

### 1. What is utility-first CSS?

Compose small single-purpose classes directly in markup instead of writing a new custom selector for every component style.

### 2. Why learn CSS before Tailwind?

Tailwind utilities map to CSS. Debugging cascade, layout, responsiveness, browser compatibility, and performance still requires CSS knowledge.

### 3. How does responsive styling work?

Unprefixed classes are the base. Prefixes such as `md:` wrap utilities in configured min-width media queries. Container variants respond to container size.

### 4. Why can dynamic class fragments fail?

Tailwind detects complete tokens in source text. A runtime string such as `bg-${color}-500` may not exist during source scanning, so no CSS is generated.

### 5. Theme token vs arbitrary value?

Theme token represents a reusable system decision and generates named utilities. Arbitrary value is a local escape hatch for a unique requirement.

### 6. Tailwind vs SCSS?

Tailwind provides generated utilities and variants. SCSS is a preprocessor for authoring custom CSS. They can coexist but solve different problems; standard CSS remains underneath both.

### 7. Does Tailwind automatically guarantee small CSS?

No. Output depends on detected/safelisted classes, plugins, custom CSS, and build setup. Measure the production artifact.

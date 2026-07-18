# 05 - SCSS Practical Activities and Interview Answers

## Activity: Small Design System

Build modules for tokens, focus mixin, button, card, and form controls. Create one `main.scss` entry and compile expanded development plus compressed production CSS.

Requirements:

- `@use`/`@forward`, no Sass `@import`
- CSS custom properties for light/dark runtime colors
- Sass variables for build-time spacing generation
- shallow component selectors
- responsive rules in the owning component
- inspect final CSS size and selectors

### Example Entry

```scss
@use "base/reset";
@use "base/typography";
@use "components/button";
@use "components/card";
// Compiled result: one CSS bundle containing the four modules exactly once.
```

## Interview Questions with Answers

### 1. Sass vs SCSS?

Sass is the preprocessor and ecosystem. SCSS is its CSS-compatible brace/semicolon syntax; indented Sass is another syntax.

### 2. Sass variable vs CSS custom property?

Sass variable is replaced at build time and does not reach the browser. Custom property remains in CSS, participates in cascade/inheritance, and can change at runtime.

### 3. `@use` vs deprecated `@import`?

`@use` loads a module once, namespaces members, and exposes a controlled API. Sass `@import` can duplicate output and pollute global scope.

### 4. Mixin vs function?

A mixin emits declaration/rule content. A function computes and returns a value.

### 5. Why avoid deep nesting?

It produces overly specific, DOM-coupled selectors that are hard to override and reuse.

### 6. Does Sass solve browser compatibility?

No. Browsers receive generated CSS, and each CSS feature still needs target-browser support or fallback/prefix processing.

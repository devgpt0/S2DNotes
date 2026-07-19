# SCSS 45-Minute Project - Themeable Card Component Kit

## Goal

Create Button, Card, and Alert components using Sass modules, functions, mixins, maps, runtime CSS tokens, shallow selectors, and a production build.

## Time Box

- 0-8 min: folders and entry point
- 8-18 min: tokens and mixins
- 18-33 min: three components
- 33-40 min: dark theme and responsive behavior
- 40-45 min: compile and inspect output

## Step 1: Structure

```text
styles/
├─ tokens/_index.scss
├─ tools/_focus.scss
├─ components/_button.scss
├─ components/_card.scss
├─ components/_alert.scss
└─ main.scss
# Result: one entry file and focused modules.
```

## Step 2: Tokens

```scss
// tokens/_index.scss
$spaces: (1: .25rem, 2: .5rem, 4: 1rem);
:root { --brand: royalblue; --surface: white; --text: #17202a; }
@media (prefers-color-scheme: dark) { :root { --surface: #15181d; --text: #f5f5f5; } }
// Compiled result: runtime light/dark custom properties and a build-time spacing map.
```

## Step 3: Tool and Button

```scss
// tools/_focus.scss
@mixin ring($color: currentColor) { outline: .2rem solid $color; outline-offset: .2rem; }

// components/_button.scss
@use "../tools/focus";
.button { border: 0; border-radius: .4rem; padding: .5rem 1rem; background: var(--brand); color: white; }
.button:focus-visible { @include focus.ring(); }
.button[disabled] { opacity: .5; cursor: not-allowed; }
// Compiled result: accessible reusable button rules with focus and disabled state.
```

## Step 4: Card and Alert

```scss
.card { container-type: inline-size; padding: 1rem; color: var(--text); background: var(--surface); border: 1px solid color-mix(in oklch, currentColor 20%, transparent); }
@container (min-width: 24rem) { .card__body { display: grid; grid-template-columns: 6rem 1fr; gap: 1rem; } }

$states: (success: #176b3a, warning: #8a4b00, danger: #9b1c1c);
@each $name, $color in $states { .alert--#{$name} { border-inline-start: .3rem solid $color; color: $color; } }
// Compiled result: container-responsive card and three finite alert variants.
```

## Step 5: Entry and Build

```scss
@layer base, components;
@use "tokens";
@use "components/button";
@use "components/card";
@use "components/alert";
// Compiled result: modules load once through the entry point.
```

```powershell
npx sass styles/main.scss dist/styles.css
npx sass --style=compressed styles/main.scss dist/styles.min.css
# Result: readable development CSS and compressed production CSS.
```

## Interview Review

Explain Sass vs SCSS, Sass variable vs CSS custom property, `@use/@forward`, mixin vs function, why nesting stays shallow, loop output risk, source maps, Autoprefixer, and why the browser still only understands CSS.

## Completion Definition

No deprecated import, no deep selector, output inspected, theme changes at runtime, focus visible, finite generated variants, and production CSS size recorded.

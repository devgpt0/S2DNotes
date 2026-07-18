# 01 - SCSS Setup, Variables, Nesting, and Parent Selector

## Compile SCSS

```powershell
npm install --save-dev sass
npx sass src/styles/main.scss dist/styles.css
# Result: Sass compiles main.scss and its modules into browser-readable styles.css.
```

Watch during development:

```powershell
npx sass --watch src/styles/main.scss:dist/styles.css
# Result: styles.css is regenerated whenever source SCSS changes.
```

## Sass Variable vs CSS Custom Property

```scss
$spacing: 1rem;
:root { --brand-color: royalblue; }
.card { padding: $spacing; color: var(--brand-color); }
// Compiled result: $spacing becomes 1rem; --brand-color remains runtime CSS.
```

Sass variables exist only during compilation. CSS custom properties cascade, inherit, and can change at runtime.

## Nesting

```scss
.card {
  padding: 1rem;

  > h2 { margin-block-start: 0; }

  &:hover { box-shadow: 0 .5rem 1rem rgb(0 0 0 / .15); }
}
// Compiled selectors: .card, .card > h2, and .card:hover.
```

Keep nesting shallow. Deep nesting creates highly specific selectors tied to fragile HTML structure.

## Parent Selector `&`

```scss
.button {
  &--primary { background: royalblue; }
  &[disabled] { opacity: .5; }
}
// Compiled selectors: .button--primary and .button[disabled].
```

## Interpolation

```scss
$name: "warning";
.#{$name} { color: darkred; }
// Compiled result: .warning { color: darkred; }
```

Use interpolation only where a selector/property string genuinely must be generated.

## Beginner Practice

Create a `.profile-card` with title, image, hover state, and `--compact` modifier. Compile it and inspect the generated selectors before opening the browser.

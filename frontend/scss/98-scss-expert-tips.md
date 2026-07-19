# SCSS Expert Tips and Architecture Playbook

## Module Design

- Use `@use` and `@forward`; never start new code with deprecated Sass `@import`.
- Expose a small public module API and keep implementation helpers private with leading `-` or `_` naming conventions.
- Configure modules once through `with`; avoid global mutable configuration.
- Keep token/functions/mixins modules output-free unless their contract intentionally emits CSS.
- Prefer feature/component ownership over a universal “helpers” dumping ground.

## Variables and Tokens

- Sass variables are compile-time constants/configuration; CSS custom properties are runtime cascading tokens.
- Generate default custom properties from Sass maps only when it reduces duplication and output remains inspectable.
- Keep semantic tokens (`--color-danger`) separate from raw palette values.
- Do not create Sass variables for every literal; name decisions with reuse or meaning.

## Mixins and Functions

- A mixin should encode a repeated declaration pattern with a clear contract.
- A function should be pure and return a value.
- Use `sass:math`, `sass:map`, `sass:list`, `sass:string`, and `sass:color` module APIs.
- Validate mixin/function arguments with helpful `@error` when invalid build input must stop compilation.
- Avoid huge mixins included hundreds of times; inspect duplicate output.
- Prefer content blocks (`@content`) only when the extension point is easier than ordinary nested CSS.

## Selector Safety

- Limit nesting to one or two meaningful levels.
- Use `&` for states/modifiers, not to construct difficult selector puzzles.
- Be cautious with `@extend`; it unifies selectors and can create surprising groups across modules.
- A shared class or mixin is often more predictable than a placeholder extension.
- Never let loop-generated combinations grow without calculating output cardinality.

## Build and Performance

- Compile expanded CSS with source maps in development and compressed CSS in production.
- Run PostCSS/Autoprefixer after Sass according to browser targets.
- Minification is not unused-CSS removal.
- Inspect compressed bytes, duplicated declarations, source-map policy, and critical CSS delivery.
- Add a CI size budget for generated CSS if growth is a product risk.
- Treat Sass deprecation warnings as migration work, not permanent noise.

## Architecture Example

```text
styles/
├─ tokens/       # Sass config + emitted CSS custom properties
├─ tools/        # output-free functions and mixins
├─ base/         # reset, type, elements
├─ layouts/      # reusable layout objects
├─ components/   # feature-owned component rules
├─ utilities/    # intentionally small utilities
└─ main.scss     # explicit ordered entry point/layers
# Result: predictable ownership, module dependencies, and CSS output order.
```

## Debugging Expert Workflow

Inspect the compiled selector/value first, use source maps to locate SCSS, run Sass with warnings visible, search duplicate output, check module load/configuration order, then debug browser cascade/layout like ordinary CSS.

## Expert Code Snippets Used in Production

### Validated Token Function

```scss
@use "sass:map";
$spaces: (1: .25rem, 2: .5rem, 4: 1rem, 8: 2rem);
@function space($key) {
  @if not map.has-key($spaces, $key) { @error "Unknown spacing token: #{$key}"; }
  @return map.get($spaces, $key);
}
.card { padding: space(4); }
// Compiled result: .card gets 1rem; unknown keys fail the build with an actionable error.
```

### Runtime Theme Generated from a Sass Map

```scss
$light: (surface: #fff, text: #17202a, brand: royalblue);
@mixin emit-theme($tokens) {
  @each $name, $value in $tokens { --#{$name}: #{$value}; }
}
:root { @include emit-theme($light); }
// Compiled result: CSS custom properties --surface, --text, and --brand remain runtime-changeable.
```

### Public Module Facade

```scss
// tools/_index.scss
@forward "focus" show ring;
@forward "layout" show cluster, wrapper;

// component.scss
@use "../tools" as tools;
.button:focus-visible { @include tools.ring(); }
// Result: consumers see only the intentionally forwarded mixins through one namespace.
```

### Responsive Mixin Without Device Names

```scss
@mixin from($width) { @media (min-width: $width) { @content; } }
.layout { display: grid; @include from(48rem) { grid-template-columns: 16rem minmax(0, 1fr); } }
// Compiled result: content-based 48rem enhancement; no misleading "tablet" abstraction.
```

## High-Use Public Module Pattern

```scss
// components/_index.scss
@forward "button";
@forward "card";

// main.scss
@use "components";

.card-list { display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 18rem), 1fr)); gap: var(--space-4); }
```

`@forward` creates one intentional public Sass entry point. Keep component selectors usable on their own; use Sass modules for authoring organization and CSS custom properties for runtime extension.

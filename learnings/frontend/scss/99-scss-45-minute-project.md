# 99 - Build a Themeable Card Kit in 45 Minutes

## Project Overview

Build a small card, button, and alert kit with Sass modules. Sass handles author-time organization and finite generated variants. CSS custom properties handle runtime themes. The result is responsive, keyboard-friendly, and compiled into one browser-ready stylesheet.

## What You Will Learn

- the difference between Sass source and browser CSS
- `@use`, namespacing, partials, maps, mixins, and loops
- when to use a Sass variable and when to use a CSS custom property
- shallow component selectors and predictable variant output
- container-responsive composition, focus states, and dark theme tokens
- development and compressed production builds

## Folder Structure

```text
scss-card-kit/
|-- index.html
|-- package.json
`-- styles/
    |-- _tokens.scss
    |-- _tools.scss
    |-- _components.scss
    `-- main.scss
```

`dist/styles.css` and `dist/styles.min.css` are generated files, so edit the Sass source instead.

## File: `package.json`

```json
{
  "name": "scss-card-kit",
  "private": true,
  "scripts": {
    "dev": "sass --watch --source-map styles/main.scss:dist/styles.css",
    "build": "sass --no-source-map --style=compressed styles/main.scss:dist/styles.min.css"
  },
  "devDependencies": {
    "sass": "^1.89.0"
  }
}
```

Concepts learned from this file:

- watch mode creates readable CSS and source maps for development.
- the production command creates compressed output without a public source map.
- only the compiler is required; the browser still receives ordinary CSS.

## File: `index.html`

```html
<!doctype html>
<html lang="en" data-theme="light">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>SCSS Card Kit</title>
    <link rel="stylesheet" href="dist/styles.css">
  </head>
  <body>
    <main class="page-shell">
      <header class="stack">
        <p class="eyebrow">SCSS project</p>
        <h1>Reusable course cards</h1>
        <p>Resize the page to see each card respond to its own width.</p>
      </header>

      <section class="card-grid" aria-label="Courses">
        <article class="card">
          <div class="card__body">
            <div class="card__image" aria-hidden="true">J</div>
            <div class="stack">
              <h2 class="card__title">Java Foundations</h2>
              <p>Variables, methods, control flow, and objects.</p>
              <div class="alert alert--success" role="status">Enrollment is open</div>
            </div>
          </div>
          <a class="button" href="#java">View course</a>
        </article>

        <article class="card">
          <div class="card__body">
            <div class="card__image" aria-hidden="true">R</div>
            <div class="stack">
              <h2 class="card__title">React Practice</h2>
              <p>Components, state, forms, and accessible UI.</p>
              <div class="alert alert--warning" role="status">Two places remain</div>
            </div>
          </div>
          <button class="button button--secondary" type="button">Join waitlist</button>
        </article>
      </section>
    </main>
  </body>
</html>
```

Concepts learned from this file:

- component class names express structure without depending on element order.
- links navigate; buttons perform actions.
- a live status is used only for meaningful current information.
- the HTML has no Sass knowledge and works with the generated stylesheet.

## File: `styles/_tokens.scss`

```scss
$space: (
  1: 0.25rem,
  2: 0.5rem,
  3: 0.75rem,
  4: 1rem,
  6: 1.5rem,
  8: 2rem,
);

$alert-colors: (
  success: #176b3a,
  warning: #8a4b00,
  danger: #9b1c1c,
);

:root {
  color-scheme: light;
  --brand: #3157d5;
  --brand-strong: #213d9d;
  --surface: #f6f7fb;
  --surface-raised: #fff;
  --text: #17202a;
  --border: #d7dbe7;
  --shadow: 0 0.75rem 2rem rgb(20 30 60 / 12%);
}

[data-theme="dark"] {
  color-scheme: dark;
  --brand: #9aaeff;
  --brand-strong: #c5d0ff;
  --surface: #11131a;
  --surface-raised: #1b1e28;
  --text: #f3f5fa;
  --border: #3c4252;
  --shadow: none;
}
```

Concepts learned from this file:

- Sass maps are build-time data used while compiling.
- CSS custom properties remain in the browser and can change at runtime.
- semantic token names describe roles, so a theme can change values without rewriting components.

## File: `styles/_tools.scss`

```scss
@use "sass:map";
@use "tokens";

@function space($step) {
  $value: map.get(tokens.$space, $step);
  @if $value == null {
    @error "Unknown spacing step: #{$step}";
  }
  @return $value;
}

@mixin focus-ring($color: var(--brand)) {
  outline: 0.2rem solid $color;
  outline-offset: 0.2rem;
}
```

Concepts learned from this file:

- namespaced module access shows where shared values come from.
- the function fails compilation for an invalid token instead of returning an unclear value.
- a mixin is useful here because it emits a repeated group of declarations.

## File: `styles/_components.scss`

```scss
@use "sass:map";
@use "tokens";
@use "tools";

.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 18rem), 1fr));
  gap: tools.space(6);
}

.card {
  container-type: inline-size;
  display: flex;
  flex-direction: column;
  gap: tools.space(6);
  padding: tools.space(6);
  border: 1px solid var(--border);
  border-radius: 1rem;
  background: var(--surface-raised);
  box-shadow: var(--shadow);
}

.card__body {
  display: grid;
  gap: tools.space(4);
}

.card__image {
  display: grid;
  place-items: center;
  inline-size: 4rem;
  aspect-ratio: 1;
  border-radius: 50%;
  color: white;
  background: var(--brand);
  font-size: 1.5rem;
  font-weight: 800;
}

.card__title { font-size: 1.25rem; }
.card > :last-child { margin-block-start: auto; }

@container (min-width: 24rem) {
  .card__body {
    grid-template-columns: auto minmax(0, 1fr);
    align-items: start;
  }
}

.button {
  display: inline-flex;
  min-block-size: 2.75rem;
  align-items: center;
  justify-content: center;
  border: 1px solid transparent;
  border-radius: 0.5rem;
  padding-inline: tools.space(4);
  color: white;
  background: var(--brand-strong);
  font: inherit;
  font-weight: 700;
  text-decoration: none;
  cursor: pointer;
}

.button--secondary {
  border-color: var(--border);
  color: var(--text);
  background: transparent;
}

.button:focus-visible { @include tools.focus-ring; }

.alert {
  padding: tools.space(3);
  border-inline-start: 0.3rem solid currentColor;
  background: color-mix(in srgb, currentColor 8%, transparent);
}

@each $name, $color in tokens.$alert-colors {
  .alert--#{$name} { color: $color; }
}
```

Concepts learned from this file:

- shallow selectors keep component rules easy to override and move.
- a container query lets a card adapt wherever it is placed.
- the loop generates a small known set of variants; it does not create open-ended CSS.
- `margin-block-start: auto` aligns actions without fixed card heights.

## File: `styles/main.scss`

```scss
@use "tokens";
@use "tools";
@use "components";

*, *::before, *::after { box-sizing: border-box; }
body, h1, h2, p { margin: 0; }
body {
  min-block-size: 100dvh;
  color: var(--text);
  background: var(--surface);
  font-family: ui-sans-serif, system-ui, sans-serif;
  line-height: 1.5;
}

.page-shell {
  inline-size: min(100% - 2rem, 72rem);
  margin-inline: auto;
  padding-block: clamp(2rem, 8vw, 5rem);
}

.page-shell > * + * { margin-block-start: 2rem; }
.stack { display: grid; gap: 0.75rem; }
.eyebrow { color: var(--brand-strong); font-size: 0.8rem; font-weight: 800; text-transform: uppercase; }
```

Concepts learned from this file:

- the entry point loads each module once and owns global page rules.
- modules do not leak Sass variables globally.
- fluid spacing and a maximum line width make the demo responsive without many breakpoints.

## Run and Verify

```powershell
npm install
npm run dev
# Output: Sass watches styles/main.scss and writes dist/styles.css.
```

Serve the folder with `python -m http.server 8000`, open `http://localhost:8000`, then run `npm run build` for compressed CSS.

Verify keyboard focus, 320px width, 200% zoom, light/dark tokens, the container layout, generated `.alert--*` rules, source mapping, and final compressed size.

## Completion Definition

Every source file above exists, Sass builds without warnings, generated output is inspected rather than edited, cards do not overflow, focus stays visible, themes use runtime tokens, and you can explain the concept section for every file.

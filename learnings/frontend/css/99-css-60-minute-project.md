# 99 - Build a Responsive Course Dashboard in 60 Minutes

## Project Overview

Build a responsive dashboard using semantic HTML and standard CSS. The layout adapts without device-specific breakpoints, supports dark mode and reduced motion, contains an overflow-safe table, and exposes visible keyboard focus.

## What You Will Learn

- cascade layers, custom properties, inheritance, and low-specificity selectors
- mobile-first Grid and Flexbox layouts
- intrinsic sizing with `min()`, `minmax()`, `clamp()`, and `auto-fit`
- component-level container queries
- responsive tables, focus states, dark mode, and reduced motion
- browser rendering checks: layout, paint, overflow, and performance
- interview topics: box model, specificity, formatting contexts, stacking, and media vs container queries

## Time Plan

| Minutes | Work |
|---:|---|
| 0-5 | Create files and run the server |
| 5-15 | Add reset, tokens, and page shell |
| 15-35 | Build the responsive cards and toolbar |
| 35-45 | Add the table and interaction states |
| 45-55 | Add preference queries and container enhancement |
| 55-60 | Test and answer interview questions |

## Folder Structure

```text
css-course-dashboard/
|-- index.html
`-- styles.css
# Result: one semantic page and one standards-based stylesheet.
```

## Step 1: Create `index.html`

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="Responsive course progress dashboard.">
    <title>Course Dashboard</title>
    <link rel="stylesheet" href="styles.css">
  </head>
  <body>
    <a class="skip-link" href="#main-content">Skip to main content</a>

    <header class="site-header">
      <a class="brand" href="#">SkillTrack</a>
      <nav aria-label="Primary navigation">
        <a aria-current="page" href="#courses">Courses</a>
        <a href="#schedule">Schedule</a>
      </nav>
    </header>

    <main id="main-content" class="page-shell">
      <section class="hero" aria-labelledby="page-title">
        <p class="eyebrow">Learning dashboard</p>
        <h1 id="page-title">Keep your frontend plan moving</h1>
        <p>Track the modules that matter most for your next interview.</p>
      </section>

      <section id="courses" aria-labelledby="courses-heading">
        <div class="toolbar">
          <div>
            <h2 id="courses-heading">Your courses</h2>
            <p class="muted">Three active learning paths</p>
          </div>
          <button type="button">Add course</button>
        </div>

        <div class="course-grid">
          <article class="course-card">
            <div class="course-card__content">
              <span class="course-card__icon" aria-hidden="true">H</span>
              <div>
                <p class="eyebrow">Foundation</p>
                <h3>Semantic HTML</h3>
                <p>Landmarks, forms, tables, media, and accessibility.</p>
              </div>
            </div>
            <label for="html-progress">Progress: 80%</label>
            <progress id="html-progress" max="100" value="80">80%</progress>
          </article>

          <article class="course-card">
            <div class="course-card__content">
              <span class="course-card__icon" aria-hidden="true">C</span>
              <div>
                <p class="eyebrow">Presentation</p>
                <h3>Responsive CSS</h3>
                <p>Cascade, Grid, container queries, and browser rendering.</p>
              </div>
            </div>
            <label for="css-progress">Progress: 55%</label>
            <progress id="css-progress" max="100" value="55">55%</progress>
          </article>

          <article class="course-card">
            <div class="course-card__content">
              <span class="course-card__icon" aria-hidden="true">J</span>
              <div>
                <p class="eyebrow">Behavior</p>
                <h3>JavaScript Essentials</h3>
                <p>Language fundamentals, DOM, async work, and testing.</p>
              </div>
            </div>
            <label for="js-progress">Progress: 25%</label>
            <progress id="js-progress" max="100" value="25">25%</progress>
          </article>
        </div>
      </section>

      <section id="schedule" aria-labelledby="schedule-heading">
        <h2 id="schedule-heading">This week's schedule</h2>
        <div class="table-scroll" tabindex="0" role="region" aria-label="Weekly lesson schedule">
          <table>
            <caption>Upcoming lessons</caption>
            <thead>
              <tr><th scope="col">Day</th><th scope="col">Course</th><th scope="col">Topic</th><th scope="col">Time</th></tr>
            </thead>
            <tbody>
              <tr><th scope="row">Monday</th><td>HTML</td><td>Accessible forms</td><td>7:00 PM</td></tr>
              <tr><th scope="row">Wednesday</th><td>CSS</td><td>Intrinsic layouts</td><td>7:00 PM</td></tr>
              <tr><th scope="row">Friday</th><td>JavaScript</td><td>Async patterns</td><td>6:30 PM</td></tr>
            </tbody>
          </table>
        </div>
      </section>
    </main>

    <footer><p>&copy; 2026 SkillTrack</p></footer>
    <!-- Browser result: responsive course cards, progress indicators, and an overflow-safe schedule. -->
  </body>
</html>
```

Concepts learned from `index.html`:

- semantic source order remains useful before any CSS is loaded
- component classes describe roles without changing native control meaning
- progress, table headers, skip navigation, and landmarks provide accessible structure

## Step 2: Create `styles.css`

```css
@layer reset, base, layout, components, utilities;

@layer reset {
  *, *::before, *::after { box-sizing: border-box; }
  body, h1, h2, h3, p { margin: 0; }
  img, svg { display: block; max-inline-size: 100%; }
  button, input, select, textarea { font: inherit; }
}

@layer base {
  :root {
    color-scheme: light dark;
    --brand: oklch(55% 0.2 264);
    --brand-strong: oklch(45% 0.2 264);
    --surface: oklch(99% 0.005 264);
    --surface-raised: white;
    --text: oklch(22% 0.02 264);
    --muted: oklch(48% 0.03 264);
    --border: oklch(86% 0.02 264);
    --shadow: 0 0.5rem 1.5rem rgb(20 24 40 / 0.1);
    --radius: 0.8rem;
    --space: clamp(1rem, 2vw, 1.5rem);
  }

  html { font-family: Inter, ui-sans-serif, system-ui, sans-serif; line-height: 1.5; }
  body { min-block-size: 100dvh; color: var(--text); background: var(--surface); }
  a { color: var(--brand-strong); text-underline-offset: 0.2em; }
  :focus-visible { outline: 0.2rem solid var(--brand); outline-offset: 0.2rem; }
  h1 { font-size: clamp(2rem, 7vw, 4rem); line-height: 1.05; max-inline-size: 16ch; }
  h2 { font-size: clamp(1.4rem, 3vw, 2rem); }
  h3 { font-size: 1.15rem; }
}

@layer layout {
  .site-header, .page-shell, footer {
    inline-size: min(100% - 2rem, 72rem);
    margin-inline: auto;
  }

  .site-header {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
    padding-block: 1rem;
  }

  .site-header nav { display: flex; flex-wrap: wrap; gap: 1rem; }
  .page-shell { display: grid; gap: clamp(2.5rem, 7vw, 5rem); padding-block: 3rem; }
  .hero { display: grid; gap: 1rem; padding-block: clamp(2rem, 8vw, 6rem); }
  section { display: grid; gap: var(--space); }
  footer { padding-block: 2rem; }
}

@layer components {
  .skip-link { position: fixed; inset: 0 auto auto 0; z-index: 10; padding: 0.75rem; background: var(--text); color: var(--surface); transform: translateY(-110%); }
  .skip-link:focus { transform: translateY(0); }
  .brand { color: var(--text); font-size: 1.25rem; font-weight: 800; text-decoration: none; }
  .toolbar { display: flex; flex-wrap: wrap; align-items: end; justify-content: space-between; gap: 1rem; }
  button { border: 0; border-radius: 0.5rem; padding: 0.7rem 1rem; color: white; background: var(--brand-strong); cursor: pointer; }
  button:hover { background: var(--brand); }

  .course-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 18rem), 1fr)); gap: var(--space); }
  .course-card { container-type: inline-size; display: grid; gap: 1.25rem; padding: var(--space); border: 1px solid var(--border); border-radius: var(--radius); background: var(--surface-raised); box-shadow: var(--shadow); }
  .course-card__content { display: grid; gap: 1rem; }
  .course-card__icon { display: grid; place-items: center; inline-size: 3rem; aspect-ratio: 1; border-radius: 50%; color: white; background: var(--brand); font-weight: 800; }
  .course-card label { font-size: 0.9rem; }
  progress { inline-size: 100%; accent-color: var(--brand); }

  @container (min-width: 22rem) {
    .course-card__content { grid-template-columns: auto minmax(0, 1fr); align-items: start; }
  }

  .table-scroll { max-inline-size: 100%; overflow-x: auto; border: 1px solid var(--border); border-radius: var(--radius); }
  table { inline-size: 100%; min-inline-size: 42rem; border-collapse: collapse; }
  caption { padding: 1rem; font-weight: 700; text-align: start; }
  th, td { padding: 0.8rem 1rem; border-block-start: 1px solid var(--border); text-align: start; }
  thead { background: color-mix(in oklch, var(--brand) 10%, var(--surface-raised)); }
}

@layer utilities {
  .eyebrow { color: var(--brand-strong); font-size: 0.8rem; font-weight: 800; letter-spacing: 0.08em; text-transform: uppercase; }
  .muted { color: var(--muted); }
}

@media (prefers-color-scheme: dark) {
  :root {
    --surface: oklch(18% 0.02 264);
    --surface-raised: oklch(23% 0.025 264);
    --text: oklch(94% 0.01 264);
    --muted: oklch(75% 0.02 264);
    --border: oklch(38% 0.025 264);
    --brand: oklch(72% 0.16 264);
    --brand-strong: oklch(78% 0.14 264);
    --shadow: none;
  }
}

@media (prefers-reduced-motion: no-preference) {
  .course-card { transition: translate 160ms ease, box-shadow 160ms ease; }
  .course-card:hover { translate: 0 -0.2rem; }
  .skip-link { transition: transform 120ms ease; }
}

@media (forced-colors: active) {
  button, .course-card { border: 1px solid ButtonText; }
}

/* Browser result: intrinsic card wrapping, container-aware content, dark mode, visible focus, and safe table scrolling. */
```

Concepts learned from `styles.css`:

- layers control broad precedence without specificity escalation
- intrinsic Grid and container queries respond to available space instead of named devices
- tokens keep themes extendable while logical properties support different writing directions
- focus, dark mode, reduced motion, forced colors, and overflow are functional requirements, not decoration

## Step 3: Run the Project

```powershell
python -m http.server 8000
# Terminal output: Serving HTTP on ... port 8000.
```

Open `http://localhost:8000`, then stop with `Ctrl+C`.

## Expected Behavior

- Cards form one or more columns based on available width without fixed device breakpoints.
- Card content changes layout when each card—not the viewport—reaches 22rem.
- The schedule scrolls inside its region instead of overflowing the page.
- Keyboard focus is clearly visible.
- The operating-system dark theme changes tokens.
- Reduced-motion users do not receive hover movement.

## Browser and Responsive Test Plan

1. Drag the viewport continuously from 320px to 1600px; look for horizontal page overflow.
2. Zoom to 200% and increase the browser's default text size.
3. Replace a title with a 60-character unbroken value and add `overflow-wrap: anywhere` only where the product permits breaking identifiers.
4. Inspect Grid, container, and scroll overlays in DevTools.
5. Emulate dark mode, reduced motion, and forced colors.
6. Record a Performance trace while resizing. Look for repeated expensive layout or paint work.
7. Test current Chromium, Firefox, and Safari/WebKit when those browsers are in the support policy.

## Practice Extensions

1. Add a sidebar at wide viewport sizes without changing source order.
2. Style `progress` consistently while preserving its semantic value.
3. Add print styles that remove navigation and shadows.
4. Add a user-controlled theme by changing custom properties on `[data-theme="dark"]`.

## Interview Questions and Solutions

### Why use `minmax(min(100%, 18rem), 1fr)`?

It creates equal flexible tracks while allowing a card to shrink below 18rem on narrow containers, preventing page overflow.

### Why use `minmax(0, 1fr)` inside the card?

Grid items have an automatic intrinsic minimum. Setting the track minimum to zero lets long content shrink instead of forcing overflow.

### Container query or media query?

Use a container query when a component responds to its own space. Use a media query for viewport conditions or user preferences such as reduced motion.

### What is the difference between layout and paint?

Layout calculates element geometry. Paint draws pixels. Some changes also require compositing. DevTools Performance and Rendering panels show which work repeats.

### Why use cascade layers?

Layers define precedence before specificity is compared, making resets, components, and utilities predictable without escalating selectors.

## Completion Definition

The project is complete when it has no page-level overflow at 320px or 200% zoom, retains logical source/focus order, respects user preferences, exposes a usable schedule, and you can explain every interview answer.

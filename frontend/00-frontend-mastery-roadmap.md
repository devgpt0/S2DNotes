# Frontend Development - Beginner to Expert Roadmap

Use the dedicated [Chrome browser understanding, diagnostics, and performance roadmap](browser/00-chrome-browser-roadmap.md) alongside every module. It explains what the browser does and how to measure problems instead of guessing.

After React and TypeScript fundamentals, use the [Redux Toolkit state-management roadmap](redux/00-redux-toolkit-roadmap.md) when an application has demonstrated shared client-state complexity.

This course assumes no frontend experience. Study in order because each module uses ideas from the previous one.

## Learning Order

1. [HTML](html/00-html-roadmap.md) - content, structure, forms, accessibility, and browser loading
2. [Standard CSS](css/00-standard-css-roadmap.md) - styling, layout, responsive design, and browser rendering
3. [SCSS](scss/00-scss-roadmap.md) - maintainable CSS authoring with Sass
4. [Tailwind CSS](tailwind/00-tailwind-roadmap.md) - utility-first styling using Tailwind CSS 4
5. [JavaScript](javascript/00-javascript-roadmap.md) - language, DOM, asynchronous code, browser APIs, and performance
6. [TypeScript](typescript/00-typescript-roadmap.md) - safe JavaScript with static types, targeting TypeScript 7
7. [React](react/00-react-roadmap.md) - React 19 components, rendering, hooks, async UI, testing, and architecture
8. [shadcn/ui](shadcn/00-shadcn-roadmap.md) - source-owned accessible components, Tailwind theming, forms, and production composition

## How to Study

For every example:

1. Predict what the browser or console will show.
2. Type the example instead of copying it.
3. Open browser DevTools and inspect the DOM, CSS, network, and console.
4. Change one value and explain the new result.
5. Complete the activity before reading its solution.

## Browser Mental Model

```text
HTML -> DOM tree
CSS -> CSSOM tree
DOM + CSSOM -> render tree -> layout -> paint -> compositing -> pixels
JavaScript can read or change the DOM/CSSOM while the page runs.
# Result: the browser turns files into an interactive visual page.
```

## Current Tool Versions

- Tailwind CSS 4.3.x
- Sass 1.101.x
- TypeScript 7.x
- React 19.2.x
- shadcn CLI 4.13.x

Core HTML, CSS, and JavaScript notes use web standards rather than framework-specific behavior.

## Every Module Ends the Same Way

- `98-*-expert-tips.md`: production tips plus code patterns experts commonly use
- `99-*-project.md`: a focused 30-60 minute project combining the module's interview-important concepts

Complete the project without copying, then compare your result with the supplied steps and completion checklist.

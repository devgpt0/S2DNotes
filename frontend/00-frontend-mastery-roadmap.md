# Frontend Development - Beginner to Expert Roadmap

This course assumes no frontend experience. Study in order because each module uses ideas from the previous one.

## Learning Order

1. [HTML](html/00-html-roadmap.md) - content, structure, forms, accessibility, and browser loading
2. [Standard CSS](css/00-standard-css-roadmap.md) - styling, layout, responsive design, and browser rendering
3. [SCSS](scss/00-scss-roadmap.md) - maintainable CSS authoring with Sass
4. [Tailwind CSS](tailwind/00-tailwind-roadmap.md) - utility-first styling using Tailwind CSS 4
5. [JavaScript](javascript/00-javascript-roadmap.md) - language, DOM, asynchronous code, browser APIs, and performance
6. [TypeScript](typescript/00-typescript-roadmap.md) - safe JavaScript with static types, targeting TypeScript 7

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

Core HTML, CSS, and JavaScript notes use web standards rather than framework-specific behavior.

# 05 - Hands-On Chrome Performance Lab

## Lab Goal

Build a deliberately slow course list, prove why it is slow in Chrome, then apply one measured improvement.

You will record one interaction, find a long main-thread task, separate computation from DOM work, render only the useful result, and compare before and after under the same conditions.

## Folder Structure

```text
chrome-performance-lab/
|-- index.html
|-- app.js
`-- styles.css
```

## File: `index.html`

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Chrome Performance Lab</title>
    <link rel="stylesheet" href="styles.css">
  </head>
  <body>
    <main class="shell">
      <h1>Course search performance lab</h1>
      <label for="query">Search 20,000 courses</label>
      <input id="query" type="search" autocomplete="off">
      <p id="status" role="status"></p>
      <ol id="results"></ol>
    </main>
    <script type="module" src="app.js"></script>
  </body>
</html>
```

Concepts learned: one measurable interaction, one visible result, an announced status, and module loading after parsing.

## File: `styles.css`

```css
*, *::before, *::after { box-sizing: border-box; }
body { margin: 0; font-family: ui-sans-serif, system-ui, sans-serif; line-height: 1.5; }
.shell { inline-size: min(100% - 2rem, 48rem); margin-inline: auto; padding-block: 3rem; }
label { display: block; font-weight: 700; }
input { inline-size: 100%; min-block-size: 2.75rem; padding-inline: 0.75rem; font: inherit; }
li { padding-block: 0.35rem; }
```

Concepts learned: the layout is intentionally simple so the profile centers on application work; the input remains usable at narrow widths and zoom.

## File: `app.js` - Slow Version

```javascript
const query = document.querySelector("#query");
const status = document.querySelector("#status");
const results = document.querySelector("#results");

if (!(query instanceof HTMLInputElement)
  || !(status instanceof HTMLParagraphElement)
  || !(results instanceof HTMLOListElement)) {
  throw new Error("required lab elements are missing");
}

const courses = Array.from({ length: 20_000 }, (_, index) => ({
  id: `course-${index}`,
  title: `Course ${index}: JavaScript and Browser Skills`,
}));

function renderMatches(searchText) {
  const normalized = searchText.toLocaleLowerCase();
  const matches = courses.filter((course) =>
    course.title.toLocaleLowerCase().includes(normalized),
  );

  results.replaceChildren(...matches.map((course) => {
    const item = document.createElement("li");
    item.textContent = course.title;
    return item;
  }));
  status.textContent = `${matches.length} courses found`;
}

query.addEventListener("input", () => renderMatches(query.value));
renderMatches("");
```

The deliberate problem is not the filter alone. The page creates and inserts up to 20,000 DOM nodes for every keystroke.

## Measure the Slow Version

1. Run `python -m http.server 8000` in the folder.
2. Open `http://localhost:8000`.
3. Open Performance and set a 4x CPU slowdown.
4. Start recording and type `199`.
5. Stop after results appear.
6. Find the Input event and its main-thread task.
7. Locate `renderMatches` in Call Tree or Bottom-Up.
8. Record scripting, rendering, paint, DOM-node, and visible-delay evidence.

Use this measurement note:

```text
Chrome version, CPU profile, viewport:
Interaction: type 199
Longest task:
renderMatches time:
DOM nodes before/after:
Visible delay:
```

## Hypothesis

> Limiting DOM output to the first 100 matches will remove most node creation and reduce interaction delay while preserving a clear total result count.

## File: `app.js` - Optimized `renderMatches`

Replace only the function and add the constant:

```javascript
const MAX_VISIBLE_RESULTS = 100;

function renderMatches(searchText) {
  performance.mark("course-search-start");

  const normalized = searchText.toLocaleLowerCase();
  const matches = courses.filter((course) =>
    course.title.toLocaleLowerCase().includes(normalized),
  );
  const visibleMatches = matches.slice(0, MAX_VISIBLE_RESULTS);
  const fragment = document.createDocumentFragment();

  for (const course of visibleMatches) {
    const item = document.createElement("li");
    item.textContent = course.title;
    fragment.append(item);
  }

  results.replaceChildren(fragment);
  status.textContent = matches.length > MAX_VISIBLE_RESULTS
    ? `${matches.length} courses found; showing the first ${MAX_VISIBLE_RESULTS}`
    : `${matches.length} courses found`;

  performance.mark("course-search-end");
  performance.measure(
    "course-search",
    "course-search-start",
    "course-search-end",
  );
}
```

Why it helps:

- filtering still checks 20,000 small objects
- DOM creation falls from as many as 20,000 rows to at most 100
- the user is told that results are limited
- named performance entries make comparison easier

`DocumentFragment` makes assembly clear, but the main improvement is doing less DOM work. Prove that in the trace.

## Measure Again

Repeat the same Chrome version, viewport, CPU setting, input, and recording window. Run at least three times and note variation rather than reporting the single best result.

| Evidence | Before | After |
|---|---:|---:|
| longest interaction task | measure | measure |
| visible rows | up to 20,000 | up to 100 |
| `renderMatches` time | measure | measure |
| accessibility/correctness | verify | verify |

## Next Experiments

Change one thing per experiment: require two search characters, debounce if delayed feedback is acceptable, precompute normalized titles, test virtualization, move heavy pure computation to a Worker, or paginate on the server.

## Completion Definition

The lab is complete when you can show the original trace, state one evidence-based cause, show the changed trace under the same conditions, explain why the change reduces work, and confirm that accessibility and result messaging still work.

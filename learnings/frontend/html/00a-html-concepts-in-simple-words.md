# HTML Concepts in Simple Words

## The One-Sentence Idea

HTML tells the browser **what each piece of content means**. CSS decides how it looks; JavaScript controls changing behavior.

## Browser Translation

```text
HTML text -> parser -> DOM tree -> accessibility/rendering input
# Result: tags become connected element objects that browsers, CSS, JavaScript, and assistive tools can use.
```

## Essential Concepts

| Concept | Simple meaning | Example |
|---|---|---|
| element | one meaningful page part | heading, paragraph, button |
| tag | syntax marking an element | `<p>` |
| attribute | extra element information | `href`, `alt`, `type` |
| nesting | putting related elements inside another | list items inside a list |
| semantic HTML | element chosen by purpose | `button` for action |
| DOM | browser's object tree made from HTML | JavaScript can query it |
| accessibility tree | information exposed to assistive technology | names, roles, states |
| URL | address of a resource | page, image, API |
| form control | input that collects a named value | email, checkbox |
| metadata | information about the document | title, description, language |

## How to Choose an Element

Ask these questions in order:

1. Is it navigation? Use a link inside suitable navigation.
2. Is it an action? Use a button.
3. Is it a heading? Use the correct heading level.
4. Is it a list? Use `ul`/`ol` with `li`.
5. Is it tabular data? Use a table.
6. Is it a labelled input? Use label plus the correct control.
7. Is there no meaningful element? Use `div` or `span`.

## Small Complete Example

```html
<article>
  <h2>HTML Basics</h2>
  <p>Learn page structure in one hour.</p>
  <a href="/courses/html">View course</a>
  <button type="button">Save course</button>
</article>
<!-- Browser result: a meaningful course article with navigation and action controls. -->
```

## Beginner Mistakes to Avoid

- choosing headings for font size
- using `div` as a clickable button
- using placeholder instead of label
- missing image `alt`
- putting block content in invalid parents
- duplicate IDs
- absolute computer file paths
- relying only on client validation
- adding ARIA when native HTML already solves the problem

## Learning Test

If CSS and JavaScript are removed, a good HTML page should still have a sensible reading order, meaningful controls, understandable form labels, and useful content.

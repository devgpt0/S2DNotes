# 01 - HTML Document Structure, Text, and Elements

## What Is HTML?

HTML stands for HyperText Markup Language. It labels content so browsers and assistive technologies understand its role.

## Minimal Document

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>My first page</title>
  </head>
  <body>
    <h1>Hello HTML</h1>
    <p>This is my first page.</p>
  </body>
</html>
<!-- Browser result: a heading and paragraph; the tab title is "My first page". -->
```

## Element Anatomy

```html
<p class="summary">Easy to read notes</p>
<!-- p is the element, class is an attribute, and the text is its content. -->
```

Most elements have opening and closing tags. Void elements such as `img`, `input`, `br`, and `meta` have no closing tag.

## Heading Order

Use one clear page-level `h1`, then nest sections without skipping levels for visual size.

```html
<h1>Java Course</h1>
<h2>Module 1</h2>
<h3>Lesson 1</h3>
<!-- Browser result: a meaningful document outline with three heading levels. -->
```

Change heading appearance with CSS, not by choosing an incorrect heading level.

## Text Elements

```html
<p>Use <strong>strong</strong> for importance and <em>emphasis</em> for stress.</p>
<blockquote cite="https://example.com/source">Learning requires practice.</blockquote>
<pre><code>console.log("preserved spacing");</code></pre>
<!-- Browser result: paragraph, quoted text, and a preformatted code block. -->
```

Useful elements include `p`, `strong`, `em`, `small`, `mark`, `code`, `pre`, `blockquote`, `q`, `time`, `abbr`, `sub`, and `sup`.

## Lists

```html
<ol>
  <li>Learn HTML</li>
  <li>Learn CSS</li>
</ol>
<ul>
  <li>Practice daily</li>
</ul>
<!-- Browser result: one numbered list and one bulleted list. -->
```

Use `dl`, `dt`, and `dd` for name/value descriptions such as a glossary.

## Global Attributes

- `id`: unique document identifier
- `class`: reusable styling/script hook
- `title`: supplementary advisory text, not a replacement for visible labels
- `hidden`: removes content from normal rendering and accessibility tree
- `data-*`: application-specific data
- `lang`: language of a document or changed-language section

## Beginner Practice

Create an article containing one title, two sections, a quote, an ordered learning plan, and a code block. Open DevTools Elements and confirm the nesting matches your intended outline.

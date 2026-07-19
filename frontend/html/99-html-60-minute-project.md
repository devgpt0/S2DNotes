# 99 - Build an Accessible Course Registration Page in 60 Minutes

## Project Overview

Build a two-page course registration website using only HTML. The finished project has meaningful landmarks, navigation, a course table, accessible details, and a browser-validated registration form.

This project deliberately has no CSS or JavaScript. You will learn what the browser provides before adding presentation or behavior.

## What You Will Learn

- document metadata and a logical heading outline
- semantic landmarks and skip navigation
- accessible links, lists, tables, and disclosure widgets
- labels, fieldsets, autocomplete, validation, and error prevention
- GET form submission and URL query parameters
- browser inspection and keyboard testing
- interview topics: semantics, accessibility tree, native controls, GET vs POST, and progressive enhancement

## Time Plan

| Minutes | Work |
|---:|---|
| 0-5 | Create the folder and files |
| 5-20 | Build the page structure and course content |
| 20-40 | Build the registration form |
| 40-50 | Build the confirmation page |
| 50-60 | Run accessibility and interview checks |

## Prerequisites

- a text editor
- Python 3 or any static-file server
- a modern browser with DevTools

## Folder Structure

```text
html-course-registration/
|-- index.html
`-- success.html
# Result: two complete HTML pages and no hidden dependencies.
```

## Step 1: Create `index.html`

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="Compare and register for beginner web courses.">
    <title>Web Skills Academy | Course Registration</title>
  </head>
  <body>
    <a href="#main-content">Skip to main content</a>

    <header>
      <a href="index.html" aria-label="Web Skills Academy home">Web Skills Academy</a>
      <nav aria-label="Primary navigation">
        <ul>
          <li><a href="#courses">Courses</a></li>
          <li><a href="#register">Register</a></li>
          <li><a href="#questions">Questions</a></li>
        </ul>
      </nav>
    </header>

    <main id="main-content">
      <section aria-labelledby="page-title">
        <h1 id="page-title">Choose your next web course</h1>
        <p>Short, practical courses for developers beginning their frontend journey.</p>
      </section>

      <section id="courses" aria-labelledby="courses-heading">
        <h2 id="courses-heading">Available courses</h2>
        <div role="region" aria-label="Course comparison" tabindex="0">
          <table>
            <caption>Course schedule and difficulty</caption>
            <thead>
              <tr>
                <th scope="col">Course</th>
                <th scope="col">Duration</th>
                <th scope="col">Level</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <th scope="row">HTML Foundations</th>
                <td>2 weeks</td>
                <td>Beginner</td>
              </tr>
              <tr>
                <th scope="row">Responsive CSS</th>
                <td>3 weeks</td>
                <td>Beginner</td>
              </tr>
              <tr>
                <th scope="row">JavaScript Essentials</th>
                <td>4 weeks</td>
                <td>Intermediate</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <section id="register" aria-labelledby="register-heading">
        <h2 id="register-heading">Register</h2>
        <p>All fields marked required must be completed.</p>

        <form action="success.html" method="get">
          <fieldset>
            <legend>Your details</legend>

            <p>
              <label for="full-name">Full name</label><br>
              <input id="full-name" name="name" type="text" autocomplete="name" minlength="2" required>
            </p>

            <p>
              <label for="email">Email address</label><br>
              <input id="email" name="email" type="email" autocomplete="email" aria-describedby="email-help" required>
              <br><small id="email-help">We send the course link to this address.</small>
            </p>

            <p>
              <label for="course">Course</label><br>
              <select id="course" name="course" required>
                <option value="">Choose a course</option>
                <option value="html">HTML Foundations</option>
                <option value="css">Responsive CSS</option>
                <option value="javascript">JavaScript Essentials</option>
              </select>
            </p>
          </fieldset>

          <fieldset>
            <legend>Learning format</legend>
            <label><input type="radio" name="format" value="self-paced" required> Self-paced</label>
            <label><input type="radio" name="format" value="instructor-led"> Instructor-led</label>
          </fieldset>

          <p>
            <label>
              <input type="checkbox" name="terms" value="accepted" required>
              I accept the <a href="#terms">course terms</a>
            </label>
          </p>

          <button type="submit">Register for course</button>
        </form>
      </section>

      <section id="questions" aria-labelledby="questions-heading">
        <h2 id="questions-heading">Common questions</h2>
        <details>
          <summary>Do I need previous experience?</summary>
          <p>No. Start with HTML Foundations if you are completely new.</p>
        </details>
        <details>
          <summary>Will I receive a certificate?</summary>
          <p>Yes, after completing the practical assessment.</p>
        </details>
      </section>

      <section id="terms" aria-labelledby="terms-heading">
        <h2 id="terms-heading">Course terms</h2>
        <p>Registration reserves a place but does not collect payment.</p>
      </section>
    </main>

    <footer>
      <address>Questions? <a href="mailto:learn@example.com">learn@example.com</a></address>
      <p><small>&copy; 2026 Web Skills Academy</small></p>
    </footer>
    <!-- Browser result: a semantic, keyboard-operable registration page with native validation. -->
  </body>
</html>
```

Concepts learned from `index.html`:

- landmarks and headings create a readable document and accessibility outline
- native table, details, form, and validation behavior work without JavaScript
- labels, descriptions, fieldsets, and autocomplete make form intent explicit
- GET submission places values in the URL, so it is unsuitable for secrets or real state-changing registration

## Step 2: Create `success.html`

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="robots" content="noindex">
    <title>Registration Received | Web Skills Academy</title>
  </head>
  <body>
    <main>
      <h1>Registration received</h1>
      <p>Thank you. Check your email for the next steps.</p>
      <p><a href="index.html">Return to course registration</a></p>
    </main>
    <!-- Browser result: successful form submission navigates here; submitted GET values appear in the URL. -->
  </body>
</html>
```

Concepts learned from `success.html`:

- a separate result page gives form navigation a clear destination
- `noindex` prevents a generic confirmation page from becoming a search result
- the return link completes the navigation flow without JavaScript

## Step 3: Run the Project

Open a terminal inside `html-course-registration`:

```powershell
python -m http.server 8000
# Terminal output: Serving HTTP on ... port 8000.
```

Open `http://localhost:8000`. Stop the server with `Ctrl+C`.

If `python` is unavailable, opening `index.html` directly also works for this project.

## Expected Behavior

1. The skip link moves focus to the main content.
2. Primary links move to the correct sections.
3. The table exposes column and row headers.
4. The question summaries expand and collapse without JavaScript.
5. An empty or invalid form is blocked by browser validation.
6. A valid form opens `success.html` and places non-sensitive values in the query string.

## Verification Checklist

- Use only the keyboard: `Tab`, `Shift+Tab`, `Enter`, `Space`, and arrow keys.
- Inspect the Accessibility tree and confirm header, navigation, main, sections, form, and footer.
- Confirm every input has an accessible name.
- Confirm headings do not skip levels.
- Run the page through the W3C HTML validator.
- Test at 200% zoom and with CSS/JavaScript disabled.
- Do not submit passwords or secrets through GET because the values appear in URLs and history.

## Practice Extensions

1. Add a `date` input with visible instructions and a safe minimum date.
2. Add a second table captioned “Upcoming cohorts.”
3. Add a downloadable syllabus link showing the file type and size.
4. Add a video with captions and a transcript.

## Interview Questions and Solutions

### Why use semantic HTML instead of many `div` elements?

Semantic elements communicate structure to browsers, assistive technology, search engines, and developers without custom scripts or ARIA.

### Why is a placeholder not a label?

A placeholder disappears during entry, may have low contrast, and does not reliably provide a persistent accessible instruction. Use a visible `label`.

### Why use `scope` on table headers?

It explicitly associates header cells with their row or column, helping screen readers announce context.

### When should a form use GET instead of POST?

Use GET for safe, bookmarkable retrieval such as search. Use POST for state changes or data that should not appear in a URL. A real registration endpoint normally uses HTTPS and POST; GET is used here because a static server cannot process POST.

### What is progressive enhancement?

Start with functional semantic HTML, then add CSS and JavaScript without making the basic task depend on them.

## Completion Definition

The project is complete when both pages validate, every control works by keyboard, native validation blocks invalid submissions, a valid submission reaches the confirmation page, and you can explain the interview answers without reading them.

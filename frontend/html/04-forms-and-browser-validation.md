# 04 - Forms and Browser Validation

## What Is a Form?

A form collects named values and submits them to a server or JavaScript handler.

```html
<form action="/register" method="post">
  <label for="name">Name</label>
  <input id="name" name="name" required minlength="2">

  <label for="email">Email</label>
  <input id="email" name="email" type="email" autocomplete="email" required>

  <button type="submit">Create account</button>
</form>
<!-- Browser result: empty or invalid fields block submission and show browser validation messages. -->
```

Only successful controls with a `name` are submitted.

## GET vs POST

- GET places query data in the URL; use for safe searches/filters.
- POST places data in the request body; use for creation or commands.

Never send passwords or secrets in URLs. HTTPS is required for sensitive forms.

## Input Types

```html
<input type="search" name="query">
<input type="number" name="quantity" min="1" max="10" step="1">
<input type="date" name="startDate">
<input type="file" name="resume" accept=".pdf,application/pdf">
<!-- Browser result: purpose-specific controls and mobile keyboards where supported. -->
```

Browser UI varies by operating system and browser. The server must validate every value again.

## Grouping Controls

```html
<fieldset>
  <legend>Preferred contact</legend>
  <label><input type="radio" name="contact" value="email" required> Email</label>
  <label><input type="radio" name="contact" value="phone"> Phone</label>
</fieldset>
<!-- Browser result: one labeled radio group where only one option can be selected. -->
```

Checkboxes allow independent selections. Radios with the same `name` form one choice group.

## Select and Text Area

```html
<label for="level">Experience level</label>
<select id="level" name="level" required>
  <option value="">Choose a level</option>
  <option value="beginner">Beginner</option>
</select>

<label for="message">Message</label>
<textarea id="message" name="message" maxlength="500"></textarea>
<!-- Browser result: required dropdown plus multiline text limited to 500 characters. -->
```

## Validation and Errors

- HTML validation improves immediate feedback
- JavaScript can improve interaction, not establish trust
- server validation is always required
- errors should identify the field and explain how to fix it
- preserve valid user input after a server error
- announce dynamic errors using a suitable live region

```html
<p id="email-error" role="alert">Enter a valid email address.</p>
<input aria-describedby="email-error" aria-invalid="true" type="email">
<!-- Accessibility result: the field exposes its invalid state and associated error. -->
```

## Security

Use CSRF protection for cookie-authenticated state changes, encode output to prevent XSS, limit uploads by type/size/content, and never trust `accept`, `required`, `min`, or other client-side attributes as security controls.

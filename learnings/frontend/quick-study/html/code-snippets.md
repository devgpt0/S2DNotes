# HTML: 3 commonly asked coding questions

Try each question before reading the model answer. Complete browser-ready versions are in [`examples`](examples/).

```powershell
python -m http.server 8000 --directory frontend/quick-study/html/examples
```

Open `/01-accessible-signup/`, `/02-semantic-article/`, or `/03-comparison-table/` at <http://localhost:8000>. No package installation is required.

For a complete local page containing all required HTML, styling, and demo behavior, follow [the runnable example guide](./examples/README.md).

## 1. Build an accessible sign-up form

**Question:** Create name, email, password, plan, terms, and submit controls. Use native validation and accessible labels.

```html
<form action="/signup" method="post">
  <fieldset>
    <legend>Create your account</legend>

    <label for="name">Full name</label>
    <input id="name" name="name" autocomplete="name" required />

    <label for="email">Email</label>
    <input id="email" name="email" type="email" autocomplete="email" required />

    <label for="password">Password</label>
    <input id="password" name="password" type="password" autocomplete="new-password" minlength="8" required />

    <label for="plan">Plan</label>
    <select id="plan" name="plan" required>
      <option value="">Choose a plan</option>
      <option value="starter">Starter</option>
      <option value="pro">Pro</option>
    </select>

    <label><input name="terms" type="checkbox" required /> I accept the terms</label>
    <button type="submit">Create account</button>
  </fieldset>
</form>
```

## 2. Mark up a semantic article page

**Question:** Create a page with navigation, main article, related links, publication date, and footer. Make the hierarchy understandable without CSS.

```html
<header>
  <a href="#content">Skip to main content</a>
  <nav aria-label="Primary"><a href="/">Home</a> <a href="/articles">Articles</a></nav>
</header>
<main id="content">
  <article>
    <header>
      <h1>How browsers render a page</h1>
      <p>Published <time datetime="2026-07-28">28 July 2026</time></p>
    </header>
    <section aria-labelledby="parsing-heading">
      <h2 id="parsing-heading">Parsing HTML</h2>
      <p>The browser turns markup into a DOM tree.</p>
    </section>
  </article>
  <aside aria-labelledby="related-heading">
    <h2 id="related-heading">Related reading</h2>
    <a href="/css">CSS rendering</a>
  </aside>
</main>
<footer><p>&copy; 2026 Web Notes</p></footer>
```

## 3. Build an accessible product comparison table

**Question:** Mark up plan features so screen-reader users can understand row and column relationships.

```html
<table>
  <caption>Plan comparison per month</caption>
  <thead>
    <tr><th scope="col">Feature</th><th scope="col">Starter</th><th scope="col">Pro</th></tr>
  </thead>
  <tbody>
    <tr><th scope="row">Projects</th><td>3</td><td>Unlimited</td></tr>
    <tr><th scope="row">Support</th><td>Email</td><td>Priority</td></tr>
    <tr><th scope="row">Price</th><td>₹499</td><td>₹999</td></tr>
  </tbody>
</table>
```

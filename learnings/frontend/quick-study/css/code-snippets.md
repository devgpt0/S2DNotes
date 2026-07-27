# CSS: 3 commonly asked coding questions

Complete examples include the required HTML, CSS, and dropdown JavaScript in [`examples`](examples/).

```powershell
python -m http.server 8001 --directory frontend/quick-study/css/examples
```

Open `/01-centered-card/`, `/02-responsive-grid/`, or `/03-accessible-dropdown/` at <http://localhost:8001>. No package installation is required.

For complete HTML and CSS that can be run immediately, follow [the runnable example guide](./examples/README.md).

## 1. Center a card in the viewport

**Question:** Center a card horizontally and vertically without absolute positioning.

```css
body {
  min-height: 100vh;
  margin: 0;
  display: grid;
  place-items: center;
}

.card {
  width: min(90%, 30rem);
  padding: 1.5rem;
  border: 1px solid #d1d5db;
  border-radius: 0.75rem;
}
```

## 2. Build a responsive card grid

**Question:** Show as many cards as fit, with no device-specific breakpoints, and collapse naturally to one column.

```css
* { box-sizing: border-box; }

.cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(16rem, 100%), 1fr));
  gap: 1rem;
}

.card {
  padding: 1rem;
  border: 1px solid #d1d5db;
  border-radius: 0.5rem;
}
```

## 3. Build an accessible dropdown menu state

**Question:** Show a submenu on keyboard focus and mouse hover without removing focus indication.

```css
.menu-item { position: relative; }
.submenu {
  display: none;
  position: absolute;
  inset-block-start: 100%;
  inset-inline-start: 0;
  min-width: 12rem;
  padding: 0.5rem;
  background: white;
  border: 1px solid #d1d5db;
}

.menu-item:hover .submenu,
.menu-item:focus-within .submenu { display: block; }

.menu-item a:focus-visible {
  outline: 3px solid #2563eb;
  outline-offset: 2px;
}
```

In production, JavaScript should also manage the trigger’s `aria-expanded` state and Escape-key behavior.

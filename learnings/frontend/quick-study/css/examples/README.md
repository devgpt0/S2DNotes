# Run the CSS examples

This page demonstrates centering, a responsive card grid, and a keyboard-accessible dropdown state.

```text
examples/
├── 01-centered-card/
├── 02-responsive-grid/
├── 03-accessible-dropdown/
├── README.md
├── index.html              # Runs all three examples together
└── styles.css
```

From the repository root:

```powershell
python -m http.server 8001 --directory frontend/quick-study/css/examples
```

Open `http://localhost:8001`. Resize the browser and use Tab to test the examples.

Open a numbered folder from the directory listing to run only that interview question.

# Run the HTML examples

This page demonstrates the accessible sign-up form, semantic article, and product comparison table.

```text
examples/
├── 01-accessible-signup/
├── 02-semantic-article/
├── 03-comparison-table/
├── README.md
├── index.html              # Runs all three examples together
└── styles.css
```

From the repository root:

```powershell
python -m http.server 8000 --directory frontend/quick-study/html/examples
```

Open `http://localhost:8000`. Submit the form to see native HTML validation.
The demo intentionally prevents a real network submission.

Open a numbered folder from the directory listing to run only that interview question.

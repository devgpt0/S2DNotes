# Run the quick-study examples

Every topic contains a runnable application showing all three coding-interview examples. HTML, CSS, and JavaScript also include one standalone folder per question. No source code needs to be added before running them.

## Folder structure

```text
quick-study/
├── html/examples/          # Combined page plus 3 standalone examples
├── css/examples/           # Combined page plus 3 standalone examples
├── javascript/examples/    # Combined page plus 3 standalone examples
├── typescript/examples/    # Vite + TypeScript project
└── react/examples/         # Vite + React + TypeScript project
```

## HTML, CSS, and JavaScript

Run any one of these commands from `frontend/quick-study`:

```powershell
# HTML
python -m http.server 8000 --directory html/examples

# CSS
python -m http.server 8001 --directory css/examples

# JavaScript
python -m http.server 8002 --directory javascript/examples
```

Open the URL printed in the terminal, such as `http://localhost:8000`. Press `Ctrl+C` to stop the server.

## TypeScript

```powershell
cd frontend/quick-study/typescript/examples
npm.cmd install
npm.cmd run dev
```

Open the URL printed by Vite. Run `npm.cmd run build` to type-check and create
a production build.

## React

```powershell
cd frontend/quick-study/react/examples
npm.cmd install
npm.cmd run dev
```

Open the URL printed by Vite. Run `npm.cmd run build` to type-check and create
a production build.

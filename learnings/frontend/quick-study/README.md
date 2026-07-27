# Frontend quick-study

Each topic contains notes, MCQs, interview questions, code questions, and runnable examples.

## Runnable example structure

```text
quick-study/
├── html/examples/
│   ├── 01-accessible-signup/
│   ├── 02-semantic-article/
│   └── 03-comparison-table/
├── css/examples/
│   ├── 01-centered-card/
│   ├── 02-responsive-grid/
│   └── 03-accessible-dropdown/
├── javascript/examples/
│   ├── 01-debounce/
│   ├── 02-flatten-array/
│   └── 03-group-by/
├── typescript/examples/
│   ├── package.json
│   ├── tsconfig.json
│   └── src/01-*.ts, 02-*.ts, 03-*.ts
└── react/examples/
    ├── package.json
    ├── index.html
    └── src/
```

Run commands from the repository root: `C:\pocs\notes\learnings`.

## HTML examples

```powershell
python -m http.server 8000 --directory frontend/quick-study/html/examples
```

Open:

- <http://localhost:8000/01-accessible-signup/>
- <http://localhost:8000/02-semantic-article/>
- <http://localhost:8000/03-comparison-table/>

## CSS examples

```powershell
python -m http.server 8001 --directory frontend/quick-study/css/examples
```

Open:

- <http://localhost:8001/01-centered-card/>
- <http://localhost:8001/02-responsive-grid/>
- <http://localhost:8001/03-accessible-dropdown/>

## JavaScript examples

```powershell
python -m http.server 8002 --directory frontend/quick-study/javascript/examples
```

Open:

- <http://localhost:8002/01-debounce/>
- <http://localhost:8002/02-flatten-array/>
- <http://localhost:8002/03-group-by/>

Stop any local server with `Ctrl+C` in its terminal.

## TypeScript examples

Node.js 20 or newer is required.

```powershell
cd frontend/quick-study/typescript/examples
npm.cmd install
npm.cmd run check
npm.cmd run examples
```

Run only one example with `npm.cmd run example:1`, `npm.cmd run example:2`, or `npm.cmd run example:3`. Results appear in the terminal.

## React examples

Node.js 20 or newer is required.

```powershell
cd frontend/quick-study/react/examples
npm.cmd install
npm.cmd run dev
```

Open the local URL printed by Vite, normally <http://localhost:5173>. The page displays all three interactive React examples. Verify a production build with:

```powershell
npm.cmd run build
```

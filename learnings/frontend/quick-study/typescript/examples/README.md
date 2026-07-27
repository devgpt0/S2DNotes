# Run the TypeScript examples

This project demonstrates a type-safe property getter, exhaustive request
states, and validation of unknown API data.

```text
examples/
├── src/
│   ├── main.ts
│   ├── 01-property-getter.ts
│   ├── 02-request-state.ts
│   ├── 03-validate-api-data.ts
│   └── styles.css
├── .gitignore
├── index.html
├── package.json
├── README.md
└── tsconfig.json
```

From the repository root:

```powershell
cd frontend/quick-study/typescript/examples
npm.cmd install
npm.cmd run dev
```

Open the URL printed by Vite. To verify strict types and create a production bundle:

```powershell
npm.cmd run build
```

To run the three interview snippets directly in the terminal:

```powershell
npm.cmd run examples
```

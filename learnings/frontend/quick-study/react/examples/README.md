# Run the React examples

This project demonstrates functional state updates, an immutable todo list,
and a reusable debounced-value hook.

```text
examples/
├── src/
│   ├── App.tsx
│   ├── main.tsx
│   └── styles.css
├── .gitignore
├── index.html
├── package.json
├── README.md
├── tsconfig.json
└── vite.config.ts
```

From the repository root:

```powershell
cd frontend/quick-study/react/examples
npm.cmd install
npm.cmd run dev
```

Open the URL printed by Vite. To verify strict types and create a production bundle:

```powershell
npm.cmd run build
```

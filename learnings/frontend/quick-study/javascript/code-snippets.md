# JavaScript: 3 commonly asked coding questions

Complete browser pages with visible output are in [`examples`](examples/).

```powershell
python -m http.server 8002 --directory frontend/quick-study/javascript/examples
```

Open `/01-debounce/`, `/02-flatten-array/`, or `/03-group-by/` at <http://localhost:8002>. No package installation is required.

For a complete page with inputs and visible results, follow [the runnable example guide](./examples/README.md).

## 1. Implement debounce

**Question:** Return a function that runs `callback` only after calls stop for `delay` milliseconds while preserving `this` and arguments.

```js
function debounce(callback, delay) {
  let timeoutId;

  return function (...args) {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => callback.apply(this, args), delay);
  };
}

const search = debounce((query) => console.log(`Searching: ${query}`), 300);
search("rea");
search("react"); // only this call runs
```

## 2. Flatten a nested array without `flat`

**Question:** Flatten an arbitrarily nested array without mutating the input.

```js
function flatten(values) {
  return values.reduce(
    (result, value) => result.concat(Array.isArray(value) ? flatten(value) : value),
    [],
  );
}

console.log(flatten([1, [2, [3, 4]], 5])); // [1, 2, 3, 4, 5]
```

Time is O(n) for visited values; repeated `concat` allocations can be costly for huge input. An accumulator-based version is preferable at that scale.

## 3. Group objects by a property

**Question:** Convert an array into an object whose keys contain arrays of matching items.

```js
function groupBy(items, getKey) {
  return items.reduce((groups, item) => {
    const key = getKey(item);
    (groups[key] ??= []).push(item);
    return groups;
  }, Object.create(null));
}

const people = [
  { name: "Asha", team: "web" },
  { name: "Ben", team: "api" },
  { name: "Chen", team: "web" },
];

console.log(groupBy(people, (person) => person.team));
```

`Object.create(null)` avoids inherited special property names. Use a `Map` when keys are not strings.

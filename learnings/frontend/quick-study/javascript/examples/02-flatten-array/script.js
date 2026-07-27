"use strict";

function flatten(values) {
  return values.reduce(
    (result, value) => result.concat(Array.isArray(value) ? flatten(value) : value),
    [],
  );
}

const runButton = document.querySelector("#run");
const result = document.querySelector("#result");
if (!(runButton instanceof HTMLButtonElement) || !(result instanceof HTMLElement)) {
  throw new Error("Required demo elements were not found");
}

runButton.addEventListener("click", () => {
  result.textContent = JSON.stringify(flatten([1, [2, [3, 4]], 5]));
});

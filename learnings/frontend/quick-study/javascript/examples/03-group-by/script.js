"use strict";

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

const runButton = document.querySelector("#run");
const result = document.querySelector("#result");
if (!(runButton instanceof HTMLButtonElement) || !(result instanceof HTMLElement)) {
  throw new Error("Required demo elements were not found");
}

runButton.addEventListener("click", () => {
  result.textContent = JSON.stringify(groupBy(people, (person) => person.team), null, 2);
});

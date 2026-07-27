"use strict";

function debounce(callback, delay) {
  let timeoutId;
  return function (...args) {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => callback.apply(this, args), delay);
  };
}

function flatten(values) {
  return values.reduce(
    (result, value) => result.concat(Array.isArray(value) ? flatten(value) : value),
    [],
  );
}

function groupBy(items, getKey) {
  return items.reduce((groups, item) => {
    const key = getKey(item);
    (groups[key] ??= []).push(item);
    return groups;
  }, Object.create(null));
}

const searchInput = document.querySelector("#search");
const debounceOutput = document.querySelector("#debounce-output");
const flattenOutput = document.querySelector("#flatten-output");
const groupOutput = document.querySelector("#group-output");

if (!searchInput || !debounceOutput || !flattenOutput || !groupOutput) {
  throw new Error("Required example element is missing");
}

const showSearch = debounce((query) => {
  debounceOutput.textContent = query ? `Searching for “${query}”` : "Waiting for input";
}, 500);

searchInput.addEventListener("input", (event) => {
  if (!(event.target instanceof HTMLInputElement)) return;
  debounceOutput.textContent = "Typing…";
  showSearch(event.target.value.trim());
});

flattenOutput.textContent = JSON.stringify(flatten([1, [2, [3, 4]], 5]));

const people = [
  { name: "Asha", team: "web" },
  { name: "Ben", team: "api" },
  { name: "Chen", team: "web" },
];
groupOutput.textContent = JSON.stringify(groupBy(people, (person) => person.team), null, 2);

"use strict";

function debounce(callback, delay) {
  let timeoutId;
  return function (...args) {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => callback.apply(this, args), delay);
  };
}

const search = document.querySelector("#search");
const result = document.querySelector("#result");
if (!(search instanceof HTMLInputElement) || !(result instanceof HTMLParagraphElement)) {
  throw new Error("Required demo elements were not found");
}

const showSearch = debounce((query) => {
  result.textContent = query ? `Searching for “${query}”` : "Waiting for input…";
}, 500);

search.addEventListener("input", () => showSearch(search.value.trim()));

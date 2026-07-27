"use strict";

const form = document.querySelector("#signup-form");
const result = document.querySelector("#result");

if (!(form instanceof HTMLFormElement) || !(result instanceof HTMLParagraphElement)) {
  throw new Error("Required form elements were not found");
}

form.addEventListener("submit", (event) => {
  event.preventDefault();
  result.textContent = "Form is valid and ready to submit.";
  result.hidden = false;
});

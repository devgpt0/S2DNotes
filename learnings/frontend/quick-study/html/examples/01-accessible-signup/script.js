"use strict";

const form = document.querySelector("#signup-form");
const result = document.querySelector("#result");

if (
  !(form instanceof HTMLFormElement) ||
  !(result instanceof HTMLParagraphElement)
) {
  throw new Error("Required form elements were not found");
}

form.addEventListener("submit", (event) => {
  event.preventDefault();
  const data = new FormData(form);
  result.textContent = `Demo submitted for ${String(data.get("name"))} on the ${String(data.get("plan"))} plan.`;
  result.hidden = false;
});

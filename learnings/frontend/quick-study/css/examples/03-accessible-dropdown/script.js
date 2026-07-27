"use strict";

const button = document.querySelector("#menu-button");
const submenu = document.querySelector("#submenu");

if (!(button instanceof HTMLButtonElement) || !(submenu instanceof HTMLUListElement)) {
  throw new Error("Required menu elements were not found");
}

function setOpen(isOpen) {
  button.setAttribute("aria-expanded", String(isOpen));
  submenu.hidden = !isOpen;
}

button.addEventListener("click", () => setOpen(button.getAttribute("aria-expanded") !== "true"));
document.addEventListener("keydown", (event) => {
  if (event.key !== "Escape") return;
  setOpen(false);
  button.focus();
});

export function announceToScreenReader(message: string): void {
  const el = document.createElement("div");
  el.setAttribute("aria-live", "polite");
  el.setAttribute("aria-atomic", "true");
  el.className = "sr-only";
  el.textContent = message;
  document.body.appendChild(el);
  setTimeout(() => {
    if (document.body.contains(el)) {
      document.body.removeChild(el);
    }
  }, 1000);
}

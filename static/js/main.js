/* =========================
   Signal Ridge Systems
   Main JavaScript
   =========================
   Handles progressive enhancements:
   - Scroll reveal animations
   - Staggered section entry
   - Safe fallback for older browsers
   ========================= */

document.addEventListener("DOMContentLoaded", () => {
  /* =========================
     Scroll Reveal
     Adds .is-visible when a .reveal section enters the viewport.
     CSS handles the actual animation.
     ========================= */

  const revealItems = document.querySelectorAll(".reveal");

  // If there are no reveal elements on the page, do nothing.
  if (!revealItems.length) return;

  // Respect users who prefer reduced motion.
  const prefersReducedMotion = window.matchMedia(
    "(prefers-reduced-motion: reduce)"
  ).matches;

  if (prefersReducedMotion) {
    revealItems.forEach((item) => item.classList.add("is-visible"));
    return;
  }

  // Fallback for older browsers without IntersectionObserver support.
  if (!("IntersectionObserver" in window)) {
    revealItems.forEach((item) => item.classList.add("is-visible"));
    return;
  }

  const revealObserver = new IntersectionObserver(
    (entries, observer) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;

        entry.target.classList.add("is-visible");
        observer.unobserve(entry.target);
      });
    },
    {
      threshold: 0.14,
      rootMargin: "0px 0px -80px 0px",
    }
  );

  revealItems.forEach((item) => revealObserver.observe(item));
});
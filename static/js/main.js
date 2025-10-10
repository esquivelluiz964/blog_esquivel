document.addEventListener("DOMContentLoaded", () => {
  console.debug("Luiz Esquivel site script — running beautifully ✨");

  // Efeito fade-in em todos os blocos principais
  const fadeEls = document.querySelectorAll(".fade-in");
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((e) => {
      if (e.isIntersecting) e.target.classList.add("visible");
    });
  }, { threshold: 0.2 });
  fadeEls.forEach((el) => observer.observe(el));
});

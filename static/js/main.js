document.addEventListener("DOMContentLoaded", () => {
  const mobileMenuBtn = document.getElementById("mobile-menu-btn");
  const mobileNav = document.getElementById("mobile-nav");

  if (mobileMenuBtn && mobileNav) {
    mobileMenuBtn.addEventListener("click", () => {
      mobileNav.classList.toggle("show");
    });
  }

  // Close mobile menu when clicking outside
  document.addEventListener("click", (event) => {
    if (
      mobileNav &&
      mobileNav.classList.contains("show") &&
      !mobileNav.contains(event.target) &&
      !mobileMenuBtn.contains(event.target)
    ) {
      mobileNav.classList.remove("show");
    }
  });
});

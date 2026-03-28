// Subtle fade-in animation
document.addEventListener("DOMContentLoaded", function () {
  document.querySelector(".login-card").style.opacity = "0";
  document.querySelector(".login-card").style.transform = "translateY(20px)";

  setTimeout(() => {
    document.querySelector(".login-card").style.transition = "all 0.6s ease";
    document.querySelector(".login-card").style.opacity = "1";
    document.querySelector(".login-card").style.transform = "translateY(0)";
  }, 200);
});

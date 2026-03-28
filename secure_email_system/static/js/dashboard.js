// Subtle animation for cards
document.addEventListener("DOMContentLoaded", () => {
  const cards = document.querySelectorAll(".stat-card");

  cards.forEach((card, index) => {
    card.style.opacity = "0";
    card.style.transform = "translateY(20px)";

    setTimeout(() => {
      card.style.transition = "all 0.5s ease";
      card.style.opacity = "1";
      card.style.transform = "translateY(0)";
    }, 200 * index);
  });
});

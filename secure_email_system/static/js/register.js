const passwordInput = document.getElementById("password");
const strengthBar = document.getElementById("strength-bar");
const strengthText = document.getElementById("strength-text");

passwordInput.addEventListener("input", function () {
  const value = passwordInput.value;
  let strength = 0;

  if (value.length >= 6) strength++;
  if (value.match(/[A-Z]/)) strength++;
  if (value.match(/[0-9]/)) strength++;
  if (value.match(/[^A-Za-z0-9]/)) strength++;

  switch (strength) {
    case 0:
      strengthBar.style.width = "0%";
      strengthText.innerText = "";
      break;
    case 1:
      strengthBar.style.width = "25%";
      strengthBar.style.background = "red";
      strengthText.innerText = "Weak";
      break;
    case 2:
      strengthBar.style.width = "50%";
      strengthBar.style.background = "orange";
      strengthText.innerText = "Moderate";
      break;
    case 3:
      strengthBar.style.width = "75%";
      strengthBar.style.background = "#3b82f6";
      strengthText.innerText = "Strong";
      break;
    case 4:
      strengthBar.style.width = "100%";
      strengthBar.style.background = "#00f5d4";
      strengthText.innerText = "Very Strong";
      break;
  }
});

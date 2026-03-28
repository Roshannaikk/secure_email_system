const messageBox = document.getElementById("messageBox");
const charCount = document.getElementById("charCount");

messageBox.addEventListener("input", () => {
  charCount.innerText = messageBox.value.length + " characters";
});

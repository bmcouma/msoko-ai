const form = document.getElementById("chat-form");
const input = document.getElementById("user-input");
const chatbox = document.getElementById("chatbox");

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const userText = input.value.trim();
  if (!userText) {
    input.focus();
    return;
  }

  appendMessage("user", userText);
  input.value = "";

  appendMessage("ai", "Typing...");

  try {
    const response = await fetch("http://127.0.0.1:8000/api/chat/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message: userText }),
    });

    const data = await response.json();
    console.log("Response:", data);

    const reply = data.response || data.reply || "Sorry, I didn’t catch that.";
    chatbox.removeChild(chatbox.lastChild);
    appendMessage("ai", reply);
  } catch (err) {
    console.error("Error fetching response:", err);
    chatbox.removeChild(chatbox.lastChild);
    appendMessage("ai", "Something went wrong. Try again later.");
  }
});

function appendMessage(sender, text) {
  const messageDiv = document.createElement("div");
  messageDiv.classList.add("message", sender);
  messageDiv.textContent = text;
  chatbox.appendChild(messageDiv);
  chatbox.scrollTop = chatbox.scrollHeight;
}

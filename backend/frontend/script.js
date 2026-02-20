const form = document.getElementById("chat-form");
const input = document.getElementById("user-input");
const chatbox = document.getElementById("chatbox");
const sendBtn = document.getElementById("send-btn");
const newChatBtn = document.getElementById("new-chat-btn");
const copyChatBtn = document.getElementById("copy-chat-btn");
const statusDot = document.getElementById("status-dot");
const statusText = document.getElementById("status-text");
const quickChips = document.getElementById("quick-chips");

// Get API URL from environment or use default
const API_URL = window.API_URL || "http://127.0.0.1:8000/api/chat/";
const STORAGE_KEY = "msoko_chat_history";

const quickPrompts = [
  "Price my mitumba stock for Nairobi CBD",
  "Boost sales on slow weekdays",
  "How to keep cashflow steady?",
  "Low-cost marketing ideas for boda service",
  "Customer care tips for kiosk owners",
  "Should I give credit? How to manage it safely?"
];

let history = [];

init();

function init() {
  renderQuickPrompts();
  loadHistory();
  input.focus();
}

function renderQuickPrompts() {
  quickChips.innerHTML = "";
  quickPrompts.forEach(prompt => {
    const chip = document.createElement("button");
    chip.type = "button";
    chip.className = "chip";
    chip.textContent = prompt;
    chip.addEventListener("click", () => {
      input.value = prompt;
      input.focus();
      form.dispatchEvent(new Event("submit"));
    });
    quickChips.appendChild(chip);
  });
}

function loadHistory() {
  try {
    const saved = JSON.parse(localStorage.getItem(STORAGE_KEY) || "[]");
    history = Array.isArray(saved) ? saved : [];
  } catch {
    history = [];
  }

  // If empty, seed welcome message
  if (history.length === 0) {
    history.push({ role: "ai", content: "Habari! I’m here to help with pricing, marketing, cash flow, and growth. Ask anything about your hustle. 💪" });
  }

  chatbox.innerHTML = "";
  history.forEach(msg => appendMessage(msg.role, msg.content, { persist: false }));
}

function saveHistory() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(history));
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const userText = input.value.trim();
  if (!userText) {
    input.focus();
    return;
  }

  setBusy(true);

  appendMessage("user", userText);
  input.value = "";

  const typingMessage = appendMessage("ai", null, { typing: true, persist: false });

  try {
    const response = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: userText }),
    });

    updateStatus(response.ok);

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }

    const data = await response.json();
    const reply = data.response || data.reply || data.error || "Sorry, I didn't catch that. Please try again.";

    removeNode(typingMessage);
    appendMessage("ai", reply);
  } catch (err) {
    console.error("Error fetching response:", err);
    updateStatus(false);
    removeNode(typingMessage);

    let errorMessage = "Something went wrong. ";
    if (err.message.includes("Failed to fetch") || err.message.includes("NetworkError")) {
      errorMessage += "Please check your connection and make sure the backend server is running.";
    } else {
      errorMessage += err.message;
    }
    appendMessage("ai", errorMessage);
    history.push({ role: "ai", content: errorMessage });
    saveHistory();
  } finally {
    setBusy(false);
  }
});

newChatBtn.addEventListener("click", () => {
  history = [];
  saveHistory();
  loadHistory();
});

copyChatBtn.addEventListener("click", () => {
  const plain = history.map(h => `${h.role === "user" ? "You" : "Msoko AI"}: ${h.content}`).join("\n\n");
  navigator.clipboard.writeText(plain).then(() => {
    copyChatBtn.textContent = "Copied!";
    setTimeout(() => (copyChatBtn.textContent = "Copy chat"), 1200);
  }).catch(() => {
    alert("Could not copy chat. Please try again.");
  });
});

function appendMessage(sender, text, { typing = false, persist = true } = {}) {
  const wrapper = document.createElement("div");
  wrapper.classList.add("message", sender);

  const avatar = document.createElement("div");
  avatar.className = "avatar";
  avatar.textContent = sender === "user" ? "🧑" : "🤖";

  const bubble = document.createElement("div");
  bubble.className = "bubble";

  const meta = document.createElement("div");
  meta.className = "meta";
  meta.textContent = sender === "user" ? "You" : "Msoko AI · Coach";

  const content = document.createElement("div");
  content.className = "content";

  if (typing) {
    const dots = document.createElement("div");
    dots.className = "typing-indicator";
    dots.innerHTML = `<span class="dot-typing"></span><span class="dot-typing"></span><span class="dot-typing"></span>`;
    content.appendChild(dots);
  } else if (sender === "ai") {
    content.innerHTML = renderMarkdown(text || "");
  } else {
    content.textContent = text;
  }

  bubble.appendChild(meta);
  bubble.appendChild(content);

  if (sender === "user") {
    wrapper.appendChild(bubble);
    wrapper.appendChild(avatar);
  } else {
    wrapper.appendChild(avatar);
    wrapper.appendChild(bubble);
  }

  chatbox.appendChild(wrapper);
  chatbox.scrollTop = chatbox.scrollHeight;

  if (persist && text) {
    history.push({ role: sender, content: text });
    saveHistory();
  }

  return wrapper;
}

function renderMarkdown(text) {
  if (typeof marked === "undefined" || typeof DOMPurify === "undefined") {
    return escapeHtml(text);
  }
  const html = marked.parse(text);
  return DOMPurify.sanitize(html);
}

function escapeHtml(text) {
  const div = document.createElement("div");
  div.textContent = text;
  return div.innerHTML;
}

function removeNode(node) {
  if (node && node.parentNode) {
    node.parentNode.removeChild(node);
  }
}

function setBusy(isBusy) {
  input.disabled = isBusy;
  sendBtn.disabled = isBusy;
  sendBtn.textContent = isBusy ? "Sending..." : "Send";
  if (!isBusy) input.focus();
}

function updateStatus(isOnline) {
  if (!statusDot || !statusText) return;
  statusDot.classList.toggle("offline", !isOnline);
  statusText.textContent = isOnline ? "Online" : "Offline";
}

// Allow Enter key to submit (Shift+Enter for new line)
input.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    form.dispatchEvent(new Event("submit"));
  }
});

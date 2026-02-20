/**
 * Msoko AI - Professional Modern Frontend Logic
 */

document.addEventListener("DOMContentLoaded", () => {
  const userInput = document.getElementById("user-input");
  const sendBtn = document.getElementById("send-btn");
  const chatArea = document.getElementById("chat-area");
  const messageList = document.getElementById("message-list");
  const welcomeScreen = document.getElementById("welcome-screen");
  const suggestionCards = document.querySelectorAll(".suggestion-card");
  const newChatBtn = document.getElementById("new-chat-btn");
  const dashboardBtn = document.getElementById("dashboard-btn");
  const profileBtn = document.getElementById("profile-btn");
  const statusDot = document.getElementById("status-dot");
  const statusText = document.getElementById("status-text");

  let history = [];
  let currentThreadId = null;
  let recognition = null;
  let isRecording = false;
  let selectedImage = null;

  // INITIAL LOAD
  loadThreads();
  initVoice();
  initImage();

  dashboardBtn.addEventListener("click", showDashboard);
  profileBtn.addEventListener("click", showProfile);

  async function showDashboard() {
    try {
        const res = await fetch("/api/dashboard/");
        const data = await res.json();
        
        const content = `
            <div class="dashboard-header">
                <h3><i class="fas fa-chart-line"></i> Strategic Dashboard</h3>
                <p>Performance insights for ${data.business_name}</p>
            </div>
            <div class="stats-grid">
                <div class="stat-card">
                    <label>Consultations</label>
                    <div class="stat-value">${data.stats.consultations}</div>
                </div>
                <div class="stat-card">
                    <label>Messages</label>
                    <div class="stat-value">${data.stats.total_messages}</div>
                </div>
                <div class="stat-card">
                    <label>Target</label>
                    <div class="stat-value">${data.stats.revenue_target || '—'}</div>
                </div>
            </div>
            
            <div class="goals-section">
                <div class="section-header">
                    <h4>Active Goals</h4>
                    <button class="add-goal-btn" id="add-goal-btn"><i class="fas fa-plus"></i></button>
                </div>
                <div class="goals-list">
                    ${data.goals.length ? data.goals.map(g => `
                        <div class="goal-item">
                            <div class="goal-info">
                                <span>${g.title}</span>
                                <span>${g.progress}%</span>
                            </div>
                            <div class="progress-bar">
                                <div class="progress-fill" style="width: ${g.progress}%"></div>
                            </div>
                        </div>
                    `).join('') : '<p class="empty-text">No active goals. Set one to start tracking!</p>'}
                </div>
            </div>

            <div class="insights-list" style="margin-top: 20px;">
                <h4>Mama Msoko's Insights</h4>
                <ul class="insight-ul">
                    ${data.recent_insights.map(i => `<li><i class="fas fa-magic"></i> ${i}</li>`).join('')}
                </ul>
            </div>
        `;
        showOverlay(content);
        document.getElementById("add-goal-btn").onclick = showAddGoalForm;
    } catch (e) { console.error(e); }
  }

  function showAddGoalForm() {
      const content = `
          <div class="dashboard-header">
              <h3><i class="fas fa-bullseye"></i> Set a New Goal</h3>
              <p>What milestone are we hitting next?</p>
          </div>
          <form id="goal-form" class="profile-form">
              <div class="form-group">
                  <label>Goal Title (e.g., Save for new fridge)</label>
                  <input type="text" name="title" placeholder="Enter title..." required>
              </div>
              <div class="form-group">
                  <label>Goal Type</label>
                  <select name="goal_type">
                      <option value="revenue">Revenue Target</option>
                      <option value="inventory">Inventory Milestone</option>
                      <option value="savings">Savings Goal</option>
                  </select>
              </div>
              <div class="form-group">
                  <label>Target Value (KES)</label>
                  <input type="number" name="target_value" value="1000" required>
              </div>
              <div class="form-group">
                  <label>Deadline</label>
                  <input type="date" name="deadline">
              </div>
              <button type="submit" class="save-btn">Create Goal</button>
          </form>
      `;
      showOverlay(content);

      document.getElementById("goal-form").onsubmit = async (e) => {
          e.preventDefault();
          const formData = new FormData(e.target);
          const payload = Object.fromEntries(formData.entries());
          payload.current_value = 0; // Start at 0
          
          await fetch("/api/goals/", {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify(payload)
          });
          showDashboard(); // Reload dashboard
          alert("Goal set! Mama Msoko is watching your progress. 🚀");
      };
  }

  async function showProfile() {
    try {
        const res = await fetch("/api/profile/");
        const data = await res.json();
        
        const content = `
            <div class="dashboard-header">
                <h3><i class="fas fa-store"></i> Business Profile</h3>
                <p>Personalize your coaching experience.</p>
            </div>
            <form id="profile-form" class="profile-form">
                <div class="form-group">
                    <label>Business Name</label>
                    <input type="text" name="business_name" value="${data.business_name || ''}">
                </div>
                <div class="form-group">
                    <label>Sector</label>
                    <select name="sector">
                        <option value="retail" ${data.sector==='retail' ? 'selected':''}>Retail / Kiosk</option>
                        <option value="services" ${data.sector==='services' ? 'selected':''}>Services</option>
                        <option value="wholesale" ${data.sector==='wholesale' ? 'selected':''}>Wholesale</option>
                        <option value="agri" ${data.sector==='agri' ? 'selected':''}>Agribusiness</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Location</label>
                    <input type="text" name="location" value="${data.location || ''}">
                </div>
                <button type="submit" class="save-btn">Save Hustle Details</button>
            </form>
        `;
        showOverlay(content);

        document.getElementById("profile-form").onsubmit = async (e) => {
            e.preventDefault();
            const formData = new FormData(e.target);
            const payload = Object.fromEntries(formData.entries());
            await fetch("/api/profile/", {
                method: "PATCH",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            });
            hideOverlay();
            alert("Mama Msoko updated your profile! 🚀");
        };
    } catch (e) { console.error(e); }
  }

  function showOverlay(content) {
      const overlay = document.createElement("div");
      overlay.className = "modal-overlay";
      overlay.innerHTML = `
        <div class="modal-content">
            <button class="close-modal">&times;</button>
            ${content}
        </div>
      `;
      document.body.appendChild(overlay);
      overlay.querySelector(".close-modal").onclick = hideOverlay;
      overlay.onclick = (e) => { if(e.target === overlay) hideOverlay(); };
  }

  function hideOverlay() {
      const overlay = document.querySelector(".modal-overlay");
      if(overlay) overlay.remove();
  }

  function initImage() {
    const attachBtn = document.getElementById("attach-btn");
    const imageInput = document.getElementById("image-input");

    attachBtn.addEventListener("click", () => imageInput.click());

    imageInput.addEventListener("change", (e) => {
      const file = e.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = (ev) => {
          selectedImage = ev.target.result;
          showImagePreview(selectedImage);
        };
        reader.readAsDataURL(file);
      }
    });
  }

  function showImagePreview(src) {
    let preview = document.querySelector(".image-preview-bar");
    if (!preview) {
      preview = document.createElement("div");
      preview.className = "image-preview-bar";
      document.querySelector(".input-box").prepend(preview);
    }
    preview.innerHTML = `
      <div class="preview-item">
        <img src="${src}" />
        <button onclick="removeImage()">×</button>
      </div>
    `;
    sendBtn.disabled = false;
  }

  window.removeImage = () => {
    selectedImage = null;
    const preview = document.querySelector(".image-preview-bar");
    if (preview) preview.remove();
    const imageInput = document.getElementById("image-input");
    imageInput.value = "";
    sendBtn.disabled = userInput.value.trim() === "";
  };

  function initVoice() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SpeechRecognition) {
      recognition = new SpeechRecognition();
      recognition.continuous = false;
      recognition.interimResults = false;
      recognition.lang = 'en-US'; // Default, we can make it dynamic later

      recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        userInput.value = transcript;
        userInput.dispatchEvent(new Event('input'));
        toggleRecording(false);
      };

      recognition.onerror = () => toggleRecording(false);
      recognition.onend = () => toggleRecording(false);
    }

    const voiceBtn = document.getElementById("voice-btn");
    if (voiceBtn) {
      voiceBtn.addEventListener("click", () => {
        if (!recognition) {
          alert("Voice recognition not supported in this browser.");
          return;
        }
        if (isRecording) {
            recognition.stop();
        } else {
            recognition.start();
            toggleRecording(true);
        }
      });
    }
  }

  function toggleRecording(state) {
    isRecording = state;
    const btn = document.getElementById("voice-btn");
    if (btn) {
      btn.classList.toggle("recording", state);
      btn.innerHTML = state 
        ? '<i class="fas fa-stop"></i>' 
        : '<i class="fas fa-microphone"></i>';
    }
  }

  function speak(text) {
    if (!window.speechSynthesis) return;
    // Strip markdown for cleaner audio
    const cleanText = text.replace(/[#*`_~\[\]]/g, '');
    const utterance = new SpeechSynthesisUtterance(cleanText);
    utterance.rate = 0.95; // Slightly slower for 'Grandma' feel
    utterance.pitch = 1.0;
    // We could try to find a Swahili/localized voice if available
    window.speechSynthesis.speak(utterance);
  }

  // Auto-resize textarea
  userInput.addEventListener("input", function () {
    this.style.height = "auto";
    this.style.height = this.scrollHeight + "px";
    sendBtn.disabled = this.value.trim() === "";
  });

  // Handle Suggestions
  suggestionCards.forEach((card) => {
    card.addEventListener("click", () => {
      const prompt = card.getAttribute("data-prompt");
      sendMessage(prompt);
    });
  });

  // New Chat
  newChatBtn.addEventListener("click", () => {
    resetChat();
  });

  function resetChat() {
    currentThreadId = null;
    history = [];
    messageList.innerHTML = "";
    messageList.style.display = "none";
    welcomeScreen.style.display = "block";
    userInput.value = "";
    userInput.style.height = "auto";
    document.querySelectorAll(".history-item").forEach(el => el.classList.remove("active"));
  }

  // Send on Enter
  userInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      if (!sendBtn.disabled) {
        sendMessage(userInput.value.trim());
      }
    }
  });

  sendBtn.addEventListener("click", () => {
    sendMessage(userInput.value.trim());
  });

  async function loadThreads() {
    try {
      const response = await fetch("/api/threads/");
      if (response.ok) {
        const threads = await response.json();
        renderThreadList(threads);
      }
    } catch (e) {
      console.error("Failed to load threads", e);
    }
  }

  function renderThreadList(threads) {
    const list = document.getElementById("history-list");
    list.innerHTML = "";
    threads.forEach(t => {
      const item = document.createElement("div");
      item.className = `history-item ${t.id === currentThreadId ? 'active' : ''}`;
      item.textContent = t.title || "New Consultation";
      item.onclick = () => switchThread(t.id);
      list.appendChild(item);
    });
  }

  async function switchThread(id) {
    currentThreadId = id;
    welcomeScreen.style.display = "none";
    messageList.style.display = "flex";
    messageList.innerHTML = ""; // Clear
    const loading = appendTypingIndicator(); // Show loading indicator
    
    try {
      const response = await fetch(`/api/threads/${id}/messages/`);
      if (response.ok) {
        const messages = await response.json();
        removeElement(loading);
        messages.forEach(m => appendMessage(m.role, m.content, m.media_url));
        showProactiveTip(); // Mama Msoko welcomes you back
        loadThreads(); // Refresh list to show active
      }
    } catch (e) {
      console.error("Failed to switch thread", e);
    }
  }

  async function sendMessage(text) {
    if (!text) return;

    // UI State
    welcomeScreen.style.display = "none";
    messageList.style.display = "flex";

    appendMessage("user", text, selectedImage);
    userInput.value = "";
    userInput.style.height = "auto";
    sendBtn.disabled = true;

    const streamingMessage = appendStreamingMessage();
    const bubble = streamingMessage.querySelector(".message-bubble");
    let fullReply = "";

    const payload = { 
      message: text, 
      thread_id: currentThreadId,
      image: selectedImage // Sending as base64
    };

    if (selectedImage) removeImage();

    try {
      const response = await fetch("/api/stream/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (!response.ok) throw new Error(`Status ${response.status}`);

      const reader = response.body.getReader();
      const decoder = new TextDecoder();

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value);
        const lines = chunk.split("\n");

        for (const line of lines) {
          if (line.startsWith("data: ")) {
            const dataStr = line.slice(6).trim();
            if (dataStr === "[DONE]") break;

            try {
              const data = JSON.parse(dataStr);
              if (data.thread_id && !currentThreadId) {
                 currentThreadId = data.thread_id;
                 loadThreads(); // Update sidebar with new thread
              }
              if (data.text) {
                fullReply += data.text;
                bubble.innerHTML = renderMarkdown(fullReply);
                chatArea.scrollTo({ top: chatArea.scrollHeight, behavior: "auto" });
              }
            } catch (e) {
              console.error("Error parsing SSE", e);
            }
          }
        }
      }
      
      updateStatus(true);
    } catch (error) {
      console.error("Streaming Error:", error);
      bubble.innerHTML = `🚨 Error: ${error.message}. Check backend.`;
      updateStatus(false);
    } finally {
      sendBtn.disabled = userInput.value.trim() === "";
    }
  }

  function appendStreamingMessage() {
    const msgDiv = document.createElement("div");
    msgDiv.className = `message ai`;

    msgDiv.innerHTML = `
        <div class="message-avatar"><i class="fas fa-robot" style="color:white;"></i></div>
        <div class="message-bubble"><span class="cursor">|</span></div>
    `;
    
    messageList.appendChild(msgDiv);
    chatArea.scrollTo({ top: chatArea.scrollHeight, behavior: "smooth" });
    return msgDiv;
  }

  function appendMessage(role, text, image = null) {
    const isAI = role === 'ai' || role === 'assistant';
    const msgDiv = document.createElement("div");
    msgDiv.className = `message ${isAI ? 'ai' : 'user'}`;

    const avatar = document.createElement("div");
    avatar.className = "message-avatar";
    avatar.innerHTML =
      isAI
        ? '<i class="fas fa-robot" style="color:white;"></i>'
        : '<i class="fas fa-user" style="color:#475569;"></i>';

    const bubble = document.createElement("div");
    bubble.className = "message-bubble";

    if (image) {
      const img = document.createElement("img");
      img.src = image;
      img.className = "message-image";
      bubble.appendChild(img);
    }

    if (isAI) {
      bubble.innerHTML = renderMarkdown(text);
      const speakerBtn = document.createElement("button");
      speakerBtn.className = "action-btn speaker-btn";
      speakerBtn.innerHTML = '<i class="fas fa-volume-up"></i>';
      speakerBtn.onclick = () => speak(text);
      bubble.appendChild(speakerBtn);
    } else {
      const textDiv = document.createElement("div");
      textDiv.textContent = text;
      bubble.appendChild(textDiv);
    }

    msgDiv.appendChild(avatar);
    msgDiv.appendChild(bubble);
    messageList.appendChild(msgDiv);

    // Scroll to bottom
    chatArea.scrollTo({ top: chatArea.scrollHeight, behavior: "smooth" });
  }

  async function showProactiveTip() {
    let tip = "Mama Msoko says: Saturdays are for hustle! Nairobi is awake now. ☀️";
    
    try {
        const res = await fetch("/api/dashboard/");
        if (res.ok) {
            const data = await res.json();
            if (data.goals && data.goals.length > 0) {
                const randomGoal = data.goals[Math.floor(Math.random() * data.goals.length)];
                tip = `Mama Msoko says: You are ${randomGoal.progress}% close to your goal '${randomGoal.title}'. Keep pushing! 🚀`;
            } else {
                const tips = [
                  "Kitu Safi: Did you record your sales from yesterday? Record-keeping is king! 👑",
                  "Biashara ni connection: Reach out to one new customer today! 🤝",
                  "Hustle safi: If you're selling mitumba, display your best GRADE A at the front. ✨"
                ];
                tip = tips[Math.floor(Math.random() * tips.length)];
            }
        }
    } catch (e) { /* Fallback to default tip */ }
    
    const tipDiv = document.createElement("div");
    tipDiv.className = "proactive-tip";
    tipDiv.innerHTML = `<i class="fas fa-lightbulb"></i> ${tip}`;
    chatArea.appendChild(tipDiv);
    
    setTimeout(() => {
        tipDiv.style.opacity = "0";
        setTimeout(() => tipDiv.remove(), 1000);
    }, 8000); 
  }

  function appendTypingIndicator() {
    const div = document.createElement("div");
    div.className = "message ai typing";
    div.innerHTML = `
            <div class="message-avatar"><i class="fas fa-robot" style="color:white;"></i></div>
            <div class="message-bubble" style="display:flex; gap:4px; align-items:center;">
                <div class="dot-typing"></div>
                <div class="dot-typing"></div>
                <div class="dot-typing"></div>
            </div>
        `;
    messageList.appendChild(div);
    chatArea.scrollTo({ top: chatArea.scrollHeight, behavior: "smooth" });
    return div;
  }

  function renderMarkdown(text) {
    if (typeof marked === "undefined") return text;
    const rawHtml = marked.parse(text);
    return typeof DOMPurify !== "undefined"
      ? DOMPurify.sanitize(rawHtml)
      : rawHtml;
  }

  function removeElement(el) {
    if (el && el.parentNode) el.parentNode.removeChild(el);
  }

  function updateStatus(isOnline) {
    statusDot.style.backgroundColor = isOnline ? "var(--primary)" : "#f43f5e";
    statusText.textContent = isOnline ? "AI Coach Online" : "AI Coach Offline";
  }
});

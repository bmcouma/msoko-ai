/**
 * Msoko AI - Professional Modern Frontend Logic
 * Msoko AI - Professional Modern Frontend Logic
 */

function initTheme() {
    const savedTheme = localStorage.getItem("msoko-theme") || "system";
    applyTheme(savedTheme);
    
    // Listen for system theme changes
    window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", (e) => {
        if (localStorage.getItem("msoko-theme") === "system") {
            applyTheme("system");
        }
    });
}

function applyTheme(theme) {
    const html = document.documentElement;
    let actualTheme = theme;
    
    if (theme === "system") {
        actualTheme = window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
    }
    
    html.setAttribute("data-theme", actualTheme);
    updateThemeIcon(actualTheme);
}

function updateThemeIcon(theme) {
    const icon = document.querySelector("#theme-toggle-btn i");
    if (icon) {
        icon.className = theme === "dark" ? "fas fa-sun" : "fas fa-moon";
    }
}

function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute("data-theme");
    const newTheme = currentTheme === "dark" ? "light" : "dark";
    
    localStorage.setItem("msoko-theme", newTheme);
    applyTheme(newTheme);
}

document.addEventListener("DOMContentLoaded", () => {
  const userInput = document.getElementById("user-input");
  const sendBtn = document.getElementById("send-btn");
  const chatArea = document.getElementById("chat-area");
  const messageList = document.getElementById("message-list");
  const welcomeScreen = document.getElementById("welcome-screen");
  const suggestionCards = document.querySelectorAll(".pill-btn");
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
  let isAuthenticated = false;

  // INITIAL LOAD
  initTheme();
  checkSession();
  initVoice();
  initImage();
  initAuth();

  dashboardBtn.addEventListener("click", showDashboard);
  profileBtn.addEventListener("click", showProfile);
  document.getElementById("theme-toggle-btn").addEventListener("click", toggleTheme);
  
  // Advanced Features Init
  initAttachments();
  initSearchToggle();

  async function showDashboard() {
    try {
        const res = await fetch("/api/dashboard/");
        const data = await res.json();
        
        const content = `
            <div class="dashboard-header">
                <h3><i class="fas fa-chart-line"></i> Strategic Dashboard</h3>
                <div style="display:flex; gap:8px;">
                    <button class="add-goal-btn" id="benchmark-btn" title="Audit Venture"><i class="fas fa-vial"></i></button>
                    <p>Performance insights for ${data.business_name}</p>
                </div>
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
                <h4>Msoko AI Insights</h4>
                <ul class="insight-ul">
                    ${data.recent_insights.map(i => `<li><i class="fas fa-magic"></i> ${i}</li>`).join('')}
                </ul>
            </div>
        `;
        showOverlay(content);
        document.getElementById("add-goal-btn").onclick = showAddGoalForm;
        document.getElementById("benchmark-btn").onclick = () => {
            hideOverlay();
            sendMessage("Perform a strategic audit and benchmark my venture against global standards based on my profile and goals.");
        };
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
            alert("Msoko AI updated your profile! 🚀");
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

  async function checkSession() {
    try {
        const res = await fetch("/api/auth/session/");
        const data = await res.json();
        isAuthenticated = data.authenticated;
        updateUIForAuth(data.authenticated, data.user);
        if (data.authenticated) {
            loadThreads();
        }
    } catch (e) { console.error("Session check failed"); }
  }

  function updateUIForAuth(isAuth, user) {
      const authSection = document.getElementById("auth-section");
      const dashboardBtn = document.getElementById("dashboard-btn");
      const profileBtn = document.getElementById("profile-btn");
      const newChatBtn = document.getElementById("new-chat-btn");

      if (isAuth && user) {
          authSection.innerHTML = `
              <div class="user-pill">
                  <i class="fas fa-user-circle"></i>
                  <span>${user.first_name || 'Hustler'}</span>
                  <button id="logout-btn" title="Sign Out"><i class="fas fa-sign-out-alt"></i></button>
              </div>
          `;
          document.getElementById("logout-btn").onclick = handleLogout;
          dashboardBtn.disabled = false;
          profileBtn.disabled = false;
          newChatBtn.disabled = false;
      } else {
          authSection.innerHTML = `
              <button class="nav-item" id="login-btn">
                  <i class="fas fa-user-shield"></i>
                  <span>Sign In / Join</span>
              </button>
          `;
          document.getElementById("login-btn").onclick = showAuthChoice;
          dashboardBtn.disabled = true;
          profileBtn.disabled = true;
          newChatBtn.disabled = true;
      }
  }

  function showAuthChoice() {
      const content = `
        <div class="dashboard-header" style="text-align:center;">
            <h3>Start Your Strategy</h3>
            <p>Sign in to save your goals and history.</p>
        </div>
        <div style="display:flex; flex-direction:column; gap:12px;">
            <button class="save-btn" id="go-login">Sign In</button>
            <button class="save-btn" style="background:#475569;" id="go-signup">Create Account</button>
        </div>
      `;
      showOverlay(content);
      document.getElementById("go-login").onclick = showLoginForm;
      document.getElementById("go-signup").onclick = showSignupForm;
  }

  function showLoginForm() {
      const content = `
        <div class="dashboard-header">
            <h3>Welcome Back</h3>
            <p>Sign in to your strategic dashboard.</p>
        </div>
        <form id="login-form" class="profile-form">
            <div class="form-group">
                <input type="email" name="email" placeholder="Email Address" required>
            </div>
            <div class="form-group">
                <input type="password" name="password" placeholder="Password" required>
            </div>
            <div style="text-align:right; margin-bottom:12px;">
                <a href="#" id="forgot-pw-link" style="font-size:0.8rem; color:var(--primary);">Forgot Password?</a>
            </div>
            <button type="submit" class="save-btn">Sign In</button>
        </form>
      `;
      showOverlay(content);
      document.getElementById("forgot-pw-link").onclick = (e) => { e.preventDefault(); showForgotPasswordForm(); };
      
      document.getElementById("login-form").onsubmit = async (e) => {
          e.preventDefault();
          const formData = new FormData(e.target);
          const res = await fetch("/api/auth/login/", {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify(Object.fromEntries(formData))
          });
          const data = await res.json();
          if (res.ok) {
              hideOverlay();
              checkSession();
          } else {
              alert(data.error || "Invalid login details.");
          }
      };
  }

  function showSignupForm() {
      const content = `
        <div class="dashboard-header">
            <h3>Join Msoko AI</h3>
            <p>Professional strategic hub for entrepreneurs.</p>
        </div>
        <form id="signup-form" class="profile-form">
            <div style="display:flex; gap:8px;">
                <div class="form-group" style="flex:1;">
                    <input type="text" name="first_name" placeholder="First Name" required>
                </div>
                <div class="form-group" style="flex:1;">
                    <input type="text" name="last_name" placeholder="Surname" required>
                </div>
            </div>
            <div class="form-group">
                <input type="email" name="email" placeholder="Email Address" required>
            </div>
            <div class="form-group">
                <input type="password" name="password" placeholder="Password (Min 8 chars)" required minlength="8">
            </div>
            <div class="form-group">
                <input type="password" name="confirm_password" placeholder="Confirm Password" required>
            </div>
            <div style="margin: 12px 0; font-size: 0.8rem; display:flex; align-items:flex-start; gap:8px;">
                <input type="checkbox" required id="terms-check" style="width:auto; margin-top:3px;">
                <label for="terms-check">I agree to the <a href="#" onclick="showLegal('ToS')">Terms of Service</a> and <a href="#" onclick="showLegal('Privacy')">Privacy Policy</a>.</label>
            </div>
            <button type="submit" class="save-btn">Create Professional Account</button>
        </form>
      `;
      showOverlay(content);
      document.getElementById("signup-form").onsubmit = async (e) => {
          e.preventDefault();
          const formData = new FormData(e.target);
          const payload = Object.fromEntries(formData);
          
          if (payload.password !== payload.confirm_password) {
              alert("Passwords do not match.");
              return;
          }

          const res = await fetch("/api/auth/register/", {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify(payload)
          });
          const data = await res.json();
          if (res.ok) {
              hideOverlay();
              checkSession();
              alert("Welcome to Msoko AI! Let's set up your business profile.");
              setTimeout(showProfile, 1000);
          } else {
              alert(data.error || "Registration failed.");
          }
      };
  }

  async function handleLogout() {
      await fetch("/api/auth/logout/", { method: "POST" });
      checkSession();
      resetChat();
  }

  function initAuth() {
     // Placeholder for any other auth init if needed
  }

  function initAttachments() {
    const attachBtn = document.getElementById("plus-attach-btn");
    const fileInput = document.getElementById("universal-file-input");

    if (!attachBtn || !fileInput) return;

    attachBtn.addEventListener("click", () => fileInput.click());

    fileInput.addEventListener("change", (e) => {
      const files = Array.from(e.target.files);
      files.forEach(file => {
        const reader = new FileReader();
        reader.onload = (ev) => {
          const fileData = {
            name: file.name,
            type: file.type,
            data: ev.target.result,
            isImage: file.type.startsWith("image/")
          };
          addAttachmentPreview(fileData);
        };
        if (file.type.startsWith("image/")) {
            reader.readAsDataURL(file);
        } else {
            // For docs/pdfs, we just store the name and a placeholder for now
            // In a real scenario, we'd upload this to get a link or process content
            reader.readAsText(file.slice(0, 1024)); // Just a peek
        }
      });
    });
  }

  function addAttachmentPreview(file) {
    let previewBar = document.querySelector(".attachment-preview-bar");
    if (!previewBar) {
      previewBar = document.createElement("div");
      previewBar.className = "attachment-preview-bar";
      document.querySelector(".input-box").prepend(previewBar);
    }

    const previewItem = document.createElement("div");
    previewItem.className = "preview-item";
    
    if (file.isImage) {
        previewItem.innerHTML = `<img src="${file.data}" alt="${file.name}">`;
    } else {
        const iconClass = file.type.includes("pdf") ? "fa-file-pdf" : "fa-file-alt";
        previewItem.innerHTML = `
            <div class="file-icon-preview">
                <i class="fas ${iconClass}"></i>
                <span>${file.name.split('.').pop().toUpperCase()}</span>
            </div>
        `;
    }

    const removeBtn = document.createElement("button");
    removeBtn.innerHTML = "&times;";
    removeBtn.onclick = () => previewItem.remove();
    previewItem.appendChild(removeBtn);
    
    previewBar.appendChild(previewItem);
  }

  let isSearchEnabled = false;
  function initSearchToggle() {
    const searchBtn = document.getElementById("search-toggle-btn");
    if (!searchBtn) return;

    searchBtn.addEventListener("click", () => {
        isSearchEnabled = !isSearchEnabled;
        searchBtn.classList.toggle("active", isSearchEnabled);
        if (isSearchEnabled) {
            console.log("Web Research Mode Active");
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

  // Suggestion Pills
  document.addEventListener("click", (e) => {
    const btn = e.target.closest(".pill-btn");
    if (btn) {
      const prompt = btn.getAttribute("data-prompt");
      sendMessage(prompt);
    }
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
    
    if (threads.length > 0) {
      const sectionHeader = document.createElement("div");
      sectionHeader.className = "history-title";
      sectionHeader.style.marginTop = "8px";
      sectionHeader.innerHTML = '<i class="fas fa-clock"></i> Recent';
      list.appendChild(sectionHeader);
    }

    threads.forEach(t => {
      const item = document.createElement("div");
      item.className = `history-item ${t.id === currentThreadId ? 'active' : ''}`;
      item.innerHTML = `
        <i class="far fa-comment-alt"></i>
        <span>${t.title || "New Consultation"}</span>
      `;
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
      image: selectedImage, // Sending as base64
      search_enabled: isSearchEnabled
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
      
      renderQuickReplies(streamingMessage, fullReply);
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
      const actions = document.createElement("div");
      actions.className = "ai-actions";
      
      const speakerBtn = document.createElement("button");
      speakerBtn.className = "action-btn";
      speakerBtn.innerHTML = '<i class="fas fa-volume-up"></i>';
      speakerBtn.onclick = () => speak(text);
      
      const thumbUp = document.createElement("button");
      thumbUp.className = "action-btn";
      thumbUp.innerHTML = '<i class="far fa-thumbs-up"></i>';
      thumbUp.onclick = () => { thumbUp.innerHTML = '<i class="fas fa-thumbs-up"></i>'; };

      const thumbDown = document.createElement("button");
      thumbDown.className = "action-btn";
      thumbDown.innerHTML = '<i class="far fa-thumbs-down"></i>';
      thumbDown.onclick = () => { thumbDown.innerHTML = '<i class="fas fa-thumbs-down"></i>'; };

      actions.appendChild(speakerBtn);
      actions.appendChild(thumbUp);
      actions.appendChild(thumbDown);
      bubble.appendChild(actions);

      renderQuickReplies(msgDiv, text);
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
    let tip = "Msoko AI: Global markets are active. How are we growing today? 🚀";
    
    try {
        const res = await fetch("/api/dashboard/");
        if (res.ok) {
            const data = await res.json();
            if (data.goals && data.goals.length > 0) {
                const randomGoal = data.goals[Math.floor(Math.random() * data.goals.length)];
                tip = `Msoko AI suggests: You are ${randomGoal.progress}% close to your goal '${randomGoal.title}'. Keep pushing! 🚀`;
            } else {
                const tips = [
                  "Knowledge is Capital: Have you updated your portfolio or stock list recently? 📈",
                  "Strategic Value: Positioning your business as a solution increases your margin. 💸",
                  "Global Vision: Even local ventures can adopt international standards of quality. ✨"
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

  function renderQuickReplies(msgDiv, text) {
    const bubble = msgDiv.querySelector(".message-bubble");
    // Extract [Questions] from the end of the text
    const regex = /\[([^\]]+)\]/g;
    const matches = [...text.matchAll(regex)];
    
    if (matches.length > 0) {
      // Remove tokens from display
      let cleanText = text.replace(regex, '').trim();
      bubble.innerHTML = renderMarkdown(cleanText);
      
      // Re-add actions if they were there (in appendMessage)
      if (msgDiv.classList.contains('ai')) {
         // ... simplified for now, we just ensure quick-replies div is separate
      }

      const existing = msgDiv.querySelector(".quick-replies");
      if (existing) existing.remove();

      const qrContainer = document.createElement("div");
      qrContainer.className = "quick-replies";
      
      matches.forEach(match => {
        const btn = document.createElement("button");
        btn.className = "qr-btn";
        btn.textContent = match[1];
        btn.onclick = () => sendMessage(match[1]);
        qrContainer.appendChild(btn);
      });
      
      msgDiv.appendChild(qrContainer);
    }
  }

  function renderMarkdown(text) {
    if (typeof marked === "undefined") return text;
    
    marked.setOptions({
        highlight: function(code, lang) {
            if (typeof hljs !== 'undefined') {
                const language = hljs.getLanguage(lang) ? lang : 'plaintext';
                return hljs.highlight(code, { language }).value;
            }
            return code;
        },
        langPrefix: 'hljs language-'
    });

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

  // --- Industrial Product Ready Modules ---

  window.showHelp = function() {
    document.getElementById("help-modal").style.display = "flex";
  };
  window.hideHelp = function() {
    document.getElementById("help-modal").style.display = "none";
  };
  
  window.showAbout = function() {
    document.getElementById("about-modal").style.display = "flex";
  };
  window.hideAbout = function() {
    document.getElementById("about-modal").style.display = "none";
  };

  window.showLegal = (type) => {
    const title = document.getElementById("legal-title");
    const content = document.getElementById("legal-content");
    title.innerText = type === 'ToS' ? "Terms of Service" : "Privacy Policy";
    
    content.innerHTML = type === 'ToS' 
      ? `<p>Welcome to Msoko AI. By using our platform, you agree to prioritize legal monetization and strategic growth. We provide high-fidelity AI-driven business coaching. Use it at your own strategic risk.</p>
         <p>1. <b>Account Security</b>: You are responsible for your strategic credentials.<br>
         2. <b>Fair Use</b>: Msoko AI must be used for ethical business intelligence only.</p>`
      : `<p>Your business strategics are yours. We collect names and emails to personalize your coaching experience. Your data is encrypted and used solely for generating precision insights for your venture.</p>
         <p>1. <b>Data Retention</b>: We keep your goals and history as long as your account is active.<br>
         2. <b>Transparency</b>: We never share your strategic data with third-party competitors.</p>`;
    
    document.getElementById("legal-modal").style.display = "flex";
  };
  window.hideLegal = () => {
    document.getElementById("legal-modal").style.display = "none";
  };

  function showForgotPasswordForm() {
    const content = `
        <div class="dashboard-header">
            <h3>Reset Strategy Access</h3>
            <p>Enter your email to receive a reset link.</p>
        </div>
        <form id="forgot-pw-form" class="profile-form">
            <div class="form-group">
                <input type="email" name="email" placeholder="Professional Email" required>
            </div>
            <button type="submit" class="save-btn">Send Reset Link</button>
            <div style="text-align:center; margin-top:12px;">
                <a href="#" onclick="showLoginForm(); return false;" style="font-size:0.8rem; color:var(--text-muted);">Back to Login</a>
            </div>
        </form>
    `;
    showOverlay(content);
    document.getElementById("forgot-pw-form").onsubmit = async (e) => {
        e.preventDefault();
        const formData = new FormData(e.target);
        const res = await fetch("/api/auth/password-reset/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(Object.fromEntries(formData))
        });
        const data = await res.json();
        alert(data.message);
        hideOverlay();
    };
  }
});

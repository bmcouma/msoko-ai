# msoko-ai

# M-Soko AI – Smart Business Coach for Hustlers

**M-Soko AI** is a multilingual AI-powered business coach built to empower informal entrepreneurs across Africa. It provides personalized advice on pricing, marketing, cash flow, and business growth strategies — all in Swahili, English, or Sheng.

## 💡 Problem
Most small-scale business owners in Africa lack access to business mentorship or financial literacy tools. M-Soko AI fills that gap by offering accessible, localized, and intelligent guidance tailored to real hustlers — mama mbogas, mitumba sellers, boda operators, and more.

## 🎯 Features

- 💬 AI-Powered Business Chatbot (GPT-based)
- 🧮 Pricing Strategy & Cashflow Coaching
- 📢 Localized Marketing Tips
- 🧠 Business Growth Roadmaps
- 🌐 Multilingual Support (Swahili, English, Sheng)
- 📱 USSD/SMS Support (Planned)
- 📊 Simple Interface (Streamlit or Django Frontend)

## 🛠️ Tech Stack

| Layer         | Tech                                    |
|---------------|------------------------------------------|
| Backend       | Django                                   |
| AI Engine     | GPT-4 / Mistral / OpenRouter             |
| Language API  | Google Translate API (fallback)          |
| Frontend      | Streamlit (for MVP) or Django Templates  |
| Data Store    | SQLite / Firebase                        |
| Messaging     | Africa’s Talking (for SMS/USSD, future)  |

## 🧪 How It Works

1. User enters business type and question
2. Django backend formats the prompt and sends it to the GPT API
3. Response is returned in selected language (EN/SWA/SHENG)
4. Displayed on UI or sent via SMS (coming soon)

## 🔄 Prompt Flow Example

```plaintext
Business Type: Mitumba seller in Mathare
User Input: Ninaeza uza trousers kwa bei gani?
→ GPT Prompt returns: “Uza kwa KES 250–300 kulingana na ubora. Nunua kwa KES 150–200 kupata faida ya KES 80+ per trouser...”


---

```markdown
# 🧠 Msoko AI – Your Smart Hustle Coach

Msoko AI is an AI-powered business assistant designed to empower informal sector entrepreneurs, including mama mbogas, boda boda riders, small kiosk owners, and everyday hustlers. It delivers practical, friendly, and localized business advice using conversational AI, making technology accessible to grassroots businesses.

---

## ✨ Features

- 🤖 AI chatbot trained with custom business prompts
- 🌍 Localized language style for Kenyan micro-entrepreneurs
- 💬 Real-time responses via Django backend + OpenRouter AI API
- 🧾 Advice categories include pricing, saving, expansion, marketing & customer care
- 📱 Simple responsive chat frontend built with HTML, CSS, JS

---

---

## ⚙️ Tech Stack

- **Backend:** Python, Django, httpx
- **Frontend:** HTML, CSS, JavaScript (Vanilla)
- **AI Engine:** OpenRouter AI API (e.g. OpenChat 3.5)
- **API Security:** dotenv `.env` file (environment variables)

---

## 🚀 Getting Started Locally

1. **Clone this repo**
   ```bash
   git clone https://github.com/bmcouma/msoko-ai.git
   cd msoko-ai
````

2. **Create & activate a virtual environment**

   ```bash
   python -m venv env
   env\Scripts\activate  # On Windows
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Create your ****`.env`**** file**

   ```
   OPENAI_API_KEY=your_openrouter_api_key
   ```

5. **Run migrations and start server**

   ```bash
   cd backend
   python manage.py migrate
   python manage.py runserver
   ```

6. **Open frontend**

   * Either serve static files in Django or
   * Open `frontend/index.html` directly via VS Code Live Server or a browser

---

## 🌐 Deployment Recommendations

* **Frontend:** Vercel, Netlify, or GitHub Pages
* **Backend:** Render.com, Railway, or PythonAnywhere
* **Environment config:** Add `.env` variables securely in deployment dashboard

---

## 🔐 .env File (Not committed to GitHub)

This project uses an environment file to keep API keys secure.

**Example ****`.env`****:**

```
OPENAI_API_KEY=sk-your-openrouter-key
```

---

## 📦 requirements.txt (Sample)

Generated using:

```bash
pip freeze > requirements.txt
```

Example content:

```
Django==5.2.4
httpx
python-dotenv
```

---

## 🤝 Contribution Guide

1. Fork this repo
2. Create your branch (`git checkout -b feature-name`)
3. Commit changes (`git commit -am 'Add something'`)
4. Push to your branch (`git push origin feature-name`)
5. Open a Pull Request

---

## 🧠 Prompt Design

The chatbot uses a custom system prompt to give localized business coaching. It's designed to:

* Speak in simple terms
* Avoid technical jargon
* Guide hustlers with real, actionable steps

---

## 📸 Screenshots (Optional)

Add screenshots of:

* Chatbot interface
* Sample responses
* Mobile view

---

## 🙋‍♂️ Maintainer

**Bravin Ouma**
Digital Innovator | Web Dev | Hustler Tech Evangelist
GitHub: [@bmcouma](https://github.com/bmcouma)
X (Twitter): [@bmc\_ouma](https://x.com/bmc_ouma)

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 🏁 What's Next

*

---

*Msoko AI – built by hustlers, for hustlers.* 🚀

```

---


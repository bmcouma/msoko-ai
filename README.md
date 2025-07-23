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

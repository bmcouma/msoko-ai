# 🛒 Msoko AI — Strategic Hustle Intelligence for African Entrepreneurs

> **Mama Msoko** is your AI-powered biashara mentor — speaking Swahili, Sheng, and business. Built for mama mbogas, bodaboda hustlers, mitumba traders, and every small entrepreneur grinding in East Africa.

[![Django](https://img.shields.io/badge/Django-5.x-092E20?style=flat-square&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-REST%20Framework-red?style=flat-square&logo=django)](https://www.django-rest-framework.org/)
[![OpenRouter](https://img.shields.io/badge/AI-OpenRouter%20Multimodal-6C63FF?style=flat-square&logo=openai&logoColor=white)](https://openrouter.ai/)
[![PWA](https://img.shields.io/badge/PWA-Ready-5A0FC8?style=flat-square&logo=googlechrome&logoColor=white)](https://web.dev/progressive-web-apps/)
[![CI Status](https://github.com/bmcouma/msoko-ai/actions/workflows/ci.yml/badge.svg)](https://github.com/bmcouma/msoko-ai/actions)
[![Deploy on Railway](https://img.shields.io/badge/Deploy-Railway-black?style=flat-square&logo=railway)](https://railway.app/new/template)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)
[![Made in Kenya](https://img.shields.io/badge/Made%20in-Kenya%20🇰🇪-black?style=flat-square)](https://teklini.tech)

---

## 🌐 Live Demo

> 🚧 **Coming soon** — Deploying on [Railway](https://railway.app) / [Render](https://render.com).  
> Track progress on the [`upgrade-phase1`](https://github.com/bmcouma/msoko-ai/tree/upgrade-phase1) branch.

---

## 🏗️ Architecture

```mermaid
graph TD
    subgraph Frontend["🖥️ Frontend (PWA)"]
        A["Vanilla JS + Glassmorphism UI"]
        B["Voice + Vision Upload"]
        C["Offline Support (Service Worker)"]
    end

    subgraph Backend["⚙️ Backend (Django + DRF)"]
        D["Django Views / REST API"]
        E["SSE Streaming Endpoint"]
        F["Session Auth + JWT"]
        G["Gunicorn WSGI Server"]
    end

    subgraph AI["🤖 AI Layer (OpenRouter)"]
        H["Multimodal Models (Vision + Text)"]
        I["Mama Msoko Persona / System Prompt"]
        J["Semantic RAG — Knowledge Store"]
    end

    subgraph Data["🗄️ Data Layer"]
        K["PostgreSQL — Chat Threads, Users, Goals"]
        L["Redis — Cache / Rate Limiting"]
        M["Media Storage — Uploads / Docs"]
    end

    A -->|HTTP + SSE| D
    B -->|Base64 Image| E
    D --> F
    D --> E
    E --> H
    H --> I
    H --> J
    D --> K
    D --> L
    D --> M
```

---

## ✨ Why Msoko Stands Out

| Feature | Msoko AI 🛒 | Generic Chatbot 🤖 |
|---|---|---|
| **Local language** | Swahili + Sheng fluent | English only |
| **Business context** | Mama mboga, boda, mitumba persona | Generic assistant |
| **Vision analysis** | Inventory photo → pricing advice | Text only |
| **Persistent threads** | Full chat history per user | One-shot or basic memory |
| **Business profile** | Tracks your sector, goals, revenue | No business context |
| **SSE streaming** | Real-time token-by-token response | Request/response only |
| **PWA** | Installable, offline-ready | Web only |
| **African market data** | RAG-backed local market knowledge | Generic global training |
| **Goal tracking** | Revenue targets, milestones | None |
| **Open source** | MIT licensed, self-hostable | Closed / SaaS |

---

## 🌟 Core Capabilities

### 🧠 Strategic Coaching
- **Business Profiler**: Context-aware advice tailored to your sector and stage.
- **Executive Dashboard**: Track growth metrics, active goals, and strategic insights.
- **Goal Engine**: Set revenue targets, inventory milestones, and savings goals.

### 👁️ Multimodal Intelligence
- **Vision Analysis**: Upload your inventory photos — Mama Msoko tells you what to restock and at what price.
- **Document Analysis**: Upload Excel/CSV sales records for AI-powered trend analysis.
- **Voice Flow**: Hands-free strategic sessions.

### ⚡ Engineering Excellence
- **SSE Streaming**: Real-time responses, character by character.
- **PWA**: Install on your phone's home screen. Works offline.
- **Glassmorphism UI**: Premium dark-mode interface built for low-latency performance.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django 5, Django REST Framework |
| AI | OpenRouter (multimodal, auto-model) |
| Frontend | Vanilla JS, CSS Glassmorphism, PWA |
| Database | PostgreSQL (SQLite in dev) |
| Cache | Redis |
| Static Files | WhiteNoise |
| Server | Gunicorn |
| Admin | Jazzmin (dark theme) |

---

## 🚀 Getting Started

### Option A: Local Development (Python)

```bash
# 1. Clone the repo
git clone https://github.com/bmcouma/msoko-ai.git
cd msoko-ai

# 2. Set up environment
cp .env.example backend/.env
# Edit backend/.env and add your OPENROUTER_API_KEY

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run migrations and start
cd backend
python manage.py migrate
python manage.py runserver
```

Visit [http://localhost:8000](http://localhost:8000) — Mama Msoko is ready to hustle.

---

### Option B: Docker (Recommended for Production)

```bash
# 1. Clone and configure
git clone https://github.com/bmcouma/msoko-ai.git
cd msoko-ai
cp .env.example .env
# Edit .env with your values

# 2. Build and start all services
docker-compose up --build

# 3. Run migrations (first time)
docker-compose exec web python backend/manage.py migrate
docker-compose exec web python backend/manage.py createsuperuser
```

Visit [http://localhost:8000](http://localhost:8000)

> **Services started**: Django + Gunicorn (`web`), PostgreSQL (`db`), Redis (`redis`).

### 🚢 Deploy to Railway (Production)

Msoko AI is natively configured for 1-click deployments to platforms like **Railway** or Heroku.

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template)

#### Step 1: Connect your Repo
1. Sign up on [Railway](https://railway.app/).
2. Click **New Project** > **Deploy from GitHub repo**.
3. Select `bmcouma/msoko-ai`.

#### Step 2: Add Databases
1. In your Railway project, click **New** > **Database** > Add both **PostgreSQL** and **Redis**.

#### Step 3: Configure Environment Variables
Navigate to your Web Service > **Variables** and add:
- `DATABASE_URL` = (Reference the connected Postgres URL)
- `REDIS_URL` = (Reference the connected Redis URL)
- `CELERY_BROKER_URL` = (Same as Redis URL)
- `OPENROUTER_API_KEY` = your OpenRouter key
- `SECRET_KEY` = (A strong, random Django secret)
- `DEBUG` = `False`
- `PORT` = `8000`

#### Step 4: Deploy & Test
1. Railway will automatically detect the `Procfile` and `requirements.txt`.
2. Gunicorn and WhiteNoise will serve the app. 
3. Database migrations run automatically via `entrypoint.sh`.
4. The first time the app starts, the LlamaIndex engine will automatically index the `backend/chatbot/rag/data` folder to populate the Vector Store.

---

## ⚙️ Environment Variables

See [`.env.example`](.env.example) for a full list. Key ones:

| Variable | Description |
|---|---|
| `SECRET_KEY` | Django secret key |
| `OPENROUTER_API_KEY` | Your OpenRouter API key |
| `DATABASE_URL` | Postgres connection string |
| `REDIS_URL` | Redis connection string |
| `DEBUG` | `True` for dev, `False` for prod |

---

## 🤝 Contributing

Pull requests are welcome. For major changes, open an issue first. See [LICENSE](LICENSE) for terms.

---

## 🏢 About Teklini Technologies

> *We build intelligent systems that solve real African problems.*

- 🌐 [teklini.tech](https://teklini.tech)
- 💬 [WhatsApp](https://wa.me/254791832015)
- © 2026 Teklini Technologies — MIT Licensed

# Msoko AI V3: Strategic Hustle Intelligence 🚀

Msoko AI is a sophisticated AI business coach designed specifically for African entrepreneurs (mama mbogas, boda riders, kiosk owners, and mitumba retailers). V3 elevates the platform from a chat assistant to a **Strategic Intelligence Partner**.

## 🌟 V3 Key Features

### 🧠 Strategic Coaching

- **Business Profiler**: Personalized advice based on sector (Retail, Agri, Wholesale, etc.) and location.
- **Executive Dashboard**: A unified view of consultations, growth metrics, and active goals.
- **Goal Management**: Set and track revenue, inventory, and savings targets with Mama Msoko's guidance.

### 👁️ Multimodal Intelligence

- **Advanced Vision Analysis**: Upload photos of your inventory or displays for automated counts, organization tips, and restocking advice.
- **Voice Interaction**: Speak directly to Mama Msoko in a natural blend of English, Swahili, and Sheng.

### ⚡ Professional Performance

- **Real-time Streaming (SSE)**: Industrial-standard low latency responses.
- **Progressive Web App (PWA)**: Installable on home screens with service worker caching for offline resilience in market environments.
- **Semantic RAG**: A localized market knowledge base providing real-time pricing and trend data.

## 🛠️ Tech Stack

- **Backend**: Django, Django REST Framework, SSE (Server-Sent Events).
- **Frontend**: Modern Vanilla JS, CSS Glassmorphism, PWA Manifest.
- **AI Engine**: OpenRouter (Auto-selecting best-in-class free models), Vision-capable multimodal payloads.
- **Context Management**: SQLite persistent threads & message history.

## 🚀 Getting Started

1. **Clone the repo**
2. **Setup Environment**:
   ```bash
   cp .env.example .env
   # Add your OPENAI_API_KEY (OpenRouter)
   ```
3. **Migrate & Run**:
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```
4. **Access**: [http://localhost:8000](http://localhost:8000)

## 🧙 Persona: Mama Msoko

Mama Msoko isn't just an AI; she's a "Biashara Mentor" who speaks your language. She understands the hustle of Nairobi markets and provides street-smart wisdom to help you grow your Kitu Safi!

---

_Built with ❤️ for the empowerment of everyday entrepreneurs._

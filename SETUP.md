# Msoko AI - Setup Guide

## Quick Start

### 1. Prerequisites
- Python 3.12+ (required for Django 6.0)
- pip (Python package manager)
- Virtual environment (recommended)

### 2. Installation Steps

```bash
# Clone the repository
git clone https://github.com/bmcouma/msoko-ai.git
cd msoko-ai

# Create virtual environment
python -m venv env

# Activate virtual environment
# On Windows:
env\Scripts\activate
# On Linux/Mac:
source env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file (copy from .env.example if available)
# Add your OPENAI_API_KEY and DJANGO_SECRET_KEY

# Navigate to backend
cd backend

# Run migrations
python manage.py migrate

# Create superuser (optional, for admin access)
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

### 3. Environment Variables

Create a `.env` file in the project root with:

```env
DJANGO_SECRET_KEY=your-secret-key-here
DEBUG=True
OPENAI_API_KEY=your_openrouter_api_key_here
```

**Get your OpenRouter API key:**
1. Visit https://openrouter.ai/
2. Sign up/login
3. Go to Keys section
4. Create a new API key
5. Copy and paste into `.env` file

### 4. Running the Application

**Backend (Django):**
```bash
cd backend
python manage.py runserver
```
Server runs at: http://127.0.0.1:8000

**Frontend:**
- Open `backend/frontend/index.html` in your browser
- Or serve it through Django static files

**API Endpoints:**
- `GET /` - Health check
- `GET /api/chat/` - Check if AI is ready
- `POST /api/chat/` - Send message to AI

### 5. Testing the API

```bash
# Test with curl
curl -X POST http://127.0.0.1:8000/api/chat/ \
  -H "Content-Type: application/json" \
  -d '{"message": "How do I price my products?"}'
```

### 6. Production Deployment

**Important settings for production:**
1. Set `DEBUG=False` in settings.py
2. Update `ALLOWED_HOSTS` with your domain
3. Set a strong `DJANGO_SECRET_KEY`
4. Use environment variables for all secrets
5. Configure proper database (PostgreSQL recommended)
6. Set up static file serving (WhiteNoise is included)
7. Use HTTPS
8. Configure CORS properly (currently allows all origins)

**Deployment platforms:**
- **Backend:** Render.com, Railway, PythonAnywhere, Heroku
- **Frontend:** Vercel, Netlify, GitHub Pages

### 7. Troubleshooting

**Issue: Django version error**
- Ensure Python 3.12+ is installed
- Or downgrade Django to 5.0.x for Python 3.10+

**Issue: API key not working**
- Verify `.env` file is in project root
- Check API key is correct (no extra spaces)
- Ensure OpenRouter account has credits

**Issue: CORS errors**
- Backend CORS is configured to allow all origins
- Check `django-cors-headers` is installed
- Verify middleware order in settings.py

**Issue: Static files not loading**
- Run `python manage.py collectstatic`
- Check `STATIC_ROOT` and `STATIC_URL` in settings

### 8. Project Structure

```
msoko-ai/
├── backend/
│   ├── chatbot/          # Main Django app
│   │   ├── utils/        # Utility functions
│   │   └── prompts/      # AI prompt templates
│   ├── frontend/         # HTML/CSS/JS frontend
│   ├── integrations/    # External API integrations
│   └── msoko_backend/    # Django project settings
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables (not in git)
└── README.md             # Project documentation
```

### 9. Development Tips

- Use Django admin at `/admin/` for database management
- Check Django logs for debugging
- Use browser DevTools to inspect API calls
- Test API with Postman or curl

### 10. Next Steps

- [ ] Add user authentication
- [ ] Implement conversation history
- [ ] Add rate limiting per user
- [ ] Set up database models for chat logs
- [ ] Add multilingual support (Swahili, Sheng)
- [ ] Add analytics and monitoring

---

For more help, check the [README.md](README.md) or open an issue on GitHub.

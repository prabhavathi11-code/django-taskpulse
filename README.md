# ⚡ NexusAI Studio - Advanced Django AI Chatbot Platform

An advanced, production-grade AI Chatbot web application built with **Django 6**, modern glassmorphism UI, real-time Markdown & code syntax highlighting, conversation persistence, voice recognition, and multi-model support (Built-in Ultra Engine, Google Gemini, OpenAI GPT-4o).

---

## ✨ Features

- 🧠 **Multi-Model Intelligence**:
  - **Built-in Smart Engine**: Zero-setup intelligent reasoning, code generation, and Django architecture recommendations.
  - **Google Gemini & OpenAI Integration**: Plug in your API keys in the Settings modal or environment variables to tap directly into live LLMs.
- 🎨 **Ultra-Modern Glassmorphism UI**:
  - Dark mode first design with custom gradients, neon accents, and smooth micro-animations.
  - Responsive layout with expandable collapsible drawer for mobile and desktop screens.
  - Dark / Light mode toggle with saved state.
- 💬 **ChatGPT-Style Conversations**:
  - Persistent conversation threads stored in Django SQLite/PostgreSQL models.
  - Ability to create new chats, switch between sessions, delete individual chats, or clear all history.
- ⚡ **Rich Markdown & Code Formatter**:
  - Powered by `marked.js` and `highlight.js` (Atom One Dark).
  - One-click **Copy Code** button for code snippets.
  - Interactive prompt chips for immediate testing.
- 🎙️ **Voice Recognition & Speech Synthesis**:
  - Voice-to-Text input using Web Speech API.
  - Text-to-Speech audio playback for assistant answers.
- 📥 **Export to Markdown**:
  - Export full chat threads directly to `.md` files with a single click.

---

## 🚀 Quick Start (Running Locally)

### 1. Activate Environment & Navigate
```bash
# In the project root:
.\env\Scripts\activate
cd myapp
```

### 2. Apply Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Start Development Server
```bash
python manage.py runserver
```

Open your browser and navigate to:
👉 **`http://127.0.0.1:8000/`** or **`http://127.0.0.1:8000/chatbot/`**

---

## 🐙 Push to GitHub Repository

Run the following commands in the project root directory (`c:\Users\ch prabahavathi\Downloads\django`):

```bash
# 1. Initialize git
git init

# 2. Add all files
git add .

# 3. Create your first commit
git commit -m "feat: Add NexusAI advanced Django chatbot"

# 4. Set default branch to main
git branch -M main

# 5. Link your GitHub repository (replace with your repo URL)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# 6. Push to GitHub
git push -u origin main
```

---

## 🌐 Deploy Live (Step-by-Step)

### Option 1: Render.com (Recommended - Free & Fast)
1. Push your repository to GitHub.
2. Sign in to [Render.com](https://render.com).
3. Click **New +** -> **Web Service** -> Connect your GitHub repo.
4. Settings:
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt && cd myapp && python manage.py migrate`
   - **Start Command**: `cd myapp && gunicorn myapp.wsgi:application`
5. Click **Deploy Web Service** to receive your live URL!

### Option 2: PythonAnywhere
1. Create a free account on [PythonAnywhere](https://www.pythonanywhere.com/).
2. Clone your GitHub repository in the Bash console.
3. Configure virtualenv and reload the web app.

---

## 🔑 Optional API Configuration
You can use the chatbot completely free without any API keys. To connect external models:
- Set environment variables:
  ```bash
  set GEMINI_API_KEY="your-gemini-key"
  set OPENAI_API_KEY="your-openai-key"
  ```
- Or click the **API & Settings** button in the sidebar and enter your key directly.

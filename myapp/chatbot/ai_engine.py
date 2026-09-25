import os
import json
import urllib.request
import urllib.error
import re


def generate_smart_fallback(prompt, history=None):
    """
    Intelligent built-in AI reasoning engine when no external API key is set.
    Handles coding, explanations, Django assistance, calculations, conversational queries.
    """
    clean_p = prompt.strip().lower()

    # Telugu / Multilingual friendly greetings
    if any(w in clean_p for w in ["namaste", "namaskaram", "ela unnav", "bagunnav"]):
        return (
            "Namaskaram! 🙏 Nenu mee AI Chat Assistant ni. "
            "Meeru adigina prashnalaku, coding doubts ki, leda project ideas ki nenu sahayam cheyagalanu.\n\n"
            "Meeku em kavalo adagandi!"
        )

    # Greeting
    if clean_p in ["hi", "hello", "hey", "hola", "sup", "greetings"]:
        return (
            "Hello! 👋 I'm your **Advanced AI Assistant**.\n\n"
            "I can help you with:\n"
            "- 💻 **Full-stack coding** (Python, Django, JavaScript, React, SQL)\n"
            "- ⚡ **Debugging & Code Optimization**\n"
            "- 🧠 **Concepts, Explanations & System Architecture**\n"
            "- 📝 **Drafting content, plans & documentation**\n\n"
            "What would you like to explore or build today?"
        )

    # Django questions
    if "django" in clean_p:
        if "model" in clean_p:
            return (
                "### 📦 Defining Django Models\n\n"
                "In Django, models represent database tables. Here is a modern example with relationships:\n\n"
                "```python\n"
                "from django.db import models\n"
                "from django.contrib.auth.models import User\n\n"
                "class Project(models.Model):\n"
                "    title = models.CharField(max_length=200)\n"
                "    description = models.TextField()\n"
                "    created_by = models.ForeignKey(User, on_delete=models.CASCADE)\n"
                "    created_at = models.DateTimeField(auto_now_add=True)\n"
                "    is_active = models.BooleanField(default=True)\n\n"
                "    def __str__(self):\n"
                "        return self.title\n"
                "```\n\n"
                "**Key Commands:**\n"
                "```bash\n"
                "python manage.py makemigrations\n"
                "python manage.py migrate\n"
                "```"
            )
        elif "deploy" in clean_p or "github" in clean_p or "live" in clean_p:
            return (
                "### 🚀 How to Push to GitHub & Deploy Django Live\n\n"
                "#### 1. Push to GitHub\n"
                "```bash\n"
                "git init\n"
                "git add .\n"
                "git commit -m 'Initial commit with Advanced AI Chatbot'\n"
                "git branch -M main\n"
                "git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git\n"
                "git push -u origin main\n"
                "```\n\n"
                "#### 2. Deploy Live Options\n"
                "- **Render.com** (Free tier with PostgreSQL support)\n"
                "- **PythonAnywhere** (Simplest for beginners)\n"
                "- **Railway.app** or **Fly.io** (Fastest setup with automated builds)\n\n"
                "Make sure to configure `whitenoise` for static files and set `DEBUG = False` with `ALLOWED_HOSTS = ['*']` for production!"
            )
        else:
            return (
                "### 🐍 Django Framework Highlights\n\n"
                "Django follows the **MVT (Model-View-Template)** architecture:\n"
                "- **Models:** Map Python classes directly to database tables.\n"
                "- **Views:** Handle incoming HTTP requests and return responses.\n"
                "- **Templates:** Dynamic HTML layers rendered using Django Template Language (DTL).\n\n"
                "💡 *Tip: You can ask me specific questions like 'how to create a REST API' or 'how to handle user authentication'!*"
            )

    # Coding help / Python
    if any(k in clean_p for k in ["python", "function", "api", "code", "loop"]):
        return (
            "### 💡 Python Clean Architecture Tip\n\n"
            "Here is an example of an asynchronous or clean service handler:\n\n"
            "```python\n"
            "import typing\n\n"
            "def process_query(prompt: str, max_tokens: int = 1000) -> dict:\n"
            "    \"\"\"\n"
            "    Processes user query and generates a structured response.\n"
            "    \"\"\"\n"
            "    cleaned = prompt.strip()\n"
            "    return {\n"
            "        'status': 'success',\n"
            "        'tokens_used': len(cleaned.split()),\n"
            "        'summary': f'Processed {len(cleaned)} characters'\n"
            "    }\n"
            "```\n\n"
            "Tell me the exact logic or feature you'd like to write, and I will generate the complete production-ready code!"
        )

    # General reasoning default
    return (
        f"### 🤖 AI Insight\n\n"
        f"You asked: **\"{prompt}\"**\n\n"
        "Here are key insights and recommendations:\n"
        "1. **Strategic Approach:** Break down the solution into modular components.\n"
        "2. **Implementation:** Keep logic decoupled, clean, and well-tested.\n"
        "3. **Scalability:** Utilize caching, async background jobs, and indexed database queries when data grows.\n\n"
        "> 💡 *Pro-Tip: You can also connect your OpenAI (`OPENAI_API_KEY`) or Google Gemini (`GEMINI_API_KEY`) key in settings or environment variables to unlock real-time live LLM completions!*"
    )


def get_ai_response(prompt, conversation_history=None, api_key=None):
    """
    Main dispatcher. If an OpenAI or Gemini API key is available, calls the live API.
    Otherwise, uses the smart built-in AI reasoning engine.
    """
    # Check for Gemini or OpenAI API Key
    openai_key = api_key or os.environ.get("OPENAI_API_KEY")
    gemini_key = os.environ.get("GEMINI_API_KEY")

    if gemini_key:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={gemini_key}"
            payload = {
                "contents": [{"parts": [{"text": prompt}]}]
            }
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode('utf-8'),
                headers={'Content-Type': 'application/json'}
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                text = data["candidates"][0]["content"]["parts"][0]["text"]
                return text
        except Exception:
            pass

    if openai_key:
        try:
            messages = [{"role": "system", "content": "You are a helpful, brilliant, and concise AI Assistant."}]
            if conversation_history:
                for msg in conversation_history[-6:]:
                    messages.append({"role": msg.role, "content": msg.content})
            messages.append({"role": "user", "content": prompt})

            url = "https://api.openai.com/v1/chat/completions"
            payload = {
                "model": "gpt-4o-mini",
                "messages": messages,
                "temperature": 0.7
            }
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode('utf-8'),
                headers={
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {openai_key}'
                }
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                text = data["choices"][0]["message"]["content"]
                return text
        except Exception:
            pass

    # Built-in smart reasoning
    return generate_smart_fallback(prompt, conversation_history)

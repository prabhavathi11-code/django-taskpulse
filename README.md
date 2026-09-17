# ⚡ TaskPulse — Modern Django Web Application

[![Django CI/CD Pipeline](https://github.com/prabhavathi11-code/django-taskpulse/actions/workflows/django-ci.yml/badge.svg)](https://github.com/prabhavathi11-code/django-taskpulse/actions)
![Python Version](https://img.shields.io/badge/python-3.11%20%7C%203.12%20%7C%203.13%20%7C%203.14-blue)
![Django](https://img.shields.io/badge/Django-6.1-green)
![License](https://img.shields.io/badge/license-MIT-purple)

A production-ready, beautifully designed Django 6.1 web application for tracking tasks, projects, and sprint goals with live analytics, glassmorphic UI, and built-in GitHub Actions CI/CD.

---

## ✨ Features

- **📊 Live Sprint Metrics**: Instant progress bar, total task count, completed count, and high-priority alerts.
- **⚡ Quick Actions**: One-click status toggling (`Pending` ↔ `Completed`), fast task creation modal, inline editing, and deletion.
- **🔍 Smart Search & Filtering**: Multi-criteria filtering by Category (Work, Personal, Development, Design), Priority (Low, Medium, High), and Status.
- **🎨 Glassmorphic Dark UI**: Built with custom Vanilla CSS variables, Outfit & Plus Jakarta Sans typography, and micro-animations.
- **🚀 Cloud Deployment Ready**: Preconfigured with `WhiteNoise` for zero-overhead static asset serving, `Gunicorn` WSGI runner, and `render.yaml` for 1-click cloud deployment.
- **🤖 GitHub Actions CI**: Automated unit tests and deployment checks on every `git push` and `pull_request`.
- **🩺 Health Check Endpoint**: Live JSON health status probe at `/health/` for uptime monitoring.

---

## 🛠️ Tech Stack

- **Backend**: Python 3.14, Django 6.1.1
- **WSGI / Production Server**: Gunicorn 26.2.0
- **Static Asset Pipeline**: WhiteNoise 6.12.0 with Compressed Manifest storage
- **Database**: SQLite3 (Local development) / PostgreSQL ready
- **Frontend**: Semantic HTML5, CSS3 Glassmorphism, Google Fonts, FontAwesome 6
- **CI/CD**: GitHub Actions

---

## 🚀 Quickstart Guide

### 1. Clone or Open the Repository
```bash
git clone https://github.com/prabhavathi11-code/django-taskpulse.git
cd django-taskpulse
```

### 2. Set Up Virtual Environment
```bash
# Windows
py -m venv .venv
.venv\Scripts\activate

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Seed Initial Tasks (Optional)
```bash
python manage.py seed_sample_data
```

### 6. Start Development Server
```bash
python manage.py runserver
```
Visit `http://127.0.0.1:8000/` in your browser!

---

## 🧪 Running Automated Tests

Run the full Django test suite:
```bash
python manage.py test
```

Run deployment readiness check:
```bash
python manage.py check --deploy
```

---

## 🌐 Cloud Deployment (Render / Railway / Heroku)

### Option A: Deploy on Render
1. Push this repository to your GitHub account (`prabhavathi11-code`).
2. Log into [Render.com](https://render.com) and click **New > Blueprint**.
3. Select this repository. Render will automatically read `render.yaml` and configure:
   - Build Command: `pip install -r requirements.txt && python manage.py collectstatic --no-input && python manage.py migrate`
   - Start Command: `gunicorn config.wsgi:application`
4. Click **Apply** to deploy!

### Option B: Deploy with Procfile
A `Procfile` is already included:
```text
web: gunicorn config.wsgi:application --log-file -
```

---

## 📂 Project Structure

```
django/
├── .github/
│   └── workflows/
│       └── django-ci.yml        # GitHub Actions CI pipeline
├── config/
│   ├── settings.py              # Production & development settings
│   ├── urls.py                  # Root URL routing
│   ├── wsgi.py                  # WSGI entrypoint for Gunicorn
│   └── asgi.py
├── tasks/
│   ├── models.py                # Task data model
│   ├── views.py                 # Dashboard, CRUD, & health endpoints
│   ├── forms.py                 # Form definitions and input widgets
│   ├── urls.py                  # App URL routing
│   ├── admin.py                 # Django admin registration
│   └── tests.py                 # Automated unit tests
├── static/
│   ├── css/style.css            # Modern glassmorphism stylesheet
│   └── js/main.js               # Client interactive behaviors
├── templates/
│   ├── base.html                # Master HTML layout
│   └── tasks/
│       ├── task_list.html       # Main interactive dashboard
│       ├── task_form.html       # Create/edit task form
│       └── task_confirm_delete.html # Deletion confirmation view
├── .env.example                 # Environment variables template
├── .gitignore                   # Standard Python/Django gitignore
├── Procfile                     # PaaS process file
├── render.yaml                  # 1-Click Render blueprint
├── requirements.txt             # Pinned project dependencies
└── manage.py                    # Django CLI management script
```

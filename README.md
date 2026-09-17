# ⚡ TaskPulse — Django Project & Task Manager

[![Django CI/CD Pipeline](https://github.com/prabhavathi11-code/django-taskpulse/actions/workflows/django-ci.yml/badge.svg)](https://github.com/prabhavathi11-code/django-taskpulse/actions)
![Python Version](https://img.shields.io/badge/python-3.11%20%7C%203.12%20%7C%203.13%20%7C%203.14-blue)
![Django](https://img.shields.io/badge/Django-6.1-green)
![License](https://img.shields.io/badge/license-MIT-purple)

**TaskPulse** is a full-stack Django 6.1 web application designed for agile task tracking, engineering sprint management, and productivity metrics. Features a responsive dark glassmorphic UI, real-time analytics, automated testing, and CI/CD deployment workflows.

---

## 🔗 Local Host URLs & Application Access

When the Django development server is running locally (`python manage.py runserver`), access the application at:

| Service | Local URL | Description |
| :--- | :--- | :--- |
| 🌐 **Main Dashboard** | [http://localhost:8000/](http://localhost:8000/) or [http://127.0.0.1:8000/](http://127.0.0.1:8000/) | Live sprint metrics, search, filter, and task management |
| 🩺 **Health Check** | [http://127.0.0.1:8000/health/](http://127.0.0.1:8000/health/) | JSON health status probe for uptime monitoring |
| ⚙️ **Django Admin** | [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) | Administrative management portal |

---

## ✨ Key Features

- **📊 Live Sprint Metrics**: Instant progress bar with total, completed, pending, and high-priority counters.
- **⚡ One-Click Actions**: Quick status toggle (`Pending` ↔ `Completed`), fast task creation modal, inline editing, and deletion.
- **🔍 Smart Search & Filtering**: Multi-attribute filtering across category (Work, Personal, Development, Design), priority, and status.
- **🎨 Glassmorphic Dark UI**: Custom CSS3 design system with vibrant accents, responsive cards, and micro-animations.
- **⚡ Database Optimization**: Database-level indexing on `status`, `priority`, `category`, and `created_at` for high-throughput queries.
- **🔒 Secure Architecture**: Strict HTTP method guards (`@require_POST`, `@require_http_methods`), CSRF validation, and environment-based settings.
- **🚀 Production Ready**: Configured with WhiteNoise for compressed static asset serving, Gunicorn WSGI server, and GitHub Actions CI pipeline.

---

## 🛠️ Technology Stack

| Layer | Technologies Used |
| :--- | :--- |
| **Backend** | Python 3.14, Django 6.1.1 (MVT architecture, ORM, ModelForms) |
| **Frontend** | HTML5 Semantic layout, Vanilla CSS3 (Glassmorphism, CSS variables), JavaScript |
| **Database** | SQLite3 (Local development) / PostgreSQL ready |
| **WSGI / Production** | Gunicorn 26.2.0, WhiteNoise 6.12.0 (Manifest static compression) |
| **CI/CD & DevOps** | Git, GitHub Actions (`.github/workflows/django-ci.yml`), Render Blueprint (`render.yaml`) |
| **Testing** | Django Test Framework (10/10 automated unit tests passing) |

---

## 🔗 URL Routing Reference

| Endpoint | Method | Handler | Purpose |
| :--- | :--- | :--- | :--- |
| `/` | `GET` | `tasks:list` | Main task dashboard with metrics and filters |
| `/tasks/create/` | `GET`, `POST` | `tasks:create` | Task creation form |
| `/tasks/<id>/edit/` | `GET`, `POST` | `tasks:update` | Update existing task details |
| `/tasks/<id>/delete/` | `GET`, `POST` | `tasks:delete` | Confirm and delete task |
| `/tasks/<id>/toggle/` | `POST` | `tasks:toggle` | Instant completion toggle |
| `/health/` | `GET` | `tasks:health` | JSON health probe endpoint |
| `/admin/` | `GET`, `POST` | Django Admin | Secure administrative portal |

---

## 📂 Project Directory Structure

```text
django/
├── .github/
│   └── workflows/
│       └── django-ci.yml        # GitHub Actions CI matrix pipeline
├── config/
│   ├── settings.py              # Environment settings & WhiteNoise config
│   ├── urls.py                  # Main routing configuration
│   └── wsgi.py                  # WSGI entrypoint for Gunicorn
├── tasks/
│   ├── admin.py                 # Admin dashboard with list_editable
│   ├── apps.py                  # Django app config
│   ├── forms.py                 # Form validation & widgets
│   ├── models.py                # Indexed Task data model
│   ├── tests.py                 # 10 automated unit tests
│   ├── urls.py                  # App URL routing
│   ├── views.py                 # View controllers with HTTP method guards
│   └── management/
│       └── commands/
│           └── seed_sample_data.py # Sample data seeder
├── static/
│   ├── css/style.css            # Glassmorphic dark design system
│   └── js/main.js               # Modal and toast notification scripts
├── templates/
│   ├── base.html                # Responsive layout wrapper
│   └── tasks/
│       ├── task_list.html       # Interactive dashboard
│       ├── task_form.html       # Create/edit views
│       └── task_confirm_delete.html
├── .env.example                 # Environment variables template
├── .gitignore                   # Git ignore specifications
├── Procfile                     # Production PaaS process definition
├── render.yaml                  # 1-Click Render blueprint
├── requirements.txt             # Pinned dependency requirements
└── manage.py                    # Django management script
```

---

## 👤 Author & Contact

- **Developer**: Prabhavathi Chirumala
- **GitHub**: [@prabhavathi11-code](https://github.com/prabhavathi11-code)
- **Repository**: [django-taskpulse](https://github.com/prabhavathi11-code/django-taskpulse)

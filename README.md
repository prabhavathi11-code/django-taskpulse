# ⚡ TaskPulse — Django Project & Task Manager

[![Django CI/CD Pipeline](https://github.com/prabhavathi11-code/django-taskpulse/actions/workflows/django-ci.yml/badge.svg)](https://github.com/prabhavathi11-code/django-taskpulse/actions)
![Python Version](https://img.shields.io/badge/python-3.11%20%7C%203.12%20%7C%203.13%20%7C%203.14-blue)
![Django](https://img.shields.io/badge/Django-6.1-green)
![License](https://img.shields.io/badge/license-MIT-purple)

**TaskPulse** is a full-stack Django 6.1 web application designed for agile task tracking, engineering sprint management, and productivity metrics. Features a responsive dark glassmorphic UI, real-time analytics, automated testing, and CI/CD deployment workflows.

---

## 🌐 Live Demo & Application Access

| Service | URL | Access Notes |
| :--- | :--- | :--- |
| 🚀 **Live Demo (Render)** | [https://taskpulse-django.onrender.com](https://taskpulse-django.onrender.com) | **Permanent Live URL** — Always accessible |
| 💻 **Local Dashboard** | [http://localhost:8000/](http://localhost:8000/) | Local sprint metrics, search & filter |
| 🩺 **Health Check (Live)** | [https://taskpulse-django.onrender.com/health/](https://taskpulse-django.onrender.com/health/) | JSON health status probe |
| 🩺 **Health Check (Local)** | [http://127.0.0.1:8000/health/](http://127.0.0.1:8000/health/) | Local JSON health status probe |
| ⚙️ **Django Admin (Live)** | [https://taskpulse-django.onrender.com/admin/](https://taskpulse-django.onrender.com/admin/) | Administrative management portal |

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
TaskPulse/
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

## 🗄️ Database Architecture & Schema

The core data model is [`Task`](file:///c:/Users/ch%20prabahavathi/OneDrive/Desktop/django/tasks/models.py) which encapsulates engineering sprint workflows:

| Field | Type | Attributes & Choices | Purpose |
| :--- | :--- | :--- | :--- |
| `title` | `CharField(200)` | Required, indexed | Short descriptive task title |
| `description` | `TextField` | Optional (`blank=True`) | Detailed acceptance criteria & context |
| `status` | `CharField(20)` | `pending` (default), `completed` | Workflow lifecycle tracking |
| `priority` | `CharField(20)` | `low`, `medium` (default), `high` | Task urgency ranking |
| `category` | `CharField(20)` | `work`, `personal`, `dev`, `design` | Functional domain categorization |
| `due_date` | `DateField` | Optional (`null=True`, `blank=True`) | Target completion date |
| `created_at` | `DateTimeField` | Auto-set on create (`auto_now_add=True`) | Audit trail & sorting |
| `updated_at` | `DateTimeField` | Auto-set on save (`auto_now=True`) | Modification timestamp |

> **⚡ Performance Optimization:** Database indexes (`models.Index`) are applied across `status`, `priority`, `category`, and `created_at` for high-concurrency filtering.

---

## 🧪 Automated Testing & Quality Assurance

TaskPulse includes an automated test suite in [`tasks/tests.py`](file:///c:/Users/ch%20prabahavathi/OneDrive/Desktop/django/tasks/tests.py) covering 10 distinct test scenarios:

```bash
# Run test suite
python manage.py test
```

- ✅ `test_task_creation_and_string_representation`: Validates model integrity and `__str__` format.
- ✅ `test_dashboard_renders_metrics_and_tasks`: Checks dashboard status `200 OK` and template context metrics.
- ✅ `test_task_create_view_post`: Tests task creation flow and automatic redirection.
- ✅ `test_task_update_view`: Tests updating existing task metadata and fields.
- ✅ `test_task_delete_view`: Confirms deletion and count reduction.
- ✅ `test_task_toggle_status`: Validates `@require_POST` fast status toggling between `pending` and `completed`.
- ✅ `test_filter_tasks_by_status`: Ensures status query filtering returns accurate subsets.
- ✅ `test_filter_tasks_by_priority`: Validates priority filtering logic.
- ✅ `test_search_tasks_by_query`: Tests case-insensitive search across title and description.
- ✅ `test_health_check_endpoint`: Verifies `/health/` returns JSON `200 OK` with database health status.

---

## 🎤 Interview & Project Presentation Guide

### Key Points to Highlight:
1. **MVT Architecture:** Clean separation of concerns between Models (ORM schema & indexes), Views (method guards & query sets), and Templates (semantic glassmorphism).
2. **Security Practices:** CSRF validation across all endpoints, strict HTTP method decorators (`@require_POST`), and parameterized ORM queries preventing SQL injection.
3. **Responsive Glassmorphism:** Crafted with CSS variables, backdrop blur filters, and micro-animations without heavy CSS framework bloat.
4. **DevOps Ready:** Built with WhiteNoise manifest compression, Gunicorn WSGI, GitHub Actions CI matrix, and live cloud deployment blueprints.

---

## 👤 Author & Contact

- **Developer**: Prabhavathi Chirumala
- **GitHub**: [@prabhavathi11-code](https://github.com/prabhavathi11-code)
- **Repository**: [django-taskpulse](https://github.com/prabhavathi11-code/django-taskpulse)

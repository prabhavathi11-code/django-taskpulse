# ⚡ TaskPulse — Modern Full-Stack Django Web Application

[![Django CI/CD Pipeline](https://github.com/prabhavathi11-code/django-taskpulse/actions/workflows/django-ci.yml/badge.svg)](https://github.com/prabhavathi11-code/django-taskpulse/actions)
![Python Version](https://img.shields.io/badge/python-3.11%20%7C%203.12%20%7C%203.13%20%7C%203.14-blue)
![Django](https://img.shields.io/badge/Django-6.1-green)
![License](https://img.shields.io/badge/license-MIT-purple)
![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-brightgreen.svg)

A production-grade, full-stack **Django 6.1** web application engineered for tracking engineering sprints, daily productivity, and project milestones. Features real-time completion analytics, dynamic multi-attribute filtering, glassmorphic dark UI, automated unit testing, and continuous deployment pipelines (CI/CD).

---

## 📖 About The Project

In fast-paced software development and agile workflows, teams and developers often struggle with complex, bloated project management software. **TaskPulse** provides a lightweight, blazingly fast, and aesthetically pleasing task management dashboard.

### Why TaskPulse?
- **Zero Configuration Friction**: Built-in sample data seeding allows developers to test features with a single command.
- **Enterprise-Grade Architecture**: Strictly adheres to Django's **MVT (Model-View-Template)** pattern with decoupled logic, reusable components, and comprehensive unit tests.
- **Cloud-Native & Production-Ready**: Comes preconfigured with **WhiteNoise** for compressed static asset serving, **Gunicorn** WSGI HTTP server, and automatic **Render / Railway** blueprint deployment.

---

## 🧠 Key Skills & Technologies Demonstrated

| Category | Skills & Tools Used |
| :--- | :--- |
| **Backend Engineering** | Python 3.14, Django 6.1, Django MVT, Django ORM, RESTful JSON health endpoint |
| **Frontend Development** | HTML5 Semantic layout, Vanilla CSS3 (Glassmorphism, CSS Custom Properties/Variables, Flexbox/Grid), JavaScript (DOM, Modals, Toasts) |
| **Testing & Quality Assurance** | Django Test Framework, Automated Unit Tests (10/10 passing), System checks |
| **DevOps & CI/CD** | Git Version Control, GitHub Actions Workflow Matrix, Automated testing on push/PR |
| **Production Serving** | WhiteNoise 6.12 (Manifest Static Storage & Gzip/Brotli compression), Gunicorn 26.2 |
| **Deployment** | `render.yaml` infrastructure-as-code, `Procfile`, `.env` configuration |

---

## ✨ Features & Capabilities

- **📊 Live Sprint Metrics**: Dynamically calculated metrics banner displaying total tasks, completed tasks, pending/in-progress counts, and high-priority alarms with an animated completion rate bar.
- **⚡ Quick One-Click Actions**: Toggle task completion status (`Pending` ↔ `Completed`) with a single click, open quick-add modal, or perform inline edits and safe deletion.
- **🔍 Multi-Factor Search & Filtering**:
  - Full-text search across titles and descriptions.
  - Status filter: `All`, `Pending`, `In Progress`, `Completed`.
  - Priority filter: `Low`, `Medium`, `High`.
  - Category filter: `Work`, `Personal`, `Development`, `Design`, `Other`.
- **🎨 Glassmorphic Dark UI**: High-contrast, accessibility-aware dark mode with translucent acrylic cards (`backdrop-filter: blur(12px)`), vibrant neon accents, and micro-animations.
- **🩺 Health & Uptime Probe**: Lightweight JSON endpoint at `/health/` for synthetic monitoring and load balancer health checks.

---

## 🗄️ Data Architecture & Schema

The core model is defined in `tasks/models.py`:

```
+-------------------------------------------------------------+
|                            Task                             |
+-------------------------------------------------------------+
| id          : BigAutoField (Primary Key)                    |
| title       : CharField(max_length=200)                     |
| description : TextField(blank=True)                         |
| priority    : CharField(choices: LOW, MEDIUM, HIGH)         |
| status      : CharField(choices: PENDING, IN_PROGRESS, ...) |
| category    : CharField(choices: Work, Personal, Dev, ...)  |
| due_date    : DateField(null=True, blank=True)              |
| created_at  : DateTimeField(auto_now_add=True)              |
| updated_at  : DateTimeField(auto_now=True)                  |
+-------------------------------------------------------------+
```

### Model Properties:
- `is_completed`: Returns boolean based on whether task status is `COMPLETED`.
- `is_overdue`: Compares `due_date` against `timezone.now().date()` to flag delayed deliverables.

---

## 🔗 URL Routing & API Endpoints

| Endpoint | HTTP Method | View Function | Description |
| :--- | :--- | :--- | :--- |
| `/` | `GET` | `tasks:list` | Main interactive dashboard with metrics & filters |
| `/tasks/create/` | `GET`, `POST` | `tasks:create` | Form page to create a new task |
| `/tasks/<id>/edit/` | `GET`, `POST` | `tasks:update` | Update details of an existing task |
| `/tasks/<id>/delete/`| `GET`, `POST` | `tasks:delete` | Confirmation and deletion of task |
| `/tasks/<id>/toggle/`| `POST` | `tasks:toggle` | Instant status toggle between Pending & Completed |
| `/health/` | `GET` | `tasks:health` | JSON health probe (`status`, `database`, `total_tasks`) |
| `/admin/` | `GET`, `POST` | Django Admin | Administrative management portal |

---

## 🛠️ Tech Stack & Dependencies

- **Python**: `3.14.7` (Supports 3.11+)
- **Django**: `6.1.1`
- **WSGI Runner**: `Gunicorn 26.2.0`
- **Static Compression**: `WhiteNoise 6.12.0`
- **SQL Parser**: `sqlparse 0.6.0`
- **Database**: SQLite3 (Local) / PostgreSQL Ready (Production)

---

## 🔗 Local Host URLs & Application Access

When the development server is running locally, access the application via:

- 🌐 **Web App Dashboard**: [http://localhost:8000/](http://localhost:8000/) or [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- 🩺 **Health Check Endpoint**: [http://127.0.0.1:8000/health/](http://127.0.0.1:8000/health/)
- ⚙️ **Django Admin Portal**: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)


---

## 📂 Repository Directory Structure

```
django/
├── .github/
│   └── workflows/
│       └── django-ci.yml        # GitHub Actions CI/CD pipeline
├── config/
│   ├── settings.py              # Environment & WhiteNoise settings
│   ├── urls.py                  # Main routing entrypoint
│   ├── wsgi.py                  # WSGI config for Gunicorn
│   └── asgi.py                  # ASGI config
├── tasks/
│   ├── admin.py                 # Admin dashboard configuration
│   ├── apps.py                  # Tasks application configuration
│   ├── forms.py                 # ModelForm validation rules
│   ├── models.py                # Task database schema
│   ├── tests.py                 # 10 Automated unit tests
│   ├── urls.py                  # App-level routing
│   ├── views.py                 # Views, metrics calculations & health probe
│   └── management/
│       └── commands/
│           └── seed_sample_data.py # Sample data seeder
├── static/
│   ├── css/
│   │   └── style.css            # Dark glassmorphic design system
│   └── js/
│       └── main.js              # Modal, toasts, and keyboard events
├── templates/
│   ├── base.html                # Master layout with navbar and footer
│   └── tasks/
│       ├── task_list.html       # Dashboard with metric cards & filters
│       ├── task_form.html       # Create & edit views
│       └── task_confirm_delete.html # Safe deletion confirmation
├── .env.example                 # Environment variables template
├── .gitignore                   # Ignore rules for git
├── Procfile                     # PaaS process file
├── render.yaml                  # 1-Click Render blueprint
├── requirements.txt             # Pinned project dependencies
└── manage.py                    # Django command-line utility
```

---

## 👤 Author & Contact

- **Developer**: Prabhavathi Chirumala
- **GitHub**: [@prabhavathi11-code](https://github.com/prabhavathi11-code)
- **Email**: `prabhavathichirumala326@gmail.com`
- **Project Repository**: [django-taskpulse](https://github.com/prabhavathi11-code/django-taskpulse)

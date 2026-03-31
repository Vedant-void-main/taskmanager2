<<<<<<< HEAD
# ✦ TaskMaster — Setup Guide

A full-stack Django task management + birthday/anniversary reminder system
with real-time browser notifications, dark mode, and a polished UI.

---

## 📦 Requirements
- Python 3.8+
- pip

---

## 🚀 Quick Start (3 commands)

```bash
# 1. Install Django
pip install -r requirements.txt

# 2. Set up the database
python manage.py migrate

# 3. Run the server
python manage.py runserver
```

Then open: **http://127.0.0.1:8000**

---

## 🔐 Create Admin (optional)
```bash
python manage.py createsuperuser
```
Admin panel: http://127.0.0.1:8000/admin/

---

## 📁 Project Structure

```
taskmaster/
├── manage.py
├── requirements.txt
├── taskmaster/          ← Django project config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── apps/
│   ├── users/           ← Auth, profiles, dark mode
│   │   ├── models.py    → UserProfile
│   │   ├── views.py     → register, login, logout, toggle_dark_mode
│   │   ├── forms.py
│   │   ├── signals.py   → auto-create profile on user creation
│   │   └── urls.py
│   ├── tasks/           ← Task CRUD + dashboard
│   │   ├── models.py    → Task (title, desc, priority, due_date, status)
│   │   ├── views.py     → dashboard, list, create, edit, delete, toggle
│   │   ├── forms.py
│   │   ├── urls.py
│   │   └── dashboard_urls.py
│   └── reminders/       ← Birthday/anniversary/custom reminders
│       ├── models.py    → Reminder (title, type, date, time)
│       ├── views.py     → list, create, edit, delete
│       ├── forms.py
│       └── urls.py
├── templates/
│   ├── base.html        ← Sidebar, topbar, dark mode toggle, notification panel
│   ├── users/           ← login, register, password reset templates
│   ├── tasks/           ← dashboard, task_list, task_edit
│   └── reminders/       ← reminder_list, reminder_edit
└── static/
    ├── css/main.css     ← Full design system with dark mode
    └── js/main.js       ← Dark mode, AJAX task toggle, notification polling
```

---

## ✨ Features

### Tasks
- Create / edit / delete tasks
- Priority: Low / Medium / High (color-coded)
- Due date + time
- Mark complete (AJAX — no page reload)
- Filter by status + priority
- Overdue & "due soon" badges

### Reminders
- Types: Birthday 🎂 / Anniversary 💍 / Custom 🔔
- Recurring yearly (matches month+day each year)
- "Days away" countdown on each card
- Today's events highlighted with animation

### Notifications
- Browser popup (Notification API) for due tasks + today's events
- In-app notification panel (bell icon in topbar)
- Toast messages for all actions
- Polls `/tasks/notifications/` every 60 seconds via AJAX

### UI
- Sidebar navigation with user avatar
- Dashboard with 4 stat cards + progress bar
- Dark mode toggle (persisted in localStorage + DB)
- Responsive for mobile
- Smooth animations throughout

### Auth
- Register / Login / Logout
- Password reset (emails print to console in dev)

---

## ⚙️ Configuration

Edit `taskmaster/settings.py`:

- `TIME_ZONE` — change from `'Asia/Kolkata'` to your timezone
- `EMAIL_BACKEND` — swap to SMTP for real password reset emails
- `SECRET_KEY` — change before deploying to production
- `DEBUG = False` for production

---

## 🎨 Customization

- Colors: Edit CSS variables in `static/css/main.css` `:root` block
- Notification poll interval: Change `60000` (ms) in `static/js/main.js`
- Add more reminder types: Update `TYPE_CHOICES` in `apps/reminders/models.py`
=======
# taskmanager
TaskMaster is a Django-based task management and reminder system that allows users to create, manage, and track tasks efficiently. It includes user authentication, task priority, reminders, and a dashboard to monitor productivity.
>>>>>>> 9354a491c4e247753c813f972da7f46b98e640c6

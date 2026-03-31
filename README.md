# Task Manager — Setup Guide

A simple Django task management system built for learning Django fundamentals.

---

## Run in 4 steps

```
# Step 1 — Install Django
pip install -r requirements.txt

# Step 2 — Create the database tables
python manage.py migrate

# Step 3 — (Optional) Create an admin account
python manage.py createsuperuser

# Step 4 — Start the server
python manage.py runserver
```

Open your browser at: http://127.0.0.1:8000/login/

---

## What each file does

```
simple_taskmanager/
│
├── manage.py               ← Entry point to run Django commands
├── requirements.txt        ← Python packages needed
│
├── taskmanager/            ← Project configuration
│   ├── settings.py         ← All Django settings
│   └── urls.py             ← URL routes for the whole project
│
├── tasks/                  ← Our main app
│   ├── models.py           ← Task database model
│   ├── views.py            ← Page logic (what happens when you visit a URL)
│   ├── forms.py            ← Signup and task forms
│   ├── admin.py            ← Register models for admin panel
│   └── migrations/         ← Database migration files (auto-generated)
│
├── templates/              ← HTML files
│   ├── base.html           ← Shared layout (navbar etc.)
│   ├── login.html          ← Login page
│   ├── signup.html         ← Signup page
│   ├── dashboard.html      ← Main dashboard with task list
│   └── tasks/
│       ├── add_task.html       ← Add new task form
│       └── confirm_delete.html ← Delete confirmation page
│
└── static/
    └── css/style.css       ← All styles
```

---

## Pages and URLs

| URL                        | What it does               |
|----------------------------|----------------------------|
| /login/                    | Login page                 |
| /signup/                   | Create a new account       |
| /logout/                   | Logs you out               |
| /dashboard/                | Shows all your tasks       |
| /dashboard/?filter=pending | Shows only pending tasks   |
| /dashboard/?filter=completed | Shows completed tasks    |
| /dashboard/?filter=today   | Shows today's tasks        |
| /tasks/add/                | Add a new task             |
| /tasks/complete/1/         | Toggle task 1 complete     |
| /tasks/delete/1/           | Delete task 1              |
| /admin/                    | Django admin panel         |

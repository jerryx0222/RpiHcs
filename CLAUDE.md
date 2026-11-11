# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

A small Django 6.1 project (`RpiHcs` project + `main` app) using SQLite (`db.sqlite3` at the repo root).

- `RpiHcs/` — project package (settings, root URLconf, wsgi/asgi).
- `main/` — the only app. Home page (`/`, `@login_required`) shows a "啟動unraid" button that currently has no action wired up. Templates live in `main/templates/` (`main/home.html`, `registration/login.html`).
- `Rpi/` — the Python 3.12 virtualenv, inside the project directory. Its `pip list` includes ROS 2 packages (`*-msgs`, `ament-*`); treat it as environment, not source. Don't edit or search inside it.
- `requirements.txt` — only `Django==6.1.3`. Don't regenerate it with `pip freeze` (the ROS packages would pollute it).

## Commands

Activate the venv with `source Rpi/bin/activate` (or call `Rpi/bin/python` directly):

```
python manage.py runserver          # dev server
python manage.py makemigrations     # after model changes
python manage.py migrate
python manage.py createsuperuser    # needed to log in if no known user exists
python manage.py test               # all tests
python manage.py test main.tests.HomeTests.test_home_requires_login   # single test
pip install -r requirements.txt
```

No linter or formatter is configured.

## Things to know

- Auth uses Django's built-in views: [RpiHcs/urls.py](RpiHcs/urls.py) includes `django.contrib.auth.urls` under `accounts/`, and the custom login template is `registration/login.html`. `LOGIN_URL`, `LOGIN_REDIRECT_URL` and `LOGOUT_REDIRECT_URL` are set at the bottom of [RpiHcs/settings.py](RpiHcs/settings.py). Logout is POST-only (Django 5+), so the home page uses a form.
- Settings are dev defaults: `DEBUG = True`, `ALLOWED_HOSTS = []`, hardcoded insecure `SECRET_KEY`. `MAILERS` in settings is not a real Django setting (the real one is `EMAIL_BACKEND`), so it has no effect.
- `TIME_ZONE = 'UTC'`, `LANGUAGE_CODE = 'en-us'`.

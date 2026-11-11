# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

A freshly scaffolded Django 6.1 project (`django-admin startproject RpiHcs` + `startapp main`), not yet customized. SQLite database (`db.sqlite3`) at the repo root. Not a git repository.

- `RpiHcs/` — project package (settings, root URLconf, wsgi/asgi).
- `main/` — the only app; `models.py`, `views.py`, `admin.py`, `tests.py` are still empty stubs and there are no migrations beyond `__init__.py`.
- `Rpi/` — the Python 3.12 virtualenv (checked into the project directory). Its `pip list` includes ROS 2 packages (`*-msgs`, `ament-*`), so the venv likely uses system site packages or ROS tooling; treat it as environment, not source. Don't edit or search inside it.

## Commands

Use the venv's Python (or activate it with `source Rpi/bin/activate`):

```
Rpi/bin/python manage.py runserver          # dev server
Rpi/bin/python manage.py makemigrations     # after model changes
Rpi/bin/python manage.py migrate
Rpi/bin/python manage.py test               # all tests
Rpi/bin/python manage.py test main.tests.ClassName.test_name   # single test
```

No linter, formatter, or requirements file is configured.

## Things to know

- `main` is **not yet in `INSTALLED_APPS`** in [RpiHcs/settings.py](RpiHcs/settings.py). Add `'main'` (or `'main.apps.MainConfig'`) before its models/migrations/tests will be picked up.
- [RpiHcs/urls.py](RpiHcs/urls.py) only routes `admin/`; app views need to be wired in there (e.g. via `include('main.urls')`, which doesn't exist yet).
- Settings are dev defaults: `DEBUG = True`, `ALLOWED_HOSTS = []`, hardcoded insecure `SECRET_KEY`. `MAILERS` in settings is not a real Django setting (the real one is `EMAIL_BACKEND`), so it has no effect.
- `TIME_ZONE = 'UTC'`, `LANGUAGE_CODE = 'en-us'`.

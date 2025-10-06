# Thrift Management System - Thrift_MS

**A Django-based API for managing community thrift (ajo) groups — local development with MySQL.**

---

## Table of contents

1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Tech Stack](#tech-stack)
4. [Project Structure](#project-structure)
5. [Prerequisites](#prerequisites)
6. [Environment & Configuration](#environment--configuration)
7. [Database (MySQL) Setup](#database-mysql-setup)
8. [Install & Run (Local)](#install--run-local)
9. [Django Management Tasks](#django-management-tasks)
10. [API Endpoints & Examples](#api-endpoints--examples)
11. [Authentication](#authentication)
12. [Testing with Postman / curl](#testing-with-postman--curl)
13. [Optional: Temporary Public Access (Ngrok)](#optional-temporary-public-access-ngrok)
14. [Common Issues & Tips](#common-issues--tips)
15. [Recommended Commits & Changelog Notes](#recommended-commits--changelog-notes)
16. [Next Steps & Deployment Notes](#next-steps--deployment-notes)
17. [Credits & License](#credits--license)

---

## Project overview

`thrift_ms` is a backend API built with **Django** and **Django REST Framework (DRF)** that digitizes community thrift (ajo) groups. The API supports creating and joining thrift groups, tracking regular contributions, and recording payouts. The project uses a **custom user model** (extends `AbstractUser`) and **MySQL** as the local database.

This README explains how to set up and run the project locally, how the API is structured, and examples for testing endpoints.

---

## Features

### MVP (implemented)

* User registration and authentication
* Custom `User` model (extra fields: phone, account_number, bank_name, account_name)
* Create and manage thrift groups (admin creates a group)
* Membership management (users can join groups)
* Record contributions (payments made by members)
* Record payouts and payout order
* Dashboard endpoints for members (summary)

### Secondary / Stretch (notes)

* Role-based permissions (Admin vs Member)
* Email/SMS reminders
* Online payments integrations (Paystack / Flutterwave)
* Automated payout rotation

---

## Tech stack

* Python 3.10+ (use `python --version` to confirm)
* Django (>=4.x)
* Django REST Framework
* MySQL (local)
* `mysqlclient` Python package
* I also used `python-decouple` (for environment variables)

---

## Project structure (example)

```
thrift_ms/
├── accounts/                  # custom user app (models, serializers, views)
├── thrift/                    # thrift groups, memberships, contributions, payouts
├── dashboard/                 # (coming) user dashboard and reporting endpoints
├── payments/                  # (future) payment integrations
├── thrift_ms/                 # django project settings, wsgi, urls
├── manage.py
├── requirements.txt
├── Procfile (optional)
├── runtime.txt (optional)
└── README.md
```

---

## Prerequisites

1. Python 3.10+ installed
2. MySQL server installed and running locally
3. Virtual environment tool (`venv`) recommended
4. Git installed

---

## Environment & configuration

Create and use a Python virtual environment:

```bash
python -m venv venv
source venv/bin/activate   # linux / mac
venv\Scripts\activate     # windows
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Example `requirements.txt`:

```
Django
djangorestframework
mysqlclient
gunicorn
python-decouple
```

### Environment variables (.env)

Create a `.env` file in the project root (do **not** commit this file):

```
# Django
SECRET_KEY=your_django_secret_key_here
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

# MySQL (local)
DB_NAME=thrift_management_system
DB_USER=root
DB_PASSWORD=your_local_mysql_password
DB_HOST=127.0.0.1
DB_PORT=3306
```

Load these values in `settings.py` (recommended):

```python
from decouple import config

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='3306'),
    }
}
```

If you are not using `python-decouple`, you can use `os.getenv()` instead — still keep secrets out of source control.

---

## Database (MySQL) Setup (local)

If you haven't created the database yet, do it in MySQL shell or via a GUI:

```sql
CREATE DATABASE thrift_management_system CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'thrift_user'@'localhost' IDENTIFIED BY 'secure_password_here';
GRANT ALL PRIVILEGES ON thrift_management_system.* TO 'thrift_user'@'localhost';
FLUSH PRIVILEGES;
```

Update `.env` with these credentials. Then run Django migrations (see next section).

---

## Install & Run (Local)

1. Activate your virtual environment.
2. Install dependencies: `pip install -r requirements.txt`.
3. Set up `.env` (as shown above).
4. Run migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

5. Create superuser (for admin and testing):

```bash
python manage.py createsuperuser
# follow interactive prompts
```

6. Run the development server:

```bash
python manage.py runserver
```

Open the API root: `http://127.0.0.1:8000/api/`

---

## Django management tasks (common)

* Make migrations: `python manage.py makemigrations`
* Apply migrations: `python manage.py migrate`
* Create superuser: `python manage.py createsuperuser`
* Collect static (if needed): `python manage.py collectstatic`
* Run server: `python manage.py runserver`

---

## API Endpoints & Examples

> **Base path**: `http://127.0.0.1:8000/api/`

> Replace with your paths if you used another router prefix.

### Accounts & Authentication

* `POST /api/accounts/register/` — Register new user (`AllowAny`)

  * Example body:

    ```json
    {
      "username": "Alphakeem",
      "password": "supersecure123",
      "email": "john@example.com",
      "phone": "08123456789"
    }
    ```

* `POST /api/token/` (SimpleJWT) — Obtain JWT pair (if you use SimpleJWT)

  * Body: `{ "username": "Alphakeem", "password": "supersecure123" }`

* `POST /api/api-token-auth/` (DRF TokenAuth) — Obtain token (if you use DRF TokenAuth)

  * Body: `{ "username": "Alphakeem", "password": "supersecure123" }`

* `GET /api/accounts/users/` — List all users (Admin only)

* `GET /api/accounts/me/` — Retrieve logged-in user profile (Authenticated)

* `PATCH /api/accounts/me/` — Update logged-in user profile (Authenticated)

### Thrift Groups

* `GET /api/thrift-groups/` — List groups
* `POST /api/thrift-groups/` — Create a new group

  * Example body:

    ```json
    {
      "name": "Two Million Pack",
      "contribution_amount": "200000.00",
      "cycle": "monthly",
      "admin": 1
    }
    ```
* `GET /api/thrift-groups/{id}/` — Group details
* `PATCH /api/thrift-groups/{id}/` — Update group (admin only)
* `DELETE /api/thrift-groups/{id}/` — Delete group (admin only)

### Memberships

* `GET /api/memberships/` — List memberships (or your groups)
* `POST /api/memberships/` — Join a group

  * Example body: `{ "user": 2, "group": 1 }`
* `GET /api/memberships/{id}/` — Membership detail
* `PATCH /api/memberships/{id}/` — Update membership (admin only)
* `DELETE /api/memberships/{id}/` — Leave group

### Contributions

* `GET /api/contributions/` — List contributions
* `POST /api/contributions/` — Record a contribution

  * Example: `{ "member": 1, "amount": "200000.00", "status": "paid" }`
* `GET /api/contributions/{id}/` — Contribution detail
* `PATCH /api/contributions/{id}/` — Edit contribution (admin only)
* `DELETE /api/contributions/{id}/` — Delete contribution (admin only)

### Payouts

* `GET /api/payouts/` — List payouts
* `POST /api/payouts/` — Record a payout

  * Example: `{ "member": 1, "amount": "2000000.00", "order": 1 }`
* `GET /api/payouts/{id}/` — Payout detail
* `PATCH /api/payouts/{id}/` — Update payout (admin only)
* `DELETE /api/payouts/{id}/` — Delete payout (admin only)

> **Headers**: For protected endpoints include either:
>
> * `Authorization: Token <your_token>` (DRF TokenAuth)
> * `Authorization: Bearer <your_access_token>` (JWT SimpleJWT)

---

## Authentication (Notes)

* You have a **custom user model** defined in `accounts.models.User`. Ensure `settings.py` includes:

```python
AUTH_USER_MODEL = 'accounts.User'
```

* For token-based flow, either use DRF TokenAuth or SimpleJWT. Example with SimpleJWT:

```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}
```

When testing locally, you may temporarily set `DEFAULT_PERMISSION_CLASSES` to `AllowAny` while building features.

---

## Testing with Postman / curl

**Register (curl)**

```bash
curl -X POST http://127.0.0.1:8000/api/accounts/register/ \
-H "Content-Type: application/json" \
-d '{"username":"johndoe","password":"test1234","email":"john@example.com"}'
```

**Obtain DRF Token (if enabled)**

```bash
curl -X POST http://127.0.0.1:8000/api/api-token-auth/ \
-H "Content-Type: application/json" \
-d '{"username":"johndoe","password":"test1234"}'
```

**Authorized request example**

```bash
curl -H "Authorization: Token <token>" http://127.0.0.1:8000/api/thrift-groups/
```

Use Postman variables to store tokens for convenience.

---

## Optional: Temporary Public Access (Ngrok)

If you want someone to test while your machine is online, use Ngrok to expose your local server briefly:

```bash
python manage.py runserver
ngrok http 8000
```

Share the HTTPS URL Ngrok provides. Keep in mind the tunnel is temporary and closes when you stop ngrok.

---

## Common issues & troubleshooting

* **`ImportError: MySQLdb`** → install `mysqlclient`:

  ```bash
  pip install mysqlclient
  ```
* **`No active account found` on login** - ensure the user exists and `is_active=True` or create superuser.
* **`Authentication credentials were not provided`** - include the correct `Authorization` header.
* **Pylance warnings for `decouple` or `dj_database_url`** - install packages in your virtualenv and reload VS Code.
* **Migrations errors after switching user model** - define `AUTH_USER_MODEL` before creating initial migrations; if necessary, reset migrations carefully.

---

## Recommended commits / changelog note

Use clear, conventional commit messages. Examples (pick those that match the work you completed):

```
chore: initialize Django project thrift_ms
feat(accounts): extend AbstractUser with phone and bank fields
feat(accounts): add registration endpoint and serializer
feat(thrift): add ThriftGroup model and CRUD endpoints
feat(membership): add Membership model and join endpoint
feat(contribution): add Contribution model and record endpoint
feat(payout): add Payout model and record endpoint
fix(auth): token/JWT login issues and permission fixes
docs: add API documentation and README
```

---

## Next steps (suggestions)

* Add tests for critical endpoints (registration, contribution, payout flows).
* Add role-based permissions (e.g., `IsGroupAdmin` custom permission class).
* Add automated email/SMS reminders (Twilio / SMTP).
* Integrate payment provider (Paystack / Flutterwave) for actual online contributions.
* Consider deploying with PostgreSQL when moving to a hosted service.

---

## Credits & License

Built by **Busari Abdulhakeem Tunde** as a capstone project at ALX. Licensed under the MIT License (add a `LICENSE` file if needed).

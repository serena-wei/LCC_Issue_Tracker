# LCC Issue Tracker

Flask web app for the Lincoln Community Campsite (LCC): visitors report and track issues; helpers and admins manage issues and accounts.

Originally a postgraduate project at Lincoln University. Refactored for portfolio use — clearer structure, safer configuration, and focused tests — so it reads as maintainable backend work rather than a one-file coursework dump.

## Tech Stack

- **Backend:** Python, Flask
- **Database:** MySQL
- **Frontend:** HTML, CSS, JavaScript, Jinja2
- **Password Security:** bcrypt
- **Testing:** pytest

## Architecture

| Layer | Responsibility |
|------|----------------|
| `create_app()` | Application factory and extension wiring |
| `blueprints/` | HTTP routes: `auth`, `users`, `issues` |
| `repositories/` | SQL / data access only |
| `config.py` | Secrets and DB settings from environment (`.env`) |
| `tests/` | Focused coverage for login, RBAC, and issue workflow |

### Design decisions

- **Blueprints + repositories** — keep HTTP handlers thin; SQL lives in one place and is easier to change or mock.
- **Config from the environment** — no secrets in source; local setup uses `.env` (see `.env.example`).
- **Role checks as decorators** — visitor / helper / admin access is explicit on protected routes.
- **Tests cover critical paths only** — authentication, access control, and the main issue workflow, not every UI edge case.

## Features

### Roles

| Role | Access |
|------|--------|
| **Visitor** | Profile, own issues and comments, report issues |
| **Helper** | Visitor features + view/manage all issues and comments, change issue status |
| **Admin** | Helper features + user list, role changes, batch activate/deactivate |

Protected routes use role decorators. Non-admins do not see the Users nav item; direct access to `/userlist` returns **403**.

### Auth and accounts

- Sign up, login, logout, password reset (bcrypt hashes; inactive users cannot log in)
- New users default to `visitor` and `active`
- Profile view/edit, including profile image upload/delete (username stays read-only)

### Issues and comments

- Visitors create issues and work on their own unresolved/resolved lists
- Helpers/admins see all issues, update status (`new` / `open` / `stalled` / `resolved`)
- Comments on an issue; a **helper or admin** comment sets the issue status to `open`

## Database

MySQL, with scripts:

- `create_database.sql` — schema
- `populate_database.sql` — sample users, issues, comments

Sample data includes 20 visitors, 5 helpers, 2 admins, 20 issues, and 20 comments. Sample passwords are stored as bcrypt hashes.

## How to Run

### 1. Clone

```bash
git clone https://github.com/serena-wei/LCC_Issue_Tracker.git
cd LCC_Issue_Tracker
```

### 2. Virtual environment

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Dependencies

```bash
pip install -r requirements.txt
```

### 4. Database

Run in order: `create_database.sql`, then `populate_database.sql`.

### 5. Configuration

```bash
cp .env.example .env
```

Edit `.env`:

```env
SECRET_KEY=replace-with-a-long-random-string
DB_USER=your_username
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306
DB_NAME=lcc_issue_tracker_db
```

Do not commit `.env`. Settings load via `app/config.py` in `create_app()`.

### 6. Start

```bash
python run.py
```

On macOS, port **5000** is often taken by AirPlay Receiver. If the app fails to bind, use another port:

```bash
flask --app run run --port 5003
```

### 7. Tests

Needs the same `.env` and sample data as the app:

```bash
pytest
```

## Demo Accounts

For local testing only:

| Role | Username | Password |
|------|----------|----------|
| Visitor | `visitor1` | `Visitor1pass*` |
| Helper | `helper1` | `Helper1pass*` |
| Admin | `admin1` | `Admin1pass*` |

## Project Structure

```text
LCC_Issue_Tracker/
├── app/
│   ├── blueprints/          # HTTP routes (auth, users, issues)
│   ├── repositories/        # Database access
│   ├── static/
│   ├── templates/
│   ├── __init__.py          # create_app()
│   ├── config.py            # Loads settings from environment
│   ├── constants.py
│   ├── db.py
│   ├── decorators.py
│   ├── extensions.py
│   ├── utils.py
│   └── validators.py
├── tests/                   # Auth, RBAC, issue workflow
├── .env.example
├── create_database.sql
├── populate_database.sql
├── password_hash_generator.py   # bcrypt hashes for sample accounts
├── requirements.txt
├── run.py
└── README.md
```

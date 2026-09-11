# LCC Issue Tracker

The LCC Issue Tracker is a Flask-based web application developed for the Lincoln Community Campsite (LCC). It allows visitors to report and track issues, while helpers and administrators can manage reported issues and user accounts.

The application includes user authentication, role-based access control, issue management, comments, profile management, and user administration.

## Tech Stack

- **Backend:** Python, Flask
- **Database:** MySQL
- **Frontend:** HTML, CSS, JavaScript, Jinja2
- **Password Security:** bcrypt

## Features

### User Authentication

- User registration and login
- Logout
- Password reset
- Password validation
- Account activation and deactivation
- New users are assigned the `visitor` role by default
- New users are active by default
- Inactive users cannot log in
- Passwords are stored using bcrypt hashes rather than plain text

### User Profile

All users can:

- View their personal information
- Edit their profile information
- Change their profile image
- Delete an uploaded profile image
- Keep their username unchanged when editing their profile

New users are assigned a default profile image when they register.

### Issue Management

Visitors can:

- Create new issues
- View their own unresolved issues
- View their own resolved issues
- Add comments to their own issues
- View comments on their issues

Helpers and administrators can:

- View all reported issues
- View comments on any issue
- Add comments to any issue
- Change issue status

New issues are created with a `new` status.

The application separates issues into resolved and unresolved views based on their current status.

Adding a comment to an issue with a `new`, `stalled`, or `resolved` status changes the issue status to `open`.

### Role-Based Access Control

The application has three user roles:

| Role | Access |
|------|--------|
| **Visitor** | Manage own profile, report issues, view own issues and comments |
| **Helper** | Visitor features + view and manage all issues |
| **Admin** | Helper features + manage users, roles, and account status |

Access to protected features is controlled by user role.

For example, the **User List** is visible as a navigation option after login, but only administrators can access the page. If a visitor or helper attempts to access it, they are redirected to a **403 Forbidden** page.

### User Administration

Administrators can:

- View all users
- Search users by username, first name, or last name
- View users sorted by active status
- Activate users
- Deactivate users
- Batch activate users
- Batch deactivate users
- Change a user's role to `helper` or `admin`

Role changes take effect when the affected user logs in again.

## Database

The application uses **MySQL** as its relational database.

The project includes SQL scripts for setting up and populating the database:

- `create_database.sql` — creates the database and required tables
- `populate_database.sql` — populates the database with sample users, issues, and comments

The sample database contains:

- 20 visitor accounts
- 5 helper accounts
- 2 admin accounts
- 20 issues
- 20 comments

Passwords in the sample database are stored as bcrypt hashes.

## How to Run

### 1. Clone the repository

```bash
git clone https://github.com/xiaoxuan-wei-1161823/LCC_Issue_Tracker.git
cd LCC_Issue_Tracker
```

### 2. Create a virtual environment

On macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up the database

Run the following SQL scripts in order:

`create_database.sql`

`populate_database.sql`

`create_database.sql` creates the database and required tables.

`populate_database.sql` inserts the sample users, issues, and comments.

### 5. Configure the application

Copy the example environment file and set your local values:

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

Do not commit `.env` — it is listed in `.gitignore`.
Settings are loaded in `app/config.py` and applied by `create_app()`.

### 6. Start the application

```bash
python run.py
```

The terminal will display the local URL for the Flask application.

### 7. Run tests

Tests need a configured database (same `.env` as the app) and the sample data from `populate_database.sql`.

```bash
pytest
```

## Demo Accounts

The sample database includes accounts for each role:

| Role | Username | Password |
|------|----------|----------|
| Visitor | `visitor1` | `Visitor1pass*` |
| Helper | `helper1` | `Helper1pass*` |
| Admin | `admin1` | `Admin1pass*` |

These accounts are provided for local testing only.

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
├── .env.example
├── create_database.sql
├── populate_database.sql
├── password_hash_generator.py
├── requirements.txt
├── run.py
└── README.md
```

## Password Hash Generator

The project includes `password_hash_generator.py` for generating bcrypt password hashes for sample or test accounts.

## Project Background

This project was developed as part of my postgraduate study at Lincoln University. It provided practical experience building a Python/Flask web application with MySQL, authentication, role-based access control, and server-side business logic.
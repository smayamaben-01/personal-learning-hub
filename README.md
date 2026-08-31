# Personal Learning Hub

A placement-prep tracker built with Flask and MySQL — helps students track DSA practice, company applications, and personal notes, all tied to a real user account.

**Version 2** rebuilds the backend as a layered REST API, adds full-text search, dashboard analytics, Markdown-rendered notes, editable user profiles, and a fully Dockerized local environment.

## Features
- User authentication (register, login, logout) with hashed passwords
- DSA Tracker — add topics, track status and questions solved
- Company Tracker — track applications by status (Applied / OA / Interview / Rejected / Selected)
- Notes — create, edit, delete personal notes, with Markdown rendering
- Search across your tracked data
- Dashboard summarizing your progress with charts
- Editable user profile (full name, email, bio)
- REST API backing the frontend, documented via Postman

## Tech Stack
- Backend: Flask (Python), layered into routes / services / repositories
- Database: MySQL
- Frontend: HTML, CSS, JavaScript
- Containerization: Docker & Docker Compose

## Architecture

Version 2 restructures the app into layers instead of one flat routes file:

```
Routes (blueprints)  →  Services (business logic)  →  Repositories (DB queries)  →  MySQL
```

This keeps request handling, business rules, and raw SQL separated, so each layer can be tested and changed independently.

Locally, the app runs as two containers managed by Docker Compose:

- **app** — the Flask application, built from the project's `Dockerfile`
- **db** — a MySQL 8 container, with a named volume (`mysql_data`) so data survives container restarts

The two containers communicate over Compose's internal network — the app reaches the database at the hostname `db`, not `localhost`.

In production, the app connects instead to a managed MySQL instance (Aiven), over an SSL connection using a CA certificate.

## API Reference

The full set of API endpoints (DSA, companies, notes, auth, profile) is documented as a Postman collection:

📄 [`docs/postman_collection.json`](docs/postman_collection.json) — import directly into Postman to explore and test every endpoint.

## Setup Instructions

### Option A — Docker Compose (recommended)

This runs the full app plus a local MySQL database, no manual MySQL install needed.

1. Clone the repo:
   ```
   git clone https://github.com/smayamaben-01/personal-learning-hub.git
   cd personal-learning-hub
   ```

2. Start the containers:
   ```
   docker compose up
   ```

3. In a separate terminal, load the schema and migrations into the containerized database:
   ```
   docker exec -i personal_learning_hub-db-1 mysql -u app_user -pdevpass1234 learning_hub < schema.sql
   docker exec -i personal_learning_hub-db-1 mysql -u app_user -pdevpass1234 learning_hub < migrations/002_add_profile_fields.sql
   ```

4. Visit `http://localhost:5000` in your browser.

5. To stop the containers (keeping your data):
   ```
   docker compose down
   ```
   Your data persists in the `mysql_data` volume across restarts. To wipe the database completely, add `-v` to the command above.

### Option B — Manual local setup (without Docker)

1. Clone the repo:
   ```
   git clone https://github.com/smayamaben-01/personal-learning-hub.git
   cd personal-learning-hub
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root with:
   ```
   DB_HOST=localhost
   DB_USER=root
   DB_PASSWORD=your_mysql_password
   DB_NAME=learning_hub
   SECRET_KEY=your_secret_key
   ```

5. Create the database and run the schema and migrations:
   ```
   mysql -u root -p -e "CREATE DATABASE learning_hub;"
   mysql -u root -p learning_hub < schema.sql
   mysql -u root -p learning_hub < migrations/002_add_profile_fields.sql
   ```

6. Run the app:
   ```
   flask --app app run --debug
   ```

7. Visit `http://localhost:5000` in your browser.
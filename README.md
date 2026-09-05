# Personal Learning Hub

A placement-prep tracker built with Flask, MySQL, and React — helps students track DSA practice, company applications, and personal notes, all tied to a real user account.

**Version 2** rebuilt the backend as a layered REST API, added full-text search, dashboard analytics, Markdown-rendered notes, editable user profiles, and a fully Dockerized local environment.

**Version 3** replaces the frontend with a React + Tailwind single-page app, adds a weekly Goals tracker and a dedicated password-change flow, and extends Docker Compose to run the frontend alongside the backend and database.

## Features
- User authentication (register, login, logout) with hashed passwords
- DSA Tracker — add topics, track status and questions solved
- Company Tracker — track applications by status (Applied / OA / Interview / Rejected / Selected)
- Notes — create, edit, delete personal notes, with Markdown rendering
- Weekly Goals — set goals with a target count, track progress, resets each week
- Search across your tracked data
- Dashboard summarizing your progress with charts
- Editable user profile (full name, email, bio) and dedicated password-change page
- REST API backing the frontend, documented via Postman

## Tech Stack
- Backend: Flask (Python), layered into routes / services / repositories
- Database: MySQL
- Frontend: React (Vite) + Tailwind CSS, React Router, Recharts
- Containerization: Docker & Docker Compose

## Architecture

The backend is structured into layers instead of one flat routes file:
```
Routes (blueprints)  →  Services (business logic)  →  Repositories (DB queries)  →  MySQL
```


This keeps request handling, business rules, and raw SQL separated, so each layer can be tested and changed independently.

Locally, the app runs as three containers managed by Docker Compose:

- **app** — the Flask backend, built from the project's `Dockerfile`
- **frontend** — the React app, served via Vite's dev server for hot-reload during development
- **db** — a MySQL 8 container, with a named volume (`mysql_data`) so data survives container restarts

The frontend and backend communicate over `localhost`, the same as they would running outside Docker — the browser talks directly to both containers via their mapped ports (`5173` for the frontend, `5000` for the API), rather than the frontend container talking to the backend container internally. The `app` and `db` containers do communicate over Compose's internal network, where the app reaches the database at the hostname `db`, not `localhost`.

In production, the app connects instead to a managed MySQL instance (Aiven), over an SSL connection using a CA certificate.

## Known Limitations

- **Dark mode is not yet wired up.** Tailwind `dark:` classes exist throughout the frontend, but there's no theme toggle or `prefers-color-scheme` config connecting them — they're currently inert. Planned for a future version.
- **Goals can't be edited after creation.** Only progress (`current_count`) can be updated once a goal is created; the description and target count are fixed. To change either, delete the goal and create a new one.

## API Reference

The full set of API endpoints (DSA, companies, notes, auth, profile, password, goals) is documented as a Postman collection:

📄 [`docs/postman_collection.json`](docs/postman_collection.json) — import directly into Postman to explore and test every endpoint.

## Setup Instructions

### Option A — Docker Compose (recommended)

This runs the full app — backend, frontend, and a local MySQL database — with no manual installs needed.

1. Clone the repo:
   ```
   git clone https://github.com/smayamaben-01/personal-learning-hub.git
   cd personal-learning-hub
   ```

2. Start the containers:
   ```
   docker compose up --build
   ```

3. In a separate terminal, load the schema and migrations into the containerized database:
   ```
   docker exec -i personal_learning_hub-db-1 mysql -u app_user -pdevpass1234 learning_hub < schema.sql
   docker exec -i personal_learning_hub-db-1 mysql -u app_user -pdevpass1234 learning_hub < migrations/002_add_profile_fields.sql
   docker exec -i personal_learning_hub-db-1 mysql -u app_user -pdevpass1234 learning_hub < migrations/003_add_goals_table.sql
   ```

4. Visit `http://localhost:5173` in your browser for the app. The backend API runs separately at `http://localhost:5000`.

5. To stop the containers (keeping your data):
   ```
   docker compose down
   ```
   Your data persists in the `mysql_data` volume across restarts. To wipe the database completely, add `-v` to the command above.

### Option B — Manual local setup (without Docker)

> **Note:** Option B hasn't been fully re-verified end-to-end for v3. Steps 7–8 (frontend) and the `003_add_goals_table.sql` migration are new and tested; the rest of the backend setup is unchanged from v2.


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
   mysql -u root -p learning_hub < migrations/003_add_goals_table.sql
   ```

6. Run the backend:
   ```
   flask --app app run --debug
   ```
   The API will be available at `http://localhost:5000`.

7. **Frontend setup** — in a separate terminal, from the `frontend/` folder:
   ```
   cd frontend
   npm install
   npm run dev
   ```

8. Visit `http://localhost:5173` in your browser.
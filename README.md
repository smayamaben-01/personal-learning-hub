# Personal Learning Hub

A placement-prep tracker built with Flask and MySQL — helps students track DSA practice, company applications, and personal notes, all tied to a real user account.

## Features
- User authentication (register, login, logout) with hashed passwords
- DSA Tracker — add topics, track status and questions solved
- Company Tracker — track applications by status (Applied / OA / Interview / Rejected / Selected)
- Notes — create, edit, delete personal notes
- Dashboard summarizing your progress across all three

## Tech Stack
- Backend: Flask (Python)
- Database: MySQL
- Frontend: HTML, CSS, JavaScript

🔗 **Live demo:** https://personal-learning-hub.onrender.com

> Note: hosted on a free tier — the first load after inactivity may take 10-30 seconds while the server wakes up.

## Setup Instructions

1. Clone the repo:
   \`\`\`
   git clone https://github.com/smayamaben-01/personal-learning-hub.git
   cd personal-learning-hub
   \`\`\`

2. Create and activate a virtual environment:
   \`\`\`
   python -m venv venv
   venv\Scripts\activate
   \`\`\`

3. Install dependencies:
   \`\`\`
   pip install -r requirements.txt
   \`\`\`

4. Create a `.env` file in the project root with:
   \`\`\`
   DB_HOST=localhost
   DB_USER=root
   DB_PASSWORD=your_mysql_password
   DB_NAME=learning_hub
   SECRET_KEY=your_secret_key
   \`\`\`

5. Create the database and run the schema:
   \`\`\`
   mysql -u root -p -e "CREATE DATABASE learning_hub;"
   mysql -u root -p learning_hub < schema.sql
   \`\`\`

6. Run the app:
   \`\`\`
   flask --app app run --debug
   \`\`\`

7. Visit `http://localhost:5000` in your browser.

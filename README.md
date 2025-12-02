# 📦 Project Setup

---

# 🧩 1. Install Homebrew (Mac Only)

> Skip this step if you're on Windows.

Homebrew is a package manager for macOS.
You’ll use it to easily install Git, Python, Docker, etc.

**Install Homebrew:**

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

**Verify Homebrew:**

```bash
brew --version
```

If you see a version number, you're good to go.

---

# 🧩 2. Install and Configure Git

## Install Git

- **MacOS (using Homebrew)**

```bash
brew install git
```

- **Windows**

Download and install [Git for Windows](https://git-scm.com/download/win).
Accept the default options during installation.

**Verify Git:**

```bash
git --version
```

---

## Configure Git Globals

Set your name and email so Git tracks your commits properly:

```bash
git config --global user.name "Your Name"
git config --global user.email "your_email@example.com"
```

Confirm the settings:

```bash
git config --list
```

---

## Generate SSH Keys and Connect to GitHub

> Only do this once per machine.

1. Generate a new SSH key:

```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
```

(Press Enter at all prompts.)

2. Start the SSH agent:

```bash
eval "$(ssh-agent -s)"
```

3. Add the SSH private key to the agent:

```bash
ssh-add ~/.ssh/id_ed25519
```

4. Copy your SSH public key:

- **Mac/Linux:**

```bash
cat ~/.ssh/id_ed25519.pub | pbcopy
```

- **Windows (Git Bash):**

```bash
cat ~/.ssh/id_ed25519.pub | clip
```

5. Add the key to your GitHub account:
   - Go to [GitHub SSH Settings](https://github.com/settings/keys)
   - Click **New SSH Key**, paste the key, save.

6. Test the connection:

```bash
ssh -T git@github.com
```

You should see a success message.

---

# 🧩 3. Clone the Repository

Now you can safely clone the course project:

```bash
git clone <repository-url>
cd <repository-directory>
```

---

# 🛠️ 4. Install Python 3.10+

## Install Python

- **MacOS (Homebrew)**

```bash
brew install python
```

- **Windows**

Download and install [Python for Windows](https://www.python.org/downloads/).
✅ Make sure you **check the box** `Add Python to PATH` during setup.

**Verify Python:**

```bash
python3 --version
```
or
```bash
python --version
```

---

## Create and Activate a Virtual Environment

(Optional but recommended)

```bash
python3 -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate.bat  # Windows
```

### Install Required Packages

```bash
pip install -r requirements.txt
```

---

# 🐳 5. (Optional) Docker Setup

> Skip if Docker isn't used in this module.

## Install Docker

- [Install Docker Desktop for Mac](https://www.docker.com/products/docker-desktop/)
- [Install Docker Desktop for Windows](https://www.docker.com/products/docker-desktop/)

## Build Docker Image

```bash
docker build -t <image-name> .
```

## Run Docker Container

```bash
docker run -it --rm <image-name>
```

---

# 🚀 6. Running the Project

- **Without Docker**:

```bash
python main.py
```

(or update this if the main script is different.)

- **With Docker**:

```bash
docker run -it --rm <image-name>
```

---

# 📝 7. Submission Instructions

After finishing your work:

```bash
git add .
git commit -m "Complete Module X"
git push origin main
```

Then submit the GitHub repository link as instructed.

---

# 🔥 Useful Commands Cheat Sheet

| Action                         | Command                                          |
| ------------------------------- | ------------------------------------------------ |
| Install Homebrew (Mac)          | `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"` |
| Install Git                     | `brew install git` or Git for Windows installer |
| Configure Git Global Username  | `git config --global user.name "Your Name"`      |
| Configure Git Global Email     | `git config --global user.email "you@example.com"` |
| Clone Repository                | `git clone <repo-url>`                          |
| Create Virtual Environment     | `python3 -m venv venv`                           |
| Activate Virtual Environment   | `source venv/bin/activate` / `venv\Scripts\activate.bat` |
| Install Python Packages        | `pip install -r requirements.txt`               |
| Build Docker Image              | `docker build -t <image-name> .`                |
| Run Docker Container            | `docker run -it --rm <image-name>`               |
| Push Code to GitHub             | `git add . && git commit -m "message" && git push` |

---

# 📋 Notes

- Install **Homebrew** first on Mac.
- Install and configure **Git** and **SSH** before cloning.
- Use **Python 3.10+** and **virtual environments** for Python projects.
- **Docker** is optional depending on the project.

---

# 📎 Quick Links

- [Homebrew](https://brew.sh/)
- [Git Downloads](https://git-scm.com/downloads)
- [Python Downloads](https://www.python.org/downloads/)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [GitHub SSH Setup Guide](https://docs.github.com/en/authentication/connecting-to-github-with-ssh)

## Module 13 — JWT Authentication with Front-End and E2E Testing

This module implements JWT-based authentication for user registration and login, including front-end pages and comprehensive Playwright E2E tests.

### Features Implemented

- **JWT Authentication**:
  - POST `/users/register` - Register new users and receive JWT token
  - POST `/users/login` - Authenticate users and receive JWT token
  - Password hashing with passlib
  - Token generation and verification with python-jose

- **Front-End Pages**:
  - GET `/register` - Registration page with client-side validation
  - GET `/login` - Login page with client-side validation
  - Email format validation
  - Password length validation (minimum 6 characters)
  - Password confirmation matching
  - JWT token storage in localStorage

- **Playwright E2E Tests**:
  - Positive tests: Valid registration and login
  - Negative tests: Short passwords, invalid emails, wrong credentials
  - UI feedback verification
  - Server response validation

---

## Module 14 — Calculation BREAD Operations with User Authentication

This module implements complete BREAD (Browse, Read, Edit, Add, Delete) endpoints for calculations with JWT authentication, ensuring users can only access their own calculations.

### Features Implemented

- **User-Specific Calculation Endpoints**:
  - POST `/calculations` - Create a new calculation (authenticated)
  - GET `/calculations` - Browse all calculations for logged-in user (authenticated)
  - GET `/calculations/{id}` - Read specific calculation (authenticated, user-owned only)
  - PUT `/calculations/{id}` - Update calculation (authenticated, user-owned only)
  - DELETE `/calculations/{id}` - Delete calculation (authenticated, user-owned only)
  - All endpoints require JWT Bearer token in Authorization header

- **Front-End Calculations Page**:
  - GET `/calculations-page` - Calculations management interface
  - Add new calculations with operation selection (Add, Subtract, Multiply, Divide)
  - Browse all user's calculations in a table
  - Read specific calculation by ID
  - Edit existing calculations
  - Delete calculations with confirmation
  - Client-side validation for division by zero
  - Automatic token handling from localStorage
  - Protected access (redirects to login if not authenticated)

- **Comprehensive E2E Tests**:
  - Positive scenarios for all BREAD operations
  - Negative scenarios: division by zero, non-existent resources, unauthorized access
  - Full workflow testing with registration, login, and calculation management
  - Verification of UI feedback and server responses

### Running the Application

1. **Install dependencies**:
```bash
pip install -r requirements.txt
```

2. **Start the FastAPI server**:
```bash
python main.py
```

3. **Access the application**:
   - Home page: `http://localhost:8000`
   - Registration: `http://localhost:8000/register`
   - Login: `http://localhost:8000/login`
   - My Calculations: `http://localhost:8000/calculations-page` (requires login)

### Running Tests Locally

1. **Run all tests**:
```bash
pytest -v
```

2. **Run only unit tests**:
```bash
pytest tests/unit/ -v
```

3. **Run only E2E tests**:
```bash
# Install Playwright browsers first (one-time setup)
playwright install --with-deps chromium

# Run E2E tests
pytest tests/e2e/ -v
```

4. **Run with coverage**:
```bash
pytest --cov=app --cov-report=html
```

### Using the Calculation BREAD Operations

#### Via Web Interface:

1. **Register and Login**:
   - Navigate to `/register` and create an account
   - Login at `/login`
   - Token is automatically stored in browser

2. **Navigate to Calculations**:
   - Click "My Calculations" in navigation
   - Or go directly to `/calculations-page`

3. **Add Calculation**:
   - Enter two numbers
   - Select operation (Add, Sub, Multiply, Divide)
   - Click "Add Calculation"
   - Result is displayed and calculation is saved

4. **Browse Calculations**:
   - Click "Refresh List" to see all your calculations
   - Table shows ID, operands, operation, and result
   - Use action buttons to edit or delete

5. **Read Specific Calculation**:
   - Enter calculation ID
   - Click "Get Calculation"
   - Details are displayed below

6. **Edit Calculation**:
   - Use "Edit" button in table to auto-fill form
   - Or manually enter calculation ID
   - Update values and operation
   - Click "Update Calculation"

7. **Delete Calculation**:
   - Click "Delete" button in table (with confirmation)
   - Or enter ID in Delete section
   - Calculation is permanently removed

#### Via API (with JWT Token):

**Get token first**:
```bash
# Register
TOKEN=$(curl -X POST http://localhost:8000/users/register \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","password":"password123"}' \
  | jq -r '.access_token')

# Or login
TOKEN=$(curl -X POST http://localhost:8000/users/login \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"password123"}' \
  | jq -r '.access_token')
```

**Create calculation**:
```bash
curl -X POST http://localhost:8000/calculations \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"a":10,"b":5,"type":"Add"}'
```

**Browse calculations**:
```bash
curl -X GET http://localhost:8000/calculations \
  -H "Authorization: Bearer $TOKEN"
```

**Read specific calculation**:
```bash
curl -X GET http://localhost:8000/calculations/1 \
  -H "Authorization: Bearer $TOKEN"
```

**Update calculation**:
```bash
curl -X PUT http://localhost:8000/calculations/1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"a":20,"b":10,"type":"Multiply"}'
```

**Delete calculation**:
```bash
curl -X DELETE http://localhost:8000/calculations/1 \
  -H "Authorization: Bearer $TOKEN"
```

### Docker Hub Repository

**Docker Hub Link**: [https://hub.docker.com/r/<your-dockerhub-username>/is218-module-14](https://hub.docker.com/r/<your-dockerhub-username>/is218-module-14)

*Note: Replace `<your-dockerhub-username>` with your actual Docker Hub username.*

### Pulling and Running the Docker Image

```bash
docker pull <your-dockerhub-username>/is218-module-14:latest
docker run -p 8000:8000 <your-dockerhub-username>/is218-module-14:latest
```

Then access the application at `http://localhost:8000`

### CI/CD Pipeline

The GitHub Actions workflow (`.github/workflows/ci.yml`) automatically:
1. Spins up PostgreSQL database
2. Runs unit and integration tests
3. Installs Playwright and runs E2E tests for calculations BREAD operations
4. Builds and pushes Docker image to Docker Hub (on success)
5. Tags images with both `latest` and git SHA for versioning

### Security Notes

- All calculation endpoints require JWT authentication
- Users can only access their own calculations
- Tokens expire after 30 minutes (configurable in `app/security.py`)
- Passwords are hashed using pbkdf2_sha256
- Token secret should be changed in production (set via environment variable)

---

## Previous Modules

### Module 12 — User & Calculation CRUD with Integration Tests

Install dependencies and run pytest:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pytest -q
```

To run only integration tests:

```bash
pytest tests/integration/ -v
```

To run tests with coverage:

```bash
pytest --cov=app --cov-report=html
```

## Testing with OpenAPI Documentation

Start the FastAPI server locally:

```bash
python main.py
```

Access the interactive API documentation:

- **Swagger UI**: `http://127.0.0.1:8000/docs`
- **ReDoc**: `http://127.0.0.1:8000/redoc`

### Manual Testing Steps

1. **Register a User** (POST `/users/register`)
   - Endpoint: `/users/register`
   - Body: `{"username": "testuser", "email": "test@example.com", "password": "password123"}`
   - Expected: 200 OK with user data (without password)

2. **Login** (POST `/users/login`)
   - Endpoint: `/users/login`
   - Body: `{"username": "testuser", "password": "password123"}`
   - Expected: 200 OK with user data

3. **Create Calculation** (POST `/calculations`)
   - Endpoint: `/calculations`
   - Body: `{"a": 10, "b": 5, "type": "Add"}`
   - Expected: 200 OK with calculation result

4. **Browse Calculations** (GET `/calculations`)
   - Endpoint: `/calculations`
   - Expected: 200 OK with list of calculations

5. **Read Specific Calculation** (GET `/calculations/{id}`)
   - Endpoint: `/calculations/1`
   - Expected: 200 OK with calculation details

6. **Update Calculation** (PUT `/calculations/{id}`)
   - Endpoint: `/calculations/1`
   - Body: `{"a": 20, "b": 10, "type": "Multiply"}`
   - Expected: 200 OK with updated calculation

7. **Delete Calculation** (DELETE `/calculations/{id}`)
   - Endpoint: `/calculations/1`
   - Expected: 200 OK with deletion confirmation

## CI / Docker Hub

- The repository includes a GitHub Actions workflow at `.github/workflows/ci.yml` that runs tests against a Postgres service and (on success) builds and pushes a Docker image to Docker Hub.
- Docker Hub repository (replace with your repo): `docker.io/<your-username>/is218-module-12`

## Module 12 — User & Calculation CRUD with Integration Tests

This module completes the back-end logic with full CRUD operations for users and calculations.

### Features Implemented

- **User Endpoints**:
  - POST `/users/register` - Register new users with email validation and password hashing
  - POST `/users/login` - Authenticate users with username/password

- **Calculation Endpoints (BREAD)**:
  - POST `/calculations` - Add new calculations
  - GET `/calculations` - Browse all calculations with pagination
  - GET `/calculations/{id}` - Read specific calculation
  - PUT `/calculations/{id}` - Edit existing calculation
  - DELETE `/calculations/{id}` - Delete calculation

### Running with Docker

Pull and run the latest image from Docker Hub:

```bash
docker pull <your-dockerhub-username>/is218-module-12:latest
docker run -p 8000:8000 <your-dockerhub-username>/is218-module-12:latest
```

### Docker Hub Link

**Docker Hub Repository**: [https://hub.docker.com/r/<your-dockerhub-username>/is218-module-12](https://hub.docker.com/r/<your-dockerhub-username>/is218-module-12)

*Note: Replace `<your-dockerhub-username>` with your actual Docker Hub username.*

---

**Docker Hub**: Replace with your published image, e.g. `docker.io/<your-username>/is218-module-12`.

## Module 9 — PostgreSQL & pgAdmin (FastAPI + Postgres)

Follow these steps to satisfy the Module 9 assignment requirements.

- **Start services:** Run the Docker Compose configuration that includes FastAPI (web), PostgreSQL (db), and pgAdmin (optional) from the project root:

```bash
docker-compose up --build
```

- **Access pgAdmin:** Open `http://localhost:5050` in your browser. Use the credentials defined in the Compose file (if present). If your compose file exposes pgAdmin on a different port, use that port instead.

- **Connect to the database:** In pgAdmin create/connect to a server using:
   - Host: `db` (or `localhost` if using port forwarding)
   - User: `postgres` (or the user defined in `docker-compose.yml`)
   - Database: the database defined in Compose (commonly `fastapi_db`)

- **SQL files:** The repository includes SQL scripts you can run in pgAdmin Query Tool or via `psql`:
   - `sql/create_tables.sql` — create `users` and `calculations` tables
   - `sql/insert_data.sql` — insert sample rows
   - `sql/queries.sql` — run SELECT and JOIN queries
   - `sql/update_delete.sql` — examples of UPDATE and DELETE statements

- **Execution tips:**
   - In pgAdmin open the Query Tool, paste the contents of a script, and click the run button.
   - After each run, take a screenshot of the Query Tool results showing the "Query returned successfully" message (or rows displayed).

- **Documentation / Submission:** Create a Word document or PDF compiling the screenshots. For each screenshot include a short caption (one sentence) describing what the screenshot shows (e.g., "Created tables: users and calculations — 2 rows affected"). Include a short reflection (1–2 paragraphs) about challenges and what you learned.

If you want to run the SQL scripts directly from the host using `psql` and Docker, you can (alternative to pgAdmin):

```bash
# Run the create script inside the running postgres container (replace container name if different)
docker exec -i $(docker ps -qf "name=db") psql -U postgres -d postgres < sql/create_tables.sql
```

Replace `postgres` with the target database name if different.

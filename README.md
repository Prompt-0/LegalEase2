# 🏛️ Legalease - Virtual Law Assistant (Django Version)

A full-stack web application built with Python/Django and JavaScript, designed to be a "Virtual Law Assistant" for citizens. It provides a dashboard of tools to help with everyday legal needs, including a helpful chatbot, dynamic database-driven finders, and secure form submissions.

---

## 🛠️ Features

* **Full User Authentication:** Secure signup, login, and logout functionality using Django's built-in auth system.
* **Dynamic API Backend:** A REST API built with Django Rest Framework serves all application data from an SQLite database.
* **Form Submissions:** Secure, backend-powered forms for:
    * Online FIR
    * Anonymous Reports
    * Contact Messages
* **Database-Driven Finders:**
    * **Lawyer Connect:** Find lawyers by name, specialization, or location, with all data served from the backend API.
    * **Police Stations:** A tool to find police stations (pre-loaded with Delhi stations) from the database.
    * **Case Finder:** Search for legal cases stored in the database.
* **LegalBot:** Features an embedded chatbot for instant legal guidance.
* **Client-Side Document Generator:** A tool to generate a Legal Notice, which uses browser `localStorage` to save progress.

---

## 🧱 Tech Stack

* **Backend:** Python 3, Django, Django Rest Framework
* **Database:** SQLite (for development)
* **API:** RESTful API with JSON responses
* **Frontend:** Django Templates (HTML), Vanilla JavaScript (for dynamic data fetching), CSS
* **Core Dependencies:** `django`, `djangorestframework`, `django-cors-headers`

---

## 🚀 Getting Started (Linux/Development)

This is a Django project and requires a Python environment to run.

1.  **Clone the repository (if you haven't):**
    ```bash
    git clone [your-repo-url]
    cd legalease/legalease_backend
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    (You will need to create a `requirements.txt` file. Based on your project, it should contain:)
    ```bash
    pip install django djangorestframework django-cors-headers
    ```

4.  **Run database migrations:**
    This will set up your `db.sqlite3` database based on the schemas in `api/models.py`.
    ```bash
    python manage.py migrate
    ```

5.  **Create a superuser (for Admin access):**
    This lets you log in to `/admin/` to manage the data.
    ```bash
    python manage.py createsuperuser
    ```
    (Follow the prompts to create a username and password)

6.  **Run the development server:**
    ```bash
    python manage.py runserver
    ```

7.  **Open the application:**
    Open your web browser and go to **http://127.0.0.1:8000/**

---

### Other Files to Delete

These files are either broken, unused, or add no value to the project:

* `legalease_backend/templates/LegalBot_Upgrade.html` (Unused, broken draft)
* `legalease` (The three empty files at the root of the project)

#  Gr8Tutor — Tutor Marketplace Platform (online marketplace connecting students with qualified English tutors for personalised language learning)

Gr8Tutor is a **fullstack Django + Vanilla JavaScript web application** that connects **students and tutors** in an intuitive and secure online environment.  
Tutors can publish profiles, manage student requests, and chat with confirmed learners — while students can easily browse tutors, send requests, and communicate through a built-in messaging system.

---

## Table of Contents
1. [Overview](#-overview)
2. [Features](#-features)
3. [Tech Stack](#-tech-stack)
4. [Database Models](#-database-models)
5. [App Structure](#-app-structure)
6. [Setup & Installation](#-setup--installation)
7. [Usage](#-usage)
8. [Testing](#-testing)
9. [Project Highlights](#-project-highlights)
10. [Future Improvements](#-future-improvements)
11. [License](#-license)

---

## Overview

Gr8Tutor provides a **marketplace experience** for tutors and students using a unified authentication system.  
Users sign up once and can register as either a **Tutor** or **Student**, each receiving a role-based dashboard.  

The platform focuses on:
- clean and maintainable **Django backend logic**,  
- lightweight **frontend interactivity** powered by pure JavaScript,  
- and **PostgreSQL** database for production-level data integrity.

---

## Features

- **Unified Authentication** — Shared Django `User` model extended via `UserProfile` (roles: tutor/student/admin).  
- **Tutor Management (CRUD)** — Tutors can create, edit, and delete profiles directly from the frontend.  
- **Student Requests** — Students can browse tutors and send callback requests.  
- **Tutor Confirmations** — Tutors can approve or reject student connections.  
- **Messaging System** — Secure one-to-one chat between confirmed tutor–student pairs.  
- **Role Differentiation** — Each role has unique permissions and views.  
- **Signals** — Django signals automatically create `UserProfile` entries on user registration.  
- **Automated Tests** for backend flows and manual JavaScript test plan.  

---

## Tech Stack

| Layer | Technology |
|-------|-------------|
| Backend | Django 5.x |
| Frontend | HTML5, CSS3, Bootstrap 5, Vanilla JS |
| Database | PostgreSQL |
| ORM | Django ORM |
| Testing | Django `unittest` (Python) + manual JS tests |
| Version Control | Git & GitHub |
| Language | Python 3.10+ |

---

## Database Models

| Model | Description |
|--------|--------------|
| **UserProfile** | Extends Django’s `User`, adds a `role` field (`admin`, `tutor`, `student`). |
| **Tutor** | Connected via OneToOneField to `UserProfile`; includes `bio`, `hourly_rate`, `subject`, and `experience`. |
| **Student** | OneToOneField to `UserProfile`; contains learning `goals`. |
| **StudentTutorRelationship** | Links a student to a tutor, tracks active and pending requests. |
| **Message** | Stores chat messages between verified tutor–student pairs. |

---

## App Structure

gr8tutor/<br>
│<br>
├── models.py<br>
├── views.py<br>
├── urls.py<br>
├── signals.py<br>
├── templates/gr8tutor/<br>
│ ├── index.html<br>
│ ├── dashboard.html<br>
│ ├── login.html<br>
│ ├── register.html<br>
│ └── chat.html<br>
└── static/js/

yaml
Copy code

---

## Setup & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/gr8tutor.git
cd gr8tutor
2. Create & Activate Virtual Environment
bash
Copy code
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
3. Install Dependencies
bash
Copy code
pip install -r requirements.txt
4. Apply Migrations
bash
Copy code
python manage.py migrate
5. Create a Superuser (optional)
bash
Copy code
python manage.py createsuperuser
6. Run the Development Server
bash
Copy code
python manage.py runserver
Now visit: http://127.0.0.1:8000/

Usage
Register a new user or log in.

Choose a role (Tutor or Student) upon first login.

If a Tutor, complete your profile and manage student requests.

If a Student, browse tutors and request a callback.

Confirmed users can exchange messages through the chat view.

Admins can access all users and delete profiles when needed.

Testing
Automated Python Tests
Run all Django test cases from the project root:

bash
Copy code
python manage.py test gr8tutor.tests
Manual JS Tests
Open browser console in the dashboard or tutor list page.

Simulate button clicks and CRUD actions to verify dynamic behavior.

Check for error messages, validation, and DOM updates.

The test suite validates:

User registration and login

Role assignment logic

Tutor–student relationship management

Messaging and chat permissions

Data integrity after deletions

Project Highlights
Cleanly separated roles and logic — prevents accidental role-switching.

Clear data relationships using Django ORM.

Robust access control (e.g. only tutors can confirm students).

Reusable dashboard views with Bootstrap components.

Consistent user flow from registration → dashboard → messaging.

Future Improvements
Add real-time chat with WebSockets (Django Channels).

Integrate email or SMS notifications for requests and confirmations.

Enable profile images and rating system for tutors.

Implement pagination and search filters for tutor browsing.

Add REST API endpoints for mobile app or SPA integration.

License
This project is licensed under the MIT License — feel free to use, modify, and distribute with attribution.

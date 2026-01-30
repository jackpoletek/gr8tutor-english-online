# Gr8Tutor is a digital marketplace dedicated to English language learning. It connects students seeking personalised instruction with a curated network of qualified and experienced tutors. <br>

[View Live Site](https://gr8tutor-english-online-5967a17d29d9.herokuapp.com/)    <br>
[View GitHub Repository](https://github.com/jackpoletek/gr8tutor-english-online) <br>

![gr8tutor](https://github.com/jackpoletek/gr8tutor-english-online/blob/main/screenshots/home%20page/home%20page_screenshot.jpg)

---

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Database Models](#database-models)
- [App Structure](#app-structure)
- [Project Goals](#project-goals)
- [UX](#ux)
- [Features & User Story Alignment](#features--user-story-alignment)
- [Template Attribution](#template-attribution)
- [Error Handling](#error-handling)
- [Testing](#testing)
- [Bug Fixes](#bug-fixes)
- [Security](#security)
- [Setup & Installation](#setup--installation)
- [Usage](#usage)
- [Deployment](#deployment)
- [Validation and Performance](#validation-and-performance)
- [Project Highlights](#project-highlights)
- [Future Improvements](#future-improvements)
- [Credits](#credits)
- [License](#license)

---

## Overview

**Gr8Tutor** is a full-stack **Django + Vanilla JavaScript** web application that connects students and tutors in an intuitive and secure online environment.

Tutors can publish profiles, manage student requests, and chat with confirmed learners - while students can browse tutors, send requests, and communicate through a built-in messaging system.

The project demonstrates:

- Full-stack web development using **Django**, **PostgreSQL**, and **Bootstrap**
- User-centered design principles and structured UX planning
- Role-based dashboards for tutors and students

Gr8Tutor provides a marketplace experience using a unified authentication system.  
Users sign up once and register as either a **Tutor** or **Student**.

The platform focuses on:

- Clean and maintainable Django backend logic  
- Lightweight frontend interactivity using pure JavaScript  
- PostgreSQL for production-level data integrity  

---

## Features

- **Unified Authentication** - Shared Django `User` model extended via `UserProfile` (roles: tutor/student/admin)  
- **Tutor Management (CRUD)** - Create, edit, delete tutor profiles from the frontend  
- **Student Requests** - Browse tutors and send callback requests  
- **Tutor Confirmations** - Approve or reject student connections  
- **Messaging System** - Secure one-to-one chat between confirmed pairs  
- **Role Differentiation** - Each role has unique permissions and views  
- **Signals** - Auto-create `UserProfile` on registration  
- **Automated Tests** - Backend tests + manual JavaScript test plan  

---

## Tech Stack

| Layer | Technology |
|------|-------------|
| Backend | Django 5.x |
| Frontend | HTML5, CSS3, Bootstrap 5, Vanilla JS |
| Database | PostgreSQL |
| ORM | Django ORM |
| Testing | Django `unittest` + manual JS tests |
| Version Control | Git & GitHub |
| Language | Python 3.10+ |
| Additional | SweetAlert2, Gunicorn, Whitenoise, Heroku |

---

## Database Models

| Model | Description |
|------|-------------|
| `UserProfile` | Extends Django `User`, adds role field |
| `Tutor` | OneToOne -> UserProfile; bio, rate, subject, experience |
| `Student` | OneToOne -> UserProfile; learning goals |
| `StudentTutorRelationship` | Links students to tutors |
| `Message` | Stores chat messages |

### Database Schema

User<br>
└── UserProfile (role)

Tutor<br>
└── OneToOne -> UserProfile

Student<br>
└── OneToOne -> UserProfile

StudentTutorRelationship<br>
└── ForeignKey -> Student<br>
└── ForeignKey -> Tutor<br>
└── is_active

Message<br>
└── ForeignKey -> sender (User)<br>
└── ForeignKey -> recipient (User)<br>
└── text<br>
└── time


Ensures:

- Each user has exactly one role  
- Unique tutor-student relationships  
- Traceable message history  

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
└── static


---

## Project Goals

### Business Goals
- Match students with tutors  
- Separate user roles  
- Support communication  
- Enable future monetisation  
- Demonstrate Django competence  

### User Goals
- Secure registration/login  
- Browse tutors  
- Request lessons  
- Message tutors  
- Manage profiles  

---

## UX

### Target Audience
- Adult English learners  
- Independent tutors  
- Desktop & mobile users  

### User Stories
- As a student, I want to find a tutor easily  
- As a tutor, I want to receive lesson requests  
- As a user, I want to register and log in securely  
- As a student, I want to message my tutor  

UX prioritises:

- Clear role separation  
- Predictable navigation  
- Minimal forms  
- Immediate feedback  

### Wireframes
Initial wireframes were designed in Figma during the early planning stage to map out page layouts, information structure, and user flows for desktop, tablet, and mobile screens.<br>
The wireframes helped achieve:
- A consistent and predictable experience across different devices
- Clear distinction between tutor and student interactions
- Straightforward navigation between key features such as registration, dashboards, and messaging
- Continuous visibility of tutor listings, lesson requests, and conversations

<br>The completed application closely reflects these wireframes in terms of layout, structure, and interaction behaviour.

#### Desktop (992px)
<img src="https://github.com/jackpoletek/gr8tutor-english-online/blob/main/wireframes/Wireframe_desktop(992px)%20-%20Home.jpg" alt="Desktop (992px) - Home Page" width=35% height=35%/>&nbsp;&nbsp;

#### Tablet (768px)
<img src="https://github.com/jackpoletek/gr8tutor-english-online/blob/main/wireframes/Wireframe_tablet(768px)%20-%20Home.jpg" alt="Tablet (768px) - Home Page" width=28% height=28%/>&nbsp;&nbsp;

#### Mobile (576px)
<img src="https://github.com/jackpoletek/gr8tutor-english-online/blob/main/wireframes/Wireframe_mobile(576px)%20-%20Home.jpg" alt="Mobile (576px) - Home Page" width=20% height=20%/>&nbsp;&nbsp;

[View all wireframes](https://github.com/jackpoletek/gr8tutor-english-online/tree/main/wireframes)

---

## Features & User Story Alignment

### Authentication & Roles
- Role-based registration  
- Secure login/logout  
- Django auth backend  

### Tutor Profiles
- Discoverable tutor listings  

### Lesson Requests
- Student -> Tutor requests  
- Tutor approval  
- Chat unlocked after approval  

### Messaging
- Chat-style UI  
- Database persistence  
- Permission checks  

---

## Template Attribution

Design inspired by:  
**Tuturn - Online Tuition & Tutor Marketplace WordPress Theme** (ThemeForest)

Used as reference only; templates were rebuilt for Django.

---

## Error Handling

- Custom 404 page  
- Controlled error routing  

---

## Testing

### Manual Testing

| Feature | Action | Expected | Result |
|--------|--------|----------|--------|
| Register Student | Submit form | Account created | Pass |
| Login | Valid credentials | Logged in | Pass |
| Lesson Request | Submit | Saved | Pass |
| Messaging | Send message | Displayed | Pass |

### Automated Testing

Focus:
- Role creation  
- Profile linking  
- Signal execution  

Run tests:<br>

```bash
python manage.py test gr8tutor.tests

---

## Bug Fixes

### Bug 1 - Undefined tutor
- Fix: tutor = get_object_or_404(Tutor, id=tutor_id)

### Bug 2 - .get().exists() misuse
- Fix: StudentTutorRelationship.objects.filter(...).exists()

### Bug 3 - User called as function
- Fix: user_to_delete.delete()

### Bug 4 - Unassigned variable
- Fix: <br>
if not created:
    message = "Request already exists"
else:
message = "Request sent"

### Bug 5 - No feedback
- Fix: Implemented SweetAlert2 modals

### Bug 6 - JS not loading
- Fix: <br>Correct static paths<br>
Ran collectstatic

---

## Security
- Environment variables for secrets
- DEBUG=False
- CSRF protection
- Hashed passwords
- HTTPS (Heroku)
- Django ORM SQL protection

---

### Setup & Installation
- git clone https://github.com/jackpoletek/gr8tutor-english-online.git
- cd gr8tutor-english-online
- python -m venv venv
- source venv/bin/activate  # Linux/Mac
- venv\Scripts\activate     # Windows
- pip install -r requirements.txt
- python manage.py migrate
- python manage.py runserver
- Usage
- Register
- Visit: http://127.0.0.1:8000/

---

### Usage
- Register and log in
- Choose Tutor or Student
- Tutors manage profiles
- Students browse and request
- Confirmed users can chat

---

## Deployment
Deployed on Heroku<br>
Steps:
- Create app
- Add config vars
- Configure Gunicorn
- Configure Whitenoise
- Run migrations
- Collect static files
- Push to Heroku

---

## Validation and Performance

- W3C HTML Checker - Passed<br>
<img src="https://github.com/jackpoletek/gr8tutor-english-online/blob/main/screenshots/validators/HTML_checker%20-%20Home%20Page.jpg" alt="W3C HTML Checker" width=50% height=50%/><br>

- W3C CSS Validator - Passed<br>
<img src="https://github.com/jackpoletek/gr8tutor-english-online/blob/main/screenshots/validators/CSS_validator%20-%20Home%20Page.jpg" alt="W3C CSS Validator" width=50% height=50%/><br>

- JSHint - No critical issues<br>
<img src="https://github.com/jackpoletek/gr8tutor-english-online/blob/main/screenshots/validators/JS_Hint%20-%20Home%20Page.jpg" alt="JSHint" width=50% height=50%/><br>

- GTmetrix Audit - Performance<br>
<img src="https://github.com/jackpoletek/gr8tutor-english-online/blob/main/screenshots/web%20test/Web%20Test%20-%20GTmetrix_performance.jpg" alt="GTmetrix Score - Performance" width=50% height=50%/><br>
- GTmetrix Audit - Summary<br>
<img src="https://github.com/jackpoletek/gr8tutor-english-online/blob/main/screenshots/web%20test/Web%20Test%20-%20GTmetrix_summary.jpg" alt="GTmetrix Score - Summary" width=50% height=50%/><br>
- GTmetrix Audit - Structure<br>
<img src="https://github.com/jackpoletek/gr8tutor-english-online/blob/main/screenshots/web%20test/Web%20Test%20-%20GTmetrix_structure.jpg" alt="GTmetrix Score - Structure" width=50% height=50%/><br>

---

## Project Highlights
- Strict role separation
- Clear ORM relationships
- Secure access control
- Reusable dashboards
- Predictable user flow

---

## Future Improvements
- WebSocket chat
- Email/SMS notifications
- Tutor ratings
- Pagination & filters
- REST API
- Payments
- Scheduling
- Video lessons
- Mobile app

---

## Credits

### Code:
- Django docs
- Bootstrap docs
- SweetAlert2

### Acknowledgements:
#### I would like to express my gratitude to:
- My lecturer and mentor
- City of Bristol College
- Code Institute
- And a special thank you to Urszula.

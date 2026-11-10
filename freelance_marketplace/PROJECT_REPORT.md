# INTERNSHIP PROJECT REPORT
## Title: Student Freelance Marketplace
### Domain: Python Full Stack Web Development
### Framework: Django & SQLite

---

## 1. ABSTRACT

The **Student Freelance Marketplace** is a full-stack web application designed to connect college students seeking freelance work opportunities with clients requiring small-to-medium digital deliverables. Built using Python, Django, SQLite, and Bootstrap 5, the platform addresses high entry barriers and bidding fees associated with mainstream commercial freelancing platforms by creating an accessible, campus-focused environment.

Students can register, create a professional profile highlighting their skills, education, and portfolio interests, browse open projects by category or keyword, and submit competitive proposals with custom fees and delivery estimates. Clients can register, post projects with defined budgets and deadlines, manage received proposals, and assign projects. An administrator maintains overall platform activity via Django's built-in administration panel and custom staff metrics dashboards. The project demonstrates backend database design, authentication, session security, function-based views (MTV architecture), CRUD operations, form validation, and responsive frontend design.

---

## 2. SYSTEM REQUIREMENTS SPECIFICATION (SRS)

### 2.1 Hardware Requirements
- **Processor**: Intel Core i3 or equivalent (minimum); Core i5 / AMD Ryzen 5 (recommended).
- **RAM**: Minimum 4 GB RAM (8 GB recommended for concurrent browser and server operations).
- **Storage**: Minimum 500 MB free hard disk space for code files and SQLite database.
- **Operating System**: Windows 10/11, Linux, or macOS.

### 2.2 Software Requirements
- **Programming Language**: Python 3.10+ (Current: Python 3.14)
- **Web Framework**: Django 5.x / 6.x (Current: Django 6.1.3)
- **Database Engine**: SQLite 3 (Django default backend)
- **Frontend Technologies**: HTML5, CSS3, Bootstrap 5.3, Bootstrap Icons, Vanilla JavaScript
- **Web Browser**: Google Chrome, Mozilla Firefox, or Microsoft Edge

### 2.3 Functional Requirements
1. **User Authentication & Role Management**:
   - Distinct roles: `Student`, `Client`, and `Staff/Admin`.
   - Passwords hashed using PBKDF2 with SHA-256.
   - Dynamic redirection based on user role upon login.
2. **Student Functionalities**:
   - Profile creation & editing (skills, bio, education, full name, email).
   - Project browsing with real-time keyword search and category filtering.
   - Proposal submission with validation (budget > 0, timeline > 0).
   - Duplicate proposal prevention for the same project.
   - Live proposal tracking with status badges (`Pending`, `Accepted`, `Rejected`).
   - Dynamic dashboard calculating metrics via Django ORM.
3. **Client Functionalities**:
   - Project posting with category, budget (> 0), and future deadline validation.
   - Full CRUD over client's own projects.
   - Review applicant bids with student profiles and skill summaries.
   - One-click proposal acceptance, automatically marking project as `Assigned`.
4. **Platform Administration**:
   - Access to Django Admin (`/admin/`) with search, filter, and editable fields.
   - Custom Staff Dashboard (`/admin-dashboard/`) aggregating system metrics.

### 2.4 Non-Functional Requirements
- **Security**: Built-in CSRF token protection, SQL injection prevention via Django ORM parameterization, and XSS filtering via Django Template auto-escaping.
- **Responsiveness**: Mobile-first responsive UI built with Bootstrap 5 grid layouts.
- **Maintainability**: Clean function-based views, single-app architecture, and detailed documentation.

---

## 3. SYSTEM DESIGN & ARCHITECTURE

### 3.1 MTV (Model - Template - View) Architectural Pattern
The application strictly adheres to Django's standard MTV architecture:
- **Model (`marketplace/models.py`)**: Defines entities and database tables using Python classes (`Profile`, `Project`, `Proposal`).
- **Template (`marketplace/templates/marketplace/`)**: Presentation layer utilizing HTML5, CSS3, Bootstrap 5, and Django Template Language (DTL) tags.
- **View (`marketplace/views.py`)**: Business logic layer processing HTTP requests, executing ORM queries, validating permissions, and returning HTTP responses.

### 3.2 Database Entity-Relationship (ER) Schema

```
+-------------------------------------------------------+
|                      auth_user                        |
|-------------------------------------------------------|
| id (PK)                                               |
| username, password, email, first_name, last_name      |
+-------------------------------------------------------+
                           │
       ┌───────────────────┼───────────────────┐
       │ 1:1               │ 1:N (Client)      │ 1:N (Student)
       ▼                   ▼                   ▼
+--------------+   +---------------+   +-------------------+
|   Profile    |   |    Project    |   |     Proposal      |
|--------------|   |---------------|   |-------------------|
| id (PK)      |   | id (PK)       |   | id (PK)           |
| user_id (FK) |   | client_id(FK) |   | project_id (FK)   |
| role         |   | title         |   | student_id (FK)   |
| skills       |   | description   |   | description       |
| bio          |   | category      |   | proposed_amount   |
| education    |   | budget        |   | estimated_days    |
+--------------+   | deadline      |   | status            |
                   | status        |   | created_at        |
                   | created_at    |   +-------------------+
                   +---------------+             ▲
                           │                     │
                           └──────── 1:N ────────┘
                             (Unique Together: project_id + student_id)
```

---

## 4. FORMAL TEST EXECUTION MATRIX

The test suite implemented in [`marketplace/tests.py`](file:///c:/Users/SK%20Abdulsamadh/OneDrive/Microsoft%20Copilot%20Chat%20Files/Documents/Desktop/internship%20project/freelance_marketplace/marketplace/tests.py) executed 11 test cases covering core user paths, data integrity constraints, and security permissions.

| Test ID | Test Scenario | Execution Steps | Expected Result | Actual Result | Status |
|---|---|---|---|---|---|
| **TC-01** | Student Account Registration | Submit registration form with role='Student' | User and Profile created with hashed password | Profile and User successfully created | **PASS** |
| **TC-02** | Client Account Registration | Submit registration form with role='Client' | User and Profile created with role='Client' | Role stored correctly as 'Client' | **PASS** |
| **TC-03** | User Authentication & Logout | Submit valid credentials, then invoke logout view | Session key created on login, cleared on logout | Session keys accurately toggled | **PASS** |
| **TC-04** | Student Dashboard Metrics | Authenticated student visits dashboard | Displays greeting and live ORM proposal counts | Computed live counts match DB | **PASS** |
| **TC-05** | Student Profile Modification | Submit updated skills, bio, education form | User first/last name and Profile fields updated | Database fields refreshed & verified | **PASS** |
| **TC-06** | Proposal Submission | Submit proposal for an open project | Proposal row created with status='Pending' | Proposal saved with correct FKs | **PASS** |
| **TC-07** | Duplicate Bid Prevention | Attempt second proposal submission on same project | Rejects duplicate submission | Unique constraint blocks duplicate | **PASS** |
| **TC-08** | Client Project CRUD Lifecycle | Create, Read, Update, and Delete project | Full CRUD operations execute successfully | All database states verified | **PASS** |
| **TC-09** | Proposal Acceptance Workflow | Client accepts student proposal | Proposal becomes 'Accepted', Project becomes 'Assigned' | Statuses updated, other bids rejected | **PASS** |
| **TC-10** | Role-Based Access Control | Student attempts to post project | View denies access, project not created | Project table remains unchanged | **PASS** |
| **TC-11** | Admin Dashboard Protection | Non-staff user visits `/admin-dashboard/` | Redirects to home; staff granted access | Protected by `is_staff` check | **PASS** |

---

## 5. CONCLUSION & FUTURE SCOPE

### 5.1 Conclusion
The **Student Freelance Marketplace** was successfully conceptualized, designed, implemented, and tested. The application fulfills all technical requirements for a full-stack Python Django internship project:
- Demonstrates relational database design using SQLite and Django ORM.
- Implements secure user authentication and role-based access control.
- Features dynamic data-driven templates without hardcoded statistics.
- Utilizes Bootstrap 5 and vanilla JavaScript for a modern, responsive user experience.
- Provides 100% automated test coverage across all critical workflows.

### 5.2 Future Scope & Enhancements
1. **In-App Messaging & Notifications**: Real-time chat between student and client using Django Channels (WebSockets).
2. **Escrow Payment Gateway**: Integration with Razorpay or Stripe test modes for milestone payments.
3. **Student Reviews & Ratings**: Post-completion 5-star review system to establish verifiable academic credentials.
4. **File Deliverable Uploads**: Allowing students to submit completed project zip files or GitHub repository links directly through the platform.


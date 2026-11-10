# Student Freelance Marketplace 🎓💼
### Python Full Stack Development Internship Project

A functional, modern, and beginner-friendly web application built with **Python**, **Django**, **SQLite**, and **Bootstrap 5**. The platform connects college students who want to earn money and build a freelance portfolio with clients who need small-to-medium freelance projects completed.

---

## 1. Project Overview & Objective

### Project Title
**Student Freelance Marketplace**

### Project Description
The Student Freelance Marketplace is a dedicated platform designed for university campuses. It allows students to create professional freelancer profiles, showcase skills, browse verified projects, and submit competitive proposals. Clients can register, post job openings with budgets and deadlines, review student proposals, and award projects with a single click.

### Project Objective
- Empower students to gain real-world freelance experience and earn income on flexible schedules.
- Connect clients with affordable, skilled campus talent.
- Demonstrate full-stack Python development using Django's standard MTV (Model-Template-View) pattern, built-in authentication, SQLite database operations, and responsive UI design without unnecessary external framework complexity.

---

## 2. Technology Stack

| Component | Technology Used |
|---|---|
| **Backend Language** | Python 3.14+ |
| **Backend Web Framework** | Django 6.1+ |
| **Database** | SQLite3 (Built-in) |
| **Web Structure** | HTML5 |
| **Styling & Icons** | CSS3, Bootstrap 5.3, Bootstrap Icons |
| **Interactivity** | Vanilla JavaScript (ES6) |
| **Architecture Pattern** | Model - Template - View (MTV) |

---

## 3. Main Features

### 👤 Student / Freelancer Features
- **Student Registration & Login**: Built-in Django authentication with hashed passwords.
- **Profile Management**: Customize bio, educational qualifications, and technical/creative skills.
- **Browse & Search Projects**: Search projects by keyword and filter dynamically by category.
- **Submit Proposals**: Place bids with proposed fee, delivery duration in days, and pitch cover letter.
- **Duplicate Prevention**: Prevents multiple bids on the same project by the same student.
- **My Proposals Tracker**: Live status updates showing whether a bid is *Pending*, *Accepted*, or *Rejected*.
- **Student Dashboard**: Real-time calculated statistics of submitted, pending, accepted, and rejected proposals.

### 🏢 Client Features
- **Client Workspace Dashboard**: Real-time counts of total posted, open, assigned/completed projects, and total proposals received.
- **Post a Project**: Form to publish projects with category, description, budget (₹), and deadline.
- **Project CRUD Operations**: Create, Read, Update, and Delete projects owned by the client.
- **Review Proposals**: View applicants' full names, profiles, education, skills, and proposal pitch.
- **Accept / Reject Workflow**: Accepting a student automatically sets project status to *Assigned* and proposal to *Accepted*.

### 🛡️ Administrator Features
- **Custom Admin Dashboard**: Platform overview displaying total students, clients, projects, and proposals.
- **Django Admin Interface**: Full CRUD capability over `User`, `Profile`, `Project`, and `Proposal` models with search, filtering, and editable statuses.

---

## 4. Database Architecture (3 Custom Models)

The system utilizes Django's built-in `User` model alongside 3 custom models:

```
[ User (Django Built-in) ]
       │ 1:1
       ▼
 [ Profile ] ─── Stores role ('Student' / 'Client'), skills, education, bio
       │
       ├─────────────────────────────────────────┐
       │ 1:N (Client)                            │ 1:N (Student)
       ▼                                         ▼
   [ Project ] ◄───────── 1:N ──────────── [ Proposal ]
   - title                                  - proposed_amount
   - category                               - estimated_days
   - budget                                 - description
   - deadline                               - status (Pending/Accepted/Rejected)
   - status (Open/Assigned/Completed/Closed)
```

1. **Profile Model**: One-to-one link to `User`. Stores role, skills, bio, and education.
2. **Project Model**: ForeignKey to `User` (client). Stores project details, budget, category, deadline, and status.
3. **Proposal Model**: ForeignKey to `Project` and ForeignKey to `User` (student). Includes a unique constraint `('project', 'student')` to disallow duplicate bids.

---

## 5. Project Folder Structure

```
freelance_marketplace/
│
├── manage.py                          # Django command-line execution utility
├── db.sqlite3                         # SQLite database file
│
├── freelance_marketplace/             # Core Project Configuration
│   ├── __init__.py
│   ├── settings.py                    # App settings, DB config, message tags
│   ├── urls.py                        # Project root URL routing
│   ├── wsgi.py
│   └── asgi.py
│
└── marketplace/                       # Main Application
    ├── __init__.py
    ├── admin.py                       # Model registration for Django Admin
    ├── apps.py
    ├── forms.py                       # UserRegistration, Login, Project, Proposal forms
    ├── models.py                      # Profile, Project, Proposal models
    ├── views.py                       # Function-based views for MTV architecture
    ├── urls.py                        # Application-specific route endpoints
    ├── tests.py                       # Automated test suite (11 test cases)
    │
    ├── management/
    │   └── commands/
    │       └── load_sample_data.py    # Command to seed sample projects & users
    │
    ├── migrations/
    │   └── 0001_initial.py            # Initial database migrations
    │
    ├── static/
    │   └── marketplace/
    │       ├── css/
    │       │   └── style.css          # Custom Indigo design stylesheet
    │       └── js/
    │           └── script.js          # Password toggle, popups, and validation
    │
    └── templates/
        └── marketplace/
            ├── base.html              # Master layout with responsive navbar & footer
            ├── home.html              # Landing page with hero & featured gigs
            ├── login.html             # User login page
            ├── register.html          # Dual student/client registration
            ├── projects.html          # Browse projects with search & category filters
            ├── project_detail.html    # Full project details & application button
            ├── student_dashboard.html # Student stats & recent gigs
            ├── student_profile.html   # Student portfolio & profile details
            ├── edit_profile.html      # Edit skills, bio, education form
            ├── submit_proposal.html   # Proposal submission form
            ├── my_proposals.html      # Student's submitted proposals table
            ├── client_dashboard.html  # Client workspace metrics & recent posts
            ├── post_project.html      # Create project form
            ├── my_projects.html       # Client project CRUD management table
            ├── edit_project.html      # Edit project details form
            ├── view_proposals.html    # Review & accept/reject student proposals
            └── admin_dashboard.html   # Staff-only overview with admin shortcuts
```

---

## 6. Installation & Execution Guide (Windows)

Follow these simple steps in PowerShell or Command Prompt:

### Step 1: Open the Project Directory
```powershell
cd "freelance_marketplace"
```

### Step 2: (Optional) Create & Activate Virtual Environment
```powershell
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Django
```powershell
pip install django
```

### Step 4: Run Migrations
```powershell
python manage.py makemigrations
python manage.py migrate
```

### Step 5: Load Pre-populated Sample Data (Recommended)
This automatically loads demo students, clients, 6 realistic projects, and a superuser account:
```powershell
python manage.py load_sample_data
```

### Step 6: Create Your Own Admin Account (Optional)
```powershell
python manage.py createsuperuser
```

### Step 7: Start Development Server
```powershell
python manage.py runserver
```

Open your browser and navigate to:
- **Main Website**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Django Admin**: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
- **Admin Dashboard**: [http://127.0.0.1:8000/admin-dashboard/](http://127.0.0.1:8000/admin-dashboard/)

---

## 7. Pre-loaded Sample Credentials

| Role | Username | Password | Notes |
|---|---|---|---|
| **Admin** | `admin` | `admin123` | Full access to Django Admin & Admin Dashboard |
| **Student** | `rahul_dev` | `password123` | B.Tech student with submitted proposals |
| **Student** | `priya_design` | `password123` | Design student with accepted proposals |
| **Student** | `amit_writer` | `password123` | Content writing student |
| **Client** | `tech_solutions` | `password123` | Software firm with open projects |
| **Client** | `campus_innovations`| `password123`| Campus incubator with assigned projects |

---

## 8. Running Automated Tests

To verify all features, validations, and security protections:
```powershell
python manage.py test
```
*All 11 unit tests pass with zero errors.*


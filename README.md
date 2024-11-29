# Task Management System

A web-based **Task Management System** built with **Django** for managing tasks. The system allows managers to assign tasks to employees, track progress, and mark tasks as complete. It also includes user authentication for secure login and registration.

## Features

- **User Authentication**: Login, Register, and Logout functionality with session management.
- **Task Management**: 
  - Managers can assign tasks to employees.
  - Employees can view and update(task status) their assigned tasks.
  - Managers can set task details, including due dates, descriptions, and completion status.
- **Role-based Access**: Managers and employees have different permissions and views.
- **Notifications**: Alerts and messages on successful and failed actions (e.g., login, task assignment).
- **Database**: PostgreSQL (or SQLite) as the database for storing user and task data.

## Technologies Used

- **Backend**: Django, Python
- **Frontend**: HTML, Bootstrap 5
- **Database**: PostgreSQL (or SQLite for development)
- **Authentication**: Django's built-in authentication system

## Getting Started

To get started with this project on your local machine, follow the instructions below.

### Prerequisites

- Python 3.8+ 
- Django 3.x+
- PostgreSQL (or SQLite)
- Virtual Environment (recommended)

### Installation

1. **Clone the repository:**
   ```
    git clone https://github.com/your-username/task-management.git

2.**Navigate to the project directory:** 

    cd task-management
    
3.**Set up a virtual environment (optional but recommended):** 

    cd task-management
    
4.**Navigate to the project directory:** 

    python -m venv venv
    
5.**Activate the virtual environment(For Windows):** 

    venv\Scripts\activate

6.**Install dependencies:** 

    pip install -r requirements.txt

7.**Run migrations:** 

    pythion manage.py make migrations
    python manage.py migrate

7.**Start the development server:** 

    python manage.py runserver


**Credentials**
Manager Credential
username - manager1
pass - manager1@123

Employee Credential
username - employee1
pass - Employee1@123



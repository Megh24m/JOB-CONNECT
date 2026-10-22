# 🏘️ LocalJobConnect

**Connecting talent with opportunity**

LocalJobConnect is a Django-based web platform that connects job seekers with employers. Designed for blue-collar and service-sector hiring, from shop assistants to electricians, it helps bridge the gap between job seekers and employment opportunities.

## ✨ Features

### 👤 User Roles
- **Job Seeker:** Browse, save, and apply for jobs; track application status; and message employers.
- **Employer:** Post job listings, manage applicants, update application status, and send messages.

### 📋 Job Listings
- Post jobs with category, type, salary, location, vacancy count, and description.
- Jobs organized by category, including retail, hospitality, delivery, electrical work, cooking, and security.
- Multiple job types: Full Time, Part Time, Temporary, Contract, Daily Wage, and Internship.
- Open and Closed job status management.

### 📝 Applications
- One-click job application.
- Application status pipeline: Applied → Viewed → Shortlisted → Interview → Selected / Rejected.
- Full status change history log.
- Job seekers can accept or decline selections.
- Waiting-days counter since the application date.

### 💾 Saved Jobs & History
- Save jobs for later using the ❤️ bookmark feature.
- Track recently viewed jobs.

### 💬 Messaging
- Direct in-platform messaging between job seekers and employers.
- Read/unread message tracking.

### 🔔 Notifications
- In-app notifications for application status changes and messages.

### ⭐ Reviews
- Mutual review system for employers and job seekers.
- Reviews are unlocked only after an application reaches the Selected status.

### 🙍 User Profiles
- Profile image uploads.
- Skills listing.
- Availability toggle.
- Verified badge support.
- Customizable display settings, including timestamp visibility.

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3, Django |
| Database | SQLite (development) / PostgreSQL (production) |
| Frontend | HTML5, CSS3, JavaScript |
| Authentication | Django built-in authentication |
| Media | Django media file handling |

## 📁 Project Structure

```text
LocalJobConnect/
├── accounts/          # User profiles, roles, messaging, settings
├── applications/      # Job applications and status history
├── jobs/              # Job listings, saved jobs, recently viewed
├── notifications/     # In-app notifications
├── reviews/           # Mutual review system
├── templates/         # HTML templates
├── static/            # CSS, JavaScript, and image assets
├── media/             # Uploaded profile images
├── config/            # Django settings and URLs
├── manage.py
├── requirements.txt
├── README.md
└── LICENSE
```

## 🚀 Getting Started

### Prerequisites
- Python 3.10 or later
- pip
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/Megh24m/JOB-CONNECT.git
cd JOB-CONNECT
```

### 2. Create and Activate a Virtual Environment

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

If `requirements.txt` does not exist, generate it in your development environment using:

```bash
pip freeze > requirements.txt
```

### 4. Apply Database Migrations

```bash
python manage.py migrate
```

### 5. Create an Admin Account

```bash
python manage.py createsuperuser
```

Follow the prompts to create your administrator account.

### 6. Run the Development Server

```bash
python manage.py runserver
```

Open your browser and visit:

http://127.0.0.1:8000/

## 🔑 User Roles

Users choose their role during registration:

- **Job Seeker (`jobseeker`):** Browse jobs, submit applications, save listings, track application status, and communicate with employers.
- **Employer (`employer`):** Post job opportunities, manage applicants, update application status, and communicate with job seekers.

## 📸 Pages Overview

| Route | Description |
|---|---|
| `/` | Home / landing page |
| `/jobs/` | Browse job listings |
| `/jobs/<id>/` | Job details |
| `/dashboard/` | Job seeker dashboard |
| `/employer/dashboard/` | Employer dashboard |
| `/my-applications/` | Track applications |
| `/applicants/` | View applicants (employer) |
| `/saved-jobs/` | Bookmarked jobs |
| `/recently-viewed/` | Recently viewed jobs |
| `/messages/` | In-platform messaging |
| `/notifications/` | Notifications inbox |
| `/profile/` | User profile and settings |
| `/reviews/<id>/` | Leave a review |

*Note: Routes are based on the documented project features. Actual routes may vary depending on the Django URL configuration.*

## 🤝 Contributing

Contributions are welcome! For major changes, please open an issue to discuss your proposed changes first.

1. Fork the repository.
2. Create a feature branch:

   ```bash
   git checkout -b feature/your-feature
   ```

3. Commit your changes:

   ```bash
   git commit -m "Add some feature"
   ```

4. Push your branch:

   ```bash
   git push origin feature/your-feature
   ```

5. Open a Pull Request.

## 👩‍💻 Author

**Meghana M**

---

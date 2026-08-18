# NWZ Nutrition & Wellness — Website & Booking System

A Django website built for **NWZ Nutrition & Wellness**, the practice of registered
dietitian nutritionist **Chizitere Chibuzo-Eke**, based in Rumuosi, Port Harcourt.

The site works as a real business website (Home, About, Services, Contact) with a
built-in appointment scheduling system layered in as a core feature — clients can
create an account, book a session, and manage their appointments from a dashboard.

## Features

- **Public pages** — Home, About (bio & credentials), Services, individual Service
  detail pages, and Contact (with a working contact form).
- **Accounts** — sign up, log in, log out (Django's built-in auth, extended with a
  custom sign-up form).
- **Booking system**
  - Book a session for any active service, choosing a date, time and format
    (in-person or online).
  - Server-side validation: no past dates, appointments restricted to NWZ's working
    hours (9:00 AM – 5:00 PM, every day), and no double-booking of a time slot.
  - Client dashboard listing upcoming and past appointments, with the ability to
    cancel an upcoming appointment.
- **Admin panel** — manage services, review/update appointment status, and read
  messages submitted through the contact form, all from `/admin/`.
- **Design** — a custom visual identity (navy/blue/red palette, Fraunces + Inter
  type, a "balanced plate" motif) rather than default Bootstrap styling, with
  vanilla JS for scroll-reveal animations, animated stat counters, and a mobile
  navigation menu.

## Tech stack

- Python 3 / Django 5.0
- SQLite (default database, file-based — no extra setup needed)
- Vanilla HTML, CSS and JavaScript (no frontend build step required)

## Project structure

```
nwz_wellness/
├── manage.py
├── requirements.txt
├── nwz_project/            # Django project settings & URL config
│   ├── settings.py
│   ├── urls.py
│   └── ...
├── core/                   # Main app
│   ├── models.py           # Service, Appointment, ContactMessage
│   ├── forms.py            # Sign-up, booking and contact forms
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   ├── context_processors.py   # Injects business info into every template
│   └── management/commands/seed_services.py   # Seeds default service list
├── templates/
│   ├── base.html
│   └── core/                # home, about, services, contact, book, dashboard, auth
├── static/core/
│   ├── css/style.css
│   └── js/main.js
└── db.sqlite3               # Pre-seeded with NWZ's default services
```

## Getting started

1. **Create a virtual environment (recommended)**
   ```bash
   python3 -m venv venv
   source venv/bin/activate        # Windows: venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Apply migrations**
   ```bash
   python manage.py migrate
   ```
   > The included `db.sqlite3` already has migrations applied and services seeded.
   > If you start from a fresh database, run this step first.

4. **Seed the default services** (skip if using the included database)
   ```bash
   python manage.py seed_services
   ```

5. **Create an admin account**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```
   Visit `http://127.0.0.1:8000/` for the site and `http://127.0.0.1:8000/admin/`
   for the admin panel.

## Business details used in this build

| Field | Value |
|---|---|
| Business name | NWZ |
| Owner | Chizitere Chibuzo-Eke |
| Qualifications | BSc. Human Nutrition & Dietetics, M.IDN |
| Experience | 2 years |
| Address | 22 Marcel Anaenugu Crescent, Farm Rd, Rumuosi, Rivers State |
| Phone / WhatsApp | 0808 118 7444 |
| Email | chiziterechibuzo@gmail.com |
| Hours | Every day, 9:00 AM – 5:00 PM |
| Session formats | In-person and online |

Business details (name, contact info, hours) live in one place —
`core/context_processors.py` — so they can be updated across the whole site by
editing a single dictionary. Services can be added, edited or deactivated from the
Django admin panel without touching any code.

## Notes on content

- The **list of services** (names, durations and prices) and Chizitere's **short
  bio** were not provided in the original intake form, so reasonable, editable
  placeholder content was written for them. Update these anytime from the admin
  panel (Services) or in `core/context_processors.py` (bio/about copy lives in
  `templates/core/about.html`).
- The contact page includes a styled address placeholder in place of an embedded
  map, since no map API key was configured for this build.

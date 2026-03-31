# HSA Management System

A web-based Health Savings Account (HSA) management platform built with Django. Users can register, create HSA accounts, deposit funds, issue virtual debit cards, and make IRS-compliant medical transactions.

Built as a demo project for Human Interest's application process.

## Features

- **User registration & authentication** via Django's built-in auth
- **HSA account creation** with auto-generated account numbers
- **Virtual debit card issuance** (16-digit number, 5-year expiry)
- **Fund deposits** with real-time balance updates
- **IRS-compliant transaction validation** — approved for qualified medical expenses, declined for non-qualified ones
- **Transaction history** with status and decline reasons
- **Admin panel** for managing categories, users, and transactions

## Tech Stack

- **Backend:** Django 4.x, Python 3.8+
- **Database:** SQLite
- **Frontend:** HTML5, CSS3, JavaScript (Django templates)

## Architecture

```
Django Web App
├── InterestApp      # Auth, routing
└── HSA App          # Accounts, cards, transactions, IRS logic
        ↕
    SQLite DB
    (Users, Accounts, Cards, Transactions, Expense Categories)
```

## Getting Started

```bash
git clone https://github.com/myhiraj/humaninterest2025.git
cd humaninterest2025/InterestApp

pip install -r requirements.txt

python manage.py makemigrations
python manage.py migrate

python manage.py runserver
```

Visit [http://localhost:8000](http://localhost:8000) to use the app.

Optionally create a superuser for admin access:

```bash
python manage.py createsuperuser
```

Then visit `/admin` to manage expense categories, users, and transactions.

## IRS Expense Categories

The admin panel lets you define qualified vs. non-qualified medical expense categories. Transactions are automatically approved or declined based on whether the selected category is IRS-qualified (e.g. doctor visits, prescriptions) or not (e.g. cosmetics, gym memberships).

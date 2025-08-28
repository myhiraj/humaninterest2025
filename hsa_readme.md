# HSA Management System

A web-based Health Savings Account (HSA) management platform built with Django that allows users to create HSA accounts, deposit funds, issue virtual debit cards, and process IRS-compliant medical transactions.

## High-Level Architecture

```
┌────────────────────────────────────────────────────────────┐
│                    Django Web Application                  │
├────────────────────────────────────────────────────────────┤
│  Frontend (Templates)     │  Backend (Django Apps)         │
│  ├── User Registration    │  ├── InterestApp (Main)        │
│  ├── HSA Dashboard        │  │   ├── User Authentication   │
│  ├── Transaction Forms    │  │   └── URL Routing           │
│  └── Card Management      │  └── HSA App                   │
│                           │      ├── Account Management    │
│                           │      ├── Card Issuance         │
│                           │      ├── Transaction Logic     │
│                           │      └── IRS Compliance        │
├────────────────────────────────────────────────────────────┤
│                    SQLite Database                         │
│  ├── User Accounts        ├── HSA Accounts                 │
│  ├── Debit Cards          ├── Transactions                 │
│  └── Medical Expense Categories                            │
└────────────────────────────────────────────────────────────┘
```

## Key Features

- **User Registration & Authentication**
- **HSA Account Creation** with unique account numbers
- **Virtual Debit Card Issuance** with card numbers and expiry dates
- **Fund Deposits** to HSA accounts
- **IRS-Compliant Transaction Validation** against qualified medical expenses
- **Real-time Balance Tracking**
- **Transaction History** with detailed records

---

## User Guide

### 1. Sign Up & Create HSA Account

1. Visit the application at local host
2. Click "Sign Up" to create a new account
3. Fill in your details:
   - Username
   - Email
   - Password
   - Confirm Password
4. Submit - Your HSA account is automatically created upon registration

### 2. Issue a Debit Card

1. Log in to your account
2. Navigate to Dashboard → Click "Issue HSA Card"
3. Request a new card - A virtual debit card will be generated with:
   - 16-digit card number
   - Expiry date (5 years from issue)
   - Active status
4. Card is ready for transactions immediately

### 3. Deposit Funds

1. From Dashboard → Click "Deposit Funds"
2. Enter deposit amount (minimum $1.00)
3. Click "Deposit" - Funds are added instantly
4. View updated balance on your dashboard

### 4. Make Transactions

1. From Dashboard → Click "Make Purchase"
2. Fill in transaction details:
   - Merchant/Provider (e.g., "ABC Medical Center")
   - Amount (cannot exceed available balance)
   - Medical Expense Category (choose from dropdown)
3. Submit transaction
4. Automatic validation:
   - **Approved:** IRS-qualified expenses (doctor visits, prescriptions, etc.)
   - **Declined:** Non-qualified expenses (cosmetics, gym memberships, etc.)

### 5. View Transaction History

1. From Dashboard → Click "View All Transactions"
2. Review all transactions with:
   - Transaction details
   - Approval/decline status
   - Decline reasons (if applicable)
   - Running balance

---

## Installation & Setup

### Prerequisites
- Python 3.8+
- Django 4.0+

### Quick Start
```bash
# Clone the repository
git clone <repository-url>
cd InterestApp

# Install dependencies
pip install django

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Run the development server
python manage.py runserver
```

---

## Superuser Administration

### Access Admin Panel
1. Create superuser: `python manage.py createsuperuser`
2. Visit: `/admin`
3. Log in with superuser credentials

### Manage Medical Expense Categories

#### Add New Categories
1. Navigate to: Admin Panel → HSA → Medical Expense Categories
2. Click "Add Medical Expense Category"
3. Fill in details:
   - Name: Category name (e.g., "Prescription Medications")
   - Description: Detailed description
   - Is Qualified: ✅ Check for IRS-qualified expenses
4. Save

### Manage User Accounts
1. Navigate to: Admin Panel → Authentication → Users
2. View/Edit user accounts, HSA balances, and transaction history
3. Activate/Deactivate user accounts as needed

### Monitor Transactions
1. Navigate to: Admin Panel → HSA → Transactions
2. Review all transactions across all users
3. Filter by status: Approved, Declined, Pending
4. Export data for compliance reporting

---

## Technical Stack

- Backend: Django 4.x, Python
- Database: SQLite (development) 
- Frontend: HTML5, CSS3, JavaScript
- Authentication: Django built-in authentication

---

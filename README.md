# Healthcare Clinic Management System

A comprehensive clinic management solution built with Django, designed to streamline healthcare operations and enhance patient care.

## Overview

The Healthcare Clinic Management System (CMS) is an integrated platform that manages administrative and clinical functions of health clinics. The system provides a user-friendly interface for managing patients, appointments, medical records, lab results, and more.

## Features

- **Patient Management**: Registration, medical records, and hospitalization tracking
- **Appointment Scheduling**: Online booking.
- **Surgery Management**: Schedule and track surgical procedures
- **Doctor & Staff Management**: Profile and schedule management
- **Billing System**: Generate and track payments
- **Inventory Management**: Track medical supplies
- **Admin Dashboard**: Comprehensive clinic operations monitoring

## Tech Stack

- **Backend**: Django 4.2+
- **Database**: SQLite (default), can be configured for PostgreSQL in production
- **Authentication**: Django Authentication System
- **API**: Django REST Framework

## Prerequisites

- Python 3.8+
- pip
- virtualenv (recommended)
- Node.js 16+ (for React frontend)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/healthcare-cms.git
cd healthcare-cms
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Setup database:
```bash
python manage.py migrate
```

5. Create superuser:
```bash
python manage.py createsuperuser
```

6. Run development server:
```bash
python manage.py runserver
```

## Development Setup

1. Install frontend dependencies:
```bash
cd frontend
npm install
```

2. Run frontend development server:
```bash
npm start
```

## Database Configuration

The project uses SQLite by default for development. The database configuration can be found in `settings.py`
For production deployment, it's recommended to switch to PostgreSQL.

## Testing
Run the test suite:
```bash
python manage.py test
```

## Security Features

- Role-based access control
- Data encryption at rest and in transit
- Secure session management
- CSRF protection
- SQL injection prevention
- XSS protection

## Support

For support, please open an issue in the GitHub repository or contact us.

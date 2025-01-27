# Internal CRM Software

A CLI-based Customer Relationship Management (CRM) application designed to manage users, customers, contracts, and events efficiently.

## Features
- Manage users (create, update, delete).
- Manage customers (create, update, delete).
- Manage contracts (create, sign, update, delete).
- Manage events (create, assign support, update, delete).
- Integrated error tracking and logging with Sentry.

## Prerequisites
- Python 3.8+
- MySQL installed and running

## Installation
1. Clone the repository:
   ```bash
   git clone git@github.com:MouloudB-24/internal_CRM_software.git
   cd internal_CRM_software
   
2. Create and activate a virtual environment:
    ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install dependencies
    ```bash
   pip install -r requirements.txt

4. Set up your .env file:
   - Create a .env file in the project root using .env.example as a template.
   - Fill in your database credentials and Sentry DSN.

5. Initialize the database and create initial tables
    ```bash
   flask db init
   flask db upgrade
   flask db upgrade

## Start application
```bash
    python cli.py







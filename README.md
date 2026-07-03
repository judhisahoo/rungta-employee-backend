# Rungta Employee REST API

Flask REST API for organisation and employee management with PostgreSQL, Swagger UI, SQLAlchemy, and Flask-Migrate.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Edit `.env` with your PostgreSQL connection information.

## Database Migration

Create the database in PostgreSQL, then run:

```bash
flask db upgrade
```

The initial migration is included at `migrations/versions/0001_initial_schema.py`.

## Run

```bash
flask run
```

API base URL:

```text
http://127.0.0.1:5001
```

Swagger UI:

```text
http://127.0.0.1:5001/swagger
```

## Deploy To Render

The repository includes `render.yaml` with the Render build and start commands.

```text
Python Version: 3.12.7
Build Command: pip install -r requirements.txt
Start Command: gunicorn run:app --bind 0.0.0.0:$PORT
```

In Render, create a new Web Service from this repository. Add `DATABASE_URL` in
the service environment settings. Render generates `SECRET_KEY` from
`render.yaml`; if you do not use the blueprint flow, add `SECRET_KEY` manually.

For a manual Web Service deploy, add this environment variable in Render:

```env
PYTHON_VERSION=3.12.7
```

`DATABASE_URL` must point to a reachable PostgreSQL database. Without it, the app
falls back to `POSTGRES_HOST=localhost`, which only works when PostgreSQL is
running locally.

The Render blueprint runs database migrations before each deploy:

```bash
flask --app run.py db upgrade
```

To run migrations manually from your machine, first set `DATABASE_URL` to your
PostgreSQL connection string, then run the same command.

## Main Endpoints

```text
GET    /organisations
POST   /organisations
GET    /organisations/<id>
PUT    /organisations/<id>
DELETE /organisations/<id>

GET    /designations
POST   /designations
GET    /designations/<id>
PUT    /designations/<id>
DELETE /designations/<id>

GET    /employees
POST   /employees
GET    /employees/<id>
PUT    /employees/<id>
DELETE /employees/<id>
```

## Example Organisation Payload

```json
{
  "name": "Head Office",
  "parent_id": null
}
```

## Example Designation Payload

```json
{
  "name": "Supervisor"
}
```

## Example Employee Payload

`password` is generated automatically as Base64 of `employee_code`. For example, `EMP001` becomes `RU1QMDAx`.

```json
{
  "employee_code": "EMP001",
  "name": "Amit",
  "middle_name": "Kumar",
  "surname": "Sharma",
  "gender": "male",
  "guardian_name": "Ramesh Sharma",
  "date_of_birth": "1990-01-15",
  "place_of_birth": "Kolkata",
  "nationality": "Indian",
  "education_level": "Graduate",
  "date_of_joining": "2024-04-01",
  "designation": 1,
  "category": "Skilled",
  "employment_type": "FT",
  "mobile_number": "9876543210",
  "universal_account_number": "100200300400",
  "pan": "ABCDE1234F",
  "nominee": "Spouse",
  "eps_nps": "EPS",
  "family_details": [{"name": "Family Member", "relation": "Spouse"}],
  "posting_details": {"location": "Plant 1", "department": "Operations"},
  "pay": 25000,
  "promotion": "Promoted to Supervisor in 2025",
  "esic_insurance_no": "ESIC123",
  "aadhaar_number": "123412341234",
  "bank_account_no": "1234567890",
  "bank_ifsc": "SBIN0000001",
  "branch": "Main Branch",
  "present_address": "Current address",
  "permanent_address": "Permanent address",
  "service_book_no": "SB001",
  "date_of_exit": null,
  "reason_for_exit": null,
  "mark_of_identification": "Mole on right hand",
  "photo": "https://example.com/photo.jpg",
  "specimen_signature_thumb_impression": "https://example.com/signature.jpg",
  "remarks": "Active employee",
  "organisation_id": 1,
  "employee_app_type": "employee"
}
```

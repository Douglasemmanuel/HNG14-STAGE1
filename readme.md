# Backend Wizards — Stage 1: Data Persistence & API Design

## 📌 Overview

This project is a Django REST Framework (DRF) backend service that:

* Accepts a name input
* Fetches data from three external APIs
* Applies classification logic
* Stores the processed result in a database
* Exposes RESTful endpoints to manage the data

The system is designed with **idempotency**, **robust error handling**, and **clean API design** in mind.

---

## ⚙️ Tech Stack

* **Backend:** Django, Django REST Framework
* **Database:** PostgreSQL / SQLite (development)
* **HTTP Client:** Requests
* **UUID Generation:** UUID v7 (`uuid6`)
* **Deployment:** Railway / Vercel / Heroku

---

## 🌐 External APIs Used

| API         | Purpose             |
| ----------- | ------------------- |
| Genderize   | Predict gender      |
| Agify       | Predict age         |
| Nationalize | Predict nationality |

---

## 🧠 Business Logic

### Age Classification

| Age Range | Group    |
| --------- | -------- |
| 0–12      | child    |
| 13–19     | teenager |
| 20–59     | adult    |
| 60+       | senior   |

### Nationality Selection

* Select the country with the **highest probability** from the Nationalize response.

---

## 🚀 API Endpoints

### 1. Create Profile

**POST** `/api/profiles`

#### Request

```json
{
  "name": "ella"
}
```

#### Response (201 Created)

```json
{
  "status": "success",
  "data": {
    "id": "uuid",
    "name": "ella",
    "gender": "female",
    "gender_probability": 0.99,
    "sample_size": 1234,
    "age": 46,
    "age_group": "adult",
    "country_id": "US",
    "country_probability": 0.85,
    "created_at": "2026-04-01T12:00:00Z"
  }
}
```

#### Idempotency Behavior

If profile already exists:

```json
{
  "status": "success",
  "message": "Profile already exists",
  "data": { ...existing profile... }
}
```

---

### 2. Get Single Profile

**GET** `/api/profiles/{id}`

#### Response (200)

```json
{
  "status": "success",
  "data": { ...profile... }
}
```

---

### 3. Get All Profiles

**GET** `/api/profiles`

#### Optional Query Params

* `gender`
* `country_id`
* `age_group`

#### Example

```
/api/profiles?gender=male&country_id=NG
```

#### Response (200)

```json
{
  "status": "success",
  "count": 2,
  "data": [
    {
      "id": "id-1",
      "name": "emmanuel",
      "gender": "male",
      "age": 25,
      "age_group": "adult",
      "country_id": "NG"
    }
  ]
}
```

---

### 4. Delete Profile

**DELETE** `/api/profiles/{id}`

#### Response

```
204 No Content
```

---

## ❌ Error Handling

All errors follow a consistent structure:

```json
{
  "status": "error",
  "message": "Error message"
}
```

### Error Codes

| Code | Description           |
| ---- | --------------------- |
| 400  | Missing or empty name |
| 422  | Invalid data type     |
| 404  | Profile not found     |
| 502  | External API failure  |

### External API Failure Example

```json
{
  "status": "error",
  "message": "Genderize returned an invalid response"
}
```

---

## 🧪 Edge Case Handling

* Genderize returns `null` or `count = 0` → ❌ reject
* Agify returns `null age` → ❌ reject
* Nationalize returns no country → ❌ reject

---

## 🗄️ Data Model

```text
Profile
--------
id (UUID v7)
name (unique)
gender
gender_probability
sample_size
age
age_group
country_id
country_probability
created_at (UTC ISO 8601)
```

---

## 🔁 Idempotency

* Profiles are **unique by name**
* Duplicate requests return existing data instead of creating new records

---

## 🔍 Filtering

Supports case-insensitive filtering:

```
/api/profiles?gender=Male
/api/profiles?country_id=ng
```

---

## 🌍 CORS

CORS is enabled globally:

```python
CORS_ALLOW_ALL_ORIGINS = True
```

---

## ⚡ Setup Instructions

### 1. Clone the repo

```bash
git clone <your-repo-url>
cd project
```

### 2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run migrations

```bash
python manage.py migrate
```

### 5. Start server

```bash
python manage.py runserver
```

---

## 🚀 Deployment

This project can be deployed on:

* Railway (recommended)
* Heroku
* AWS
* Vercel (via serverless adapter)

### Production Command

```bash
gunicorn project.wsgi
```

---

## ✅ Evaluation Coverage

| Criteria              | Status |
| --------------------- | ------ |
| API Design            | ✅      |
| Multi-API Integration | ✅      |
| Data Persistence      | ✅      |
| Idempotency           | ✅      |
| Filtering             | ✅      |
| Data Modeling         | ✅      |
| Error Handling        | ✅      |
| Response Structure    | ✅      |

---


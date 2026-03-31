# Buyer Portal

A simple buyer portal for a real-estate broker.  
Users can register, login, and manage their favourite properties. The dashboard shows user info and allows adding/removing favourites.

---

## Features

- User registration and login (email + password)
- JWT-based authentication
- Buyer dashboard:
  - Shows user name and role
  - Lists “My Favourites”
  - Add/remove properties to favourites
- Backend validation and error handling
- Frontend with React for forms and dashboard

---

## Tech Stack

- **Backend:** FastAPI, SQLAlchemy, MySQL, Passlib (password hashing), Python 3.13  
- **Frontend:** React, Axios  
- **Authentication:** JWT (JSON Web Tokens)

---

## Folder Structure

buyer_portal/
├─ backend/
│ ├─ main.py
│ ├─ models.py
│ ├─ auth.py
│ ├─ database.py
│ ├─ requirements.txt
│ └─ .env.example
└─ frontend/
├─ src/
│ ├─ Register.jsx
│ ├─ Login.jsx
│ └─ Dashboard.jsx
└─ package.json


---

## Setup Instructions

### 1. Backend

1. Create a `.env` file in `backend/` based on `.env.example`:

2. Install dependencies:

```bash
cd backend
pip install -r requirements.txt

3. Run the server:
uvicorn main:app --reload




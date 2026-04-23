# 🏥 SmartCare Clinic API

### 🚀 FastAPI Backend Project

---

## 📌 Project Overview

**SmartCare Clinic API** is a RESTful backend application built using FastAPI to manage doctors and medical appointments.

👉 *“Smart Healthcare, Simplified.”*

This project focuses on implementing real-world backend logic such as filtering, searching, sorting, pagination, and appointment workflow handling using in-memory data.

---

## 🎯 Objective

To build a backend system that can:

* Manage doctors and their availability
* Handle appointment booking and lifecycle
* Apply business rules like fee calculation & discounts
* Support dynamic data operations (filter/search/sort/page)

---

## 🏥 Features

### 👨‍⚕️ Doctor Management

* Get all doctors with availability count
* Add new doctor with validation
* Prevent duplicate doctor names
* Update doctor fee & availability
* Delete doctor *(only if no active appointments)*
* Get doctor by ID

---

### 📅 Appointment Management

* Create appointment with validation
* Prevent booking unavailable doctors
* Automatic fee calculation
* Track appointment status

---

## 💰 Fee Calculation Rules

| Appointment Type | Fee  |
| ---------------- | ---- |
| In-person        | 100% |
| Video            | 80%  |
| Emergency        | 150% |

👉 Senior Citizen → **15% discount applied after calculation**

---

## 🔄 Appointment Workflow

```id="q1a2b3"
Scheduled → Confirmed → Completed  
Scheduled → Cancelled  
```

---

## 🔍 Data Operations

### ✅ Filtering (`/doctors/filter`)

* Specialization
* Max fee
* Min experience
* Availability

### 🔎 Searching

* Doctors → name / specialization
* Appointments → patient name

### 📊 Sorting

* Doctors → fee, name, experience
* Appointments → final_fee, date

### 📄 Pagination

* Doctors → `/doctors/page`
* Appointments → `/appointments/page`

---

## 🔗 API Endpoints

### 👨‍⚕️ Doctors

| Method | Endpoint         | Description      |
| ------ | ---------------- | ---------------- |
| GET    | /doctors         | Get all doctors  |
| GET    | /doctors/{id}    | Get doctor by ID |
| POST   | /doctors         | Add new doctor   |
| PUT    | /doctors/{id}    | Update doctor    |
| DELETE | /doctors/{id}    | Delete doctor    |
| GET    | /doctors/summary | Doctors summary  |

---

### 🔍 Advanced Doctor APIs

| Endpoint        | Description                         |
| --------------- | ----------------------------------- |
| /doctors/filter | Filter doctors                      |
| /doctors/search | Search doctors                      |
| /doctors/sort   | Sort doctors                        |
| /doctors/page   | Pagination                          |
| /doctors/browse | Combined search + sort + pagination |

---

### 📅 Appointments

| Method | Endpoint      | Description          |
| ------ | ------------- | -------------------- |
| GET    | /appointments | Get all appointments |
| POST   | /appointments | Create appointment   |

---

### 🔄 Appointment Workflow APIs

| Endpoint                    | Description          |
| --------------------------- | -------------------- |
| /appointments/{id}/confirm  | Confirm appointment  |
| /appointments/{id}/cancel   | Cancel appointment   |
| /appointments/{id}/complete | Complete appointment |

---

### 🔍 Advanced Appointment APIs

| Endpoint                     | Description              |
| ---------------------------- | ------------------------ |
| /appointments/active         | Active appointments      |
| /appointments/by-doctor/{id} | Doctor-wise appointments |
| /appointments/search         | Search appointments      |
| /appointments/sort           | Sort appointments        |
| /appointments/page           | Pagination               |

---

## 🧪 Validation Rules

* Patient name ≥ 2 characters
* Reason ≥ 5 characters
* Doctor ID must exist
* Doctor must be available for booking
* Appointment type supports: `video`, `in-person`, `emergency`

---

## 📂 Project Structure

```id="z9x8y7"
project/
│── main.py
│── README.md
│── screenshots/
```

---

## ▶️ How to Run

### 1️⃣ Install dependencies

```bash id="abc123"
pip install fastapi uvicorn
```

### 2️⃣ Run server

```bash id="def456"
uvicorn main:app --reload
```

### 3️⃣ Open in browser

👉 http://127.0.0.1:8000/docs

---

## 📸 Screenshots

```md id="ghi789"
![Home](screenshots/Q1_home.png)
![Doctors](screenshots/Q2_get_doctors.png)
```

---

## 💡 Design Highlights

* Clean API structure using FastAPI
* Pydantic models for validation
* Helper functions for reusable logic
* Business rules implemented (availability, deletion checks, fee logic)
* In-memory data handling for simplicity

---

## ⚠️ Limitations

* Data stored in memory (resets on restart)
* No authentication system
* No database integration

---

## 🚀 Future Improvements

* Add database (PostgreSQL / MongoDB)
* Add authentication (JWT)
* Add time-slot booking
* Deploy API online

---

## 👩‍💻 Author

### Swathi Gounikadi
#### Data Science Trainee – Innomatics Research Labs

---

## ⭐ Final Note

This project demonstrates strong backend fundamentals and is a solid foundation for building production-level applications.


# 🏥 SmartCare Clinic API

### Python FastAPI Backend System 🚀

---

## 📌 Project Overview

**SmartCare Clinic API** is a RESTful backend application built using **FastAPI** to manage doctors, appointments, and consultation workflows.

👉 **Welcome to SmartCare Clinic API – Smart Healthcare, Simplified.**

This project simulates a **real-world clinic management system** and demonstrates strong backend development concepts such as API design, validation, and business logic handling.

---

## 🎯 Objective

The objective of this project is to build a **complete backend system** that handles:

* Doctor management
* Appointment booking
* Consultation workflow
* Real-time filtering, searching, and pagination

---

## 🏥 Features

### 👨‍⚕️ Doctor Management

* Add new doctors with validation
* Prevent duplicate doctor entries
* Update consultation fee & availability
* Delete doctor *(only if no active appointments)*
* Get doctor details and list

---

### 📅 Appointment Management

* Book appointment with validation
* Auto-assign doctor based on availability
* Prevent booking unavailable doctors
* Manage full appointment lifecycle

---

## 💰 Fee Calculation Rules

| Appointment Type | Fee Applied |
| ---------------- | ----------- |
| In-person        | 100%        |
| Video            | 80%         |
| Emergency        | 150%        |

👉 **Senior Citizen Discount:**
Additional **15% reduction** applied after fee calculation

---

## 🔄 Appointment Workflow

### Status Flow:

* **Scheduled → Confirmed → Completed**
* **Scheduled → Cancelled**

---

## 🔍 Data Operations

### ✅ Filtering

* Specialization
* Maximum fee
* Minimum experience
* Availability

---

### 🔎 Searching

* Doctors → by name & specialization
* Appointments → by patient name

---

### 📊 Sorting

* Doctors → fee, name, experience
* Appointments → date, final fee

---

### 📄 Pagination

* Supported for both doctors and appointments

---

## 🔗 API Endpoints

### 👨‍⚕️ Doctors

| Method | Endpoint        | Description      |
| ------ | --------------- | ---------------- |
| GET    | `/doctors`      | Get all doctors  |
| GET    | `/doctors/{id}` | Get doctor by ID |
| POST   | `/doctors`      | Add new doctor   |
| PUT    | `/doctors/{id}` | Update doctor    |
| DELETE | `/doctors/{id}` | Delete doctor    |

---

### 🔍 Advanced Doctor APIs

| Endpoint          | Description                         |
| ----------------- | ----------------------------------- |
| `/doctors/filter` | Filter doctors                      |
| `/doctors/search` | Search doctors                      |
| `/doctors/sort`   | Sort doctors                        |
| `/doctors/page`   | Pagination                          |
| `/doctors/browse` | Combined search + sort + pagination |

---

### 📅 Appointments

| Method | Endpoint        | Description          |
| ------ | --------------- | -------------------- |
| GET    | `/appointments` | Get all appointments |
| POST   | `/appointments` | Create appointment   |

---

### 🔄 Appointment Workflow APIs

| Endpoint                      | Description          |
| ----------------------------- | -------------------- |
| `/appointments/{id}/confirm`  | Confirm appointment  |
| `/appointments/{id}/cancel`   | Cancel appointment   |
| `/appointments/{id}/complete` | Complete appointment |

---

### 🔍 Advanced Appointment APIs

| Endpoint                       | Description             |
| ------------------------------ | ----------------------- |
| `/appointments/active`         | Get active appointments |
| `/appointments/search`         | Search appointments     |
| `/appointments/sort`           | Sort appointments       |
| `/appointments/page`           | Pagination              |
| `/appointments/by-doctor/{id}` | Appointments by doctor  |

---

## 🧪 Validation Rules

* Patient name ≥ 2 characters
* Reason ≥ 5 characters
* Doctor ID must be valid
* Appointment date uses proper date format
* Appointment type restricted using Enum

---

## 📂 Project Structure

```
project/
│── main.py
│── README.md
```

---

## ▶️ How to Run

### 1️⃣ Install dependencies

```bash
pip install fastapi uvicorn
```

### 2️⃣ Run the server

```bash
uvicorn main:app --reload
```

### 3️⃣ Open in browser

👉 Swagger UI:
http://127.0.0.1:8000/docs

---

## 💡 Design Highlights

* Clean REST API structure
* Use of Pydantic models for validation
* Enum-based request validation
* Proper error handling using HTTPException
* Modular helper functions
* Business rules implemented (doctor availability, deletion checks)
* In-memory storage for simplicity

---

## 🚀 Future Enhancements

* 🗄 Database integration (PostgreSQL / MongoDB)
* 🔐 Authentication (JWT Login System)
* ⏰ Time-slot based booking system
* 💳 Payment integration
* 🤖 AI-based doctor recommendation system

---

## 👩‍💻 Author

**Swathi Gounikadi**
Data Science Trainee
Innomatics Research Labs

from fastapi import FastAPI, Query
from pydantic import BaseModel, Field

app = FastAPI()

# -----------------Data------------------

ddoctors = [
    {"id": 1, "name": "Dr. Rajesh Kumar", "specialization": "Cardiologist", "fee": 800, "experience_years": 12, "is_available": True},
    {"id": 2, "name": "Dr. Priya Verma", "specialization": "Dermatologist", "fee": 500, "experience_years": 8, "is_available": True},
    {"id": 3, "name": "Dr. Arun Desai", "specialization": "Pediatrician", "fee": 600, "experience_years": 10, "is_available": False},
    {"id": 4, "name": "Dr. Neha Patel", "specialization": "General Physician", "fee": 300, "experience_years": 5, "is_available": True},
    {"id": 5, "name": "Dr. Vikram Singh", "specialization": "Cardiologist", "fee": 900, "experience_years": 15, "is_available": True},
    {"id": 6, "name": "Dr. Shreya Nair", "specialization": "Dermatologist", "fee": 450, "experience_years": 7, "is_available": False},
    {"id": 7, "name": "Dr. Kiran Reddy", "specialization": "Orthopedic", "fee": 700, "experience_years": 11, "is_available": True},
    {"id": 8, "name": "Dr. Anjali Mehta", "specialization": "Gynecologist", "fee": 650, "experience_years": 9, "is_available": True},
]

appointments = []
appt_counter = 1


# -----------------Endpoint 1 - Home------------------
@app.get('/')
def home():
    return {"message": "Welcome to SmartCare Clinic API"}



# -----------------Helper Functions------------------
def find_doctor(doctor_id: int):
    return next((doc for doc in doctors if doc["id"] == doctor_id), None)

def calculate_fee(base_fee, appointment_type, senior_citizen):
    multiplier = {
        "video": 0.8,
        "in-person": 1,
        "emergency": 1.5
    }

    fee = base_fee * multiplier.get(appointment_type, 1)
    original_fee = fee

    if senior_citizen:
        fee *= 0.85

    return int(original_fee), int(fee)


# -----------------Endpoint 2 - Get All Doctors------------------
@app.get("/doctors")
def get_doctors():
    available_count = sum(1 for d in doctors if d["is_available"])

    return {
        "total": len(doctors),
        "available_count": available_count,
        "doctors": doctors
    }


# -----------------Pydantic Model for New Doctor------------------
class NewDoctor(BaseModel):
    name: str = Field(..., min_length=2)
    specialization: str = Field(..., min_length=2)
    fee: int = Field(..., gt=0)
    experience_years: int = Field(..., gt=0)
    is_available: bool = True

# -----------------Endpoint 3 - Add Doctor------------------
@app.post("/doctors", status_code=201)
def add_doctor(doc: NewDoctor):
    new_id = max([d["id"] for d in doctors], default=0) + 1

    if any(d["name"].lower() == doc.name.lower() for d in doctors):
        return {"error": "Doctor with this name already exists"}

    new_doc = {"id": new_id, **doc.dict()}
    doctors.append(new_doc)

    return {"doctor": new_doc}


# -----------------Endpoint 4 - Doctors Summary------------------
@app.get("/doctors/summary")
def doctors_summary():
    if not doctors:
        return {"error": "No doctors available"}

    available_count = sum(d["is_available"] for d in doctors)

    most_exp = max(doctors, key=lambda d: d["experience_years"])
    cheapest_fee = min(d["fee"] for d in doctors)

    specialization_count = {}
    for spec in [d["specialization"] for d in doctors]:
        specialization_count[spec] = specialization_count.get(spec, 0) + 1

    return {
        "total_doctors": len(doctors),
        "available_count": available_count,
        "most_experienced": most_exp["name"],
        "cheapest_fee": cheapest_fee,
        "specializations": specialization_count
    }


# -----------------Endpoint 5 - Get All Appointments------------------
@app.get("/appointments")
def get_appointments():
    return {
        "total": len(appointments),
        "appointments": appointments
    }


# -----------------Pydantic Model------------------
class AppointmentRequest(BaseModel):
    patient_name: str = Field(..., min_length=2)
    doctor_id: int = Field(..., gt=0)
    date: str = Field(..., min_length=8)
    reason: str = Field(..., min_length=5)
    appointment_type: str = "in-person"
    senior_citizen: bool = False

# -----------------Endpoint 6 - Create Appointment------------------
@app.post("/appointments")
def create_appointment(request: AppointmentRequest):
    global appt_counter

    doctor = find_doctor(request.doctor_id)

    if doctor is None:
        return {"error": "Doctor not found"}

    if not doctor["is_available"]:
        return {"error": "Doctor not available"}

    original_fee, final_fee = calculate_fee(
        doctor["fee"],
        request.appointment_type,
        request.senior_citizen
    )

    appointment = {
        "appointment_id": appt_counter,
        "patient": request.patient_name,
        "doctor_name": doctor["name"],
        "doctor_id": doctor["id"],
        "date": request.date,
        "type": request.appointment_type,
        "original_fee": original_fee,
        "final_fee": final_fee,
        "status": "scheduled"
    }

    appointments.append(appointment)
    appt_counter += 1

    return {
        "message": "Appointment created",
        "appointment": appointment
    }


# -----------------Endpoint 7 - Filter Doctors------------------
@app.get("/doctors/filter")
def filter_doctors(
    specialization: str = Query(None),
    max_fee: int = Query(None),
    min_experience: int = Query(None),
    is_available: bool = Query(None)
):
    result = doctors

    filters = [
        (specialization, lambda d: d["specialization"] == specialization),
        (max_fee, lambda d: d["fee"] <= max_fee),
        (min_experience, lambda d: d["experience_years"] >= min_experience),
        (is_available, lambda d: d["is_available"] == is_available),
    ]

    for value, condition in filters:
        if value is not None:
            result = list(filter(condition, result))

    return {
        "total_found": len(result),
        "doctors": result
    }


# -----------------Endpoint 8 - Update Doctor------------------
@app.put("/doctors/{doctor_id}")
def update_doctor(
    doctor_id: int,
    fee: int = Query(None),
    is_available: bool = Query(None)
):
    doctor = find_doctor(doctor_id)

    if not doctor:
        return {"error": "Doctor not found"}

    updates = {
        "fee": fee,
        "is_available": is_available
    }

    for key, value in updates.items():
        if value is not None:
            doctor[key] = value

    return {"updated_doctor": doctor}


# -----------------Endpoint 9 - Delete Doctor------------------
@app.delete("/doctors/{doctor_id}")
def delete_doctor(doctor_id: int):
    doctor = find_doctor(doctor_id)

    if not doctor:
        return {"error": "Doctor not found"}

    # check active appointments
    active = any(
        a["doctor_id"] == doctor_id and a["status"] == "scheduled"
        for a in appointments
    )

    if active:
        return {"error": "Doctor has active appointments"}

    doctors.remove(doctor)

    return {"message": "Doctor deleted successfully"}


# -----------------Helper for Appointment------------------
def find_appointment(appointment_id: int):
    return next((a for a in appointments if a["appointment_id"] == appointment_id), None)


# -----------------Endpoint 10 - Confirm Appointment------------------
@app.post("/appointments/{appointment_id}/confirm")
def confirm_appointment(appointment_id: int):
    appt = find_appointment(appointment_id)

    if not appt:
        return {"error": "Appointment not found"}

    appt["status"] = "confirmed"

    return {"message": "Appointment confirmed", "appointment": appt}


# -----------------Endpoint 11 - Cancel Appointment------------------
@app.post("/appointments/{appointment_id}/cancel")
def cancel_appointment(appointment_id: int):
    appt = find_appointment(appointment_id)

    if not appt:
        return {"error": "Appointment not found"}

    appt["status"] = "cancelled"

    # make doctor available again
    doctor = find_doctor(appt["doctor_id"])
    if doctor:
        doctor["is_available"] = True

    return {"message": "Appointment cancelled", "appointment": appt}


# -----------------Endpoint 12 - Complete Appointment------------------
@app.post("/appointments/{appointment_id}/complete")
def complete_appointment(appointment_id: int):
    appt = find_appointment(appointment_id)

    if not appt:
        return {"error": "Appointment not found"}

    appt["status"] = "completed"

    return {"message": "Appointment completed", "appointment": appt}


# -----------------Endpoint 13 - Active Appointments------------------
@app.get("/appointments/active")
def active_appointments():
    result = [
        a for a in appointments
        if a["status"] in ["scheduled", "confirmed"]
    ]

    return {
        "total": len(result),
        "appointments": result
    }


# -----------------Endpoint 14 - Appointments by Doctor------------------
@app.get("/appointments/by-doctor/{doctor_id}")
def appointments_by_doctor(doctor_id: int):
    result = [a for a in appointments if a["doctor_id"] == doctor_id]

    return {
        "total": len(result),
        "appointments": result
    }


# -----------------Endpoint 15 - Search Doctors------------------
@app.get("/doctors/search")
def search_doctors(keyword: str = Query(...)):
    keyword = keyword.lower()

    result = [
        d for d in doctors
        if keyword in d["name"].lower() or keyword in d["specialization"].lower()
    ]

    if not result:
        return {"message": f"No doctors found for '{keyword}'"}

    return {
        "total_found": len(result),
        "doctors": result
    }


# -----------------Endpoint 16 - Sort Doctors------------------
@app.get("/doctors/sort")
def sort_doctors(
    sort_by: str = Query("fee"),
    order: str = Query("asc")
):
    if sort_by not in ["fee", "name", "experience_years"]:
        return {"error": "Invalid sort field"}

    reverse = order == "desc"

    sorted_list = sorted(doctors, key=lambda d: d[sort_by], reverse=reverse)

    return {
        "sort_by": sort_by,
        "order": order,
        "doctors": sorted_list
    }

# -----------------Endpoint 17 - Pagination Doctors------------------
@app.get("/doctors/page")
def paginate_doctors(
    page: int = Query(1, ge=1),
    limit: int = Query(3, ge=1)
):
    total = len(doctors)
    start = (page - 1) * limit

    return {
        "page": page,
        "limit": limit,
        "total": total,
        "total_pages": -(-total // limit),
        "doctors": doctors[start:start + limit]
    }


# -----------------Endpoint 18 - Browse Doctors------------------
@app.get("/doctors/browse")
def browse_doctors(
    keyword: str = Query(None),
    sort_by: str = Query("fee"),
    order: str = Query("asc"),
    page: int = Query(1, ge=1),
    limit: int = Query(4, ge=1)
):
    result = doctors

    # Step 1: Search
    if keyword:
        keyword = keyword.lower()
        result = [
            d for d in result
            if keyword in d["name"].lower() or keyword in d["specialization"].lower()
        ]

    # Step 2: Sort
    if sort_by in ["fee", "name", "experience_years"]:
        result = sorted(result, key=lambda d: d[sort_by], reverse=(order == "desc"))

    # Step 3: Pagination
    total = len(result)
    start = (page - 1) * limit
    paged = result[start:start + limit]

    return {
        "total_found": total,
        "page": page,
        "limit": limit,
        "total_pages": -(-total // limit),
        "doctors": paged
    }


# -----------------Endpoint 19 - Get Doctor by ID------------------
@app.get("/doctors/{doctor_id}")
def get_doctor(doctor_id: int):
    doctor = find_doctor(doctor_id)

    if doctor:
        return {"doctor": doctor}

    return {"error": "Doctor not found"}


# -----------------Endpoint 20 - Appointment Search------------------
@app.get("/appointments/search")
def search_appointments(patient_name: str = Query(...)):
    result = [
        a for a in appointments
        if patient_name.lower() in a["patient"].lower()
    ]

    return {
        "total_found": len(result),
        "appointments": result
    }


# -----------------Endpoint 21 - Appointment Sort------------------
@app.get("/appointments/sort")
def sort_appointments(sort_by: str = Query("final_fee")):
    if sort_by not in ["final_fee", "date"]:
        return {"error": "Invalid sort field"}

    sorted_list = sorted(appointments, key=lambda a: a[sort_by])

    return {
        "appointments": sorted_list
    }


# -----------------Endpoint 22 - Appointment Pagination------------------
@app.get("/appointments/page")
def paginate_appointments(
    page: int = Query(1, ge=1),
    limit: int = Query(3, ge=1)
):
    total = len(appointments)
    start = (page - 1) * limit

    return {
        "page": page,
        "limit": limit,
        "total": total,
        "total_pages": -(-total // limit),
        "appointments": appointments[start:start + limit]
    }

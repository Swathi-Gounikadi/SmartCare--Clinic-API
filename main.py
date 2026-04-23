from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel, Field
from datetime import date
from enum import Enum

app = FastAPI()

# ----------------- ENUM ------------------
class AppointmentType(str, Enum):
    video = "video"
    in_person = "in-person"
    emergency = "emergency"


# ----------------- DATA ------------------
doctors = [
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


# ----------------- HOME ------------------
@app.get('/')
def home():
    return {"message": "Welcome to SmartCare Clinic API"}

# ----------------- HELPERS ------------------
def find_doctor(doctor_id: int):
    return next((d for d in doctors if d["id"] == doctor_id), None)


def find_appointment(appointment_id: int):
    return next((a for a in appointments if a["appointment_id"] == appointment_id), None)


def calculate_fee(base_fee, appointment_type, senior):
    multiplier = {
        "video": 0.8,
        "in-person": 1,
        "emergency": 1.5
    }

    fee = base_fee * multiplier.get(appointment_type, 1)

    if senior:
        fee *= 0.85

    return int(fee)


def has_active_appointments(doctor_id: int):
    return any(
        a["doctor_id"] == doctor_id and a["status"] in ["scheduled", "confirmed"]
        for a in appointments
    )


# ----------------- MODELS ------------------
class NewDoctor(BaseModel):
    name: str = Field(..., min_length=2)
    specialization: str = Field(..., min_length=2)
    fee: int = Field(..., gt=0)
    experience_years: int = Field(..., gt=0)
    is_available: bool = True


class AppointmentRequest(BaseModel):
    patient_name: str = Field(..., min_length=2)
    doctor_id: int = Field(..., gt=0)
    date: date
    reason: str = Field(..., min_length=5)
    appointment_type: AppointmentType = AppointmentType.in_person
    senior_citizen: bool = False


# ----------------- GET DOCTORS ------------------
@app.get("/doctors")
def get_doctors():
    return {
        "total": len(doctors),
        "available": sum(d["is_available"] for d in doctors),
        "doctors": doctors
    }


# ----------------- ADD DOCTOR ------------------
@app.post("/doctors", status_code=201)
def add_doctor(doc: NewDoctor):
    if any(
        d["name"].lower() == doc.name.lower() and
        d["specialization"].lower() == doc.specialization.lower()
        for d in doctors
    ):
        raise HTTPException(400, "Doctor already exists")

    new_id = max([d["id"] for d in doctors], default=0) + 1

    new_doc = {"id": new_id, **doc.dict()}
    doctors.append(new_doc)

    return new_doc


# ----------------- CREATE APPOINTMENT ------------------
@app.post("/appointments")
def create_appointment(req: AppointmentRequest):
    global appt_counter

    doctor = find_doctor(req.doctor_id)

    if not doctor:
        raise HTTPException(404, "Doctor not found")

    if not doctor["is_available"]:
        raise HTTPException(400, "Doctor not available")

    fee = calculate_fee(
        doctor["fee"],
        req.appointment_type,
        req.senior_citizen
    )

    appointment = {
        "appointment_id": appt_counter,
        "patient": req.patient_name,
        "doctor_id": doctor["id"],
        "doctor_name": doctor["name"],
        "date": req.date,
        "type": req.appointment_type,
        "final_fee": fee,
        "status": "scheduled"
    }

    appointments.append(appointment)
    appt_counter += 1

    # ✅ IMPORTANT FIX
    doctor["is_available"] = False

    return appointment


# ----------------- CONFIRM ------------------
@app.post("/appointments/{appointment_id}/confirm")
def confirm(appointment_id: int):
    appt = find_appointment(appointment_id)

    if not appt:
        raise HTTPException(404, "Appointment not found")

    appt["status"] = "confirmed"
    return appt


# ----------------- CANCEL ------------------
@app.post("/appointments/{appointment_id}/cancel")
def cancel(appointment_id: int):
    appt = find_appointment(appointment_id)

    if not appt:
        raise HTTPException(404, "Appointment not found")

    appt["status"] = "cancelled"

    doctor = find_doctor(appt["doctor_id"])

    # ✅ FIX: Only free doctor if no active appointments
    if doctor and not has_active_appointments(doctor["id"]):
        doctor["is_available"] = True

    return appt


# ----------------- COMPLETE ------------------
@app.post("/appointments/{appointment_id}/complete")
def complete(appointment_id: int):
    appt = find_appointment(appointment_id)

    if not appt:
        raise HTTPException(404, "Appointment not found")

    appt["status"] = "completed"
    return appt


# ----------------- FILTER DOCTORS ------------------
@app.get("/doctors/filter")
def filter_doctors(
    specialization: str = Query(None),
    max_fee: int = Query(None),
    min_experience: int = Query(None),
    is_available: bool = Query(None)
):
    result = doctors

    if specialization:
        result = [d for d in result if d["specialization"] == specialization]

    if max_fee:
        result = [d for d in result if d["fee"] <= max_fee]

    if min_experience:
        result = [d for d in result if d["experience_years"] >= min_experience]

    if is_available is not None:
        result = [d for d in result if d["is_available"] == is_available]

    return result


# ----------------- UPDATE DOCTOR ------------------
@app.put("/doctors/{doctor_id}")
def update_doctor(
    doctor_id: int,
    fee: int = Query(None),
    is_available: bool = Query(None)
):
    doctor = find_doctor(doctor_id)

    if not doctor:
        raise HTTPException(404, "Doctor not found")

    if fee is not None:
        doctor["fee"] = fee

    if is_available is not None:
        doctor["is_available"] = is_available

    return doctor


# ----------------- DELETE DOCTOR ------------------
@app.delete("/doctors/{doctor_id}")
def delete_doctor(doctor_id: int):
    doctor = find_doctor(doctor_id)

    if not doctor:
        raise HTTPException(404, "Doctor not found")

    if has_active_appointments(doctor_id):
        raise HTTPException(400, "Doctor has active appointments")

    doctors.remove(doctor)

    return {"message": "Deleted successfully"}
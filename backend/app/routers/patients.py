from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.models import Patient, User, HealthMetric, Alert
from app.schemas import PatientCreate, Patient as PatientSchema
from app.dependencies import get_db
from app.utils.roles import get_current_user
from app.schemas import HealthMetric as HealthMetricSchema

router = APIRouter()

#   Create patient — linked to the doctor
@router.post("/add", response_model=PatientSchema)
def create_patient(
    patient: PatientCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    existing_patient = db.query(Patient).filter(Patient.email == patient.email).first()
    if existing_patient:
        raise HTTPException(status_code=400, detail="Patient already registered")

    #   Fix BMI calculation
    bmi = None
    if patient.height and patient.weight:
        try:
            bmi = round(patient.weight / ((patient.height / 100) ** 2), 2)
        except ZeroDivisionError:
            bmi = None

    #   Allow nullable values for height and weight
    new_patient = Patient(
        name=patient.name,
        age=patient.age,
        condition=patient.condition,
        email=patient.email,
        phone=patient.phone,
        emergency_contact=patient.emergency_contact,
        blood_group=patient.blood_group,
        height=patient.height or None,
        weight=patient.weight or None,
        bmi=bmi,
        address=patient.address or None,
        doctor_id=user.id
    )

    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)
    return new_patient


#   Get patients — only the logged-in doctor’s patients
@router.get("/", response_model=List[PatientSchema])
def get_patients(
    name: Optional[str] = None,
    age: Optional[int] = None,
    blood_group: Optional[str] = None,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    query = db.query(Patient).filter(Patient.doctor_id == user.id)

    if name:
        query = query.filter(Patient.name.ilike(f"%{name}%"))
    if age:
        query = query.filter(Patient.age == age)
    if blood_group:
        query = query.filter(Patient.blood_group.ilike(f"%{blood_group}%"))

    patients = query.all()
    return patients


#   Get specific patient — only if belongs to logged-in doctor
@router.get("/{patient_id}", response_model=PatientSchema)
def get_patient(patient_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    patient = db.query(Patient).filter(Patient.id == patient_id, Patient.doctor_id == user.id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found or not accessible")
    return patient


#   Update patient — only if belongs to logged-in doctor
@router.put("/{patient_id}", response_model=PatientSchema)
def update_patient(patient_id: int, updated_patient: PatientCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    patient = db.query(Patient).filter(Patient.id == patient_id, Patient.doctor_id == user.id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found or not accessible")

    for key, value in updated_patient.dict(exclude_unset=True).items():
        if value is not None:
            setattr(patient, key, value)

    db.commit()
    db.refresh(patient)
    return patient


#   Delete patient — only if belongs to logged-in doctor
@router.delete("/{patient_id}")
def delete_patient(patient_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    patient = db.query(Patient).filter(Patient.id == patient_id, Patient.doctor_id == user.id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found or not accessible")

    db.delete(patient)
    db.commit()
    return {"message": "Patient deleted successfully"}

#   Combined Filtering for Patient and Health Metrics
#   Combined Filtering for Patient and Health Metrics
@router.get("/filter", response_model=List[PatientSchema])
def filter_patients(
    condition: Optional[str] = None,
    age: Optional[int] = None,
    min_age: Optional[int] = None,
    max_age: Optional[int] = None,
    bmi_min: Optional[float] = None,
    bmi_max: Optional[float] = None,
    blood_group: Optional[str] = None,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    query = db.query(Patient).filter(Patient.doctor_id == user.id)

    #   Patient model filters
    if condition:
        query = query.filter(Patient.condition == condition)
    if age:
        query = query.filter(Patient.age == age)
    if min_age:
        query = query.filter(Patient.age >= min_age)
    if max_age:
        query = query.filter(Patient.age <= max_age)
    if bmi_min:
        query = query.filter(Patient.bmi >= bmi_min)
    if bmi_max:
        query = query.filter(Patient.bmi <= bmi_max)
    if blood_group:
        query = query.filter(Patient.blood_group == blood_group)

    patients = query.all()
    return patients

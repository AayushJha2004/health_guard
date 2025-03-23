from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models import Patient
from app.dependencies import get_db

router = APIRouter()

@router.get("/patients/condition-counts")
def get_patient_counts(db: Session = Depends(get_db)):
    total = db.query(Patient).count()
    good = db.query(Patient).filter(Patient.condition == "Good").count()
    normal = db.query(Patient).filter(Patient.condition == "Normal").count()
    abnormal = db.query(Patient).filter(Patient.condition == "Abnormal").count()
    critical = db.query(Patient).filter(Patient.condition == "Critical").count()

    return {
        "Good": good,
        "Normal": normal,
        "Abnormal": abnormal,
        "Critical": critical,
        "Total": total
    }

@router.get("/patients/by-condition")
def get_patients_by_condition(condition: str, db: Session = Depends(get_db)):
    patients = db.query(Patient).filter(Patient.condition == condition).all()
    return patients

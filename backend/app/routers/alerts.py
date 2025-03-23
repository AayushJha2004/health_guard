from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.models import Alert, Patient, User
from app.schemas import AlertCreate, Alert as AlertSchema
from app.dependencies import get_db
from app.utils.roles import get_current_user

router = APIRouter()

#   Create a new alert
@router.post("/", response_model=AlertSchema)
def create_alert(alert: AlertCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    patient = db.query(Patient).filter(Patient.id == alert.patient_id, Patient.doctor_id == user.id).first()
    if not patient:
        raise HTTPException(status_code=403, detail="Cannot create alert for this patient")

    new_alert = Alert(**alert.dict())
    db.add(new_alert)
    db.commit()
    db.refresh(new_alert)
    return new_alert

@router.get("/{alert_id}")
def get_alert(alert_id: int, db: Session = Depends(get_db)):
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")

    patient = db.query(Patient).filter(Patient.id == alert.patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    #   Include patient details
    return {
        "id": alert.id,
        "message": alert.message,
        "status": alert.status,
        "created_at": alert.created_at,
        "patient": {
            "id": patient.id,
            "name": patient.name,
            "age": patient.age,
            "condition": patient.condition,
        }
    }

#   Get all active alerts
@router.get("/", response_model=List[AlertSchema])
def get_active_alerts(db: Session = Depends(get_db)):
    alerts = db.query(Alert).filter(Alert.status == "active").all()
    return alerts

#   Update alert status (e.g., resolve alert)
@router.put("/{alert_id}")
def update_alert_status(alert_id: int, status: str, db: Session = Depends(get_db)):
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")

    alert.status = status
    db.commit()
    db.refresh(alert)
    return alert

#   Notify Emergency Contact
@router.post("/{alert_id}/notify")
def notify_guardian(alert_id: int, db: Session = Depends(get_db)):
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")

    # Simulate sending a notification
    print(f"🔔 Notifying emergency contact for alert {alert_id}...")
    return {"message": "Guardian notified"}


#   Delete an alert
@router.delete("/{alert_id}")
def delete_alert(alert_id: int, db: Session = Depends(get_db)):
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")

    db.delete(alert)
    db.commit()
    return {"message": "Alert deleted successfully"}

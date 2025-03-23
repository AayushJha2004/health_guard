from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.models import HealthMetric, Patient, User
from app.schemas import HealthMetricCreate, HealthMetric as HealthMetricSchema
from app.dependencies import get_db
from app.utils.roles import get_current_user

router = APIRouter()

@router.get("/{patient_id}/metrics", response_model=List[HealthMetricSchema])
def get_patient_metrics(patient_id: int, db: Session = Depends(get_db), user = Depends(get_current_user)):
    patient = db.query(Patient).filter(Patient.id == patient_id, Patient.doctor_id == user.id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    metrics = db.query(HealthMetric).filter(HealthMetric.patient_id == patient_id).all()
    return metrics

#   Create health metric for a patient
@router.post("/", response_model=HealthMetricSchema)
def create_health_metric(metric: HealthMetricCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    patient = db.query(Patient).filter(Patient.id == metric.patient_id, Patient.doctor_id == user.id).first()
    if not patient:
        raise HTTPException(status_code=403, detail="Cannot create health metric for this patient")

    new_metric = HealthMetric(**metric.dict())
    db.add(new_metric)
    db.commit()
    db.refresh(new_metric)
    return new_metric

#   Get health metrics for a specific patient
@router.get("/{patient_id}", response_model=List[HealthMetricSchema])
def get_health_metrics(patient_id: int, db: Session = Depends(get_db)):
    metrics = db.query(HealthMetric).filter(HealthMetric.patient_id == patient_id).all()
    if not metrics:
        raise HTTPException(status_code=404, detail="No health metrics found for this patient")
    return metrics

#   Update health metric
@router.put("/{metric_id}", response_model=HealthMetricSchema)
def update_health_metric(metric_id: int, updated_metric: HealthMetricCreate, db: Session = Depends(get_db)):
    metric = db.query(HealthMetric).filter(HealthMetric.id == metric_id).first()
    if not metric:
        raise HTTPException(status_code=404, detail="Health metric not found")

    for key, value in updated_metric.dict().items():
        setattr(metric, key, value)

    db.commit()
    db.refresh(metric)
    return metric

#   Delete health metric
@router.delete("/{metric_id}")
def delete_health_metric(metric_id: int, db: Session = Depends(get_db)):
    metric = db.query(HealthMetric).filter(HealthMetric.id == metric_id).first()
    if not metric:
        raise HTTPException(status_code=404, detail="Health metric not found")

    db.delete(metric)
    db.commit()
    return {"message": "Health metric deleted successfully"}

#   Get health metrics for a specific patient with filtering
@router.get("/filter/{patient_id}", response_model=List[HealthMetricSchema])
def filter_health_metrics(
    patient_id: int,
    metric_type: str = None,
    db: Session = Depends(get_db)
):
    query = db.query(HealthMetric).filter(HealthMetric.patient_id == patient_id)
    
    if metric_type:
        query = query.filter(HealthMetric.metric_type == metric_type)
    
    metrics = query.all()
    return metrics

#   Endpoint to plot chart data
@router.get("/chart/{patient_id}")
def get_chart_data(patient_id: int, db: Session = Depends(get_db)):
    metrics = db.query(HealthMetric).filter(HealthMetric.patient_id == patient_id).all()

    chart_data = {}
    for metric in metrics:
        if metric.metric_type not in chart_data:
            chart_data[metric.metric_type] = []
        chart_data[metric.metric_type].append({
            "value": metric.value,
            "created_at": metric.created_at
        })

    return chart_data
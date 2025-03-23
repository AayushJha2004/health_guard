from fastapi import Request, APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.models import HealthMetric, Patient
from app.dependencies import get_db
from datetime import datetime
from app.ml_model import predict_condition, generate_alert_message

router = APIRouter()

@router.api_route("/data", methods=["POST"])
async def receive_data(request: Request, db: Session = Depends(get_db)):
    try:
        data = await request.json()
        patient_id = 1  # Example patient ID — modify this logic to fetch patient dynamically

        for entry in data:
            timestamp = entry.get('timestamp') or entry.get('ecgStartDate')
            if not timestamp:
                continue

            created_at = datetime.utcfromtimestamp(timestamp)

            for key, value in entry.items():
                if key in ["timestamp", "ecgStartDate", "patient_id"]:
                    continue

                if key == "heartRate":
                    metric_type = "heart_rate"
                elif key == "respiratoryRate":
                    metric_type = "respiratory_rate"
                elif key == "bodyTemperature":
                    metric_type = "body_temp"
                else:
                    metric_type = key

                metric = HealthMetric(
                    patient_id=patient_id,
                    metric_type=metric_type,
                    value=value,
                    created_at=created_at
                )
                db.add(metric)

        db.commit()
        await update_patient_condition(patient_id, db)

        return JSONResponse(content={"status": "success", "message": "Data saved and condition updated"})

    except Exception as e:
        db.rollback()
        return JSONResponse(content={"status": "error", "message": str(e)}, status_code=400)

async def update_patient_condition(patient_id: int, db: Session):
    try:
        print("🔎 update_patient_condition called", flush=True)

        #   Get latest available data
        latest_heart_rate = db.query(HealthMetric).filter(
            HealthMetric.patient_id == patient_id,
            HealthMetric.metric_type == 'heart_rate'
        ).order_by(HealthMetric.created_at.desc()).first()

        latest_resp_rate = db.query(HealthMetric).filter(
            HealthMetric.patient_id == patient_id,
            HealthMetric.metric_type == 'respiratory_rate'
        ).order_by(HealthMetric.created_at.desc()).first()

        latest_body_temp = db.query(HealthMetric).filter(
            HealthMetric.patient_id == patient_id,
            HealthMetric.metric_type == 'body_temp'
        ).order_by(HealthMetric.created_at.desc()).first()

        if latest_heart_rate and latest_resp_rate and latest_body_temp:
            patient = db.query(Patient).filter(Patient.id == patient_id).first()
            if not patient:
                raise Exception("Patient not found")

            age = patient.age
            bmi = patient.bmi or 0
            heart_rate = latest_heart_rate.value
            respiratory_rate = latest_resp_rate.value
            body_temp = latest_body_temp.value

            #   Call the model for prediction
            condition = predict_condition(age, bmi, heart_rate, respiratory_rate, body_temp, patient_id, db)
            print(f"  Predicted condition: {condition}")

            #   Store prediction in the database
            patient.condition = str(condition)  # Store as string for readability
            db.commit()

            #   Generate Alert + Email Notification
            generate_alert_message(patient_id, condition, db)

        else:
            print("❌ Missing one or more required health metrics", flush=True)

    except Exception as e:
        print(f"🚨 Failed to update patient condition: {e}", flush=True)
        db.rollback()

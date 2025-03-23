from fastapi import Request, APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.models import HealthMetric
from app.dependencies import get_db
from datetime import datetime

router = APIRouter()

@router.api_route("/static", methods=["POST"])
async def receive_data(request: Request, db: Session = Depends(get_db)):
    try:
        data = await request.json()
        print(f"🔍 Incoming data: {data}", flush=True)
        patient_id = 1  # Example patient ID — adjust dynamically if needed

        #   Identify data type (ECG or Sleep)
        if "voltageMeasurements" in data[0]:
            data_type = "ecg"
        elif "inBed" in data[0] or "rem" in data[0]:
            data_type = "sleep"
        else:
            return JSONResponse(content={"status": "error", "message": "Unknown data type"}, status_code=400)

        if data_type == "ecg":
            await handle_ecg_data(data, patient_id, db)
        elif data_type == "sleep":
            await handle_sleep_data(data, patient_id, db)

        return JSONResponse(content={"status": "success", "message": f"{data_type.capitalize()} data saved successfully"})

    except Exception as e:
        db.rollback()
        print(f"🚨 Error: {e}", flush=True)
        return JSONResponse(content={"status": "error", "message": str(e)}, status_code=400)

#   Handle ECG Data (Including voltageMeasurements)
async def handle_ecg_data(data, patient_id, db):
    for entry in data:
        timestamp = entry.get('timestamp') or entry.get('ecgStartDate')
        if not timestamp:
            continue

        created_at = datetime.utcfromtimestamp(timestamp)

        #   Handle ECG-specific data (non-voltage related)
        for key, value in entry.items():
            if key in ["timestamp", "ecgStartDate", "patient_id", "voltageMeasurements"]:
                continue

            if key == "ecgSignal":
                metric_type = "ecg_signal"
            elif key == "ecgHeartRate":
                metric_type = "ecg_heart_rate"
            else:
                metric_type = key

            metric = HealthMetric(
                patient_id=patient_id,
                metric_type=metric_type,
                value=value,
                created_at=created_at
            )
            db.add(metric)
            print(f"  Stored {metric_type}: {value} at {created_at}", flush=True)

        #   Handle Voltage Measurements (Flattened)
        if "voltageMeasurements" in entry:
            for measurement in entry["voltageMeasurements"]:
                time_since_start = measurement.get("timeSinceSampleStart")
                voltage = measurement.get("voltage")

                #   Store voltage data in HealthMetric
                if time_since_start is not None and voltage is not None:
                    metric = HealthMetric(
                        patient_id=patient_id,
                        metric_type="voltage",
                        value=voltage,
                        created_at=created_at
                    )
                    db.add(metric)
                    print(f"  Stored voltage at time {time_since_start}: {voltage}", flush=True)

    #   Commit data to database
    db.commit()
    print("  ECG data committed successfully", flush=True)

#   Handle Sleep Data
async def handle_sleep_data(data, patient_id, db):
    for entry in data:
        timestamp = entry.get('timestamp') or entry.get('sleepStartDate')
        if not timestamp:
            continue

        created_at = datetime.utcfromtimestamp(timestamp)

        for key, value in entry.items():
            if key in ["timestamp", "sleepStartDate", "patient_id"]:
                continue

            #   Handle sleep-specific data
            if key == "inBed":
                metric_type = "in_bed"
            elif key == "awake":
                metric_type = "awake"
            elif key == "rem":
                metric_type = "rem"
            elif key == "deep":
                metric_type = "deep"
            elif key == "core":
                metric_type = "core"
            elif key == "unspecified":
                metric_type = "unspecified"
            else:
                metric_type = key

            metric = HealthMetric(
                patient_id=patient_id,
                metric_type=metric_type,
                value=value,
                created_at=created_at
            )
            db.add(metric)
            print(f"  Stored {metric_type}: {value} at {created_at}", flush=True)

    db.commit()
    print("  Sleep data committed successfully", flush=True)

#   Fetch ECG data for a specific patient
@router.get("/static/ecg/{patient_id}")
def get_ecg_data(patient_id: int, db: Session = Depends(get_db)):
    ecg_data = db.query(HealthMetric).filter(
        HealthMetric.patient_id == patient_id,
        HealthMetric.metric_type == "voltage"
    ).order_by(HealthMetric.created_at).all()

    if not ecg_data:
        raise HTTPException(status_code=404, detail="No ECG data found for this patient")

    #   Convert to JSON format
    return [
        {
            "time": index,
            "voltage": entry.value,
            "created_at": entry.created_at
        }
        for index, entry in enumerate(ecg_data)
    ]
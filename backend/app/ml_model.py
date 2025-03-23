import joblib 
import numpy as np
import logging
import os
import sys
import warnings
from app.models import Alert, Patient
from app.email_alerts import send_health_alert
from sqlalchemy.orm import Session

#   Set up UTF-8 encoding for logging
os.environ['PYTHONIOENCODING'] = 'utf-8'

#   Suppress sklearn warnings about feature names
warnings.filterwarnings("ignore", message="X does not have valid feature names")

#   Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("prediction.log", encoding="utf-8")
    ]
)
logger = logging.getLogger(__name__)

try:
    #   Load the trained model
    logger.info("🔄 Loading model...")
    model = joblib.load("app/models/random_forest_model.pkl")
    logger.info("  Model loaded successfully")
except Exception as e:
    logger.error(f"🚨 Error loading model: {e}")
    model = None

def generate_alert_message(patient_id, prediction, db: Session):
    heart_rate_status = prediction[0]  # 0 = normal, 1 = abnormal, 2 = emergency
    respiratory_status = prediction[1]
    body_temp_status = prediction[2]

    messages = []
    alert_type = "normal"

    if heart_rate_status == 1:
        messages.append("Abnormal heart rate")
        alert_type = "abnormal"
    elif heart_rate_status == 2:
        messages.append("Emergency! Heart rate is critical")
        alert_type = "emergency"

    if respiratory_status == 1:
        messages.append("Abnormal respiratory rate")
        alert_type = "abnormal"
    elif respiratory_status == 2:
        messages.append("Emergency! Respiratory rate is critical")
        alert_type = "emergency"

    if body_temp_status == 1:
        messages.append("Abnormal body temperature")
        alert_type = "abnormal"
    elif body_temp_status == 2:
        messages.append("Emergency! Body temperature is critical")
        alert_type = "emergency"

    #   Create a combined alert message
    if messages:
        combined_message = "; ".join(messages)

        alert = Alert(
            patient_id=patient_id,
            message=combined_message,
            status="active"
        )
        db.add(alert)
        db.commit()
        db.refresh(alert)

        #   Get patient details for email
        patient = db.query(Patient).filter(Patient.id == patient_id).first()

        if alert_type != "normal":
            #   Send email notification
            health_issue = combined_message
            send_health_alert(
                alert_type,
                patient.name,
                health_issue,
                patient.email,
                "natsuam.rawal07@gmail.com"  # Practitioner email
            )

        print(f"  Alert created and email sent for {patient.name} - {combined_message}")


def predict_condition(age, bmi, heart_rate, respiratory_rate, body_temp, patient_id, db: Session):
    try:
        logger.info("🔎 predict_condition() called")

        #   Validate inputs
        if not all(isinstance(i, (int, float)) for i in [age, bmi, heart_rate, respiratory_rate, body_temp]):
            logger.error("❌ Invalid input types")
            return "Invalid input"

        if model is None:
            logger.error("❌ Model not loaded")
            return "Model not loaded"

        #   Prepare input data
        input_data = np.array([[age, bmi, heart_rate, respiratory_rate, body_temp]])
        logger.debug(f"📊 Input data: {input_data}")

        #   Predict condition
        prediction = model.predict(input_data)[0]
        logger.info(f"  Prediction: {prediction}")

        #   Generate and store alerts based on prediction
        generate_alert_message(patient_id, prediction, db)

        return prediction

    except Exception as e:
        logger.error(f"🚨 Prediction error: {e}")
        return "Unknown"

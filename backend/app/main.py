from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import dashboard, patients, alerts, auth, health_metrics, appleWatch, ecgSleep
import os
import sys

app = FastAPI()

#   Set up UTF-8 encoding for logging and output
os.environ['PYTHONIOENCODING'] = 'utf-8'
sys.stdout.reconfigure(encoding='utf-8')

#   Add CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    # allow_origins=["http://localhost:5174"],  # 👈 Allow frontend origin
    allow_credentials=True,
    allow_methods=["*"],  # 👈 Allow all methods (POST, GET, PUT, DELETE)
    allow_headers=["*"],  # 👈 Allow all headers
)

#   Include Routers (with prefixes and tags)
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
app.include_router(patients.router, prefix="/patients", tags=["patients"])
app.include_router(alerts.router, prefix="/alerts", tags=["alerts"])
app.include_router(health_metrics.router, prefix="/health-metrics", tags=["health-metrics"])
app.include_router(appleWatch.router, prefix="/api", tags=["apple-watch"])
app.include_router(ecgSleep.router, prefix="/api", tags=["ECG and Sleep"])

@app.get("/")
def root():
    return {"message": "Healthcare API is running"}

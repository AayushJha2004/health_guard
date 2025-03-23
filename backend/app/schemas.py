from pydantic import BaseModel, EmailStr, Field
import datetime
from typing import Optional

#   Patient Schema
class PatientBase(BaseModel):
    name: str
    age: int
    condition: str
    email: EmailStr
    phone: str
    emergency_contact: str
    blood_group: str
    height: Optional[float] = Field(None, description="Patient's height in cm")
    weight: Optional[float] = Field(None, description="Patient's weight in kg")
    address: Optional[str] = None

class PatientCreate(PatientBase):
    pass

class Patient(PatientBase):
    id: int
    bmi: Optional[float] = None
    created_at: datetime.datetime

    class Config:
        from_attributes = True

#   User Schemas
class UserBase(BaseModel):
    email: str
    full_name: str

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int

    class Config:
        from_attributes = True

#   HealthMetric Schemas
class HealthMetricBase(BaseModel):
    patient_id: int
    heart_rate: float
    blood_pressure: str
    oxygen_level: float

class HealthMetricCreate(HealthMetricBase):
    pass

class HealthMetric(HealthMetricBase):
    id: int
    created_at: datetime.datetime

    class Config:
        from_attributes = True

#   Alert Schemas
class AlertBase(BaseModel):
    patient_id: int
    message: str
    status: str  # e.g., "active", "resolved"

class AlertCreate(AlertBase):
    pass

class AlertUpdate(BaseModel):
    status: str

class Alert(AlertBase):
    id: int
    created_at: datetime.datetime

    class Config:
        from_attributes = True

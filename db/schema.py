from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from enum import Enum


class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"

class PatientBase(BaseModel):
    name: str
    date_of_birth: datetime

class PatientCreate(PatientBase):
    gender: Gender

class XrayResponse(BaseModel):
    id: int
    x_ray_image: str
    result: Optional[str]
    confidence: Optional[float]
    created_at: datetime
    
    class Config:
        from_attributes = True  # For SQLAlchemy

class PatientResponse(PatientBase):
    id: int
    created_at: datetime
    gender: Gender
    age: int
    xrays: List[XrayResponse] = []
    
    class Config:
        from_attributes = True

class XrayAnalysisResult(BaseModel):
    result: str
    confidence: float


from .db import Base 
from sqlalchemy import Column, Integer, String, DateTime, Text, Float, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime





class BaseModel(Base):
    __abstract__ = True
    id = Column(Integer, primary_key= True, index= True)
    created_at = Column (DateTime, default=datetime.now)
    updated_at = Column (DateTime, default=datetime.now, onupdate=datetime.now)

class Patient(BaseModel):


    MALE = "male"
    FEMALE = "female"
    OTHER = "other"


    __tablename__ = "patient"
    name = Column(String(255), nullable=False)
    date_of_birth = Column (DateTime, nullable=False)
    gender = Column(String(10), nullable=False)


    @property
    def age(self):
        return datetime.now().year - self.date_of_birth.year


class Xray(BaseModel):
    __tablename__ = "xray"

    patient_id = Column(Integer, ForeignKey("patient.id"), nullable=False)
    x_ray_image = Column(String(255), nullable=False)
    result = Column(String(255), nullable=False)
    confidence = Column(Float, nullable=False)

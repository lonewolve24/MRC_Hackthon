from sqlalchemy.orm import Session
from db.models import Patient, Xray
from db.schema import PatientCreate
from fastapi import HTTPException, UploadFile
from pathlib import Path
from typing import List
import os

class PatientService:
    
    def __init__(self):
        self.upload_dir = Path("uploads")
        self.upload_dir.mkdir(exist_ok=True)
    
    def create_patient(self, patient: PatientCreate, db: Session):
        """Create new patient in database"""
        db_patient = Patient(
            name=patient.name,
            date_of_birth=patient.date_of_birth,
            gender=patient.gender
        )
        db.add(db_patient)
        db.commit()
        db.refresh(db_patient)
        return db_patient
    
    def get_patient(self, patient_id: int, db: Session):
        """Get patient by ID"""
        patient = db.query(Patient).filter(Patient.id == patient_id).first()
        if not patient:
            raise HTTPException(status_code=404, detail="Patient not found")
        return patient
    
    def list_patients(self, db: Session):
        """Get all patients"""
        return db.query(Patient).all()
    
    def get_patient_xrays(self, patient_id: int, db: Session):
        """Get all X-rays for a patient"""
        xrays = db.query(Xray).filter(Xray.patient_id == patient_id).all()
        if not xrays:
            raise HTTPException(status_code=404, detail="No X-rays found")
        return xrays
    
    async def upload_xrays(self, patient_id: int, files: List[UploadFile], db: Session):
        """Handle X-ray upload and analysis"""
        # Check patient exists
        patient = self.get_patient(patient_id, db)
        
        uploaded_results = []
        
        for file in files:
            # Save file
            file_path = self.upload_dir / f"{patient_id}_{file.filename}"
            
            with open(file_path, "wb") as f:
                content = await file.read()
                f.write(content)
            
            # Analyze with AI model
            analysis = await self.analyze_xray_image(str(file_path))
            
            # Save to DB
            db_xray = Xray(
                patient_id=patient_id,
                x_ray_image=str(file_path),
                result=analysis["result"],
                confidence=analysis["confidence"]
            )
            db.add(db_xray)
            db.commit()
            db.refresh(db_xray)
            
            uploaded_results.append({
                "id": db_xray.id,
                "filename": file.filename,
                "result": db_xray.result,
                "confidence": db_xray.confidence
            })
        
        return {
            "patient_id": patient_id,
            "uploaded_count": len(uploaded_results),
            "results": uploaded_results
        }
    
    async def analyze_xray_image(self, image_path: str) -> dict:
        """
        Call your AI model here
        Replace with your actual model inference
        """
        # Placeholder - integrate your ML model here
        return {
            "result": "No abnormalities detected",
            "confidence": 0.95
        }
import boto3
from sqlalchemy.orm import Session
from botocore.exceptions import ClientError
from db.models import Patient, Xray
from db.schema import PatientCreate
from fastapi import HTTPException, UploadFile
from pathlib import Path
from typing import List
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()


class PatientService:

    ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png'}
    
    def __init__(self):
        self.upload_dir = Path("uploads")
        self.upload_dir.mkdir(exist_ok=True)

        
        self.s3_client = boto3.client(
            's3',
            endpoint_url=os.getenv('AWS_S3_ENDPOINT'),
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=os.getenv('AWS_REGION', 'eu-west-1')
        )
        self.bucket_name = os.getenv('S3_BUCKET_NAME')
        
        # Check if in debug mode
        self.debug_mode = os.getenv("DEBUG") == 'True'

    def _validate_file(self, filename: str) -> bool:
        """Validate file extension"""
        file_ext = Path(filename).suffix.lower()
        if file_ext not in self.ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file type. Only JPG/JPEG and PNG allowed."
            )
        return True
    
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
        patient = self.get_patient(patient_id, db)
        
        uploaded_results = []
        
        for file in files:
            # Validate file type
            self._validate_file(file.filename)
            
            # Read file content
            content = await file.read()
            
            # Choose storage based on DEBUG mode
            if self.debug_mode and self.s3_client and self.bucket_name:
                # Upload to AWS S3 (Cloud - for production)
                s3_key = f"xrays/{patient_id}/{file.filename}"
                
                try:
                    self.s3_client.put_object(
                        Bucket=self.bucket_name,
                        Key=s3_key,
                        Body=content,
                        ContentType=file.content_type
                    )
                    
                    # Generate public URL
                    file_url = f"https://{self.bucket_name}.s3.amazonaws.com/{s3_key}"
                    image_path = file_url
                    
                except ClientError as e:
                    raise HTTPException(
                        status_code=500,
                        detail=f"S3 upload failed: {str(e)}"
                    )
            else:
                # Save locally (Development only)
                file_path = self.upload_dir / f"{patient_id}_{file.filename}"
                with open(file_path, "wb") as f:
                    f.write(content)
                image_path = str(file_path)
            
            # Analyze with AI model
            analysis = await self.analyze_xray_image(image_path)
            
            # Save to DB
            db_xray = Xray(
                patient_id=patient_id,
                x_ray_image=image_path,
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

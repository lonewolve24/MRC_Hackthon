from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from typing import List
from db.db import get_db
from db.schema import PatientCreate, PatientResponse, XrayResponse
from db.models import Patient, Xray
from services.patient_service import PatientService

router = APIRouter(prefix="/api", tags=["patients"])

# Initialize service
patient_service = PatientService()

# ============ PATIENT ENDPOINTS ============

@router.post("/patients", response_model=PatientResponse)
async def create_patient(patient: PatientCreate, db: Session = Depends(get_db)):
    """Create a new patient"""
    return patient_service.create_patient(patient, db)

@router.get("/patients/{patient_id}", response_model=PatientResponse)
async def get_patient(patient_id: int, db: Session = Depends(get_db)):
    """Get patient with all their X-ray results"""
    return patient_service.get_patient(patient_id, db)

@router.get("/patients", response_model=List[PatientResponse])
async def list_patients(db: Session = Depends(get_db)):
    """List all patients"""
    return patient_service.list_patients(db)

# ============ X-RAY ENDPOINTS ============

@router.post("/patients/{patient_id}/xrays")
async def upload_xrays(
    patient_id: int,
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db)
):
    """Upload X-ray images"""
    return await patient_service.upload_xrays(patient_id, files, db)

@router.get("/patients/{patient_id}/xrays", response_model=List[XrayResponse])
async def get_patient_xrays(patient_id: int, db: Session = Depends(get_db)):
    """Get all X-rays for a patient"""
    return patient_service.get_patient_xrays(patient_id, db)
"""
API routers for cabinet management
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import Cabinet, Material, CabinetComponent
from pydantic import BaseModel

router = APIRouter(prefix="/api/cabinets", tags=["cabinets"])


# Pydantic models for request/response
class CabinetCreate(BaseModel):
    name: str
    description: str = None
    width: float
    height: float
    depth: float
    material_id: int = None


class CabinetResponse(BaseModel):
    id: int
    name: str
    description: str = None
    width: float
    height: float
    depth: float
    material_id: int = None
    is_active: bool
    
    class Config:
        from_attributes = True


@router.post("/", response_model=CabinetResponse)
def create_cabinet(cabinet: CabinetCreate, db: Session = Depends(get_db)):
    """
    Create a new cabinet
    """
    db_cabinet = Cabinet(**cabinet.dict())
    db.add(db_cabinet)
    db.commit()
    db.refresh(db_cabinet)
    return db_cabinet


@router.get("/", response_model=List[CabinetResponse])
def list_cabinets(db: Session = Depends(get_db)):
    """
    List all cabinets
    """
    cabinets = db.query(Cabinet).filter(Cabinet.is_active == True).all()
    return cabinets


@router.get("/{cabinet_id}", response_model=CabinetResponse)
def get_cabinet(cabinet_id: int, db: Session = Depends(get_db)):
    """
    Get a specific cabinet by ID
    """
    cabinet = db.query(Cabinet).filter(Cabinet.id == cabinet_id).first()
    if not cabinet:
        raise HTTPException(status_code=404, detail="Cabinet not found")
    return cabinet


@router.put("/{cabinet_id}", response_model=CabinetResponse)
def update_cabinet(cabinet_id: int, cabinet: CabinetCreate, db: Session = Depends(get_db)):
    """
    Update a cabinet
    """
    db_cabinet = db.query(Cabinet).filter(Cabinet.id == cabinet_id).first()
    if not db_cabinet:
        raise HTTPException(status_code=404, detail="Cabinet not found")
    
    for key, value in cabinet.dict().items():
        setattr(db_cabinet, key, value)
    
    db.commit()
    db.refresh(db_cabinet)
    return db_cabinet


@router.delete("/{cabinet_id}")
def delete_cabinet(cabinet_id: int, db: Session = Depends(get_db)):
    """
    Delete a cabinet (soft delete)
    """
    db_cabinet = db.query(Cabinet).filter(Cabinet.id == cabinet_id).first()
    if not db_cabinet:
        raise HTTPException(status_code=404, detail="Cabinet not found")
    
    db_cabinet.is_active = False
    db.commit()
    return {"message": "Cabinet deleted"}
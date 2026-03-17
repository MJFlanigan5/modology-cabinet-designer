"""
API routers for material management
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import Material
from pydantic import BaseModel

router = APIRouter(prefix="/api/materials", tags=["materials"])


# Pydantic models for request/response
class MaterialCreate(BaseModel):
    name: str
    type: str  # plywood, mdf, hardwood, particleboard
    thickness: float
    sheet_width: float = 48.0
    sheet_height: float = 96.0
    price_per_sqft: float
    supplier: str = None
    description: str = None


class MaterialResponse(BaseModel):
    id: int
    name: str
    type: str
    thickness: float
    sheet_width: float
    sheet_height: float
    price_per_sqft: float
    supplier: str = None
    description: str = None
    is_active: bool
    
    class Config:
        from_attributes = True


@router.post("/", response_model=MaterialResponse)
def create_material(material: MaterialCreate, db: Session = Depends(get_db)):
    """
    Create a new material
    """
    db_material = Material(**material.dict())
    db.add(db_material)
    db.commit()
    db.refresh(db_material)
    return db_material


@router.get("/", response_model=List[MaterialResponse])
def list_materials(db: Session = Depends(get_db)):
    """
    List all materials
    """
    materials = db.query(Material).filter(Material.is_active == True).all()
    return materials


@router.get("/{material_id}", response_model=MaterialResponse)
def get_material(material_id: int, db: Session = Depends(get_db)):
    """
    Get a specific material by ID
    """
    material = db.query(Material).filter(Material.id == material_id).first()
    if not material:
        raise HTTPException(status_code=404, detail="Material not found")
    return material


@router.put("/{material_id}", response_model=MaterialResponse)
def update_material(material_id: int, material: MaterialCreate, db: Session = Depends(get_db)):
    """
    Update a material
    """
    db_material = db.query(Material).filter(Material.id == material_id).first()
    if not db_material:
        raise HTTPException(status_code=404, detail="Material not found")
    
    for key, value in material.dict().items():
        setattr(db_material, key, value)
    
    db.commit()
    db.refresh(db_material)
    return db_material


@router.delete("/{material_id}")
def delete_material(material_id: int, db: Session = Depends(get_db)):
    """
    Delete a material (soft delete)
    """
    db_material = db.query(Material).filter(Material.id == material_id).first()
    if not db_material:
        raise HTTPException(status_code=404, detail="Material not found")
    
    db_material.is_active = False
    db.commit()
    return {"message": "Material deleted"}
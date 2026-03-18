# FastAPI Backend for KerfOS Cabinet Designer

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
from datetime import datetime
import json

app = FastAPI(
    title="KerfOS API",
    description="Backend API for KerfOS Cabinet Designer",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class Cabinet(BaseModel):
    id: Optional[int] = None
    name: str
    width: float
    height: float
    depth: float
    material: str
    created_at: Optional[datetime] = None

class Project(BaseModel):
    id: Optional[int] = None
    name: str
    description: Optional[str] = None
    cabinets: List[Cabinet] = []
    created_at: Optional[datetime] = None

class Material(BaseModel):
    id: Optional[int] = None
    name: str
    type: str  # plywood, mdf, hardwood
    thickness: float
    price_per_sheet: float
    sheet_width: float = 48.0  # inches
    sheet_height: float = 96.0  # inches

# In-memory storage (replace with database in production)
cabinets_db = []
projects_db = []
materials_db = []

# Initialize with sample data
def init_sample_data():
    # Sample materials
    materials_db.extend([
        Material(
            id=1,
            name="Birch Plywood",
            type="plywood",
            thickness=0.75,
            price_per_sheet=65.99
        ),
        Material(
            id=2,
            name="MDF",
            type="mdf",
            thickness=0.75,
            price_per_sheet=42.50
        ),
        Material(
            id=3,
            name="Oak Hardwood",
            type="hardwood",
            thickness=0.75,
            price_per_sheet=89.99
        )
    ])
    
    # Sample cabinets
    cabinets_db.extend([
        Cabinet(
            id=1,
            name="Base Cabinet",
            width=36.0,
            height=34.5,
            depth=24.0,
            material="Birch Plywood",
            created_at=datetime.now()
        ),
        Cabinet(
            id=2,
            name="Wall Cabinet",
            width=30.0,
            height=30.0,
            depth=12.0,
            material="Birch Plywood",
            created_at=datetime.now()
        )
    ])
    
    # Sample project
    projects_db.append(
        Project(
            id=1,
            name="Kitchen Remodel",
            description="Complete kitchen cabinet set",
            cabinets=cabinets_db.copy(),
            created_at=datetime.now()
        )
    )

# Initialize sample data on startup
init_sample_data()

# Health check
@app.get("/")
async def root():
    return {
        "message": "KerfOS API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health")
async def health():
    return {"status": "healthy", "timestamp": datetime.now()}

@app.get("/init-db")
async def init_db():
    """Initialize database with sample data"""
    init_sample_data()
    return {"message": "Database initialized with sample data"}

# Cabinet endpoints
@app.get("/api/cabinets", response_model=List[Cabinet])
async def get_cabinets():
    return cabinets_db

@app.get("/api/cabinets/{cabinet_id}", response_model=Cabinet)
async def get_cabinet(cabinet_id: int):
    for cabinet in cabinets_db:
        if cabinet.id == cabinet_id:
            return cabinet
    raise HTTPException(status_code=404, detail="Cabinet not found")

@app.post("/api/cabinets", response_model=Cabinet)
async def create_cabinet(cabinet: Cabinet):
    cabinet.id = len(cabinets_db) + 1
    cabinet.created_at = datetime.now()
    cabinets_db.append(cabinet)
    return cabinet

@app.put("/api/cabinets/{cabinet_id}", response_model=Cabinet)
async def update_cabinet(cabinet_id: int, cabinet_update: Cabinet):
    for i, cabinet in enumerate(cabinets_db):
        if cabinet.id == cabinet_id:
            cabinet_update.id = cabinet_id
            cabinet_update.created_at = cabinet.created_at
            cabinets_db[i] = cabinet_update
            return cabinet_update
    raise HTTPException(status_code=404, detail="Cabinet not found")

@app.delete("/api/cabinets/{cabinet_id}")
async def delete_cabinet(cabinet_id: int):
    for i, cabinet in enumerate(cabinets_db):
        if cabinet.id == cabinet_id:
            cabinets_db.pop(i)
            return {"message": "Cabinet deleted"}
    raise HTTPException(status_code=404, detail="Cabinet not found")

# Project endpoints
@app.get("/api/projects", response_model=List[Project])
async def get_projects():
    return projects_db

@app.get("/api/projects/{project_id}", response_model=Project)
async def get_project(project_id: int):
    for project in projects_db:
        if project.id == project_id:
            return project
    raise HTTPException(status_code=404, detail="Project not found")

@app.post("/api/projects", response_model=Project)
async def create_project(project: Project):
    project.id = len(projects_db) + 1
    project.created_at = datetime.now()
    projects_db.append(project)
    return project

# Material endpoints
@app.get("/api/materials", response_model=List[Material])
async def get_materials():
    return materials_db

@app.get("/api/materials/{material_id}", response_model=Material)
async def get_material(material_id: int):
    for material in materials_db:
        if material.id == material_id:
            return material
    raise HTTPException(status_code=404, detail="Material not found")

# Cut list calculation
@app.post("/api/cutlists/generate")
async def generate_cut_list(cabinet: Cabinet):
    """Generate a simple cut list for a cabinet"""
    # Basic cut list calculation
    # In a real implementation, this would use the 2D bin packing algorithm
    cuts = []
    
    # Calculate parts based on cabinet dimensions
    # Bottom/top: width x depth
    cuts.append({
        "part": "Bottom/Top",
        "quantity": 2,
        "width": cabinet.width,
        "height": cabinet.depth,
        "material": cabinet.material
    })
    
    # Sides: height x depth
    cuts.append({
        "part": "Sides",
        "quantity": 2,
        "width": cabinet.height,
        "height": cabinet.depth,
        "material": cabinet.material
    })
    
    # Back: width x height
    cuts.append({
        "part": "Back",
        "quantity": 1,
        "width": cabinet.width,
        "height": cabinet.height,
        "material": cabinet.material
    })
    
    return {
        "cabinet": cabinet,
        "cuts": cuts,
        "total_parts": len(cuts),
        "generated_at": datetime.now()
    }

# Price calculation
@app.post("/api/calculate-price")
async def calculate_price(cabinet: Cabinet):
    """Calculate material cost for a cabinet"""
    # Find material price
    material_price = None
    for material in materials_db:
        if material.name == cabinet.material:
            material_price = material.price_per_sheet
            break
    
    if not material_price:
        raise HTTPException(status_code=404, detail="Material not found")
    
    # Simple cost calculation (in real app, use actual cut list optimization)
    # Estimate sheet usage based on cabinet volume
    cabinet_volume = cabinet.width * cabinet.height * cabinet.depth
    sheet_area = 48.0 * 96.0  # Standard sheet size in square inches
    estimated_sheets = cabinet_volume / (sheet_area * 0.75)  # Rough estimate
    
    material_cost = estimated_sheets * material_price
    hardware_cost = 25.00  # Estimated hardware cost
    
    return {
        "cabinet": cabinet,
        "material_cost": round(material_cost, 2),
        "hardware_cost": hardware_cost,
        "total_cost": round(material_cost + hardware_cost, 2),
        "estimated_sheets": round(estimated_sheets, 2)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
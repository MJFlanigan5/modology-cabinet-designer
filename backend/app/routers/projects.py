"""
Projects router for project management with collaboration support
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.database import get_db
from app.models import Project, Sheet, Part, User, OptimizationResult
from app.routers.auth import get_current_user, get_current_user_optional
from pydantic import BaseModel

router = APIRouter(prefix="/api/projects", tags=["projects"])

# Pydantic schemas
class SheetBase(BaseModel):
    name: str
    material: Optional[str] = None
    width: float
    length: float
    thickness: float = 0.75
    quantity: int = 1
    cost: float = 0.0

class SheetCreate(SheetBase):
    pass

class SheetResponse(SheetBase):
    id: int
    project_id: int
    class Config:
        from_attributes = True

class PartBase(BaseModel):
    name: str
    width: float
    length: float
    quantity: int = 1
    grain_direction: str = "none"
    edge_banding: Optional[str] = None
    notes: Optional[str] = None

class PartCreate(PartBase):
    pass

class PartResponse(PartBase):
    id: int
    project_id: int
    class Config:
        from_attributes = True

class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    is_public: bool = False

class ProjectCreate(ProjectBase):
    sheets: List[SheetCreate] = []
    parts: List[PartCreate] = []

class ProjectResponse(ProjectBase):
    id: int
    owner_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    sheets: List[SheetResponse] = []
    parts: List[PartResponse] = []
    
    class Config:
        from_attributes = True


@router.get("", response_model=List[ProjectResponse])
async def list_projects(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_optional)
):
    """List all projects - owned and shared"""
    if current_user:
        # Get owned projects
        owned = db.query(Project).filter(Project.owner_id == current_user.id).all()
        # Get shared projects
        shared = [share.project for share in current_user.shared_projects]
        return owned + shared
    else:
        # Return public projects only
        return db.query(Project).filter(Project.is_public == True).all()


@router.post("", response_model=ProjectResponse)
async def create_project(
    project: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new project"""
    db_project = Project(
        name=project.name,
        description=project.description,
        is_public=project.is_public,
        owner_id=current_user.id
    )
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    
    # Add sheets
    for sheet in project.sheets:
        db_sheet = Sheet(**sheet.dict(), project_id=db_project.id)
        db.add(db_sheet)
    
    # Add parts
    for part in project.parts:
        db_part = Part(**part.dict(), project_id=db_project.id)
        db.add(db_part)
    
    db.commit()
    db.refresh(db_project)
    return db_project


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_optional)
):
    """Get a specific project"""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Check access
    if project.owner_id != current_user.id if current_user else None:
        if not project.is_public:
            if current_user:
                share = [s for s in project.shares if s.user_id == current_user.id]
                if not share:
                    raise HTTPException(status_code=403, detail="Access denied")
            else:
                raise HTTPException(status_code=401, detail="Authentication required")
    
    return project


@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: int,
    project_update: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a project"""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Check edit permission
    if project.owner_id != current_user.id:
        share = [s for s in project.shares if s.user_id == current_user.id and s.permission in ["edit", "admin"]]
        if not share:
            raise HTTPException(status_code=403, detail="Edit access denied")
    
    project.name = project_update.name
    project.description = project_update.description
    project.is_public = project_update.is_public
    
    db.commit()
    db.refresh(project)
    return project


@router.delete("/{project_id}")
async def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a project"""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    if project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only owner can delete")
    
    db.delete(project)
    db.commit()
    return {"message": "Project deleted"}


@router.post("/{project_id}/sheets", response_model=SheetResponse)
async def add_sheet(
    project_id: int,
    sheet: SheetCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Add a sheet to a project"""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Check edit permission
    if project.owner_id != current_user.id:
        share = [s for s in project.shares if s.user_id == current_user.id and s.permission in ["edit", "admin"]]
        if not share:
            raise HTTPException(status_code=403, detail="Edit access denied")
    
    db_sheet = Sheet(**sheet.dict(), project_id=project_id)
    db.add(db_sheet)
    db.commit()
    db.refresh(db_sheet)
    return db_sheet


@router.post("/{project_id}/parts", response_model=PartResponse)
async def add_part(
    project_id: int,
    part: PartCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Add a part to a project"""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Check edit permission
    if project.owner_id != current_user.id:
        share = [s for s in project.shares if s.user_id == current_user.id and s.permission in ["edit", "admin"]]
        if not share:
            raise HTTPException(status_code=403, detail="Edit access denied")
    
    db_part = Part(**part.dict(), project_id=project_id)
    db.add(db_part)
    db.commit()
    db.refresh(db_part)
    return db_part


@router.post("/{project_id}/optimize")
async def run_optimization(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Run cutlist optimization for a project"""
    from app.cutlist_optimizer import optimize_cutlist
    
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Check access
    if project.owner_id != current_user.id:
        share = [s for s in project.shares if s.user_id == current_user.id]
        if not share:
            raise HTTPException(status_code=403, detail="Access denied")
    
    # Run optimization
    sheets = [{"width": s.width, "length": s.length, "name": s.name} for s in project.sheets]
    parts = [{"width": p.width, "length": p.length, "name": p.name, "quantity": p.quantity} for p in project.parts]
    
    result = optimize_cutlist(sheets, parts)
    
    # Save result
    import json
    opt_result = OptimizationResult(
        project_id=project_id,
        waste_percentage=result.get("waste_percentage", 0),
        total_sheets_used=result.get("total_sheets", 0),
        layout_data=json.dumps(result.get("layout", [])),
        settings=json.dumps({"kerf": 0.125})
    )
    db.add(opt_result)
    db.commit()
    
    return {
        "optimization_id": opt_result.id,
        "waste_percentage": opt_result.waste_percentage,
        "total_sheets_used": opt_result.total_sheets_used,
        "layout": result.get("layout", [])
    }

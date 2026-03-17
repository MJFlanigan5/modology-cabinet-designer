"""
Collaboration router for project sharing
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.database import get_db
from app.models import Project, User, ProjectShare
from app.routers.auth import get_current_user
from pydantic import BaseModel, EmailStr

router = APIRouter(prefix="/api/collaboration", tags=["collaboration"])

# Pydantic schemas
class ProjectShareCreate(BaseModel):
    user_email: EmailStr
    permission: str = "view"  # view, edit, admin

class ProjectShareResponse(BaseModel):
    id: int
    user_id: int
    user_email: str
    user_name: str = None
    permission: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class SharedProjectResponse(BaseModel):
    project_id: int
    project_name: str
    owner_name: str = None
    permission: str
    shared_at: datetime


@router.post("/{project_id}/share", response_model=ProjectShareResponse)
async def share_project(
    project_id: int,
    share: ProjectShareCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Share a project with another user"""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Check permission - owner or admin can share
    if project.owner_id != current_user.id:
        share_record = [s for s in project.shares if s.user_id == current_user.id and s.permission == "admin"]
        if not share_record:
            raise HTTPException(status_code=403, detail="Only owner or admin can share")
    
    # Find target user
    target_user = db.query(User).filter(User.email == share.user_email).first()
    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if target_user.id == project.owner_id:
        raise HTTPException(status_code=400, detail="Cannot share with owner")
    
    # Validate permission
    if share.permission not in ["view", "edit", "admin"]:
        raise HTTPException(status_code=400, detail="Invalid permission. Use: view, edit, or admin")
    
    # Check for existing share
    existing = db.query(ProjectShare).filter(
        ProjectShare.project_id == project_id,
        ProjectShare.user_id == target_user.id
    ).first()
    
    if existing:
        # Update existing share
        existing.permission = share.permission
        db.commit()
        db.refresh(existing)
        return ProjectShareResponse(
            id=existing.id,
            user_id=target_user.id,
            user_email=target_user.email,
            user_name=target_user.name,
            permission=existing.permission,
            created_at=existing.created_at
        )
    
    # Create new share
    new_share = ProjectShare(
        project_id=project_id,
        user_id=target_user.id,
        permission=share.permission
    )
    db.add(new_share)
    db.commit()
    db.refresh(new_share)
    
    return ProjectShareResponse(
        id=new_share.id,
        user_id=target_user.id,
        user_email=target_user.email,
        user_name=target_user.name,
        permission=new_share.permission,
        created_at=new_share.created_at
    )


@router.get("/{project_id}/shares", response_model=List[ProjectShareResponse])
async def list_shares(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List all shares for a project"""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Only owner can view shares
    if project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only owner can view shares")
    
    return [ProjectShareResponse(
        id=s.id,
        user_id=s.user_id,
        user_email=s.user.email,
        user_name=s.user.name,
        permission=s.permission,
        created_at=s.created_at
    ) for s in project.shares]


@router.delete("/{project_id}/share/{user_id}")
async def remove_share(
    project_id: int,
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Remove a user's access to a project"""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Only owner can remove shares
    if project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only owner can remove shares")
    
    share = db.query(ProjectShare).filter(
        ProjectShare.project_id == project_id,
        ProjectShare.user_id == user_id
    ).first()
    
    if not share:
        raise HTTPException(status_code=404, detail="Share not found")
    
    db.delete(share)
    db.commit()
    return {"message": "Share removed"}


@router.get("/shared-with-me", response_model=List[SharedProjectResponse])
async def shared_with_me(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all projects shared with the current user"""
    shares = db.query(ProjectShare).filter(ProjectShare.user_id == current_user.id).all()
    return [
        SharedProjectResponse(
            project_id=s.project_id,
            project_name=s.project.name,
            owner_name=s.project.owner.name if s.project.owner else None,
            permission=s.permission,
            shared_at=s.created_at
        ) for s in shares
    ]


@router.put("/{project_id}/share/{user_id}")
async def update_share_permission(
    project_id: int,
    user_id: int,
    permission: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a user's permission on a project"""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    if project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only owner can update permissions")
    
    if permission not in ["view", "edit", "admin"]:
        raise HTTPException(status_code=400, detail="Invalid permission")
    
    share = db.query(ProjectShare).filter(
        ProjectShare.project_id == project_id,
        ProjectShare.user_id == user_id
    ).first()
    
    if not share:
        raise HTTPException(status_code=404, detail="Share not found")
    
    share.permission = permission
    db.commit()
    
    return {"message": "Permission updated", "permission": permission}

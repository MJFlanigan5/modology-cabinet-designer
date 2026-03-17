"""
Database models for Modology Cabinet Designer
"""
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Cabinet(Base):
    """
    Cabinet model for storing cabinet designs
    """
    __tablename__ = "cabinets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text, nullable=True)
    width = Column(Float)  # Width in inches
    height = Column(Float)  # Height in inches
    depth = Column(Float)  # Depth in inches
    material_id = Column(Integer, ForeignKey("materials.id"), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    material = relationship("Material", back_populates="cabinets")
    components = relationship("CabinetComponent", back_populates="cabinet", cascade="all, delete-orphan")
    cut_lists = relationship("CutList", back_populates="cabinet", cascade="all, delete-orphan")


class Material(Base):
    """
    Material model for storing sheet goods (plywood, MDF, etc.)
    """
    __tablename__ = "materials"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    type = Column(String)  # plywood, mdf, hardwood, particleboard
    thickness = Column(Float)  # Thickness in inches (e.g., 0.75 for 3/4")
    sheet_width = Column(Float, default=48.0)  # Standard 4x8 sheet width
    sheet_height = Column(Float, default=96.0)  # Standard 4x8 sheet height
    price_per_sqft = Column(Float)  # Price per square foot
    supplier = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    cabinets = relationship("Cabinet", back_populates="material")


class Hardware(Base):
    """
    Hardware model for storing cabinet hardware (hinges, slides, etc.)
    """
    __tablename__ = "hardware"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    type = Column(String)  # hinge, slide, screw, bracket, handle, knob, etc.
    description = Column(Text, nullable=True)
    price = Column(Float)
    supplier = Column(String, nullable=True)
    url = Column(String, nullable=True)  # Link to supplier
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class CabinetComponent(Base):
    """
    CabinetComponent model for storing individual parts of a cabinet
    """
    __tablename__ = "cabinet_components"

    id = Column(Integer, primary_key=True, index=True)
    cabinet_id = Column(Integer, ForeignKey("cabinets.id"))
    name = Column(String)  # Side, top, bottom, back, shelf, door, drawer
    width = Column(Float)  # Width in inches
    height = Column(Float)  # Height in inches
    thickness = Column(Float, nullable=True)  # Thickness in inches
    material_id = Column(Integer, ForeignKey("materials.id"), nullable=True)
    quantity = Column(Integer, default=1)
    edge_banding = Column(String, nullable=True)  # none, all, top, bottom, left, right
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    cabinet = relationship("Cabinet", back_populates="components")
    material = relationship("Material")


class CutList(Base):
    """
    CutList model for storing optimized cutting plans
    """
    __tablename__ = "cut_lists"

    id = Column(Integer, primary_key=True, index=True)
    cabinet_id = Column(Integer, ForeignKey("cabinets.id"))
    name = Column(String)
    optimization_algorithm = Column(String, default="guillotine")  # guillotine, nested
    material_id = Column(Integer, ForeignKey("materials.id"))
    total_sheets_needed = Column(Integer, default=0)
    waste_percentage = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    cabinet = relationship("Cabinet", back_populates="cut_lists")
    material = relationship("Material")
    cut_items = relationship("CutItem", back_populates="cut_list", cascade="all, delete-orphan")


class CutItem(Base):
    """
    CutItem model for storing individual cut positions on a sheet
    """
    __tablename__ = "cut_items"

    id = Column(Integer, primary_key=True, index=True)
    cut_list_id = Column(Integer, ForeignKey("cut_lists.id"))
    component_id = Column(Integer, ForeignKey("cabinet_components.id"))
    sheet_index = Column(Integer)  # Which sheet this cut belongs to
    x_position = Column(Float)  # X position on sheet (inches)
    y_position = Column(Float)  # Y position on sheet (inches)
    width = Column(Float)  # Width of cut (inches)
    height = Column(Float)  # Height of cut (inches)
    rotation = Column(Boolean, default=False)  # Whether part is rotated 90 degrees
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    cut_list = relationship("CutList", back_populates="cut_items")


class Project(Base):
    """
    Project model for grouping cabinets into projects
    """
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text, nullable=True)
    user_id = Column(String, nullable=True)  # For multi-user support later
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    cabinets = relationship("Cabinet", secondary="project_cabinets", back_populates="projects")


# Association table for many-to-many relationship between projects and cabinets
from sqlalchemy import Table

project_cabinets = Table(
    "project_cabinets",
    Base.metadata,
    Column("project_id", Integer, ForeignKey("projects.id"), primary_key=True),
    Column("cabinet_id", Integer, ForeignKey("cabinets.id"), primary_key=True)
)

# Add back-reference to Project
Project.cabinets = relationship("Cabinet", secondary=project_cabinets, back_populates="projects")
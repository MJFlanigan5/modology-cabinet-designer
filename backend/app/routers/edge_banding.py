"""
Edge Banding Router - API endpoints for edge banding optimization
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
from enum import Enum

from app.edge_banding import (
    EdgeBandingOptimizer,
    EdgeBandingType,
    EdgePosition,
    EdgeBandingSpec,
    calculate_edge_banding,
    get_edge_banding_summary
)

router = APIRouter(prefix="/api/edge-banding", tags=["edge-banding"])


class EdgeBandingTypeEnum(str, Enum):
    WOOD_VENEER = "wood_veneer"
    PVC = "pvc"
    MELAMINE = "melamine"
    ABS = "abs"
    METAL = "metal"
    NONE = "none"


class EdgePositionEnum(str, Enum):
    TOP = "top"
    BOTTOM = "bottom"
    LEFT = "left"
    RIGHT = "right"
    FRONT = "front"
    BACK = "back"
    ALL = "all"


class ComponentEdges(BaseModel):
    id: str
    name: str
    width: float
    height: float
    edges: List[EdgePositionEnum]
    visible_edges: bool = True
    priority: int = 1


class EdgeBandingRequest(BaseModel):
    components: List[ComponentEdges]
    default_banding_type: EdgeBandingTypeEnum = EdgeBandingTypeEnum.WOOD_VENEER
    default_thickness: float = 1.0
    waste_factor: float = 1.1


class SingleComponentRequest(BaseModel):
    width: float
    height: float
    edges: List[EdgePositionEnum]
    banding_type: EdgeBandingTypeEnum = EdgeBandingTypeEnum.WOOD_VENEER
    thickness: float = 1.0


@router.post("/calculate")
async def calculate_edge_banding_requirements(request: EdgeBandingRequest):
    """
    Calculate edge banding requirements for multiple components.
    
    Returns:
    - Total linear feet needed
    - Total cost estimate
    - Breakdown by component
    - Purchase list with roll recommendations
    """
    try:
        components_dict = [
            {
                "id": c.id,
                "name": c.name,
                "width": c.width,
                "height": c.height,
                "edges": [e.value for e in c.edges],
                "visible_edges": c.visible_edges,
                "priority": c.priority
            }
            for c in request.components
        ]
        
        result = calculate_edge_banding(
            components=components_dict,
            default_banding_type=request.default_banding_type.value,
            default_thickness=request.default_thickness,
            waste_factor=request.waste_factor
        )
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Edge banding calculation failed: {str(e)}")


@router.post("/single")
async def calculate_single_component(request: SingleComponentRequest):
    """
    Quick edge banding calculation for a single component.
    
    Returns linear feet and cost estimate for one component.
    """
    try:
        result = get_edge_banding_summary(
            width=request.width,
            height=request.height,
            edges=[e.value for e in request.edges],
            banding_type=request.banding_type.value,
            thickness=request.thickness
        )
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Calculation failed: {str(e)}")


@router.get("/types")
async def list_edge_banding_types():
    """List available edge banding types with cost information."""
    return [
        {
            "id": "wood_veneer",
            "name": "Wood Veneer",
            "description": "Real wood veneer for natural look",
            "cost_per_foot": 0.15,
            "thicknesses_mm": [0.5, 1.0, 2.0],
            "best_for": ["Stained cabinets", "Premium finish", "Visible edges"]
        },
        {
            "id": "pvc",
            "name": "PVC",
            "description": "Durable plastic edge banding",
            "cost_per_foot": 0.08,
            "thicknesses_mm": [0.5, 1.0, 2.0, 3.0],
            "best_for": ["Painted cabinets", "High moisture areas", "Commercial use"]
        },
        {
            "id": "melamine",
            "name": "Melamine",
            "description": "Paper-based edge banding",
            "cost_per_foot": 0.05,
            "thicknesses_mm": [0.5],
            "best_for": ["Budget projects", "Matching melamine panels", "Low visibility edges"]
        },
        {
            "id": "abs",
            "name": "ABS",
            "description": "Acrylonitrile butadiene styrene - durable and eco-friendly",
            "cost_per_foot": 0.12,
            "thicknesses_mm": [1.0, 2.0, 3.0],
            "best_for": ["Eco-friendly projects", "Durable finish", "European standards"]
        },
        {
            "id": "metal",
            "name": "Metal",
            "description": "Aluminum or steel edge banding",
            "cost_per_foot": 0.35,
            "thicknesses_mm": [1.0, 2.0],
            "best_for": ["Industrial style", "Commercial fixtures", "High durability"]
        }
    ]


@router.get("/positions")
async def list_edge_positions():
    """List edge position options with descriptions."""
    return [
        {"id": "top", "name": "Top Edge", "description": "Top horizontal edge"},
        {"id": "bottom", "name": "Bottom Edge", "description": "Bottom horizontal edge"},
        {"id": "left", "name": "Left Edge", "description": "Left vertical edge"},
        {"id": "right", "name": "Right Edge", "description": "Right vertical edge"},
        {"id": "front", "name": "Front Edge", "description": "Front visible edge (most common)"},
        {"id": "back", "name": "Back Edge", "description": "Back edge (usually not needed)"},
        {"id": "all", "name": "All Edges", "description": "Band all edges"}
    ]


@router.get("/roll-sizes")
async def list_roll_sizes():
    """List standard edge banding roll sizes."""
    return [
        {
            "size": "small",
            "length_feet": 25,
            "description": "Small project or single cabinet",
            "best_for": ["Single cabinet", "Touch-up work", "Small repairs"]
        },
        {
            "size": "medium",
            "length_feet": 50,
            "description": "Medium project",
            "best_for": ["Kitchenette", "Bathroom vanity", "Small kitchen"]
        },
        {
            "size": "large",
            "length_feet": 250,
            "description": "Large project or professional use",
            "best_for": ["Full kitchen", "Multiple rooms", "Professional shop"]
        }
    ]


@router.get("/suppliers")
async def list_edge_banding_suppliers():
    """List suppliers for edge banding materials."""
    return [
        {
            "name": "Rockler",
            "url": "https://www.rockler.com/search?q=edge+banding",
            "carries": ["Wood Veneer", "PVC", "Iron-on"],
            "notes": "Good selection of pre-glued options"
        },
        {
            "name": "Woodcraft",
            "url": "https://www.woodcraft.com/search?q=edge+banding",
            "carries": ["Wood Veneer", "PVC"],
            "notes": "Wide variety of wood species"
        },
        {
            "name": "Home Depot",
            "url": "https://www.homedepot.com/s/edge%20banding",
            "carries": ["Wood Veneer", "PVC"],
            "notes": "Basic selection, good for quick pickup"
        },
        {
            "name": "FastCap",
            "url": "https://www.fastcap.com/product/edge-banding",
            "carries": ["Wood Veneer", "PVC", "ABS"],
            "notes": "Professional grade, peel-and-stick options"
        }
    ]

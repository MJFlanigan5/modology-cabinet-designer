"""
Hardware Recommendations Router - API endpoints for design-based hardware suggestions
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
from enum import Enum

from app.hardware_recommendations import (
    HardwareRecommendationEngine,
    CabinetType,
    DoorType,
    HardwareCategory,
    get_hardware_recommendations
)

router = APIRouter(prefix="/api/hardware-recommendations", tags=["hardware-recommendations"])


class CabinetTypeEnum(str, Enum):
    BASE = "base"
    WALL = "wall"
    TALL = "tall"
    CORNER = "corner"
    VANITY = "vanity"
    PANTRY = "pantry"
    ENTERTAINMENT = "entertainment"
    GARAGE = "garage"


class DoorTypeEnum(str, Enum):
    SINGLE_DOOR = "single_door"
    DOUBLE_DOOR = "double_door"
    DRAWER_BANK = "drawer_bank"
    DOOR_DRAWER = "door_drawer"
    OPEN_SHELF = "open_shelf"
    LAZY_SUSAN = "lazy_susan"
    NONE = "none"


class HardwareRecommendationRequest(BaseModel):
    width: float
    height: float
    depth: float
    cabinet_type: CabinetTypeEnum = CabinetTypeEnum.BASE
    door_type: DoorTypeEnum = DoorTypeEnum.SINGLE_DOOR
    num_doors: int = 1
    num_drawers: int = 0
    num_shelves: int = 2
    has_soft_close: bool = True
    has_face_frame: bool = True
    material_thickness: float = 0.75


@router.post("/analyze")
async def analyze_cabinet_design(request: HardwareRecommendationRequest):
    """
    Analyze cabinet design and get hardware recommendations.
    
    Returns comprehensive hardware suggestions based on:
    - Cabinet type (base, wall, tall, etc.)
    - Door configuration
    - Dimensions
    - Desired features (soft-close, face frame, etc.)
    
    Includes:
    - Quantity calculations
    - Price estimates
    - Supplier links
    - Installation notes
    """
    try:
        result = get_hardware_recommendations(
            width=request.width,
            height=request.height,
            depth=request.depth,
            cabinet_type=request.cabinet_type.value,
            door_type=request.door_type.value,
            num_doors=request.num_doors,
            num_drawers=request.num_drawers,
            num_shelves=request.num_shelves,
            has_soft_close=request.has_soft_close,
            has_face_frame=request.has_face_frame
        )
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Hardware recommendation failed: {str(e)}")


@router.get("/cabinet-types")
async def list_cabinet_types():
    """List all cabinet types with descriptions."""
    return [
        {
            "id": "base",
            "name": "Base Cabinet",
            "description": "Standard floor cabinet, typically 34.5\" tall",
            "typical_height": 34.5,
            "typical_depth": 24,
            "typical_width_range": [12, 48]
        },
        {
            "id": "wall",
            "name": "Wall Cabinet",
            "description": "Wall-mounted upper cabinet",
            "typical_height": 30,
            "typical_depth": 12,
            "typical_width_range": [12, 48]
        },
        {
            "id": "tall",
            "name": "Tall Cabinet",
            "description": "Floor-to-ceiling cabinet (pantry, utility)",
            "typical_height": 84,
            "typical_depth": 24,
            "typical_width_range": [12, 36]
        },
        {
            "id": "corner",
            "name": "Corner Cabinet",
            "description": "Corner cabinet with lazy susan or blind corner",
            "typical_height": 34.5,
            "typical_depth": 34,
            "typical_width_range": [33, 42]
        },
        {
            "id": "vanity",
            "name": "Vanity Cabinet",
            "description": "Bathroom vanity cabinet",
            "typical_height": 34,
            "typical_depth": 21,
            "typical_width_range": [18, 72]
        },
        {
            "id": "pantry",
            "name": "Pantry Cabinet",
            "description": "Tall cabinet for food storage",
            "typical_height": 84,
            "typical_depth": 24,
            "typical_width_range": [12, 24]
        },
        {
            "id": "entertainment",
            "name": "Entertainment Cabinet",
            "description": "Media console or TV cabinet",
            "typical_height": 24,
            "typical_depth": 18,
            "typical_width_range": [48, 96]
        },
        {
            "id": "garage",
            "name": "Garage Cabinet",
            "description": "Heavy-duty utility cabinet",
            "typical_height": 72,
            "typical_depth": 24,
            "typical_width_range": [24, 48]
        }
    ]


@router.get("/door-types")
async def list_door_types():
    """List all door configuration types."""
    return [
        {
            "id": "single_door",
            "name": "Single Door",
            "description": "One door covering the cabinet opening",
            "typical_width_range": [12, 24]
        },
        {
            "id": "double_door",
            "name": "Double Doors",
            "description": "Two doors meeting in the center",
            "typical_width_range": [24, 48]
        },
        {
            "id": "drawer_bank",
            "name": "Drawer Bank",
            "description": "Multiple drawers stacked vertically",
            "typical_drawers": [3, 5]
        },
        {
            "id": "door_drawer",
            "name": "Door over Drawer",
            "description": "Door above with drawer below (or vice versa)",
            "typical_configuration": "1 door + 1 drawer"
        },
        {
            "id": "open_shelf",
            "name": "Open Shelf",
            "description": "No doors, open shelving",
            "hardware_needed": "Shelf pins only"
        },
        {
            "id": "lazy_susan",
            "name": "Lazy Susan",
            "description": "Corner cabinet with rotating shelves",
            "hardware_needed": "Specialized corner hardware"
        },
        {
            "id": "none",
            "name": "No Doors",
            "description": "Cabinet box only, no doors or drawers",
            "hardware_needed": "Assembly hardware only"
        }
    ]


@router.get("/hardware-categories")
async def list_hardware_categories():
    """List all hardware categories."""
    return [
        {
            "id": "hinge",
            "name": "Hinges",
            "description": "Door mounting hardware",
            "essential": True
        },
        {
            "id": "drawer_slide",
            "name": "Drawer Slides",
            "description": "Drawer mounting hardware",
            "essential": True
        },
        {
            "id": "knob",
            "name": "Knobs",
            "description": "Door/drawer knobs",
            "essential": False
        },
        {
            "id": "pull",
            "name": "Pulls",
            "description": "Door/drawer pulls and handles",
            "essential": False
        },
        {
            "id": "shelf_pin",
            "name": "Shelf Pins",
            "description": "Adjustable shelf supports",
            "essential": False
        },
        {
            "id": "screw",
            "name": "Screws & Fasteners",
            "description": "Assembly hardware",
            "essential": True
        },
        {
            "id": "bracket",
            "name": "Brackets",
            "description": "Mounting and support brackets",
            "essential": False
        },
        {
            "id": "catch",
            "name": "Catches & Latches",
            "description": "Door catches and magnetic latches",
            "essential": False
        },
        {
            "id": "lighting",
            "name": "Cabinet Lighting",
            "description": "Under-cabinet and interior lighting",
            "essential": False
        }
    ]


@router.get("/hinge-guide")
async def get_hinge_selection_guide():
    """Get guide for selecting the right hinges."""
    return {
        "overlay_types": [
            {
                "type": "Standard Overlay",
                "description": "Door covers part of the face frame",
                "overlay": "0.5\" - 0.625\"",
                "best_for": "Traditional face frame cabinets"
            },
            {
                "type": "Full Overlay",
                "description": "Door covers entire face frame",
                "overlay": "0.625\" - 0.75\"",
                "best_for": "Frameless cabinets, modern look"
            },
            {
                "type": "Inset",
                "description": "Door sits flush with face frame",
                "overlay": "0\"",
                "best_for": "Traditional furniture-style cabinets"
            }
        ],
        "opening_angles": [
            {"angle": 95, "description": "Standard opening", "best_for": "Most applications"},
            {"angle": 110, "description": "Wide opening", "best_for": "Corner cabinets, tight spaces"},
            {"angle": 170, "description": "Extra-wide opening", "best_for": "Lazy susan, corner access"}
        ],
        "hinges_per_door": [
            {"door_height": "Up to 40\"", "hinges": 2},
            {"door_height": "40\" - 48\"", "hinges": 3},
            {"door_height": "Over 48\"", "hinges": 4}
        ],
        "soft_close_benefits": [
            "Prevents door slamming",
            "Extends hinge life",
            "Quieter operation",
            "Safer for children"
        ]
    }


@router.get("/drawer-slide-guide")
async def get_drawer_slide_guide():
    """Get guide for selecting drawer slides."""
    return {
        "extension_types": [
            {
                "type": "3/4 Extension",
                "description": "Drawer opens 3/4 of its length",
                "best_for": "Budget builds, less frequently used drawers"
            },
            {
                "type": "Full Extension",
                "description": "Drawer opens completely",
                "best_for": "Most applications, full access to contents"
            },
            {
                "type": "Over-travel",
                "description": "Drawer extends past cabinet",
                "best_for": "File drawers, deep access needed"
            }
        ],
        "mounting_styles": [
            {
                "type": "Side Mount",
                "description": "Mounted on drawer sides",
                "pros": ["Easy installation", "Adjustable"],
                "cons": ["Visible when open"]
            },
            {
                "type": "Under-mount",
                "description": "Hidden beneath drawer",
                "pros": ["Clean look", "Full width drawer"],
                "cons": ["More expensive", "Requires specific drawer box"]
            },
            {
                "type": "Center Mount",
                "description": "Single slide under center",
                "pros": ["Very economical", "Simple"],
                "cons": ["Less stable", "Lower weight capacity"]
            }
        ],
        "standard_lengths": [12, 14, 15, 16, 18, 20, 21, 22, 24],
        "weight_capacities": {
            "light_duty": "75-100 lbs",
            "medium_duty": "100-150 lbs",
            "heavy_duty": "150-500 lbs"
        }
    }


@router.post("/quick-estimate")
async def quick_hardware_estimate(
    cabinet_type: CabinetTypeEnum,
    width: float,
    height: float,
    depth: float,
    num_doors: int = 1,
    num_drawers: int = 0
):
    """
    Quick hardware cost estimate without full analysis.
    
    Returns rough cost range for hardware based on cabinet parameters.
    """
    result = get_hardware_recommendations(
        width=width,
        height=height,
        depth=depth,
        cabinet_type=cabinet_type.value,
        num_doors=num_doors,
        num_drawers=num_drawers
    )
    
    return {
        "cabinet_type": cabinet_type.value,
        "dimensions": f"{width}\" × {height}\" × {depth}\"",
        "estimated_hardware_cost": {
            "low": result["summary"]["total_cost_low"],
            "high": result["summary"]["total_cost_high"]
        },
        "categories_needed": result["summary"]["categories_needed"],
        "total_items": result["summary"]["total_items"]
    }

"""
Advanced Nesting Router - API endpoints for non-guillotine nesting algorithms
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
from enum import Enum

from app.advanced_nesting import (
    AdvancedNester,
    NestingAlgorithm,
    nest_parts,
    NestingResult,
    NestedSheet
)

router = APIRouter(prefix="/api/nesting", tags=["advanced-nesting"])


class NestingAlgorithmEnum(str, Enum):
    BOTTOM_LEFT = "bottom_left"
    NFDH = "nfdh"
    FFDH = "ffdh"
    BFDH = "bfdh"


class PartToNest(BaseModel):
    id: str
    name: str
    width: float
    height: float
    quantity: int = 1
    material_id: Optional[str] = None


class NestingRequest(BaseModel):
    parts: List[PartToNest]
    sheet_width: float = 48.0
    sheet_height: float = 96.0
    algorithm: NestingAlgorithmEnum = NestingAlgorithmEnum.BOTTOM_LEFT
    kerf_width: float = 0.125
    part_spacing: float = 0.25
    allow_rotation: bool = True


class NestedPartResponse(BaseModel):
    part_id: str
    part_name: str
    x: float
    y: float
    width: float
    height: float
    rotation: int


class SheetResponse(BaseModel):
    sheet_number: int
    width: float
    height: float
    utilization: float
    parts: List[NestedPartResponse]


class NestingResponse(BaseModel):
    algorithm: str
    sheets: List[SheetResponse]
    total_sheets: int
    waste_percentage: float
    total_used_area: float
    total_material_area: float
    execution_time_ms: float


@router.post("/optimize", response_model=NestingResponse)
async def optimize_nesting(request: NestingRequest):
    """
    Optimize part placement using advanced nesting algorithms.
    
    Supports multiple algorithms:
    - **bottom_left**: Places parts at lowest, leftmost valid position
    - **nfdh**: Next Fit Decreasing Height - parts sorted by height
    - **ffdh**: First Fit Decreasing Height - first level that fits
    - **bfdh**: Best Fit Decreasing Height - best level that fits
    
    All algorithms support rotation for better material utilization.
    """
    try:
        # Convert parts to dict format
        parts_dict = [
            {
                "id": p.id,
                "name": p.name,
                "width": p.width,
                "height": p.height,
                "quantity": p.quantity,
                "material_id": p.material_id
            }
            for p in request.parts
        ]
        
        result = nest_parts(
            parts=parts_dict,
            sheet_size=(request.sheet_width, request.sheet_height),
            algorithm=request.algorithm.value,
            kerf_width=request.kerf_width,
            part_spacing=request.part_spacing,
            allow_rotation=request.allow_rotation
        )
        
        return NestingResponse(**result)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Nesting optimization failed: {str(e)}")


@router.get("/algorithms")
async def list_algorithms():
    """List available nesting algorithms with descriptions."""
    return [
        {
            "id": "bottom_left",
            "name": "Bottom-Left",
            "description": "Places each part at the lowest, leftmost valid position. Good for irregular shapes.",
            "best_for": ["Mixed sizes", "Irregular shapes"],
            "speed": "Medium"
        },
        {
            "id": "nfdh",
            "name": "Next Fit Decreasing Height",
            "description": "Parts sorted by height and placed in levels. Fast but less optimal.",
            "best_for": ["Quick estimates", "Similar height parts"],
            "speed": "Fast"
        },
        {
            "id": "ffdh",
            "name": "First Fit Decreasing Height",
            "description": "Places each part in the first level where it fits. Better than NFDH.",
            "best_for": ["Moderate optimization", "Standard sheets"],
            "speed": "Fast"
        },
        {
            "id": "bfdh",
            "name": "Best Fit Decreasing Height",
            "description": "Places each part in the level with least remaining width. Most optimal level-based.",
            "best_for": ["Maximum efficiency", "Expensive materials"],
            "speed": "Medium"
        }
    ]


@router.post("/compare")
async def compare_algorithms(request: NestingRequest):
    """
    Compare all algorithms on the same parts to find the best result.
    Returns results from all algorithms sorted by waste percentage.
    """
    parts_dict = [
        {
            "id": p.id,
            "name": p.name,
            "width": p.width,
            "height": p.height,
            "quantity": p.quantity,
            "material_id": p.material_id
        }
        for p in request.parts
    ]
    
    results = []
    
    for algo in NestingAlgorithmEnum:
        try:
            result = nest_parts(
                parts=parts_dict,
                sheet_size=(request.sheet_width, request.sheet_height),
                algorithm=algo.value,
                kerf_width=request.kerf_width,
                part_spacing=request.part_spacing,
                allow_rotation=request.allow_rotation
            )
            results.append({
                "algorithm": algo.value,
                "total_sheets": result["total_sheets"],
                "waste_percentage": result["waste_percentage"],
                "execution_time_ms": result["execution_time_ms"]
            })
        except Exception:
            continue
    
    # Sort by waste percentage (ascending)
    results.sort(key=lambda x: x["waste_percentage"])
    
    return {
        "best_algorithm": results[0] if results else None,
        "comparison": results
    }

"""
Sketch-to-Design Import API
Converts uploaded sketches/photos to 3D cabinet models using AI
"""

from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from fastapi.responses import JSONResponse
from typing import Optional, List, Dict, Any
from pydantic import BaseModel
import base64
import json
from datetime import datetime

router = APIRouter()

# In-memory storage for sketches (in production, use database)
sketches_db: Dict[str, Dict] = {}

class SketchAnalysis(BaseModel):
    sketch_id: str
    detected_type: str  # cabinet, bookshelf, vanity, etc.
    confidence: float
    dimensions: Dict[str, float]
    style: str
    components: List[Dict[str, Any]]
    suggestions: List[str]

class CabinetFromSketch(BaseModel):
    sketch_id: str
    name: str
    width: float
    height: float
    depth: float
    style: str
    components: List[Dict[str, Any]]

# Cabinet style patterns for detection
STYLE_PATTERNS = {
    "shaker": {
        "description": "Classic shaker style with recessed panel doors",
        "features": ["recessed panel", "simple frame", "clean lines"],
        "door_style": "shaker"
    },
    "flat_panel": {
        "description": "Modern flat panel style with slab doors",
        "features": ["flat surface", "no frame", "minimalist"],
        "door_style": "slab"
    },
    "raised_panel": {
        "description": "Traditional raised panel with detailed doors",
        "features": ["raised center", "beveled edges", "ornate"],
        "door_style": "raised_panel"
    },
    "slab": {
        "description": "Simple slab doors for modern look",
        "features": ["flat", "no detail", "contemporary"],
        "door_style": "slab"
    },
    "beadboard": {
        "description": "Cottage style with vertical grooves",
        "features": ["vertical lines", "grooves", "country"],
        "door_style": "beadboard"
    },
    "glass_front": {
        "description": "Cabinet with glass door panels",
        "features": ["glass panel", "display", "open shelving option"],
        "door_style": "glass"
    }
}

# Cabinet type templates
CABINET_TEMPLATES = {
    "base_cabinet": {
        "default_height": 34.5,
        "default_depth": 24,
        "default_width": 36,
        "components": ["box", "door", "shelf", "drawer"]
    },
    "wall_cabinet": {
        "default_height": 30,
        "default_depth": 12,
        "default_width": 30,
        "components": ["box", "door", "shelf"]
    },
    "tall_cabinet": {
        "default_height": 84,
        "default_depth": 24,
        "default_width": 18,
        "components": ["box", "door", "shelf", "drawer"]
    },
    "bookshelf": {
        "default_height": 72,
        "default_depth": 12,
        "default_width": 36,
        "components": ["box", "shelves", "back"]
    },
    "vanity": {
        "default_height": 34,
        "default_depth": 21,
        "default_width": 36,
        "components": ["box", "door", "drawer", "countertop"]
    },
    "garage_cabinet": {
        "default_height": 72,
        "default_depth": 24,
        "default_width": 36,
        "components": ["box", "door", "shelf"]
    }
}

@router.post("/upload")
async def upload_sketch(
    file: UploadFile = File(...),
    name: Optional[str] = Form(None)
) -> Dict[str, Any]:
    """
    Upload a sketch or photo for analysis.
    Accepts: PNG, JPG, JPEG, PDF
    """
    # Validate file type
    allowed_types = ["image/png", "image/jpeg", "image/jpg", "application/pdf"]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed: PNG, JPG, JPEG, PDF"
        )
    
    # Read file content
    content = await file.read()
    
    # Generate sketch ID
    import uuid
    sketch_id = str(uuid.uuid4())[:8]
    
    # Store sketch metadata
    sketches_db[sketch_id] = {
        "id": sketch_id,
        "name": name or file.filename,
        "filename": file.filename,
        "content_type": file.content_type,
        "size": len(content),
        "uploaded_at": datetime.utcnow().isoformat(),
        "status": "uploaded"
    }
    
    return {
        "sketch_id": sketch_id,
        "filename": file.filename,
        "size": len(content),
        "status": "uploaded",
        "message": "Sketch uploaded successfully. Use /analyze to process."
    }

@router.post("/analyze/{sketch_id}", response_model=SketchAnalysis)
async def analyze_sketch(sketch_id: str) -> SketchAnalysis:
    """
    Analyze an uploaded sketch to detect cabinet type, style, and dimensions.
    Uses AI pattern recognition (simulated for demo).
    """
    if sketch_id not in sketches_db:
        raise HTTPException(status_code=404, detail="Sketch not found")
    
    sketch = sketches_db[sketch_id]
    sketch["status"] = "analyzing"
    
    # Simulate AI analysis
    # In production, this would call an actual ML model
    
    # Detect cabinet type (simulated)
    detected_type = "base_cabinet"  # Default
    confidence = 0.85
    
    # Detect dimensions (simulated)
    template = CABINET_TEMPLATES.get(detected_type, CABINET_TEMPLATES["base_cabinet"])
    dimensions = {
        "width": template["default_width"],
        "height": template["default_height"],
        "depth": template["default_depth"],
        "unit": "inches"
    }
    
    # Detect style (simulated)
    detected_style = "shaker"
    
    # Generate components based on template
    components = []
    for comp_name in template.get("components", []):
        components.append({
            "name": comp_name,
            "quantity": 1 if comp_name != "shelves" else 3,
            "dimensions": dimensions.copy() if comp_name == "box" else {
                "width": dimensions["width"] - 1.5,
                "height": dimensions["height"] - 3,
                "depth": dimensions["depth"] - 0.75
            }
        })
    
    # Generate suggestions
    suggestions = [
        f"Detected {detected_style} style cabinet",
        f"Estimated dimensions: {dimensions['width']}\"W x {dimensions['height']}\"H x {dimensions['depth']}\"D",
        "Consider adding soft-close hinges for better quality",
        "Add 3/4\" plywood edge banding for finished look"
    ]
    
    # Update sketch record
    sketch["status"] = "analyzed"
    sketch["analysis"] = {
        "detected_type": detected_type,
        "confidence": confidence,
        "dimensions": dimensions,
        "style": detected_style,
        "components": components
    }
    
    return SketchAnalysis(
        sketch_id=sketch_id,
        detected_type=detected_type,
        confidence=confidence,
        dimensions=dimensions,
        style=detected_style,
        components=components,
        suggestions=suggestions
    )

@router.post("/convert/{sketch_id}")
async def convert_to_cabinet(
    sketch_id: str,
    name: Optional[str] = None,
    width: Optional[float] = None,
    height: Optional[float] = None,
    depth: Optional[float] = None,
    style: Optional[str] = None
) -> Dict[str, Any]:
    """
    Convert analyzed sketch to a cabinet design.
    Allows override of detected dimensions and style.
    """
    if sketch_id not in sketches_db:
        raise HTTPException(status_code=404, detail="Sketch not found")
    
    sketch = sketches_db[sketch_id]
    
    if "analysis" not in sketch:
        raise HTTPException(
            status_code=400,
            detail="Sketch must be analyzed first. Use /analyze endpoint."
        )
    
    analysis = sketch["analysis"]
    
    # Use provided values or fall back to analysis
    final_width = width or analysis["dimensions"]["width"]
    final_height = height or analysis["dimensions"]["height"]
    final_depth = depth or analysis["dimensions"]["depth"]
    final_style = style or analysis["style"]
    
    # Generate cabinet design
    cabinet = {
        "id": f"cab_{sketch_id}",
        "name": name or sketch.get("name", "Imported Cabinet"),
        "sketch_id": sketch_id,
        "type": analysis["detected_type"],
        "width": final_width,
        "height": final_height,
        "depth": final_depth,
        "style": final_style,
        "material": "3/4\" Plywood",
        "components": generate_cabinet_components(
            final_width, final_height, final_depth, final_style
        ),
        "hardware": generate_hardware_list(analysis["detected_type"]),
        "created_from": "sketch_import",
        "created_at": datetime.utcnow().isoformat()
    }
    
    sketch["converted_cabinet"] = cabinet
    sketch["status"] = "converted"
    
    return cabinet

@router.get("/styles")
async def list_styles() -> List[Dict[str, Any]]:
    """List all detectable cabinet styles"""
    return [
        {
            "name": name,
            **pattern
        }
        for name, pattern in STYLE_PATTERNS.items()
    ]

@router.get("/types")
async def list_cabinet_types() -> List[Dict[str, Any]]:
    """List all cabinet type templates"""
    return [
        {
            "name": name,
            **template
        }
        for name, template in CABINET_TEMPLATES.items()
    ]

@router.get("/sketches")
async def list_sketches() -> List[Dict[str, Any]]:
    """List all uploaded sketches"""
    return list(sketches_db.values())

@router.get("/sketches/{sketch_id}")
async def get_sketch(sketch_id: str) -> Dict[str, Any]:
    """Get sketch details and analysis"""
    if sketch_id not in sketches_db:
        raise HTTPException(status_code=404, detail="Sketch not found")
    return sketches_db[sketch_id]

@router.delete("/sketches/{sketch_id}")
async def delete_sketch(sketch_id: str) -> Dict[str, str]:
    """Delete a sketch"""
    if sketch_id not in sketches_db:
        raise HTTPException(status_code=404, detail="Sketch not found")
    del sketches_db[sketch_id]
    return {"message": f"Sketch {sketch_id} deleted"}

def generate_cabinet_components(
    width: float,
    height: float,
    depth: float,
    style: str
) -> List[Dict[str, Any]]:
    """Generate component list for cabinet"""
    # Standard cabinet construction
    plywood_thickness = 0.75
    
    components = [
        {
            "name": "Left Side",
            "quantity": 1,
            "width": depth,
            "height": height,
            "material": "3/4\" Plywood",
            "edge_banding": ["front"]
        },
        {
            "name": "Right Side",
            "quantity": 1,
            "width": depth,
            "height": height,
            "material": "3/4\" Plywood",
            "edge_banding": ["front"]
        },
        {
            "name": "Top",
            "quantity": 1,
            "width": width - (plywood_thickness * 2),
            "height": depth,
            "material": "3/4\" Plywood",
            "edge_banding": []
        },
        {
            "name": "Bottom",
            "quantity": 1,
            "width": width - (plywood_thickness * 2),
            "height": depth,
            "material": "3/4\" Plywood",
            "edge_banding": []
        },
        {
            "name": "Back",
            "quantity": 1,
            "width": width - 0.25,
            "height": height - 0.25,
            "material": "1/4\" Plywood",
            "edge_banding": []
        },
        {
            "name": "Door",
            "quantity": 1,
            "width": width - 0.125,
            "height": height - 0.5,
            "material": "3/4\" Plywood",
            "edge_banding": ["all"],
            "style": style
        },
        {
            "name": "Shelf",
            "quantity": 2,
            "width": width - (plywood_thickness * 2) - 0.25,
            "height": depth - 0.5,
            "material": "3/4\" Plywood",
            "edge_banding": ["front"]
        }
    ]
    
    return components

def generate_hardware_list(cabinet_type: str) -> List[Dict[str, Any]]:
    """Generate hardware list for cabinet type"""
    base_hardware = [
        {
            "name": "Concealed Hinge",
            "quantity": 2,
            "type": "hinge",
            "notes": "Soft-close recommended"
        },
        {
            "name": "Shelf Pin",
            "quantity": 8,
            "type": "shelf_support",
            "notes": "5mm brass shelf pins"
        }
    ]
    
    if cabinet_type in ["base_cabinet", "vanity"]:
        base_hardware.append({
            "name": "Drawer Slide",
            "quantity": 1,
            "type": "drawer_slide",
            "size": 18,
            "notes": "Full extension soft-close"
        })
    
    return base_hardware

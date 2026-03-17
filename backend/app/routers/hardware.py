"""
API routers for hardware management with supplier integration
Supports: Rockler, Woodcraft, Home Depot, McMaster-Carr,
          Woodworker Express, DK Hardware
"""
from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from app.database import get_db
from app.models import Hardware
from pydantic import BaseModel
from datetime import datetime
import urllib.parse

router = APIRouter(prefix="/api/hardware", tags=["hardware"])

# ============================================================================
# Supplier Configuration
# ============================================================================

SUPPLIERS = {
    "rockler": {
        "name": "Rockler",
        "base_url": "https://www.rockler.com",
        "search_url": "https://www.rockler.com/catalogsearch/result/?q={query}",
        "logo": "https://www.rockler.com/favicon.ico",
        "color": "#1E3A5F"
    },
    "woodcraft": {
        "name": "Woodcraft",
        "base_url": "https://www.woodcraft.com",
        "search_url": "https://www.woodcraft.com/search?q={query}",
        "logo": "https://www.woodcraft.com/favicon.ico",
        "color": "#8B0000"
    },
    "home_depot": {
        "name": "Home Depot",
        "base_url": "https://www.homedepot.com",
        "search_url": "https://www.homedepot.com/s/{query}",
        "logo": "https://www.homedepot.com/favicon.ico",
        "color": "#F96302"
    },
    "mcmaster": {
        "name": "McMaster-Carr",
        "base_url": "https://www.mcmaster.com",
        "search_url": "https://www.mcmaster.com/{query}",
        "logo": "https://www.mcmaster.com/favicon.ico",
        "color": "#000000"
    },
    "woodworker_express": {
        "name": "Woodworker Express",
        "base_url": "https://www.woodworkerexpress.com",
        "search_url": "https://www.woodworkerexpress.com/search?q={query}",
        "logo": "https://www.woodworkerexpress.com/favicon.ico",
        "color": "#2E7D32"
    },
    "dk_hardware": {
        "name": "DK Hardware",
        "base_url": "https://www.dkhardware.com",
        "search_url": "https://www.dkhardware.com/search?q={query}",
        "logo": "https://www.dkhardware.com/favicon.ico",
        "color": "#1565C0"
    }
}

# ============================================================================
# Hardware Type Categories
# ============================================================================

HARDWARE_CATEGORIES = {
    "hinge": {
        "name": "Hinges",
        "icon": "🔩",
        "subtypes": ["concealed", "european", "butt", "piano", "pivot", "soft-close"]
    },
    "slide": {
        "name": "Drawer Slides",
        "icon": "📤",
        "subtypes": ["full-extension", "soft-close", "under-mount", "side-mount", "center-mount"]
    },
    "screw": {
        "name": "Screws & Fasteners",
        "icon": "🔩",
        "subtypes": ["wood", "machine", "confirmat", "pocket-hole", "shelf-pin"]
    },
    "bracket": {
        "name": "Brackets & Supports",
        "icon": "📐",
        "subtypes": ["corner", "shelf", "countertop", "closet", "furniture"]
    },
    "handle": {
        "name": "Handles & Pulls",
        "icon": "🤲",
        "subtypes": ["cabinet-pull", "drawer-pull", "appliance-pull", "cup-pull", "bin-pull"]
    },
    "knob": {
        "name": "Knobs",
        "icon": "⭕",
        "subtypes": ["round", "square", "t-bar", "glass", "ceramic"]
    },
    "drawer": {
        "name": "Drawer Hardware",
        "icon": "📦",
        "subtypes": ["drawer-box", "drawer-front", "drawer-lock", "drawer-guide"]
    },
    "door": {
        "name": "Door Hardware",
        "icon": "🚪",
        "subtypes": ["catch", "latch", "magnet", "bumper", "lift-system"]
    },
    "shelf": {
        "name": "Shelf Hardware",
        "icon": "📚",
        "subtypes": ["pin", "bracket", "standard", "clip", "support"]
    },
    "lighting": {
        "name": "Cabinet Lighting",
        "icon": "💡",
        "subtypes": ["led-strip", "puck", "under-cabinet", "motion-sensor"]
    }
}

# ============================================================================
# Sample Hardware Data (for seeding)
# ============================================================================

SAMPLE_HARDWARE = [
    # Hinges
    {
        "name": "Soft-Close Concealed Hinge 110°",
        "type": "hinge",
        "description": "Full overlay soft-close European hinge for frameless cabinets",
        "price": 5.99,
        "supplier": "rockler",
        "url": "https://www.rockler.com/rockler-soft-close-concealed-cabinet-hinges"
    },
    {
        "name": "European Concealed Hinge 100°",
        "type": "hinge",
        "description": "Standard overlay European hinge with clip-on mounting plate",
        "price": 4.49,
        "supplier": "woodcraft",
        "url": "https://www.woodcraft.com/products/european-concealed-hinge"
    },
    {
        "name": "35mm Concealed Hinge Soft-Close",
        "type": "hinge",
        "description": "35mm cup soft-close hinge with depth adjustment",
        "price": 3.99,
        "supplier": "woodworker_express",
        "url": "https://www.woodworkerexpress.com/hinges/concealed-hinges"
    },
    {
        "name": "Heavy Duty Concealed Hinge",
        "type": "hinge",
        "description": "Heavy-duty concealed hinge for thick doors up to 1\"",
        "price": 7.99,
        "supplier": "dk_hardware",
        "url": "https://www.dkhardware.com/hinges"
    },
    
    # Drawer Slides
    {
        "name": "22\" Full Extension Soft-Close Slide",
        "type": "slide",
        "description": "Full extension drawer slide with soft-close mechanism, 100lb capacity",
        "price": 24.99,
        "supplier": "rockler",
        "url": "https://www.rockler.com/rockler-soft-close-full-extension-drawer-slides"
    },
    {
        "name": "18\" Under-Mount Soft-Close Slide",
        "type": "slide",
        "description": "Under-mount soft-close slide for frameless cabinets",
        "price": 34.99,
        "supplier": "woodcraft",
        "url": "https://www.woodcraft.com/products/under-mount-drawer-slides"
    },
    {
        "name": "24\" Full Extension Slide 100lb",
        "type": "slide",
        "description": "Side-mount full extension ball bearing slide",
        "price": 18.99,
        "supplier": "home_depot",
        "url": "https://www.homedepot.com/p/Drawer-Slides"
    },
    {
        "name": "21\" Soft-Close Under-Mount Slide",
        "type": "slide",
        "description": "Premium under-mount slide with 3-way adjustment",
        "price": 29.99,
        "supplier": "woodworker_express",
        "url": "https://www.woodworkerexpress.com/drawer-slides/under-mount"
    },
    
    # Handles & Pulls
    {
        "name": "Bar Pull 5\" CC Brushed Nickel",
        "type": "handle",
        "description": "Modern bar pull in brushed nickel finish, 5\" center-to-center",
        "price": 4.99,
        "supplier": "rockler",
        "url": "https://www.rockler.com/cabinet-pulls"
    },
    {
        "name": "Cup Pull Oil Rubbed Bronze 3.75\"",
        "type": "handle",
        "description": "Traditional cup pull in oil rubbed bronze",
        "price": 6.99,
        "supplier": "woodcraft",
        "url": "https://www.woodcraft.com/products/cabinet-pulls"
    },
    {
        "name": "Modern Square Pull 128mm Matte Black",
        "type": "handle",
        "description": "Contemporary square profile pull in matte black",
        "price": 7.49,
        "supplier": "dk_hardware",
        "url": "https://www.dkhardware.com/cabinet-handles"
    },
    
    # Knobs
    {
        "name": "Round Knob 1.25\" Brushed Nickel",
        "type": "knob",
        "description": "Classic round knob in brushed nickel finish",
        "price": 2.99,
        "supplier": "home_depot",
        "url": "https://www.homedepot.com/b/Hardware-Cabinet-Hardware-Cabinet-Knobs"
    },
    {
        "name": "Glass Knob Clear 1.5\"",
        "type": "knob",
        "description": "Elegant clear glass knob with chrome base",
        "price": 5.99,
        "supplier": "woodworker_express",
        "url": "https://www.woodworkerexpress.com/knobs/glass-knobs"
    },
    
    # Screws & Fasteners
    {
        "name": "Confirmat Screws 7mm x 50mm (100pk)",
        "type": "screw",
        "description": "Confirmat screws for particleboard/MDF cabinet assembly",
        "price": 19.99,
        "supplier": "woodworker_express",
        "url": "https://www.woodworkerexpress.com/screws/confirmat-screws"
    },
    {
        "name": "Pocket Hole Screws 1.25\" (1000pk)",
        "type": "screw",
        "description": "Coarse thread pocket hole screws for softwood",
        "price": 24.99,
        "supplier": "rockler",
        "url": "https://www.rockler.com/pocket-hole-screws"
    },
    {
        "name": "Shelf Pins 5mm Chrome (50pk)",
        "type": "screw",
        "description": "Chrome shelf pins for 5mm holes",
        "price": 8.99,
        "supplier": "woodcraft",
        "url": "https://www.woodcraft.com/products/shelf-pins"
    },
    
    # Brackets & Supports
    {
        "name": "Countertop Support Bracket 16\"",
        "type": "bracket",
        "description": "Heavy-duty steel bracket for countertop overhang support",
        "price": 29.99,
        "supplier": "rockler",
        "url": "https://www.rockler.com/countertop-support-brackets"
    },
    {
        "name": "Corner Bracket L-Shaped 4\" (4pk)",
        "type": "bracket",
        "description": "Zinc-plated corner brackets for cabinet reinforcement",
        "price": 12.99,
        "supplier": "home_depot",
        "url": "https://www.homedepot.com/b/Building-Materials-Fencing-Hardware-Brackets"
    },
    
    # Door Hardware
    {
        "name": "Magnetic Catch with Strike Plate",
        "type": "door",
        "description": "Strong magnetic catch for cabinet doors",
        "price": 3.99,
        "supplier": "woodworker_express",
        "url": "https://www.woodworkerexpress.com/door-hardware/catches"
    },
    {
        "name": "Twin Magnet Catch Soft-Touch",
        "type": "door",
        "description": "Push-to-open magnetic catch system",
        "price": 8.99,
        "supplier": "dk_hardware",
        "url": "https://www.dkhardware.com/cabinet-catches"
    },
    
    # Shelf Hardware
    {
        "name": "Shelf Standard 48\" White (2pk)",
        "type": "shelf",
        "description": "Metal shelf standards with holes for adjustable shelving",
        "price": 14.99,
        "supplier": "home_depot",
        "url": "https://www.homedepot.com/b/Storage-Organization-Shelving-Shelf-Brackets"
    },
    {
        "name": "Glass Shelf Bracket Chrome",
        "type": "shelf",
        "description": "Elegant chrome bracket for glass shelves up to 8mm thick",
        "price": 9.99,
        "supplier": "woodworker_express",
        "url": "https://www.woodworkerexpress.com/shelf-hardware/glass-brackets"
    },
    
    # Cabinet Lighting
    {
        "name": "LED Under-Cabinet Light 24\" Linkable",
        "type": "lighting",
        "description": "Linkable LED light bar with touch dimmer",
        "price": 39.99,
        "supplier": "home_depot",
        "url": "https://www.homedepot.com/b/Lighting-Ceiling-Fans-Under-Cabinet-Lights"
    },
    {
        "name": "LED Puck Light Kit 3-Pack",
        "type": "lighting",
        "description": "Wireless LED puck lights with remote control",
        "price": 29.99,
        "supplier": "woodcraft",
        "url": "https://www.woodcraft.com/products/cabinet-lighting"
    }
]

# ============================================================================
# Pydantic Models
# ============================================================================

class HardwareCreate(BaseModel):
    name: str
    type: str
    description: Optional[str] = None
    price: float
    supplier: Optional[str] = None
    url: Optional[str] = None

class HardwareResponse(BaseModel):
    id: int
    name: str
    type: str
    description: Optional[str] = None
    price: float
    supplier: Optional[str] = None
    url: Optional[str] = None
    is_active: bool
    
    class Config:
        from_attributes = True

class SupplierSearchResult(BaseModel):
    supplier: str
    supplier_name: str
    search_url: str
    base_url: str
    color: str

class HardwareComparison(BaseModel):
    hardware_id: int
    name: str
    type: str
    prices: List[Dict[str, Any]]

class SupplierInfo(BaseModel):
    id: str
    name: str
    base_url: str
    search_url: str
    color: str

class CategoryInfo(BaseModel):
    id: str
    name: str
    icon: str
    subtypes: List[str]

# ============================================================================
# API Endpoints
# ============================================================================

@router.post("/", response_model=HardwareResponse)
def create_hardware(hardware: HardwareCreate, db: Session = Depends(get_db)):
    """
    Create new hardware item
    """
    db_hardware = Hardware(**hardware.dict())
    db.add(db_hardware)
    db.commit()
    db.refresh(db_hardware)
    return db_hardware


@router.get("/", response_model=List[HardwareResponse])
def list_hardware(
    db: Session = Depends(get_db),
    type_filter: Optional[str] = Query(None, alias="type"),
    supplier_filter: Optional[str] = Query(None, alias="supplier"),
    search: Optional[str] = Query(None),
    limit: int = Query(100, ge=1, le=500)
):
    """
    List all hardware with optional filtering
    
    - **type_filter**: Filter by hardware type (hinge, slide, screw, etc.)
    - **supplier_filter**: Filter by supplier (rockler, woodcraft, etc.)
    - **search**: Search in name and description
    - **limit**: Max results to return
    """
    query = db.query(Hardware).filter(Hardware.is_active == True)
    
    if type_filter:
        query = query.filter(Hardware.type == type_filter)
    
    if supplier_filter:
        query = query.filter(Hardware.supplier == supplier_filter)
    
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            (Hardware.name.ilike(search_term)) |
            (Hardware.description.ilike(search_term))
        )
    
    hardware = query.limit(limit).all()
    return hardware


@router.get("/suppliers", response_model=List[SupplierInfo])
def get_suppliers():
    """
    Get list of all supported suppliers with their search URLs
    """
    return [
        SupplierInfo(
            id=key,
            name=data["name"],
            base_url=data["base_url"],
            search_url=data["search_url"].replace("{query}", "SEARCH_TERM"),
            color=data["color"]
        )
        for key, data in SUPPLIERS.items()
    ]


@router.get("/categories", response_model=Dict[str, CategoryInfo])
def get_categories():
    """
    Get all hardware categories with subtypes
    """
    return {
        key: CategoryInfo(
            id=key,
            name=data["name"],
            icon=data["icon"],
            subtypes=data["subtypes"]
        )
        for key, data in HARDWARE_CATEGORIES.items()
    }


@router.get("/search/{query}")
def search_supplier_links(query: str) -> List[SupplierSearchResult]:
    """
    Get direct search links for all suppliers
    
    Returns pre-built search URLs for each supplier to find the queried hardware.
    """
    encoded_query = urllib.parse.quote(query)
    
    results = []
    for supplier_id, supplier_data in SUPPLIERS.items():
        results.append(
            SupplierSearchResult(
                supplier=supplier_id,
                supplier_name=supplier_data["name"],
                search_url=supplier_data["search_url"].format(query=encoded_query),
                base_url=supplier_data["base_url"],
                color=supplier_data["color"]
            )
        )
    
    return results


@router.get("/compare/{hardware_type}")
def compare_hardware_prices(
    hardware_type: str,
    db: Session = Depends(get_db)
) -> List[HardwareComparison]:
    """
    Compare prices for a hardware type across suppliers
    
    Returns all hardware items of the specified type grouped for comparison.
    """
    hardware_items = db.query(Hardware).filter(
        Hardware.is_active == True,
        Hardware.type == hardware_type
    ).all()
    
    # Group by name similarity (simplified)
    comparisons = []
    seen_names = set()
    
    for item in hardware_items:
        # Simple grouping - in production would use fuzzy matching
        base_name = item.name.split("\"")[0].strip() if "\"" in item.name else item.name
        
        if base_name not in seen_names:
            seen_names.add(base_name)
            
            # Find similar items
            similar = [h for h in hardware_items if h.name.startswith(base_name[:20])]
            
            prices = [
                {
                    "supplier": h.supplier,
                    "supplier_name": SUPPLIERS.get(h.supplier, {}).get("name", h.supplier),
                    "price": h.price,
                    "url": h.url
                }
                for h in similar
            ]
            
            if len(prices) > 0:
                comparisons.append(
                    HardwareComparison(
                        hardware_id=item.id,
                        name=item.name,
                        type=item.type,
                        prices=prices
                    )
                )
    
    return comparisons


@router.get("/{hardware_id}", response_model=HardwareResponse)
def get_hardware(hardware_id: int, db: Session = Depends(get_db)):
    """
    Get specific hardware by ID
    """
    hardware = db.query(Hardware).filter(Hardware.id == hardware_id).first()
    if not hardware:
        raise HTTPException(status_code=404, detail="Hardware not found")
    return hardware


@router.delete("/{hardware_id}")
def delete_hardware(hardware_id: int, db: Session = Depends(get_db)):
    """
    Delete hardware (soft delete)
    """
    db_hardware = db.query(Hardware).filter(Hardware.id == hardware_id).first()
    if not db_hardware:
        raise HTTPException(status_code=404, detail="Hardware not found")
    
    db_hardware.is_active = False
    db.commit()
    return {"message": "Hardware deleted"}


@router.post("/seed")
def seed_sample_hardware(db: Session = Depends(get_db)):
    """
    Seed database with sample hardware data
    
    Useful for testing and initial setup.
    """
    added_count = 0
    for item_data in SAMPLE_HARDWARE:
        # Check if already exists
        existing = db.query(Hardware).filter(
            Hardware.name == item_data["name"],
            Hardware.supplier == item_data["supplier"]
        ).first()
        
        if not existing:
            hardware = Hardware(**item_data)
            db.add(hardware)
            added_count += 1
    
    db.commit()
    
    return {
        "message": f"Seeded {added_count} new hardware items",
        "total_sample_items": len(SAMPLE_HARDWARE)
    }


@router.get("/recommended/{cabinet_type}")
def get_recommended_hardware(
    cabinet_type: str,
    width: float = Query(..., description="Cabinet width in inches"),
    height: float = Query(..., description="Cabinet height in inches"),
    db: Session = Depends(get_db)
):
    """
    Get hardware recommendations based on cabinet type and dimensions
    
    Returns recommended hinges, slides, handles, and other hardware
    based on the cabinet specifications.
    """
    recommendations = {
        "cabinet_type": cabinet_type,
        "dimensions": {"width": width, "height": height},
        "hardware": []
    }
    
    # Hinge recommendations
    if cabinet_type in ["base", "wall", "tall"]:
        # Number of hinges based on door height
        if height < 24:
            num_hinges = 2
        elif height < 48:
            num_hinges = 3
        else:
            num_hinges = 4
        
        hinges = db.query(Hardware).filter(
            Hardware.type == "hinge",
            Hardware.is_active == True
        ).limit(3).all()
        
        if hinges:
            recommendations["hardware"].append({
                "category": "hinges",
                "quantity": num_hinges,
                "items": [
                    {
                        "id": h.id,
                        "name": h.name,
                        "price": h.price,
                        "supplier": h.supplier,
                        "url": h.url
                    } for h in hinges
                ]
            })
    
    # Drawer slide recommendations
    if cabinet_type == "base":
        # Determine slide length based on cabinet depth (typically 22-24")
        slide_length = min(22, int(width - 2))
        
        slides = db.query(Hardware).filter(
            Hardware.type == "slide",
            Hardware.is_active == True
        ).limit(3).all()
        
        if slides:
            recommendations["hardware"].append({
                "category": "drawer_slides",
                "quantity": 1,  # Per drawer
                "recommended_length": f"{slide_length}\"",
                "items": [
                    {
                        "id": s.id,
                        "name": s.name,
                        "price": s.price,
                        "supplier": s.supplier,
                        "url": s.url
                    } for s in slides
                ]
            })
    
    # Handle/knob recommendations
    handles = db.query(Hardware).filter(
        Hardware.type.in_(["handle", "knob"]),
        Hardware.is_active == True
    ).limit(6).all()
    
    if handles:
        recommendations["hardware"].append({
            "category": "handles_knobs",
            "quantity": 1,  # Per door/drawer
            "items": [
                {
                    "id": h.id,
                    "name": h.name,
                    "price": h.price,
                    "supplier": h.supplier,
                    "url": h.url
                } for h in handles
            ]
        })
    
    # Calculate estimated cost
    total_min = 0
    total_max = 0
    for category in recommendations["hardware"]:
        if category["items"]:
            prices = [item["price"] for item in category["items"]]
            total_min += min(prices) * category["quantity"]
            total_max += max(prices) * category["quantity"]
    
    recommendations["estimated_cost"] = {
        "min": round(total_min, 2),
        "max": round(total_max, 2),
        "currency": "USD"
    }
    
    return recommendations

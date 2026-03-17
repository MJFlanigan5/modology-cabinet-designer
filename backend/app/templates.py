"""
Project Templates - Pre-built cabinet designs inspired by popular woodworkers
and high-end cabinet manufacturers.
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
from enum import Enum
import json

router = APIRouter(prefix="/templates", tags=["templates"])


class CabinetStyle(str, Enum):
    SHAKER = "shaker"
    FLAT_PANEL = "flat_panel"
    RAISED_PANEL = "raised_panel"
    SLAB = "slab"
    BEADBOARD = "beadboard"
    LOUVERED = "louvered"
    THERMOFOIL = "thermofoil"
    GLASS_FRONT = "glass_front"
    OPEN_SHELF = "open_shelf"
    BARN_DOOR = "barn_door"


class RoomType(str, Enum):
    KITCHEN = "kitchen"
    BATHROOM = "bathroom"
    LAUNDRY = "laundry"
    OFFICE = "office"
    LIVING_ROOM = "living_room"
    BEDROOM = "bedroom"
    GARAGE = "garage"
    PANTRY = "pantry"
    MUDROOM = "mudroom"
    ENTERTAINMENT = "entertainment"


class InspirationSource(str, Enum):
    STEVE_RAMSEY = "steve_ramsey"  # Woodworking for Mere Mortals
    APRIL_WILKERSON = "april_wilkerson"
    JON_PETERS = "jon_peters"
    MARC_SPIAGNUOLO = "marc_spagnuolo"  # The Wood Whisperer
    JAY_BATES = "jay_bates"
    JOHN_HEISZ = "john_heisz"  # I Build It
    MATT_CREMONA = "matt_cremona"
    FRANK_HOWARTH = "frank_howarth"
    PATRICK_SORRELL = "patrick_sorrell"
    LEXSPEED = "lexspeed"
    CABINETS_TO_GO = "cabinets_to_go"
    CLIFFSIDE_CABINETS = "cliffside_cabinets"
    BARKER_DOOR = "barker_door"
    CONESTOGA = "conestoga"
    DECORA = "decora"
    KRAFTMAID = "kraftmaid"
    CUSTOM = "custom"


class CabinetComponent(BaseModel):
    name: str
    width: float  # inches
    height: float  # inches
    depth: float  # inches
    material: str
    quantity: int = 1
    edge_banding: Optional[List[str]] = []
    notes: Optional[str] = None


class CabinetTemplate(BaseModel):
    id: str
    name: str
    description: str
    style: CabinetStyle
    room_type: RoomType
    inspiration: InspirationSource
    inspiration_notes: Optional[str] = None
    difficulty: str  # "beginner", "intermediate", "advanced"
    estimated_hours: int
    estimated_cost_low: int  # USD
    estimated_cost_high: int  # USD
    components: List[CabinetComponent]
    hardware_needed: List[Dict]
    cut_list: List[Dict]
    joinery: List[str]
    finishing_suggestions: List[str]
    tags: List[str]
    images: Optional[List[str]] = []
    video_url: Optional[str] = None
    plans_url: Optional[str] = None


# ============================================================================
# KITCHEN CABINETS
# ============================================================================

KITCHEN_TEMPLATES = [
    CabinetTemplate(
        id="kitchen-base-shaker",
        name="Classic Shaker Base Cabinet",
        description="Traditional shaker-style base cabinet with soft-close drawers. Perfect for kitchen renovations. Inspired by Steve Ramsey's practical approach to woodworking.",
        style=CabinetStyle.SHAKER,
        room_type=RoomType.KITCHEN,
        inspiration=InspirationSource.STEVE_RAMSEY,
        inspiration_notes="Simple, functional design focused on accessibility for beginner woodworkers",
        difficulty="beginner",
        estimated_hours=8,
        estimated_cost_low=150,
        estimated_cost_high=250,
        components=[
            CabinetComponent(name="Side Panel (Left)", width=24, height=34.5, depth=0.75, material="3/4\" Plywood", quantity=1),
            CabinetComponent(name="Side Panel (Right)", width=24, height=34.5, depth=0.75, material="3/4\" Plywood", quantity=1),
            CabinetComponent(name="Bottom Panel", width=22.5, height=23.25, depth=0.75, material="3/4\" Plywood", quantity=1),
            CabinetComponent(name="Back Panel", width=22.5, height=34.5, depth=0.25, material="1/4\" Plywood", quantity=1),
            CabinetComponent(name="Face Frame Stile (L)", width=1.5, height=34.5, depth=0.75, material="Hard Maple", quantity=2),
            CabinetComponent(name="Face Frame Stile (R)", width=1.5, height=34.5, depth=0.75, material="Hard Maple", quantity=2),
            CabinetComponent(name="Face Frame Rail", width=21, height=2, depth=0.75, material="Hard Maple", quantity=1),
            CabinetComponent(name="Door Panel", width=13, height=28, depth=0.75, material="Hard Maple", quantity=1),
            CabinetComponent(name="Drawer Box Front", width=18, height=5, depth=0.5, material="1/2\" Plywood", quantity=1),
            CabinetComponent(name="Drawer Box Sides", width=21, height=5, depth=0.5, material="1/2\" Plywood", quantity=2),
            CabinetComponent(name="Drawer Box Back", width=18, height=5, depth=0.5, material="1/2\" Plywood", quantity=1),
            CabinetComponent(name="Drawer Bottom", width=19, height=21, depth=0.25, material="1/4\" Plywood", quantity=1),
        ],
        hardware_needed=[
            {"name": "Soft-close drawer slides", "quantity": 1, "type": "21\" full extension"},
            {"name": "Concealed hinges", "quantity": 2, "type": "Soft-close, 110°"},
            {"name": "Drawer pull", "quantity": 1, "type": "5\" CC"},
            {"name": "Door knob/pull", "quantity": 1, "type": "3\" CC"},
            {"name": "Shelf pins", "quantity": 4, "type": "5mm"},
            {"name": "Toe kick", "quantity": 1, "type": "4\" x 24\""},
        ],
        cut_list=[
            {"sheet": "3/4\" Plywood", "pieces": 4, "waste_pct": 15},
            {"sheet": "1/4\" Plywood", "pieces": 2, "waste_pct": 30},
            {"sheet": "1/2\" Plywood", "pieces": 4, "waste_pct": 25},
            {"lumber": "Hard Maple", "board_feet": 12},
        ],
        joinery=["Pocket holes", "Dado joints", "Rabbet joints"],
        finishing_suggestions=[
            "Sand to 220 grit",
            "Apply pre-stain conditioner",
            "Water-based polyurethane (3 coats)",
            "Consider conversion varnish for durability",
        ],
        tags=["kitchen", "base", "shaker", "beginner", "drawers"],
    ),
    CabinetTemplate(
        id="kitchen-upper-raised",
        name="Raised Panel Wall Cabinet",
        description="Elegant raised panel wall cabinet with crown molding. Inspired by high-end cabinet shops like Decora and KraftMaid.",
        style=CabinetStyle.RAISED_PANEL,
        room_type=RoomType.KITCHEN,
        inspiration=InspirationSource.DECORA,
        inspiration_notes="Premium raised panel profile with elegant detailing",
        difficulty="advanced",
        estimated_hours=16,
        estimated_cost_low=300,
        estimated_cost_high=450,
        components=[
            CabinetComponent(name="Side Panel (Left)", width=12, height=30, depth=0.75, material="3/4\" Plywood", quantity=1),
            CabinetComponent(name="Side Panel (Right)", width=12, height=30, depth=0.75, material="3/4\" Plywood", quantity=1),
            CabinetComponent(name="Top Panel", width=10.5, height=11.25, depth=0.75, material="3/4\" Plywood", quantity=1),
            CabinetComponent(name="Bottom Panel", width=10.5, height=11.25, depth=0.75, material="3/4\" Plywood", quantity=1),
            CabinetComponent(name="Back Panel", width=10.5, height=29.25, depth=0.25, material="1/4\" Plywood", quantity=1),
            CabinetComponent(name="Face Frame", width=11.25, height=29.25, depth=0.75, material="Cherry", quantity=1),
            CabinetComponent(name="Door Rail (Top)", width=10, height=2.5, depth=0.75, material="Cherry", quantity=2),
            CabinetComponent(name="Door Rail (Bottom)", width=10, height=2.5, depth=0.75, material="Cherry", quantity=2),
            CabinetComponent(name="Door Stile", width=2.25, height=27, depth=0.75, material="Cherry", quantity=2),
            CabinetComponent(name="Raised Panel", width=8.5, height=24, depth=0.5, material="Cherry", quantity=1),
            CabinetComponent(name="Crown Molding", width=12, height=3, depth=0.75, material="Cherry", quantity=1),
        ],
        hardware_needed=[
            {"name": "Concealed hinges", "quantity": 2, "type": "Soft-close, 110° overlay"},
            {"name": "Door pull", "quantity": 1, "type": "3\" CC"},
            {"name": "Wall cleat", "quantity": 1, "type": "French cleat system"},
            {"name": "Adjustable shelf pins", "quantity": 4, "type": "5mm brass"},
        ],
        cut_list=[
            {"sheet": "3/4\" Plywood", "pieces": 4, "waste_pct": 20},
            {"sheet": "1/4\" Plywood", "pieces": 1, "waste_pct": 35},
            {"lumber": "Cherry", "board_feet": 18},
        ],
        joinery=["Mortise and tenon", "Cope and stick", "Raised panel"],
        finishing_suggestions=[
            "Sand to 320 grit",
            "Dye stain for depth",
            "Gel stain for uniformity",
            "Conversion varnish (2-3 coats)",
            "Rub out with 0000 steel wool",
        ],
        tags=["kitchen", "upper", "raised-panel", "advanced", "cherry", "premium"],
    ),
    CabinetTemplate(
        id="kitchen-corner-lazy-susan",
        name="Corner Lazy Susan Cabinet",
        description="Optimized corner cabinet with rotating shelves. Maximizes dead corner space. Popularized by Cabinets To Go.",
        style=CabinetStyle.SHAKER,
        room_type=RoomType.KITCHEN,
        inspiration=InspirationSource.CABINETS_TO_GO,
        inspiration_notes="Space-efficient corner solution with dual access",
        difficulty="intermediate",
        estimated_hours=12,
        estimated_cost_low=400,
        estimated_cost_high=600,
        components=[
            CabinetComponent(name="Side Panel (Front L)", width=24, height=34.5, depth=0.75, material="3/4\" Plywood", quantity=1),
            CabinetComponent(name="Side Panel (Front R)", width=24, height=34.5, depth=0.75, material="3/4\" Plywood", quantity=1),
            CabinetComponent(name="Corner Panel", width=34, height=34.5, depth=0.75, material="3/4\" Plywood", quantity=1),
            CabinetComponent(name="Lazy Susan Shelf", width=32, height=32, depth=0.75, material="3/4\" Plywood", quantity=2),
            CabinetComponent(name="Face Frame", width=22, height=34.5, depth=0.75, material="Hard Maple", quantity=2),
        ],
        hardware_needed=[
            {"name": "Lazy Susan hardware", "quantity": 1, "type": "Full rotation, 32\" diameter"},
            {"name": "Door hinges", "quantity": 4, "type": "170° wide opening"},
            {"name": "Door pulls", "quantity": 2, "type": "5\" CC"},
        ],
        cut_list=[
            {"sheet": "3/4\" Plywood", "pieces": 5, "waste_pct": 25},
            {"lumber": "Hard Maple", "board_feet": 8},
        ],
        joinery=["Pocket holes", "Dado joints"],
        finishing_suggestions=[
            "Sand to 220 grit",
            "Apply primer if painting",
            "Two-pack conversion varnish",
        ],
        tags=["kitchen", "corner", "lazy-susan", "space-saver", "intermediate"],
    ),
    CabinetTemplate(
        id="kitchen-tall-pantry",
        name="Tall Pantry Cabinet",
        description="Floor-to-ceiling pantry cabinet with adjustable shelving. Inspired by Jay Bates' storage solutions.",
        style=CabinetStyle.FLAT_PANEL,
        room_type=RoomType.PANTRY,
        inspiration=InspirationSource.JAY_BATES,
        inspiration_notes="Maximum storage efficiency with clean modern lines",
        difficulty="intermediate",
        estimated_hours=14,
        estimated_cost_low=350,
        estimated_cost_high=500,
        components=[
            CabinetComponent(name="Side Panel (Left)", width=18, height=84, depth=0.75, material="3/4\" Plywood", quantity=1),
            CabinetComponent(name="Side Panel (Right)", width=18, height=84, depth=0.75, material="3/4\" Plywood", quantity=1),
            CabinetComponent(name="Top Panel", width=16.5, height=12, depth=0.75, material="3/4\" Plywood", quantity=1),
            CabinetComponent(name="Bottom Panel", width=16.5, height=12, depth=0.75, material="3/4\" Plywood", quantity=1),
            CabinetComponent(name="Back Panel", width=16.5, height=83.25, depth=0.25, material="1/4\" Plywood", quantity=1),
            CabinetComponent(name="Adjustable Shelf", width=15.5, height=11.5, depth=0.75, material="3/4\" Plywood", quantity=6),
            CabinetComponent(name="Face Frame", width=17, height=83.5, depth=0.75, material="Hard Maple", quantity=1),
            CabinetComponent(name="Door Panel", width=15.5, height=81, depth=0.75, material="Hard Maple", quantity=1),
        ],
        hardware_needed=[
            {"name": "Concealed hinges", "quantity": 5, "type": "Soft-close, heavy duty"},
            {"name": "Door pull", "quantity": 1, "type": "8\" appliance pull"},
            {"name": "Shelf pins", "quantity": 24, "type": "5mm brass"},
            {"name": "Anti-tip kit", "quantity": 1, "type": "Wall anchor"},
        ],
        cut_list=[
            {"sheet": "3/4\" Plywood", "pieces": 11, "waste_pct": 15},
            {"sheet": "1/4\" Plywood", "pieces": 1, "waste_pct": 25},
            {"lumber": "Hard Maple", "board_feet": 20},
        ],
        joinery=["Pocket holes", "Dado joints", "Edge banding"],
        finishing_suggestions=[
            "Sand to 220 grit",
            "Tinted polyurethane",
            "Catalyzed lacquer for durability",
        ],
        tags=["pantry", "tall", "storage", "modern", "intermediate"],
    ),
]


# ============================================================================
# BATHROOM/VANITY CABINETS
# ============================================================================

VANITY_TEMPLATES = [
    CabinetTemplate(
        id="vanity-double-sink",
        name="Double Sink Vanity Cabinet",
        description="60\" double sink vanity with soft-close drawers. Modern flat panel design inspired by April Wilkerson's bathroom renovation.",
        style=CabinetStyle.FLAT_PANEL,
        room_type=RoomType.BATHROOM,
        inspiration=InspirationSource.APRIL_WILKERSON,
        inspiration_notes="Clean modern aesthetic with practical storage",
        difficulty="intermediate",
        estimated_hours=20,
        estimated_cost_low=500,
        estimated_cost_high=800,
        components=[
            CabinetComponent(name="Side Panel (Left)", width=21, height=34, depth=0.75, material="3/4\" Baltic Birch", quantity=1),
            CabinetComponent(name="Side Panel (Right)", width=21, height=34, depth=0.75, material="3/4\" Baltic Birch", quantity=1),
            CabinetComponent(name="Center Divider", width=21, height=34, depth=0.75, material="3/4\" Baltic Birch", quantity=1),
            CabinetComponent(name="Bottom Panel", width=58.5, height=21, depth=0.75, material="3/4\" Baltic Birch", quantity=1),
            CabinetComponent(name="Back Panel", width=58.5, height=33.25, depth=0.25, material="1/4\" Plywood", quantity=1),
            CabinetComponent(name="Drawer Bank Divider", width=19, height=12, depth=0.75, material="3/4\" Baltic Birch", quantity=2),
            CabinetComponent(name="Drawer Box Front (Large)", width=27, height=6, depth=0.5, material="1/2\" Baltic Birch", quantity=2),
            CabinetComponent(name="Drawer Box Front (Small)", width=12, height=6, depth=0.5, material="1/2\" Baltic Birch", quantity=4),
            CabinetComponent(name="Door Panel", width=13, height=22, depth=0.75, material="3/4\" Baltic Birch", quantity=4),
        ],
        hardware_needed=[
            {"name": "Soft-close drawer slides", "quantity": 6, "type": "18\" full extension"},
            {"name": "Concealed hinges", "quantity": 8, "type": "Soft-close, 110°"},
            {"name": "Drawer pulls", "quantity": 6, "type": "5\" CC brushed nickel"},
            {"name": "Countertop", "quantity": 1, "type": "Quartz or marble, 60\" x 22\""},
            {"name": "Undermount sinks", "quantity": 2, "type": "Rectangular ceramic"},
            {"name": "Faucets", "quantity": 2, "type": "Centerset"},
        ],
        cut_list=[
            {"sheet": "3/4\" Baltic Birch", "pieces": 12, "waste_pct": 20},
            {"sheet": "1/2\" Baltic Birch", "pieces": 6, "waste_pct": 25},
            {"sheet": "1/4\" Plywood", "pieces": 1, "waste_pct": 30},
        ],
        joinery=["Dado joints", "Pocket holes", "Dovetail drawers"],
        finishing_suggestions=[
            "Sand to 320 grit",
            "Marine-grade polyurethane (moisture resistant)",
            "Consider conversion varnish",
            "Moisture barrier on bottom edges",
        ],
        tags=["bathroom", "vanity", "double-sink", "modern", "drawers"],
    ),
    CabinetTemplate(
        id="vanity-floating",
        name="Floating Vanity Cabinet",
        description="Wall-mounted floating vanity with hidden drawer. Contemporary design inspired by high-end European cabinet makers.",
        style=CabinetStyle.SLAB,
        room_type=RoomType.BATHROOM,
        inspiration=InspirationSource.CUSTOM,
        inspiration_notes="European-inspired minimalist design",
        difficulty="advanced",
        estimated_hours=16,
        estimated_cost_low=400,
        estimated_cost_high=650,
        components=[
            CabinetComponent(name="Side Panel (Left)", width=18, height=18, depth=0.75, material="3/4\" Walnut Plywood", quantity=1),
            CabinetComponent(name="Side Panel (Right)", width=18, height=18, depth=0.75, material="3/4\" Walnut Plywood", quantity=1),
            CabinetComponent(name="Top Panel", width=32, height=17.25, depth=0.75, material="3/4\" Walnut Plywood", quantity=1),
            CabinetComponent(name="Bottom Panel", width=32, height=17.25, depth=0.75, material="3/4\" Walnut Plywood", quantity=1),
            CabinetComponent(name="Back Panel", width=32, height=17.25, depth=0.25, material="1/4\" Plywood", quantity=1),
            CabinetComponent(name="Drawer Front", width=31, height=10, depth=0.75, material="Walnut", quantity=1),
            CabinetComponent(name="Door Panel", width=14, height=16, depth=0.75, material="Walnut", quantity=2),
        ],
        hardware_needed=[
            {"name": "Wall mounting system", "quantity": 1, "type": "Heavy-duty French cleat with ledger"},
            {"name": "Soft-close drawer slides", "quantity": 1, "type": "18\" full extension"},
            {"name": "Push-to-open hinges", "quantity": 4, "type": "Integrated soft-close"},
            {"name": "Countertop", "quantity": 1, "type": "Live edge walnut or quartz"},
        ],
        cut_list=[
            {"sheet": "3/4\" Walnut Plywood", "pieces": 5, "waste_pct": 25},
            {"sheet": "1/4\" Plywood", "pieces": 1, "waste_pct": 40},
            {"lumber": "Walnut", "board_feet": 15},
        ],
        joinery=["Mitered corners", "Pocket holes", "Floating tenons"],
        finishing_suggestions=[
            "Sand to 400 grit",
            "Osmo oil finish for natural look",
            "Multiple coats for water resistance",
        ],
        tags=["bathroom", "vanity", "floating", "modern", "walnut", "minimalist"],
    ),
    CabinetTemplate(
        id="vanity-vessel-sink",
        name="Vessel Sink Vanity Console",
        description="Open console vanity for vessel sinks. Mix of traditional and modern. Inspired by Jon Peters' furniture-style pieces.",
        style=CabinetStyle.OPEN_SHELF,
        room_type=RoomType.BATHROOM,
        inspiration=InspirationSource.JON_PETERS,
        inspiration_notes="Furniture-quality piece with open storage",
        difficulty="advanced",
        estimated_hours=24,
        estimated_cost_low=600,
        estimated_cost_high=900,
        components=[
            CabinetComponent(name="Leg (Front L)", width=3, height=32, depth=3, material="White Oak", quantity=1),
            CabinetComponent(name="Leg (Front R)", width=3, height=32, depth=3, material="White Oak", quantity=1),
            CabinetComponent(name="Leg (Back L)", width=3, height=32, depth=3, material="White Oak", quantity=1),
            CabinetComponent(name="Leg (Back R)", width=3, height=32, depth=3, material="White Oak", quantity=1),
            CabinetComponent(name="Top Apron (Front)", width=36, height=4, depth=0.75, material="White Oak", quantity=1),
            CabinetComponent(name="Side Apron", width=4, height=18, depth=0.75, material="White Oak", quantity=2),
            CabinetComponent(name="Shelf", width=33, height=15, depth=0.75, material="White Oak Plywood", quantity=1),
            CabinetComponent(name="Top Surface", width=36, height=18, depth=1, material="Marble or Quartz", quantity=1),
        ],
        hardware_needed=[
            {"name": "Vessel sink", "quantity": 1, "type": "Ceramic or stone vessel"},
            {"name": "Vessel faucet", "quantity": 1, "type": "Tall vessel faucet"},
            {"name": "Shelf supports", "quantity": 4, "type": "Hidden bracket"},
            {"name": "Levelers", "quantity": 4, "type": "Adjustable feet"},
        ],
        cut_list=[
            {"lumber": "White Oak", "board_feet": 25},
            {"sheet": "White Oak Plywood", "pieces": 1, "waste_pct": 40},
        ],
        joinery=["Mortise and tenon", "Bridle joints", "Floating tenons"],
        finishing_suggestions=[
            "Sand to 320 grit",
            "Danish oil for warmth",
            "Waterlox for water resistance",
            "Wax top coat",
        ],
        tags=["bathroom", "vanity", "vessel-sink", "furniture-style", "open-shelf"],
    ),
]


# ============================================================================
# BOOKSHELVES & STORAGE
# ============================================================================

BOOKSHELF_TEMPLATES = [
    CabinetTemplate(
        id="bookshelf-built-in",
        name="Built-In Bookcase Unit",
        description="Wall-to-wall built-in bookcase with adjustable shelves. Classic design inspired by Marc Spagnuolo (The Wood Whisperer).",
        style=CabinetStyle.RAISED_PANEL,
        room_type=RoomType.LIVING_ROOM,
        inspiration=InspirationSource.MARC_SPIAGNUOLO,
        inspiration_notes="Traditional furniture-quality built-ins with crown and base molding",
        difficulty="advanced",
        estimated_hours=40,
        estimated_cost_low=800,
        estimated_cost_high=1200,
        components=[
            CabinetComponent(name="Side Panel (Left)", width=12, height=84, depth=0.75, material="3/4\" Cherry Plywood", quantity=1),
            CabinetComponent(name="Side Panel (Right)", width=12, height=84, depth=0.75, material="3/4\" Cherry Plywood", quantity=1),
            CabinetComponent(name="Fixed Shelf (Bottom)", width=47.25, height=11.25, depth=0.75, material="3/4\" Cherry Plywood", quantity=1),
            CabinetComponent(name="Fixed Shelf (Mid)", width=47.25, height=11.25, depth=0.75, material="3/4\" Cherry Plywood", quantity=1),
            CabinetComponent(name="Adjustable Shelf", width=46.5, height=11, depth=0.75, material="3/4\" Cherry Plywood", quantity=6),
            CabinetComponent(name="Top Panel", width=47.25, height=11.25, depth=0.75, material="3/4\" Cherry Plywood", quantity=1),
            CabinetComponent(name="Back Panel", width=47.25, height=83.25, depth=0.25, material="1/4\" Cherry Plywood", quantity=1),
            CabinetComponent(name="Face Frame Stile", width=2.25, height=84, depth=0.75, material="Cherry", quantity=2),
            CabinetComponent(name="Face Frame Rail", width=44.5, height=3, depth=0.75, material="Cherry", quantity=3),
            CabinetComponent(name="Crown Molding", width=48, height=5, depth=0.75, material="Cherry", quantity=1),
            CabinetComponent(name="Base Molding", width=48, height=4, depth=0.75, material="Cherry", quantity=1),
        ],
        hardware_needed=[
            {"name": "Shelf pins", "quantity": 48, "type": "5mm brass sleeve"},
            {"name": "Wall anchors", "quantity": 6, "type": "Heavy-duty French cleat"},
            {"name": "Base levelers", "quantity": 4, "type": "Adjustable"},
        ],
        cut_list=[
            {"sheet": "3/4\" Cherry Plywood", "pieces": 12, "waste_pct": 15},
            {"sheet": "1/4\" Cherry Plywood", "pieces": 1, "waste_pct": 20},
            {"lumber": "Cherry", "board_feet": 30},
        ],
        joinery=["Dado joints", "Face frame mortise and tenon", "Biscuit joints"],
        finishing_suggestions=[
            "Sand to 320 grit",
            "Cherry-specific dye for color depth",
            "Gel stain for uniformity",
            "Conversion varnish",
            "Rub out with 0000 steel wool and wax",
        ],
        tags=["bookshelf", "built-in", "living-room", "cherry", "traditional", "advanced"],
    ),
    CabinetTemplate(
        id="bookshelf-modular",
        name="Modular Cube Storage",
        description="Stackable cube shelving system. Modern design inspired by Matt Cremona's precision approach.",
        style=CabinetStyle.FLAT_PANEL,
        room_type=RoomType.LIVING_ROOM,
        inspiration=InspirationSource.MATT_CREMONA,
        inspiration_notes="Precision-cut modular units for flexible configuration",
        difficulty="intermediate",
        estimated_hours=12,
        estimated_cost_low=200,
        estimated_cost_high=350,
        components=[
            CabinetComponent(name="Cube Side (Vertical)", width=15, height=15, depth=0.75, material="3/4\" Baltic Birch", quantity=4),
            CabinetComponent(name="Cube Shelf (Horizontal)", width=14.25, height=14.25, depth=0.75, material="3/4\" Baltic Birch", quantity=2),
            CabinetComponent(name="Back Panel", width=14.25, height=14.25, depth=0.25, material="1/4\" Plywood", quantity=1),
        ],
        hardware_needed=[
            {"name": "Connector bolts", "quantity": 8, "type": "Furniture cam locks"},
            {"name": "Wall anchor", "quantity": 1, "type": "Anti-tip strap"},
            {"name": "Feet", "quantity": 4, "type": "Adjustable leveling"},
        ],
        cut_list=[
            {"sheet": "3/4\" Baltic Birch", "pieces": 6, "waste_pct": 10},
            {"sheet": "1/4\" Plywood", "pieces": 1, "waste_pct": 45},
        ],
        joinery=["Dado joints", "Rabbet joints", "Edge banding"],
        finishing_suggestions=[
            "Sand to 220 grit",
            "Clear water-based polyurethane",
            "Edge banding before finishing",
        ],
        tags=["bookshelf", "modular", "cubes", "modern", "stackable"],
    ),
    CabinetTemplate(
        id="bookshelf-ladder",
        name="Leaning Ladder Shelf",
        description="Modern leaning ladder-style bookshelf. Minimalist design inspired by Frank Howarth's artistic approach.",
        style=CabinetStyle.OPEN_SHELF,
        room_type=RoomType.LIVING_ROOM,
        inspiration=InspirationSource.FRANK_HOWARTH,
        inspiration_notes="Sculptural form meets function",
        difficulty="intermediate",
        estimated_hours=16,
        estimated_cost_low=250,
        estimated_cost_high=400,
        components=[
            CabinetComponent(name="Ladder Rail (Left)", width=3, height=72, depth=1.5, material="White Oak", quantity=1),
            CabinetComponent(name="Ladder Rail (Right)", width=3, height=72, depth=1.5, material="White Oak", quantity=1),
            CabinetComponent(name="Shelf (Top)", width=18, height=10, depth=0.75, material="White Oak", quantity=1),
            CabinetComponent(name="Shelf (Upper-Mid)", width=20, height=12, depth=0.75, material="White Oak", quantity=1),
            CabinetComponent(name="Shelf (Lower-Mid)", width=22, height=14, depth=0.75, material="White Oak", quantity=1),
            CabinetComponent(name="Shelf (Bottom)", width=24, height=16, depth=0.75, material="White Oak", quantity=1),
            CabinetComponent(name="Cross Brace", width=2, height=36, depth=0.75, material="White Oak", quantity=2),
        ],
        hardware_needed=[
            {"name": "Wall anchor", "quantity": 1, "type": "Safety strap"},
            {"name": "Rubber feet", "quantity": 2, "type": "Non-slip floor protectors"},
            {"name": "Shelf supports", "quantity": 8, "type": "Hidden brackets"},
        ],
        cut_list=[
            {"lumber": "White Oak", "board_feet": 35},
        ],
        joinery=["Sliding dovetails", "Through tenons", "Wedges"],
        finishing_suggestions=[
            "Sand to 400 grit",
            "Osmo Polyx-Oil for natural look",
            "Multiple thin coats",
        ],
        tags=["bookshelf", "ladder", "modern", "minimalist", "open-shelf"],
    ),
]


# ============================================================================
# ENTERTAINMENT & OFFICE
# ============================================================================

ENTERTAINMENT_TEMPLATES = [
    CabinetTemplate(
        id="entertainment-center",
        name="Media Console Cabinet",
        description="Low-profile entertainment center with cable management. Clean design inspired by Patrick Sorrell's furniture.",
        style=CabinetStyle.SLAB,
        room_type=RoomType.ENTERTAINMENT,
        inspiration=InspirationSource.PATRICK_SORRELL,
        inspiration_notes="Mid-century modern inspired with practical features",
        difficulty="intermediate",
        estimated_hours=24,
        estimated_cost_low=400,
        estimated_cost_high=650,
        components=[
            CabinetComponent(name="Side Panel (Left)", width=16, height=20, depth=0.75, material="3/4\" Walnut Plywood", quantity=1),
            CabinetComponent(name="Side Panel (Right)", width=16, height=20, depth=0.75, material="3/4\" Walnut Plywood", quantity=1),
            CabinetComponent(name="Bottom Panel", width=70, height=16, depth=0.75, material="3/4\" Walnut Plywood", quantity=1),
            CabinetComponent(name="Top Panel", width=72, height=18, depth=0.75, material="3/4\" Walnut Plywood", quantity=1),
            CabinetComponent(name="Shelf (Adjustable)", width=22, height=15, depth=0.75, material="3/4\" Walnut Plywood", quantity=3),
            CabinetComponent(name="Back Panel", width=70, height=18, depth=0.25, material="1/4\" Plywood", quantity=1),
            CabinetComponent(name="Door Panel", width=22, height=15, depth=0.75, material="Walnut", quantity=3),
            CabinetComponent(name="Drawer Front", width=22, height=5, depth=0.75, material="Walnut", quantity=1),
            CabinetComponent(name="Tapered Leg", width=2, height=8, depth=2, material="Walnut", quantity=4),
        ],
        hardware_needed=[
            {"name": "Soft-close drawer slides", "quantity": 1, "type": "16\" full extension"},
            {"name": "Push-to-open hinges", "quantity": 6, "type": "Soft-close integrated"},
            {"name": "Cable grommets", "quantity": 3, "type": "2\" brush pass-through"},
            {"name": "Vent strips", "quantity": 2, "type": "Louvered"},
            {"name": "Power strip", "quantity": 1, "type": "Surge protector with USB"},
        ],
        cut_list=[
            {"sheet": "3/4\" Walnut Plywood", "pieces": 8, "waste_pct": 15},
            {"sheet": "1/4\" Plywood", "pieces": 1, "waste_pct": 30},
            {"lumber": "Walnut", "board_feet": 12},
        ],
        joinery=["Dado joints", "Pocket holes", "Tapered leg angles"],
        finishing_suggestions=[
            "Sand to 320 grit",
            "Danish oil for warmth",
            "Water-based polyurethane for durability",
        ],
        tags=["entertainment", "media", "console", "modern", "walnut"],
    ),
    CabinetTemplate(
        id="office-desk-built-in",
        name="Built-In Home Office Desk",
        description="Wall-mounted desk with overhead cabinets. Professional workspace inspired by John Heisz's shop projects.",
        style=CabinetStyle.SHAKER,
        room_type=RoomType.OFFICE,
        inspiration=InspirationSource.JOHN_HEISZ,
        inspiration_notes="Functional workspace with integrated storage",
        difficulty="advanced",
        estimated_hours=32,
        estimated_cost_low=600,
        estimated_cost_high=900,
        components=[
            CabinetComponent(name="Desktop", width=60, height=30, depth=1.25, material="Baltic Birch (laminate)", quantity=1),
            CabinetComponent(name="Desk Support Cleat", width=58, height=4, depth=0.75, material="3/4\" Plywood", quantity=1),
            CabinetComponent(name="Drawer Unit Side", width=16, height=12, depth=0.75, material="3/4\" Plywood", quantity=2),
            CabinetComponent(name="Drawer Box", width=14, height=4, depth=0.5, material="1/2\" Baltic Birch", quantity=3),
            CabinetComponent(name="Overhead Cabinet Side", width=12, height=14, depth=0.75, material="3/4\" Plywood", quantity=2),
            CabinetComponent(name="Overhead Shelf", width=28, height=11, depth=0.75, material="3/4\" Plywood", quantity=2),
            CabinetComponent(name="Overhead Door", width=14, height=13, depth=0.75, material="1/2\" Plywood", quantity=2),
        ],
        hardware_needed=[
            {"name": "Soft-close drawer slides", "quantity": 3, "type": "14\" full extension"},
            {"name": "Cabinet hinges", "quantity": 4, "type": "Soft-close overlay"},
            {"name": "Cable management", "quantity": 1, "type": "Desk grommet kit"},
            {"name": "Task lighting", "quantity": 1, "type": "Under-cabinet LED strip"},
            {"name": "Wall mounting", "quantity": 1, "type": "Heavy-duty bracket system"},
        ],
        cut_list=[
            {"sheet": "3/4\" Plywood", "pieces": 10, "waste_pct": 20},
            {"sheet": "1/2\" Baltic Birch", "pieces": 4, "waste_pct": 15},
        ],
        joinery=["Dado joints", "Pocket holes", "French cleat mounting"],
        finishing_suggestions=[
            "Sand to 220 grit",
            "Tinted polyurethane for desk surface",
            "Clear coat for cabinets",
            "Add desk pad for protection",
        ],
        tags=["office", "desk", "built-in", "workspace", "drawers"],
    ),
]


# ============================================================================
# GARAGE & UTILITY
# ============================================================================

UTILITY_TEMPLATES = [
    CabinetTemplate(
        id="garage-storage",
        name="Garage Storage Cabinet",
        description="Heavy-duty garage cabinet with adjustable shelving. Practical design inspired by LexSpeed's workshop builds.",
        style=CabinetStyle.FLAT_PANEL,
        room_type=RoomType.GARAGE,
        inspiration=InspirationSource.LEXSPEED,
        inspiration_notes="Rugged construction for heavy tool storage",
        difficulty="beginner",
        estimated_hours=10,
        estimated_cost_low=200,
        estimated_cost_high=300,
        components=[
            CabinetComponent(name="Side Panel (Left)", width=24, height=72, depth=0.75, material="3/4\" MDF (melamine)", quantity=1),
            CabinetComponent(name="Side Panel (Right)", width=24, height=72, depth=0.75, material="3/4\" MDF (melamine)", quantity=1),
            CabinetComponent(name="Top Panel", width=22.5, height=16, depth=0.75, material="3/4\" MDF (melamine)", quantity=1),
            CabinetComponent(name="Bottom Panel", width=22.5, height=16, depth=0.75, material="3/4\" MDF (melamine)", quantity=1),
            CabinetComponent(name="Back Panel", width=22.5, height=71.25, depth=0.25, material="1/4\" Plywood", quantity=1),
            CabinetComponent(name="Adjustable Shelf", width=21.5, height=15.5, depth=0.75, material="3/4\" MDF (melamine)", quantity=5),
            CabinetComponent(name="Door Panel", width=22, height=34, depth=0.75, material="3/4\" MDF (melamine)", quantity=2),
        ],
        hardware_needed=[
            {"name": "Heavy-duty hinges", "quantity": 4, "type": "3\" steel butt hinges"},
            {"name": "Door handles", "quantity": 2, "type": "Utility pull"},
            {"name": "Shelf pins", "quantity": 24, "type": "Heavy-duty 5mm"},
            {"name": "Levelers", "quantity": 4, "type": "Adjustable feet"},
            {"name": "Hasp and padlock", "quantity": 2, "type": "Security lock"},
        ],
        cut_list=[
            {"sheet": "3/4\" MDF (melamine)", "pieces": 11, "waste_pct": 10},
            {"sheet": "1/4\" Plywood", "pieces": 1, "waste_pct": 25},
        ],
        joinery=["Butt joints with screws", "Confirmat screws", "Edge banding"],
        finishing_suggestions=[
            "Melamine is pre-finished",
            "Apply edge banding to exposed edges",
            "Add door bumper pads",
        ],
        tags=["garage", "storage", "utility", "heavy-duty", "beginner"],
    ),
    CabinetTemplate(
        id="mudroom-locker",
        name="Mudroom Locker System",
        description="Individual cubby lockers for family organization. Inspired by school locker designs with bench seating.",
        style=CabinetStyle.BEADBOARD,
        room_type=RoomType.MUDROOM,
        inspiration=InspirationSource.CUSTOM,
        inspiration_notes="Family-friendly organization solution",
        difficulty="intermediate",
        estimated_hours=20,
        estimated_cost_low=450,
        estimated_cost_high=650,
        components=[
            CabinetComponent(name="Locker Side (End)", width=18, height=72, depth=0.75, material="3/4\" Plywood", quantity=2),
            CabinetComponent(name="Locker Divider", width=18, height=72, depth=0.75, material="3/4\" Plywood", quantity=2),
            CabinetComponent(name="Top Panel", width=72, height=17.25, depth=0.75, material="3/4\" Plywood", quantity=1),
            CabinetComponent(name="Bench Seat", width=72, height=17.25, depth=0.75, material="3/4\" Plywood", quantity=1),
            CabinetComponent(name="Bench Divider", width=17.25, height=17.25, depth=0.75, material="3/4\" Plywood", quantity=2),
            CabinetComponent(name="Hook Rail", width=18, height=6, depth=0.75, material="Poplar", quantity=3),
            CabinetComponent(name="Beadboard Back", width=72, height=72, depth=0.25, material="1/4\" Beadboard", quantity=1),
            CabinetComponent(name="Cubby Shelf", width=17, height=17, depth=0.75, material="3/4\" Plywood", quantity=6),
        ],
        hardware_needed=[
            {"name": "Coat hooks", "quantity": 9, "type": "Double hook, oil-rubbed bronze"},
            {"name": "Bench cushion", "quantity": 1, "type": "72\" x 18\" foam with cover"},
            {"name": "Storage baskets", "quantity": 3, "type": "Woven storage bins"},
            {"name": "Wall anchor", "quantity": 4, "type": "L-bracket for safety"},
        ],
        cut_list=[
            {"sheet": "3/4\" Plywood", "pieces": 15, "waste_pct": 15},
            {"sheet": "1/4\" Beadboard", "pieces": 1, "waste_pct": 10},
            {"lumber": "Poplar", "board_feet": 10},
        ],
        joinery=["Dado joints", "Pocket holes", "Face frame"],
        finishing_suggestions=[
            "Sand to 220 grit",
            "Primer and paint (semi-gloss)",
            "Add durable clear coat on bench",
        ],
        tags=["mudroom", "locker", "organization", "family", "bench"],
    ),
]


# ============================================================================
# LAUNDRY
# ============================================================================

LAUNDRY_TEMPLATES = [
    CabinetTemplate(
        id="laundry-folding",
        name="Laundry Folding Station",
        description="Counter-height folding station with overhead storage. Designed for washer/dryer pair.",
        style=CabinetStyle.SHAKER,
        room_type=RoomType.LAUNDRY,
        inspiration=InspirationSource.CUSTOM,
        inspiration_notes="Efficient laundry workflow design",
        difficulty="intermediate",
        estimated_hours=16,
        estimated_cost_low=350,
        estimated_cost_high=500,
        components=[
            CabinetComponent(name="Side Panel (Left)", width=24, height=36, depth=0.75, material="3/4\" Plywood", quantity=1),
            CabinetComponent(name="Side Panel (Right)", width=24, height=36, depth=0.75, material="3/4\" Plywood", quantity=1),
            CabinetComponent(name="Counter Top", width=60, height=25, depth=1, material="Laminate countertop", quantity=1),
            CabinetComponent(name="Upper Cabinet Side", width=12, height=30, depth=0.75, material="3/4\" Plywood", quantity=2),
            CabinetComponent(name="Upper Shelf", width=28, height=11, depth=0.75, material="3/4\" Plywood", quantity=3),
            CabinetComponent(name="Upper Door", width=14, height=28, depth=0.75, material="1/2\" Plywood", quantity=2),
            CabinetComponent(name="Rod Support", width=4, height=6, depth=0.75, material="Poplar", quantity=2),
        ],
        hardware_needed=[
            {"name": "Folding rod", "quantity": 1, "type": "Stainless steel closet rod"},
            {"name": "Cabinet hinges", "quantity": 4, "type": "Soft-close overlay"},
            {"name": "Shelf pins", "quantity": 16, "type": "5mm"},
            {"name": "Wall cleat", "quantity": 1, "type": "French cleat for uppers"},
        ],
        cut_list=[
            {"sheet": "3/4\" Plywood", "pieces": 10, "waste_pct": 20},
            {"sheet": "1/2\" Plywood", "pieces": 2, "waste_pct": 30},
            {"lumber": "Poplar", "board_feet": 5},
            {"countertop": "Laminate", "pieces": 1},
        ],
        joinery=["Dado joints", "Pocket holes", "Face frame"],
        finishing_suggestions=[
            "Sand to 220 grit",
            "Primer and paint (semi-gloss or satin)",
            "Consider melamine for easy cleaning",
        ],
        tags=["laundry", "folding", "utility", "overhead-storage"],
    ),
]


# ============================================================================
# ALL TEMPLATES COMBINED
# ============================================================================

ALL_TEMPLATES = (
    KITCHEN_TEMPLATES +
    VANITY_TEMPLATES +
    BOOKSHELF_TEMPLATES +
    ENTERTAINMENT_TEMPLATES +
    UTILITY_TEMPLATES +
    LAUNDRY_TEMPLATES
)


# ============================================================================
# API ENDPOINTS
# ============================================================================

@router.get("/", response_model=List[CabinetTemplate])
async def list_templates():
    """List all available cabinet templates."""
    return ALL_TEMPLATES


@router.get("/styles")
async def list_styles():
    """List all available cabinet styles."""
    return [{"value": style.value, "label": style.value.replace("_", " ").title()} 
            for style in CabinetStyle]


@router.get("/rooms")
async def list_rooms():
    """List all available room types."""
    return [{"value": room.value, "label": room.value.replace("_", " ").title()} 
            for room in RoomType]


@router.get("/inspirations")
async def list_inspirations():
    """List all inspiration sources."""
    inspiration_info = {
        InspirationSource.STEVE_RAMSEY: {"name": "Steve Ramsey", "channel": "Woodworking for Mere Mortals", "style": "Beginner-friendly, practical"},
        InspirationSource.APRIL_WILKERSON: {"name": "April Wilkerson", "channel": "Wilkerson Workshop", "style": "Modern, precision"},
        InspirationSource.JON_PETERS: {"name": "Jon Peters", "channel": "Longview Woodcraft", "style": "Furniture-quality, traditional"},
        InspirationSource.MARC_SPIAGNUOLO: {"name": "Marc Spagnuolo", "channel": "The Wood Whisperer", "style": "Fine woodworking, educational"},
        InspirationSource.JAY_BATES: {"name": "Jay Bates", "channel": "Jay Bates Woodworking", "style": "Detailed, practical"},
        InspirationSource.JOHN_HEISZ: {"name": "John Heisz", "channel": "I Build It", "style": "Shop-built, innovative"},
        InspirationSource.MATT_CREMONA: {"name": "Matt Cremona", "channel": "Matt Cremona", "style": "Precision, furniture"},
        InspirationSource.FRANK_HOWARTH: {"name": "Frank Howarth", "channel": "Frank Howarth", "style": "Artistic, sculptural"},
        InspirationSource.PATRICK_SORRELL: {"name": "Patrick Sorrell", "channel": "Sorrell Woodworks", "style": "Mid-century modern"},
        InspirationSource.LEXSPEED: {"name": "LexSpeed", "channel": "LexSpeed", "style": "Workshop, utility"},
        InspirationSource.CABINETS_TO_GO: {"name": "Cabinets To Go", "type": "Manufacturer", "style": "Affordable, practical"},
        InspirationSource.CLIFFSIDE_CABINETS: {"name": "Cliffside Cabinets", "type": "Manufacturer", "style": "Traditional, quality"},
        InspirationSource.BARKER_DOOR: {"name": "Barker Door", "type": "Manufacturer", "style": "RTA, shaker"},
        InspirationSource.CONESTOGA: {"name": "Conestoga", "type": "Manufacturer", "style": "Premium RTA"},
        InspirationSource.DECORA: {"name": "Decora", "type": "Manufacturer", "style": "High-end, custom"},
        InspirationSource.KRAFTMAID: {"name": "KraftMaid", "type": "Manufacturer", "style": "Semi-custom, variety"},
        InspirationSource.CUSTOM: {"name": "Custom Design", "type": "Original", "style": "Unique"},
    }
    return [{"value": src.value, **inspiration_info.get(src, {})} 
            for src in InspirationSource]


@router.get("/room/{room_type}", response_model=List[CabinetTemplate])
async def get_templates_by_room(room_type: RoomType):
    """Get templates filtered by room type."""
    return [t for t in ALL_TEMPLATES if t.room_type == room_type]


@router.get("/style/{style}", response_model=List[CabinetTemplate])
async def get_templates_by_style(style: CabinetStyle):
    """Get templates filtered by cabinet style."""
    return [t for t in ALL_TEMPLATES if t.style == style]


@router.get("/difficulty/{level}", response_model=List[CabinetTemplate])
async def get_templates_by_difficulty(level: str):
    """Get templates filtered by difficulty level."""
    return [t for t in ALL_TEMPLATES if t.difficulty == level.lower()]


@router.get("/{template_id}", response_model=CabinetTemplate)
async def get_template(template_id: str):
    """Get a specific template by ID."""
    for template in ALL_TEMPLATES:
        if template.id == template_id:
            return template
    raise HTTPException(status_code=404, detail="Template not found")


@router.get("/{template_id}/cutlist")
async def get_template_cutlist(template_id: str):
    """Get optimized cut list for a template."""
    template = await get_template(template_id)
    
    # Calculate total material needed
    total_3_4_plywood = sum(c.get("pieces", 0) for c in template.cut_list if "Plywood" in c.get("sheet", ""))
    total_lumber_bf = sum(c.get("board_feet", 0) for c in template.cut_list if "board_feet" in c)
    
    return {
        "template_id": template_id,
        "template_name": template.name,
        "components": template.components,
        "cut_list": template.cut_list,
        "summary": {
            "total_components": len(template.components),
            "estimated_3_4_sheets": total_3_4_plywood // 4 + 1,  # Rough estimate
            "total_lumber_board_feet": total_lumber_bf,
            "estimated_hours": template.estimated_hours,
            "estimated_cost_range": f"${template.estimated_cost_low} - ${template.estimated_cost_high}",
        },
        "hardware_needed": template.hardware_needed,
        "joinery": template.joinery,
        "finishing": template.finishing_suggestions,
    }


@router.get("/{template_id}/materials")
async def get_template_materials(template_id: str):
    """Get materials list with supplier links for a template."""
    template = await get_template(template_id)
    
    materials = []
    for item in template.cut_list:
        if "sheet" in item:
            materials.append({
                "type": "sheet",
                "material": item["sheet"],
                "pieces": item.get("pieces", 0),
                "waste_estimate": item.get("waste_pct", 0),
                "suppliers": {
                    "woodworker_express": f"https://www.woodworkerexpress.com/search?q={item['sheet'].replace(' ', '+').replace('\"', '%22')}",
                    "woodcraft": f"https://www.woodcraft.com/search?q={item['sheet'].replace(' ', '+').replace('\"', '%22')}",
                    "dk_hardware": f"https://www.dkhardware.com/search?q={item['sheet'].replace(' ', '+').replace('\"', '%22')}",
                    "rockler": f"https://www.rockler.com/catalogsearch/result?q={item['sheet'].replace(' ', '+').replace('\"', '%22')}",
                    "home_depot": f"https://www.homedepot.com/s/{item['sheet'].replace(' ', '%20').replace('\"', '%22')}",
                    "mcmaster": f"https://www.mcmaster.com/{item['sheet'].replace(' ', '-')}",
                }
            })
        if "lumber" in item:
            materials.append({
                "type": "lumber",
                "species": item["lumber"],
                "board_feet": item.get("board_feet", 0),
                "suppliers": {
                    "woodworker_express": f"https://www.woodworkerexpress.com/search?q={item['lumber'].replace(' ', '+')}",
                    "woodcraft": f"https://www.woodcraft.com/search?q={item['lumber'].replace(' ', '+')}",
                    "dk_hardware": f"https://www.dkhardware.com/search?q={item['lumber'].replace(' ', '+')}",
                    "rockler": f"https://www.rockler.com/catalogsearch/result?q={item['lumber'].replace(' ', '+')}",
                }
            })
    
    return {
        "template_id": template_id,
        "template_name": template.name,
        "materials": materials,
        "hardware": template.hardware_needed,
    }

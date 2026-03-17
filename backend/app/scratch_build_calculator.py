"""
Scratch-Build Calculator - Phase 5 Feature

Estimates build time and provides tips based on tools owned.
Helps DIYers understand what they can build with their setup.
"""
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum
import math


class Tool(Enum):
    TABLE_SAW = "table_saw"
    MITER_SAW = "miter_saw"
    CIRCULAR_SAW = "circular_saw"
    ROUTER = "router"
    ROUTER_TABLE = "router_table"
    DRILL_PRESS = "drill_press"
    HAND_DRILL = "hand_drill"
    KREG_JIG = "kreg_jig"
    BISCUIT_JOINER = "biscuit_joiner"
    DOMINO = "domino"
    PLANER = "planer"
    JOINTER = "jointer"
    BAND_SAW = "band_saw"
    SCROLL_SAW = "scroll_saw"
    SANDER_ORBITAL = "orbital_sander"
    SANDER_BELT = "belt_sander"
    ROUTER_BITS = "router_bits"
    CLAMPS = "clamps"
    BRAD_NAILER = "brad_nailer"
    FINISH_NAILER = "finish_nailer"


class SkillLevel(Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


@dataclass
class OperationTime:
    """Time estimate for a specific operation"""
    operation: str
    base_time_minutes: float
    tool_specific_time: float
    difficulty: str  # "easy", "moderate", "advanced"
    tips: List[str]
    tool_alternatives: List[str]


@dataclass
class BuildEstimate:
    """Complete build time estimate"""
    total_time_hours: float
    total_time_minutes: float
    operations: List[OperationTime]
    skill_level_required: SkillLevel
    tools_needed: List[Tool]
    tools_missing: List[Tool]
    tool_rental_suggestions: List[Dict[str, Any]]
    tips_for_setup: List[str]
    estimated_setup_time: float
    warnings: List[str]


# Time estimates per operation (base time, varies by tools)
OPERATION_TIMES = {
    "cut_sheet_goods": {
        "base_time": 20,  # minutes per sheet
        "tools": {
            Tool.TABLE_SAW: 0.6,  # 60% of base time
            Tool.CIRCULAR_SAW: 1.0,  # 100% of base time
            Tool.MITER_SAW: 1.2,  # 120% - not ideal for sheets
        },
        "difficulty": "easy",
        "tips": [
            "Use a straightedge guide for circular saw cuts",
            "Score cut line with utility knife to prevent tear-out",
            "Support both sides of the cut to prevent binding"
        ]
    },
    "cut_dimensional_lumber": {
        "base_time": 5,  # minutes per cut
        "tools": {
            Tool.TABLE_SAW: 0.5,
            Tool.MITER_SAW: 0.3,
            Tool.CIRCULAR_SAW: 0.8,
        },
        "difficulty": "easy",
        "tips": [
            "Always cut with good face up on miter saw",
            "Use stop blocks for repeated cuts",
            "Check for square after every few cuts"
        ]
    },
    "rip_cuts": {
        "base_time": 3,
        "tools": {
            Tool.TABLE_SAW: 0.4,
            Tool.CIRCULAR_SAW: 0.9,
            Tool.BAND_SAW: 1.1,
        },
        "difficulty": "moderate",
        "tips": [
            "Use push sticks for narrow rips",
            "Set blade height just above material thickness",
            "Use feather boards for consistent pressure"
        ]
    },
    "cross_cuts": {
        "base_time": 2,
        "tools": {
            Tool.TABLE_SAW: 0.5,
            Tool.MITER_SAW: 0.3,
            Tool.CIRCULAR_SAW: 0.8,
        },
        "difficulty": "easy",
        "tips": [
            "Use a crosscut sled for table saw accuracy",
            "Use stop block for repeatable cuts",
            "Check blade for square periodically"
        ]
    },
    "edge_banding": {
        "base_time": 10,  # per linear foot
        "tools": {
            Tool.ROUTER: 0.6,
            Tool.ROUTER_TABLE: 0.4,
            Tool.HAND_DRILL: 1.5,  # using roller
        },
        "difficulty": "moderate",
        "tips": [
            "Pre-glued banding is easiest for beginners",
            "Trim excess with router and flush-trim bit",
            "Iron temperature: cotton setting for most banding"
        ]
    },
    "dado_cuts": {
        "base_time": 8,
        "tools": {
            Tool.TABLE_SAW: 0.5,
            Tool.ROUTER: 0.7,
            Tool.ROUTER_TABLE: 0.6,
        },
        "difficulty": "moderate",
        "tips": [
            "Test dado width on scrap first",
            "Make multiple light passes rather than one deep cut",
            "Use dado stack if available for cleanest cuts"
        ]
    },
    "rabbet_cuts": {
        "base_time": 5,
        "tools": {
            Tool.TABLE_SAW: 0.5,
            Tool.ROUTER: 0.6,
            Tool.ROUTER_TABLE: 0.4,
        },
        "difficulty": "moderate",
        "tips": [
            "Set fence once and test on scrap",
            "Rabbets on edges should be cut with the good face against fence",
            "Clean up with shoulder plane if needed"
        ]
    },
    "pocket_holes": {
        "base_time": 3,  # per joint
        "tools": {
            Tool.KREG_JIG: 0.3,
            Tool.DRILL_PRESS: 0.5,
            Tool.HAND_DRILL: 0.6,
        },
        "difficulty": "easy",
        "tips": [
            "Set depth collar based on material thickness",
            "Use coarse threads for softwood, fine for hardwood",
            "Clamp pieces together before driving screws"
        ]
    },
    "biscuit_joints": {
        "base_time": 4,
        "tools": {
            Tool.BISCUIT_JOINER: 0.4,
            Tool.DOMINO: 0.3,
            Tool.ROUTER: 1.2,
        },
        "difficulty": "moderate",
        "tips": [
            "Mark center lines on both pieces",
            "Use #20 biscuits for most cabinet work",
            "Apply glue to biscuit, not the slot"
        ]
    },
    "assembly": {
        "base_time": 15,  # per cabinet
        "tools": {
            Tool.CLAMPS: 0.6,
            Tool.BRAD_NAILER: 0.4,
            Tool.KREG_JIG: 0.5,
        },
        "difficulty": "moderate",
        "tips": [
            "Dry fit before gluing",
            "Have all clamps ready before starting",
            "Use cauls to keep panels flat",
            "Square cabinet by measuring diagonals"
        ]
    },
    "sanding": {
        "base_time": 20,  # per cabinet
        "tools": {
            Tool.SANDER_ORBITAL: 0.5,
            Tool.SANDER_BELT: 0.3,
        },
        "difficulty": "easy",
        "tips": [
            "Start with 120 grit, finish with 220",
            "Sand with the grain",
            "Don't press hard - let the sander do the work",
            "Vacuum dust between grits"
        ]
    },
    "finishing": {
        "base_time": 30,  # per cabinet
        "tools": {},
        "difficulty": "moderate",
        "tips": [
            "Sand with 320 before final coat",
            "Apply finish in thin, even coats",
            "Sand between coats with 320 grit",
            "Allow proper drying time between coats"
        ]
    },
    "hardware_installation": {
        "base_time": 20,  # per cabinet
        "tools": {
            Tool.HAND_DRILL: 0.5,
            Tool.DRILL_PRESS: 0.3,
        },
        "difficulty": "moderate",
        "tips": [
            "Use a jig for consistent hinge placement",
            "Pre-drill all screw holes",
            "Install drawer slides before assembling face frame",
            "Check door alignment before final tightening"
        ]
    }
}

# Tool rental suggestions
TOOL_RENTALS = {
    Tool.TABLE_SAW: {"daily_cost": 75, "weekly_cost": 250, "where": "Home Depot, local tool rental"},
    Tool.ROUTER: {"daily_cost": 35, "weekly_cost": 120, "where": "Home Depot, local tool rental"},
    Tool.PLANER: {"daily_cost": 60, "weekly_cost": 200, "where": "Home Depot, local tool rental"},
    Tool.JOINTER: {"daily_cost": 65, "weekly_cost": 220, "where": "Local tool rental"},
    Tool.KREG_JIG: {"daily_cost": 15, "weekly_cost": 50, "where": "Home Depot, Amazon"},
    Tool.BISCUIT_JOINER: {"daily_cost": 40, "weekly_cost": 140, "where": "Home Depot, local tool rental"},
}

# Skill level time multipliers
SKILL_MULTIPLIERS = {
    SkillLevel.BEGINNER: 1.5,  # 50% more time
    SkillLevel.INTERMEDIATE: 1.0,  # base time
    SkillLevel.ADVANCED: 0.75,  # 25% less time
}


def get_operation_time(operation: str, tools_available: List[Tool], skill_level: SkillLevel) -> OperationTime:
    """Calculate time for a specific operation based on tools and skill"""
    op_data = OPERATION_TIMES.get(operation)
    if not op_data:
        return OperationTime(
            operation=operation,
            base_time_minutes=10,
            tool_specific_time=10,
            difficulty="moderate",
            tips=[],
            tool_alternatives=[]
        )
    
    base_time = op_data["base_time"]
    tool_times = op_data.get("tools", {})
    
    # Find best available tool for this operation
    best_tool = None
    best_multiplier = 1.5  # default (manual/slower method)
    
    for tool, multiplier in tool_times.items():
        if tool in tools_available and multiplier < best_multiplier:
            best_tool = tool
            best_multiplier = multiplier
    
    tool_specific_time = base_time * best_multiplier
    
    # Apply skill multiplier
    skill_multiplier = SKILL_MULTIPLIERS.get(skill_level, 1.0)
    tool_specific_time *= skill_multiplier
    
    # Get alternatives
    alternatives = [t.value for t in tool_times.keys() if t not in tools_available]
    
    return OperationTime(
        operation=operation,
        base_time_minutes=base_time,
        tool_specific_time=round(tool_specific_time, 1),
        difficulty=op_data["difficulty"],
        tips=op_data["tips"],
        tool_alternatives=alternatives
    )


def estimate_build_time(
    cabinet_design: Dict[str, Any],
    tools_owned: List[str],
    skill_level: str = "intermediate"
) -> BuildEstimate:
    """
    Estimate build time for a cabinet design based on available tools.
    
    Args:
        cabinet_design: Cabinet dimensions and features
        tools_owned: List of tool names the user owns
        skill_level: User's skill level (beginner/intermediate/advanced)
    
    Returns:
        BuildEstimate with time breakdown and suggestions
    """
    # Parse tools
    tools_available = []
    for tool_name in tools_owned:
        try:
            tools_available.append(Tool(tool_name.lower().replace(" ", "_")))
        except ValueError:
            continue
    
    skill = SkillLevel(skill_level.lower())
    
    # Determine required operations based on cabinet design
    operations_needed = []
    
    # Basic cabinet always needs these
    operations_needed.extend([
        "cut_sheet_goods",
        "cross_cuts",
        "assembly",
        "sanding",
        "hardware_installation"
    ])
    
    # Additional operations based on design features
    features = cabinet_design.get("features", {})
    
    if features.get("edge_banding", False):
        operations_needed.append("edge_banding")
    
    if features.get("joinery_type") == "pocket_hole":
        operations_needed.append("pocket_holes")
    elif features.get("joinery_type") == "biscuit":
        operations_needed.append("biscuit_joints")
    elif features.get("joinery_type") == "dado":
        operations_needed.append("dado_cuts")
    
    if features.get("has_face_frame", False):
        operations_needed.extend(["rip_cuts", "pocket_holes"])
    
    if features.get("has_doors", False):
        operations_needed.extend(["rip_cuts", "edge_banding"])
    
    if features.get("has_drawers", False):
        operations_needed.append("dado_cuts")
    
    if cabinet_design.get("finish_required", True):
        operations_needed.append("finishing")
    
    # Calculate time for each operation
    operation_times = []
    total_time = 0
    tools_needed = set()
    tools_missing = set()
    
    for op in operations_needed:
        op_time = get_operation_time(op, tools_available, skill)
        operation_times.append(op_time)
        total_time += op_time.tool_specific_time
        
        # Track tool requirements
        op_data = OPERATION_TIMES.get(op, {})
        for tool in op_data.get("tools", {}).keys():
            tools_needed.add(tool)
            if tool not in tools_available:
                tools_missing.add(tool)
    
    # Generate tool rental suggestions
    rental_suggestions = []
    for tool in tools_missing:
        if tool in TOOL_RENTALS:
            rental = TOOL_RENTALS[tool]
            rental_suggestions.append({
                "tool": tool.value,
                "daily_cost": rental["daily_cost"],
                "weekly_cost": rental["weekly_cost"],
                "where_to_rent": rental["where"]
            })
    
    # Generate setup tips
    setup_tips = [
        "Organize your workspace before starting",
        "Gather all materials and hardware",
        "Check that all tools are in good working order",
        "Set up a cutting station with adequate support",
        "Prepare a finishing area with good ventilation"
    ]
    
    # Calculate setup time (estimate based on project complexity)
    setup_time = 15 + (len(operations_needed) * 3)
    
    # Generate warnings
    warnings = []
    if Tool.TABLE_SAW not in tools_available and Tool.CIRCULAR_SAW not in tools_available:
        warnings.append("No saw detected - you'll need at least a circular saw for sheet goods")
    
    if features.get("joinery_type") == "pocket_hole" and Tool.KREG_JIG not in tools_available:
        warnings.append("Pocket hole joinery requires a Kreg Jig or similar pocket hole jig")
    
    if features.get("edge_banding", False) and Tool.ROUTER not in tools_available:
        warnings.append("Edge banding is much easier with a router and flush-trim bit")
    
    if skill == SkillLevel.BEGINNER and features.get("joinery_type") == "dado":
        warnings.append("Dado joinery is advanced - consider pocket holes for easier assembly")
    
    return BuildEstimate(
        total_time_hours=round(total_time / 60, 1),
        total_time_minutes=round(total_time, 0),
        operations=operation_times,
        skill_level_required=skill,
        tools_needed=list(tools_needed),
        tools_missing=list(tools_missing),
        tool_rental_suggestions=rental_suggestions,
        tips_for_setup=setup_tips,
        estimated_setup_time=setup_time,
        warnings=warnings
    )


def get_tool_requirements(cabinet_type: str, features: Dict[str, bool]) -> Dict[str, Any]:
    """Get minimum and recommended tools for a cabinet project"""
    
    minimum_tools = [
        Tool.CIRCULAR_SAW,
        Tool.HAND_DRILL,
        Tool.SANDER_ORBITAL,
        Tool.CLAMPS,
    ]
    
    recommended_tools = [
        Tool.TABLE_SAW,
        Tool.MITER_SAW,
        Tool.ROUTER,
        Tool.KREG_JIG,
        Tool.BRAD_NAILER,
        Tool.SANDER_ORBITAL,
        Tool.CLAMPS,
    ]
    
    # Add specific tools based on features
    if features.get("edge_banding", False):
        minimum_tools.append(Tool.ROUTER)
        recommended_tools.append(Tool.ROUTER_TABLE)
    
    if features.get("joinery_type") == "pocket_hole":
        minimum_tools.append(Tool.KREG_JIG)
    
    if features.get("joinery_type") == "biscuit":
        minimum_tools.append(Tool.BISCUIT_JOINER)
    
    if features.get("has_drawers", True):
        recommended_tools.append(Tool.TABLE_SAW)  # For dados
    
    return {
        "minimum_tools": [t.value for t in set(minimum_tools)],
        "recommended_tools": [t.value for t in set(recommended_tools)],
        "nice_to_have": [t.value for t in [Tool.PLANER, Tool.JOINTER, Tool.DOMINO, Tool.DRILL_PRESS] if t not in minimum_tools]
    }


def suggest_technique_alternatives(desired_technique: str, tools_owned: List[str]) -> Dict[str, Any]:
    """Suggest alternative techniques based on available tools"""
    
    alternatives = {
        "dado_joints": {
            "preferred_tools": ["table_saw", "router"],
            "alternatives": [
                {
                    "technique": "rabbet_joints",
                    "tools_needed": ["circular_saw", "hand_drill"],
                    "difficulty": "easier",
                    "notes": "Easier to cut but less strength than dado"
                },
                {
                    "technique": "pocket_holes",
                    "tools_needed": ["kreg_jig", "hand_drill"],
                    "difficulty": "easier",
                    "notes": "Fast assembly, visible screws inside cabinet"
                }
            ]
        },
        "edge_banding": {
            "preferred_tools": ["router"],
            "alternatives": [
                {
                    "technique": "iron_on_banding",
                    "tools_needed": ["clothes_iron"],
                    "difficulty": "same",
                    "notes": "Pre-glued banding, trim with utility knife"
                },
                {
                    "technique": "solid_wood_edge",
                    "tools_needed": ["table_saw", "clamps"],
                    "difficulty": "harder",
                    "notes": "More durable but requires more skill"
                }
            ]
        },
        "face_frame": {
            "preferred_tools": ["table_saw", "kreg_jig"],
            "alternatives": [
                {
                    "technique": "frameless_cabinet",
                    "tools_needed": ["circular_saw"],
                    "difficulty": "easier",
                    "notes": "Modern look, easier to build"
                }
            ]
        },
        "soft_close_hardware": {
            "preferred_tools": ["hand_drill"],
            "alternatives": [
                {
                    "technique": "standard_hardware",
                    "tools_needed": ["hand_drill"],
                    "difficulty": "same",
                    "notes": "Less expensive, no soft-close feature"
                }
            ]
        }
    }
    
    return alternatives.get(desired_technique, {
        "preferred_tools": [],
        "alternatives": []
    })

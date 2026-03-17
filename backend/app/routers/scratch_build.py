"""
Scratch-Build Calculator API
Enter tools you own, get time estimates and tips specific to your setup
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime
import uuid

router = APIRouter()

# Tool database with time multipliers
TOOLS_DB = {
    # Cutting Tools
    "table_saw": {
        "name": "Table Saw",
        "category": "cutting",
        "time_multiplier": 0.7,  # 30% faster than base
        "required_for": ["rip_cuts", "cross_cuts", "sheet_goods"],
        "alternatives": ["circular_saw", "track_saw"],
        "skill_level": "intermediate"
    },
    "circular_saw": {
        "name": "Circular Saw",
        "category": "cutting",
        "time_multiplier": 1.0,  # Base time
        "required_for": ["rip_cuts", "cross_cuts", "sheet_goods"],
        "alternatives": ["table_saw", "track_saw"],
        "skill_level": "beginner"
    },
    "track_saw": {
        "name": "Track Saw",
        "category": "cutting",
        "time_multiplier": 0.8,
        "required_for": ["sheet_goods", "precise_cuts"],
        "alternatives": ["table_saw", "circular_saw"],
        "skill_level": "intermediate"
    },
    "miter_saw": {
        "name": "Miter Saw",
        "category": "cutting",
        "time_multiplier": 0.6,
        "required_for": ["cross_cuts", "angle_cuts", "trim"],
        "alternatives": ["circular_saw", "table_saw"],
        "skill_level": "beginner"
    },
    "jigsaw": {
        "name": "Jigsaw",
        "category": "cutting",
        "time_multiplier": 1.5,
        "required_for": ["curved_cuts", "notches", "cutouts"],
        "alternatives": ["bandsaw", "coping_saw"],
        "skill_level": "beginner"
    },
    "bandsaw": {
        "name": "Bandsaw",
        "category": "cutting",
        "time_multiplier": 1.0,
        "required_for": ["curved_cuts", "resawing", "thick_stock"],
        "alternatives": ["jigsaw"],
        "skill_level": "intermediate"
    },
    
    # Joinery Tools
    "kreg_jig": {
        "name": "Kreg Jig (Pocket Hole)",
        "category": "joinery",
        "time_multiplier": 0.5,
        "required_for": ["face_frames", "cabinet_boxes", "drawers"],
        "alternatives": ["biscuit_joiner", "domino"],
        "skill_level": "beginner"
    },
    "biscuit_joiner": {
        "name": "Biscuit Joiner",
        "category": "joinery",
        "time_multiplier": 0.7,
        "required_for": ["panel_glue_ups", "face_frames"],
        "alternatives": ["kreg_jig", "domino"],
        "skill_level": "intermediate"
    },
    "domino": {
        "name": "Festool Domino",
        "category": "joinery",
        "time_multiplier": 0.4,
        "required_for": ["mortise_tenon", "face_frames", "cabinet_boxes"],
        "alternatives": ["kreg_jig", "biscuit_joiner"],
        "skill_level": "advanced"
    },
    "router": {
        "name": "Router",
        "category": "joinery",
        "time_multiplier": 0.8,
        "required_for": ["edge_profiles", "dadoes", "rabbets", "dovetails"],
        "alternatives": ["router_table"],
        "skill_level": "intermediate"
    },
    "router_table": {
        "name": "Router Table",
        "category": "joinery",
        "time_multiplier": 0.7,
        "required_for": ["edge_profiles", "raised_panels", "dadoes"],
        "alternatives": ["router"],
        "skill_level": "intermediate"
    },
    
    # Assembly Tools
    "drill": {
        "name": "Drill/Driver",
        "category": "assembly",
        "time_multiplier": 0.8,
        "required_for": ["assembly", "hinges", "hardware"],
        "alternatives": ["impact_driver"],
        "skill_level": "beginner"
    },
    "impact_driver": {
        "name": "Impact Driver",
        "category": "assembly",
        "time_multiplier": 0.6,
        "required_for": ["assembly", "long_screws"],
        "alternatives": ["drill"],
        "skill_level": "beginner"
    },
    "brad_nailer": {
        "name": "Brad Nailer",
        "category": "assembly",
        "time_multiplier": 0.5,
        "required_for": ["assembly", "trim", "back_panels"],
        "alternatives": ["hammer", "finish_nailer"],
        "skill_level": "beginner"
    },
    "finish_nailer": {
        "name": "Finish Nailer",
        "category": "assembly",
        "time_multiplier": 0.5,
        "required_for": ["assembly", "trim", "face_frames"],
        "alternatives": ["brad_nailer", "hammer"],
        "skill_level": "beginner"
    },
    
    # Finishing Tools
    "orbital_sander": {
        "name": "Orbital Sander",
        "category": "finishing",
        "time_multiplier": 0.7,
        "required_for": ["sanding", "prep_finish"],
        "alternatives": ["belt_sander", "hand_sanding"],
        "skill_level": "beginner"
    },
    "belt_sander": {
        "name": "Belt Sander",
        "category": "finishing",
        "time_multiplier": 0.5,
        "required_for": ["heavy_material_removal", "flattening"],
        "alternatives": ["orbital_sander"],
        "skill_level": "intermediate"
    },
    
    # Measuring & Layout
    "tape_measure": {
        "name": "Tape Measure",
        "category": "layout",
        "time_multiplier": 1.0,
        "required_for": ["all_projects"],
        "alternatives": [],
        "skill_level": "beginner"
    },
    "square": {
        "name": "Speed Square / Framing Square",
        "category": "layout",
        "time_multiplier": 0.9,
        "required_for": ["marking_cuts", "checking_square"],
        "alternatives": [],
        "skill_level": "beginner"
    },
    "clamp_set": {
        "name": "Clamp Set (Various)",
        "category": "assembly",
        "time_multiplier": 0.8,
        "required_for": ["glue_ups", "assembly"],
        "alternatives": [],
        "skill_level": "beginner"
    }
}

# Project type base times (in hours)
PROJECT_BASE_TIMES = {
    "base_cabinet": {"cutting": 2, "joinery": 1.5, "assembly": 1, "finishing": 1, "total": 5.5},
    "wall_cabinet": {"cutting": 1.5, "joinery": 1, "assembly": 0.75, "finishing": 0.75, "total": 4},
    "tall_cabinet": {"cutting": 2.5, "joinery": 2, "assembly": 1.5, "finishing": 1.5, "total": 7.5},
    "bookshelf": {"cutting": 1.5, "joinery": 1, "assembly": 1, "finishing": 1, "total": 4.5},
    "vanity": {"cutting": 2, "joinery": 1.5, "assembly": 1.5, "finishing": 1.5, "total": 6.5},
    "garage_cabinet": {"cutting": 2, "joinery": 1, "assembly": 1, "finishing": 0.5, "total": 4.5},
}

class UserTools(BaseModel):
    tools: List[str]
    skill_level: str = "beginner"  # beginner, intermediate, advanced

class TimeEstimate(BaseModel):
    phase: str
    base_hours: float
    adjusted_hours: float
    efficiency: str
    tips: List[str]

class ProjectEstimate(BaseModel):
    project_type: str
    total_base_hours: float
    total_adjusted_hours: float
    phases: List[TimeEstimate]
    missing_tools: List[Dict[str, Any]]
    recommendations: List[str]

class ToolInventory(BaseModel):
    user_id: str
    tools: List[str]
    skill_level: str

# In-memory storage
user_inventories: Dict[str, Dict] = {}

@router.get("/tools")
async def list_all_tools() -> List[Dict[str, Any]]:
    """List all available tools with details"""
    return [
        {"id": tool_id, **tool_data}
        for tool_id, tool_data in TOOLS_DB.items()
    ]

@router.get("/tools/categories")
async def list_tool_categories() -> List[Dict[str, str]]:
    """List all tool categories"""
    categories = set(t["category"] for t in TOOLS_DB.values())
    return [{"name": cat, "description": f"{cat.title()} tools"} for cat in categories]

@router.get("/tools/{tool_id}")
async def get_tool(tool_id: str) -> Dict[str, Any]:
    """Get details for a specific tool"""
    if tool_id not in TOOLS_DB:
        raise HTTPException(status_code=404, detail="Tool not found")
    return {"id": tool_id, **TOOLS_DB[tool_id]}

@router.post("/inventory")
async def save_tool_inventory(tools: UserTools) -> Dict[str, Any]:
    """Save user's tool inventory"""
    user_id = f"user_{uuid.uuid4().hex[:8]}"
    
    # Validate tools
    invalid_tools = [t for t in tools.tools if t not in TOOLS_DB]
    if invalid_tools:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid tools: {invalid_tools}"
        )
    
    user_inventories[user_id] = {
        "user_id": user_id,
        "tools": tools.tools,
        "skill_level": tools.skill_level,
        "created_at": datetime.utcnow().isoformat()
    }
    
    return {
        "user_id": user_id,
        "tools": tools.tools,
        "skill_level": tools.skill_level,
        "message": "Tool inventory saved"
    }

@router.get("/inventory/{user_id}")
async def get_tool_inventory(user_id: str) -> Dict[str, Any]:
    """Get user's tool inventory"""
    if user_id not in user_inventories:
        raise HTTPException(status_code=404, detail="User inventory not found")
    return user_inventories[user_id]

@router.post("/estimate/{project_type}")
async def estimate_project_time(
    project_type: str,
    tools: UserTools
) -> ProjectEstimate:
    """
    Estimate time to build a project based on tools owned.
    """
    if project_type not in PROJECT_BASE_TIMES:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown project type. Available: {list(PROJECT_BASE_TIMES.keys())}"
        )
    
    base_times = PROJECT_BASE_TIMES[project_type]
    
    # Calculate adjusted times
    phases = []
    total_adjusted = 0
    
    for phase in ["cutting", "joinery", "assembly", "finishing"]:
        base_hours = base_times.get(phase, 1)
        
        # Find best tool for phase
        phase_tools = [t for t in tools.tools if TOOLS_DB.get(t, {}).get("category") == phase]
        
        if phase_tools:
            # Use the best (lowest multiplier) tool
            best_multiplier = min(TOOLS_DB[t]["time_multiplier"] for t in phase_tools)
            adjusted = base_hours * best_multiplier
            efficiency = "Optimal" if best_multiplier < 0.7 else "Good" if best_multiplier < 1.0 else "Standard"
        else:
            # No tools for this phase - add time penalty
            adjusted = base_hours * 1.5
            efficiency = "Manual/Slower"
        
        # Skill level adjustment
        skill_multipliers = {"beginner": 1.3, "intermediate": 1.0, "advanced": 0.8}
        adjusted *= skill_multipliers.get(tools.skill_level, 1.0)
        
        # Generate tips
        tips = generate_phase_tips(phase, phase_tools, tools.skill_level)
        
        phases.append(TimeEstimate(
            phase=phase.title(),
            base_hours=base_hours,
            adjusted_hours=round(adjusted, 1),
            efficiency=efficiency,
            tips=tips
        ))
        total_adjusted += adjusted
    
    # Find missing essential tools
    missing_tools = find_missing_tools(project_type, tools.tools)
    
    # Generate recommendations
    recommendations = generate_recommendations(project_type, tools.tools, tools.skill_level)
    
    return ProjectEstimate(
        project_type=project_type,
        total_base_hours=base_times["total"],
        total_adjusted_hours=round(total_adjusted, 1),
        phases=phases,
        missing_tools=missing_tools,
        recommendations=recommendations
    )

@router.post("/rental-suggestions/{project_type}")
async def suggest_rentals(
    project_type: str,
    tools: UserTools
) -> Dict[str, Any]:
    """
    Suggest tools to rent for a project.
    """
    missing = find_missing_tools(project_type, tools.tools)
    
    # Filter to tools worth renting (high impact tools)
    rental_worthy = [
        {
            **tool,
            "rental_recommendation": get_rental_recommendation(tool["id"])
        }
        for tool in missing
        if tool.get("time_impact", 1) > 1.2  # Significant time impact
    ]
    
    return {
        "project_type": project_type,
        "tools_you_own": tools.tools,
        "suggested_rentals": rental_worthy,
        "rental_cost_estimate": sum(r.get("rental_recommendation", {}).get("daily_cost", 0) for r in rental_worthy),
        "time_saved_hours": sum(
            PROJECT_BASE_TIMES[project_type].get("total", 5) * (r.get("time_impact", 1) - 1)
            for r in rental_worthy
        )
    }

def generate_phase_tips(phase: str, available_tools: List[str], skill_level: str) -> List[str]:
    """Generate tips for each phase based on available tools"""
    tips = []
    
    if phase == "cutting":
        if "table_saw" in available_tools:
            tips.append("Use a featherboard for safer, more accurate rip cuts")
            tips.append("Consider a crosscut sled for better crosscuts")
        elif "circular_saw" in available_tools:
            tips.append("Use a straightedge guide for straight cuts")
            tips.append("Support sheet goods fully to prevent binding")
        if skill_level == "beginner":
            tips.append("Measure twice, cut once - double-check all measurements")
            
    elif phase == "joinery":
        if "kreg_jig" in available_tools:
            tips.append("Pre-drill pocket holes to prevent splitting")
            tips.append("Use face clamps for alignment")
        elif "router" in available_tools:
            tips.append("Practice on scrap before cutting dados")
        if skill_level == "beginner":
            tips.append("Start with pocket hole joinery - easiest for beginners")
            
    elif phase == "assembly":
        if "brad_nailer" in available_tools or "finish_nailer" in available_tools:
            tips.append("Pre-drill for brads to prevent splitting")
        tips.append("Dry-fit before gluing")
        tips.append("Use clamps generously for strong glue joints")
        
    elif phase == "finishing":
        if "orbital_sander" in available_tools:
            tips.append("Sand progressively: 80 → 120 → 180 → 220 grit")
            tips.append("Don't skip grits - it shows in the finish")
        tips.append("Apply finish in a dust-free environment")
        tips.append("Test finish on scrap first")
    
    return tips

def find_missing_tools(project_type: str, owned_tools: List[str]) -> List[Dict[str, Any]]:
    """Find tools that would help but aren't owned"""
    essential_phases = {
        "cutting": ["table_saw", "circular_saw", "miter_saw"],
        "joinery": ["kreg_jig", "router"],
        "assembly": ["drill", "impact_driver", "clamp_set"],
        "finishing": ["orbital_sander"]
    }
    
    missing = []
    for phase, tools in essential_phases.items():
        has_phase_tool = any(t in owned_tools for t in tools)
        if not has_phase_tool:
            best_tool = tools[0]  # Recommend first option
            missing.append({
                "id": best_tool,
                "name": TOOLS_DB[best_tool]["name"],
                "category": phase,
                "reason": f"No {phase} tool - this will slow you down",
                "time_impact": 1.5,
                "alternatives": TOOLS_DB[best_tool]["alternatives"]
            })
    
    return missing

def generate_recommendations(project_type: str, tools: List[str], skill_level: str) -> List[str]:
    """Generate personalized recommendations"""
    recs = []
    
    # Skill-based recommendations
    if skill_level == "beginner":
        recs.append("Start with pocket hole joinery - it's beginner-friendly")
        recs.append("Consider a pre-cut plywood kit for your first project")
        recs.append("Watch tutorial videos before starting each phase")
    elif skill_level == "intermediate":
        recs.append("You have the basics - consider upgrading your saw blade")
        recs.append("Try adding dados for stronger cabinet construction")
    else:
        recs.append("Consider CNC cutting for complex projects")
        recs.append("Domino joinery would speed up your workflow")
    
    # Tool-specific recommendations
    if "kreg_jig" not in tools and skill_level == "beginner":
        recs.append("A Kreg jig is a great investment for beginners - $40 well spent")
    
    if "table_saw" not in tools and "circular_saw" in tools:
        recs.append("A track saw attachment would improve your circular saw cuts")
    
    # Project-specific recommendations
    if project_type in ["base_cabinet", "wall_cabinet"]:
        recs.append("Build a simple cabinet first to practice techniques")
        recs.append("Consider buying pre-made doors for your first project")
    
    return recs

def get_rental_recommendation(tool_id: str) -> Dict[str, Any]:
    """Get rental info for a tool"""
    rental_info = {
        "table_saw": {"daily_cost": 45, "weekly_cost": 150, "store": "Home Depot"},
        "track_saw": {"daily_cost": 35, "weekly_cost": 120, "store": "Home Depot"},
        "router": {"daily_cost": 25, "weekly_cost": 85, "store": "Home Depot"},
        "router_table": {"daily_cost": 30, "weekly_cost": 100, "store": "Home Depot"},
        "brad_nailer": {"daily_cost": 20, "weekly_cost": 70, "store": "Home Depot"},
        "finish_nailer": {"daily_cost": 25, "weekly_cost": 85, "store": "Home Depot"},
        "orbital_sander": {"daily_cost": 15, "weekly_cost": 50, "store": "Home Depot"},
    }
    return rental_info.get(tool_id, {"daily_cost": 30, "weekly_cost": 100, "store": "Home Depot"})

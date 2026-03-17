"""
Best Bang for Your Buck Report - Phase 5 Feature

Analyzes cabinet designs and suggests cost-saving alternatives while
maintaining quality. Provides cost/quality tradeoff analysis.
"""
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum
import math


class MaterialTier(Enum):
    BUDGET = "budget"
    STANDARD = "standard"
    PREMIUM = "premium"


class QualityScore(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    PREMIUM = 4


@dataclass
class MaterialAlternative:
    """Alternative material suggestion with cost/quality analysis"""
    original: str
    alternative: str
    original_cost: float
    alternative_cost: float
    savings: float
    savings_percent: float
    quality_impact: str  # "minimal", "moderate", "significant"
    tradeoff_notes: List[str]
    recommended: bool


@dataclass
class HardwareAlternative:
    """Alternative hardware suggestion"""
    original: str
    alternative: str
    original_cost: float
    alternative_cost: float
    savings: float
    quality_impact: str
    recommended: bool


@dataclass
class SavingsReport:
    """Complete savings analysis report"""
    total_original_cost: float
    total_optimized_cost: float
    total_savings: float
    savings_percent: float
    material_alternatives: List[MaterialAlternative]
    hardware_alternatives: List[HardwareAlternative]
    bulk_purchase_suggestions: List[Dict[str, Any]]
    quality_score_original: int
    quality_score_optimized: int


# Material cost database (per sq ft)
MATERIAL_COSTS = {
    # Plywood grades
    "baltic_birch_plywood": {"cost": 8.50, "tier": MaterialTier.PREMIUM, "quality": QualityScore.PREMIUM},
    "birch_plywood": {"cost": 6.00, "tier": MaterialTier.STANDARD, "quality": QualityScore.HIGH},
    "oak_plywood": {"cost": 7.00, "tier": MaterialTier.STANDARD, "quality": QualityScore.HIGH},
    "maple_plywood": {"cost": 7.50, "tier": MaterialTier.STANDARD, "quality": QualityScore.HIGH},
    "cherry_plywood": {"cost": 9.00, "tier": MaterialTier.PREMIUM, "quality": QualityScore.PREMIUM},
    "walnut_plywood": {"cost": 12.00, "tier": MaterialTier.PREMIUM, "quality": QualityScore.PREMIUM},
    "pine_plywood": {"cost": 4.00, "tier": MaterialTier.BUDGET, "quality": QualityScore.MEDIUM},
    "cdx_plywood": {"cost": 2.50, "tier": MaterialTier.BUDGET, "quality": QualityScore.LOW},
    
    # MDF variants
    "mdf_standard": {"cost": 2.00, "tier": MaterialTier.BUDGET, "quality": QualityScore.MEDIUM},
    "mdf_moisture_resistant": {"cost": 2.75, "tier": MaterialTier.BUDGET, "quality": QualityScore.MEDIUM},
    "mdf_veneered": {"cost": 5.00, "tier": MaterialTier.STANDARD, "quality": QualityScore.HIGH},
    
    # Particle board
    "particle_board": {"cost": 1.50, "tier": MaterialTier.BUDGET, "quality": QualityScore.LOW},
    "particle_board_melamine": {"cost": 2.25, "tier": MaterialTier.BUDGET, "quality": QualityScore.MEDIUM},
    
    # Hardwood (per board foot, converted to sq ft equivalent for comparison)
    "oak_hardwood": {"cost": 8.00, "tier": MaterialTier.PREMIUM, "quality": QualityScore.PREMIUM},
    "maple_hardwood": {"cost": 9.00, "tier": MaterialTier.PREMIUM, "quality": QualityScore.PREMIUM},
    "pine_hardwood": {"cost": 4.00, "tier": MaterialTier.STANDARD, "quality": QualityScore.MEDIUM},
    "poplar_hardwood": {"cost": 4.50, "tier": MaterialTier.STANDARD, "quality": QualityScore.MEDIUM},
}

# Material alternatives mapping
MATERIAL_ALTERNATIVES = {
    "baltic_birch_plywood": ["birch_plywood", "maple_plywood", "mdf_veneered"],
    "birch_plywood": ["baltic_birch_plywood", "mdf_veneered", "mdf_standard"],
    "oak_plywood": ["maple_plywood", "mdf_veneered_oak", "mdf_standard"],
    "maple_plywood": ["birch_plywood", "mdf_veneered", "mdf_standard"],
    "cherry_plywood": ["maple_plywood", "oak_plywood", "mdf_veneered"],
    "walnut_plywood": ["cherry_plywood", "oak_plywood", "mdf_veneered"],
    "oak_hardwood": ["maple_hardwood", "poplar_hardwood", "pine_hardwood"],
    "maple_hardwood": ["oak_hardwood", "poplar_hardwood", "pine_hardwood"],
    "mdf_standard": ["particle_board_melamine", "particle_board"],
    "mdf_veneered": ["birch_plywood", "mdf_standard"],
}

# Hardware cost database (per unit)
HARDWARE_COSTS = {
    # Drawer slides
    "full_extension_soft_close": {"cost": 25.00, "quality": QualityScore.PREMIUM},
    "full_extension_standard": {"cost": 15.00, "quality": QualityScore.HIGH},
    "3_4_extension_standard": {"cost": 10.00, "quality": QualityScore.MEDIUM},
    "side_mount_basic": {"cost": 8.00, "quality": QualityScore.MEDIUM},
    "undermount_soft_close": {"cost": 35.00, "quality": QualityScore.PREMIUM},
    
    # Hinges
    "concealed_soft_close": {"cost": 8.00, "quality": QualityScore.PREMIUM},
    "concealed_standard": {"cost": 4.00, "quality": QualityScore.HIGH},
    "european_110_deg": {"cost": 3.00, "quality": QualityScore.MEDIUM},
    "butt_hinge": {"cost": 2.00, "quality": QualityScore.MEDIUM},
    "piano_hinge_per_ft": {"cost": 6.00, "quality": QualityScore.HIGH},
    
    # Handles/Pulls
    "bar_pull_5inch": {"cost": 4.00, "quality": QualityScore.HIGH},
    "bar_pull_3inch": {"cost": 3.00, "quality": QualityScore.HIGH},
    "cup_pull": {"cost": 6.00, "quality": QualityScore.PREMIUM},
    "knob_round": {"cost": 2.00, "quality": QualityScore.MEDIUM},
    "knob_decorative": {"cost": 5.00, "quality": QualityScore.PREMIUM},
}

# Hardware alternatives
HARDWARE_ALTERNATIVES = {
    "full_extension_soft_close": ["full_extension_standard", "3_4_extension_standard"],
    "undermount_soft_close": ["full_extension_soft_close", "full_extension_standard"],
    "concealed_soft_close": ["concealed_standard", "european_110_deg"],
    "concealed_standard": ["european_110_deg", "butt_hinge"],
    "cup_pull": ["bar_pull_5inch", "knob_round"],
    "knob_decorative": ["knob_round", "bar_pull_3inch"],
}


def get_material_alternatives(material: str, sqft: float) -> List[MaterialAlternative]:
    """Get cost-saving alternatives for a material"""
    alternatives = []
    
    if material not in MATERIAL_COSTS:
        return alternatives
    
    original_data = MATERIAL_COSTS[material]
    original_cost = original_data["cost"] * sqft
    
    for alt_material in MATERIAL_ALTERNATIVES.get(material, []):
        if alt_material not in MATERIAL_COSTS:
            continue
            
        alt_data = MATERIAL_COSTS[alt_material]
        alt_cost = alt_data["cost"] * sqft
        
        if alt_cost >= original_cost:
            continue  # No savings
        
        savings = original_cost - alt_cost
        savings_percent = (savings / original_cost) * 100
        
        # Determine quality impact
        quality_diff = original_data["quality"].value - alt_data["quality"].value
        
        if quality_diff == 0:
            quality_impact = "minimal"
            recommended = True
        elif quality_diff == 1:
            quality_impact = "moderate"
            recommended = True
        else:
            quality_impact = "significant"
            recommended = False
        
        # Generate tradeoff notes
        notes = []
        if alt_data["tier"] != original_data["tier"]:
            tier_names = {MaterialTier.BUDGET: "budget", MaterialTier.STANDARD: "standard", MaterialTier.PREMIUM: "premium"}
            notes.append(f"Moves from {tier_names[original_data['tier']]} to {tier_names[alt_data['tier']]} tier")
        
        if "mdf" in alt_material.lower() and "mdf" not in material.lower():
            notes.append("MDF is heavier and less moisture-resistant than plywood")
            notes.append("MDF provides smoother paint finish")
        
        if "particle" in alt_material.lower() and "particle" not in material.lower():
            notes.append("Particle board is less durable than plywood/MDF")
            notes.append("Not recommended for heavy loads or moisture-prone areas")
        
        alternatives.append(MaterialAlternative(
            original=material,
            alternative=alt_material,
            original_cost=round(original_cost, 2),
            alternative_cost=round(alt_cost, 2),
            savings=round(savings, 2),
            savings_percent=round(savings_percent, 1),
            quality_impact=quality_impact,
            tradeoff_notes=notes,
            recommended=recommended
        ))
    
    return sorted(alternatives, key=lambda x: x.savings_percent, reverse=True)


def get_hardware_alternatives(hardware_type: str, quantity: int) -> List[HardwareAlternative]:
    """Get cost-saving alternatives for hardware"""
    alternatives = []
    
    if hardware_type not in HARDWARE_COSTS:
        return alternatives
    
    original_data = HARDWARE_COSTS[hardware_type]
    original_cost = original_data["cost"] * quantity
    
    for alt_hardware in HARDWARE_ALTERNATIVES.get(hardware_type, []):
        if alt_hardware not in HARDWARE_COSTS:
            continue
        
        alt_data = HARDWARE_COSTS[alt_hardware]
        alt_cost = alt_data["cost"] * quantity
        
        if alt_cost >= original_cost:
            continue
        
        savings = original_cost - alt_cost
        
        quality_diff = original_data["quality"].value - alt_data["quality"].value
        quality_impact = "minimal" if quality_diff == 0 else "moderate" if quality_diff == 1 else "significant"
        recommended = quality_diff <= 1
        
        alternatives.append(HardwareAlternative(
            original=hardware_type,
            alternative=alt_hardware,
            original_cost=round(original_cost, 2),
            alternative_cost=round(alt_cost, 2),
            savings=round(savings, 2),
            quality_impact=quality_impact,
            recommended=recommended
        ))
    
    return alternatives


def generate_bulk_suggestions(materials: Dict[str, float], hardware: Dict[str, int]) -> List[Dict[str, Any]]:
    """Generate bulk purchase suggestions"""
    suggestions = []
    
    # Check for materials that could benefit from bulk purchase
    for material, sqft in materials.items():
        # Standard sheet is 32 sq ft (4x8)
        sheets_needed = math.ceil(sqft / 32)
        
        if sheets_needed >= 3:
            # Bulk discount typically starts at 5+ sheets
            if sheets_needed < 5:
                suggestions.append({
                    "type": "material",
                    "item": material,
                    "current_quantity": sheets_needed,
                    "suggested_quantity": 5,
                    "reason": "Buy 5 sheets for bulk discount (typically 10-15% off)",
                    "potential_savings": round(MATERIAL_COSTS.get(material, {}).get("cost", 5) * 32 * 0.12, 2)
                })
    
    # Check for hardware bulk opportunities
    for hardware_type, quantity in hardware.items():
        if quantity >= 10:
            suggestions.append({
                "type": "hardware",
                "item": hardware_type,
                "current_quantity": quantity,
                "suggested_quantity": quantity + 5,  # Suggest extra for spares
                "reason": f"Buying {quantity}+ units qualifies for contractor pricing",
                "potential_savings": round(HARDWARE_COSTS.get(hardware_type, {}).get("cost", 5) * quantity * 0.10, 2)
            })
    
    return suggestions


def generate_savings_report(
    cabinet_design: Dict[str, Any],
    materials: Dict[str, float],  # material -> sqft
    hardware: Dict[str, int]  # hardware_type -> quantity
) -> SavingsReport:
    """Generate a complete savings report for a cabinet design"""
    
    # Calculate original costs
    material_cost = sum(
        MATERIAL_COSTS.get(m, {"cost": 5})["cost"] * sqft
        for m, sqft in materials.items()
    )
    
    hardware_cost = sum(
        HARDWARE_COSTS.get(h, {"cost": 5})["cost"] * qty
        for h, qty in hardware.items()
    )
    
    total_original = material_cost + hardware_cost
    
    # Get alternatives
    all_material_alternatives = []
    for material, sqft in materials.items():
        all_material_alternatives.extend(get_material_alternatives(material, sqft))
    
    all_hardware_alternatives = []
    for hardware_type, quantity in hardware.items():
        all_hardware_alternatives.extend(get_hardware_alternatives(hardware_type, quantity))
    
    # Calculate optimized cost (sum of best recommended alternatives)
    material_savings = sum(a.savings for a in all_material_alternatives if a.recommended)
    hardware_savings = sum(a.savings for a in all_hardware_alternatives if a.recommended)
    
    total_optimized = total_original - material_savings - hardware_savings
    total_savings = total_original - total_optimized
    savings_percent = (total_savings / total_original * 100) if total_original > 0 else 0
    
    # Generate bulk suggestions
    bulk_suggestions = generate_bulk_suggestions(materials, hardware)
    
    # Calculate quality scores
    quality_original = sum(
        MATERIAL_COSTS.get(m, {"quality": QualityScore.MEDIUM})["quality"].value
        for m in materials.keys()
    ) + sum(
        HARDWARE_COSTS.get(h, {"quality": QualityScore.MEDIUM})["quality"].value
        for h in hardware.keys()
    )
    
    quality_optimized = quality_original - sum(
        1 for a in all_material_alternatives if a.recommended and a.quality_impact != "minimal"
    ) - sum(
        1 for a in all_hardware_alternatives if a.recommended and a.quality_impact != "minimal"
    )
    
    return SavingsReport(
        total_original_cost=round(total_original, 2),
        total_optimized_cost=round(total_optimized, 2),
        total_savings=round(total_savings, 2),
        savings_percent=round(savings_percent, 1),
        material_alternatives=all_material_alternatives,
        hardware_alternatives=all_hardware_alternatives,
        bulk_purchase_suggestions=bulk_suggestions,
        quality_score_original=quality_original,
        quality_score_optimized=max(quality_optimized, 1)
    )


def get_budget_tier_recommendations(budget: str) -> Dict[str, Any]:
    """Get material and hardware recommendations for a budget tier"""
    
    if budget == "budget":
        return {
            "primary_material": "mdf_standard",
            "secondary_material": "particle_board_melamine",
            "hardware_tier": "basic",
            "recommended_hardware": {
                "slides": "side_mount_basic",
                "hinges": "butt_hinge",
                "pulls": "knob_round"
            },
            "notes": [
                "MDF provides smooth paint finish at low cost",
                "Basic hardware is functional but won't have soft-close",
                "Consider upgrading slides for heavy drawers"
            ],
            "estimated_cost_multiplier": 0.6  # 60% of standard cost
        }
    
    elif budget == "standard":
        return {
            "primary_material": "birch_plywood",
            "secondary_material": "mdf_veneered",
            "hardware_tier": "standard",
            "recommended_hardware": {
                "slides": "full_extension_standard",
                "hinges": "concealed_standard",
                "pulls": "bar_pull_3inch"
            },
            "notes": [
                "Birch plywood offers good durability and appearance",
                "Concealed hinges look professional",
                "Full-extension slides provide good access"
            ],
            "estimated_cost_multiplier": 1.0  # Baseline
        }
    
    else:  # premium
        return {
            "primary_material": "baltic_birch_plywood",
            "secondary_material": "maple_plywood",
            "hardware_tier": "premium",
            "recommended_hardware": {
                "slides": "undermount_soft_close",
                "hinges": "concealed_soft_close",
                "pulls": "cup_pull"
            },
            "notes": [
                "Baltic birch has superior ply count and void-free core",
                "Soft-close hardware adds luxury feel",
                "Cup pulls provide classic premium look"
            ],
            "estimated_cost_multiplier": 1.5  # 150% of standard cost
        }

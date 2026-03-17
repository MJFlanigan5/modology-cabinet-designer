"""
Board Yield Optimizer - Phase 5 Feature

Optimizes plywood usage by calculating exact sheets needed and
which cuts should come from which sheet to minimize waste.
"""
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import math


class SheetSize(Enum):
    STANDARD_4x8 = (48, 96)
    STANDARD_4x4 = (48, 48)
    EXTENDED_4x10 = (48, 120)
    EXTENDED_5x5 = (60, 60)
    EUROPEAN_5x5 = (1524, 1524)  # mm


@dataclass
class CutPiece:
    """A piece to be cut from a sheet"""
    name: str
    width: float
    height: float
    quantity: int
    material: str
    grain_direction: Optional[str] = None  # "horizontal", "vertical", or None
    priority: int = 0  # Higher priority = cut first


@dataclass
class SheetPlan:
    """Plan for a single sheet with cuts mapped out"""
    sheet_number: int
    sheet_size: Tuple[float, float]
    cuts: List[Dict[str, Any]]
    waste_pieces: List[Dict[str, Any]]
    utilization_percent: float
    remaining_area: float


@dataclass
class YieldReport:
    """Complete yield optimization report"""
    sheets_needed: int
    sheet_plans: List[SheetPlan]
    total_material_cost: float
    cost_per_cut: float
    total_waste_percent: float
    savings_vs_naive: float
    recommendations: List[str]


# Standard sheet sizes and prices
SHEET_PRICES = {
    "birch_plywood": {SheetSize.STANDARD_4x8: 65, SheetSize.EXTENDED_4x10: 85},
    "oak_plywood": {SheetSize.STANDARD_4x8: 75, SheetSize.EXTENDED_4x10: 95},
    "mdf": {SheetSize.STANDARD_4x8: 35, SheetSize.EXTENDED_4x10: 45},
    "particle_board": {SheetSize.STANDARD_4x8: 25},
    "melamine": {SheetSize.STANDARD_4x8: 40},
}

# Kerf (blade width) for calculations
DEFAULT_KERF = 0.125  # 1/8 inch


def calculate_sheets_needed(
    pieces: List[CutPiece],
    sheet_size: SheetSize = SheetSize.STANDARD_4x8,
    kerf: float = DEFAULT_KERF
) -> int:
    """
    Calculate minimum number of sheets needed using area-based estimation.
    """
    sheet_area = sheet_size.value[0] * sheet_size.value[1]
    total_piece_area = sum(p.width * p.height * p.quantity for p in pieces)
    
    # Add kerf waste (rough estimate)
    num_cuts = sum(p.quantity * 4 for p in pieces)  # Approx 4 cuts per piece
    kerf_area = num_cuts * kerf * max(sheet_size.value)
    
    total_needed = total_piece_area + kerf_area
    return math.ceil(total_needed / sheet_area)


def optimize_cuts_for_sheet(
    pieces: List[CutPiece],
    sheet_size: Tuple[float, float],
    kerf: float = DEFAULT_KERF,
    grain_important: bool = True
) -> SheetPlan:
    """
    Optimize cut layout for a single sheet using guillotine cutting.
    Returns a plan with cut positions and waste areas.
    """
    # Sort pieces by size (largest first for better fit)
    sorted_pieces = sorted(pieces, key=lambda p: p.width * p.height, reverse=True)
    
    cuts = []
    waste_pieces = []
    
    # Track remaining space on sheet
    remaining_rects = [(0, 0, sheet_size[0], sheet_size[1])]
    
    for piece in sorted_pieces:
        for _ in range(piece.quantity):
            placed = False
            
            # Try to fit piece in remaining rectangles
            for i, rect in enumerate(remaining_rects):
                x, y, w, h = rect
                
                # Check if piece fits (considering grain direction)
                fits_normal = piece.width <= w and piece.height <= h
                fits_rotated = piece.height <= w and piece.width <= h
                
                # Respect grain direction if important
                if grain_important and piece.grain_direction:
                    if piece.grain_direction == "vertical":
                        fits_rotated = False
                    elif piece.grain_direction == "horizontal":
                        fits_normal = False
                
                if fits_normal:
                    cuts.append({
                        "name": piece.name,
                        "x": x,
                        "y": y,
                        "width": piece.width,
                        "height": piece.height,
                        "rotated": False
                    })
                    
                    # Update remaining rectangles
                    remaining_rects.pop(i)
                    # Add right remainder
                    if w > piece.width + kerf:
                        remaining_rects.append((x + piece.width + kerf, y, w - piece.width - kerf, piece.height))
                    # Add top remainder
                    if h > piece.height + kerf:
                        remaining_rects.append((x, y + piece.height + kerf, w, h - piece.height - kerf))
                    
                    placed = True
                    break
                
                elif fits_rotated:
                    cuts.append({
                        "name": piece.name,
                        "x": x,
                        "y": y,
                        "width": piece.height,
                        "height": piece.width,
                        "rotated": True
                    })
                    
                    remaining_rects.pop(i)
                    if w > piece.height + kerf:
                        remaining_rects.append((x + piece.height + kerf, y, w - piece.height - kerf, piece.width))
                    if h > piece.width + kerf:
                        remaining_rects.append((x, y + piece.width + kerf, w, h - piece.width - kerf))
                    
                    placed = True
                    break
            
            if not placed:
                # Piece doesn't fit on this sheet
                waste_pieces.append({
                    "name": piece.name,
                    "width": piece.width,
                    "height": piece.height,
                    "reason": "Does not fit on remaining space"
                })
    
    # Calculate utilization
    sheet_area = sheet_size[0] * sheet_size[1]
    used_area = sum(c["width"] * c["height"] for c in cuts)
    utilization = (used_area / sheet_area) * 100
    
    return SheetPlan(
        sheet_number=1,
        sheet_size=sheet_size,
        cuts=cuts,
        waste_pieces=waste_pieces,
        utilization_percent=round(utilization, 1),
        remaining_area=sheet_area - used_area
    )


def generate_yield_report(
    pieces: List[CutPiece],
    material: str,
    supplier_price: Optional[float] = None,
    sheet_size: SheetSize = SheetSize.STANDARD_4x8,
    kerf: float = DEFAULT_KERF
) -> YieldReport:
    """
    Generate a complete yield optimization report.
    """
    sheet_plans = []
    remaining_pieces = pieces.copy()
    sheet_num = 1
    
    # Get sheet price
    if supplier_price:
        sheet_cost = supplier_price
    else:
        sheet_cost = SHEET_PRICES.get(material, {}).get(sheet_size, 50)
    
    while remaining_pieces:
        # Try to fit pieces on a sheet
        plan = optimize_cuts_for_sheet(remaining_pieces, sheet_size.value, kerf)
        plan.sheet_number = sheet_num
        sheet_plans.append(plan)
        
        # Remove placed pieces
        placed_names = {c["name"] for c in plan.cuts}
        new_remaining = []
        for p in remaining_pieces:
            placed_count = sum(1 for c in plan.cuts if c["name"] == p.name)
            remaining_qty = p.quantity - placed_count
            if remaining_qty > 0:
                new_remaining.append(CutPiece(
                    name=p.name,
                    width=p.width,
                    height=p.height,
                    quantity=remaining_qty,
                    material=p.material,
                    grain_direction=p.grain_direction
                ))
        
        remaining_pieces = new_remaining
        sheet_num += 1
        
        # Safety check to prevent infinite loops
        if sheet_num > 100:
            break
    
    # Calculate totals
    total_sheets = len(sheet_plans)
    total_cost = total_sheets * sheet_cost
    total_cuts = sum(len(p.cuts) for p in sheet_plans)
    cost_per_cut = total_cost / total_cuts if total_cuts > 0 else 0
    
    avg_utilization = sum(p.utilization_percent for p in sheet_plans) / total_sheets if total_sheets > 0 else 0
    total_waste = 100 - avg_utilization
    
    # Calculate savings vs naive approach (simple area division)
    naive_sheets = calculate_sheets_needed(pieces, sheet_size, kerf)
    naive_cost = naive_sheets * sheet_cost
    savings = naive_cost - total_cost if total_sheets <= naive_sheets else 0
    
    # Generate recommendations
    recommendations = []
    if avg_utilization < 70:
        recommendations.append("Consider combining with another project to improve sheet utilization")
    if total_sheets < naive_sheets:
        recommendations.append(f"Optimized layout saves {naive_sheets - total_sheets} sheet(s)")
    if total_sheets > 1 and sheet_plans[-1].utilization_percent < 50:
        recommendations.append("Last sheet has low utilization - good for future projects")
    
    return YieldReport(
        sheets_needed=total_sheets,
        sheet_plans=sheet_plans,
        total_material_cost=round(total_cost, 2),
        cost_per_cut=round(cost_per_cut, 2),
        total_waste_percent=round(total_waste, 1),
        savings_vs_naive=round(savings, 2),
        recommendations=recommendations
    )


def get_cutting_sequence(sheet_plan: SheetPlan) -> List[Dict[str, Any]]:
    """
    Generate optimal cutting sequence for a sheet.
    Groups cuts by direction to minimize saw adjustments.
    """
    # Sort cuts by position for efficient cutting
    cuts = sheet_plan.cuts.copy()
    
    # Group by rows (y position)
    rows = {}
    for cut in cuts:
        y = round(cut["y"], 1)
        if y not in rows:
            rows[y] = []
        rows[y].append(cut)
    
    sequence = []
    step = 1
    
    # First pass: rip cuts (full length)
    for y in sorted(rows.keys()):
        row_cuts = sorted(rows[y], key=lambda c: c["x"])
        for cut in row_cuts:
            sequence.append({
                "step": step,
                "type": "cross_cut",
                "piece_name": cut["name"],
                "start_x": cut["x"],
                "start_y": cut["y"],
                "width": cut["width"],
                "height": cut["height"],
                "instruction": f"Cut {cut['name']}: {cut['width']}\" x {cut['height']}\" at ({cut['x']}\", {cut['y']}\")"
            })
            step += 1
    
    return sequence


def estimate_offcut_usability(waste_pieces: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Assess which waste pieces are usable for future projects.
    """
    usable = []
    
    for piece in waste_pieces:
        min_dim = min(piece.get("width", 0), piece.get("height", 0))
        area = piece.get("width", 0) * piece.get("height", 0)
        
        # Pieces larger than 6" in both dimensions are potentially useful
        if min_dim >= 6:
            uses = []
            if min_dim >= 12:
                uses.append("Drawer bottom")
                uses.append("Shelf")
            if min_dim >= 6:
                uses.append("Small parts")
                uses.append("Test pieces")
            
            usable.append({
                **piece,
                "usable": True,
                "potential_uses": uses,
                "area_sq_in": area
            })
    
    return usable


def compare_sheet_sizes(pieces: List[CutPiece], material: str) -> Dict[str, Any]:
    """
    Compare different sheet sizes to find most cost-effective option.
    """
    comparisons = []
    
    for size in SheetSize:
        try:
            report = generate_yield_report(pieces, material, sheet_size=size)
            comparisons.append({
                "sheet_size": f"{size.value[0]}\" x {size.value[1]}\"",
                "sheets_needed": report.sheets_needed,
                "total_cost": report.total_material_cost,
                "waste_percent": report.total_waste_percent,
                "cost_per_sqft": round(report.total_material_cost / (size.value[0] * size.value[1] * report.sheets_needed), 2)
            })
        except KeyError:
            continue
    
    if comparisons:
        best = min(comparisons, key=lambda x: x["total_cost"])
        return {
            "comparisons": comparisons,
            "recommendation": best
        }
    
    return {"comparisons": [], "recommendation": None}

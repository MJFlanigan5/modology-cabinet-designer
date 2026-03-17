"""
Phase 4: Advanced Nesting Optimizer
Implements non-guillotine (true shape) nesting algorithm for better material utilization.
Uses a bottom-left placement strategy with rotation optimization.
"""

from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, field
from enum import Enum
import math


class NestingAlgorithm(str, Enum):
    GUILLOTINE = "guillotine"  # Current implementation - straight cuts only
    BOTTOM_LEFT = "bottom_left"  # Simple non-guillotine
    MAXIMAL_RECTANGLE = "maximal_rectangle"  # Advanced rectangle packing
    NFP = "nfp"  # No-Fit Polygon for irregular shapes (future)


@dataclass
class NestingPart:
    """Represents a part to be nested."""
    id: str
    name: str
    width: float
    height: float
    quantity: int = 1
    material_id: str = "default"
    grain_direction: Optional[str] = None  # "horizontal", "vertical", None
    can_rotate: bool = True
    priority: int = 0  # Higher priority = placed first
    
    def area(self) -> float:
        return self.width * self.height
    
    def rotated_dimensions(self) -> Tuple[float, float]:
        return (self.height, self.width)


@dataclass
class PlacedPart:
    """A part that has been placed on a sheet."""
    part: NestingPart
    x: float
    y: float
    rotated: bool = False
    sheet_index: int = 0
    
    @property
    def width(self) -> float:
        return self.part.height if self.rotated else self.part.width
    
    @property
    def height(self) -> float:
        return self.part.width if self.rotated else self.part.height
    
    def bounds(self) -> Tuple[float, float, float, float]:
        """Returns (x1, y1, x2, y2) of the part."""
        return (self.x, self.y, self.x + self.width, self.y + self.height)


@dataclass
class NestingSheet:
    """A sheet with placed parts."""
    index: int
    width: float
    height: float
    placed_parts: List[PlacedPart] = field(default_factory=list)
    material_id: str = "default"
    
    def used_area(self) -> float:
        return sum(p.width * p.height for p in self.placed_parts)
    
    def free_area(self) -> float:
        return (self.width * self.height) - self.used_area()
    
    def utilization(self) -> float:
        total = self.width * self.height
        return (self.used_area() / total) * 100 if total > 0 else 0


@dataclass
class NestingResult:
    """Result of a nesting optimization."""
    sheets: List[NestingSheet]
    total_sheets: int
    total_parts: int
    placed_parts: int
    unplaced_parts: List[NestingPart]
    overall_utilization: float
    algorithm_used: NestingAlgorithm
    optimization_time_ms: float
    
    def to_dict(self) -> Dict:
        return {
            "sheets": [
                {
                    "index": sheet.index,
                    "width": sheet.width,
                    "height": sheet.height,
                    "material_id": sheet.material_id,
                    "utilization": round(sheet.utilization(), 2),
                    "parts": [
                        {
                            "id": p.part.id,
                            "name": p.part.name,
                            "x": p.x,
                            "y": p.y,
                            "width": p.width,
                            "height": p.height,
                            "rotated": p.rotated,
                        }
                        for p in sheet.placed_parts
                    ]
                }
                for sheet in self.sheets
            ],
            "total_sheets": self.total_sheets,
            "total_parts": self.total_parts,
            "placed_parts": self.placed_parts,
            "unplaced_parts": [
                {"id": p.id, "name": p.name, "width": p.width, "height": p.height}
                for p in self.unplaced_parts
            ],
            "overall_utilization": round(self.overall_utilization, 2),
            "algorithm_used": self.algorithm_used.value,
            "optimization_time_ms": round(self.optimization_time_ms, 2),
        }


class AdvancedNestingOptimizer:
    """
    Advanced nesting optimizer supporting multiple algorithms.
    Default uses Bottom-Left placement which is more efficient than guillotine.
    """
    
    def __init__(
        self,
        sheet_width: float = 48.0,
        sheet_height: float = 96.0,
        algorithm: NestingAlgorithm = NestingAlgorithm.BOTTOM_LEFT,
        spacing: float = 0.125,  # 1/8" kerf/cutting allowance
        trim_edges: float = 0.25,  # Edge trimming
        allow_rotation: bool = True,
    ):
        self.sheet_width = sheet_width
        self.sheet_height = sheet_height
        self.algorithm = algorithm
        self.spacing = spacing
        self.trim_edges = trim_edges
        self.allow_rotation = allow_rotation
        self.sheets: List[NestingSheet] = []
    
    def optimize(self, parts: List[NestingPart]) -> NestingResult:
        """
        Optimize part placement using the selected algorithm.
        """
        import time
        start_time = time.time()
        
        # Reset
        self.sheets = []
        
        # Expand parts by quantity
        expanded_parts = []
        for part in parts:
            for _ in range(part.quantity):
                expanded_parts.append(part)
        
        total_parts = len(expanded_parts)
        unplaced_parts = []
        
        # Sort parts by area (largest first for better packing)
        expanded_parts.sort(key=lambda p: p.area(), reverse=True)
        
        # Use selected algorithm
        if self.algorithm == NestingAlgorithm.GUILLOTINE:
            placed_count = self._guillotine_pack(expanded_parts, unplaced_parts)
        else:
            placed_count = self._bottom_left_pack(expanded_parts, unplaced_parts)
        
        # Calculate overall utilization
        total_area = sum(s.width * s.height for s in self.sheets)
        used_area = sum(s.used_area() for s in self.sheets)
        utilization = (used_area / total_area * 100) if total_area > 0 else 0
        
        optimization_time = (time.time() - start_time) * 1000
        
        return NestingResult(
            sheets=self.sheets,
            total_sheets=len(self.sheets),
            total_parts=total_parts,
            placed_parts=placed_count,
            unplaced_parts=unplaced_parts,
            overall_utilization=utilization,
            algorithm_used=self.algorithm,
            optimization_time_ms=optimization_time,
        )
    
    def _guillotine_pack(self, parts: List[NestingPart], unplaced: List[NestingPart]) -> int:
        """
        Guillotine packing - parts placed in rectangles created by previous cuts.
        More restrictive but compatible with panel saws.
        """
        placed_count = 0
        
        for part in parts:
            placed = False
            
            # Try existing sheets
            for sheet in self.sheets:
                if self._try_place_guillotine(sheet, part):
                    placed = True
                    placed_count += 1
                    break
            
            if not placed:
                # Create new sheet
                new_sheet = NestingSheet(
                    index=len(self.sheets),
                    width=self.sheet_width,
                    height=self.sheet_height,
                    material_id=part.material_id,
                )
                self.sheets.append(new_sheet)
                
                if self._try_place_guillotine(new_sheet, part):
                    placed_count += 1
                else:
                    unplaced.append(part)
        
        return placed_count
    
    def _try_place_guillotine(self, sheet: NestingSheet, part: NestingPart) -> bool:
        """Try to place part using guillotine constraints."""
        # Simplified guillotine - find first available corner
        x, y = self._find_guillotine_position(sheet, part)
        
        if x is not None:
            placed = PlacedPart(
                part=part,
                x=x,
                y=y,
                rotated=False,
                sheet_index=sheet.index,
            )
            sheet.placed_parts.append(placed)
            return True
        
        # Try rotation
        if self.allow_rotation and part.can_rotate:
            x, y = self._find_guillotine_position(sheet, part, rotated=True)
            if x is not None:
                placed = PlacedPart(
                    part=part,
                    x=x,
                    y=y,
                    rotated=True,
                    sheet_index=sheet.index,
                )
                sheet.placed_parts.append(placed)
                return True
        
        return False
    
    def _find_guillotine_position(
        self, 
        sheet: NestingSheet, 
        part: NestingPart, 
        rotated: bool = False
    ) -> Tuple[Optional[float], Optional[float]]:
        """Find a position for the part respecting guillotine cuts."""
        width = part.height if rotated else part.width
        height = part.width if rotated else part.height
        
        # Add spacing
        width += self.spacing
        height += self.spacing
        
        # Get candidate positions from existing parts
        x_candidates = [self.trim_edges]
        y_candidates = [self.trim_edges]
        
        for p in sheet.placed_parts:
            x_candidates.append(p.x + p.width + self.spacing)
            y_candidates.append(p.y + p.height + self.spacing)
        
        # Try each position
        for x in sorted(set(x_candidates)):
            for y in sorted(set(y_candidates)):
                if self._can_place_at(sheet, x, y, width, height):
                    return (x, y)
        
        return (None, None)
    
    def _bottom_left_pack(self, parts: List[NestingPart], unplaced: List[NestingPart]) -> int:
        """
        Bottom-Left packing - places parts at the lowest, leftmost available position.
        Non-guillotine - allows for more efficient packing.
        """
        placed_count = 0
        
        for part in parts:
            placed = False
            best_position = None
            best_sheet = None
            best_rotated = False
            best_score = float('inf')
            
            # Try both orientations
            orientations = [False]
            if self.allow_rotation and part.can_rotate:
                orientations.append(True)
            
            # Find best position across all sheets
            for sheet in self.sheets:
                for rotated in orientations:
                    pos = self._find_bottom_left_position(sheet, part, rotated)
                    if pos:
                        x, y = pos
                        # Score: prefer lower y, then lower x
                        score = y * 1000 + x
                        if score < best_score:
                            best_score = score
                            best_position = (x, y)
                            best_sheet = sheet
                            best_rotated = rotated
            
            if best_position:
                placed = PlacedPart(
                    part=part,
                    x=best_position[0],
                    y=best_position[1],
                    rotated=best_rotated,
                    sheet_index=best_sheet.index,
                )
                best_sheet.placed_parts.append(placed)
                placed_count += 1
            else:
                # Create new sheet
                new_sheet = NestingSheet(
                    index=len(self.sheets),
                    width=self.sheet_width,
                    height=self.sheet_height,
                    material_id=part.material_id,
                )
                self.sheets.append(new_sheet)
                
                # Place at origin
                for rotated in orientations:
                    width = part.height if rotated else part.width
                    height = part.width if rotated else part.height
                    
                    if width <= self.sheet_width and height <= self.sheet_height:
                        placed = PlacedPart(
                            part=part,
                            x=self.trim_edges,
                            y=self.trim_edges,
                            rotated=rotated,
                            sheet_index=new_sheet.index,
                        )
                        new_sheet.placed_parts.append(placed)
                        placed_count += 1
                        break
                else:
                    unplaced.append(part)
        
        return placed_count
    
    def _find_bottom_left_position(
        self, 
        sheet: NestingSheet, 
        part: NestingPart, 
        rotated: bool
    ) -> Optional[Tuple[float, float]]:
        """Find the bottom-leftmost valid position for the part."""
        width = part.height if rotated else part.width
        height = part.width if rotated else part.height
        
        # Add spacing
        width += self.spacing
        height += self.spacing
        
        # Check if part fits on sheet
        if width > self.sheet_width or height > self.sheet_height:
            return None
        
        # Generate candidate positions
        x_candidates = [self.trim_edges]
        y_candidates = [self.trim_edges]
        
        for p in sheet.placed_parts:
            x_candidates.append(p.x + p.width + self.spacing)
            y_candidates.append(p.y + p.height + self.spacing)
        
        # Find the bottom-leftmost valid position
        best_pos = None
        best_y = float('inf')
        
        for y in sorted(set(y_candidates)):
            if y + height > self.sheet_height:
                continue
            
            for x in sorted(set(x_candidates)):
                if x + width > self.sheet_width:
                    continue
                
                if self._can_place_at(sheet, x, y, width, height):
                    if y < best_y or (y == best_y and (best_pos is None or x < best_pos[0])):
                        best_y = y
                        best_pos = (x, y)
        
        return best_pos
    
    def _can_place_at(
        self, 
        sheet: NestingSheet, 
        x: float, 
        y: float, 
        width: float, 
        height: float
    ) -> bool:
        """Check if part can be placed at the given position."""
        # Check sheet bounds
        if x + width > self.sheet_width or y + height > self.sheet_height:
            return False
        
        # Check overlap with existing parts
        new_bounds = (x, y, x + width, y + height)
        
        for p in sheet.placed_parts:
            existing_bounds = p.bounds()
            if self._rectangles_overlap(new_bounds, existing_bounds):
                return False
        
        return True
    
    def _rectangles_overlap(
        self, 
        r1: Tuple[float, float, float, float], 
        r2: Tuple[float, float, float, float]
    ) -> bool:
        """Check if two rectangles overlap."""
        return not (
            r1[2] <= r2[0] or  # r1 right <= r2 left
            r1[0] >= r2[2] or  # r1 left >= r2 right
            r1[3] <= r2[1] or  # r1 bottom <= r2 top
            r1[1] >= r2[3]     # r1 top >= r2 bottom
        )


def optimize_nesting(
    parts: List[Dict],
    sheet_width: float = 48.0,
    sheet_height: float = 96.0,
    algorithm: str = "bottom_left",
    spacing: float = 0.125,
) -> Dict:
    """
    Convenience function for nesting optimization.
    
    Args:
        parts: List of part dicts with id, name, width, height, quantity, etc.
        sheet_width: Sheet width in inches
        sheet_height: Sheet height in inches
        algorithm: "guillotine" or "bottom_left"
        spacing: Kerf/cutting allowance
        
    Returns:
        Dict with nesting result
    """
    # Parse algorithm
    algo = NestingAlgorithm(algorithm)
    
    # Create part objects
    part_objs = [
        NestingPart(
            id=p.get("id", str(i)),
            name=p.get("name", f"Part {i}"),
            width=float(p["width"]),
            height=float(p["height"]),
            quantity=int(p.get("quantity", 1)),
            material_id=p.get("material_id", "default"),
            grain_direction=p.get("grain_direction"),
            can_rotate=p.get("can_rotate", True),
            priority=p.get("priority", 0),
        )
        for i, p in enumerate(parts)
    ]
    
    # Optimize
    optimizer = AdvancedNestingOptimizer(
        sheet_width=sheet_width,
        sheet_height=sheet_height,
        algorithm=algo,
        spacing=spacing,
    )
    result = optimizer.optimize(part_objs)
    
    return result.to_dict()


# Example usage
if __name__ == "__main__":
    test_parts = [
        {"id": "1", "name": "Side Panel", "width": 24, "height": 72, "quantity": 2},
        {"id": "2", "name": "Top", "width": 36, "height": 24, "quantity": 2},
        {"id": "3", "name": "Shelf", "width": 34, "height": 12, "quantity": 4},
        {"id": "4", "name": "Door", "width": 36, "height": 24, "quantity": 2},
    ]
    
    print("=== Bottom-Left Nesting ===")
    result = optimize_nesting(test_parts, algorithm="bottom_left")
    print(f"Sheets: {result['total_sheets']}")
    print(f"Utilization: {result['overall_utilization']}%")
    print(f"Parts placed: {result['placed_parts']}/{result['total_parts']}")

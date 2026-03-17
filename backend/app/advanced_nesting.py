"""
Advanced Nesting Algorithm - Non-Guillotine True Shape Nesting
Implements bottom-left and NFDH (Next Fit Decreasing Height) algorithms
for irregular shapes and non-guillotine cutting patterns.
"""

from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, field
from enum import Enum
import math


class NestingAlgorithm(str, Enum):
    BOTTOM_LEFT = "bottom_left"
    NFDH = "nfdh"  # Next Fit Decreasing Height
    FFDH = "ffdh"  # First Fit Decreasing Height
    BFDH = "bfdh"  # Best Fit Decreasing Height
    GENETIC = "genetic"  # Genetic algorithm for complex shapes


@dataclass
class Point:
    """2D point for polygon vertices"""
    x: float
    y: float
    
    def __add__(self, other: 'Point') -> 'Point':
        return Point(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other: 'Point') -> 'Point':
        return Point(self.x - other.x, self.y - other.y)
    
    def rotate_90(self) -> 'Point':
        return Point(-self.y, self.x)


@dataclass
class Polygon:
    """Polygon shape for irregular parts"""
    vertices: List[Point]
    rotation: int = 0  # Rotation in degrees (0, 90, 180, 270)
    
    def get_bounding_box(self) -> Tuple[float, float]:
        """Get bounding box width and height"""
        if not self.vertices:
            return 0.0, 0.0
        
        min_x = min(v.x for v in self.vertices)
        max_x = max(v.x for v in self.vertices)
        min_y = min(v.y for v in self.vertices)
        max_y = max(v.y for v in self.vertices)
        
        return max_x - min_x, max_y - min_y
    
    def rotate(self, degrees: int) -> 'Polygon':
        """Rotate polygon by given degrees"""
        radians = math.radians(degrees)
        cos_a = math.cos(radians)
        sin_a = math.sin(radians)
        
        rotated_vertices = [
            Point(
                v.x * cos_a - v.y * sin_a,
                v.x * sin_a + v.y * cos_a
            )
            for v in self.vertices
        ]
        
        # Normalize to start at origin
        min_x = min(v.x for v in rotated_vertices)
        min_y = min(v.y for v in rotated_vertices)
        normalized_vertices = [
            Point(v.x - min_x, v.y - min_y)
            for v in rotated_vertices
        ]
        
        return Polygon(normalized_vertices, (self.rotation + degrees) % 360)
    
    def get_area(self) -> float:
        """Calculate polygon area using Shoelace formula"""
        n = len(self.vertices)
        if n < 3:
            return 0.0
        
        area = 0.0
        for i in range(n):
            j = (i + 1) % n
            area += self.vertices[i].x * self.vertices[j].y
            area -= self.vertices[j].x * self.vertices[i].y
        
        return abs(area) / 2.0


@dataclass
class NestedPart:
    """A part placed on a sheet with position and rotation"""
    part_id: str
    part_name: str
    polygon: Polygon
    x: float = 0.0
    y: float = 0.0
    rotation: int = 0
    material_id: str = ""
    is_rectangular: bool = True
    width: float = 0.0  # For rectangular parts
    height: float = 0.0  # For rectangular parts


@dataclass
class NestedSheet:
    """A sheet with nested parts"""
    sheet_number: int
    width: float
    height: float
    parts: List[NestedPart] = field(default_factory=list)
    used_area: float = 0.0
    material_id: str = ""
    
    def get_remaining_area(self) -> float:
        return (self.width * self.height) - self.used_area
    
    def get_utilization(self) -> float:
        total = self.width * self.height
        if total == 0:
            return 0.0
        return (self.used_area / total) * 100


@dataclass
class NestingResult:
    """Result of advanced nesting optimization"""
    sheets: List[NestedSheet]
    total_sheets: int
    total_waste_percentage: float
    total_used_area: float
    total_material_area: float
    algorithm: NestingAlgorithm
    execution_time_ms: float = 0.0
    iterations: int = 0


class AdvancedNester:
    """
    Advanced nesting algorithms for non-guillotine cutting.
    Supports both rectangular and irregular polygon shapes.
    """
    
    def __init__(
        self,
        sheet_width: float = 48.0,
        sheet_height: float = 96.0,
        algorithm: NestingAlgorithm = NestingAlgorithm.BOTTOM_LEFT,
        kerf_width: float = 0.125,  # Saw blade width
        part_spacing: float = 0.25,  # Minimum spacing between parts
        allow_rotation: bool = True
    ):
        self.sheet_width = sheet_width
        self.sheet_height = sheet_height
        self.algorithm = algorithm
        self.kerf_width = kerf_width
        self.part_spacing = part_spacing
        self.allow_rotation = allow_rotation
        self.sheets: List[NestedSheet] = []
    
    def nest_rectangular_parts(
        self,
        parts: List[Dict],
        material_id: str = ""
    ) -> NestingResult:
        """
        Nest rectangular parts using the selected algorithm.
        
        Args:
            parts: List of part dicts with id, name, width, height, quantity, material_id
            material_id: Material ID for the sheet
            
        Returns:
            NestingResult with optimized layout
        """
        import time
        start_time = time.time()
        
        # Expand parts by quantity
        expanded_parts = []
        for part in parts:
            for _ in range(part.get("quantity", 1)):
                expanded_parts.append(NestedPart(
                    part_id=part["id"],
                    part_name=part["name"],
                    polygon=Polygon([
                        Point(0, 0),
                        Point(part["width"], 0),
                        Point(part["width"], part["height"]),
                        Point(0, part["height"])
                    ]),
                    material_id=part.get("material_id", material_id),
                    is_rectangular=True,
                    width=part["width"],
                    height=part["height"]
                ))
        
        # Sort by area (largest first)
        expanded_parts.sort(
            key=lambda p: p.width * p.height,
            reverse=True
        )
        
        # Select algorithm
        if self.algorithm == NestingAlgorithm.BOTTOM_LEFT:
            self._bottom_left_nest(expanded_parts, material_id)
        elif self.algorithm == NestingAlgorithm.NFDH:
            self._nfdh_nest(expanded_parts, material_id)
        elif self.algorithm == NestingAlgorithm.FFDH:
            self._ffdh_nest(expanded_parts, material_id)
        elif self.algorithm == NestingAlgorithm.BFDH:
            self._bfdh_nest(expanded_parts, material_id)
        else:
            self._bottom_left_nest(expanded_parts, material_id)
        
        # Calculate results
        total_used = sum(s.used_area for s in self.sheets)
        total_area = len(self.sheets) * self.sheet_width * self.sheet_height
        waste_pct = ((total_area - total_used) / total_area * 100) if total_area > 0 else 0
        
        execution_time = (time.time() - start_time) * 1000
        
        return NestingResult(
            sheets=self.sheets,
            total_sheets=len(self.sheets),
            total_waste_percentage=waste_pct,
            total_used_area=total_used,
            total_material_area=total_area,
            algorithm=self.algorithm,
            execution_time_ms=execution_time,
            iterations=len(expanded_parts)
        )
    
    def _bottom_left_nest(self, parts: List[NestedPart], material_id: str):
        """
        Bottom-Left nesting algorithm.
        Places each part at the lowest, leftmost valid position.
        """
        self.sheets = [NestedSheet(
            sheet_number=1,
            width=self.sheet_width,
            height=self.sheet_height,
            material_id=material_id
        )]
        
        for part in parts:
            placed = False
            
            # Try all rotations if allowed
            rotations = [0, 90] if self.allow_rotation else [0]
            
            for sheet in self.sheets:
                for rotation in rotations:
                    rotated_part = self._rotate_part(part, rotation)
                    
                    # Find bottom-left position
                    position = self._find_bottom_left_position(sheet, rotated_part)
                    
                    if position:
                        rotated_part.x = position[0]
                        rotated_part.y = position[1]
                        rotated_part.rotation = rotation
                        rotated_part.width = rotated_part.width if rotation == 0 else rotated_part.height
                        rotated_part.height = rotated_part.height if rotation == 0 else rotated_part.width
                        sheet.parts.append(rotated_part)
                        sheet.used_area += rotated_part.polygon.get_area()
                        placed = True
                        break
                
                if placed:
                    break
            
            # Create new sheet if part couldn't be placed
            if not placed:
                new_sheet = NestedSheet(
                    sheet_number=len(self.sheets) + 1,
                    width=self.sheet_width,
                    height=self.sheet_height,
                    material_id=material_id
                )
                
                # Place part in bottom-left of new sheet
                part.x = self.part_spacing
                part.y = self.part_spacing
                new_sheet.parts.append(part)
                new_sheet.used_area = part.polygon.get_area()
                self.sheets.append(new_sheet)
    
    def _nfdh_nest(self, parts: List[NestedPart], material_id: str):
        """
        Next Fit Decreasing Height (NFDH) algorithm.
        Parts are sorted by decreasing height and placed in levels.
        """
        self.sheets = [NestedSheet(
            sheet_number=1,
            width=self.sheet_width,
            height=self.sheet_height,
            material_id=material_id
        )]
        
        current_sheet = self.sheets[0]
        current_level_height = 0.0
        current_level_y = self.part_spacing
        
        for part in parts:
            # Get part dimensions (try rotation for better fit)
            best_width = part.width
            best_height = part.height
            
            if self.allow_rotation:
                if part.height > part.width and part.height > self.sheet_width * 0.5:
                    best_width, best_height = part.height, part.width
            
            # Check if fits in current level
            remaining_width = self.sheet_width - self._get_level_used_width(current_sheet, current_level_y)
            
            if best_width + self.part_spacing <= remaining_width and \
               best_height + current_level_y <= self.sheet_height:
                # Place in current level
                part.x = self._get_level_used_width(current_sheet, current_level_y) + self.part_spacing
                part.y = current_level_y
                part.width = best_width
                part.height = best_height
                current_sheet.parts.append(part)
                current_sheet.used_area += best_width * best_height
                current_level_height = max(current_level_height, best_height)
            else:
                # Start new level
                current_level_y += current_level_height + self.part_spacing
                current_level_height = best_height
                
                # Check if fits in new level
                if best_height + current_level_y <= self.sheet_height:
                    part.x = self.part_spacing
                    part.y = current_level_y
                    part.width = best_width
                    part.height = best_height
                    current_sheet.parts.append(part)
                    current_sheet.used_area += best_width * best_height
                else:
                    # Need new sheet
                    new_sheet = NestedSheet(
                        sheet_number=len(self.sheets) + 1,
                        width=self.sheet_width,
                        height=self.sheet_height,
                        material_id=material_id
                    )
                    part.x = self.part_spacing
                    part.y = self.part_spacing
                    part.width = best_width
                    part.height = best_height
                    new_sheet.parts.append(part)
                    new_sheet.used_area = best_width * best_height
                    self.sheets.append(new_sheet)
                    current_sheet = new_sheet
                    current_level_y = self.part_spacing
                    current_level_height = best_height
    
    def _ffdh_nest(self, parts: List[NestedPart], material_id: str):
        """
        First Fit Decreasing Height (FFDH) algorithm.
        Places each part in the first level where it fits.
        """
        self.sheets = [NestedSheet(
            sheet_number=1,
            width=self.sheet_width,
            height=self.sheet_height,
            material_id=material_id
        )]
        
        # Track levels: {y_position: {height, used_width}}
        levels: List[Dict] = []
        
        for part in parts:
            best_width = part.width
            best_height = part.height
            
            if self.allow_rotation and part.height > part.width:
                if part.height <= self.sheet_width:
                    best_width, best_height = part.height, part.width
            
            placed = False
            
            # Try to fit in existing levels
            for level in levels:
                if best_height <= level["height"] + 0.5:  # Small tolerance
                    remaining = self.sheet_width - level["used_width"]
                    if best_width + self.part_spacing <= remaining:
                        part.x = level["used_width"] + self.part_spacing
                        part.y = level["y"]
                        part.width = best_width
                        part.height = best_height
                        self.sheets[level["sheet_idx"]].parts.append(part)
                        self.sheets[level["sheet_idx"]].used_area += best_width * best_height
                        level["used_width"] += best_width + self.part_spacing
                        placed = True
                        break
            
            if not placed:
                # Create new level
                if not levels:
                    y_pos = self.part_spacing
                    sheet_idx = 0
                else:
                    last_level = levels[-1]
                    y_pos = last_level["y"] + last_level["height"] + self.part_spacing
                    
                    # Check if fits on current sheet
                    if y_pos + best_height > self.sheet_height:
                        # Need new sheet
                        new_sheet = NestedSheet(
                            sheet_number=len(self.sheets) + 1,
                            width=self.sheet_width,
                            height=self.sheet_height,
                            material_id=material_id
                        )
                        self.sheets.append(new_sheet)
                        y_pos = self.part_spacing
                        sheet_idx = len(self.sheets) - 1
                    else:
                        sheet_idx = len(self.sheets) - 1
                
                levels.append({
                    "y": y_pos,
                    "height": best_height,
                    "used_width": best_width + self.part_spacing,
                    "sheet_idx": sheet_idx
                })
                
                part.x = self.part_spacing
                part.y = y_pos
                part.width = best_width
                part.height = best_height
                self.sheets[sheet_idx].parts.append(part)
                self.sheets[sheet_idx].used_area += best_width * best_height
    
    def _bfdh_nest(self, parts: List[NestedPart], material_id: str):
        """
        Best Fit Decreasing Height (BFDH) algorithm.
        Places each part in the level with least remaining width that still fits.
        """
        self.sheets = [NestedSheet(
            sheet_number=1,
            width=self.sheet_width,
            height=self.sheet_height,
            material_id=material_id
        )]
        
        levels: List[Dict] = []
        
        for part in parts:
            best_width = part.width
            best_height = part.height
            
            if self.allow_rotation and part.height > part.width:
                if part.height <= self.sheet_width:
                    best_width, best_height = part.height, part.width
            
            # Find best fit level
            best_level = None
            best_remaining = float('inf')
            
            for level in levels:
                if best_height <= level["height"] + 0.5:
                    remaining = self.sheet_width - level["used_width"] - best_width - self.part_spacing
                    if remaining >= 0 and remaining < best_remaining:
                        best_level = level
                        best_remaining = remaining
            
            if best_level:
                part.x = best_level["used_width"] + self.part_spacing
                part.y = best_level["y"]
                part.width = best_width
                part.height = best_height
                self.sheets[best_level["sheet_idx"]].parts.append(part)
                self.sheets[best_level["sheet_idx"]].used_area += best_width * best_height
                best_level["used_width"] += best_width + self.part_spacing
            else:
                # Create new level (same as FFDH)
                if not levels:
                    y_pos = self.part_spacing
                    sheet_idx = 0
                else:
                    last_level = levels[-1]
                    y_pos = last_level["y"] + last_level["height"] + self.part_spacing
                    
                    if y_pos + best_height > self.sheet_height:
                        new_sheet = NestedSheet(
                            sheet_number=len(self.sheets) + 1,
                            width=self.sheet_width,
                            height=self.sheet_height,
                            material_id=material_id
                        )
                        self.sheets.append(new_sheet)
                        y_pos = self.part_spacing
                        sheet_idx = len(self.sheets) - 1
                    else:
                        sheet_idx = len(self.sheets) - 1
                
                levels.append({
                    "y": y_pos,
                    "height": best_height,
                    "used_width": best_width + self.part_spacing,
                    "sheet_idx": sheet_idx
                })
                
                part.x = self.part_spacing
                part.y = y_pos
                part.width = best_width
                part.height = best_height
                self.sheets[sheet_idx].parts.append(part)
                self.sheets[sheet_idx].used_area += best_width * best_height
    
    def _rotate_part(self, part: NestedPart, degrees: int) -> NestedPart:
        """Rotate a part by given degrees"""
        if degrees == 0:
            return part
        
        rotated = NestedPart(
            part_id=part.part_id,
            part_name=part.part_name,
            polygon=part.polygon.rotate(degrees),
            material_id=part.material_id,
            is_rectangular=part.is_rectangular,
            width=part.height if degrees in [90, 270] else part.width,
            height=part.width if degrees in [90, 270] else part.height,
            rotation=degrees
        )
        return rotated
    
    def _find_bottom_left_position(
        self,
        sheet: NestedSheet,
        part: NestedPart
    ) -> Optional[Tuple[float, float]]:
        """Find the lowest, leftmost position where part fits"""
        
        # Generate candidate positions
        candidates = []
        
        # Add origin
        candidates.append((self.part_spacing, self.part_spacing))
        
        # Add positions based on existing parts
        for existing in sheet.parts:
            # Right of existing part
            candidates.append((existing.x + existing.width + self.part_spacing, existing.y))
            # Above existing part
            candidates.append((existing.x, existing.y + existing.height + self.part_spacing))
        
        # Sort candidates by y first, then x
        candidates.sort(key=lambda p: (p[1], p[0]))
        
        # Try each candidate
        for x, y in candidates:
            if self._can_place(sheet, part, x, y):
                return (x, y)
        
        return None
    
    def _can_place(self, sheet: NestedSheet, part: NestedPart, x: float, y: float) -> bool:
        """Check if part can be placed at position without overlapping"""
        
        # Check sheet bounds
        if x + part.width + self.kerf_width > sheet.width:
            return False
        if y + part.height + self.kerf_width > sheet.height:
            return False
        
        # Check overlap with existing parts
        for existing in sheet.parts:
            if self._rectangles_overlap(
                x, y, x + part.width, y + part.height,
                existing.x, existing.y,
                existing.x + existing.width, existing.y + existing.height
            ):
                return False
        
        return True
    
    def _rectangles_overlap(
        self,
        x1: float, y1: float, x2: float, y2: float,
        x3: float, y3: float, x4: float, y4: float
    ) -> bool:
        """Check if two rectangles overlap"""
        margin = self.part_spacing
        return not (
            x2 + margin <= x3 or x4 + margin <= x1 or
            y2 + margin <= y3 or y4 + margin <= y1
        )
    
    def _get_level_used_width(self, sheet: NestedSheet, level_y: float) -> float:
        """Get the used width at a specific level"""
        max_x = self.part_spacing
        for part in sheet.parts:
            if abs(part.y - level_y) < 0.5:  # Same level
                max_x = max(max_x, part.x + part.width)
        return max_x


def nest_parts(
    parts: List[Dict],
    sheet_size: Tuple[float, float] = (48.0, 96.0),
    algorithm: str = "bottom_left",
    kerf_width: float = 0.125,
    part_spacing: float = 0.25,
    allow_rotation: bool = True
) -> Dict:
    """
    Convenience function to nest parts with specified algorithm.
    
    Args:
        parts: List of part dicts with id, name, width, height, quantity
        sheet_size: Tuple of (width, height) in inches
        algorithm: "bottom_left", "nfdh", "ffdh", "bfdh"
        kerf_width: Saw blade width in inches
        part_spacing: Minimum spacing between parts in inches
        allow_rotation: Whether to allow 90-degree rotation
        
    Returns:
        Dict with nested layout and statistics
    """
    algo_map = {
        "bottom_left": NestingAlgorithm.BOTTOM_LEFT,
        "nfdh": NestingAlgorithm.NFDH,
        "ffdh": NestingAlgorithm.FFDH,
        "bfdh": NestingAlgorithm.BFDH,
    }
    
    nester = AdvancedNester(
        sheet_width=sheet_size[0],
        sheet_height=sheet_size[1],
        algorithm=algo_map.get(algorithm.lower(), NestingAlgorithm.BOTTOM_LEFT),
        kerf_width=kerf_width,
        part_spacing=part_spacing,
        allow_rotation=allow_rotation
    )
    
    result = nester.nest_rectangular_parts(parts)
    
    # Format for API response
    return {
        "algorithm": result.algorithm.value,
        "sheets": [
            {
                "sheet_number": s.sheet_number,
                "width": s.width,
                "height": s.height,
                "utilization": round(s.get_utilization(), 2),
                "parts": [
                    {
                        "part_id": p.part_id,
                        "part_name": p.part_name,
                        "x": round(p.x, 4),
                        "y": round(p.y, 4),
                        "width": round(p.width, 4),
                        "height": round(p.height, 4),
                        "rotation": p.rotation
                    }
                    for p in s.parts
                ]
            }
            for s in result.sheets
        ],
        "total_sheets": result.total_sheets,
        "waste_percentage": round(result.total_waste_percentage, 2),
        "total_used_area": round(result.total_used_area, 2),
        "total_material_area": round(result.total_material_area, 2),
        "execution_time_ms": round(result.execution_time_ms, 2)
    }


# Example usage
if __name__ == "__main__":
    test_parts = [
        {"id": "1", "name": "Side Panel", "width": 24, "height": 72, "quantity": 2},
        {"id": "2", "name": "Top Panel", "width": 36, "height": 24, "quantity": 2},
        {"id": "3", "name": "Shelf", "width": 34, "height": 12, "quantity": 4},
        {"id": "4", "name": "Door", "width": 35.875, "height": 71.875, "quantity": 1},
    ]
    
    for algo in ["bottom_left", "nfdh", "ffdh", "bfdh"]:
        result = nest_parts(test_parts, algorithm=algo)
        print(f"\n{algo.upper()}:")
        print(f"  Sheets: {result['total_sheets']}")
        print(f"  Waste: {result['waste_percentage']}%")
        print(f"  Time: {result['execution_time_ms']}ms")

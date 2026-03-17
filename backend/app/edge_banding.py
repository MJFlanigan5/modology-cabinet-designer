"""
Phase 4: Edge Banding Optimizer
Calculates edge banding requirements and optimizes application.
"""

from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
from decimal import Decimal


class EdgeBandingType(str, Enum):
    WOOD_VENEER = "wood_veneer"
    PVC = "pvc"
    MELAMINE = "melamine"
    ABS = "abs"
    METAL = "metal"


class EdgePosition(str, Enum):
    FRONT = "front"  # Visible front edge
    BACK = "back"    # Back edge
    LEFT = "left"
    RIGHT = "right"
    TOP = "top"
    BOTTOM = "bottom"


@dataclass
class EdgeBandingSpec:
    """Specification for edge banding material."""
    type: EdgeBandingType
    width: float  # Width of the band (typically 13mm, 22mm, 45mm)
    thickness: float  # Thickness (0.4mm to 3mm)
    length_per_roll: float = 250.0  # Length per roll in feet
    color: Optional[str] = None
    wood_species: Optional[str] = None  # For wood veneer
    pre_glued: bool = False
    price_per_roll: float = 25.0
    
    def coverage_per_roll(self) -> float:
        """Returns linear feet covered per roll."""
        return self.length_per_roll


@dataclass
class EdgeRequirement:
    """Edge banding requirement for a component."""
    component_id: str
    component_name: str
    edge_position: EdgePosition
    edge_length: float  # Length in inches
    visible: bool  # Whether this edge is visible
    banding_type: Optional[EdgeBandingType] = None
    banding_width: float = 13.0  # Default 13mm


@dataclass
class ComponentEdgeAnalysis:
    """Edge banding analysis for a single component."""
    component_id: str
    component_name: str
    width: float
    height: float
    thickness: float
    edges: List[EdgeRequirement]
    total_edge_length: float
    visible_edge_length: float
    
    def to_dict(self) -> Dict:
        return {
            "component_id": self.component_id,
            "component_name": self.component_name,
            "dimensions": {
                "width": self.width,
                "height": self.height,
                "thickness": self.thickness,
            },
            "edges": [
                {
                    "position": e.edge_position.value,
                    "length": e.edge_length,
                    "visible": e.visible,
                    "banding_type": e.banding_type.value if e.banding_type else None,
                }
                for e in self.edges
            ],
            "total_edge_length": round(self.total_edge_length, 2),
            "visible_edge_length": round(self.visible_edge_length, 2),
        }


@dataclass
class EdgeBandingSummary:
    """Summary of all edge banding requirements."""
    components: List[ComponentEdgeAnalysis]
    total_linear_inches: float
    total_linear_feet: float
    visible_linear_feet: float
    hidden_linear_feet: float
    rolls_needed: Dict[str, int]  # banding_type -> count
    estimated_cost: float
    waste_factor: float = 1.1  # 10% waste allowance
    
    def to_dict(self) -> Dict:
        return {
            "components": [c.to_dict() for c in self.components],
            "totals": {
                "total_linear_inches": round(self.total_linear_inches, 2),
                "total_linear_feet": round(self.total_linear_feet, 2),
                "visible_linear_feet": round(self.visible_linear_feet, 2),
                "hidden_linear_feet": round(self.hidden_linear_feet, 2),
                "with_waste_allowance": round(self.total_linear_feet * self.waste_factor, 2),
            },
            "materials_needed": self.rolls_needed,
            "estimated_cost": round(self.estimated_cost, 2),
            "waste_factor": self.waste_factor,
        }


class EdgeBandingOptimizer:
    """
    Analyzes cabinet components and calculates edge banding requirements.
    Optimizes for material usage and cost.
    """
    
    # Standard edge banding widths (mm)
    STANDARD_WIDTHS = {
        "thin": 13,      # 13mm (1/2") - standard for 3/4" plywood
        "medium": 22,    # 22mm (7/8") - for thicker materials
        "thick": 45,     # 45mm (1-3/4") - for exposed edges
    }
    
    def __init__(
        self,
        default_banding: EdgeBandingSpec = None,
        include_hidden_edges: bool = False,
        waste_factor: float = 1.1,
    ):
        self.default_banding = default_banding or EdgeBandingSpec(
            type=EdgeBandingType.WOOD_VENEER,
            width=13.0,
            thickness=0.5,
        )
        self.include_hidden_edges = include_hidden_edges
        self.waste_factor = waste_factor
    
    def analyze_component(
        self,
        component: Dict,
        edge_config: Optional[Dict] = None
    ) -> ComponentEdgeAnalysis:
        """
        Analyze a single component for edge banding requirements.
        
        Args:
            component: Dict with id, name, width, height, thickness, edge_banding
            edge_config: Optional dict specifying which edges need banding
        """
        component_id = component.get("id", "unknown")
        component_name = component.get("name", "Component")
        width = float(component.get("width", 0))
        height = float(component.get("height", 0))
        thickness = float(component.get("thickness", 0.75))
        
        # Parse edge banding configuration
        edge_banding_config = component.get("edge_banding", "")
        
        edges = []
        total_length = 0.0
        visible_length = 0.0
        
        # Determine which edges need banding
        edges_to_band = self._parse_edge_config(edge_banding_config, edge_config)
        
        # Calculate edge lengths
        edge_lengths = {
            EdgePosition.FRONT: width,  # Front edge (width)
            EdgePosition.BACK: width,   # Back edge
            EdgePosition.LEFT: height,  # Left edge (height)
            EdgePosition.RIGHT: height, # Right edge
            EdgePosition.TOP: width,    # Top edge (width)
            EdgePosition.BOTTOM: width, # Bottom edge
        }
        
        for position, needs_banding in edges_to_band.items():
            if needs_banding or self.include_hidden_edges:
                edge_len = edge_lengths.get(position, 0)
                is_visible = needs_banding  # Visible edges are those specified
                
                edge = EdgeRequirement(
                    component_id=component_id,
                    component_name=component_name,
                    edge_position=position,
                    edge_length=edge_len,
                    visible=is_visible,
                    banding_type=self.default_banding.type if is_visible else None,
                )
                edges.append(edge)
                total_length += edge_len
                if is_visible:
                    visible_length += edge_len
        
        return ComponentEdgeAnalysis(
            component_id=component_id,
            component_name=component_name,
            width=width,
            height=height,
            thickness=thickness,
            edges=edges,
            total_edge_length=total_length,
            visible_edge_length=visible_length,
        )
    
    def _parse_edge_config(
        self,
        config: str,
        override: Optional[Dict] = None
    ) -> Dict[EdgePosition, bool]:
        """
        Parse edge banding configuration string.
        
        Formats:
        - "all" - all edges
        - "none" - no edges
        - "front,back,left" - specific edges
        - "visible" - only visible edges (front, left, right for exposed panels)
        """
        defaults = {pos: False for pos in EdgePosition}
        
        if override:
            for pos in EdgePosition:
                if pos.value in override:
                    defaults[pos] = override[pos.value]
            return defaults
        
        config = config.lower().strip() if config else "none"
        
        if config == "all":
            return {pos: True for pos in EdgePosition}
        
        if config == "none" or not config:
            return defaults
        
        if config == "visible":
            # Typical visible edges
            return {
                EdgePosition.FRONT: True,
                EdgePosition.LEFT: True,
                EdgePosition.RIGHT: True,
                EdgePosition.TOP: False,
                EdgePosition.BOTTOM: False,
                EdgePosition.BACK: False,
            }
        
        # Parse comma-separated list
        result = defaults.copy()
        for edge_name in config.split(","):
            edge_name = edge_name.strip()
            for pos in EdgePosition:
                if pos.value == edge_name:
                    result[pos] = True
                    break
        
        return result
    
    def optimize(
        self,
        components: List[Dict],
        edge_configs: Optional[Dict[str, Dict]] = None
    ) -> EdgeBandingSummary:
        """
        Analyze all components and optimize edge banding requirements.
        
        Args:
            components: List of component dicts
            edge_configs: Optional dict mapping component_id to edge config
        """
        analyses = []
        total_inches = 0.0
        visible_inches = 0.0
        
        for component in components:
            component_id = component.get("id", "unknown")
            edge_config = edge_configs.get(component_id) if edge_configs else None
            
            analysis = self.analyze_component(component, edge_config)
            analyses.append(analysis)
            
            total_inches += analysis.total_edge_length
            visible_inches += analysis.visible_edge_length
        
        # Convert to feet
        total_feet = total_inches / 12.0
        visible_feet = visible_inches / 12.0
        hidden_feet = (total_inches - visible_inches) / 12.0
        
        # Calculate rolls needed
        coverage_per_roll = self.default_banding.coverage_per_roll()
        feet_needed = total_feet * self.waste_factor
        rolls_needed = math.ceil(feet_needed / coverage_per_roll)
        
        rolls_by_type = {
            self.default_banding.type.value: rolls_needed,
        }
        
        # Estimate cost
        estimated_cost = rolls_needed * self.default_banding.price_per_roll
        
        return EdgeBandingSummary(
            components=analyses,
            total_linear_inches=total_inches,
            total_linear_feet=total_feet,
            visible_linear_feet=visible_feet,
            hidden_linear_feet=hidden_feet,
            rolls_needed=rolls_by_type,
            estimated_cost=estimated_cost,
            waste_factor=self.waste_factor,
        )
    
    def suggest_banding_width(self, thickness: float) -> float:
        """Suggest appropriate banding width based on material thickness."""
        if thickness <= 0.5:  # 1/2" or thinner
            return self.STANDARD_WIDTHS["thin"]
        elif thickness <= 0.75:  # 3/4"
            return self.STANDARD_WIDTHS["thin"]
        elif thickness <= 1.0:  # 1"
            return self.STANDARD_WIDTHS["medium"]
        else:
            return self.STANDARD_WIDTHS["thick"]


import math


def calculate_edge_banding(
    components: List[Dict],
    banding_type: str = "wood_veneer",
    include_hidden: bool = False,
) -> Dict:
    """
    Convenience function to calculate edge banding requirements.
    
    Args:
        components: List of component dicts
        banding_type: Type of edge banding (wood_veneer, pvc, melamine, abs, metal)
        include_hidden: Include hidden edges in calculation
        
    Returns:
        Dict with edge banding summary
    """
    banding_spec = EdgeBandingSpec(
        type=EdgeBandingType(banding_type),
        width=13.0,
        thickness=0.5,
    )
    
    optimizer = EdgeBandingOptimizer(
        default_banding=banding_spec,
        include_hidden_edges=include_hidden,
    )
    
    result = optimizer.optimize(components)
    return result.to_dict()


# Example usage
if __name__ == "__main__":
    test_components = [
        {"id": "1", "name": "Side Panel", "width": 24, "height": 72, "thickness": 0.75, "edge_banding": "front"},
        {"id": "2", "name": "Shelf", "width": 22.5, "height": 11.5, "thickness": 0.75, "edge_banding": "front"},
        {"id": "3", "name": "Door", "width": 12, "height": 30, "thickness": 0.75, "edge_banding": "all"},
    ]
    
    result = calculate_edge_banding(test_components)
    print(f"Total linear feet: {result['totals']['total_linear_feet']}")
    print(f"Visible edges: {result['totals']['visible_linear_feet']}")
    print(f"Rolls needed: {result['materials_needed']}")
    print(f"Estimated cost: ${result['estimated_cost']}")

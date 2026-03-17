"""
G-code generator for CNC machines
Generates G-code for ShopBot, Shapeoko, GRBL, and other CNC machines
"""

from typing import List, Dict
from dataclasses import dataclass

@dataclass
class GCodeConfig:
    """Configuration for G-code generation"""
    z_safe_height: float = 5.0  # Height to move to before rapid moves
    feed_rate: float = 100.0  # Feed rate for cutting (mm/min)
    plunge_rate: float = 50.0  # Plunge rate (mm/min)
    rapid_feed: float = 500.0  # Rapid travel feed rate
    spindle_speed: int = 12000  # RPM
    material_thickness: float = 18.0  # mm
    pass_depth: float = 3.0  # Cut depth per pass (mm)

class GCodeGenerator:
    """Generate G-code for CNC machines"""
    
    def __init__(self, config: GCodeConfig = None):
        self.config = config or GCodeConfig()
        self.gcode_lines = []
        
    def add_comment(self, comment: str):
        """Add comment to G-code"""
        self.gcode_lines.append(f"({comment})")
        
    def add_header(self):
        """Add G-code header"""
        self.add_comment("Modology Cabinet Designer - G-code for CNC")
        self.add_comment(f"Generated: {self._get_timestamp()}")
        self.gcode_lines.append("")  # Empty line
        self.gcode_lines.append("G20")  # Inch mode
        self.gcode_lines.append("G90")  # Absolute positioning
        self.gcode_lines.append("")  # Empty line
        
    def add_footer(self):
        """Add G-code footer"""
        self.add_comment("End of G-code")
        self.gcode_lines.append("M05")  # Spindle off
        self.gcode_lines.append("G00 X0 Y0 Z20")  # Move to home position
        self.gcode_lines.append("")  # Empty line
        self.gcode_lines.append("M02")  # Program end
        
    def move_to_safe_z(self):
        """Move Z to safe height"""
        self.gcode_lines.append(f"G00 Z{self.config.z_safe_height}")
        
    def rapid_move(self, x: float, y: float):
        """Rapid move to X, Y"""
        self.move_to_safe_z()
        self.gcode_lines.append(f"G00 X{x:.4f} Y{y:.4f}")
        
    def move_to_z(self, z: float):
        """Move Z to specified position"""
        self.gcode_lines.append(f"G01 Z{z:.4f} F{self.config.plunge_rate}")
        
    def plunge(self):
        """Plunge into material"""
        target_z = -self.config.pass_depth
        self.move_to_z(target_z)
        
    def retract(self):
        """Retract Z to safe height"""
        self.move_to_safe_z()
        
    def spindle_on(self):
        """Turn on spindle"""
        self.gcode_lines.append(f"M03 S{self.config.spindle_speed}")
        self.gcode_lines.append(f"G04 P2")  # Dwell for 2 seconds
        
    def spindle_off(self):
        """Turn off spindle"""
        self.gcode_lines.append("M05")
        
    def set_feed_rate(self, feed: float):
        """Set feed rate"""
        self.gcode_lines.append(f"F{feed:.1f}")
        
    def cut_line(self, x1: float, y1: float, x2: float, y2: float):
        """Cut a straight line"""
        # Rapid to start position
        self.rapid_move(x1, y1)
        # Plunge
        self.spindle_on()
        self.plunge()
        # Cut to end position
        self.set_feed_rate(self.config.feed_rate)
        self.gcode_lines.append(f"G01 X{x2:.4f} Y{y2:.4f}")
        # Retract
        self.retract()
        self.spindle_off()
        
    def cut_rectangle(self, x: float, y: float, width: float, height: float, multiple_passes: bool = False):
        """Cut a rectangle (pocket or outline)"""
        x2 = x + width
        y2 = y + height
        
        if multiple_passes:
            # Pocket cut (multiple passes)
            num_passes = int(self.config.material_thickness / self.config.pass_depth)
            pass_depth = self.config.material_thickness / num_passes
            
            for pass_num in range(num_passes):
                current_depth = -((pass_num + 1) * pass_depth)
                self._cut_rect_at_depth(x, y, x2, y2, current_depth)
                if pass_num < num_passes - 1:
                    # Retract between passes
                    self.move_to_safe_z()
        else:
            # Single pass outline cut
            self._cut_rect_at_depth(x, y, x2, y2, -self.config.material_thickness)
            
    def _cut_rect_at_depth(self, x: float, y: float, x2: float, y2: float, depth: float):
        """Cut rectangle at specific depth"""
        # Move to start position
        self.rapid_move(x, y)
        # Move to depth
        self.spindle_on()
        self.gcode_lines.append(f"G01 Z{depth:.4f} F{self.config.plunge_rate}")
        # Cut rectangle
        self.gcode_lines.append(f"G01 X{x2:.4f} F{self.config.feed_rate}")
        self.gcode_lines.append(f"G01 Y{y2:.4f}")
        self.gcode_lines.append(f"G01 X{x:.4f}")
        self.gcode_lines.append(f"G01 Y{y:.4f}")
        # Retract
        self.move_to_safe_z()
        self.spindle_off()
        
    def cut_sheet_cuts(self, cuts: List[Dict]):
        """
        Cut all pieces from a sheet
        cuts: List of dicts with x, y, width, height, partName
        """
        self.add_comment(f"Cutting {len(cuts)} pieces")
        self.gcode_lines.append("")
        
        for i, cut in enumerate(cuts):
            self.add_comment(f"Piece {i+1}: {cut['partName']}")
            # Cut rectangle (outline only)
            self.cut_rectangle(
                x=cut['x'],
                y=cut['y'],
                width=cut['width'],
                height=cut['height'],
                multiple_passes=False
            )
            # Move to safe position between cuts
            self.move_to_safe_z()
            self.gcode_lines.append("")
            
    def generate(self, cuts: List[Dict]) -> str:
        """Generate complete G-code"""
        self.add_header()
        self.cut_sheet_cuts(cuts)
        self.add_footer()
        return "\n".join(self.gcode_lines)
        
    def generate_from_cutlist(self, cutlist_data: Dict) -> str:
        """Generate G-code from cut list response"""
        cuts = []
        for sheet in cutlist_data.get('cutList', []):
            for cut in sheet.get('cuts', []):
                cuts.append({
                    'x': cut['x'],
                    'y': cut['y'],
                    'width': cut['width'],
                    'height': cut['height'],
                    'partName': f"{cut['partName']}_{cut['partId']}"
                })
        return self.generate(cuts)
        
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def generate_gcode(cutlist_data: Dict, config: GCodeConfig = None) -> str:
    """
    Generate G-code from cut list data
    
    Args:
        cutlist_data: Cut list response from backend
        config: Optional G-code configuration
        
    Returns:
        G-code string
    """
    generator = GCodeGenerator(config)
    return generator.generate_from_cutlist(cutlist_data)


def generate_gcode_preview(cutlist_data: Dict) -> List[Dict]:
    """
    Generate preview data for G-code (for UI display)
    
    Returns:
        List of cutting operations with metadata
    """
    operations = []
    op_num = 1
    
    for sheet in cutlist_data.get('cutList', []):
        for cut in sheet.get('cuts', []):
            operations.append({
                'operation': op_num,
                'type': 'rect_cut',
                'name': f"{cut['partName']}_{cut['partId']}",
                'x': cut['x'],
                'y': cut['y'],
                'width': cut['width'],
                'height': cut['height'],
                'sheet': sheet['sheetNumber'],
                'commands': [
                    f"Rapid to ({cut['x']:.2f}, {cut['y']:.2f})",
                    f"Plunge to {-18.0:.1f} mm",
                    f"Cut rectangle ({cut['width']:.2f}\" x {cut['height']:.2f}\")",
                    f"Retract Z"
                ]
            })
            op_num += 1
            
    return operations
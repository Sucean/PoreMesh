#!/usr/bin/env python3
"""
Universal OpenFOAM dictionary file generator
"""

from pathlib import Path
from typing import Any, Dict, List, Union
from dataclasses import dataclass
from .stl_analyzer import STLAnalyzer
import numpy as np


@dataclass
class OpenFOAMDimension:
    """OpenFOAM dimension specification [mass length time temperature ...]"""
    mass: int = 0
    length: int = 0  
    time: int = 0
    temperature: int = 0
    moles: int = 0
    current: int = 0
    luminous_intensity: int = 0
    
    def __str__(self):
        return f"[{self.mass} {self.length} {self.time} {self.temperature} {self.moles} {self.current} {self.luminous_intensity}]"

class OpenFOAMDict:
    """
    Universal OpenFOAM dictionary generator
    """
    
    def __init__(self, class_type: str = "dictionary", object_name: str = "file"):
        self.content = []
        self.indent_level = 0
        self.class_type = class_type
        self.object_name = object_name
    
    def _format_value(self, value: Any) -> str:
        """Format value according to OpenFOAM rules"""
        if isinstance(value, str):
            # Check if it's a single word (no spaces, no special chars)
            if " " in value or "-" in value or value.lower() in ["true", "false", "yes", "no"]:
                return f'{value}'
            else:
                return value
        elif isinstance(value, bool):
            return "true" if value else "false"
        elif isinstance(value, (int, float)):
            return str(value)
        elif isinstance(value, (list, tuple, np.ndarray)):
            if len(value) == 0:
                return "()"
            # Check if it's a vector (3 elements, all numeric)
            if len(value) == 3 and all(isinstance(x, (int, float)) for x in value):
                return f"({value[0]} {value[1]} {value[2]})"
            elif len(value) == 7 and all(isinstance(x, (int, float)) for x in value):
                return f"[{value[0]} {value[1]} {value[2]} {value[3]} {value[4]} {value[5]} {value[6]}]"
            else:
                items = " ".join(str(self._format_value(x)).strip('"') for x in value)
                return f"({items})"
        elif isinstance(value, OpenFOAMDimension):
            return str(value)
        elif isinstance(value, dict):
            # This is a sub-dictionary
            sub_dict = OpenFOAMDict()
            for k, v in value.items():
                sub_dict.add_entry(k, v)
            return str(sub_dict)
        else:
            return str(value)
    
    def add_comment(self, comment: str, style: str = "//"):
        """Add comment to dictionary"""
        indent = "    " * self.indent_level
        if style == "//":
            self.content.append(f"{indent}// {comment}")
        else:
            self.content.append(f"{indent}/* {comment} */")
    
    def add_header(self, version: str = "2.0", format_type: str = "ascii", 
                   location: str = "", object_name: str = None):
        """Add standard OpenFOAM header"""
        object_name = object_name or self.object_name
        
        header_dict = {
            "version": version,
            "format": format_type,
            "class": self.class_type,
            "object": object_name
        }
        
        if location:
            header_dict["location"] = location
            
        self.add_comment("-" * 70, "/*")
        self.add_comment(f"OpenFOAM Dictionary: {object_name}")
        self.add_comment("-" * 70, "*/")
        self.add_entry("FoamFile", header_dict)
    
    def add_entry(self, key: str, value: Any, comment: str = None, terminator = ";"):
        """Add key-value entry to dictionary"""
        indent = "    " * self.indent_level
        formatted_value = self._format_value(value)
        
        line = f"{indent}{key} {formatted_value}{terminator}"
        
        if comment:
            line += f" // {comment}"
            
        self.content.append(line)
    
    def start_dict(self, key: str):
        """Start a sub-dictionary"""
        indent = "    " * self.indent_level
        self.content.append(f"{indent}{key}")
        self.content.append(f"{indent}{{")
        self.indent_level += 1
    
    def end_dict(self, terminator=""):
        """End current sub-dictionary"""
        if self.indent_level > 0:
            self.indent_level -= 1
            indent = "    " * self.indent_level
            self.content.append(f"{indent}}}{terminator}")

    def start_list(self, key: str):
        """Start a sub-dictionary"""
        indent = "    " * self.indent_level
        self.content.append(f"{indent}{key}")
        self.content.append(f"{indent}(")
        self.indent_level += 1
    
    def end_list(self):
        """End current sub-dictionary"""
        if self.indent_level > 0:
            self.indent_level -= 1
            indent = "    " * self.indent_level
            self.content.append(f"{indent});")

    def add_raw_line(self, line: str):
        """ Add raw line """
        indent = "    " * self.indent_level
        self.content.append(f"{indent}{line}")
    
    def add_item(self, key: str, item: List[Any], comment: str = None):
        """Add a list entry"""
        self.add_entry("", item, comment, terminator = "")
    
    def add_vector(self, key: str, x: float, y: float, z: float, comment: str = None):
        """Add a vector entry"""
        self.add_entry(key, (x, y, z), comment, terminator = "")

    def add_boundary(self, name: str, typ: str, faces: tuple):
        self.start_dict(name)
        self.add_entry("type", typ)
        self.start_list("faces")

        if isinstance(faces, tuple) and all(isinstance(x, int) for x in faces):
            self.add_item(" ", faces)
        else:
            for face in faces:
                self.add_item(" ", face)

        self.end_list()
        self.end_dict()
    
    def add_dimensioned_value(self, key: str, value: Any, dimensions: OpenFOAMDimension, comment: str = None):
        """Add dimensioned value with units"""
        formatted_value = f"{dimensions} {self._format_value(value)}"
        self.add_entry(key, formatted_value, comment)
    
    def __str__(self) -> str:
        """Return formatted dictionary as string"""
        return "\n".join(self.content)
    
    def write(self, filepath: Path):
        """Write dictionary to file"""
        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, 'w') as f:
            f.write(str(self))
        
        print(f"Written OpenFOAM dictionary: {filepath}")



#################################################################

# src/openfoam_builder.py
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field

@dataclass
class MeshSettings:
    """Clean, typed mesh settings"""
    background_scale: float = 1.2  # Background mesh as % of geometry size
    boundary_layer: bool = True
    boundary_layers: int = 3
    expansion_ratio: float = 1.2
    min_cell_size: float = 0.01
    max_cell_size: float = 0.1

@dataclass  
class SolverSettings:
    """Clean, typed solver settings"""
    solver: str = "icoFoam"
    start_time: float = 0
    end_time: float = 10
    time_step: float = 0.001
    write_interval: float = 1
    max_co: float = 0.5  # Maximum Courant number

@dataclass
class BoundarySettings:
    """Clean boundary condition specification"""
    name: str
    type: str  # patch, wall, empty, etc.
    condition: Dict[str, Any]  # Actual boundary condition

class OpenFOAMCaseBuilder:
    """
    Clean, fluent interface for building OpenFOAM cases
    """
    
    def __init__(self, case_name: str, base_path: Path):
        self.case_name = case_name
        self.base_path = Path(base_path)
        self.case_path = self.base_path / case_name
        
        # Initialize with sensible defaults
        self.mesh_settings = MeshSettings()
        self.solver_settings = SolverSettings()
        self.geometry = None
        self.boundaries: List[BoundarySettings] = []
        self.fields: Dict[str, Any] = {}
        
        self.stl_analyzer = STLAnalyzer()
    
    def with_stl_geometry(self, stl_path: Path) -> 'OpenFOAMCaseBuilder':
        """Set up case based on STL geometry"""
        self.geometry = self.stl_analyzer.analyze_stl(stl_path)
        return self
    
    def with_mesh_settings(self, **kwargs) -> 'OpenFOAMCaseBuilder':
        """Configure mesh settings"""
        for key, value in kwargs.items():
            if hasattr(self.mesh_settings, key):
                setattr(self.mesh_settings, key, value)
        return self
    
    def with_solver_settings(self, **kwargs) -> 'OpenFOAMCaseBuilder':
        """Configure solver settings"""
        for key, value in kwargs.items():
            if hasattr(self.solver_settings, key):
                setattr(self.solver_settings, key, value)
        return self
    
    def with_boundary(self, name: str, boundary_type: str, **condition_kwargs) -> 'OpenFOAMCaseBuilder':
        """Add a boundary condition"""
        self.boundaries.append(BoundarySettings(
            name=name,
            type=boundary_type,
            condition=condition_kwargs
        ))
        return self
    
    def with_field(self, field_name: str, internal_field: Any, **boundary_conditions) -> 'OpenFOAMCaseBuilder':
        """Add a field with boundary conditions"""
        self.fields[field_name] = {
            'internalField': internal_field,
            'boundaryField': boundary_conditions
        }
        return self
    
    def build_block_mesh(self) -> OpenFOAMDict: # REDACTED?
        """Build blockMeshDict based on STL geometry"""
        if not self.geometry:
            raise ValueError("No geometry defined. Call with_stl_geometry() first.")
        
        bounds = self.geometry.bounds
        scale = self.mesh_settings.background_scale
        
        # Create slightly larger background mesh
        x_min, x_max = bounds[0] * scale, bounds[1] * scale
        y_min, y_max = bounds[2] * scale, bounds[3] * scale  
        z_min, z_max = bounds[4] * scale, bounds[5] * scale
        
        vertices = [
            (x_min, y_min, z_min),  # 0
            (x_max, y_min, z_min),  # 1
            (x_max, y_max, z_min),  # 2
            (x_min, y_max, z_min),  # 3
            (x_min, y_min, z_max),  # 4
            (x_max, y_min, z_max),  # 5
            (x_max, y_max, z_max),  # 6
            (x_min, y_max, z_max),  # 7
        ]
        
        cells_x, cells_y, cells_z = self.stl_analyzer.get_mesh_resolution(
            self.geometry, self.mesh_settings.max_cell_size
        )
        
        mesh_dict = OpenFOAMDict("dictionary", "blockMeshDict")
        mesh_dict.add_header(location="system")
        mesh_dict.add_entry("convertToMeters", 1.0)
        
        # Vertices
        mesh_dict.start_dict("vertices")
        for i, vertex in enumerate(vertices):
            mesh_dict.add_entry("", vertex, f"vertex {i}")
        mesh_dict.end_dict()
        
        # Single block
        mesh_dict.start_dict("blocks")
        mesh_dict.add_entry("hex", [0, 1, 2, 3, 4, 5, 6, 7])
        mesh_dict.add_entry("", (cells_x, cells_y, cells_z), "cell count")
        mesh_dict.add_entry("", "simpleGrading", "grading")
        mesh_dict.add_entry("", (1, 1, 1), "grading factors")
        mesh_dict.end_dict()
        
        # Boundaries
        mesh_dict.start_dict("boundary")
        
        # Automatically create boundaries based on geometry
        boundary_faces = {
            "inlet": [(0, 4, 7, 3)],    # x-min face
            "outlet": [(1, 2, 6, 5)],   # x-max face  
            "lowerWall": [(0, 1, 5, 4)], # y-min face
            "upperWall": [(2, 3, 7, 6)], # y-max face
            "front": [(0, 3, 2, 1)],     # z-min face
            "back": [(4, 5, 6, 7)]      # z-max face
        }
        
        for name, faces in boundary_faces.items():
            mesh_dict.start_dict(name)
            mesh_dict.add_entry("type", "patch")
            mesh_dict.start_dict("faces")
            for face in faces:
                mesh_dict.add_entry("", face)
            mesh_dict.end_dict()  # faces
            mesh_dict.end_dict()  # boundary
        
        mesh_dict.end_dict()  # boundary
        
        return mesh_dict
    
    def build_control_dict(self) -> OpenFOAMDict:
        """Build controlDict"""
        control_dict = OpenFOAMDict("dictionary", "controlDict")
        control_dict.add_header(location="system")
        
        control_dict.add_entry("application", self.solver_settings.solver)
        control_dict.add_entry("startFrom", "startTime")
        control_dict.add_entry("startTime", self.solver_settings.start_time)
        control_dict.add_entry("stopAt", "endTime")
        control_dict.add_entry("endTime", self.solver_settings.end_time)
        control_dict.add_entry("deltaT", self.solver_settings.time_step)
        control_dict.add_entry("writeControl", "runTime")
        control_dict.add_entry("writeInterval", self.solver_settings.write_interval)
        
        # Standard output settings
        control_dict.add_entry("writeFormat", "ascii")
        control_dict.add_entry("writePrecision", 6)
        control_dict.add_entry("writeCompression", "off")
        control_dict.add_entry("timeFormat", "general")
        control_dict.add_entry("timePrecision", 6)
        control_dict.add_entry("runTimeModifiable", True)
        
        return control_dict
    
    def build_snappy_hex_mesh_dict(self, stl_files: List[Path]) -> OpenFOAMDict:
        """Build snappyHexMeshDict for STL incorporation"""
        snappy_dict = OpenFOAMDict("dictionary", "snappyHexMeshDict")
        snappy_dict.add_header(location="system")
        
        # Geometry section - add all STL files
        snappy_dict.start_dict("geometry")
        for stl_file in stl_files:
            snappy_dict.start_dict(stl_file.stem)
            snappy_dict.add_entry("type", "triSurfaceMesh")
            snappy_dict.add_entry("name", stl_file.stem)
            snappy_dict.end_dict()
        snappy_dict.end_dict()
        
        # Add standard snappyHexMesh configuration
        # ... (snappyHexMeshDict is complex, but you get the pattern)
        
        return snappy_dict
    
    def build_case(self, stl_files: List[Path] = None) -> Path:
        """Build complete OpenFOAM case"""
        if stl_files is None:
            stl_files = []
        
        # Create directory structure
        system_dir = self.case_path / "system"
        constant_dir = self.case_path / "constant" 
        zero_dir = self.case_path / "0"
        
        system_dir.mkdir(parents=True, exist_ok=True)
        constant_dir.mkdir(parents=True, exist_ok=True)
        zero_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate core files
        self.build_block_mesh().write(system_dir / "blockMeshDict")
        self.build_control_dict().write(system_dir / "controlDict")
        
        # Add STL files to constant/triSurface
        if stl_files:
            tri_surface_dir = constant_dir / "triSurface"
            tri_surface_dir.mkdir(exist_ok=True)
            
            for stl_file in stl_files:
                # Copy STL files to case
                import shutil
                shutil.copy2(stl_file, tri_surface_dir / stl_file.name)
            
            # Generate snappyHexMeshDict
            self.build_snappy_hex_mesh_dict(stl_files).write(system_dir / "snappyHexMeshDict")
        
        print(f"OpenFOAM case created: {self.case_path}")
        return self.case_path


##################################################################

def create_control_file(header_dict, content_dict, object_name="file"):
    # Define which keys need termination
    NEEDS_TERMINATION = {
        "geometry", "castellatedMeshControls", "snapControls", 
        "addLayersControls", "meshQualityControls", "refinementSurfaces",
        "refinementRegions", "layers"
    }
    
    generalDict = OpenFOAMDict(object_name=object_name)
    generalDict.add_comment("Autogenerated with PoreMesh by SKD3")
    
    # Add header
    generalDict.start_dict("FoamFile")
    for key, value in header_dict.items():
        generalDict.add_entry(key, value)
    generalDict.end_dict()
    
    # Recursively process content
    def _process_content(parent_dict, content, needs_termination=False):
        for key, value in content.items():
            if isinstance(value, dict):
                # Check if this dictionary needs termination
                should_terminate = key in NEEDS_TERMINATION
                
                parent_dict.start_dict(key)
                _process_content(parent_dict, value, should_terminate)
                parent_dict.end_dict(terminator=";" if should_terminate else "")
                
            elif isinstance(value, list):
                parent_dict.start_list(key)
                for item in value:
                    if isinstance(item, dict):
                        parent_dict.start_dict("")
                        _process_content(parent_dict, item, False)  # List items don't terminate
                        parent_dict.end_dict(terminator="")
                    else:
                        parent_dict.add_item("", item)
                parent_dict.end_list()
            else:
                parent_dict.add_entry(key, value)
    
    _process_content(generalDict, content_dict, False)
    return generalDict

############################################################

def analyze_stl_and_generate_blockmesh(stl_file, flow_direction, background_scale, target_cell_size):
    try:
        # Check if stl_file is provided
        if not stl_file:
            return "❌ Please upload an STL file", ""
        
        # Analyze STL file - stl_file is already a string path from Gradio
        analyzer = STLAnalyzer()
        geometry = analyzer.analyze_stl(Path(stl_file))  # Remove .name
        
        # Calculate bounds with background scaling
        bounds = geometry.bounds
        x_min, x_max, y_min, y_max, z_min, z_max = bounds
        
        # Apply background scaling
        center_x = (x_min + x_max) / 2
        center_y = (y_min + y_max) / 2  
        center_z = (z_min + z_max) / 2
        
        width = (x_max - x_min) * background_scale
        height = (y_max - y_min) * background_scale
        depth = (z_max - z_min) * background_scale
        
        scaled_bounds = (
            center_x - width/2, center_x + width/2,
            center_y - height/2, center_y + height/2,
            center_z - depth/2, center_z + depth/2
        )

        # min_x, max_x, min_y, max_y, min_z, max_z = scaled_bounds
        
        # offset_x = max(0, -min_x)  # Only positive offset if min is negative
        # offset_y = max(0, -min_y)
        # offset_z = max(0, -min_z)
        
        # # Apply offset to all bounds
        # scaled_bounds = (
        # min_x + offset_x, max_x + offset_x,
        # min_y + offset_y, max_y + offset_y, 
        # min_z + offset_z, max_z + offset_z
        # )
        
        # Generate vertices
        vertices = [
            (scaled_bounds[0], scaled_bounds[2], scaled_bounds[4]),  # vertex 0
            (scaled_bounds[1], scaled_bounds[2], scaled_bounds[4]),  # vertex 1
            (scaled_bounds[1], scaled_bounds[3], scaled_bounds[4]),  # vertex 2
            (scaled_bounds[0], scaled_bounds[3], scaled_bounds[4]),  # vertex 3
            (scaled_bounds[0], scaled_bounds[2], scaled_bounds[5]),  # vertex 4
            (scaled_bounds[1], scaled_bounds[2], scaled_bounds[5]),  # vertex 5
            (scaled_bounds[1], scaled_bounds[3], scaled_bounds[5]),  # vertex 6
            (scaled_bounds[0], scaled_bounds[3], scaled_bounds[5])   # vertex 7
        ]
        
        # Calculate cell counts
        dim_x = scaled_bounds[1] - scaled_bounds[0]
        dim_y = scaled_bounds[3] - scaled_bounds[2]
        dim_z = scaled_bounds[5] - scaled_bounds[4]
        
        cells_x = max(10, int(dim_x / target_cell_size))
        cells_y = max(10, int(dim_y / target_cell_size))
        cells_z = max(10, int(dim_z / target_cell_size))
        
        # Flow direction face lookup
        flow_faces = {
            'x': {  # Flow along X-axis
                'inlet': [(0, 4, 7, 3)],
                'outlet': [(1, 5, 6, 2)],
                'front': [(0, 1, 5, 4)],
                'back': [(2, 3, 7, 6)],
                'bottom': [(0, 1, 2, 3)],
                'top': [(4, 5, 6, 7)]
            },
            'y': {  # Flow along Y-axis
                'inlet': [(0, 1, 5, 4)],
                'outlet': [(2, 3, 7, 6)],
                'front': [(0, 4, 7, 3)],
                'back': [(1, 5, 6, 2)],
                'bottom': [(0, 1, 2, 3)],
                'top': [(4, 5, 6, 7)]
            },
            'z': {  # Flow along Z-axis
                'inlet': [(0, 1, 2, 3)],
                'outlet': [(4, 5, 6, 7)],
                'front': [(0, 1, 5, 4)],
                'back': [(2, 3, 7, 6)],
                'bottom': [(0, 4, 7, 3)],
                'top': [(1, 5, 6, 2)]
            }
        }
        
        boundary_types = {
            'inlet': 'patch',
            'outlet': 'patch',
            'front': 'symmetry', 
            'back': 'symmetry',
            'bottom': 'symmetry',
            'top': 'symmetry'
        }
        
        # Generate blockMeshDict
        blockmesh = OpenFOAMDict()
        blockmesh.add_comment("Generated by PoreMesh OpenFOAM Generator")
        
        # Header
        header_dict = {
            "version": 2.0,
            "format": "ascii",
            "class": "dictionary", 
            "object": "blockMeshDict"
        }
        blockmesh.start_dict("FoamFile")
        for key, value in header_dict.items():
            blockmesh.add_entry(key, value)
        blockmesh.end_dict()
        
        blockmesh.add_entry("scale", 1.0)
        
        # Vertices
        blockmesh.start_list("vertices")
        for i, vertex in enumerate(vertices):
            x, y, z = vertex
            blockmesh.add_vector("", round(x, 6), round(y, 6), round(z, 6))
        blockmesh.end_list()
        
        # Blocks
        blockmesh.add_comment("Mesh blocks")
        blockmesh.start_list("blocks")
        blockmesh.add_raw_line(f"hex (0 1 2 3 4 5 6 7) ({cells_x} {cells_y} {cells_z}) simpleGrading (1 1 1)")
        blockmesh.end_list()
        
        # Edges
        blockmesh.start_list("edges")
        blockmesh.end_list()
        
        # Boundaries
        blockmesh.start_list("boundary")
        faces = flow_faces[flow_direction]
        for boundary_name, face_list in faces.items():
            boundary_type = boundary_types[boundary_name]
            blockmesh.add_boundary(boundary_name, boundary_type, face_list)
        blockmesh.end_list()
        
        # Merge patches
        blockmesh.start_list("mergePatchPairs")
        blockmesh.end_list()
        
        blockmesh_content = str(blockmesh)
        
        # Create summary
        summary = f"""📊 STL Analysis Complete:
• Original bounds: {bounds}
• Scaled bounds: {tuple(round(x, 2) for x in scaled_bounds)}
• Domain dimensions: {dim_x:.1f} × {dim_y:.1f} × {dim_z:.1f}
• Cell counts: {cells_x} × {cells_y} × {cells_z} = {cells_x * cells_y * cells_z:,} total cells
• Flow direction: {flow_direction.upper()}-axis
• Actual cell size: ~{target_cell_size:.3f} units

✅ blockMeshDict generated successfully!"""
        
        return summary, blockmesh_content
        
    except Exception as e:
        return f"❌ Error processing STL: {str(e)}", ""
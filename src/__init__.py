"""
FIB-SEM to Mesh Processing Pipeline
"""

__version__ = "0.01"
__author__ = "SKD3"

# Core pipeline
from .data_loader import DataLoader
from .preprocessor import Preprocessor, PreprocessingConfig
from .mesh_generator import MeshGenerator
from .pipeline import MeshPipeline, PipelineResult

# OpenFOAM integration
from .openfoam_writer import OpenFOAMDict, OpenFOAMDimension, create_control_file

# Template management
from .template_manager import TemplateManager

# Geometry analysis
from .stl_analyzer import STLAnalyzer, STLGeometry

# Custom Geometry Code:
from .walking_cubes import WalkingCubes
from .mesh_auxillary import show_mesh, create_proto_voxel, create_proto_face, rotate_face, map_to_3d, map_to_binary, vert

# Optional: OpenFOAM builders (if you have these modules)
try:
    from .openfoam_builder import OpenFOAMCaseBuilder, MeshSettings, SolverSettings, BoundarySettings
    from .openfoam_writer import OpenFOAMCaseGenerator
    HAS_BUILDERS = True
except ImportError:
    HAS_BUILDERS = False

# Group exports by functionality for better IDE discovery
__all__ = [
    # Core pipeline
    "DataLoader",
    "Preprocessor", 
    "PreprocessingConfig",
    "MeshGenerator",
    "MeshPipeline",
    "PipelineResult",
    
    # OpenFOAM writers
    "OpenFOAMDict",
    "OpenFOAMDimension", 
    "create_control_file",
    
    # Template management
    "TemplateManager",
    
    # Geometry
    "STLAnalyzer",
    "STLGeometry"
]

# Conditionally add builder exports if available
if HAS_BUILDERS:
    __all__.extend([
        "OpenFOAMCaseGenerator",
        "OpenFOAMCaseBuilder", 
        "MeshSettings",
        "SolverSettings", 
        "BoundarySettings"
    ])
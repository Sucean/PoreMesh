# src/stl_analyzer.py
import vtk
from pathlib import Path
import numpy as np
from typing import Tuple, Dict, Any
from dataclasses import dataclass

@dataclass
class STLGeometry:
    bounds: Tuple[float, float, float, float, float, float]  # xmin, xmax, ymin, ymax, zmin, zmax
    center: Tuple[float, float, float]
    dimensions: Tuple[float, float, float]  # width, height, depth
    volume: float
    surface_area: float

class STLAnalyzer:
    def __init__(self):
        self.reader = vtk.vtkSTLReader()
    
    def analyze_stl(self, stl_path: Path) -> STLGeometry:
        """Analyze STL file to get geometry parameters"""
        self.reader.SetFileName(str(stl_path))
        self.reader.Update()
        
        polydata = self.reader.GetOutput()
        bounds = polydata.GetBounds()
        
        # Calculate center
        center = (
            (bounds[1] + bounds[0]) / 2,
            (bounds[3] + bounds[2]) / 2, 
            (bounds[5] + bounds[4]) / 2
        )
        
        # Calculate dimensions
        dimensions = (
            bounds[1] - bounds[0],  # width (x)
            bounds[3] - bounds[2],  # height (y) 
            bounds[5] - bounds[4]   # depth (z)
        )
        
        # Calculate volume and surface area
        mass_properties = vtk.vtkMassProperties()
        mass_properties.SetInputData(polydata)
        mass_properties.Update()
        
        volume = mass_properties.GetVolume()
        surface_area = mass_properties.GetSurfaceArea()
        
        return STLGeometry(
            bounds=bounds,
            center=center,
            dimensions=dimensions,
            volume=volume,
            surface_area=surface_area
        )
    
    def get_mesh_resolution(self, geometry: STLGeometry, target_cell_size: float = 0.1) -> Tuple[int, int, int]:
        """Calculate appropriate mesh resolution based on geometry size"""
        cells_x = max(10, int(geometry.dimensions[0] / target_cell_size))
        cells_y = max(10, int(geometry.dimensions[1] / target_cell_size)) 
        cells_z = max(10, int(geometry.dimensions[2] / target_cell_size))
        
        return cells_x, cells_y, cells_z
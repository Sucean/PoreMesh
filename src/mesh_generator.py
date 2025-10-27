import vtk
from vtk.util import numpy_support
import numpy as np
from pathlib import Path
from typing import Optional

class MeshGenerator:
    def __init__(self, threshold: int = 127):
        self.threshold = threshold
    
    def numpy_to_vtk(self, data: np.ndarray) -> vtk.vtkImageData:
        """Convert numpy array to VTK image data with proper dimension handling"""
        # Reorder dimensions for VTK (x, y, z)
        if data.shape[0] <= data.shape[2]:
            data = np.transpose(data, (2, 1, 0))
        
        z, y, x = data.shape
        
        vtk_data = vtk.vtkImageData()
        vtk_data.SetDimensions(x, y, z)
        vtk_data.SetSpacing(1.0, 1.0, 1.0)
        vtk_data.SetOrigin(0, 0, 0)
        
        flat_data = data.ravel(order='C')
        vtk_array = numpy_support.numpy_to_vtk(
            num_array=flat_data,
            deep=True,
            array_type=vtk.VTK_UNSIGNED_CHAR
        )
        vtk_data.GetPointData().SetScalars(vtk_array)
        return vtk_data
    
    def extract_mesh(self, vtk_data: vtk.vtkImageData) -> vtk.vtkPolyData:
        """Extract mesh using marching cubes"""
        try:
            extractor = vtk.vtkMarchingCubes()
        except AttributeError:
            extractor = vtk.vtkFlyingEdges3D()
        
        extractor.SetInputData(vtk_data)
        extractor.SetValue(0, self.threshold)
        extractor.ComputeNormalsOn()
        extractor.Update()
        
        polydata = extractor.GetOutput()
        
        # Clean the mesh
        cleaner = vtk.vtkCleanPolyData()
        cleaner.SetInputData(polydata)
        cleaner.Update()
        
        return cleaner.GetOutput()
    
    def test_watertightness(self, polydata: vtk.vtkPolyData) -> int:
        """Test if mesh is watertight"""
        feature_edges = vtk.vtkFeatureEdges()
        feature_edges.SetInputData(polydata)
        feature_edges.BoundaryEdgesOn()
        feature_edges.FeatureEdgesOff()
        feature_edges.NonManifoldEdgesOn()
        feature_edges.ManifoldEdgesOff()
        feature_edges.Update()
        return feature_edges.GetOutput().GetNumberOfCells()
    
    def write_mesh(self, polydata: vtk.vtkPolyData, output_path: Path, ascii: bool = True):
        """Write mesh to STL file"""
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        writer = vtk.vtkSTLWriter()
        writer.SetFileName(str(output_path))
        writer.SetInputData(polydata)
        writer.SetFileTypeToASCII() if ascii else writer.SetFileTypeToBinary()
        writer.Write()
    
    def generate_mesh_from_array(self, data: np.ndarray) -> vtk.vtkPolyData:
        """Complete pipeline from numpy array to mesh"""
        vtk_data = self.numpy_to_vtk(data)
        mesh = self.extract_mesh(vtk_data)
        return mesh
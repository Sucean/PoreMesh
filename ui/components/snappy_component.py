import gradio as gr
import os
from pathlib import Path
import vtk
import numpy as np
from .base_component import create_base_component


def create_snappy_component(working_dir, current_dir):

    def get_dynamic_values(working_dir, current_dir):
        trimesh_dir = os.path.join(working_dir, current_dir, "constant", "trimesh")
        
        geometry = {}
        features = []               
        refinementSurfaces = {}
        location_in_mesh = None
    
        stl_files = [f for f in os.listdir(trimesh_dir) if f.lower().endswith(".stl")]
        
        if not stl_files:
            raise FileNotFoundError(f"No .stl files found in {trimesh_dir}")
    
        print(f"[INFO] Found {len(stl_files)} STL file(s): {stl_files}")
    
        first_stl = stl_files[0]
        first_name = os.path.splitext(first_stl)[0]
    
        for stl_file in stl_files:
            name = os.path.splitext(stl_file)[0]
    
            # === geometry ===
            geometry[f'"{name}.stl"'] = {
                "type": "triSurfaceMesh",
                "name": name,

            }
    
            features.append({
                "file": f"{name}.eMesh",
                "level": 3                    
            })
    
            # === refinementSurfaces ===
            refinementSurfaces[name] = {
                "level": "(4 4)",            
                "faceZone": name,
                "cellZone": name,
                "cellZoneInside": "inside",    # ← CRITICAL for pore-space STL
                "patchInfo": { "type": "wall" }
            }
    
        # === Find a point strictly INSIDE the pore space (first STL) ===
        reader = vtk.vtkSTLReader()
        reader.SetFileName(os.path.join(trimesh_dir, first_stl))
        reader.Update()
        polydata = reader.GetOutput()
    
        if polydata.GetNumberOfPoints() == 0:
            raise ValueError(f"{first_stl} is empty or corrupt")
    
        distance_filter = vtk.vtkImplicitPolyDataDistance()
        distance_filter.SetInput(polydata)
    
        # Start from centroid as good initial guess
        bounds = polydata.GetBounds()
        point = np.array([
            (bounds[0] + bounds[1]) / 2,
            (bounds[2] + bounds[3]) / 2,
            (bounds[4] + bounds[5]) / 2
        ])
    
        max_attempts = 10000
        step_size = min(bounds[1]-bounds[0], bounds[3]-bounds[2], bounds[5]-bounds[4]) * 0.1
    
        for i in range(max_attempts):
            dist = distance_filter.EvaluateFunction(point.tolist())
            if dist < 0:  # Negative = inside (VTK convention)
                location_in_mesh = (point[0], point[1], point[2])
                print(f"[SUCCESS] Found point inside mesh after {i+1} attempts: {location_in_mesh}")
                break
            else:
                # Random walk biased toward center
                point += (np.random.rand(3) - 0.5) * step_size
    
        else:
            raise RuntimeError("Could not find a point inside the STL after 10,000 attempts. Is it closed?")
    
        # Return everything in ONE clean dict for castellatedMeshControls
        castellated_controls = {
            "features": features,                    # list!
            "refinementSurfaces": refinementSurfaces,
            "locationInMesh": f"({location_in_mesh[0]:.10f} {location_in_mesh[1]:.10f} {location_in_mesh[2]:.10f})",
            "nCellsBetweenLevels": 2,
            "resolveFeatureAngle": 30,
            "allowFreeStandingZoneFaces": True,
        }
    
        return geometry, castellated_controls
    
    # def get_dynamic_values(working_dir, current_dir):
    #     print(working_dir, current_dir)
    #     trimesh_dir = f'{working_dir}/{current_dir}/constant/trimesh/'
    #     geometry = {}
    #     stl_defs = {}
    #     point = [0, 0, 0]
        
    #     print(f"[DEBUG] Reading stl dir from {trimesh_dir}")
    #     for f in os.listdir(trimesh_dir):
    #         if f.lower().endswith(".stl"):
    #             name = os.path.splitext(f)[0]
    #             stl_defs[f] = {
    #             "type": "triSurfaceMesh",
    #             "name": name,
    #             "regions": {
    #                 name: {
    #                     "name": name
    #                 }
    #             }
    #             }
    #             features[f] = {
    #                 "file": f'{name}.eMesh',
    #                 "level": 2
    #             }

    #     for f in features:
    #         name = f['file'].splitext[0]

    #         refinementSurfaces[f] = {
    #             f'{name}': {
    #             "level": "(2 2)",
    #             "faceZone": "fluidRegion",
    #             "cellZone": "fluidRegion",
    #             "cellZoneInside": "inside",
    #             "patchInfo": "{ type wall; }"
    #             }
    #         }
        
    #     print(f"[DEBUG] {stl_defs}")
    #     geometry.update(stl_defs)
    #     print(f"[DEBUG] {geometry}")

    #     reader = vtk.vtkSTLReader()
    #     reader.SetFileName(f'{trimesh_dir}{name}.stl')  # force string
    #     reader.Update()
        
    #     polydata = reader.GetOutput()
    
    #     distance_filter = vtk.vtkImplicitPolyDataDistance()
    #     distance_filter.SetInput(polydata)

    #     while distance_filter.EvaluateFunction(point) > 0:
    #         point += np.random.rand(3)*2
    #         print(f'[DEBUG] {distance_filter.EvaluateFunction(point)}')
            
    #     location_in_mesh = {"locationInMesh" : f'({point[0]} {point[1]} {point[2]})'}
        
    #     return geometry, location_in_mesh, features, refinementSurfaces
    
    component_definitions = {
        "castellatedMesh": {
            'component_type': 'Checkbox',
            'value': True,
            'label': "Castellated Mesh"
        },
        "snap": {
            'component_type': 'Checkbox',
            'value': True,
            'label': "Snap to Surface"
        },
        "addLayers": {
            'component_type': 'Checkbox',
            'value': False,
            'label': "Add Boundary Layers"
        },
        "geometry": {},

        "nSmoothPatch": {
            "component_type": "Number",
            "value": 3,
            "label": "Smoothing Iterations",
            "minimum": 1,
            "maximum": 10
        },
        "nSolveIter": {
            "component_type": "Number",
            "value": 30,
            "label": "Solution Iterations",
            "minimum": 10,
            "maximum": 100
        },
        "nRelaxIter": {
            "component_type": "Number",
            "value": 5,
            "label": "Relaxation Iterations",
            "minimum": 1,
            "maximum": 20
        }
    }
    
    return create_base_component("snappyHexMeshDict", component_definitions, working_dir, current_dir, snappy_function = get_dynamic_values)
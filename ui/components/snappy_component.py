import gradio as gr
from .base_component import create_base_component

def create_snappy_component():
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
        "nSmoothPatch": {
            'component_type': 'Number',
            'value': 3,
            'label': "Smoothing Iterations",
            'minimum': 1,
            'maximum': 10
        },
        "nSolveIter": {
            'component_type': 'Number',
            'value': 30,
            'label': "Solution Iterations",
            'minimum': 10,
            'maximum': 100
        },
        "nRelaxIter": {
            'component_type': 'Number',
            'value': 5,
            'label': "Relaxation Iterations",
            'minimum': 1,
            'maximum': 20
        }
    }
    
    return create_base_component("snappyHexMeshDict", component_definitions)
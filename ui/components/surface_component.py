import gradio as gr
from .base_component import create_base_component

def create_surface_component(working_dir, current_dir):
    component_definitions = {
    "surfaces": {
        'component_type': 'Textbox',
        "value": f'constant/triSurface/block000.stl',
        "label": "Path to STL",
        "placeholder": f'constant/triSurface/block000.stl'
    },
    "extractionMethod": {
        'component_type': 'Dropdown', 
        'value': "extractFromSurface",
        'choices': ["extractFromSurface"],
        'label': "extraction Method"
    },
    "includedAngle": {
        'component_type': 'Number', 
        'value': 150,
        'label': "Included extraction angle"
    },
    "writeObj": {
        'component_type': 'Dropdown', 
        'value': 'yes',
        'choices': ["yes", "no"],
        'label': "Write Object?"
    },
    "extractFromEdgesCoeffs": {
        'component_type': 'Textbox', 
        'value': '{ includeAngle 150;}',
        'label': "includeAngle for Edges"
    },
    "writeFormat": {
        'component_type': 'Radio',
        'choices': ["ascii", "binary"],
        'value': "ascii",
        'label': "Write Format"
    }
    }
    
    return create_base_component("surfaceFeatureExtractDict", component_definitions, working_dir, current_dir)
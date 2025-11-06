import gradio as gr
from .base_component import create_base_component

def create_velocity_component():
    component_definitions = {
        "internalField": {
            'component_type': 'Textbox',
            'value': "uniform (0 0 0)",
            'label': "Initial Velocity",
            'placeholder': "uniform (0 0 0) or nonuniform List<vector>"
        },
        "inletValue": {
            'component_type': 'Textbox',
            'value': "uniform (1 0 0)", 
            'label': "Inlet Velocity",
            'placeholder': "uniform (1 0 0) for 1 m/s in x-direction"
        },
        "inletType": {
            'component_type': 'Dropdown',
            'choices': ["fixedValue", "flowRateInletVelocity", "pressureInletVelocity", "inletOutlet"],
            'value': "fixedValue",
            'label': "Inlet Boundary Type"
        },
        "outletType": {
            'component_type': 'Dropdown', 
            'choices': ["zeroGradient", "fixedValue", "inletOutlet", "pressureInletOutletVelocity"],
            'value': "zeroGradient",
            'label': "Outlet Boundary Type"
        },
        "wallType": {
            'component_type': 'Dropdown',
            'choices': ["noSlip", "fixedValue", "slip", "movingWallVelocity"],
            'value': "noSlip", 
            'label': "Wall Boundary Type"
        }
    }
    
    return create_base_component("U", component_definitions)
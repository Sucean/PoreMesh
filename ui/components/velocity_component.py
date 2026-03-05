import gradio as gr
from .base_component import create_base_component

def create_velocity_component(working_dir, current_dir):
    # component_definitions = {
    #     "internalField": {
    #         'component_type': 'Textbox',
    #         'value': "uniform (0 0 0)",
    #         'label': "Initial Velocity",
    #         'placeholder': "uniform (0 0 0) or nonuniform List<vector>"
    #     },
    #     "inletValue": {
    #         'component_type': 'Textbox',
    #         'value': "uniform (1 0 0)", 
    #         'label': "Inlet Velocity",
    #         'placeholder': "uniform (1 0 0) for 1 m/s in x-direction"
    #     },
    #     "inletType": {
    #         'component_type': 'Dropdown',
    #         'choices': ["fixedValue", "flowRateInletVelocity", "pressureInletVelocity", "inletOutlet"],
    #         'value': "fixedValue",
    #         'label': "Inlet Boundary Type"
    #     },
    #     "outletType": {
    #         'component_type': 'Dropdown', 
    #         'choices': ["zeroGradient", "fixedValue", "inletOutlet", "pressureInletOutletVelocity"],
    #         'value': "zeroGradient",
    #         'label': "Outlet Boundary Type"
    #     },
    #     "wallType": {
    #         'component_type': 'Dropdown',
    #         'choices': ["noSlip", "fixedValue", "slip", "movingWallVelocity"],
    #         'value': "noSlip", 
    #         'label': "Wall Boundary Type"
    #     }
    # }

    component_definitions = {
        "dimensions": {
            "component_type": "Textbox",
            "value": "[0 1 -1 0 0 0 0]",
            "label": "Dimensions",
            "placeholder": "[0 1 -1 0 0 0 0]"
        },
        "internalField": {
            "component_type": "Textbox",
            "value": "uniform (1.0 0.0 0.0)",
            "label": "Internal Field",
            "placeholder": "uniform (1.0 0.0 0.0)"
        },
        "boundaryField": {
            "inlet": {
                "type": {
                    "component_type": "Dropdown",
                    "choices": ["fixedValue", "flowRateInletVelocity", "pressureInletVelocity", "inletOutlet"],
                    "value": "fixedValue",
                    "label": "Inlet Type"
                },
                "value": {
                    "component_type": "Textbox",
                    "value": "uniform (1.0 0.0 0.0)",
                    "label": "Inlet Value",
                    "placeholder": "uniform (1.0 0.0 0.0)"
                }
            },
            "outlet": {
                "type": {
                    "component_type": "Dropdown",
                    "choices": ["inletOutlet", "zeroGradient", "fixedValue", "pressureInletOutletVelocity"],
                    "value": "inletOutlet",
                    "label": "Outlet Type"
                },
                "inletValue": {
                    "component_type": "Textbox",
                    "value": "uniform (0 0 0)",
                    "label": "Outlet InletValue",
                    "placeholder": "uniform (0 0 0)"
                },
                "value": {
                    "component_type": "Textbox",
                    "value": "uniform (0 0 0)",
                    "label": "Outlet Value",
                    "placeholder": "uniform (0 0 0)"
                }
            },
            "walls": {
                "type": {
                    "component_type": "Dropdown",
                    "choices": ["fixedValue", "noSlip", "slip", "movingWallVelocity"],
                    "value": "fixedValue",
                    "label": "Wall Type"
                },
                "value": {
                    "component_type": "Textbox",
                    "value": "uniform (0 0 0)",
                    "label": "Wall Value",
                    "placeholder": "uniform (0 0 0)"
                }
            }
        }
    }
    return create_base_component("U", component_definitions, working_dir, current_dir)
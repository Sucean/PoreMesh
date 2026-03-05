import gradio as gr
from .base_component import create_base_component

def create_pressure_component(working_dir, current_dir):

    def get_dynamic_values():
        print("[DEBUG] Placeholder")
        return "TODO DUMMY"
    
    component_definitions = {
        "dimensions": {
            "component_type": "Textbox",
            "value": "[0 2 -2 0 0 0 0]",
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
                    "choices": ["fixedValue", "zeroGradient"],
                    "value": "fixedValue",
                    "label": "Inlet Type"
                },
                "value": {
                    "component_type": "Textbox",
                    "value": "uniform 0",
                    "label": "Inlet Value",
                    "placeholder": "uniform 0"
                }
            },
            "outlet": {
                "type": {
                    "component_type": "Dropdown",
                    "choices": ["zeroGradient", "fixedValue"],
                    "value": "fixedValue",
                    "label": "Outlet Type"
                },
                "value": {
                    "component_type": "Textbox",
                    "value": "uniform 0",
                    "label": "Outlet Value",
                    "placeholder": "uniform 0"
                }
            },
            "walls": {
                "type": {
                    "component_type": "Dropdown",
                    "choices": ["zeroGradient", "fixedValue", "noSlip", "slip", "movingWallVelocity"],
                    "value": "zeroGradient",
                    "label": "Wall Type"
                },
                "value": {
                    "component_type": "Textbox",
                    "value": "uniform 0",
                    "label": "Wall Value",
                    "placeholder": "uniform 0"
                }
            }
        }
    }
    return create_base_component("p", component_definitions, working_dir, current_dir, )
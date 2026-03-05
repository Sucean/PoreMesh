import gradio as gr
from .base_component import create_base_component

def create_turbulence_component(working_dir, current_dir):
    component_definitions = {
        "simulation Type": {
            "component_type": "Dropdown",
            "choices": ["laminar", "RAS", "LES"],
            "value": "laminar",
            "label": "Type of Turbulence",
        }
    }
    return create_base_component("turbulenceProperties", component_definitions, working_dir, current_dir)
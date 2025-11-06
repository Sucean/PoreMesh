import gradio as gr
from .base_component import create_base_component

def create_pressure_component():
    component_definitions = {
        "internalField": {
            'component_type': 'Number',
            'value': 0,
            'label': "Initial Pressure"
        },
        "inletValue": {
            'component_type': 'Number', 
            'value': 0,
            'label': "Inlet Pressure"
        }
    }
    return create_base_component("u", component_definitions)
import gradio as gr
from .base_component import create_base_component

def create_decompose_component():
    component_definitions = {
        "method": {
            'component_type': 'Dropdown',
            'choices': ["none", "manual", "simple", "hierarchical", "kahip", "metis", "scotch", "structured", "multiLevel"],
            'value': "simple",
            'label': "Method"
        },
        "numberOfSubdomains": {
            'component_type': 'Number',
            'value': 1,
            'label': "Number of Domains"
        }
    }
    return create_base_component("decomposeParDict", component_definitions)
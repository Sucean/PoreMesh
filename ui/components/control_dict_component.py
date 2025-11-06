import gradio as gr
from .base_component import create_base_component

def create_control_dict_component():
    component_definitions = {
    "application": {
        'component_type': 'Dropdown',
        'choices': ["simpleFoam", "icoFoam", "pimpleFoam", "pisoFoam"],
        'value': "simpleFoam",
        'label': "Solver"
    },
    "startTime": {
        'component_type': 'Number', 
        'value': 0,
        'label': "Start Time"
    },
    "endTime": {
        'component_type': 'Number', 
        'value': 1000,
        'label': "End Time"
    },
    "deltaT": {
        'component_type': 'Number', 
        'value': 1,
        'label': "Time Step"
    },
    "writeInterval": {
        'component_type': 'Number', 
        'value': 100,
        'label': "Write Interval"
    },
    "writeFormat": {
        'component_type': 'Radio',
        'choices': ["ascii", "binary"],
        'value': "ascii",
        'label': "Write Format"
    }
    }
    
    return create_base_component("controlDict", component_definitions)
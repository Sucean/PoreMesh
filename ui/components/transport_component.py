import gradio as gr
from .base_component import create_base_component

def create_transport_component(working_dir, current_dir):
    component_definitions = {
        "transportModel": {
            "component_type": "Dropdown",
            "choices": ["Newtonian", "BirdCarreau", "CrossPowerLaw", "powerLaw", "HerschelBulkley", "Casson", "strainRateFunction", "viscoelastic", "Maxwell", "Giesekus", "PTT", "lambdaThixotropic"],
            "value": "Newtonian",
            "label": "Compressibility Model or so dunno",
        },
        "nu": {
            "component_type": "Textbox",
            "value": "nu [0 2 -1 0 0 0 0] 1e-6",
            "label": "Kinematic ciscosity m^2/s",
            "placeholder": "nu [0 2 -1 0 0 0 0] 1e-6"
        }
    }
    return create_base_component("transportProperties", component_definitions, working_dir, current_dir)
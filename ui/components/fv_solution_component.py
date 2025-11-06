import gradio as gr
from .base_component import create_base_component

def create_fv_solution_component():
    component_definitions = {
        "solver_type": {
            'component_type': 'Radio',
            'choices': ["SIMPLE", "PISO", "PIMPLE"],
            'value': "SIMPLE",
            'label': "Solver Algorithm"
        },
        "p_solver": {
            'component_type': 'Dropdown',
            'choices': ["GAMG", "PCG", "smoothSolver"],
            'value': "GAMG",
            'label': "Pressure Solver"
        },
        "U_solver": {
            'component_type': 'Dropdown',
            'choices': ["smoothSolver", "PBiCG", "GAMG"],
            'value': "smoothSolver",
            'label': "Velocity Solver"
        },
        "p_tolerance": {
            'component_type': 'Number',
            'value': 1e-6,
            'label': "Pressure Tolerance",
            'precision': 10
        },
        "U_tolerance": {
            'component_type': 'Number',
            'value': 1e-6,
            'label': "Velocity Tolerance",
            'precision': 10
        },
        "p_relax": {
            'component_type': 'Number',
            'value': 0.3,
            'label': "Pressure Relaxation",
            'minimum': 0.1,
            'maximum': 1.0,
            'step': 0.05
        },
        "U_relax": {
            'component_type': 'Number',
            'value': 0.7,
            'label': "Velocity Relaxation",
            'minimum': 0.1,
            'maximum': 1.0,
            'step': 0.05
        }
    }
    
    return create_base_component("fvSolution", component_definitions)
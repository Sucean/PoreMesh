import gradio as gr
from .base_component import create_base_component

def create_fv_schemes_component():
    component_definitions = {
        "ddtSchemes_default": {
            'component_type': 'Dropdown',
            'choices': ["Euler", "steadyState", "backward", "CrankNicolson"],
            'value': "steadyState",
            'label': "Time Scheme (default)"
        },
        "gradSchemes_default": {
            'component_type': 'Dropdown',
            'choices': ["Gauss linear", "leastSquares", "cellLimited Gauss linear 1"],
            'value': "Gauss linear",
            'label': "Gradient Scheme (default)"
        },
        "divSchemes_default": {
            'component_type': 'Dropdown',
            'choices': ["Gauss linear", "Gauss upwind", "Gauss limitedLinear 1", "bounded Gauss upwind"],
            'value': "Gauss linear",
            'label': "Divergence Scheme (default)"
        },
        "laplacianSchemes_default": {
            'component_type': 'Dropdown',
            'choices': ["Gauss linear orthogonal", "Gauss linear corrected", "Gauss linear limited 1"],
            'value': "Gauss linear orthogonal",
            'label': "Laplacian Scheme (default)"
        },
        "interpolationSchemes_default": {
            'component_type': 'Dropdown',
            'choices': ["linear", "upwind"],
            'value': "linear",
            'label': "Interpolation Scheme (default)"
        },
        "snGradSchemes_default": {
            'component_type': 'Dropdown',
            'choices': ["corrected", "uncorrected", "limited 1"],
            'value': "corrected",
            'label': "Surface Normal Gradient (default)"
        }
    }
    
    return create_base_component("fvSchemes", component_definitions)
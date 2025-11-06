import gradio as gr
from ui.components import (
    create_blockmesh_component,
    create_control_dict_component,
    create_fv_schemes_component,
    create_fv_solution_component,
    create_decompose_component,
    create_snappy_component,
    create_velocity_component
)

def create_openfoam_tab():
    """OpenFOAM system files tab"""
    print(type(gr))
    gr.Markdown("### Generate OpenFOAM System Control Files")
    gr.Markdown("## system/")
    
    stl_file = gr.File(label="Upload STL File", file_types=[".stl"], elem_id="stl_file")

    # Load Components
    with gr.Accordion("1. blockMeshDict", open=False):
        create_blockmesh_component(stl_file)

    with gr.Accordion("2. controlDict", open=False):
        create_control_dict_component()

    with gr.Accordion("3. fvSchemes", open=False):
        create_fv_schemes_component()

    with gr.Accordion("4. fvSolution", open=False):
        create_fv_solution_component()

    with gr.Accordion("5. decomposeParDict", open=False):
        create_decompose_component()

    with gr.Accordion("6. snappyHexMeshDict", open=False):
        create_snappy_component()

    gr.Markdown("## 0/")

    with gr.Accordion("Velocity U", open=False):
        create_velocity_component()
        
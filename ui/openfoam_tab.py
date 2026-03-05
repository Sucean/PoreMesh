import gradio as gr
import os
from pathlib import Path
from ui.components import (
    create_blockmesh_component,
    create_control_dict_component,
    create_fv_schemes_component,
    create_fv_solution_component,
    create_decompose_component,
    create_surface_component,
    create_snappy_component,
    create_velocity_component,
    create_pressure_component,
    create_transport_component,
    create_turbulence_component
)


def create_openfoam_tab():
    """OpenFOAM system files tab"""
    
    gr.Markdown("### Generate OpenFOAM System Control Files")

    
    with gr.Row():
        working_dir = gr.Textbox(label="Working Directory", value=os.getcwd()) 
        #update_btn = gr.Button("Update")
    
    # Directory browser
        current_dir = gr.Dropdown(label="Project Directories", info="Available directories in working path", choices=[])

    def update_directories(path):
        """Update directory list based on working directory"""
        try:
            path_obj = Path(path)
            if path_obj.exists() and path_obj.is_dir():
                dirs = [d for d in os.listdir(path_obj) if (path_obj / d).is_dir()]
                return gr.Dropdown(choices=dirs, value=dirs[0] if dirs else None, interactive=True)
            return gr.Dropdown(choices=[], interactive=True)
        except Exception:
            return gr.Dropdown(choices=[], interactive=True)
    
    #update_btn.click(fn=update_directories, inputs=[working_dir], outputs=[current_dir])
    working_dir.change(fn=update_directories, inputs=[working_dir], outputs=[current_dir])
    
    gr.Markdown("## system/")
    
    stl_file = gr.File(label="Upload STL File", file_types=[".stl"], elem_id="stl_file")

    # Load Components
    with gr.Accordion("1. blockMeshDict", open=False):
        create_blockmesh_component(stl_file, working_dir, current_dir)

    with gr.Accordion("2. controlDict", open=False):
        create_control_dict_component(working_dir, current_dir)

    with gr.Accordion("3. fvSchemes", open=False):
        create_fv_schemes_component(working_dir, current_dir)

    with gr.Accordion("4. fvSolution", open=False):
        create_fv_solution_component(working_dir, current_dir)

    with gr.Accordion("5. decomposeParDict", open=False):
        create_decompose_component(working_dir, current_dir)

    with gr.Accordion("6. surfaceFeatureExtractDict", open=False):
        create_surface_component(working_dir, current_dir)

    with gr.Accordion("7. snappyHexMeshDict", open=False):
        create_snappy_component(working_dir, current_dir)


    
    gr.Markdown("## 0/")

    with gr.Accordion("Velocity U", open=False):
        create_velocity_component(working_dir, current_dir)

    with gr.Accordion("Pressure p", open=False):
        create_pressure_component(working_dir, current_dir)

    gr.Markdown("## constant/")

    with gr.Accordion("Velocity U", open=False):
        create_transport_component(working_dir, current_dir)

    with gr.Accordion("Pressure p", open=False):
        create_turbulence_component(working_dir, current_dir)
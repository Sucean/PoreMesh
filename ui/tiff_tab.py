import gradio as gr
from pathlib import Path
import tempfile
import tifffile
import multiprocessing as mp
import os
import numpy as np

# These imports work because main.py set up the path

from src.mesh_generator import MeshGenerator
from src.preprocessor import Preprocessor, PreprocessingConfig

def browse_directory():
    # This is a hack - opens file browser but user must manually type path
    current_dir = os.getcwd()
    return gr.Textbox(value=current_dir)

def create_tiff_tab():
    """TIFF to Mesh conversion tab"""

    gr.Markdown("### Convert TIFF stacks to 3D surface meshes")
    
    with gr.Row():
        with gr.Column():
            working_dir = gr.Textbox(label="Working Directory", value=os.getcwd())           
            tiff_file = gr.UploadButton(label="Upload 3D TIFF Stack", file_types=[".tif", ".tiff"], file_count="single")
            block_size = gr.Slider(64, 512, value=256, label="Block Size")
            cap_size = gr.Slider(1, 50, value=10, label="Cap Size")
            cap_axis = gr.Dropdown(choices=['x', 'y', 'z'], value = 'z', label = "Cap Axis")
            padding_size = gr.Slider(1, 20, value=8, label="Padding Size")
            threshold = gr.Slider(0, 255, value=127, label="Marching Cubes Threshold")
            use_parallel = gr.Checkbox(label='Multiprocessing', value = True)
            tiff_btn = gr.Button("Generate Meshes")
        
        with gr.Column():
            tiff_output = gr.Textbox(label="Processing Results", lines=15)
            mesh_download = gr.File(label="Download Generated Meshes", file_count="multiple")
    
    tiff_btn.click(
        fn=process_tiff_file,
        inputs=[tiff_file, block_size, cap_size, padding_size, threshold, cap_axis, working_dir, use_parallel],
        outputs=[tiff_output]
    )


def mesh_worker(args):
    threshold, block, block_id, padding_size, working_dir = args

    block = np.pad(block, ((padding_size, padding_size), (padding_size, padding_size), (padding_size, padding_size)), mode='constant', constant_values=0)
    
    mesh_generator = MeshGenerator(threshold)
    mesh = mesh_generator.generate_mesh_from_array(block)

    save_path = working_dir / f'block{block_id:03}' / 'constant' / 'trimesh' / f'block{block_id:03}.stl'
    mesh_generator.write_mesh(mesh, save_path)

    boundary_edges = mesh_generator.test_watertightness(mesh)

    return block_id, save_path, boundary_edges

def process_tiff_file(tiff_file, block_size, cap_size, padding_size, threshold, cap_axis, working_dir, use_parallel):

    if tiff_file is None:
        return "❌ Please upload a TIFF file"
    
    array = tifffile.imread(tiff_file.name)

    ## Check if it is in color mode, if so...
    if len(array) >= 4 and array.shape[-1] == 3:
        # Collapse color channels
        if np.allclose(array[...,0], array[...,1]) and np.allclose(array[...,0], array[...,2]):
            array = array[...,0]
        else:
            # if channels differ, average or select one
            data = np.mean(array, axis=-1)
    
    working_dir = Path(working_dir)

    config = PreprocessingConfig(
    cap_size=cap_size,
    cap_axis=cap_axis, 
    padding_size=padding_size,
    block_size=block_size
    )
    
    preprocessor = Preprocessor(config)
    blocks = preprocessor.blockify(data = array)
    
    for i in range(len(blocks)):

        block_path = working_dir / f'block{i:03}' / 'constant' / 'trimesh'
        block_path.mkdir(parents=True, exist_ok=True)

        system_path = working_dir / f'block{i:03}' / 'system'
        zero_path = working_dir / f'block{i:03}' / '0'
        system_path.mkdir(parents=True, exist_ok=True)
        zero_path.mkdir(parents=True, exist_ok=True)

    args_list = [(threshold, block, i, padding_size, working_dir) for i, block in enumerate(blocks)]
    
    if use_parallel:
        with mp.Pool(processes=mp.cpu_count()) as pool:
            results = pool.map(mesh_worker, args_list)

    return str(results)
    
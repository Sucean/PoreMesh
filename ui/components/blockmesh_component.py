import gradio as gr
import os
from src.openfoam_writer import analyze_stl_and_generate_blockmesh

def create_blockmesh_component(shared_stl_file, working_dir, current_dir):
    """BlockMeshDict component"""
    template_name = "blockMeshDict"
    
    with gr.Row():
        with gr.Column():
            use_upload = gr.Checkbox(label='Use uploaded stl instead')
            flow_direction = gr.Radio(
                choices=["x", "y", "z"], 
                value="z", 
                label="🌊 Flow Direction"
            )
            background_scale = gr.Slider(1.0, 3.0, value=1.0, label="Background Scale")
            target_cell_size = gr.Slider(0.1, 5.0, value=1.0, label="Target Cell Size")
            generate_btn = gr.Button("🚀 Generate blockMeshDict")
            save_btn = gr.Button("Save")
            analysis_output = gr.Textbox(label="📊 Analysis Results", lines=6)
        with gr.Column():
            blockmesh_output = gr.Code(label="Generated blockMeshDict", language="cpp", lines=20)
    
    # Connect events
    generate_btn.click(
        fn=generate_blockmesh_dict,
        inputs=[shared_stl_file, flow_direction, background_scale, target_cell_size, working_dir, current_dir, use_upload],
        outputs=[analysis_output, blockmesh_output]
    )


    save_btn.click(
        fn=write_data,
        inputs=[blockmesh_output, working_dir, current_dir],
        outputs=[analysis_output]
    )
    
    # save_btn.click(
    #     fn=write_data,
    #     inputs=[],
    #     outputs=[analysis_output],
    # )

def generate_blockmesh_dict(shared_stl_file, flow_direction, background_scale, target_cell_size, working_dir, current_dir, use_upload):
    """Generate blockMeshDict - focused on this specific task"""
    if use_upload:
        try:
            if shared_stl_file is None:
                return "❌ Please upload an STL file", ""  # Return two values
            summary, blockmesh_content = analyze_stl_and_generate_blockmesh(shared_stl_file, flow_direction, background_scale, target_cell_size)
            return summary, blockmesh_content
        except Exception as e:
            return f"[ERROR] {str(e)}", ""  # Return two values
    else:
        try:
            trimesh_dir = f'{working_dir}/{current_dir}/constant/trimesh/'
            print(trimesh_dir)
            if not os.path.exists(trimesh_dir):
                return f"[ERROR] Directory does not exist: {trimesh_dir}", ""
                
            stl_files = [f for f in os.listdir(trimesh_dir) if f.endswith(".stl")]
            if not stl_files:
                return "[ERROR] No STL files found in directory", ""
                
            shared_stl_file = trimesh_dir + stl_files[0]  # Take first STL file
            print(shared_stl_file)
            summary, blockmesh_content = analyze_stl_and_generate_blockmesh(shared_stl_file, flow_direction, background_scale, target_cell_size)
            return summary, blockmesh_content
        except Exception as e:
            return f"[ERROR] {e}", ""  # Return two values
     
def write_data(blockmesh_output, working_dir, current_dir):
    dict_dir = f'{working_dir}/{current_dir}/system/blockMeshDict'

    with open(dict_dir, 'w') as f:
        f.write(blockmesh_output)
    return f'saved data to {dict_dir}'

def create_download_file(content, filename):
    """Helper for download files"""
    import tempfile
    if content and not content.startswith("❌"):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write(content)
            return f.name
    return None
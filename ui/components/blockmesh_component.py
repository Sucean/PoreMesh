import gradio as gr
from src.openfoam_writer import analyze_stl_and_generate_blockmesh

def create_blockmesh_component(shared_stl_file):
    """BlockMeshDict component"""
    with gr.Row():
        with gr.Column():
            flow_direction = gr.Radio(
                choices=["x", "y", "z"], 
                value="z", 
                label="🌊 Flow Direction"
            )
            background_scale = gr.Slider(1.0, 3.0, value=1.0, label="Background Scale")
            target_cell_size = gr.Slider(0.1, 5.0, value=1.0, label="Target Cell Size")
            generate_btn = gr.Button("🚀 Generate blockMeshDict")
        
        with gr.Column():
            analysis_output = gr.Textbox(label="📊 Analysis Results", lines=6)
            blockmesh_output = gr.Code(label="Generated blockMeshDict", language="cpp", lines=20)
            download = gr.File(label="Download blockMeshDict")
    
    # Connect events
    generate_btn.click(
        fn=generate_blockmesh_dict,
        inputs=[shared_stl_file, flow_direction, background_scale, target_cell_size],
        outputs=[analysis_output, blockmesh_output]
    )
    
    # Connect download
    blockmesh_output.change(
        fn=lambda content: create_download_file(content, "blockMeshDict"),
        inputs=[blockmesh_output],
        outputs=[download]
    )

def generate_blockmesh_dict(stl_file, flow_direction, background_scale, target_cell_size):
    """Generate blockMeshDict - focused on this specific task"""
    try:
        if stl_file is None:
            return "❌ Please upload an STL file", ""
        
        summary, blockmesh_content = analyze_stl_and_generate_blockmesh(
            stl_file, flow_direction, background_scale, target_cell_size
        )
        return summary, blockmesh_content
    except Exception as e:
        return f"❌ Error: {str(e)}", ""

def create_download_file(content, filename):
    """Helper for download files"""
    import tempfile
    if content and not content.startswith("❌"):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write(content)
            return f.name
    return None
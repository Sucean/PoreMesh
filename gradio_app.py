import gradio as gr
from pathlib import Path
import tempfile
from src.pipeline import MeshPipeline, PreprocessingConfig

def create_gradio_interface():
    def process_tiff_file(tiff_file, block_size, cap_size, padding_size):
        config = PreprocessingConfig(
            block_size=block_size,
            cap_size=cap_size,
            padding_size=padding_size
        )
        
        pipeline = MeshPipeline(config)
        
        with tempfile.TemporaryDirectory() as tmpdir:
            result = pipeline.process_single_volume(
                Path(tiff_file.name), 
                Path(tmpdir)
            )
            
            if result.success:
                return f"Success! Generated {len(result.output_meshes)} meshes"
            else:
                return f"Error: {result.error_message}"
    
    iface = gr.Interface(
        fn=process_tiff_file,
        inputs=[
            gr.File(label="TIFF File"),
            gr.Slider(64, 512, value=256, label="Block Size"),
            gr.Slider(1, 50, value=10, label="Cap Size"), 
            gr.Slider(1, 20, value=8, label="Padding Size")
        ],
        outputs="text",
        title="FIB-SEM to Mesh Converter"
    )
    
    return iface

if __name__ == "__main__":
    iface = create_gradio_interface()
    iface.launch()
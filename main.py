import gradio as gr
import sys
import os

from ui.tiff_tab import create_tiff_tab
from ui.openfoam_tab import create_openfoam_tab
from pathlib import Path

# Add project root to path
# project_root = Path(__file__).parent
# sys.path.insert(0, str(project_root))

def create_interface():
    with gr.Blocks(title="PoreMesh") as demo:
        gr.Markdown("# PoreMesh - FIB-SEM to OpenFOAM Pipeline")

        with gr.Tab("TIFF to Mesh"):
            create_tiff_tab()

        with gr.Tab("Generate Controlfiles"):
            create_openfoam_tab()

        return demo

if __name__ == "__main__":
    demo = create_interface()
    demo.launch(server_name = "0.0.0.0")
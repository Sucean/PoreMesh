import gradio as gr
from pathlib import Path
import tempfile
import numpy as np
from src.pipeline import MeshPipeline, PreprocessingConfig
from src.stl_analyzer import STLAnalyzer
from src.openfoam_writer import OpenFOAMDict, OpenFOAMCaseBuilder, create_control_file, analyze_stl_and_generate_blockmesh
from src.template_manager import TemplateManager
import vtk

def create_gradio_interface():
    
    template_manager = TemplateManager()
    
    # Tab 1: TIFF to Mesh Conversion
    def process_tiff_file(tiff_file, block_size, cap_size, padding_size, threshold):
        try:
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
                    mesh_files = []
                    for mesh_path in result.output_meshes:
                        mesh_files.append(str(mesh_path))
                    
                    return f"✅ Success! Generated {len(result.output_meshes)} meshes\n" \
                           f"📊 Watertight blocks: {result.mesh_quality['watertight_blocks']}/{result.mesh_quality['total_blocks']}\n" \
                           f"⏱️ Processing time: {result.processing_time:.2f} seconds", mesh_files
                else:
                    return f"❌ Error: {result.error_message}", []
                    
        except Exception as e:
            return f"❌ Unexpected error: {str(e)}", []
    
    # Tab 2: System Control Files
    def generate_control_dict(application, start_time, end_time, delta_t, write_interval, write_format):
        """Generate controlDict with user parameters"""
        try:
            template = template_manager.get_template("controlDict")
            
            updates = {
                "application": application,
                "startTime": start_time,
                "endTime": end_time,
                "deltaT": delta_t,
                "writeInterval": write_interval,
                "writeFormat": write_format
            }
            
            template_manager.update_template("controlDict", updates)
            header = template_manager.get_header("controlDict")
            control_dict = create_control_file(header, template, "controlDict")
            
            return str(control_dict)
        except Exception as e:
            return f"❌ Error generating controlDict: {str(e)}"
    
    def generate_fv_schemes(ddt_scheme, grad_scheme, div_scheme, laplacian_scheme):
        """Generate fvSchemes with user parameters"""
        try:
            template = template_manager.get_template("fvSchemes")
            
            updates = {
                "ddtSchemes": {"default": ddt_scheme},
                "gradSchemes": {"default": grad_scheme},
                "divSchemes": {"default": div_scheme},
                "laplacianSchemes": {"default": laplacian_scheme}
            }
            
            template_manager.update_template("fvSchemes", updates)
            header = template_manager.get_header("fvSchemes")
            fv_schemes = create_control_file(header, template, "fvSchemes")
            
            return str(fv_schemes)
        except Exception as e:
            return f"❌ Error generating fvSchemes: {str(e)}"
    
    def generate_fv_solution(solver_type, p_solver, u_solver, p_tolerance, u_tolerance):
        """Generate fvSolution with user parameters"""
        try:
            template = template_manager.get_template("fvSolution")
            
            updates = {
                "solvers": {
                    "p": {
                        "solver": p_solver,
                        "tolerance": p_tolerance
                    },
                    "U": {
                        "solver": u_solver, 
                        "tolerance": u_tolerance
                    }
                }
            }
            
            template_manager.update_template("fvSolution", updates)
            header = template_manager.get_header("fvSolution")
            fv_solution = create_control_file(header, template, "fvSolution")
            
            return str(fv_solution)
        except Exception as e:
            return f"❌ Error generating fvSolution: {str(e)}"
    
    def generate_blockmesh_dict(stl_file, flow_direction, background_scale, target_cell_size):
        """Generate blockMeshDict from STL geometry"""
        try:
            if stl_file is None:
                return "❌ Please upload an STL file", ""
            
            summary, blockMeshContent = analyze_stl_and_generate_blockmesh(
                stl_file.name, flow_direction, background_scale, target_cell_size
            )
            return summary, blockMeshContent
        except Exception as e:
            return f"❌ Error generating blockMeshDict: {str(e)}", ""
    
    def generate_snappy_hex_mesh(castellated_mesh, snap_mesh, add_layers):
        """Generate snappyHexMeshDict"""
        try:
            template = template_manager.get_template("snappyHexMeshDict")
            
            updates = {
                "castellatedMesh": castellated_mesh,
                "snap": snap_mesh,
                "addLayers": add_layers
            }
            
            template_manager.update_template("snappyHexMeshDict", updates)
            header = template_manager.get_header("snappyHexMeshDict")
            snappy_dict = create_control_file(header, template, "snappyHexMeshDict")
            
            return str(snappy_dict)
        except Exception as e:
            return f"❌ Error generating snappyHexMeshDict: {str(e)}"
    
    # Create tabs
    with gr.Blocks(title="PoreMesh - FIB-SEM to OpenFOAM Pipeline") as demo:
        gr.Markdown("# 🏭 PoreMesh - FIB-SEM to OpenFOAM Pipeline")
        gr.Markdown("Convert micro-CT data to CFD-ready meshes and OpenFOAM cases")
        
        with gr.Tab("🔄 TIFF to Mesh"):
            gr.Markdown("### Convert TIFF stacks to 3D surface meshes")
            with gr.Row():
                with gr.Column():
                    tiff_file = gr.File(label="📁 Upload TIFF File", file_types=[".tif", ".tiff"])
                    block_size = gr.Slider(64, 512, value=256, label="📦 Block Size")
                    cap_size = gr.Slider(1, 50, value=10, label="🧢 Cap Size")
                    padding_size = gr.Slider(1, 20, value=8, label="🛡️ Padding Size")
                    threshold = gr.Slider(0, 255, value=127, label="🎯 Marching Cubes Threshold")
                    tiff_btn = gr.Button("🚀 Generate Meshes")
                
                with gr.Column():
                    tiff_output = gr.Textbox(label="📊 Processing Results", lines=4)
                    mesh_download = gr.File(label="📥 Download Generated Meshes", file_count="multiple")
        
        with gr.Tab("⚙️ System Control Files"):
            gr.Markdown("### Generate OpenFOAM System Control Files")
            
            # Shared STL file for geometry-based operations
            with gr.Row():
                stl_file_shared = gr.File(label="📁 Upload STL File for Geometry Analysis", file_types=[".stl"])
            
            # Collapsible sections for each control file
            with gr.Accordion("1. blockMeshDict", open=False):
                with gr.Row():
                    with gr.Column():
                        flow_direction = gr.Radio(
                            choices=["x", "y", "z"], 
                            value="z", 
                            label="🌊 Flow Direction",
                            info="X: left-right, Y: front-back, Z: bottom-top"
                        )
                        background_scale = gr.Slider(1.0, 3.0, value=1.2, label="📐 Background Scale", 
                                                   info="How much larger than geometry")
                        target_cell_size = gr.Slider(0.1, 5.0, value=1.0, label="🔍 Target Cell Size")
                        blockmesh_btn = gr.Button("🚀 Generate blockMeshDict")
                    
                    with gr.Column():
                        stl_output = gr.Textbox(label="📊 Analysis Results", lines=6)
                        blockmesh_output = gr.Code(
                            label="📝 Generated blockMeshDict", 
                            language="cpp",
                            lines=20
                        )
                        blockmesh_download = gr.File(label="📥 Download blockMeshDict")
            
            with gr.Accordion("2. controlDict", open=False):
                with gr.Row():
                    with gr.Column():
                        application = gr.Dropdown(
                            choices=["simpleFoam", "icoFoam", "pimpleFoam", "pisoFoam"],
                            value="simpleFoam",
                            label="🔧 Solver"
                        )
                        start_time = gr.Number(value=0, label="⏰ Start Time")
                        end_time = gr.Number(value=1000, label="⏰ End Time")
                        delta_t = gr.Number(value=1, label="⏱️ Time Step")
                        write_interval = gr.Number(value=100, label="📝 Write Interval")
                        write_format = gr.Radio(
                            choices=["ascii", "binary"],
                            value="binary",
                            label="💾 Write Format"
                        )
                        control_dict_btn = gr.Button("🚀 Generate controlDict")
                    
                    with gr.Column():
                        control_dict_output = gr.Code(label="📝 Generated controlDict", language="cpp", lines=15)
                        control_dict_download = gr.File(label="📥 Download controlDict")
            
            with gr.Accordion("3. fvSchemes", open=False):
                with gr.Row():
                    with gr.Column():
                        ddt_scheme = gr.Dropdown(
                            choices=["Euler", "steadyState", "CrankNicolson", "backward"],
                            value="steadyState",
                            label="⏳ Time Scheme"
                        )
                        grad_scheme = gr.Dropdown(
                            choices=["Gauss linear", "leastSquares", "cellLimited Gauss linear"],
                            value="Gauss linear",
                            label="📈 Gradient Scheme"
                        )
                        div_scheme = gr.Dropdown(
                            choices=["Gauss linear", "Gauss upwind", "Gauss limitedLinear", "Gauss linearUpwind"],
                            value="Gauss linear",
                            label="➗ Divergence Scheme"
                        )
                        laplacian_scheme = gr.Dropdown(
                            choices=["Gauss linear orthogonal", "Gauss linear corrected", "Gauss linear limited"],
                            value="Gauss linear orthogonal",
                            label="🌀 Laplacian Scheme"
                        )
                        fv_schemes_btn = gr.Button("🚀 Generate fvSchemes")
                    
                    with gr.Column():
                        fv_schemes_output = gr.Code(label="📝 Generated fvSchemes", language="cpp", lines=15)
                        fv_schemes_download = gr.File(label="📥 Download fvSchemes")
            
            with gr.Accordion("4. fvSolution", open=False):
                with gr.Row():
                    with gr.Column():
                        solver_type = gr.Radio(
                            choices=["SIMPLE", "PISO", "PIMPLE"],
                            value="SIMPLE",
                            label="🎯 Solver Type"
                        )
                        p_solver = gr.Dropdown(
                            choices=["GAMG", "PCG", "smoothSolver"],
                            value="GAMG",
                            label="📊 Pressure Solver"
                        )
                        u_solver = gr.Dropdown(
                            choices=["smoothSolver", "PBiCG", "GAMG"],
                            value="smoothSolver",
                            label="💨 Velocity Solver"
                        )
                        p_tolerance = gr.Number(value=1e-6, label="🎯 Pressure Tolerance")
                        u_tolerance = gr.Number(value=1e-6, label="🎯 Velocity Tolerance")
                        fv_solution_btn = gr.Button("🚀 Generate fvSolution")
                    
                    with gr.Column():
                        fv_solution_output = gr.Code(label="📝 Generated fvSolution", language="cpp", lines=15)
                        fv_solution_download = gr.File(label="📥 Download fvSolution")
            
            with gr.Accordion("5. snappyHexMeshDict", open=False):
                with gr.Row():
                    with gr.Column():
                        castellated_mesh = gr.Checkbox(value=True, label="🏰 Castellated Mesh")
                        snap_mesh = gr.Checkbox(value=True, label="🔗 Snap to Surface")
                        add_layers = gr.Checkbox(value=False, label="📚 Add Boundary Layers")
                        snappy_btn = gr.Button("🚀 Generate snappyHexMeshDict")
                    
                    with gr.Column():
                        snappy_output = gr.Code(label="📝 Generated snappyHexMeshDict", language="cpp", lines=15)
                        snappy_download = gr.File(label="📥 Download snappyHexMeshDict")
        
        # Connect events for TIFF tab
        tiff_btn.click(
            fn=process_tiff_file,
            inputs=[tiff_file, block_size, cap_size, padding_size, threshold],
            outputs=[tiff_output, mesh_download]
        )
        
        # Connect events for System Control Files tab
        blockmesh_btn.click(
            fn=generate_blockmesh_dict,
            inputs=[stl_file_shared, flow_direction, background_scale, target_cell_size],
            outputs=[stl_output, blockmesh_output]
        )
        
        control_dict_btn.click(
            fn=generate_control_dict,
            inputs=[application, start_time, end_time, delta_t, write_interval, write_format],
            outputs=[control_dict_output]
        )
        
        fv_schemes_btn.click(
            fn=generate_fv_schemes,
            inputs=[ddt_scheme, grad_scheme, div_scheme, laplacian_scheme],
            outputs=[fv_schemes_output]
        )
        
        fv_solution_btn.click(
            fn=generate_fv_solution,
            inputs=[solver_type, p_solver, u_solver, p_tolerance, u_tolerance],
            outputs=[fv_solution_output]
        )
        
        snappy_btn.click(
            fn=generate_snappy_hex_mesh,
            inputs=[castellated_mesh, snap_mesh, add_layers],
            outputs=[snappy_output]
        )
        
        # Download functionality for all generated files
        def create_download_file(content, filename):
            if content and not content.startswith("❌"):
                with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
                    f.write(content)
                    return f.name
            return None
        
        # Update downloads when content changes
        def update_blockmesh_download(content):
            file_path = create_download_file(content, "blockMeshDict")
            return gr.File(value=file_path) if file_path else gr.File(value=None)
        
        def update_control_dict_download(content):
            file_path = create_download_file(content, "controlDict")
            return gr.File(value=file_path) if file_path else gr.File(value=None)
        
        def update_fv_schemes_download(content):
            file_path = create_download_file(content, "fvSchemes")
            return gr.File(value=file_path) if file_path else gr.File(value=None)
        
        def update_fv_solution_download(content):
            file_path = create_download_file(content, "fvSolution")
            return gr.File(value=file_path) if file_path else gr.File(value=None)
        
        def update_snappy_download(content):
            file_path = create_download_file(content, "snappyHexMeshDict")
            return gr.File(value=file_path) if file_path else gr.File(value=None)
        
        # Connect download updates
        blockmesh_output.change(
            fn=update_blockmesh_download,
            inputs=[blockmesh_output],
            outputs=[blockmesh_download]
        )
        
        control_dict_output.change(
            fn=update_control_dict_download,
            inputs=[control_dict_output],
            outputs=[control_dict_download]
        )
        
        fv_schemes_output.change(
            fn=update_fv_schemes_download,
            inputs=[fv_schemes_output],
            outputs=[fv_schemes_download]
        )
        
        fv_solution_output.change(
            fn=update_fv_solution_download,
            inputs=[fv_solution_output],
            outputs=[fv_solution_download]
        )
        
        snappy_output.change(
            fn=update_snappy_download,
            inputs=[snappy_output],
            outputs=[snappy_download]
        )
    
    return demo

if __name__ == "__main__":
    demo = create_gradio_interface()
    demo.launch(
        server_name="0.0.0.0",
        share=False,
        debug=True
    )
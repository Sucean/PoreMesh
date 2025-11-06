import gradio as gr
from src.templates.control_dicts import FILE_HEADERS, FILE_BODY
from src.openfoam_writer import create_control_file

def create_base_component(template_name, component_definitions):
    """Factory function that creates any OpenFOAM-Dict Compnent"""
    components = {}
    
    with gr.Row():
        with gr.Column():    
            for key, component_args in component_definitions.items():
                kwargs = component_args.copy()
                component_type = kwargs.pop('component_type')
                
                components[key] = getattr(gr, component_type)(**kwargs)
            
            generate_btn = gr.Button(f"Generate {template_name}")

        with gr.Column():
            output = gr.Code(label=f"Generate {template_name}", language="cpp", lines=15)


    def generate_handler(*args):
        """Generate controlDict content"""
        try:
    
            template_copy = FILE_BODY[template_name].copy()
            header_copy = FILE_HEADERS[template_name].copy()
            
            keys = list(components.keys()) 
            for i, key in enumerate(keys):
                template_copy[key] = args[i]
                
            control_file = create_control_file(header_copy, template_copy, template_name)
            return str(control_file)
            
        except Exception as e:
            return f"[ERROR]: {str(e)}"
            
    generate_btn.click(fn=generate_handler, inputs=list(components.values()), outputs=[output])
    #output.change(fn=lambda content: create_download_file(content, "controlDict"), inputs=[output], outputs=[download])

    

def create_download_file(content, filename):
    """Helper for download files"""
    import tempfile
    if content and not content.startswith("❌"):
        with tempfile.NamedTemporaryFile(mode="w", suffix="", delete=False) as f:
            f.write(content)
            return f.name
    return None
    
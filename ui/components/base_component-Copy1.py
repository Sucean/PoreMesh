import gradio as gr
from src.templates.control_dicts import FILE_HEADERS, FILE_BODY
from src.openfoam_writer import create_control_file

def create_base_component(template_name, component_definitions, working_dir, current_dir):
    """Factory function that creates any OpenFOAM-Dict Compnent"""
    components = {}
    
    with gr.Row():
        with gr.Column():    
            # for key, component_args in component_definitions.items():
            #     kwargs = component_args.copy()
            #     component_type = kwargs.pop('component_type')
                
            #     components[key] = getattr(gr, component_type)(**kwargs)
            components = build_components(component_definitions)
            generate_btn = gr.Button(f"Generate {template_name}")
            save_btn = gr.Button("Save")
            analysis_output = gr.Textbox(label="📊 Analysis Results", lines=3)
            hidden_template = gr.Textbox(value=f"{template_name}", visible=False)
        with gr.Column():
            output = gr.Code(label=f"Generate {template_name}", language="cpp", lines=15)
            
def collect_leaves(cdict):
    leaves = []
    for v in cdict.values():
        if isinstance(v, dict):
            leaves.extend(collect_leaves(v))
        else:
            leaves.append(v)
    return leaves

def fill_template(template_part, component_part, values_iter):
    for key, val in template_part.items():
        if isinstance(val, dict):
            fill_template(template_part[key], component_part[key], values_iter)
        else:
            if key in component_part:
                template_part[key] = next(values_iter)

    
    # def generate_handler(*args):
    #     try:
    #         t_copy = FILE_BODY[template_name].copy()
    #         h_copy = FILE_HEADERS[template_name].copy()
    #         all_comps = collect_leaves(components)
    #         values_iter = iter(args)
    #         fill_template(t_copy, components, values_iter)
    #         control_file = create_control_file(h_copy, t_copy, template_name)
    #         return str(control_file)
    #     except Exception as e:
    #         return f"[ERROR]: {str(e)}"
                
    #     generate_btn.click(fn=generate_handler, inputs=collect_leaves(components), outputs=[output])
    #     save_btn.click(fn=write_data, inputs=[output, working_dir, current_dir, hidden_template], outputs=[analysis_output])
        #output.change(fn=write_data, inputs=[output, working_dir, current_dir], outputs=[analysis_output])

def generate_handler(*args):
    """Generate controlDict content"""
    try:
        template_copy = FILE_BODY[template_name].copy()
        header_copy = FILE_HEADERS[template_name].copy()

        # collect flat component order
        flat_components = collect_leaves(components)
        values_iter = iter(args)

        # recursive assignment
        def assign_recursive(template_subdict, comp_subdict):
            for key, val in comp_subdict.items():
                if isinstance(val, dict):
                    if key not in template_subdict:
                        template_subdict[key] = {}
                    assign_recursive(template_subdict[key], val)
                else:
                    if key in template_subdict:
                        template_subdict[key] = next(values_iter)

        assign_recursive(template_copy, components)

        control_file = create_control_file(header_copy, template_copy, template_name)
        return str(control_file)

    except Exception as e:
        return f"[ERROR]: {str(e)}"

def collect_leaves(comp_dict):
    leaves = []
    for v in comp_dict.values():
        if isinstance(v, dict):
            leaves.extend(collect_leaves(v))
        else:
            leaves.append(v)
    return leaves

def build_components(defs):
    comps = {}
    for key, val in defs.items():
        if isinstance(val, dict) and 'component_type' in val:
            kwargs = val.copy()
            comp_type = kwargs.pop('component_type')
            comps[key] = getattr(gr, comp_type)(**kwargs)
        elif isinstance(val, dict):
            with gr.Accordion(key, open=False):
                comps[key] = build_components(val)
    return comps
            

def write_data(component_output, working_dir, current_dir, template_name):
    if template_name not in ('U', 'p'):
        dict_dir = f'{working_dir}/{current_dir}/system/{template_name}'
    else:
        dict_dir = f'{working_dir}/{current_dir}/0/{template_name}'
    
    with open(dict_dir, 'w') as f:
        f.write(component_output)
    return f'saved data to {dict_dir}'

def create_download_file(content, filename):
    """Helper for download files"""
    import tempfile
    if content and not content.startswith("❌"):
        with tempfile.NamedTemporaryFile(mode="w", suffix="", delete=False) as f:
            f.write(content)
            return f.name
    return None
    
import gradio as gr
import os
from pathlib import Path
from src.templates.control_dicts import FILE_HEADERS, FILE_BODY
from src.openfoam_writer import create_control_file


def build_components(defs):
    comps = {}
    for key, val in defs.items():
        if isinstance(val, dict) and "component_type" in val:
            kwargs = val.copy()
            comp_type = kwargs.pop("component_type")
            comps[key] = getattr(gr, comp_type)(**kwargs)
        elif isinstance(val, dict):
            with gr.Accordion(key, open=False):
                comps[key] = build_components(val)
    return comps


def collect_leaves(comp_dict):
    leaves = []
    for v in comp_dict.values():
        if isinstance(v, dict):
            leaves.extend(collect_leaves(v))
        else:
            leaves.append(v)
    return leaves


def create_base_component(template_name, component_definitions, working_dir, current_dir, **kwargs):
    components = {}

    get_dynamic_values = kwargs.get("snappy_function")
    
    with gr.Row():
        with gr.Column():
            components = build_components(component_definitions)
            generate_btn = gr.Button(f"Generate {template_name}")
            save_btn = gr.Button("Save")
            analysis_output = gr.Textbox(label="📊 Analysis Results", lines=3)
            hidden_template = gr.Textbox(value=template_name, visible=False)
        with gr.Column():
            output = gr.Code(label=f"Generated {template_name}", language="cpp", lines=15)

    # --- define the handler INSIDE this scope ---
    def generate_handler(working_dir, current_dir, *args):
        try:
            template_copy = FILE_BODY[template_name].copy()
            header_copy = FILE_HEADERS[template_name].copy()
            flat_components = collect_leaves(components)
            
            if get_dynamic_values:
                geometry_dict, castellated_dict = get_dynamic_values(working_dir, current_dir)
                template_copy["geometry"] = geometry_dict
                template_copy["castellatedMeshControls"].update(castellated_dict)
            
            
            values_iter = iter(args)

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

    # connect buttons properly
    generate_btn.click(
        fn=generate_handler,
        inputs=[working_dir, current_dir, *collect_leaves(components)],
        outputs=[output],
    )

    save_btn.click(
        fn=write_data,
        inputs=[output, working_dir, current_dir, hidden_template],
        outputs=[analysis_output],
    )


def write_data(component_output, working_dir, current_dir, template_name):
    if template_name not in ("U", "p"):
        dict_dir = f"{working_dir}/{current_dir}/system/{template_name}"
    elif template_name in ("transportProperties", "turbulenceProperties"):
        dict_dir = f"{working_dir}/{current_dir}/constant/{template_name}"
    else:
        dict_dir = f"{working_dir}/{current_dir}/0/{template_name}"

    with open(dict_dir, "w") as f:
        f.write(component_output)
    return f"saved data to {dict_dir}"


def create_download_file(content, filename):
    import tempfile

    if content and not content.startswith("❌"):
        with tempfile.NamedTemporaryFile(mode="w", suffix="", delete=False) as f:
            f.write(content)
            return f.name
    return None

# src/template_manager.py
from pathlib import Path
from typing import Dict, Any
import copy

class TemplateManager:
    """Manages OpenFOAM template storage and modification"""
    
    def __init__(self):
        self.templates = {}
        self.headers = {}
        self.load_templates()
    
    def load_templates(self):
        """Load all templates from template modules"""
        from .templates.control_dicts import (
            CONTROL_DICT_TEMPLATE, FV_SCHEMES_TEMPLATE, FV_SOLUTION_TEMPLATE, FILE_HEADERS
        )
        from .templates.snappy_dicts import SNAPPY_HEX_MESH_TEMPLATE, SNAPPY_HEADER
        
        self.templates = {
            "controlDict": CONTROL_DICT_TEMPLATE,
            "fvSchemes": FV_SCHEMES_TEMPLATE, 
            "fvSolution": FV_SOLUTION_TEMPLATE,
            "snappyHexMeshDict": SNAPPY_HEX_MESH_TEMPLATE
        }
        
        self.headers = FILE_HEADERS
        self.headers["snappyHexMeshDict"] = SNAPPY_HEADER
    
    def get_template(self, file_type: str) -> Dict[str, Any]:
        """Get a deep copy of template for modification"""
        return copy.deepcopy(self.templates.get(file_type, {}))
    
    def get_header(self, file_type: str) -> Dict[str, Any]:
        """Get header for file type"""
        return self.headers.get(file_type, {}).copy()
    
    def update_template(self, file_type: str, updates: Dict[str, Any]):
        """Update a template with new values"""
        if file_type in self.templates:
            self._update_dict_recursive(self.templates[file_type], updates)
    
    def _update_dict_recursive(self, target: Dict, updates: Dict):
        """Recursively update nested dictionary"""
        for key, value in updates.items():
            if key in target and isinstance(target[key], dict) and isinstance(value, dict):
                self._update_dict_recursive(target[key], value)
            else:
                target[key] = value
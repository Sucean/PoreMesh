import tifffile
import numpy as np
from pathlib import Path
from typing import Union

class DataLoader:
    def __init__(self):
        self.supported_formats = ['.tif', '.tiff']
    
    def load_tif(self, path: Union[str, Path]) -> np.ndarray:
        """Load TIFF file and convert to binary volume"""
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"File {path} not found")
        
        data = tifffile.imread(path)
        
        # Handle multi-channel data
        if len(data.shape) >= 4 and data.shape[-1] == 3:
            if np.allclose(data[...,0], data[...,1]) and np.allclose(data[...,0], data[...,2]):
                data = data[...,0]
            else:
                data = np.mean(data, axis=-1)
        
        # Ensure uint8
        if data.dtype != np.uint8:
            data = data.astype(np.uint8)
            
        return data
    
    def validate_data(self, data: np.ndarray) -> bool:
        """Validate that data meets requirements"""
        return (len(data.shape) == 3 and 
                data.dtype == np.uint8 and 
                data.max() <= 255 and 
                data.min() >= 0)
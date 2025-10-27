import numpy as np
from typing import Tuple, Dict
from dataclasses import dataclass

@dataclass
class PreprocessingConfig:
    cap_size: int = 10
    cap_axis: str = 'z'  # 'x', 'y', 'z'
    cap_value: int = 255
    padding_size: int = 4
    block_size: int = 256

class Preprocessor:
    def __init__(self, config: PreprocessingConfig = None):
        self.config = config or PreprocessingConfig()
        self.axes_map = {'z': 0, 'y': 1, 'x': 2}
    
    def add_caps(self, data: np.ndarray, cap_size: int = None, axis: str = None, value: int = None) -> np.ndarray:
        """Add caps to volume data along specified axis"""
        cap_size = cap_size or self.config.cap_size
        axis = axis or self.config.cap_axis
        value = value or self.config.cap_value
        
        ax = self.axes_map[axis]
        shape = list(data.shape)
        shape[ax] += 2 * cap_size
        
        cap_data = np.zeros(shape, dtype=data.dtype)
        
        # Create slices
        slices = [slice(None)] * 3
        slices[ax] = slice(cap_size, cap_size + data.shape[ax])
        
        start_cap = [slice(None)] * 3
        start_cap[ax] = slice(0, cap_size)
        
        end_cap = [slice(None)] * 3
        end_cap[ax] = slice(-cap_size, None)
        
        cap_data[tuple(start_cap)] = value
        cap_data[tuple(slices)] = data
        cap_data[tuple(end_cap)] = value
        
        return cap_data
    
    def add_padding(self, data: np.ndarray, pad_size: int = None) -> np.ndarray:
        """Add symmetric padding to volume"""
        pad_size = pad_size or self.config.padding_size
        return np.pad(data, 
                     ((pad_size, pad_size), (pad_size, pad_size), (pad_size, pad_size)), 
                     mode='constant', constant_values=0)
    
    def blockify(self, data: np.ndarray, block_size: int = None, cap_size: int = None, axis: str = None) -> np.ndarray:
        """Split volume into manageable blocks with caps"""
        block_size = block_size or self.config.block_size
        cap_size = cap_size or self.config.cap_size
        axis = axis or self.config.cap_axis
        
        ax = self.axes_map[axis]
        z, x, y = data.shape
        
        # Calculate number of blocks
        nz = z // block_size
        nx = x // block_size
        ny = y // block_size
        
        # Compute block shape with caps
        block_shape = list((block_size, block_size, block_size))
        block_shape[ax] += 2 * cap_size
        block_shape = tuple(block_shape)
        
        n_blocks = nz * nx * ny
        subvolumes = np.zeros((n_blocks,) + block_shape, dtype=data.dtype)
        
        idx = 0
        for zi in range(nz):
            for xi in range(nx):
                for yi in range(ny):
                    sub = data[
                        zi * block_size : (zi + 1) * block_size,
                        xi * block_size : (xi + 1) * block_size,
                        yi * block_size : (yi + 1) * block_size
                    ]
                    subvolumes[idx] = self.add_caps(sub, cap_size, axis)
                    idx += 1
        
        return subvolumes
    
    def preprocess_single_block(self, data: np.ndarray) -> np.ndarray:
        """Full preprocessing pipeline for a single block"""
        capped = self.add_caps(data)
        padded = self.add_padding(capped)
        return padded
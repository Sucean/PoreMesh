from pathlib import Path
import numpy as np
from typing import List, Dict, Any
import json
from dataclasses import dataclass, asdict
import multiprocessing as mp
from typing import Tuple
# Relative imports within the package
from .data_loader import DataLoader
from .preprocessor import Preprocessor, PreprocessingConfig
from .mesh_generator import MeshGenerator


@dataclass
class PipelineResult:
    input_path: Path
    output_meshes: List[Path]
    processing_time: float
    mesh_quality: Dict[str, Any]
    success: bool
    error_message: str = ""
    
def _process_single_block(args):
    """
    Worker function to process a single block.
    This function must be defined at the top level for multiprocessing.
    """
    block_data, block_idx, output_dir, config_dict, threshold = args
    
    # Recreate the preprocessor and mesh generator in the worker process
    config = PreprocessingConfig(**config_dict)
    preprocessor = Preprocessor(config)
    mesh_generator = MeshGenerator(threshold=threshold)
    
    try:
        # Preprocess the block (add caps and padding)
        processed_block = preprocessor.preprocess_single_block(block_data)
        # Generate mesh
        mesh = mesh_generator.generate_mesh_from_array(processed_block)
        # Test watertightness
        boundary_edges = mesh_generator.test_watertightness(mesh)
        # Save mesh
        mesh_path = output_dir / f"block_{block_idx:04d}.stl"
        mesh_generator.write_mesh(mesh, mesh_path)
        
        return block_idx, mesh_path, boundary_edges
    except Exception as e:
        print(f"Error processing block {block_idx}: {str(e)}")
        return block_idx, None, -1



class MeshPipeline:
    def __init__(self, config: PreprocessingConfig = None, num_processes: int = None):
        self.data_loader = DataLoader()
        self.preprocessor = Preprocessor(config)
        self.mesh_generator = MeshGenerator()
        self.num_processes = num_processes or mp.cpu_count()  # NEW LINE
        self.results = []

    def process_single_volume_parallel(self, input_path: Path, output_dir: Path) -> PipelineResult:
        """Process volume using multiple processes"""
        import time
        start_time = time.time()
        
        try:
            # Load data
            data = self.data_loader.load_tif(input_path)
            if not self.data_loader.validate_data(data):
                raise ValueError("Invalid data format")
            
            # Preprocess and blockify
            blocks = self.preprocessor.blockify(data)
            
            output_dir = Path(output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)
            
            print(f"Processing {len(blocks)} blocks using {self.num_processes} processes...")
            
            # Prepare arguments for multiprocessing
            config_dict = {
                'cap_size': self.preprocessor.config.cap_size,
                'cap_axis': self.preprocessor.config.cap_axis,
                'cap_value': self.preprocessor.config.cap_value,
                'padding_size': self.preprocessor.config.padding_size,
                'block_size': self.preprocessor.config.block_size
            }
            
            args_list = [
                (block, i, output_dir, config_dict, self.mesh_generator.threshold)
                for i, block in enumerate(blocks)
            ]
            
            # Process blocks in parallel
            with mp.Pool(processes=self.num_processes) as pool:
                results = pool.map(_process_single_block, args_list)
            
            # Collect results
            output_meshes = []
            mesh_quality = {"total_blocks": len(blocks), "watertight_blocks": 0}
            
            for block_idx, mesh_path, boundary_edges in results:
                if mesh_path is not None:
                    output_meshes.append(mesh_path)
                    if boundary_edges == 0:
                        mesh_quality["watertight_blocks"] += 1
                else:
                    print(f"Block {block_idx} failed to process")
            
            processing_time = time.time() - start_time
            
            return PipelineResult(
                input_path=input_path,
                output_meshes=output_meshes,
                processing_time=processing_time,
                mesh_quality=mesh_quality,
                success=True
            )
            
        except Exception as e:
            return PipelineResult(
                input_path=input_path,
                output_meshes=[],
                processing_time=0,
                mesh_quality={},
                success=False,
                error_message=str(e)
            )
    
    def process_single_volume(self, input_path: Path, output_dir: Path, use_parallel: bool = True) -> PipelineResult:
        """Main processing method with option for parallel processing"""
        if use_parallel:
            return self.process_single_volume_parallel(input_path, output_dir)
        else:
            # Keep the original sequential version as fallback
            return self._process_single_volume_sequential(input_path, output_dir)
    
    def _process_single_volume_sequential(self, input_path: Path, output_dir: Path) -> PipelineResult:
        """Process a single volume file"""
        import time
        start_time = time.time()
        
        try:
            # Load data
            data = self.data_loader.load_tif(input_path)
            if not self.data_loader.validate_data(data):
                raise ValueError("Invalid data format")
            
            # Preprocess and blockify
            blocks = self.preprocessor.blockify(data)
            
            # Generate meshes
            output_meshes = []
            mesh_quality = {"total_blocks": len(blocks), "watertight_blocks": 0}
            
            output_dir = Path(output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)
            
            for i, block in enumerate(blocks):
                processed_block = self.preprocessor.preprocess_single_block(block)
                mesh = self.mesh_generator.generate_mesh_from_array(processed_block)
                
                # Test quality
                boundary_edges = self.mesh_generator.test_watertightness(mesh)
                if boundary_edges == 0:
                    mesh_quality["watertight_blocks"] += 1
                
                # Save mesh
                mesh_path = output_dir / f"block_{i:04d}.stl"
                self.mesh_generator.write_mesh(mesh, mesh_path)
                output_meshes.append(mesh_path)
            
            processing_time = time.time() - start_time
            
            return PipelineResult(
                input_path=input_path,
                output_meshes=output_meshes,
                processing_time=processing_time,
                mesh_quality=mesh_quality,
                success=True
            )
            
        except Exception as e:
            return PipelineResult(
                input_path=input_path,
                output_meshes=[],
                processing_time=0,
                mesh_quality={},
                success=False,
                error_message=str(e)
            )
    
    def save_pipeline_report(self, output_dir: Path):
        """Save processing report"""
        report = {
            "total_files": len(self.results),
            "successful_files": sum(1 for r in self.results if r.success),
            "results": [asdict(r) for r in self.results]
        }
        
        with open(output_dir / "pipeline_report.json", "w") as f:
            json.dump(report, f, indent=2, default=str)
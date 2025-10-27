#!/usr/bin/env python3
"""
Main pipeline runner for FIB-SEM to Mesh processing
"""

import argparse
from pathlib import Path
import sys
import multiprocessing as mp

# Add the parent directory to Python path so we can import from src
sys.path.insert(0, str(Path(__file__).parent))

from src.pipeline import MeshPipeline, PreprocessingConfig

def main():
    parser = argparse.ArgumentParser(description="FIB-SEM to Mesh Pipeline")
    parser.add_argument("--input", required=True, help="Input TIFF file or directory")
    parser.add_argument("--output", required=True, help="Output directory for meshes")
    parser.add_argument("--block-size", type=int, default=256, help="Block size for processing")
    parser.add_argument("--cap-size", type=int, default=10, help="Cap size for mesh generation")
    parser.add_argument("--padding", type=int, default=8, help="Padding size")
    parser.add_argument("--threshold", type=int, default=127, help="Marching cubes threshold")
    parser.add_argument("--processes", type=int, default=mp.cpu_count(), 
                       help=f"Number of parallel processes (default: CPU count = {mp.cpu_count()})")
    parser.add_argument("--no-parallel", action="store_true", help="Disable parallel processing")
    
    args = parser.parse_args()
    
    # Create config
    config = PreprocessingConfig(
        block_size=args.block_size,
        cap_size=args.cap_size,
        padding_size=args.padding
    )
    
    # Initialize pipeline
    pipeline = MeshPipeline(config, num_processes=args.processes)
    
    # Process files
    input_path = Path(args.input)
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    use_parallel = not args.no_parallel
    
    if input_path.is_file():
        print(f"Processing single file: {input_path}")
        if use_parallel:
            print(f"Using {args.processes} parallel processes")
        else:
            print("Using sequential processing")
            
        result = pipeline.process_single_volume(input_path, output_dir, use_parallel=use_parallel)
        pipeline.results.append(result)
        
        if result.success:
            print(f"Success! Generated {len(result.output_meshes)} meshes")
            print(f"Watertight blocks: {result.mesh_quality['watertight_blocks']}/{result.mesh_quality['total_blocks']}")
            print(f"Processing time: {result.processing_time:.2f} seconds")
        else:
            print(f"Error: {result.error_message}")
            
    else:
        # Process all TIFF files in directory
        print(f"Processing directory: {input_path}")
        tiff_files = list(input_path.glob("*.tif")) + list(input_path.glob("*.tiff"))
        if not tiff_files:
            print("No TIFF files found in directory")
            return
            
        for tiff_file in tiff_files:
            print(f"Processing: {tiff_file.name}")
            # FIX: Add use_parallel parameter here
            result = pipeline.process_single_volume(tiff_file, output_dir / tiff_file.stem, use_parallel=use_parallel)
            pipeline.results.append(result)
            
            if result.success:
                # FIX: Add time information
                print(f"  ✓ Generated {len(result.output_meshes)} meshes in {result.processing_time:.2f}s")
            else:
                print(f"  ✗ Failed: {result.error_message}")
    
    # Save report
    pipeline.save_pipeline_report(output_dir)
    
    # Print summary
    successful = sum(1 for r in pipeline.results if r.success)
    # FIX: Add total time calculation
    total_time = sum(r.processing_time for r in pipeline.results if r.success)
    print(f"\nProcessing complete: {successful}/{len(pipeline.results)} successful")
    print(f"Total processing time: {total_time:.2f} seconds")  # FIX: Add total time
    print(f"Detailed report saved to: {output_dir / 'pipeline_report.json'}")

if __name__ == "__main__":
    main()
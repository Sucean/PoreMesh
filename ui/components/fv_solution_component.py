import gradio as gr
from .base_component import create_base_component

def create_fv_solution_component(working_dir, current_dir):
    component_definitions = {
        "algorithm_type": {
            "component_type": "Radio",
            "choices": ["SIMPLE", "PISO", "PIMPLE"],
            "value": "PIMPLE",
            "label": "Solver Algorithm"
        },
        "solvers": {
            "p": {
                "solver": {
                    "component_type": "Dropdown",
                    "choices": ["PCG", "PBiCG", "PBiCGStab", "smoothSolver", "GAMG", "diagonal"],
                    "value": "GAMG",
                    "label": "Pressure Solver"
                },
                "preconditioner": {
                    "component_type": "Dropdown",
                    "choices": ["DIC", "DILU", "FDIC", "GAMG", "diagonal", "none"],
                    "value": "DIC",
                    "label": "Preconditioner (for PCG/PBiCG solvers)"
                },
                "smoother": {
                    "component_type": "Dropdown",
                    "choices": ["GaussSeidel", "symGaussSeidel", "DIC", "DILU", "DICGaussSeidel"],
                    "value": "GaussSeidel",
                    "label": "Smoother (for smoothSolver or GAMG)"
                },
                "agglomerator": {
                    "component_type": "Dropdown",
                    "choices": ["faceAreaPair", "algebraicPair"],
                    "value": "faceAreaPair",
                    "label": "Agglomerator (for GAMG)"
                },
                "nCellsInCoarsestLevel": {
                    "component_type": "Number",
                    "value": 10,
                    "label": "Cells in Coarsest Level (for GAMG)",
                    "minimum": 1,
                    "step": 1
                },
                "mergeLevels": {
                    "component_type": "Number",
                    "value": 1,
                    "label": "Merge Levels (for GAMG)",
                    "minimum": 1,
                    "step": 1
                },
                "cacheAgglomeration": {
                    "component_type": "Checkbox",
                    "value": True,
                    "label": "Cache Agglomeration (for GAMG)"
                },
                "directSolveCoarsest": {
                    "component_type": "Checkbox",
                    "value": False,
                    "label": "Direct Solve Coarsest (for GAMG)"
                },
                "nPreSweeps": {
                    "component_type": "Number",
                    "value": 0,
                    "label": "Pre Sweeps (for GAMG)",
                    "minimum": 0,
                    "step": 1
                },
                "preSweepsLevelMultiplier": {
                    "component_type": "Number",
                    "value": 1,
                    "label": "Pre Sweeps Level Multiplier (for GAMG)",
                    "minimum": 1,
                    "step": 1
                },
                "maxPreSweeps": {
                    "component_type": "Number",
                    "value": 4,
                    "label": "Max Pre Sweeps (for GAMG)",
                    "minimum": 1,
                    "step": 1
                },
                "nPostSweeps": {
                    "component_type": "Number",
                    "value": 2,
                    "label": "Post Sweeps (for GAMG)",
                    "minimum": 0,
                    "step": 1
                },
                "postSweepsLevelMultiplier": {
                    "component_type": "Number",
                    "value": 1,
                    "label": "Post Sweeps Level Multiplier (for GAMG)",
                    "minimum": 1,
                    "step": 1
                },
                "maxPostSweeps": {
                    "component_type": "Number",
                    "value": 4,
                    "label": "Max Post Sweeps (for GAMG)",
                    "minimum": 1,
                    "step": 1
                },
                "nFinestSweeps": {
                    "component_type": "Number",
                    "value": 2,
                    "label": "Finest Sweeps (for GAMG)",
                    "minimum": 1,
                    "step": 1
                },
                "nSweeps": {
                    "component_type": "Number",
                    "value": 1,
                    "label": "Sweeps (for smoothSolver)",
                    "minimum": 1,
                    "step": 1
                },
                "tolerance": {
                    "component_type": "Number",
                    "value": 1e-07,
                    "label": "Tolerance",
                    "precision": 10
                },
                "relTol": {
                    "component_type": "Number",
                    "value": 0.01,
                    "label": "Relative Tolerance",
                    "minimum": 0,
                    "maximum": 1,
                    "step": 0.01,
                    "precision": 4
                },
                "maxIter": {
                    "component_type": "Number",
                    "value": 100,
                    "label": "Max Iterations",
                    "minimum": 1,
                    "step": 1
                }
            },
            "pFinal": {
                "solver": {
                    "component_type": "Textbox",
                    "value": "$p",
                    "label": "Final Solver Reference (e.g., $p)"
                },
                "tolerance": {
                    "component_type": "Number",
                    "value": 1e-10,
                    "label": "Final Tolerance",
                    "precision": 10
                },
                "relTol": {
                    "component_type": "Number",
                    "value": 0,
                    "label": "Final Relative Tolerance",
                    "minimum": 0,
                    "maximum": 1,
                    "step": 0.01,
                    "precision": 4
                }
            },
            "U": {
                "solver": {
                    "component_type": "Dropdown",
                    "choices": ["PCG", "PBiCG", "PBiCGStab", "smoothSolver", "GAMG", "diagonal"],
                    "value": "smoothSolver",
                    "label": "Velocity Solver"
                },
                "preconditioner": {
                    "component_type": "Dropdown",
                    "choices": ["DIC", "DILU", "FDIC", "GAMG", "diagonal", "none"],
                    "value": "DILU",
                    "label": "Preconditioner (for PCG/PBiCG solvers)"
                },
                "smoother": {
                    "component_type": "Dropdown",
                    "choices": ["GaussSeidel", "symGaussSeidel", "DIC", "DILU", "DICGaussSeidel"],
                    "value": "GaussSeidel",
                    "label": "Smoother (for smoothSolver or GAMG)"
                },
                "agglomerator": {
                    "component_type": "Dropdown",
                    "choices": ["faceAreaPair", "algebraicPair"],
                    "value": "faceAreaPair",
                    "label": "Agglomerator (for GAMG)"
                },
                "nCellsInCoarsestLevel": {
                    "component_type": "Number",
                    "value": 10,
                    "label": "Cells in Coarsest Level (for GAMG)",
                    "minimum": 1,
                    "step": 1
                },
                "mergeLevels": {
                    "component_type": "Number",
                    "value": 1,
                    "label": "Merge Levels (for GAMG)",
                    "minimum": 1,
                    "step": 1
                },
                "cacheAgglomeration": {
                    "component_type": "Checkbox",
                    "value": True,
                    "label": "Cache Agglomeration (for GAMG)"
                },
                "directSolveCoarsest": {
                    "component_type": "Checkbox",
                    "value": False,
                    "label": "Direct Solve Coarsest (for GAMG)"
                },
                "nPreSweeps": {
                    "component_type": "Number",
                    "value": 0,
                    "label": "Pre Sweeps (for GAMG)",
                    "minimum": 0,
                    "step": 1
                },
                "preSweepsLevelMultiplier": {
                    "component_type": "Number",
                    "value": 1,
                    "label": "Pre Sweeps Level Multiplier (for GAMG)",
                    "minimum": 1,
                    "step": 1
                },
                "maxPreSweeps": {
                    "component_type": "Number",
                    "value": 4,
                    "label": "Max Pre Sweeps (for GAMG)",
                    "minimum": 1,
                    "step": 1
                },
                "nPostSweeps": {
                    "component_type": "Number",
                    "value": 2,
                    "label": "Post Sweeps (for GAMG)",
                    "minimum": 0,
                    "step": 1
                },
                "postSweepsLevelMultiplier": {
                    "component_type": "Number",
                    "value": 1,
                    "label": "Post Sweeps Level Multiplier (for GAMG)",
                    "minimum": 1,
                    "step": 1
                },
                "maxPostSweeps": {
                    "component_type": "Number",
                    "value": 4,
                    "label": "Max Post Sweeps (for GAMG)",
                    "minimum": 1,
                    "step": 1
                },
                "nFinestSweeps": {
                    "component_type": "Number",
                    "value": 2,
                    "label": "Finest Sweeps (for GAMG)",
                    "minimum": 1,
                    "step": 1
                },
                "nSweeps": {
                    "component_type": "Number",
                    "value": 1,
                    "label": "Sweeps (for smoothSolver)",
                    "minimum": 1,
                    "step": 1
                },
                "tolerance": {
                    "component_type": "Number",
                    "value": 1e-08,
                    "label": "Tolerance",
                    "precision": 10
                },
                "relTol": {
                    "component_type": "Number",
                    "value": 0.1,
                    "label": "Relative Tolerance",
                    "minimum": 0,
                    "maximum": 1,
                    "step": 0.01,
                    "precision": 4
                },
                "maxIter": {
                    "component_type": "Number",
                    "value": 100,
                    "label": "Max Iterations",
                    "minimum": 1,
                    "step": 1
                }
            },
            "UFinal": {
                "solver": {
                    "component_type": "Textbox",
                    "value": "$U",
                    "label": "Final Solver Reference (e.g., $U)"
                },
                "tolerance": {
                    "component_type": "Number",
                    "value": 1e-10,
                    "label": "Final Tolerance",
                    "precision": 10
                },
                "relTol": {
                    "component_type": "Number",
                    "value": 0,
                    "label": "Final Relative Tolerance",
                    "minimum": 0,
                    "maximum": 1,
                    "step": 0.01,
                    "precision": 4
                }
            }
        },
        "SIMPLE": {
            "nNonOrthogonalCorrectors": {
                "component_type": "Number",
                "value": 0,
                "label": "Non-Orthogonal Correctors",
                "minimum": 0,
                "step": 1
            },
            "consistent": {
                "component_type": "Checkbox",
                "value": True,
                "label": "Use SIMPLEC (Consistent)"
            },
            "momentumPredictor": {
                "component_type": "Checkbox",
                "value": False,
                "label": "Momentum Predictor"
            },
            "pRefCell": {
                "component_type": "Number",
                "value": 0,
                "label": "Reference Cell",
                "minimum": 0,
                "step": 1
            },
            "pRefValue": {
                "component_type": "Number",
                "value": 0,
                "label": "Reference Value"
            }
        },
        "PISO": {
            "nCorrectors": {
                "component_type": "Number",
                "value": 2,
                "label": "Correctors",
                "minimum": 1,
                "step": 1
            },
            "nNonOrthogonalCorrectors": {
                "component_type": "Number",
                "value": 1,
                "label": "Non-Orthogonal Correctors",
                "minimum": 0,
                "step": 1
            },
            "momentumPredictor": {
                "component_type": "Checkbox",
                "value": False,
                "label": "Momentum Predictor"
            },
            "pRefCell": {
                "component_type": "Number",
                "value": 0,
                "label": "Reference Cell",
                "minimum": 0,
                "step": 1
            },
            "pRefValue": {
                "component_type": "Number",
                "value": 0,
                "label": "Reference Value"
            }
        },
        "PIMPLE": {
            "nOuterCorrectors": {
                "component_type": "Number",
                "value": 20,
                "label": "Outer Correctors",
                "minimum": 1,
                "step": 1
            },
            "nCorrectors": {
                "component_type": "Number",
                "value": 1,
                "label": "Correctors",
                "minimum": 1,
                "step": 1
            },
            "nNonOrthogonalCorrectors": {
                "component_type": "Number",
                "value": 1,
                "label": "Non-Orthogonal Correctors",
                "minimum": 0,
                "step": 1
            },
            "momentumPredictor": {
                "component_type": "Checkbox",
                "value": False,
                "label": "Momentum Predictor"
            },
            "pRefCell": {
                "component_type": "Number",
                "value": 0,
                "label": "Reference Cell",
                "minimum": 0,
                "step": 1
            },
            "pRefValue": {
                "component_type": "Number",
                "value": 0,
                "label": "Reference Value"
            }
        },
        "relaxationFactors": {
            "fields": {
                "p": {
                    "component_type": "Number",
                    "value": 0.3,
                    "label": "Pressure Field Relaxation",
                    "minimum": 0,
                    "maximum": 1,
                    "step": 0.05
                }
            },
            "equations": {
                "U": {
                    "component_type": "Number",
                    "value": 0.7,
                    "label": "Velocity Equation Relaxation",
                    "minimum": 0,
                    "maximum": 1,
                    "step": 0.05
                }
            }
        }
    }
    
    return create_base_component("fvSolution", component_definitions, working_dir, current_dir)
"""
Templates for OpenFOAM control files
"""

# Common termination patterns
NEEDS_TERMINATION = {
    "geometry", "castellatedMeshControls", "snapControls", 
    "addLayersControls", "meshQualityControls", "refinementSurfaces",
    "refinementRegions", "solvers", "PIMPLE", "SIMPLE", "relaxationFactors"
}

FILE_BODY = {    
    # controlDict template
    "controlDict": {
        "application": "simpleFoam",
        "startFrom": "startTime",
        "startTime": 0,
        "stopAt": "endTime", 
        "endTime": 1000,
        "deltaT": 1,
        "writeControl": "runTime",
        "writeInterval": 100,
        "purgeWrite": 0,
        "writeFormat": "binary",
        "writePrecision": 6,
        "writeCompression": "off",
        "timeFormat": "general",
        "timePrecision": 6,
        "runTimeModifiable": True,
        "adjustTimeStep": "no",
        "maxCo": 0.5,
        "functions": {"#include": "FOs"},
        "libs": []
    },
    
    # fvSchemes template  
    "fvSchemes": {
        "ddtSchemes": {"default": "steadyState"},
        "gradSchemes": {
            "default": "Gauss linear",
            "grad(p)": "Gauss linear", 
            "grad(U)": "cellLimited Gauss linear 1"
        },
        "divSchemes": {
            "default": "Gauss linear",
            "div(phi,U)": "Gauss linearUpwind grad(U)",
            "div(phi,k)": "Gauss upwind",
            "div(phi,omega)": "Gauss upwind",
            "div(phi,epsilon)": "Gauss upwind", 
            "div(phi,nut)": "Gauss upwind",
            "div(nuEff*dev(T(grad(U))))": "Gauss linear"
        },
        "laplacianSchemes": {"default": "Gauss linear limited 0.667"},
        "interpolationSchemes": {"default": "linear"},
        "snGradSchemes": {"default": "limited 0.667"},
        "fluxRequired": {"default": "no"},
        "wallDist": {"method": "meshWave"}
    },
    
    # fvSolution template
    "fvSolution": {
        "solvers": {
            "U": {
                "solver": "smoothSolver",
                "smoother": "GaussSeidel",
                "tolerance": 1e-08,
                "relTol": 0.1,
                "maxIter": 100
            },
            "p": {
                "solver": "GAMG", 
                "smoother": "GaussSeidel",
                "agglomerator": "faceAreaPair",
                "nCellsInCoarsestLevel": 10,
                "mergeLevels": 1,
                "cacheAgglomeration": True,
                "tolerance": 1e-07,
                "relTol": 0.01,
                "maxIter": 100
            }
        },
        "PIMPLE": {
            "nOuterCorrectors": 20,
            "nCorrectors": 1,
            "nNonOrthogonalCorrectors": 1,
            "pRefCell": 0,
            "pRefValue": 0
        }
    },

    # decomposeParDict template
    "decomposeParDict": {
        "method": "simple",
        "numberOfSubdomains": 1,

        "simpleCoeffs": {
            "n": "(1 1 1)",
            "delta": 0.001,
            "order": "xyz"
        },
        
        "hierarchicalCoeffs": {
            "n": "(1 1 1)", 
            "delta": 0.001,
            "order": "xyz"
        },
        
        "manualCoeffs": {
            "dataFile": "cellDecomposition"
        },
        
        "metisCoeffs": {
            "options": "",
            "processorWeights": "()"
        },
        
        "scotchCoeffs": {
            "processorWeights": "()",
            "strategy": "b",
            "writeGraph": "no"
        },
        
        "kahipCoeffs": {
            "config": "fast",
            "imbalance": 0.1,
            "useMetis": "no"
        },
        
        "structuredCoeffs": {
            "patches": "()",
            "domains": "()" 
        },
        
        "multiLevelCoeffs": {
            "level0": {
                "numberOfSubdomains": 1,
                "method": "scotch"
            }
        }       
    },
    
    # snappyHexMesh template
    "snappyHexMeshDict": {
    "castellatedMesh": True,
    "snap": True, 
    "addLayers": False,
    "geometry": {
        "PUT YOUR": "TODO GET GEOMETRY BASED ON STL"
    },
    "castellatedMeshControls": {
        "maxLocalCells": 10000000,
        "maxGlobalCells": 50000000,
        "minRefinementCells": 10,
        "maxLoadUnbalance": 0.1,
        "nCellsBetweenLevels": 5,
        "features": [],
        "refinementSurfaces": {},
        "resolveFeatureAngle": 25,
        "refinementRegions": {},
        "locationInMesh": [0, 0, 0],  # Will be set from STL analysis
        "allowFreeStandingZoneFaces": False
    },
    "snapControls": {
        "nSmoothPatch": 3,
        "tolerance": 2.0,
        "nSolveIter": 50,
        "nRelaxIter": 5,
        "nFeatureSnapIter": 10,
        "implicitFeatureSnap": False,
        "explicitFeatureSnap": True,
        "multiRegionFeatureSnap": False
    }
},
    "U": {
        "dimensions": "[0 2 -2 0 0 0 0]",
        "internalField": "uniform 0",
        "boundaryField": {
            "inlet": {
                "type": "fixedValue",
                "value": "uniform 0"
            },
            "outlet": {
                "type": "zeroGradient"
            },
            "walls": {
                "type": "zeroGradient"
            }
        }
   } 
}
# Headers for each file type
FILE_HEADERS = {
    "controlDict": {
        "version": 2.0,
        "format": "ascii",
        "class": "dictionary", 
        "object": "controlDict"
    },
    "fvSchemes": {
        "version": 2.0,
        "format": "ascii",
        "class": "dictionary",
        "object": "fvSchemes"
    },
    "fvSolution": {
        "version": 2.0, 
        "format": "ascii",
        "class": "dictionary",
        "object": "fvSolution"
    },
    "decomposeParDict": {
        "version": 2.0, 
        "format": "ascii",
        "class": "dictionary",
        "object": "decomposeParDict"
    },
    "snappyHexMeshDict": {
        "version": 2.0,
        "format": "ascii", 
        "class": "dictionary",
        "object": "snappyHexMeshDict"
    },
    "U": {
        "version": 2.0,
        "format": "ascii", 
        "class": "volVectorField",
        "object": "U" 
    },
    "p": {
        "version": 2.0,
        "format": "ascii", 
        "class": "volVectorField",
        "object": "p" 
    }
}
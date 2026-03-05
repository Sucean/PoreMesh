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
        "functions": {},
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
            "UFinal": {
                "$U": "",
                "tolerance": 1e-10,
                "relTol": 0
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
            },
            "pFinal": {
                "$p": "",
                "tolerance": 9.99e-10,
                "relTol": 0
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
    # surfaceFeatureExtract template
    "surfaceFeatureExtractDict": {
        "proto.stl": {
            "extractionMethod": "extractFromSurface",
            "includeAngle": 170,
            "subsetFeatures": {
                "nonManifoldEdges": "no",
                "openEdges": "no",
            },
            "writeObj": "yes"
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
        "maxLocalCells": 1000000,
        "maxGlobalCells": 5000000,
        "minRefinementCells": 10,
        "maxLoadUnbalance": 0.1,
        "nCellsBetweenLevels": 5,
        "features": {            
            "file": "",
            "level": 2
                    },
        "refinementSurfaces": {},
        "resolveFeatureAngle": 30,
        "refinementRegions": {},
        "locationInMesh": [0, 0, 0],  # Will be set from STL analysis
        "allowFreeStandingZoneFaces": True
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
        },
   "addLayersControls": {
        "relativeSizes": True,
        "expansionRatio": 1.0,
        "finalLayerThickness": 0.3,
        "minThickness": 0.1,
        "nGrow": 0,
        "featureAngle": 60,
        "slipFeatureAngle": 30,
        "nRelaxIter": 3,
        "nSmoothSurfaceNormals": 1,
        "nSmoothNormals": 3,
        "nSmoothThickness": 10,
        "maxFaceThicknessRatio": 0.5,
        "maxThicknessToMedialRatio": 0.3,
        "minMedialAxisAngle": 90,
        "nBufferCellsNoExtrude": 0,
        "nLayerIter": 50
    },      
    "meshQualityControls": {
        "maxNonOrtho": 75,
        "maxBoundarySkewness": 20,
        "maxInternalSkewness": 8,
        "maxConcave": 80,
        "minVol": 1e-18,
        "minTetQuality": 1e-15,
        "minArea": -1,
        "minTwist": 0.02,
        "minDeterminant": 0.001,
        "minFaceWeight": 0.02,
        "minVolRatio": 0.01,
        "minTriangleTwist": -1
        },
    "mergeTolerance": 1e-6
    },
    
    "U": {
        "dimensions": "[0 2 -2 0 0 0 0]",
        "internalField": "uniform (0 0 0)",
        "boundaryField": {
            "inlet": {
                "type": "fixedValue",
                "value": "uniform (0 0 1)"
            },
            "outlet": {
                "type": "fixedValue",
                "inletValue": "uniform (0 0 0)",
                "value": "uniform (0 0 0)"
            },
            "walls": {
                "type": "fixedValue",
                "value": "uniform 0"
            },
            "front|back|bottom|top": {
                "type": "fixedValue",
                "value": "uniform (0 0 0)"
            }
        }
    },
    "p": {
        "dimensions": "[0 2 -2 0 0 0 0]",
        "internalField": "uniform 0",
        "boundaryField": {
            "inlet": {
                "type": "fixedValue",
                "value": "uniform (0 0 1)"
            },
            "outlet": {
                "type": "fixedValue",
                "value": "uniform (0 0 0)"
            },
            "walls": {
                "type": "zeroGradient",
                "inletValue": "uniform (0 0 0)"
            },
            "front|back|bottoms|top": {
                "type": "zeroGradient",
                "inletValue": "uniform (0 0 0)"
            }
        }
   },
    "transportProperties": {
        "transportModel": "Newtonian",
        "nu nu": "[0 2 -1 0 0 0 0] 1e-6"
   },
    "turbulenceProperties": {
        "simulationType": "laminar",
   }, 
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
    "surfaceFeatureExtractDict": {
        "version": 2.0,
        "format": "ascii", 
        "class": "dictionary",
        "object": "surfaceFeatureExtractDict"
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
    },
    "transportProperties": {
        "version": 2.0,
        "format": "ascii", 
        "class": "volVectorField",
        "object": "U" 
    },
    "turbulenceProperties": {
        "version": 2.0,
        "format": "ascii", 
        "class": "volVectorField",
        "object": "p" 
    }
}
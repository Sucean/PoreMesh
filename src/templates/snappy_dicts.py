"""
Templates for snappyHexMeshDict and related files
"""

SNAPPY_HEX_MESH_TEMPLATE = {
    "castellatedMesh": True,
    "snap": True, 
    "addLayers": False,
    "geometry": {
        # This will be populated dynamically based on STL files
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
}

SNAPPY_HEADER = {
    "version": 2.0,
    "format": "ascii", 
    "class": "dictionary",
    "object": "snappyHexMeshDict"
}
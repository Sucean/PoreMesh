import numpy as np
import time
from stl import mesh
import src.mesh_auxillary as ma


class WalkingCubes:
    
    def __init__(self):
        # Initiate Look Up Table
        self.threshold = 127
        self.neighbors = [(2, 1, 1), (0, 1, 1), (1, 2, 1), (1, 0, 1), (1, 1, 2), (1, 1, 0)]
        self.lut = self._generate_lut()

    
    def _generate_lut(self):
    
        lut = {}
        bin = [0,1]
        
        for i in range (2**6):
            binary = f'{i:06b}'
            vec_list = []
            key = np.array([int(bit) for bit in binary])
            
            structure = ma.map_to_3d(key)
            
            for i, n in enumerate(self.neighbors):
                if not structure[n]:
                    vec_list.extend(ma.vert(i))
        
            if len(vec_list) > 0:
                data = np.zeros(len(vec_list), dtype=mesh.Mesh.dtype)
                data['vectors'] = vec_list
                lut[tuple(key)] = data
                
        return lut

    def generate_mesh_padded(self, array):

        if array.max() > 1:
            array = (array > self.threshold).astype(int)
        
        start_time = time.time()
        it = np.nditer(array[1:, 1:, 1:], flags=['multi_index'])
        mesh_list = []
        
        for x in it:
            
            idx = it.multi_index
            i,j,k = idx
            
            if array[i,j,k]:
                structure = array[i-1:i+2, j-1:j+2, k-1:k+2]
                
                if (bin_map := tuple(ma.map_to_binary(structure))) != (1, 1, 1, 1, 1, 1):
                    msh = self.lut[bin_map].copy()
                    translation = np.array([i + 0.5, j + 0.5, k + 0.5])
                    msh['vectors'] = msh['vectors'] + translation
                    mesh_list.append(msh)
                    
        data = np.concatenate(mesh_list)
        self.mesh = mesh.Mesh(data, remove_empty_areas = False)
    
    
    def generate_mesh(self, array):

        if array.max() > 1:
            array = (array > self.threshold).astype(int)
        
        start_time = time.time()
        it = np.nditer(array[1:, 1:, 1:], flags=['multi_index'])
        mesh_list = []
        
        for x in it:
            
            idx = it.multi_index
            i,j,k = idx
            
            if array[i,j,k]:
                structure = array[i-1:i+2, j-1:j+2, k-1:k+2]
                
                if (bin_map := tuple(ma.map_to_binary(structure))) != (1, 1, 1, 1, 1, 1):
                    msh = self.lut[bin_map].copy()
                    translation = np.array([i + 0.5, j + 0.5, k + 0.5])
                    msh['vectors'] = msh['vectors'] + translation
                    mesh_list.append(msh)
                    
        data = np.concatenate(mesh_list)
        self.mesh = mesh.Mesh(data, remove_empty_areas = False)
        
        print(f'\n[DEBUG] Finished {len(data)} triangles after {time.time()-start_time} seconds')
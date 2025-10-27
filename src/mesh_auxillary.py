from stl import mesh
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
import numpy as np

def show_mesh(data, autoscale = True, cl = 'blue', dpi=100):

    if isinstance(data, mesh.Mesh):
        the_mesh = data
    else:
        the_mesh = mesh.Mesh(data, remove_empty_areas=True)
    
    figure = plt.figure(dpi=dpi)
    axes = mplot3d.Axes3D(figure, auto_add_to_figure=False)
    figure.add_axes(axes)

    axes.add_collection3d(mplot3d.art3d.Poly3DCollection(the_mesh.vectors, alpha=0.25, facecolor=cl, edgecolor='black'))

    if autoscale:
        scale = the_mesh.points.flatten()
        axes.auto_scale_xyz(scale, scale, scale)
    
    axes.set_xlabel('$X$')
    axes.set_ylabel('$Y$')
    axes.set_zlabel('$Z$')
    
    plt.gca().invert_zaxis()
    
    plt.show()
    
    return()

def create_proto_voxel():
    
    proto_voxel = np.zeros(12, dtype=mesh.Mesh.dtype)

    proto_voxel['vectors'][0] = [[0,0,0],[1,0,0],[0,0,1]]
    proto_voxel['vectors'][1] = [[1,0,0],[0,0,1],[1,0,1]]
    proto_voxel['vectors'][2] = [[1,1,0],[1,1,1],[1,0,1]]
    proto_voxel['vectors'][3] = [[1,0,0],[1,1,0],[1,0,1]]
    proto_voxel['vectors'][4] = [[0,0,1],[0,1,1],[0,1,0]]
    proto_voxel['vectors'][5] = [[0,0,1],[0,0,0],[0,1,0]]
    proto_voxel['vectors'][6] = [[0,1,0],[1,1,0],[0,1,1]]
    proto_voxel['vectors'][7] = [[1,1,0],[0,1,1],[1,1,1]]
    proto_voxel['vectors'][8] = [[0,1,0],[1,0,0],[0,0,0]]
    proto_voxel['vectors'][9] = [[0,1,0],[1,1,0],[1,0,0]]
    proto_voxel['vectors'][10] = [[0,1,1],[1,0,1],[0,0,1]]
    proto_voxel['vectors'][11] = [[0,1,1],[1,1,1],[1,0,1]]

    return proto_voxel

def create_proto_face():
    
    proto_voxel = np.zeros(2, dtype=mesh.Mesh.dtype)

    proto_voxel['vectors'][0] = [[0,0,0],[1,0,0],[0,0,1]]
    proto_voxel['vectors'][1] = [[1,0,0],[0,0,1],[1,0,1]]

    return proto_voxel

def rotate_face(proto_face = create_proto_face(), axis = 'x', angle = 90):

    angle = np.radians(angle)
    
    # Define Rotation matrices in a dictionary
    rotation_matrices = {
        'x': np.array([[1, 0, 0], [0, np.cos(angle), -np.sin(angle)], [0, np.sin(angle), np.cos(angle)]]),
        'y': np.array([[np.cos(angle), 0, np.sin(angle)], [0, 1, 0], [-np.sin(angle), 0, np.cos(angle)]]),
        'z': np.array([[np.cos(angle), -np.sin(angle), 0], [np.sin(angle), np.cos(angle), 0], [0, 0, 1]])
    }

    # Apply Rotation matrices on all vectors in all faces given into the function
    for i in range(len(proto_face)):
        for j in range(3):
            proto_face['vectors'][i][j] = np.dot(rotation_matrices[axis], proto_face['vectors'][i][j])
    
    return proto_face

def map_to_3d(binary_array):
    # Define mapping between bit positions and voxel positions
    bit_to_voxel = {
        0: (0, 0, -1),  # Negative z-axis
        1: (0, 0, 1),   # Positive z-axis
        2: (0, -1, 0),  # Negative y-axis
        3: (0, 1, 0),   # Positive y-axis
        4: (-1, 0, 0),  # Negative x-axis
        5: (1, 0, 0)    # Positive x-axis
    }

    # Construct the 3D structure based on the binary array
    structure = np.zeros((3, 3, 3), dtype=int)
    for bit, voxel_pos in bit_to_voxel.items():
        structure[1 + voxel_pos[0], 1 + voxel_pos[1], 1 + voxel_pos[2]] = binary_array[bit]

    return structure

def map_to_binary(structure):
    # Define mapping between voxel positions and bit positions
    voxel_to_bit = {
        (0, 0, -1): 0,  # Negative z-axis
        (0, 0, 1): 1,   # Positive z-axis
        (0, -1, 0): 2,  # Negative y-axis
        (0, 1, 0): 3,   # Positive y-axis
        (-1, 0, 0): 4,  # Negative x-axis
        (1, 0, 0): 5    # Positive x-axis
    }

    # Convert the 3D structure to a binary array
    binary_array = np.zeros(6, dtype=int)
    for voxel_pos, bit in voxel_to_bit.items():
        binary_array[bit] = structure[1 + voxel_pos[0], 1 + voxel_pos[1], 1 + voxel_pos[2]]

    return binary_array

def vert(sector, proto_voxel=create_proto_voxel()):
    #print("Put vertice at " + str(n) + " in " + str(sector))

    if sector == 0:
        return proto_voxel['vectors'][2:4]  
    
    if sector == 1:
         return proto_voxel['vectors'][4:6]
   
    if sector == 2:
        return proto_voxel['vectors'][6:8]
    
    if sector == 3:
        return proto_voxel['vectors'][0:2]
        
    if sector == 4:
        return proto_voxel['vectors'][10:12]
        
    if sector == 5:
        return proto_voxel['vectors'][8:10]


def create_test_data(width=100, height=100, depth=20, num_clusters=20):
    """
    Generate a 3D numpy array with clusters of different shapes.

    Parameters:
        width (int): Width of the array.
        height (int): Height of the array.
        depth (int): Depth of the array.
        num_clusters (int): Number of clusters to generate.

    Returns:
        numpy.ndarray: 3D numpy array with clusters of different shapes.
    """
    # Create an empty array
    array_3d = np.zeros((height, width, depth), dtype=int)

    # Define shapes for clusters

    # Generate random clusters with different shapes
    for _ in range(num_clusters):
        shape = np.random.choice(15,3)
        x = np.random.randint(0, width - shape[0] + 1)
        y = np.random.randint(0, height - shape[1] + 1)
        z = np.random.randint(0, depth - shape[2] + 1)
        array_3d[y:y+shape[1], x:x+shape[0], z:z+shape[2]] = 1

    return array_3d

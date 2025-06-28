# import trimesh
# import numpy as np
# import scipy.io as sio
# import os
# import time

# # Directory containing your input STL files
# input_dir = r'D:\SIT\Blender_batch'
# # Directory to save the processed STL files
# output_dir = r'D:\SIT\MESH_mat_Data'

# # Make sure the output directory exists
# if not os.path.exists(output_dir):
#     os.makedirs(output_dir)

# # Set the target number of vertices
# target_vertex_count = 10000

# def find_stl_files(directory):
#     stl_files = []
#     for root, _, files in os.walk(directory):
#         for file in files:
#             if file.endswith('.stl'):
#                 stl_files.append(os.path.join(root, file))
#     return stl_files

# start_time = time.time()
# # Get list of all STL files
# stl_files = find_stl_files(input_dir) 
# # Loop through all STL files in the input directory
# for filepath in stl_files:
        
#         # Load the STL mesh
#         mesh = trimesh.load(filepath)

#         # Extract vertices and faces
#         vertices = np.array(mesh.vertices)
#         faces = np.array(mesh.faces)

#         # Get the current number of vertices
#         vertex_count = vertices.shape[0]

#         if vertex_count < target_vertex_count:
#             # If fewer than 10,000 vertices, we need to up-sample
#             additional_vertices_needed = target_vertex_count - vertex_count

#             # Randomly duplicate some existing vertices to match the target count
#             duplicate_indices = np.random.choice(vertex_count, size=additional_vertices_needed, replace=True)
#             new_vertices = np.concatenate([vertices, vertices[duplicate_indices]], axis=0)

#             vertices = new_vertices  # Updated vertices to have 10,000 points

#         elif vertex_count > target_vertex_count:
#             # If more than 10,000 vertices, we need to down-sample
#             indices = np.random.choice(vertex_count, size=target_vertex_count, replace=False)
#             vertices = vertices[indices]

#         # Verify the vertex count
#         print(f"Processed {filepath}: Final number of vertices: {vertices.shape[0]}")

#         # Create a new mesh with the updated vertices and original faces
#         new_mesh = trimesh.Trimesh(vertices=vertices, faces=faces)

#         # Export the resampled mesh as STL
#         output_stl_path = os.path.join(output_dir, f"resampled_{filepath}")
#         #new_mesh.export(output_stl_path)
        
#         # Prepare data to be saved in .mat format
#         mesh_data = {
#             'v': vertices,  # Vertices array
#             'f': faces      # Faces array (indices of the vertices forming the faces)
#         }

#         # Save the mesh data to a .mat file
#         output_mat_path = os.path.join(output_dir, f"resampled_{os.path.splitext(filepath)[0]}.mat")
#         sio.savemat(output_mat_path, mesh_data)

#         #print(f"Mesh saved to {output_mat_path} and {output_stl_path}")

# end_time = time.time()
# elapsed_time = end_time-start_time
# print(f"Batch processing complete! Time taken: {elapsed_time:.2f} seconds.")
# print("Batch processing complete!")


import trimesh
import numpy as np
import scipy.io as sio
import os
import time

# Directory containing your input STL files
input_dir = r'D:\SIT\Abalation\totalSeg_meshes'
# Directory to save the processed STL files
output_dir = r'D:\SIT\Abalation\totalSeg_meshes\npy'

# Ensure the output directory exists
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Target number of vertices
target_vertex_count = 10000

# Function to find all STL files, including in subdirectories
def find_stl_files(directory):
    stl_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.stl'):
                stl_files.append(os.path.join(root, file))
    return stl_files

start_time = time.time()

# Get list of STL files
stl_files = find_stl_files(input_dir)

# Loop through each STL file
for filepath in stl_files:
    # Load the STL mesh
    mesh = trimesh.load(filepath)
        # Extract vertices and faces
    vertices = np.array(mesh.vertices)
    faces = np.array(mesh.faces)

    # Get the current number of vertices
    vertex_count = vertices.shape[0]

    if vertex_count < target_vertex_count:
        # If fewer than 10,000 vertices, we need to up-sample
        additional_vertices_needed = target_vertex_count - vertex_count

        # Randomly duplicate some existing vertices to match the target count
        duplicate_indices = np.random.choice(vertex_count, size=additional_vertices_needed, replace=True)
        new_vertices = np.concatenate([vertices, vertices[duplicate_indices]], axis=0)

        vertices = new_vertices  # Updated vertices to have 10,000 points

    elif vertex_count > target_vertex_count:
        # If more than 10,000 vertices, we need to down-sample
        indices = np.random.choice(vertex_count, size=target_vertex_count, replace=False)
        vertices = vertices[indices]

    # Verify the vertex count
    print(f"Processed {filepath}: Final number of vertices: {vertices.shape[0]}")

    # Create a new mesh with the updated vertices and original faces
    #new_mesh = trimesh.Trimesh(vertices=vertices, faces=faces)

    # Extract the folder name and base filename
    folder_name = os.path.basename(os.path.dirname(filepath))  # Get the parent folder name
    base_name = os.path.basename(filepath).split('.')[0]       # Get the file name without extension

    # Generate unique output filenames
    #output_stl_path = os.path.join(output_dir, f"resampled_{base_name}_{folder_name}.stl")
    output_mat_path = os.path.join(output_dir, f"{folder_name}.npy")

    # Save the resampled mesh as STL
    #mesh.export(output_stl_path)
    # Prepare data to be saved in .mat format
    mesh_data = {
        'v': vertices  # Vertices array
        #'f': faces      # Faces array (indices of the vertices forming the faces)
    }
    sio.savemat(output_mat_path, mesh_data)


end_time = time.time()
elapsed_time = end_time - start_time
print(f"Batch processing complete! Time taken: {elapsed_time:.2f} seconds.")

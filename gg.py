import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
import numpy as np

# Function to get the corners of the cube given two diagonal points
def get_cube_corners(diagonal):
    x_min, y_min, z_min = diagonal[0]
    x_max, y_max, z_max = diagonal[1]
    
    corners = [
        [x_min, y_min, z_min], [x_max, y_min, z_min], [x_max, y_max, z_min], [x_min, y_max, z_min], # Bottom face
        [x_min, y_min, z_max], [x_max, y_min, z_max], [x_max, y_max, z_max], [x_min, y_max, z_max]  # Top face
    ]
    return np.array(corners)

# Function to create cube faces from corners
def get_faces(corners):
    faces = [
        [corners[0], corners[1], corners[2], corners[3]],  # Bottom face
        [corners[4], corners[5], corners[6], corners[7]],  # Top face
        [corners[0], corners[1], corners[5], corners[4]],  # Front face
        [corners[2], corners[3], corners[7], corners[6]],  # Back face
        [corners[0], corners[3], corners[7], corners[4]],  # Left face
        [corners[1], corners[2], corners[6], corners[5]]   # Right face
    ]
    return faces

# Function to create cube edges from corners
def get_edges(corners):
    edges = [
        [corners[0], corners[1]], [corners[1], corners[2]], [corners[2], corners[3]], [corners[3], corners[0]],  # Bottom edges
        [corners[4], corners[5]], [corners[5], corners[6]], [corners[6], corners[7]], [corners[7], corners[4]],  # Top edges
        [corners[0], corners[4]], [corners[1], corners[5]], [corners[2], corners[6]], [corners[3], corners[7]]   # Vertical edges
    ]
    return edges

# Function to plot the cube with filled faces and edges
def plot_cube_with_edges(diagonal, face_color='cyan', edge_color='black'):
    corners = get_cube_corners(diagonal)
    faces = get_faces(corners)
    edges = get_edges(corners)
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    # Plot cube faces with specified color
    ax.add_collection3d(Line3DCollection(faces, facecolors=face_color, linewidths=1, edgecolors='r', alpha=0.25))
    
    # Plot edges
    edge_lines = Line3DCollection(edges, colors=edge_color, linewidths=2)
    ax.add_collection3d(edge_lines)

    # Set axis limits
    ax.set_xlim([min(corners[:, 0]), max(corners[:, 0])])
    ax.set_ylim([min(corners[:, 1]), max(corners[:, 1])])
    ax.set_zlim([min(corners[:, 2]), max(corners[:, 2])])

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    plt.show()

# Example diagonal coordinates
diagonal_coords = [(1, 2, 3), (4, 5, 6)]
diagonal_coords1 = [(4, 5, 6), (7, 8, 9)]
# Plot cube with filled faces and edges
plot_cube_with_edges(diagonal_coords, face_color='blue', edge_color='red')
plot_cube_with_edges(diagonal_coords1, face_color='blue', edge_color='red')

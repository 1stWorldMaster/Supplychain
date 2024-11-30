import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import os

def plot_cube(ax, corner1, corner2):
    # Get all vertices of the cube
    vertices = np.array([
        [corner1[0], corner1[1], corner1[2]],
        [corner1[0], corner1[1], corner2[2]],
        [corner1[0], corner2[1], corner1[2]],
        [corner1[0], corner2[1], corner2[2]],
        [corner2[0], corner1[1], corner1[2]],
        [corner2[0], corner1[1], corner2[2]],
        [corner2[0], corner2[1], corner1[2]],
        [corner2[0], corner2[1], corner2[2]],
    ])

    # Define the six faces of the cube
    faces = [
        [vertices[j] for j in [0, 1, 3, 2]],  # Bottom face
        [vertices[j] for j in [4, 5, 7, 6]],  # Top face
        [vertices[j] for j in [0, 1, 5, 4]],  # Front face
        [vertices[j] for j in [2, 3, 7, 6]],  # Back face
        [vertices[j] for j in [0, 2, 6, 4]],  # Left face
        [vertices[j] for j in [1, 3, 7, 5]],  # Right face
    ]

    # Create a 3D polygon collection for the cube
    cube = Poly3DCollection(faces, alpha=0.4, edgecolor='k')
    ax.add_collection3d(cube)

def plot_all_cubes(csv_file):
    # Read CSV
    data = pd.read_csv(csv_file)

    # Extract corners
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_box_aspect([1, 1, 1])  # Equal aspect ratio

    all_points = []
    for idx,row in data.iterrows():
        corner1 = row[['x1', 'y1', 'z1']].values
        corner2 = row[['x2', 'y2', 'z2']].values
        plot_cube(ax, corner1, corner2)
        all_points.extend([corner1, corner2])
        
        ax.view_init(elev=30, azim=30)  # Adjust these values to set the view angle
        plt.savefig(f'frames/cube_plot{idx+1}.png', dpi=300, bbox_inches='tight')
        print(f'saving image {idx}')

    # Set axis limits
    all_points = np.array(all_points)
    ax.set_xlim([all_points[:, 0].min(), all_points[:, 0].max()])
    ax.set_ylim([all_points[:, 1].min(), all_points[:, 1].max()])
    ax.set_zlim([all_points[:, 2].min(), all_points[:, 2].max()])

    # Save the figure
    plt.savefig(f'frames/cube_plot{idx+1}.png', dpi=300, bbox_inches='tight')

    # Adjust view for better 3D perspective
    ax.view_init(elev=30, azim=30)  # Adjust these values to set the view angle

    # Save the figure
    plt.savefig('cube_plot.png', dpi=300, bbox_inches='tight')

    # plt.show()

# for i in range (1,5):
# Example CSV file path
os.mkdir('frames')
# csv_file = f"output{i}.csv"
csv_file=f"output1.csv"
plot_all_cubes(csv_file)

        
os.system('ffmpeg -framerate 1 -i frames/cube_plot%d.png -c:v libx264 -pix_fmt yuv420p simulation.mp4')
import shutil
shutil.rmtree('frames')

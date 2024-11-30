import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.widgets import Button

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

def plot_all_cubes_with_rotation(csv_file):
    # Read CSV
    data = pd.read_csv(csv_file)

    # Prepare the plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_box_aspect([1, 1, 1])  # Equal aspect ratio

    all_points = []
    for _, row in data.iterrows():
        corner1 = row[['x1', 'y1', 'z1']].values
        corner2 = row[['x2', 'y2', 'z2']].values
        plot_cube(ax, corner1, corner2)
        all_points.extend([corner1, corner2])

    # Set axis limits
    all_points = np.array(all_points)
    ax.set_xlim([all_points[:, 0].min(), all_points[:, 0].max()])
    ax.set_ylim([all_points[:, 1].min(), all_points[:, 1].max()])
    ax.set_zlim([all_points[:, 2].min(), all_points[:, 2].max()])

    # Set initial view angle
    ax.view_init(elev=20, azim=30)

    # Define the rotation functions
    def rotate_left(event):
        azim = ax.azim - 10
        ax.view_init(elev=ax.elev, azim=azim)
        plt.draw()

    def rotate_right(event):
        azim = ax.azim + 10
        ax.view_init(elev=ax.elev, azim=azim)
        plt.draw()

    def rotate_up(event):
        elev = ax.elev + 10
        ax.view_init(elev=elev, azim=ax.azim)
        plt.draw()

    def rotate_down(event):
        elev = ax.elev - 10
        ax.view_init(elev=elev, azim=ax.azim)
        plt.draw()

    # Create buttons for rotation controls
    ax_rotate_left = plt.axes([0.7, 0.01, 0.1, 0.075])
    button_left = Button(ax_rotate_left, 'Left')
    button_left.on_clicked(rotate_left)

    ax_rotate_right = plt.axes([0.81, 0.01, 0.1, 0.075])
    button_right = Button(ax_rotate_right, 'Right')
    button_right.on_clicked(rotate_right)

    ax_rotate_up = plt.axes([0.7, 0.08, 0.1, 0.075])
    button_up = Button(ax_rotate_up, 'Up')
    button_up.on_clicked(rotate_up)

    ax_rotate_down = plt.axes([0.81, 0.08, 0.1, 0.075])
    button_down = Button(ax_rotate_down, 'Down')
    button_down.on_clicked(rotate_down)

    plt.show()

# Example CSV file path
csv_file = "output.csv"

plot_all_cubes_with_rotation(csv_file)

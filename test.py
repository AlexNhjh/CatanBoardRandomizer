import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.image as mpimg
import math
import matplotlib.transforms as transforms

# Set up the figure and axis
fig, ax = plt.subplots()

# Coordinates of the hex center
x, y = 0, 0
hex_radius = 1.0

# Load the image
img = mpimg.imread('wood.png')  # Make sure this file exists in your working directory!

rotation_deg = 30
transform = transforms.Affine2D().rotate_deg_around(x, y, rotation_deg) + ax.transData

# Show the image in the background (same size as hex)
im = ax.imshow(
    img,
    extent=[x - hex_radius, x + hex_radius, y - hex_radius, y + hex_radius],
    zorder=0,
    transform=transform
)

# Create the hexagon patch
hex = patches.RegularPolygon(
    (x, y),
    numVertices=6,
    radius=hex_radius,
    orientation=math.radians(0),
    edgecolor='navajowhite',
    linewidth=4,
    facecolor='none',
    transform=ax.transData
)

# Clip the image to the hex shape
im.set_clip_path(hex)

# Add the hexagon patch to the axes
ax.add_patch(hex)

# Display settings
ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)
ax.set_aspect('equal')
ax.axis('off')  # Hide axes

plt.show()


from build123d import *
from ocp_vscode import *

# Dimensions of the key tag (converted to mm)
width = 15.0      # 1 cm
length = 50.0    # 7 cm
thickness = 2.0  # 2 mm
corner_radius = 3.0  # radius for rounded corners
hole_radius = 2.0    # radius for keyring hole
hole_offset = 6.0    # offset from the top edge for the keyring hole

with BuildPart() as key_tag:
    # 1. Create the main body block
    Box(
        width, 
        length, 
        thickness, 
        align=(Align.CENTER, Align.CENTER, Align.MIN)
    )
    
    # 2. Fillet the vertical edges to round the corners
    fillet(key_tag.edges().filter_by(Axis.Z), radius=corner_radius)
    
    # 3. Add a hole for the keyring on one end
    # Center of tag is at (0, 0), so the top edge is at Y = length / 2
    with BuildSketch(key_tag.faces().sort_by(Axis.Z)[-1]) as hole_sketch:
        with Locations((0, (length / 2) - hole_offset)):
            Circle(radius=hole_radius)
    extrude(amount=-thickness, mode=Mode.SUBTRACT)

# Display the key tag in OCP Viewer
show(key_tag)

# Export the key tag to STL
export_stl(key_tag.part, "key_tag.stl")

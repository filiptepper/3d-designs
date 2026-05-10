from build123d import *
from ocp_vscode import *

# Dimensions of the device (Darkglass anagram)
device_w = 210.0
device_l = 100.0
device_h = 46.0

# Printing parameters
clearance = 0.5  # Extra space around the device
wall = 2.0       # Thickness of the cover walls
r = 5.0          # Corner radius

# Inner dimensions (the void)
inner_w = device_w + 2 * clearance
inner_l = device_l + 2 * clearance
inner_h = device_h + clearance

# Outer dimensions
outer_w = inner_w + 2 * wall
outer_l = inner_l + 2 * wall

# Create the cover using build123d
# BuildPart is the main context for creating 3D solids
with BuildPart() as cover:
    # 1. Create the main body (outer dimensions)
    # Box creates a cuboid; align=(..., ..., Align.MIN) ensures it starts at Z=0
    Box(
        outer_w, 
        outer_l, 
        inner_h + wall, 
        align=(Align.CENTER, Align.CENTER, Align.MIN)
    )
    
    # 2. Fillet the vertical edges
    # We select edges parallel to the Z axis to round the corners
    fillet(cover.edges().filter_by(Axis.Z), radius=r)
    
    # 3. Hollow out the part (Shelling)
    # offset() with a negative amount hollows the part inwards
    # openings removes the specified face (the bottom face in this case)
    offset(
        amount=-wall, 
        openings=cover.faces().sort_by(Axis.Z)[0]
    )

    # 4. Add a top cutout for a screen
    # ... (existing cutout code)
    hole_w = inner_w - 17 - 17
    hole_l = inner_l - 30 - 32
    hole_y_offset = (32 - 30) / 2
    
    with BuildSketch(cover.faces().sort_by(Axis.Z)[-1]) as screen_cutout:
        with Locations((0, hole_y_offset)):
            Rectangle(hole_w, hole_l)
    extrude(amount=-wall, mode=Mode.SUBTRACT)

    # 5. Add 6 circular holes for knobs/buttons
    # Diameter 17mm, 34mm from left/right inner edges, 15mm from top inner edge
    hole_dia = 17.0
    # X range: from 34mm from left to 34mm from right
    x_first = -inner_w / 2 + 34
    x_last = inner_w / 2 - 34
    # Y position: 15mm from the top (back) inner edge
    y_knobs = inner_l / 2 - 15
    
    # Generate 6 equally spaced locations along the X axis
    knob_locs = [
        (x_first + i * (x_last - x_first) / 5, y_knobs) 
        for i in range(6)
    ]
    
    with BuildSketch(cover.faces().sort_by(Axis.Z)[-1]) as knob_cutouts:
        with Locations(knob_locs):
            Circle(radius=hole_dia / 2)
    extrude(amount=-wall, mode=Mode.SUBTRACT)

    # 6. Add 3 more circular holes (second row)
    # Diameter 18mm, 32mm from left/right inner edges, 15mm from top inner edge
    y_row2 = inner_l / 2 - 80
    # Generate 3 equally spaced locations along the X axis
    row2_locs = [
        (x_first + i * (x_last - x_first) / 2, y_row2) 
        for i in range(3)
    ]
    
    with BuildSketch(cover.faces().sort_by(Axis.Z)[-1]) as row2_cutouts:
        with Locations(row2_locs):
            Circle(radius=hole_dia / 2)
    extrude(amount=-wall, mode=Mode.SUBTRACT)

    # 7. Add 3 smaller holes (8mm) under the second row
    # Diameter 8mm, centered over the second row holes (same X)
    # Placed 24mm from the top inner edge to fit between row 2 and the screen
    hole_dia_small = 7.0
    y_row3 = inner_l / 2 - 94
    row3_locs = [(loc[0], y_row3) for loc in row2_locs]
    
    with BuildSketch(cover.faces().sort_by(Axis.Z)[-1]) as row3_cutouts:
        with Locations(row3_locs):
            Circle(radius=hole_dia_small / 2)
            
    extrude(amount=-wall, mode=Mode.SUBTRACT)

# Display the result in the OCP Viewer
show(cover)

# Export the part to STL for 3D printing
# export_stl(cover.part, "darkglass-anagram-cover-v2.stl")
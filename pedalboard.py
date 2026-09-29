"""
Parametric 3D Printable Pedalboard for M-VAVE Chocolate Plus & Darkglass Anagram
with integrated Baseus GaN3 Pro 65W Desktop Charger bay and cable routing channels.

Features:
- Lower Tier: M-VAVE Chocolate Plus pocket (214 x 38 mm) with 6mm front retaining lip.
- Cable Trough: 22mm deep drop-down channel behind Chocolate for right-angle / straight TRS and USB-C plugs.
- Upper Tier: Universal-fit Darkglass Anagram tray (213.5 x 102.5 mm) raised at a 13° ergonomic tilt.
  Accommodates the Darkglass Anagram both bare and with the 3D-printed protective cover.
- Under-Deck Charger Bay: Custom slide-in sleeve on the left side tailored for Baseus GaN3 Pro 65W
  (40 x 36.9 x 70 mm), with AC cord pass-through, side cable notch, and finger push-out hole.
- Central Cable Cavity: Concealed routing under the Anagram deck with cable-tie anchor bridges.
- Rear I/O Cutouts: Three generous scalloped pass-throughs for USB-C PD, MIDI TRS, and audio jacks.
- Bottom Base: 6 recessed mounting pads for non-slip rubber bumper feet (12mm dia).

Designed with build123d.
"""

import math
from build123d import *
from ocp_vscode import *


# ==========================================
# 1. PARAMETRIC SPECIFICATIONS & DIMENSIONS
# ==========================================

# M-VAVE Chocolate Plus
choc_w = 212.0
choc_d = 36.0
choc_h = 17.0
choc_clearance_w = 2.0         # 1.0mm per side -> 214.0mm
choc_clearance_d = 2.0         # 1.0mm front/back -> 38.0mm
pocket_choc_w = choc_w + choc_clearance_w
pocket_choc_d = choc_d + choc_clearance_d
pocket_choc_floor_z = 4.0      # Sturdy 4mm solid floor beneath Chocolate

# Cable Trough between Chocolate and Anagram
trough_d = 22.0                # 22mm clearance for 1/4" TRS jacks & USB-C plugs

# Darkglass Anagram (Universal fit: bare 210x100mm, with Cover v2 212x102mm)
pocket_anagram_w = 213.5       # Fits cover (+0.75mm clearance) or bare (+1.75mm clearance)
pocket_anagram_d = 102.5       # Fits cover (+0.5mm clearance) or bare (+2.5mm clearance)
anagram_tilt_deg = 13.0        # Optimal angle for stage visibility and footswitch stomp
anagram_tilt_rad = math.radians(anagram_tilt_deg)

# Baseus GaN3 Pro 65W Desktop Charger (70L x 40W x 36.9H mm)
charger_len = 70.0
charger_w = 40.0
charger_h = 36.9
charger_pocket_len = 72.0      # 2mm clearance along insertion axis
charger_pocket_w = 42.0        # 2mm clearance width
charger_pocket_h = 38.5        # 1.6mm clearance height
charger_y_start = 80.0
charger_y_end = charger_y_start + charger_pocket_w  # 122.0 mm
charger_y_mid = (charger_y_start + charger_y_end) / 2.0

# Wall & Structural Thicknesses
wall_side = 5.0
wall_front = 4.0
wall_rear = 5.0
lip_h = 6.0                    # Retaining lip height for both tiers
deck_front_z = 42.0            # Front deck height (clears 38.5mm charger under-deck)
deck_thickness = 3.2           # Rigid structural deck thickness
floor_z = 2.5                  # Bottom floor thickness
corner_r = 7.0                 # Outer vertical corner radius (matching Darkglass aesthetic)

# Derived Y Coordinates
y_choc_start = wall_front                          # 4.0 mm
y_choc_end = y_choc_start + pocket_choc_d          # 42.0 mm
y_trough_end = y_choc_end + trough_d               # 64.0 mm
y_lip_anagram_end = y_trough_end + 3.5             # 67.5 mm (front lip thickness 3.5mm)
anagram_dx = pocket_anagram_d * math.cos(anagram_tilt_rad)  # ~99.87 mm
y_anagram_end = y_lip_anagram_end + anagram_dx     # 167.37 mm
total_d = y_anagram_end + wall_rear                # 172.37 mm
total_w = pocket_choc_w + 2 * wall_side            # 224.0 mm

# Derived Z Heights
z_front = pocket_choc_floor_z + lip_h              # 10.0 mm
z_anagram_lip_front = deck_front_z + lip_h         # 48.0 mm
deck_rear_z = deck_front_z + pocket_anagram_d * math.sin(anagram_tilt_rad)  # ~65.06 mm
z_rear = deck_rear_z + lip_h                       # 71.06 mm


# ==========================================
# 2. SOLID MODEL GENERATION
# ==========================================

print("Generating Parametric Pedalboard...")
print(f"Overall Dimensions: Width={total_w:.1f}mm, Depth={total_d:.1f}mm, Max Height={z_rear:.1f}mm")

with BuildPart() as pedalboard:
    # ----------------------------------------------------
    # Step 1: Base Wedge Hull
    # ----------------------------------------------------
    hull_pts = [
        (0.0, 0.0),
        (total_d, 0.0),
        (total_d, z_rear),
        (y_anagram_end, z_rear),
        (y_lip_anagram_end, z_anagram_lip_front),
        (y_trough_end, z_anagram_lip_front),
        (y_choc_end, z_front),
        (0.0, z_front),
    ]
    with BuildSketch(Plane.YZ) as s_hull:
        Polygon(hull_pts)
    extrude(amount=total_w / 2.0, both=True)

    # Fillet vertical corners (radius 7mm)
    fillet(pedalboard.edges().filter_by(Axis.Z), radius=corner_r)

    # ----------------------------------------------------
    # Step 2: M-VAVE Chocolate Plus Pocket
    # ----------------------------------------------------
    with Locations((0.0, y_choc_start, pocket_choc_floor_z)):
        Box(
            pocket_choc_w,
            pocket_choc_d,
            25.0,
            align=(Align.CENTER, Align.MIN, Align.MIN),
            mode=Mode.SUBTRACT,
        )

    # ----------------------------------------------------
    # Step 3: Cable Trough behind Chocolate
    # ----------------------------------------------------
    with Locations((0.0, y_choc_end, pocket_choc_floor_z)):
        Box(
            pocket_choc_w,
            trough_d,
            55.0,
            align=(Align.CENTER, Align.MIN, Align.MIN),
            mode=Mode.SUBTRACT,
        )

    # ----------------------------------------------------
    # Step 4: Darkglass Anagram Angled Tray
    # ----------------------------------------------------
    tray_plane = Plane(
        origin=(0.0, y_lip_anagram_end, deck_front_z),
        x_dir=(1.0, 0.0, 0.0),
        z_dir=(0.0, -math.sin(anagram_tilt_rad), math.cos(anagram_tilt_rad)),
    )
    with Locations(tray_plane):
        Box(
            pocket_anagram_w,
            pocket_anagram_d,
            60.0,
            align=(Align.CENTER, Align.MIN, Align.MIN),
            mode=Mode.SUBTRACT,
        )

    # ----------------------------------------------------
    # Step 5: Baseus GaN3 Pro 65W Slide-in Charger Bay
    # ----------------------------------------------------
    # Slides in from left wall (X = -total_w/2 = -112.0mm) to X = -40.0mm
    with Locations((-total_w / 2.0 + charger_pocket_len / 2.0, charger_y_mid, floor_z)):
        Box(
            charger_pocket_len + 1.0,
            charger_pocket_w,
            48.0,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
            mode=Mode.SUBTRACT,
        )

    # ----------------------------------------------------
    # Step 6: Central Cable Management Cavity
    # ----------------------------------------------------
    # Spans from partition wall (X = -37.0) to right wall (X = +107.0)
    central_cav_pts = [
        (y_lip_anagram_end, floor_z),
        (y_anagram_end, floor_z),
        (y_anagram_end, deck_rear_z - deck_thickness),
        (y_lip_anagram_end, deck_front_z - deck_thickness),
    ]
    with BuildSketch(Plane.YZ.offset((-37.0 + 107.0) / 2.0)) as s_central:
        Polygon(central_cav_pts)
    extrude(amount=(107.0 - (-37.0)) / 2.0, both=True, mode=Mode.SUBTRACT)

    # ----------------------------------------------------
    # Step 7: Front & Rear Corner Cavities (Around Charger Bay)
    # ----------------------------------------------------
    # Front-left cavity (in front of charger sleeve)
    front_cav_pts = [
        (y_lip_anagram_end, floor_z),
        (charger_y_start - 3.0, floor_z),
        (
            charger_y_start - 3.0,
            deck_front_z
            + (charger_y_start - 3.0 - y_lip_anagram_end) * math.tan(anagram_tilt_rad)
            - deck_thickness,
        ),
        (y_lip_anagram_end, deck_front_z - deck_thickness),
    ]
    with BuildSketch(Plane.YZ.offset((-107.0 + -37.0) / 2.0)) as s_front_cav:
        Polygon(front_cav_pts)
    extrude(amount=(107.0 - 37.0) / 2.0, both=True, mode=Mode.SUBTRACT)

    # Rear-left cavity (behind charger sleeve)
    rear_cav_pts = [
        (charger_y_end + 3.0, floor_z),
        (y_anagram_end, floor_z),
        (y_anagram_end, deck_rear_z - deck_thickness),
        (
            charger_y_end + 3.0,
            deck_front_z
            + (charger_y_end + 3.0 - y_lip_anagram_end) * math.tan(anagram_tilt_rad)
            - deck_thickness,
        ),
    ]
    with BuildSketch(Plane.YZ.offset((-107.0 + -37.0) / 2.0)) as s_rear_cav:
        Polygon(rear_cav_pts)
    extrude(amount=(107.0 - 37.0) / 2.0, both=True, mode=Mode.SUBTRACT)

    # ----------------------------------------------------
    # Step 8: AC Power Cord Pass-Through in Partition Wall
    # ----------------------------------------------------
    # Connects charger bay to central cavity through partition wall at X = -38.5mm
    with Locations((-38.5, charger_y_mid, floor_z)):
        Box(
            8.0,
            22.0,
            24.0,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
            mode=Mode.SUBTRACT,
        )

    # ----------------------------------------------------
    # Step 9: Side Cable Routing Notch (Left Wall)
    # ----------------------------------------------------
    # Allows USB cables plugged into Baseus side ports to route cleanly into cable trough
    with Locations((-total_w / 2.0, 54.0, pocket_choc_floor_z)):
        Box(
            12.0,
            14.0,
            18.0,
            align=(Align.MIN, Align.CENTER, Align.MIN),
            mode=Mode.SUBTRACT,
        )

    # ----------------------------------------------------
    # Step 10: Cable Trough Drop Slots
    # ----------------------------------------------------
    # 3 slots in the trough floor for Chocolate USB-C & TRS cables to drop into lower cavity
    with Locations((-60.0, 53.0, 0.0), (0.0, 53.0, 0.0), (60.0, 53.0, 0.0)):
        Box(
            26.0,
            12.0,
            10.0,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
            mode=Mode.SUBTRACT,
        )

    # ----------------------------------------------------
    # Step 11: Rear Deck Cable Pass-Throughs (Darkglass I/O)
    # ----------------------------------------------------
    # 3 scalloped openings along the rear edge for USB-C PD power, TRS MIDI, and audio jacks
    with Locations(
        (-65.0, y_anagram_end, deck_rear_z - 8.0),
        (0.0, y_anagram_end, deck_rear_z - 8.0),
        (65.0, y_anagram_end, deck_rear_z - 8.0),
    ):
        Box(
            36.0,
            16.0,
            30.0,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
            mode=Mode.SUBTRACT,
        )

    # ----------------------------------------------------
    # Step 12: Rear AC Power Cord Exit Notch
    # ----------------------------------------------------
    with Locations((-15.0, total_d, floor_z + 6.0)):
        Cylinder(
            radius=6.0,
            height=15.0,
            rotation=(90.0, 0.0, 0.0),
            mode=Mode.SUBTRACT,
        )

    # ----------------------------------------------------
    # Step 13: Push-Out Finger Hole (Under Charger)
    # ----------------------------------------------------
    with Locations((-total_w / 2.0 + 35.0, charger_y_mid, 0.0)):
        Cylinder(radius=10.0, height=10.0, mode=Mode.SUBTRACT)

    # ----------------------------------------------------
    # Step 14: Integrated Cable Tie Anchor Bridges
    # ----------------------------------------------------
    # Twin slot pairs on the central floor for zip-ties or velcro cable straps
    tie_locs = [
        (10.0, 105.0, 0.0),
        (10.0, 115.0, 0.0),
        (55.0, 105.0, 0.0),
        (55.0, 115.0, 0.0),
    ]
    with Locations(tie_locs):
        Box(
            15.0,
            3.5,
            10.0,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
            mode=Mode.SUBTRACT,
        )

    # ----------------------------------------------------
    # Step 15: Recessed Rubber Foot Mounting Pads (Bottom Z=0)
    # ----------------------------------------------------
    foot_locs = [
        (-95.0, 16.0, 0.0),
        (95.0, 16.0, 0.0),
        (-95.0, 95.0, 0.0),
        (95.0, 95.0, 0.0),
        (-95.0, 158.0, 0.0),
        (95.0, 158.0, 0.0),
    ]
    with Locations(foot_locs):
        Cylinder(
            radius=6.0,
            height=1.5,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
            mode=Mode.SUBTRACT,
        )


# ==========================================
# 3. VERIFICATION & EXPORT
# ==========================================

print("Model Generation Complete!")
print(f"Part Valid: {pedalboard.part.is_valid}")
print(f"Part Volume: {pedalboard.part.volume:.1f} mm³")
print(f"Estimated PLA Weight (1.24 g/cm³): {pedalboard.part.volume / 1000.0 * 1.24:.1f} g")

# Export high-quality STL for 3D printing
stl_filename = "chocolate-darkglass-pedalboard.stl"
export_stl(pedalboard.part, stl_filename)
print(f"Exported STL to '{stl_filename}'")

# Display in VS Code OCP CAD Viewer if active
viewer_port = None
for p in range(3939, 3946):
    if port_check(p):
        viewer_port = p
        break

if viewer_port is not None:
    set_port(viewer_port)
    show(pedalboard)
    print(f"Rendered in OCP CAD Viewer on port {viewer_port}!")
else:
    print("\n[!] OCP CAD Viewer panel is not currently open in the editor.")
    print("    To open it in Antigravity IDE / VS Code:")
    print("    1. Press Ctrl+Shift+P (or F1) and type: 'OCP CAD Viewer: Open viewer'")
    print("       (or click the OCP CAD Viewer icon in the left Activity Bar and click 'Open viewer').")
    print("    2. Once the viewer tab opens, re-run this script to display the model interactively!\n")

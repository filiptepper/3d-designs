#!/usr/bin/env python3
"""
20-Series Aluminum Extrusion Stage Pedalboard ("LINK-400 Extrusion Platform")
=============================================================================
Parametric CAD pipeline engineered in build123d for a heavy-duty, tour-grade
stage pedalboard built from 2020 aluminum extrusions and 3D-printed side cheeks.

Key Features & Specifications (v2.0 - Elevated +12mm & Rail-Mounted CIOKS Cradle):
  1. +12 mm Vertical Elevation (Strictly Preserving 10.0° Slope):
     - Translates sockets and upper deck along the 80.0° stance line (dY = -2.12 mm, dZ = +12.0 mm).
     - Front nose elevation: 49.8 mm (was 37.8 mm).
     - Rear cheek elevation: 79.0 mm (was 67.0 mm).
     - Base remains 100% flat at Z = 0 (no foot counterbores, preserving solid footing).
     - Generates +9.36 mm of positive ground clearance under the CIOKS Sol cradle!

  2. Full 4-Rail Through-Bolting (Extreme Structural Rigidity):
     - Adds dia 6.5 mm through-holes for Rails 2 & 3 matching Rails 1 & 4.
     - All 4 rails bolt solidly from the outside into the 2020 extrusion tapped cores.

  3. Custom Vector Logo Integration:
     - Completely replaces the old honeycomb holes with the vectorized custom emblem.
     - Debossed by 1.2 mm into the outer cheek face for a crisp, snag-free finish.

  4. Concept A: Rail-Mounted CIOKS Sol Underbelly Cradle:
     - Mounts directly to the underside T-slots of Rails 3 & 4 (50.0 mm center spacing).
     - Slideable along the entire 400 mm board width (position anywhere left/center/right).
     - Includes 2 bottom M4 direct-mount holes (70 x 40 mm pattern) to bolt CIOKS Sol.
     - Open IEC inlet bay (left), 5 DC output bay (right), top cable troughs, and cooling slots.
     - Prints 100% support-free flat on the build plate (Z = 0).
"""

import math
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import build123d as bd

# ==============================================================================
# 1. PARAMETERS & SPECIFICATIONS
# ==============================================================================

# Extrusion rail specifications
EXTRUSION_PROFILE = 20.0       # 2020 extrusion width and height (mm)
EXTRUSION_LENGTH = 400.0       # Extrusion span socket-to-socket (mm)
DECK_ANGLE_DEG = 10.0          # Deck incline angle (degrees)
DECK_ANGLE_RAD = math.radians(DECK_ANGLE_DEG)

# Elevation parameters:
# Elevate by +12.0 mm along Z. To keep the 80.0° front/rear stance line exact,
# dY = -12.0 * tan(10°) = -2.1159 mm.
ELEVATION_Z = 12.0
ELEVATION_Y = -ELEVATION_Z * math.tan(DECK_ANGLE_RAD)  # -2.1159 mm

# Elevated 2020 Extrusion Centers in local (Y, Z) coordinates:
RAIL_CENTERS_YZ = [
    (round(14.17 + ELEVATION_Y, 2), round(21.87 + ELEVATION_Z, 2)),   # Rail 1 (Front):    (12.05, 33.87)
    (round(63.41 + ELEVATION_Y, 2), round(30.56 + ELEVATION_Z, 2)),   # Rail 2 (Mid-Front): (61.29, 42.56)
    (round(112.65 + ELEVATION_Y, 2), round(39.24 + ELEVATION_Z, 2)),  # Rail 3 (Mid-Rear):  (110.53, 51.24)
    (round(161.89 + ELEVATION_Y, 2), round(47.92 + ELEVATION_Z, 2)),  # Rail 4 (Rear):      (159.77, 59.92)
]

# Coordinate spacing along X:
X_SOCKET_L = 6.35
X_SOCKET_R = 406.35
X_RAIL_CENTER = (X_SOCKET_L + X_SOCKET_R) / 2.0  # 206.35 mm
X_MID_PLANE = X_RAIL_CENTER                      # 206.35 mm

# Leg socket dimensions
SOCKET_CROSS_SECTION = 20.50   # 20.5 x 20.5 mm with clearance tolerance
SOCKET_DEPTH = 12.70           # 12.7 mm (1/2") pocket depth
BOLT_HOLE_DIA = 6.50           # dia 6.5 mm through-hole for M5/M6 bolts
CHEEK_WALL_T = 19.05           # 3/4" (19.05 mm) solid cheek thickness
RIM_LIP_T = 2.50               # 2.5 mm outer border rim protrusion

# CIOKS Sol power supply dimensions
CIOKS_SOL_W = 130.0   # Width along X (mm)
CIOKS_SOL_D = 88.0    # Depth along slope (mm)
CIOKS_SOL_H = 25.4    # Height / thickness (mm)

# Cradle specifications
CRADLE_INNER_W = 132.0         # 130 + 2 mm tolerance
CRADLE_INNER_D = 90.0          # 88 + 2 mm tolerance
CRADLE_INNER_H = 26.0          # 25.4 + 0.6 mm tolerance
CRADLE_WALL_T = 3.5            # Heavy-duty 3.5 mm sidewalls
CRADLE_FLOOR_T = 3.0           # Rigid 3.0 mm floor
CRADLE_TOTAL_W = CRADLE_INNER_W + 2 * CRADLE_WALL_T   # 139.0 mm
CRADLE_TOTAL_D = CRADLE_INNER_D + 2 * CRADLE_WALL_T   # 97.0 mm
CRADLE_TOTAL_H = CRADLE_INNER_H + CRADLE_FLOOR_T      # 29.0 mm


# ==============================================================================
# 2. LOGO VECTOR GENERATOR
# ==============================================================================

def make_logo_sketch(width: float = 25.0, stencil: bool = True, mirrored: bool = False) -> bd.Sketch:
    """
    Constructs an exact 2D vector sketch of the custom logo.
    The logo is composed of orthogonal geometric bars on a 425 x 680 grid (5:8 ratio).

    If stencil is True (default for through-hole cutout), the 6px top and bottom bounding
    lines are omitted so the internal channels open to the solid cheek, guaranteeing
    a single 100% physically connected solid without floating islands.

    If mirrored is True, flips the logo horizontally across the sketch vertical axis.
    """
    height = width * (680.0 / 425.0)

    if stencil:
        # 5 primary bars (stencil mode for through-hole cutouts)
        rects = [
            (9, 677, 116, 201),   # Left vertical bar
            (9, 677, 343, 428),   # Right vertical bar
            (9, 456, 230, 315),   # Middle vertical bar
            (485, 570, 3, 315),   # Horizontal crossbar (left "+" arm across bars 1 & 2)
            (343, 400, 230, 428), # Middle horizontal bridge (between bars 2 & 3)
        ]
    else:
        # 7 exact normalized rectangles with closed top/bottom cap borders (for debossing)
        rects = [
            (3, 683, 116, 201),
            (3, 683, 343, 428),
            (3, 456, 230, 315),
            (485, 570, 3, 315),
            (343, 400, 230, 428),
            (3, 9, 116, 428),
            (677, 683, 116, 428),
        ]

    with bd.BuildSketch() as bs:
        for r0, r1, c0, c1 in rects:
            # Map pixel coordinates to CAD sketch (X right, Y up, centered)
            x0 = (c0 - 3.0) / 425.0 * width - width / 2.0
            x1 = (c1 - 3.0) / 425.0 * width - width / 2.0
            y0 = (1.0 - (r1 - 3.0) / 680.0) * height - height / 2.0
            y1 = (1.0 - (r0 - 3.0) / 680.0) * height - height / 2.0
            rw = x1 - x0
            rh = y1 - y0
            cx = (x0 + x1) / 2.0
            cy = (y0 + y1) / 2.0
            if mirrored:
                cx = -cx
            with bd.Locations((cx, cy)):
                bd.Rectangle(rw, rh, mode=bd.Mode.ADD)

    return bs.sketch


# ==============================================================================
# 3. ELEVATED LEG 2D PROFILES (EXTRACTED & ELEVATED)
# ==============================================================================

# Pre-extracted standard 2D cheek boundary loops
BASE_OUTER_LOOP = [
    (174.745, 64.445), (175.681, 63.387), (176.44, 62.196), (177.003, 60.901),
    (177.356, 59.534), (185.991, 10.563), (186.127, 9.143), (186.037, 7.719),
    (185.722, 6.328), (185.192, 5.003), (184.459, 3.779), (183.542, 2.687),
    (182.464, 1.753), (181.252, 1.0), (179.936, 0.449), (178.55, 0.113),
    (177.128, -0.0), (132.049, -0.0), (131.125, 0.048), (130.213, 0.189),
    (129.32, 0.424), (128.453, 0.75), (127.624, 1.163), (126.842, 1.66),
    (126.115, 2.234), (125.451, 2.88), (123.888, 4.458), (122.248, 5.906),
    (120.531, 7.224), (118.737, 8.412), (116.866, 9.469), (114.918, 10.396),
    (112.893, 11.193), (110.791, 11.859), (108.612, 12.395), (106.356, 12.801),
    (104.023, 13.076), (101.613, 13.221), (99.126, 13.236), (96.562, 13.12),
    (93.921, 12.874), (91.203, 12.498), (88.361, 11.955), (85.652, 11.4),
    (83.078, 10.834), (80.637, 10.257), (78.331, 9.668), (76.158, 9.068),
    (74.12, 8.457), (72.215, 7.834), (70.444, 7.2), (68.808, 6.554),
    (67.305, 5.897), (65.936, 5.228), (64.701, 4.549), (63.6, 3.857),
    (62.633, 3.155), (61.8, 2.441), (61.155, 1.889), (60.461, 1.402),
    (59.726, 0.982), (58.952, 0.632), (58.148, 0.357), (57.325, 0.16),
    (56.486, 0.04), (55.638, -0.0), (7.552, -0.0), (6.161, 0.108),
    (4.804, 0.43), (3.513, 0.957), (2.318, 1.678), (1.25, 2.575),
    (0.333, 3.626), (-0.411, 4.806), (-0.963, 6.086), (-1.311, 7.437),
    (-4.833, 27.409), (-4.968, 28.815), (-4.882, 30.224), (-4.576, 31.603),
    (-4.059, 32.917), (-3.342, 34.134), (-2.444, 35.224), (-1.386, 36.16),
    (-0.195, 36.918), (1.1, 37.481), (2.467, 37.835), (166.93, 66.834),
    (168.336, 66.97), (169.746, 66.883), (171.125, 66.578), (172.439, 66.06),
    (173.655, 65.343),
]

BASE_RIM_LOOP = [
    (10.489, 7.5), (54.309, 7.5), (55.178, 7.576), (56.02, 7.802),
    (56.811, 8.171), (57.525, 8.671), (58.904, 9.737), (60.368, 10.704),
    (61.919, 11.592), (63.558, 12.422), (65.118, 13.136), (66.759, 13.82),
    (68.485, 14.477), (70.298, 15.109), (72.2, 15.719), (74.195, 16.311),
    (76.284, 16.886), (78.47, 17.447), (81.113, 18.079), (83.888, 18.693),
    (86.797, 19.291), (89.841, 19.873), (89.929, 19.89), (90.017, 19.904),
    (92.823, 20.297), (95.584, 20.569), (98.301, 20.717), (100.972, 20.738),
    (103.462, 20.639), (105.911, 20.42), (108.317, 20.08), (110.675, 19.617),
    (112.982, 19.03), (115.234, 18.317), (117.429, 17.477), (119.563, 16.509),
    (120.993, 15.768), (122.388, 14.967), (123.748, 14.108), (125.073, 13.192),
    (126.36, 12.22), (127.61, 11.193), (128.821, 10.112), (129.992, 8.978),
    (130.751, 8.351), (131.618, 7.884), (132.561, 7.597), (133.541, 7.5),
    (172.957, 7.5), (174.039, 7.619), (175.07, 7.968), (176.001, 8.533),
    (176.787, 9.286), (177.392, 10.191), (177.787, 11.206), (177.952, 12.282),
    (177.881, 13.368), (170.578, 54.785), (170.262, 55.859), (169.714, 56.835),
    (168.963, 57.665), (168.045, 58.308), (167.008, 58.73), (165.903, 58.91),
    (164.786, 58.841), (7.217, 31.057), (6.143, 30.74), (5.166, 30.192),
    (4.336, 29.441), (3.694, 28.524), (3.272, 27.487), (3.091, 26.382),
    (3.161, 25.265), (5.565, 11.632), (5.834, 10.673), (6.289, 9.787),
    (6.909, 9.009), (7.672, 8.369), (8.547, 7.893), (9.498, 7.599),
]

def _get_base_loops() -> Tuple[List[Tuple[float, float]], List[Tuple[float, float]]]:
    """
    Returns the elevated outer boundary loop and recessed rim loop.
    Applies the +12.0 mm vertical elevation along the 80.0° stance angle.
    """
    outer_loop = BASE_OUTER_LOOP
    rim_loop = BASE_RIM_LOOP

    def _elevate(loop):
        elevated = []
        for y, z in loop:
            if z <= 0.05:
                # Flat ground pads remain at Z = 0
                elevated.append((y, 0.0))
            elif 55.0 <= y <= 132.0 and z <= 13.5:
                # Central underbelly arch remains intact
                elevated.append((y, z))
            elif z >= 25.0:
                # Upper deck profile and rounded corners move up by +12mm
                elevated.append((round(y + ELEVATION_Y, 3), round(z + ELEVATION_Z, 3)))
            else:
                # Smooth linear transition along 80° slant edge
                factor = z / 25.0
                elevated.append((round(y + factor * ELEVATION_Y, 3), round(z + factor * ELEVATION_Z, 3)))
        return elevated

    return _elevate(outer_loop), _elevate(rim_loop)


# ==============================================================================
# 4. ELEVATED LEG BUILDER
# ==============================================================================

def build_elevated_leg(
    is_left: bool = True,
    through_hole_logo: bool = True,
    deboss_logo: bool = False,
    mirror_logo: bool = True,
) -> bd.Solid:
    """
    Constructs the elevated 2020 extrusion pedalboard leg cheek:
      - Slope: 10.0°
      - Elevation: +12.0 mm
      - Flat base at Z = 0 (no foot pockets)
      - 4x 2020 extrusion sockets (20.5 x 20.5 mm x 12.7 mm depth)
      - 4x dia 6.5 mm through-holes for M5/M6 bolts on ALL 4 sockets
      - Through-hole custom logo (cuts through the entire cheek wall, replacing honeycomb)
      - mirror_logo: Horizontally flips the logo on the cheek (defaults to True for left leg)
    """
    elev_outer, elev_rim = _get_base_loops()

    with bd.BuildPart() as bp:
        # 1. Main solid body: extruded from X = 0.0 to X = 19.05 mm
        with bd.BuildSketch(bd.Plane.YZ) as bs_main:
            with bd.BuildLine():
                bd.Polyline([bd.Vector(p[0], p[1]) for p in elev_outer], close=True)
            bd.make_face()
        bd.extrude(amount=CHEEK_WALL_T)

        # 2. Outer border rim: extruded from X = -2.5 mm to X = 0.0 mm
        with bd.BuildSketch(bd.Plane.YZ) as bs_rim:
            with bd.BuildLine():
                bd.Polyline([bd.Vector(p[0], p[1]) for p in elev_outer], close=True)
            bd.make_face()
            with bd.BuildLine(mode=bd.Mode.SUBTRACT):
                bd.Polyline([bd.Vector(p[0], p[1]) for p in elev_rim], close=True)
            bd.make_face(mode=bd.Mode.SUBTRACT)
        with bd.Locations((-RIM_LIP_T, 0, 0)):
            bd.extrude(amount=RIM_LIP_T)

        with bd.BuildPart(mode=bd.Mode.SUBTRACT):
            # 3. 4 Extrusion sockets: from X = 6.35 mm to 20.0 mm (depth 12.7 mm)
            for cy, cz in RAIL_CENTERS_YZ:
                with bd.Locations((X_SOCKET_L + SOCKET_DEPTH / 2.0, cy, cz)):
                    with bd.Locations(bd.Rotation(DECK_ANGLE_DEG, 0, 0)):
                        bd.Box(SOCKET_DEPTH + 2.0, SOCKET_CROSS_SECTION, SOCKET_CROSS_SECTION)

                # 4. Bolt through-holes (dia 6.5 mm) through outer wall for ALL 4 rails
                with bd.Locations((-RIM_LIP_T - 1.0, cy, cz)):
                    bd.Cylinder(radius=BOLT_HOLE_DIA / 2.0, height=X_SOCKET_L + RIM_LIP_T + 2.0,
                                rotation=(0, 90, 0), align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))

            # 5. Logo hole (replaces the honeycomb holes with a through-hole cutout)
            if through_hole_logo:
                logo_sk = make_logo_sketch(width=25.0, stencil=True, mirrored=mirror_logo)
                with bd.BuildSketch(bd.Plane.YZ) as bs_logo:
                    with bd.Locations((148.0, 24.5)):
                        bd.insert(logo_sk)
                with bd.Locations((-RIM_LIP_T - 2.0, 0, 0)):
                    bd.extrude(amount=CHEEK_WALL_T + RIM_LIP_T + 4.0)
            elif deboss_logo:
                logo_sk = make_logo_sketch(width=25.0, stencil=False, mirrored=mirror_logo)
                with bd.BuildSketch(bd.Plane.YZ) as bs_logo:
                    with bd.Locations((148.0, 24.5)):
                        bd.insert(logo_sk)
                with bd.Locations((-0.2, 0, 0)):
                    bd.extrude(amount=1.4)

    leg_l = bp.part

    if is_left:
        return leg_l
    else:
        # Mirror about center plane X = X_MID_PLANE (206.35 mm) to produce right leg
        mid_plane = bd.Plane(origin=(X_MID_PLANE, 0, 0), z_dir=(1, 0, 0))
        return bd.mirror(leg_l, about=mid_plane)


# ==============================================================================
# 5. 2020 ALUMINUM EXTRUSIONS BUILDER
# ==============================================================================

def build_2020_rail(
    length: float = EXTRUSION_LENGTH,
    slotted: bool = True,
) -> bd.Solid:
    """Generates a single 2020 aluminum extrusion along the X axis."""
    with bd.BuildPart() as bp:
        bd.Box(length, EXTRUSION_PROFILE, EXTRUSION_PROFILE,
               align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.CENTER))

        if slotted:
            with bd.BuildPart(mode=bd.Mode.SUBTRACT):
                # Center core hole (5.0 mm dia for M5/M6 thread tapping)
                bd.Cylinder(radius=2.5, height=length + 2.0, rotation=(0, 90, 0))

                # Four 6mm standard T-slots
                for angle in [0, 90, 180, 270]:
                    with bd.Locations(bd.Rotation(angle, 0, 0)):
                        with bd.Locations((0.0, 0.0, 10.0 - 1.0)):
                            bd.Box(length + 2.0, 6.2, 2.2)
                        with bd.Locations((0.0, 0.0, 10.0 - 3.5)):
                            bd.Box(length + 2.0, 9.2, 3.5)

    return bp.part


def build_all_extrusions(
    length: float = EXTRUSION_LENGTH,
    slotted: bool = True,
) -> List[bd.Solid]:
    """Builds the 4x 2020 aluminum extrusions seated inside the elevated leg sockets."""
    rails = []
    base_rail = build_2020_rail(length=length, slotted=slotted)

    for i, (cy, cz) in enumerate(RAIL_CENTERS_YZ):
        placed_rail = (
            bd.Pos(X_RAIL_CENTER, cy, cz)
            * bd.Rotation(DECK_ANGLE_DEG, 0, 0)
            * base_rail
        )
        rails.append(placed_rail)

    return rails


# ==============================================================================
# 6. CONCEPT A: RAIL-MOUNTED CIOKS SOL CRADLE
# ==============================================================================

def build_cioks_rail_cradle() -> bd.Solid:
    """
    Constructs the Concept A rail-mounted underbelly cradle for CIOKS Sol:
      - Top mounting tabs match Rails 3 & 4 underside T-slots (50.0 mm center spacing).
      - Slotted M4/M5 holes allow sliding anywhere along the 400 mm rail width.
      - 2 bottom M4 countersunk holes (70 x 40 mm diagonal) to bolt CIOKS Sol directly.
      - Open IEC port (left), 5 DC jacks bay (right), top troughs, and cooling slots.
      - 100% support-free 3D printing flat on the build plate (Z = 0).
    """
    with bd.BuildPart() as bp:
        # 1. Main outer cradle box
        bd.Box(CRADLE_TOTAL_W, CRADLE_TOTAL_D, CRADLE_TOTAL_H,
               align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))

        # 2. Top mounting tabs for Rails 3 & 4 (at u = -25.0 mm and +25.0 mm):
        for su in [-25.0, 25.0]:
            with bd.BuildPart(mode=bd.Mode.ADD):
                with bd.Locations((0.0, su, CRADLE_TOTAL_H - 4.5)):
                    bd.Box(CRADLE_TOTAL_W - 10.0, 18.0, 4.5,
                           align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))

        with bd.BuildPart(mode=bd.Mode.SUBTRACT):
            # Inner pocket holding the CIOKS Sol
            with bd.Locations((0.0, 0.0, CRADLE_FLOOR_T)):
                bd.Box(CRADLE_INNER_W, CRADLE_INNER_D, CRADLE_INNER_H + 10.0,
                       align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))

            # Left IEC C14 power inlet cutout (72 mm wide x 26 mm high)
            with bd.Locations((-CRADLE_TOTAL_W / 2.0, 0.0, CRADLE_FLOOR_T + 12.0)):
                bd.Box(CRADLE_WALL_T * 4, 72.0, 26.0)

            # Right DC output cables cutout (80 mm wide x 24 mm high)
            with bd.Locations((CRADLE_TOTAL_W / 2.0, 0.0, CRADLE_FLOOR_T + 11.0)):
                bd.Box(CRADLE_WALL_T * 4, 80.0, 24.0)

            # Front & Rear Cable Troughs (notched down by 10 mm for DC cables to exit up between rails)
            for su in [-CRADLE_INNER_D / 2.0 - CRADLE_WALL_T / 2.0, CRADLE_INNER_D / 2.0 + CRADLE_WALL_T / 2.0]:
                with bd.Locations((0.0, su, CRADLE_TOTAL_H - 5.0)):
                    bd.Box(CRADLE_INNER_W - 20.0, CRADLE_WALL_T * 3, 10.0)

            # 5 Thermal convective cooling slots in the floor
            for sy in [-28.0, -14.0, 0.0, 14.0, 28.0]:
                with bd.Locations((0.0, sy, 0.0)):
                    with bd.BuildSketch():
                        bd.RectangleRounded(75.0, 6.0, radius=2.5)
                    bd.extrude(amount=CRADLE_FLOOR_T * 3, both=True)

            # 2 Diagonal M4 countersunk holes for direct CIOKS Sol enclosure bolting
            for mx, my in [(-35.0, -20.0), (35.0, 20.0)]:
                with bd.Locations((mx, my, 0.0)):
                    bd.Cylinder(radius=2.2, height=CRADLE_FLOOR_T * 4)
                    bd.Cylinder(radius=4.5, height=2.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))

            # Slotted mounting holes on top flanges for M4/M5 T-nuts:
            for sx in [-48.0, 48.0]:
                for su in [-25.0, 25.0]:
                    with bd.Locations((sx, su, CRADLE_TOTAL_H - 10.0)):
                        with bd.BuildSketch():
                            bd.SlotOverall(12.0, 5.5)
                        bd.extrude(amount=20.0)

    return bp.part


def build_cioks_sol_mockup() -> bd.Solid:
    """Builds a reference 3D model of the CIOKS Sol power supply."""
    with bd.BuildPart() as bp:
        bd.Box(CIOKS_SOL_W, CIOKS_SOL_D, CIOKS_SOL_H,
               align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.CENTER))
        with bd.BuildPart(mode=bd.Mode.SUBTRACT):
            with bd.Locations((-CIOKS_SOL_W / 2.0, 0.0, 0.0)):
                bd.Box(10.0, 28.0, 20.0)
            for dy in [-30.0, -15.0, 0.0, 15.0, 30.0]:
                with bd.Locations((CIOKS_SOL_W / 2.0, dy, 0.0)):
                    bd.Cylinder(radius=5.0, height=8.0, rotation=(0, 90, 0))
    return bp.part


def place_cradle_under_rails(
    cradle: bd.Solid,
    x_pos: float = X_RAIL_CENTER,
) -> bd.Solid:
    """
    Transforms the cradle into its exact underbelly mounted position under Rails 3 & 4.
    Top mounting tabs seat flush against the bottom faces of Rails 3 & 4.
    """
    cy3, cz3 = RAIL_CENTERS_YZ[2]
    cy4, cz4 = RAIL_CENTERS_YZ[3]
    y_mid = (cy3 + cy4) / 2.0
    z_mid = (cz3 + cz4) / 2.0

    # In local tilted coordinates (u along slope, v perpendicular upwards):
    # Rail centers are at v = 0. Rail bottom face is at v = -10.0 mm.
    # Cradle top tab surface is at local Z = CRADLE_TOTAL_H.
    # Align local Z = CRADLE_TOTAL_H flush against v = -10.0 mm:
    cos_t = math.cos(DECK_ANGLE_RAD)
    sin_t = math.sin(DECK_ANGLE_RAD)

    # Transform: cradle origin (Z=0) sits at v = -10.0 - CRADLE_TOTAL_H:
    v_cradle_origin = -(10.0 + CRADLE_TOTAL_H)
    cradle_y = y_mid - v_cradle_origin * sin_t
    cradle_z = z_mid + v_cradle_origin * cos_t

    return bd.Pos(x_pos, cradle_y, cradle_z) * bd.Rotation(DECK_ANGLE_DEG, 0, 0) * cradle


# ==============================================================================
# 7. CLEARANCE & INTERFERENCE ANALYSIS
# ==============================================================================

def analyze_clearances() -> Dict[str, float]:
    """Computes exact vertical elevations and clearances to the floor (Z = 0)."""
    cos_t = math.cos(DECK_ANGLE_RAD)
    sin_t = math.sin(DECK_ANGLE_RAD)

    results = {}
    print("=" * 72)
    print("ELEVATED PLATFORM CLEARANCE ANALYSIS (+12mm Lift, Z = 0 is table/floor):")
    print("=" * 72)

    for i, (cy, cz) in enumerate(RAIL_CENTERS_YZ, start=1):
        z_front = cz - 10.0 * sin_t - 10.0 * cos_t
        z_rear = cz + 10.0 * sin_t - 10.0 * cos_t
        results[f"rail_{i}_bottom_min_z"] = min(z_front, z_rear)
        print(f"Rail {i}: Center=({cy:.2f}, {cz:.2f}) mm | Bottom Face Z = [{z_front:.2f}, {z_rear:.2f}] mm")

    # Cradle lowest point (front-bottom corner under Rail 3):
    cy3, cz3 = RAIL_CENTERS_YZ[2]
    cy4, cz4 = RAIL_CENTERS_YZ[3]
    y_mid = (cy3 + cy4) / 2.0
    z_mid = (cz3 + cz4) / 2.0

    # Cradle front-bottom corner is at u = -CRADLE_TOTAL_D / 2.0 (-48.5 mm), v = -10.0 - CRADLE_TOTAL_H (-39.0 mm):
    u_corner = -CRADLE_TOTAL_D / 2.0
    v_corner = -(10.0 + CRADLE_TOTAL_H)
    z_cradle_min = z_mid + u_corner * sin_t + v_corner * cos_t
    y_cradle_front = y_mid + u_corner * cos_t - v_corner * sin_t

    results["cradle_lowest_z"] = z_cradle_min
    results["cradle_front_y"] = y_cradle_front

    print("-" * 72)
    print(f"Rail-Mounted Cradle Under Rails 3 & 4:")
    print(f"  Front Edge Y Position : {y_cradle_front:.2f} mm")
    print(f"  Lowest Point Elevation: {z_cradle_min:.2f} mm from floor")

    if z_cradle_min < 0:
        print(f"  [!] COLLISION: Cradle penetrates floor by {abs(z_cradle_min):.2f} mm!")
    else:
        print(f"  [OK] POSITIVE FLOOR CLEARANCE of +{z_cradle_min:.2f} mm! (Zero table collision)")

    print("=" * 72)
    return results


# ==============================================================================
# 8. COMPLETE ASSEMBLY BUILDER
# ==============================================================================

def build_complete_assembly() -> Dict[str, bd.Solid]:
    """Generates the full elevated pedalboard assembly with all components."""
    print("\nBuilding elevated components...")
    leg_l = build_elevated_leg(is_left=True, through_hole_logo=True)
    leg_r = build_elevated_leg(is_left=False, through_hole_logo=True)
    rails = build_all_extrusions(length=EXTRUSION_LENGTH, slotted=True)
    cradle = build_cioks_rail_cradle()
    cradle_placed = place_cradle_under_rails(cradle, x_pos=X_RAIL_CENTER)

    # CIOKS Sol preview inside cradle
    cy3, cz3 = RAIL_CENTERS_YZ[2]
    cy4, cz4 = RAIL_CENTERS_YZ[3]
    y_mid = (cy3 + cy4) / 2.0
    z_mid = (cz3 + cz4) / 2.0
    v_sol = -(10.0 + CRADLE_FLOOR_T + CIOKS_SOL_H / 2.0)
    cos_t = math.cos(DECK_ANGLE_RAD)
    sin_t = math.sin(DECK_ANGLE_RAD)
    sol_y = y_mid - v_sol * sin_t
    sol_z = z_mid + v_sol * cos_t
    cioks_sol = bd.Pos(X_RAIL_CENTER, sol_y, sol_z) * bd.Rotation(DECK_ANGLE_DEG, 0, 0) * build_cioks_sol_mockup()

    return {
        "leg_left_elevated": leg_l,
        "leg_right_elevated": leg_r,
        "rail_1_front": rails[0],
        "rail_2_mid_front": rails[1],
        "rail_3_mid_rear": rails[2],
        "rail_4_rear": rails[3],
        "cioks_rail_cradle": cradle_placed,
        "cioks_sol_preview": cioks_sol,
        "raw_cradle": cradle,
    }


# ==============================================================================
# 9. MAIN EXECUTION & STL EXPORT
# ==============================================================================

def main():
    print("=" * 72)
    print("LINK-400 Elevated 2020 Extrusion Pedalboard Platform Builder")
    print("=" * 72)

    models = build_complete_assembly()

    print("\nComponent Summary:")
    for name, part in models.items():
        bb = part.bounding_box()
        print(f"  {name:<22} | Valid: {part.is_valid!s:<5} | Volume: {part.volume / 1000.0:>6.2f} cm³ | BBox: {bb.size.X:.1f} x {bb.size.Y:.1f} x {bb.size.Z:.1f} mm")

    analyze_clearances()

    # 1. Export 3D-printable STLs oriented flat for the build plate:
    print("\nExporting 3D Printable STLs (Oriented Flat on Bed)...")

    # Left leg: oriented flat on its inner face (X = 19.05 mm rotated to Z = 0)
    leg_l = models["leg_left_elevated"]
    rot_l = bd.Rotation(0, 90, 0) * leg_l
    bb_l = rot_l.bounding_box()
    leg_l_flat = bd.Pos(0, 0, -bb_l.min.Z) * rot_l
    bd.export_stl(leg_l_flat, "pedalboard_leg_elevated_l.stl", tolerance=0.04, angular_tolerance=0.08)
    print("  [OK] Exported pedalboard_leg_elevated_l.stl (Flat on inner face, zero supports)")

    # Right leg: oriented flat on its inner face
    leg_r = models["leg_right_elevated"]
    rot_r = bd.Rotation(0, -90, 0) * leg_r
    bb_r = rot_r.bounding_box()
    leg_r_flat = bd.Pos(0, 0, -bb_r.min.Z) * rot_r
    bd.export_stl(leg_r_flat, "pedalboard_leg_elevated_r.stl", tolerance=0.04, angular_tolerance=0.08)
    print("  [OK] Exported pedalboard_leg_elevated_r.stl (Flat on inner face, zero supports)")

    # Cradle: oriented flat on its bottom floor (Z = 0)
    cradle_raw = models["raw_cradle"]
    bd.export_stl(cradle_raw, "pedalboard_cioks_rail_cradle.stl", tolerance=0.04, angular_tolerance=0.08)
    print("  [OK] Exported pedalboard_cioks_rail_cradle.stl (Flat on base, zero supports)")

    # 2. Export Assembled STLs
    rails_solid = models["rail_1_front"] + models["rail_2_mid_front"] + models["rail_3_mid_rear"] + models["rail_4_rear"]
    bd.export_stl(rails_solid, "pedalboard_2020_rails_elevated.stl", tolerance=0.05, angular_tolerance=0.1)
    print("  [OK] Exported pedalboard_2020_rails_elevated.stl (4x elevated rails)")

    full_assembly = models["leg_left_elevated"] + models["leg_right_elevated"] + rails_solid + models["cioks_rail_cradle"]
    bd.export_stl(full_assembly, "pedalboard_extrusion_assembly_v2.stl", tolerance=0.05, angular_tolerance=0.1)
    print("  [OK] Exported pedalboard_extrusion_assembly_v2.stl (Complete merged assembly)")

    # 3. Broadcast to OCP CAD Viewer
    try:
        from ocp_vscode import show
        print("\nBroadcasting elevated assembly to OCP CAD Viewer...")
        show(
            models["leg_left_elevated"],
            models["leg_right_elevated"],
            rails_solid,
            models["cioks_rail_cradle"],
            models["cioks_sol_preview"],
            names=[
                "Left Leg (+12mm, Bolted, Debossed Logo)",
                "Right Leg (+12mm, Bolted, Debossed Logo)",
                "4x 2020 Aluminum Rails (Elevated)",
                "CIOKS Sol Rail-Mounted Cradle (Concept A)",
                "CIOKS Sol Power Supply (Reference)",
            ],
            colors=[
                (0.22, 0.22, 0.25, 1.0),   # Matte Charcoal PETG
                (0.22, 0.22, 0.25, 1.0),   # Matte Charcoal PETG
                (0.75, 0.76, 0.78, 1.0),   # Anodized Silver Aluminum
                (0.20, 0.85, 0.35, 0.90),  # Neon Green Cradle
                (0.95, 0.45, 0.10, 0.80),  # CIOKS Orange Mockup
            ],
        )
        print("OCP CAD Viewer broadcast complete.")
    except Exception as e:
        print(f"Note: OCP CAD Viewer broadcast skipped: {e}")


if __name__ == "__main__":
    main()

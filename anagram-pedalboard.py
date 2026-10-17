#!/usr/bin/env python3
"""
Darkglass Anagram Standalone Stage Pedalboard
=============================================
Parametric, 3D-printable stage pedalboard platform custom-designed for:
  - Upper Deck: Darkglass Anagram multi-effects modeling workstation (8.0° incline)
  - Underbelly: Baseus GaN3 Pro 65W Desktop Charger (Model CCDK65S: 70x40x36.9mm)
  - Slide-in outer flank bay: Charger slides directly into the cradle from the right flank
  - Positive snap detent locks the charger securely inside the cradle (tool-less)
  - Direct right-side AC mains cord exit (no cord threading or disassembly needed)
  - Inner USB port window (32x26mm) for clean internal routing of DC/USB cables
  - Through-wall zip-tie anchor slots (100% printable with zero floating geometry)
  - Continuous vertical stomp keel + transverse bulkhead for zero-deflection foot switching
  - 5-point non-slip base with 12.7mm (1/2") recessed rubber bumper counterbores
  - Full-width rear I/O cutout for direct plug-in of XLRs, 1/4" jacks, MIDI, and USB-C
  - Ergonomic side finger pry notches for effortless, tool-less pedal removal

Wall thicknesses optimized (-1.0mm reduction from baseline):
  - Side Walls: 3.25mm
  - Front Lip Wall: 3.0mm
  - Rear Wall: 3.5mm
  - Internal Cradle Walls: 2.5mm
  - All pocket dimensions, clearances, and insert counterbores 100% preserved.

Compatible with standard 256x256mm, 220x220mm, and 250x210mm desktop 3D printer beds.

Designed with build123d.
"""

import math
import sys
import build123d as bd

# ==============================================================================
# 1. PARAMETRIC CONFIGURATION & SPECIFICATIONS
# ==============================================================================

# --- Darkglass Anagram Device & Pocket ---
# Physical chassis: 210.0 x 105.0 x 62.0 mm, ~815 g
POCKET_WIDTH = 213.5          # +1.5 mm tolerance (fits bare or with 3D cover)
ANAGRAM_DEPTH_SLOPE = 106.5   # Pocket depth along 8° slope (+1.5 mm tolerance)
ANAGRAM_ANGLE = 8.0           # Ergonomic viewing & stomp incline (degrees)
ANAGRAM_LIP = 6.0             # Perimeter retaining lip depth (mm)

# Trigonometric projections
RAD_A = math.radians(ANAGRAM_ANGLE)
COS_A = math.cos(RAD_A)       # ~0.990268
SIN_A = math.sin(RAD_A)       # ~0.139173
TAN_A = math.tan(RAD_A)       # ~0.140541

ANAGRAM_Y_SPAN = ANAGRAM_DEPTH_SLOPE * COS_A  # ~105.46 mm

# --- Overall Chassis Envelope (Optimized 1mm Reduced Walls) ---
SIDE_WALL = 3.25              # Perimeter sidewall thickness (reduced by 1.0mm from 4.25mm)
BOARD_WIDTH = POCKET_WIDTH + 2 * SIDE_WALL    # 220.0 mm (was 222.0mm)
FRONT_WALL = 3.0              # Front perimeter lip thickness (reduced by 1.0mm from 4.0mm)
REAR_WALL = 3.5               # Rear perimeter wall thickness (reduced by 1.0mm from 4.5mm)

TOTAL_DEPTH = FRONT_WALL + ANAGRAM_Y_SPAN + REAR_WALL # ~112.0 mm (was 114.0mm)

# Deck elevations
ANAGRAM_FRONT_Z = 38.0        # Front deck floor elevation (gives ~39.2-45.5mm underbelly clearance)
UNDER_DECK_T = 3.5            # Upper deck floor plate thickness (mm)

ANAGRAM_REAR_FLOOR_Z = ANAGRAM_FRONT_Z + ANAGRAM_DEPTH_SLOPE * SIN_A # ~52.82 mm
FRONT_TOP_Z = ANAGRAM_FRONT_Z + ANAGRAM_LIP * COS_A                 # ~43.94 mm
REAR_TOP_Z = ANAGRAM_REAR_FLOOR_Z + ANAGRAM_LIP * COS_A             # ~58.76 mm

# --- Underbelly Transverse Charger Cradle: Baseus GaN3 Pro 65W (CCDK65S) ---
# Physical dimensions: 70.0 mm (L) x 40.0 mm (W) x 36.9 mm (H)
# Transverse orientation along X-axis:
#   - Length (70mm) along X (slides in from right flank inward towards center)
#   - Width (40mm) along Y
#   - Height (36.9mm) along Z
CHARGER_L_TOL = 72.5          # +2.5 mm length clearance along X
CHARGER_W_TOL = 42.0          # +2.0 mm width clearance along Y
CHARGER_H_TOL = 38.5          # +1.6 mm height clearance along Z

# Placement along X: Right end meets the right side opening
CHARGER_X_RIGHT = POCKET_WIDTH / 2.0                 # +106.75 mm
CHARGER_X_LEFT = CHARGER_X_RIGHT - CHARGER_L_TOL     # +34.25 mm
CHARGER_X_CTR = (CHARGER_X_LEFT + CHARGER_X_RIGHT) / 2.0 # +70.50 mm

# Placement along Y: Centered in underbelly run
CHARGER_Y_CTR = FRONT_WALL + ANAGRAM_Y_SPAN * 0.52   # ~57.8 mm
CHARGER_Y_FRONT = CHARGER_Y_CTR - CHARGER_W_TOL / 2.0 # ~36.8 mm
CHARGER_Y_REAR = CHARGER_Y_CTR + CHARGER_W_TOL / 2.0  # ~78.8 mm
CRADLE_WALL_T = 2.5           # Reduced internal cradle wall thickness (mm)

# --- Rubber Bumper Feet (5-Point Anti-Slip Base) ---
FOOT_DIAMETER = 12.7          # Standard 1/2" adhesive bumper feet
FOOT_DEPTH = 3.5              # Recessed counterbore depth
FEET_LOCATIONS = [
    (-95.0, 14.0),            # Front-Left
    ( 95.0, 14.0),            # Front-Right
    (-95.0, TOTAL_DEPTH - 14.0), # Rear-Left (~98.0mm)
    ( 95.0, TOTAL_DEPTH - 14.0), # Rear-Right (~98.0mm)
    (  0.0, 52.0),            # Center Stomp Pillar (directly under footswitches)
]


# ==============================================================================
# 2. SOLID MODEL GENERATION
# ==============================================================================

def build_anagram_pedalboard() -> bd.Solid:
    """Constructs the monolithic standalone Darkglass Anagram pedalboard solid."""
    print("=" * 70)
    print("Generating Standalone Darkglass Anagram Pedalboard (Optimized Walls)...")
    print(f"Footprint: {BOARD_WIDTH:.1f} mm (W) x {TOTAL_DEPTH:.1f} mm (D) x {REAR_TOP_Z:.1f} mm (H)")
    print(f"Walls: Sides {SIDE_WALL:.2f}mm | Front {FRONT_WALL:.1f}mm | Rear {REAR_WALL:.1f}mm")
    print(f"Incline: {ANAGRAM_ANGLE:.1f}° | Front Deck Z: {ANAGRAM_FRONT_Z:.1f} mm")
    print("=" * 70)

    # --------------------------------------------------------------------------
    # Step 1: Base Monolithic Hull Extrusion (YZ Silhouette extruded along X)
    # --------------------------------------------------------------------------
    hull_pts = [
        (0.0, 0.0),
        (0.0, FRONT_TOP_Z),
        (FRONT_WALL, FRONT_TOP_Z),
        (TOTAL_DEPTH, REAR_TOP_Z),
        (TOTAL_DEPTH, 0.0),
        (0.0, 0.0),
    ]

    with bd.BuildPart() as bp:
        with bd.BuildSketch(bd.Plane.YZ):
            bd.Polygon(hull_pts)
        bd.extrude(amount=BOARD_WIDTH / 2.0, both=True)

        # Fillet exterior 4 vertical corners (3.0mm radius matching reduced wall thickness)
        front_edges = bp.edges().filter_by(bd.Axis.Z).sort_by(bd.Axis.Y)[:2]
        rear_edges = bp.edges().filter_by(bd.Axis.Z).sort_by(bd.Axis.Y)[-2:]
        bd.fillet(front_edges, radius=3.0)
        bd.fillet(rear_edges, radius=3.0)

        # ----------------------------------------------------------------------
        # Step 2: Upper Deck - Darkglass Anagram Angled Tray Pocket (8.0° Incline)
        # ----------------------------------------------------------------------
        deck_mid_dist = ANAGRAM_DEPTH_SLOPE / 2.0
        deck_mid_y = FRONT_WALL + deck_mid_dist * COS_A
        deck_mid_z = ANAGRAM_FRONT_Z + deck_mid_dist * SIN_A

        tray_plane = bd.Plane(
            origin=(0.0, deck_mid_y, deck_mid_z),
            x_dir=(1.0, 0.0, 0.0),
            z_dir=(0.0, -SIN_A, COS_A),  # Normal perpendicular to angled deck
        )
        with bd.BuildPart(mode=bd.Mode.SUBTRACT):
            with bd.Locations(tray_plane):
                # Subtract pedal pocket cavity
                with bd.Locations((0.0, 0.0, 25.0)):
                    bd.Box(POCKET_WIDTH, ANAGRAM_DEPTH_SLOPE, 50.0)

        # ----------------------------------------------------------------------
        # Step 3: Large Open Rear Perimeter Bay for Darkglass I/O
        # ----------------------------------------------------------------------
        # Direct line-of-sight access for all XLRs, 1/4" audio, TRS MIDI, USB, and DC
        with bd.BuildPart(mode=bd.Mode.SUBTRACT):
            with bd.Locations((0.0, TOTAL_DEPTH, (ANAGRAM_REAR_FLOOR_Z + REAR_TOP_Z) / 2.0)):
                bd.Box(175.0, 20.0, 28.0)

        # ----------------------------------------------------------------------
        # Step 4: Ergonomic Side Finger Pry Notches
        # ----------------------------------------------------------------------
        # Enables effortless, tool-less lifting of the Anagram
        with bd.BuildPart(mode=bd.Mode.SUBTRACT):
            for side in [-1, 1]:
                with bd.Locations((side * (BOARD_WIDTH / 2.0), deck_mid_y, deck_mid_z + 8.0)):
                    bd.Cylinder(radius=15.0, height=20.0)

        # ----------------------------------------------------------------------
        # Step 5: Open Underbelly Chamber Beneath Anagram Deck
        # ----------------------------------------------------------------------
        under_pts = [
            (FRONT_WALL, 0.0),
            (TOTAL_DEPTH - REAR_WALL, 0.0),
            (TOTAL_DEPTH - REAR_WALL, ANAGRAM_REAR_FLOOR_Z - UNDER_DECK_T),
            (FRONT_WALL, ANAGRAM_FRONT_Z - UNDER_DECK_T),
            (FRONT_WALL, 0.0),
        ]
        with bd.BuildSketch(bd.Plane.YZ) as s_under:
            bd.Polygon(under_pts)
        bd.extrude(amount=POCKET_WIDTH / 2.0, both=True, mode=bd.Mode.SUBTRACT)

        # ----------------------------------------------------------------------
        # Step 6: Central Longitudinal Stomp Spine (Zero-Flex Keel)
        # ----------------------------------------------------------------------
        # Continuous 3.5mm thick vertical spine connecting deck underside to floor (Z=0)
        with bd.BuildPart(mode=bd.Mode.ADD):
            with bd.BuildSketch(bd.Plane.YZ):
                bd.Polygon(under_pts)
            bd.extrude(amount=3.5 / 2.0, both=True)

        # ----------------------------------------------------------------------
        # Step 7: Transverse Stomp Bulkhead Under Anagram Footswitches
        # ----------------------------------------------------------------------
        stomp_y = FRONT_WALL + 32.0   # Directly beneath footswitches A, B, C
        stomp_deck_z = ANAGRAM_FRONT_Z + (stomp_y - FRONT_WALL) * TAN_A - UNDER_DECK_T
        with bd.BuildPart(mode=bd.Mode.ADD):
            with bd.Locations((0.0, stomp_y, 0.0)):
                bd.Box(
                    POCKET_WIDTH,
                    3.5,
                    stomp_deck_z,
                    align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
                )

        # Central spine cable routing portal
        with bd.BuildPart(mode=bd.Mode.SUBTRACT):
            with bd.Locations((0.0, stomp_y, 10.0)):
                bd.Box(20.0, 16.0, 14.0)

        # ----------------------------------------------------------------------
        # Step 8: Transverse Baseus GaN3 Pro Slide-In Cradle (Right Flank)
        # ----------------------------------------------------------------------
        # Front and Rear Cradle Guiding Walls along the charger length (X-axis)
        cradle_y_front = CHARGER_Y_FRONT - CRADLE_WALL_T / 2.0
        cradle_y_rear = CHARGER_Y_REAR + CRADLE_WALL_T / 2.0

        for cy in [cradle_y_front, cradle_y_rear]:
            wall_deck_z = ANAGRAM_FRONT_Z + (cy - FRONT_WALL) * TAN_A - UNDER_DECK_T
            with bd.BuildPart(mode=bd.Mode.ADD):
                with bd.Locations((CHARGER_X_CTR, cy, 0.0)):
                    bd.Box(
                        CHARGER_L_TOL,
                        CRADLE_WALL_T,
                        wall_deck_z,
                        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
                    )

        # Inner Stop Wall (at X = CHARGER_X_LEFT) to seat charger when fully slid in
        inner_stop_deck_z = ANAGRAM_FRONT_Z + (CHARGER_Y_CTR - FRONT_WALL) * TAN_A - UNDER_DECK_T
        with bd.BuildPart(mode=bd.Mode.ADD):
            with bd.Locations((CHARGER_X_LEFT - CRADLE_WALL_T / 2.0, CHARGER_Y_CTR, 0.0)):
                bd.Box(
                    CRADLE_WALL_T,
                    CHARGER_W_TOL + 2 * CRADLE_WALL_T,
                    inner_stop_deck_z,
                    align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
                )

        # Inner USB Port Window in the inner stop wall
        # Gives unobstructed access to all 4 USB ports into the central underbelly chamber
        with bd.BuildPart(mode=bd.Mode.SUBTRACT):
            with bd.Locations((CHARGER_X_LEFT - CRADLE_WALL_T / 2.0, CHARGER_Y_CTR, 18.0)):
                bd.Box(15.0, 32.0, 26.0)

        # Bottom resting shelves along front and rear cradle walls (1.0mm height)
        # Supports the bottom edges of the charger while leaving a 36mm wide center airflow gap
        ledge_w = 3.0
        ledge_h = 1.0
        with bd.BuildPart(mode=bd.Mode.ADD):
            # Front bottom shelf
            with bd.Locations((CHARGER_X_CTR, CHARGER_Y_FRONT + ledge_w / 2.0, 0.0)):
                bd.Box(
                    CHARGER_L_TOL,
                    ledge_w,
                    ledge_h,
                    align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
                )
            # Rear bottom shelf
            with bd.Locations((CHARGER_X_CTR, CHARGER_Y_REAR - ledge_w / 2.0, 0.0)):
                bd.Box(
                    CHARGER_L_TOL,
                    ledge_w,
                    ledge_h,
                    align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
                )

        # ----------------------------------------------------------------------
        # Step 9: Right Flank Slide-In Portal (Enables Direct Tool-Less Insertion)
        # ----------------------------------------------------------------------
        # Completely opens the right flank so the charger slides straight into the cradle!
        with bd.BuildPart(mode=bd.Mode.SUBTRACT):
            with bd.Locations((BOARD_WIDTH / 2.0, CHARGER_Y_CTR, 0.0)):
                bd.Box(25.0, CHARGER_W_TOL, CHARGER_H_TOL * 2)

        # Positive Snap Detent Bump at the outer entry (locks charger in place when seated)
        with bd.BuildPart(mode=bd.Mode.ADD):
            with bd.Locations((CHARGER_X_RIGHT + 0.5, CHARGER_Y_REAR - 0.5, 12.0)):
                bd.Cylinder(radius=1.5, height=16.0)

        # ----------------------------------------------------------------------
        # Step 10: 100% Printable Through-Wall Zip-Tie Cable Anchor Slots
        # ----------------------------------------------------------------------
        # Slots cut directly through existing solid vertical walls (zero floating geometry)
        with bd.BuildPart(mode=bd.Mode.SUBTRACT):
            # Slots in Inner Stop Wall (secures USB-C cables right at charger exit)
            with bd.Locations((CHARGER_X_LEFT - CRADLE_WALL_T / 2.0, CHARGER_Y_CTR - 10.0, 32.0)):
                bd.Box(10.0, 4.0, 2.5)
            with bd.Locations((CHARGER_X_LEFT - CRADLE_WALL_T / 2.0, CHARGER_Y_CTR + 10.0, 32.0)):
                bd.Box(10.0, 4.0, 2.5)
            # Slots in Central Load Spine (secures power/MIDI cables heading to rear I/O)
            with bd.Locations((0.0, 60.0, 22.0)):
                bd.Box(10.0, 4.0, 2.5)
            with bd.Locations((0.0, 90.0, 26.0)):
                bd.Box(10.0, 4.0, 2.5)
            # Slot in Stomp Bulkhead (left-side cable anchoring)
            with bd.Locations((-45.0, stomp_y, 18.0)):
                bd.Box(4.0, 10.0, 2.5)

        # ----------------------------------------------------------------------
        # Step 11: Skeletal Side Wall Cutouts (Left Flank)
        # ----------------------------------------------------------------------
        # Weight-saving triangular windows on the left side wall (away from charger)
        with bd.BuildPart(mode=bd.Mode.SUBTRACT):
            with bd.Locations((-BOARD_WIDTH / 2.0, 42.0, 15.0)):
                bd.Box(15.0, 24.0, 14.0)
            with bd.Locations((-BOARD_WIDTH / 2.0, 85.0, 22.0)):
                bd.Box(15.0, 28.0, 18.0)

        # ----------------------------------------------------------------------
        # Step 12: 5 Non-Slip Rubber Bumper Feet Recessed Pockets
        # ----------------------------------------------------------------------
        with bd.BuildPart(mode=bd.Mode.SUBTRACT):
            for fx, fy in FEET_LOCATIONS:
                with bd.Locations((fx, fy, 0.0)):
                    bd.Cylinder(radius=FOOT_DIAMETER / 2.0, height=FOOT_DEPTH * 2.0)

    solid = bp.part
    print(f"Build completed successfully! Solid Volume: {solid.volume / 1000.0:.2f} cm³")
    print(f"Watertight Solid: {solid.is_valid}")
    return solid


# ==============================================================================
# 3. COMPLETE ASSEMBLY VISUALIZATION WITH DUMMY DEVICES
# ==============================================================================

def build_assembly() -> bd.Compound:
    """Builds full assembly mockup including pedalboard chassis and populated devices."""
    pedalboard = build_anagram_pedalboard()

    # Mockup: Darkglass Anagram
    deck_mid_dist = ANAGRAM_DEPTH_SLOPE / 2.0
    deck_mid_y = FRONT_WALL + deck_mid_dist * COS_A
    deck_mid_z = ANAGRAM_FRONT_Z + deck_mid_dist * SIN_A
    tray_plane = bd.Plane(
        origin=(0.0, deck_mid_y, deck_mid_z),
        x_dir=(1.0, 0.0, 0.0),
        z_dir=(0.0, -SIN_A, COS_A),
    )
    with bd.BuildPart() as ana_bp:
        with bd.Locations(tray_plane):
            with bd.Locations((0.0, 0.0, 31.0)):
                # Main body (210 x 105 x 62 mm)
                bd.Box(210.0, 105.0, 62.0)
            # Display Area (7 inch screen)
            with bd.Locations((0.0, 12.0, 62.5)):
                bd.Box(155.0, 60.0, 1.0)
            # 3 Primary Footswitches
            for sw_x in [-75.0, 0.0, 75.0]:
                with bd.Locations((sw_x, -36.0, 62.0)):
                    bd.Cylinder(radius=6.0, height=8.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
            # Rotary Knobs
            for kx in [-75.0, -45.0, -15.0, 15.0, 45.0, 75.0]:
                with bd.Locations((kx, 42.0, 62.0)):
                    bd.Cylinder(radius=5.0, height=12.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
    anagram_full = ana_bp.part

    # Mockup: Baseus GaN3 Pro 65W Desktop Charger (Transverse: 70 along X, 40 along Y, 36.9 along Z)
    charger_body = bd.Box(70.0, 40.0, 36.9, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
    charger_body = charger_body.translate((CHARGER_X_CTR, CHARGER_Y_CTR, 1.0))

    # Mockup: Rubber Feet
    feet = []
    for fx, fy in FEET_LOCATIONS:
        foot = bd.Cylinder(radius=12.7 / 2.0, height=4.5, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MAX))
        foot = foot.translate((fx, fy, 0.0))
        feet.append(foot)

    # Combine into assembly compound
    assembly = bd.Compound(
        [
            pedalboard,
            anagram_full,
            charger_body,
        ] + feet
    )
    return assembly


# ==============================================================================
# 4. EXECUTION & CAD VIEWER EXPORT
# ==============================================================================

if __name__ == "__main__":
    pedalboard = build_anagram_pedalboard()

    # Export high-resolution mesh STL for 3D printing
    stl_path = "anagram-pedalboard.stl"
    print(f"Exporting high-resolution mesh to {stl_path}...")
    bd.export_stl(pedalboard, stl_path, tolerance=0.05, angular_tolerance=0.1)
    print(f"Successfully exported {stl_path}!")

    # Attempt to render in VS Code OCP CAD Viewer
    try:
        from ocp_vscode import show
        print("Broadcasting pedalboard to OCP CAD Viewer...")
        show(
            pedalboard,
            names=["Darkglass Anagram Pedalboard"],
            colors=[(0.2, 0.2, 0.22, 1.0)],
        )
        print("Model visible in VS Code CAD Viewer.")
    except Exception as e:
        print(f"Note: OCP CAD Viewer broadcast skipped: {e}")

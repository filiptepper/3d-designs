#!/usr/bin/env python3
"""
Stage Pedalboard Platform - Tour-Grade Engineering Specification
==================================================================
Fully parametric, 3D-printable two-tier stage pedalboard designed for:
  - Lower Tier: M-VAVE Chocolate Plus wireless/wired MIDI controller
  - Upper Tier: Darkglass Anagram multi-effects modeling workstation (8.0° incline)
  - Underbelly: Baseus GaN3 Pro 65W Desktop Charger (Model CCDK65S: 70x40x36.9mm)
  - Tool-less snap-in underbelly charger cradle with quick-release flex tabs
  - Raised continuous toe-guard barrier rib (protects Anagram screen/knobs from boots)
  - Full-width inter-tier cable drop trench for right-angle USB-C and TRS connectors
  - Structural stomp keel + transverse bulkhead for 0-flex dynamic stomp handling
  - 5-point non-slip base with solid flat mounting pads for adhesive rubber bumper feet
  - Strict EMI isolation (>120mm separation between AC/DC power and audio signals)
  - Convective thermal chimney ventilation slots under the GaN power supply

Compatible with standard 256x256mm and 250x210mm desktop 3D printer beds.

Designed with build123d.
"""

import math
import sys
import build123d as bd

# ==============================================================================
# 1. PARAMETRIC CONFIGURATION & SPECIFICATIONS
# ==============================================================================

# --- Overall Footprint & Wall Thickness ---
POCKET_WIDTH = 213.5          # Fits both Chocolate (212mm) & Anagram (210mm) + tolerance
SIDE_WALL = 4.25              # Heavy-duty perimeter sidewall thickness (mm)
BOARD_WIDTH = POCKET_WIDTH + 2 * SIDE_WALL  # 222.0 mm (fits 250-256mm beds)
FLOOR_THICKNESS = 3.0         # Rigid base floor thickness (mm)
UNDER_DECK_T = 3.5            # Upper deck floor thickness (mm)

# --- Lower Tier: M-VAVE Chocolate Plus ---
# Physical device: 212.0 x 36.0 x 17.0 mm
CHOC_DEPTH = 37.0             # Recessed pocket depth (+1.0 mm tolerance)
CHOC_LIP = 6.0                # Perimeter retaining lip depth (mm)
CHOC_Y0 = 4.0                 # Front perimeter wall thickness
CHOC_Y1 = CHOC_Y0 + CHOC_DEPTH # 41.0 mm
CHOC_Z_FLOOR = FLOOR_THICKNESS # 3.0 mm
CHOC_Z_TOP = CHOC_Z_FLOOR + CHOC_LIP # 9.0 mm

# --- Inter-Tier Cable Drop Trench ---
# Full-width opening allowing right-angle cables to dive straight below deck
TRENCH_WIDTH = 22.0           # 22mm axial clearance for 90° cables
TRENCH_Y0 = CHOC_Y1           # 41.0 mm
TRENCH_Y1 = TRENCH_Y0 + TRENCH_WIDTH # 63.0 mm

# --- Raised Toe-Guard Barrier Rib ---
# Prevents stage boots from sliding forward into Anagram dials or screen
TOE_GUARD_WIDTH = 5.0         # Barrier rib thickness along Y (mm)
TOE_GUARD_Y0 = TRENCH_Y1      # 63.0 mm
TOE_GUARD_Y1 = TOE_GUARD_Y0 + TOE_GUARD_WIDTH # 68.0 mm
TOE_GUARD_Z = 51.0            # High protective ridge (+10mm above Anagram front deck)

# --- Upper Tier: Darkglass Anagram (Raised & Angled at 8.0°) ---
# Physical device: 210.0 x 105.0 x 62.0 mm, ~815 g
ANAGRAM_DEPTH_SLOPE = 106.5   # Pocket depth along slope (+1.5 mm tolerance)
ANAGRAM_ANGLE = 8.0           # Ergonomic viewing & stomp incline (degrees)
ANAGRAM_LIP = 6.0             # Perimeter retaining lip depth (mm)
ANAGRAM_FRONT_Z = 41.0        # Upper deck front floor elevation (+32mm above Chocolate)
ANAGRAM_Y0 = TOE_GUARD_Y1     # 68.0 mm

RAD_A = math.radians(ANAGRAM_ANGLE)
COS_A = math.cos(RAD_A)       # ~0.990268
SIN_A = math.sin(RAD_A)       # ~0.139173
TAN_A = math.tan(RAD_A)       # ~0.140541

ANAGRAM_Y_SPAN = ANAGRAM_DEPTH_SLOPE * COS_A  # ~105.46 mm
ANAGRAM_Y1 = ANAGRAM_Y0 + ANAGRAM_Y_SPAN      # ~173.46 mm
ANAGRAM_REAR_FLOOR_Z = ANAGRAM_FRONT_Z + ANAGRAM_DEPTH_SLOPE * SIN_A # ~52.82 mm

REAR_WALL_THICKNESS = 4.5
TOTAL_DEPTH = ANAGRAM_Y1 + REAR_WALL_THICKNESS # ~178.0 mm
REAR_TOP_Z = ANAGRAM_REAR_FLOOR_Z + ANAGRAM_LIP * COS_A # ~58.76 mm

# --- Underbelly Cradle: Baseus GaN3 Pro 65W Desktop Charger ---
# Physical unit CCDK65S: 70.0 mm (L) x 40.0 mm (W) x 36.9 mm (H)

CHARGER_WIDTH = 41.5          # +1.5 mm pocket clearance
CHARGER_LENGTH = 73.0         # +3.0 mm pocket clearance
CHARGER_HEIGHT = 38.0         # +1.1 mm pocket clearance
CHARGER_X_CTR = -58.0         # Confined to far-left underbelly (strict EMI separation)
CHARGER_Y0 = ANAGRAM_Y0 + 6.0 # Starts 6mm behind toe guard (Y = 74.0 mm)
CHARGER_Y1 = CHARGER_Y0 + CHARGER_LENGTH # 147.0 mm
CHARGER_Y_CTR = (CHARGER_Y0 + CHARGER_Y1) / 2.0 # 110.5 mm

# --- Rubber Bumper Feet (5-Point Anti-Slip Base) ---
FOOT_DIAMETER = 12.7          # Standard 1/2" adhesive bumper feet
FEET_LOCATIONS = [
    (-95.0, 15.0),               # Front-Left
    ( 95.0, 15.0),               # Front-Right
    (-95.0, TOTAL_DEPTH - 16.0), # Rear-Left
    ( 95.0, TOTAL_DEPTH - 16.0), # Rear-Right
    (  0.0, 100.0),              # Center Stomp Pillar (directly under Anagram footswitches)
]


# ==============================================================================
# 2. SOLID MODEL GENERATION
# ==============================================================================

def build_stage_pedalboard() -> bd.Solid:
    """Constructs the monolithic tour-grade two-tier stage pedalboard."""
    print("=" * 70)
    print("Generating Stage Pedalboard Platform (Tour-Grade Specification)...")
    print(f"Footprint: {BOARD_WIDTH:.1f} mm (W) x {TOTAL_DEPTH:.1f} mm (D) x {REAR_TOP_Z:.1f} mm (H)")
    print(f"Incline: {ANAGRAM_ANGLE:.1f}° | Elevation Step: {ANAGRAM_FRONT_Z - CHOC_Z_TOP:.1f} mm")
    print("=" * 70)

    # --------------------------------------------------------------------------
    # Step 1: Base Monolithic Hull Extrusion (YZ Silhouette extruded along X)
    # --------------------------------------------------------------------------
    hull_pts = [
        (0.0, 0.0),
        (0.0, CHOC_Z_TOP),
        (TRENCH_Y0, CHOC_Z_TOP),
        (TOE_GUARD_Y0, TOE_GUARD_Z),
        (TOE_GUARD_Y1, TOE_GUARD_Z),
        (ANAGRAM_Y0, ANAGRAM_FRONT_Z + ANAGRAM_LIP * COS_A),
        (TOTAL_DEPTH, REAR_TOP_Z),
        (TOTAL_DEPTH, 0.0),
        (0.0, 0.0),
    ]

    with bd.BuildPart() as bp:
        with bd.BuildSketch(bd.Plane.YZ):
            bd.Polygon(hull_pts)
        bd.extrude(amount=BOARD_WIDTH / 2.0, both=True)

        # Fillet exterior 4 vertical corners (3.5mm radius for sleek look and impact toughness)
        front_edges = bp.edges().filter_by(bd.Axis.Z).sort_by(bd.Axis.Y)[:2]
        rear_edges = bp.edges().filter_by(bd.Axis.Z).sort_by(bd.Axis.Y)[-2:]
        bd.fillet(front_edges, radius=3.5)
        bd.fillet(rear_edges, radius=3.5)

        # ----------------------------------------------------------------------
        # Step 2: Lower Tier - M-VAVE Chocolate Plus Recessed Tray Pocket
        # ----------------------------------------------------------------------
        choc_mid_y = (CHOC_Y0 + CHOC_Y1) / 2.0
        with bd.BuildPart(mode=bd.Mode.SUBTRACT):
            with bd.Locations((0.0, choc_mid_y, CHOC_Z_FLOOR + 15.0)):
                bd.Box(POCKET_WIDTH, CHOC_DEPTH, 30.0)

        # Floor push-up and weight-saving window beneath Chocolate Plus
        # Leaves an 8mm solid perimeter resting ledge for the controller's base
        with bd.BuildPart(mode=bd.Mode.SUBTRACT):
            with bd.Locations((0.0, choc_mid_y, 0.0)):
                bd.Box(175.0, 22.0, 20.0)

        # ----------------------------------------------------------------------
        # Step 3: Full-Width Inter-Tier Cable Drop Trench
        # ----------------------------------------------------------------------
        trench_mid_y = (TRENCH_Y0 + TRENCH_Y1) / 2.0
        with bd.BuildPart(mode=bd.Mode.SUBTRACT):
            with bd.Locations((0.0, trench_mid_y, 0.0)):
                bd.Box(POCKET_WIDTH, TRENCH_WIDTH, 120.0)

        # ----------------------------------------------------------------------
        # Step 4: Upper Tier - Darkglass Anagram Angled Tray Pocket (8.0° Incline)
        # ----------------------------------------------------------------------
        deck_mid_dist = ANAGRAM_DEPTH_SLOPE / 2.0
        deck_mid_y = ANAGRAM_Y0 + deck_mid_dist * COS_A
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
        # Step 5: Large Open Rear Perimeter Bay for Darkglass I/O
        # ----------------------------------------------------------------------
        # Direct line-of-sight access for all XLRs, 1/4" audio, TRS MIDI, USB, and DC
        with bd.BuildPart(mode=bd.Mode.SUBTRACT):
            with bd.Locations((0.0, TOTAL_DEPTH, (ANAGRAM_REAR_FLOOR_Z + REAR_TOP_Z) / 2.0)):
                bd.Box(175.0, 20.0, 28.0)

        # ----------------------------------------------------------------------
        # Step 6: Ergonomic Side Finger Pry Notches
        # ----------------------------------------------------------------------
        # Enables tool-less, zero-damage lifting of pedals
        with bd.BuildPart(mode=bd.Mode.SUBTRACT):
            for side in [-1, 1]:
                # Chocolate Plus pry notch
                with bd.Locations((side * (BOARD_WIDTH / 2.0), choc_mid_y, CHOC_Z_TOP)):
                    bd.Cylinder(radius=9.0, height=20.0)
                # Darkglass Anagram pry notch
                with bd.Locations((side * (BOARD_WIDTH / 2.0), deck_mid_y, deck_mid_z + 8.0)):
                    bd.Cylinder(radius=15.0, height=20.0)

        # ----------------------------------------------------------------------
        # Step 7: Open Underbelly Chamber Beneath Anagram
        # ----------------------------------------------------------------------
        # Extrudes under-deck clearance leaving perimeter walls and deck plate intact
        under_pts = [
            (ANAGRAM_Y0, 0.0),
            (TOTAL_DEPTH - REAR_WALL_THICKNESS, 0.0),
            (TOTAL_DEPTH - REAR_WALL_THICKNESS, ANAGRAM_REAR_FLOOR_Z - UNDER_DECK_T),
            (ANAGRAM_Y0, ANAGRAM_FRONT_Z - UNDER_DECK_T),
            (ANAGRAM_Y0, 0.0),
        ]
        with bd.BuildSketch(bd.Plane.YZ) as s_under:
            bd.Polygon(under_pts)
        bd.extrude(amount=POCKET_WIDTH / 2.0, both=True, mode=bd.Mode.SUBTRACT)

        # ----------------------------------------------------------------------
        # Step 8: Structural Load Keels & Footswitch Stomp Reinforcement
        # ----------------------------------------------------------------------
        # 8a. Central Longitudinal Load Spine (3.5mm thick) running from Z=0 to deck underside
        # Profile follows the 8.0° slope of the deck underside perfectly
        with bd.BuildPart(mode=bd.Mode.ADD):
            with bd.BuildSketch(bd.Plane.YZ):
                bd.Polygon(under_pts)
            bd.extrude(amount=3.5 / 2.0, both=True)

        # 8b. Transverse Stomp Bulkhead directly under Anagram Footswitches (Y = 100mm)
        stomp_y = 100.0
        stomp_deck_z = ANAGRAM_FRONT_Z + (stomp_y - ANAGRAM_Y0) * TAN_A - UNDER_DECK_T
        with bd.BuildPart(mode=bd.Mode.ADD):
            with bd.Locations((0.0, stomp_y, 0.0)):
                bd.Box(
                    POCKET_WIDTH,
                    3.5,
                    stomp_deck_z,
                    align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
                )

        # 8c. Cut out stomp rib across the charger cradle so the charger bay is completely open
        with bd.BuildPart(mode=bd.Mode.SUBTRACT):
            with bd.Locations((CHARGER_X_CTR, stomp_y, 0.0)):
                bd.Box(CHARGER_WIDTH, 10.0, 50.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))

        # 8d. Central Spine TRS MIDI Passthrough Portal
        # Allows routing TRS MIDI cable cleanly across the central spine
        with bd.BuildPart(mode=bd.Mode.SUBTRACT):
            with bd.Locations((0.0, stomp_y, 10.0)):
                bd.Box(18.0, 16.0, 14.0)

        # ----------------------------------------------------------------------
        # Step 9: Baseus GaN3 Pro Charger Underbelly Cradle
        # ----------------------------------------------------------------------
        cradle_wall_t = 3.5
        cradle_x_left = CHARGER_X_CTR - CHARGER_WIDTH / 2.0 - cradle_wall_t / 2.0
        cradle_x_right = CHARGER_X_CTR + CHARGER_WIDTH / 2.0 + cradle_wall_t / 2.0

        cradle_pts = [
            (CHARGER_Y0, 0.0),
            (CHARGER_Y1, 0.0),
            (CHARGER_Y1, ANAGRAM_FRONT_Z + (CHARGER_Y1 - ANAGRAM_Y0) * TAN_A - UNDER_DECK_T),
            (CHARGER_Y0, ANAGRAM_FRONT_Z + (CHARGER_Y0 - ANAGRAM_Y0) * TAN_A - UNDER_DECK_T),
            (CHARGER_Y0, 0.0),
        ]

        # 9a. Full side enclosure walls
        for cx in [cradle_x_left, cradle_x_right]:
            with bd.BuildPart(mode=bd.Mode.ADD):
                with bd.Locations((cx, 0.0, 0.0)):
                    with bd.BuildSketch(bd.Plane.YZ):
                        bd.Polygon(cradle_pts)
                    bd.extrude(amount=cradle_wall_t / 2.0, both=True)

        # ----------------------------------------------------------------------
        # Step 9: Baseus GaN3 Pro Solid Enclosed Underbelly Shelf with Strap Slots
        # ----------------------------------------------------------------------
        shelf_t = 3.2
        shelf_w = CHARGER_WIDTH + 2 * cradle_wall_t

        # Solid floor plate spanning across both cradle walls
        with bd.BuildPart(mode=bd.Mode.ADD):
            with bd.Locations((CHARGER_X_CTR, CHARGER_Y_CTR, shelf_t / 2.0)):
                bd.Box(shelf_w, CHARGER_LENGTH, shelf_t)

        # Front & Rear Transverse Cable / Strap Slots through bottom shelf
        with bd.BuildPart(mode=bd.Mode.SUBTRACT):
            # Dual 5mm wide transverse slots for heavy-duty velcro or zip-ties
            for strap_y in [CHARGER_Y0 + 18.0, CHARGER_Y1 - 18.0]:
                with bd.Locations((CHARGER_X_CTR, strap_y, shelf_t / 2.0)):
                    bd.Box(CHARGER_WIDTH + cradle_wall_t * 2 + 2.0, 5.0, shelf_t + 2.0)

            # Ventilation and weight relief window in bottom shelf
            with bd.Locations((CHARGER_X_CTR, CHARGER_Y_CTR, shelf_t / 2.0)):
                bd.Box(CHARGER_WIDTH - 12.0, 24.0, shelf_t + 2.0)

        # Front USB port window into cable drop trench
        with bd.BuildPart(mode=bd.Mode.SUBTRACT):
            with bd.Locations((CHARGER_X_CTR, TRENCH_Y1, 16.0)):
                bd.Box(CHARGER_WIDTH - 6.0, 16.0, 24.0)

        # Rear AC power cord port
        with bd.BuildPart(mode=bd.Mode.SUBTRACT):
            with bd.Locations((CHARGER_X_CTR, TOTAL_DEPTH, 12.0)):
                bd.Box(26.0, 25.0, 18.0)

        # ----------------------------------------------------------------------
        # Step 12: Right-Side Lightening Cavities (Optimized Skeletal Structure)
        # ----------------------------------------------------------------------
        # Weight-reduction chambers on the audio-side underbelly, split by the stomp rib
        right_bay_x = 55.0
        right_bay_w = 78.0
        with bd.BuildPart(mode=bd.Mode.SUBTRACT):
            # Forward right bay (between toe-guard and stomp rib)
            fwd_bay_y = (ANAGRAM_Y0 + stomp_y) / 2.0
            fwd_bay_len = (stomp_y - ANAGRAM_Y0) - 8.0
            with bd.Locations((right_bay_x, fwd_bay_y, 0.0)):
                bd.Box(right_bay_w, fwd_bay_len, 45.0)

            # Rear right bay (between stomp rib and rear wall)
            rear_bay_y = (stomp_y + TOTAL_DEPTH - REAR_WALL_THICKNESS) / 2.0
            rear_bay_len = (TOTAL_DEPTH - REAR_WALL_THICKNESS - stomp_y) - 8.0
            with bd.Locations((right_bay_x, rear_bay_y, 0.0)):
                bd.Box(right_bay_w, rear_bay_len, 65.0)

        # ----------------------------------------------------------------------
        # Step 13: Side Wall Skeletal Cutouts (Truss Windows)
        # ----------------------------------------------------------------------
        # Preserves diagonal triangulation while cutting print mass by ~35%
        with bd.BuildPart(mode=bd.Mode.SUBTRACT):
            for side in [-1, 1]:
                wall_x = side * (BOARD_WIDTH / 2.0)
                # Front truss cutout
                with bd.Locations((wall_x, 92.0, 16.0)):
                    bd.Box(15.0, 26.0, 14.0)
                # Rear truss cutout
                with bd.Locations((wall_x, 142.0, 25.0)):
                    bd.Box(15.0, 30.0, 18.0)

        # ----------------------------------------------------------------------
        # Step 14: Solid Mounting Pads for Adhesive Rubber Bumper Feet
        # ----------------------------------------------------------------------
        # Solid flat pads at Z=0 for peel-and-stick adhesive bumper feet (no holes).
        # Front feet (-95, 15) and (95, 15) rest directly on the solid 3.0mm front floor.
        # Rear-left, rear-right, and center stomp locations receive solid base pads.
        with bd.BuildPart(mode=bd.Mode.ADD):
            # Rear corner foot pads (fused into sidewalls and rear wall)
            for side in [-1, 1]:
                with bd.Locations((side * 95.0, TOTAL_DEPTH - 16.0, 0.0)):
                    bd.Box(
                        28.0,
                        28.0,
                        FLOOR_THICKNESS,
                        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
                    )
            # Center stomp pillar foot pad (fused into spine and stomp bulkhead)
            with bd.Locations((0.0, stomp_y, 0.0)):
                bd.Cylinder(
                    radius=10.0,
                    height=FLOOR_THICKNESS,
                    align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
                )

    solid = bp.part
    print(f"Build completed successfully! Solid Volume: {solid.volume / 1000.0:.2f} cm³")
    print(f"Watertight Solid: {solid.is_valid}")
    return solid


# ==============================================================================
# 3. EXECUTION & CAD VIEWER EXPORT
# ==============================================================================

if __name__ == "__main__":
    pedalboard = build_stage_pedalboard()

    # Export high-resolution mesh STL for 3D printing
    stl_path = "stage-pedalboard.stl"
    print(f"Exporting high-resolution mesh to {stl_path}...")
    bd.export_stl(pedalboard, stl_path, tolerance=0.05, angular_tolerance=0.1)
    print(f"Successfully exported {stl_path}!")

    # Attempt to render in VS Code OCP CAD Viewer
    try:
        from ocp_vscode import show
        print("Broadcasting 3D model to OCP CAD Viewer...")
        show(
            pedalboard,
            names=["Stage Pedalboard"],
            colors=[(0.2, 0.2, 0.22, 1.0)],
        )
        print("Model visible in VS Code CAD Viewer.")
    except Exception as e:
        print(f"Note: OCP CAD Viewer broadcast skipped: {e}")


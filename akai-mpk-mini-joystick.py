"""
Akai MPK Mini MK2 Replacement Joystick Generator (build123d)
============================================================
Parametric 3D printable replacement for the red 4-way pitch bend & modulation
thumbstick on the Akai MPK Mini MK2 (also compatible with MK3 / MPK Mini Play).

Models the authentic low-profile mushroom thumbstick geometry:
- Hollow convex hemispherical dome skirt (clears the gimbal housing while
  sealing the chassis bezel opening through +/-25 deg travel)
- Short, stout cylindrical waist/neck
- Ergonomic rounded mushroom head with a smooth concave thumb dish
- Flush contoured center plug (replaces the OEM rubber screw cover)

Includes multiple mounting variants for different failure modes:
1. OEM Screw Mount (Drop-in factory replacement, uses central M2 screw)
2. Repair Sleeve Mount (Reinforced deep socket to sleeve over a snapped stub)
3. Square Stem Press-Fit (Seamless solid top, 3.4x3.4 mm socket for bare Alps gimbals)
4. Contoured Top Plug (Flush snap-in cover matching the concave dish curvature)
5. Chassis Blanking Cover (Snap-in dust cover to blank off the bezel gap if unused)

Target Printer: Bambu Lab A1 (0.4mm nozzle, PETG or Tough PLA, 0.12mm layer height)
"""

import os
import math
from build123d import *
from ocp_vscode import *


def _dish_sphere_z(r: float, total_height: float, dish_depth: float, dish_radius: float) -> float:
    """Returns Z height on the concave dish sphere at radial distance r."""
    z_center = total_height - dish_depth + dish_radius
    return z_center - math.sqrt(max(dish_radius**2 - r**2, 0.0))


def build_joystick(
    variant: str = "oem",
    total_height: float = 12.4,
    dome_radius: float = 8.2,
    dome_center_z: float = -1.2,
    dome_wall: float = 1.6,
    neck_dia: float = 5.8,
    head_dia: float = 12.6,
    head_rim_z: float = 10.75,
    dish_depth: float = 0.65,
    dish_radius: float = 20.0,
    screw_hole_dia: float = 2.2,
    screw_head_dia: float = 4.1,
    screw_head_depth: float = 2.0,
    plug_recess_dia: float = 5.0,
    plug_recess_depth: float = 0.85,
    bottom_socket_dia: float = 3.8,
    bottom_socket_depth: float = 3.5,
    sleeve_inner_dia: float = 4.3,
    sleeve_depth: float = 6.5,
    square_shaft_size: float = 3.4,
) -> Part:
    """Builds a parametric mushroom thumbstick cap for the specified mounting variant."""
    # Slightly thicker neck wall for the repair sleeve variant to maximize hoop strength
    neck_r = (neck_dia + 0.8) / 2.0 if variant == "repair_sleeve" else neck_dia / 2.0
    head_r = head_dia / 2.0

    # Base of the convex dome at Z = 0
    r_base = math.sqrt(dome_radius**2 - dome_center_z**2)
    z_dome_top = 4.7
    r_dome_top = math.sqrt(dome_radius**2 - (z_dome_top - dome_center_z) ** 2)

    # Sphere tangent vector pointing upward-inward at (r_dome_top, z_dome_top)
    tx_dome = -(z_dome_top - dome_center_z) / dome_radius
    tz_dome = r_dome_top / dome_radius

    ang_b = math.asin(-dome_center_z / dome_radius)
    ang_t = math.asin((z_dome_top - dome_center_z) / dome_radius)
    ang_m = (ang_b + ang_t) / 2.0

    # Outer edge of the concave dish where the rounded rim meets the dish
    dish_outer_r = head_r - 1.35
    z_dish_outer = _dish_sphere_z(dish_outer_r, total_height, dish_depth, dish_radius)
    z_dish_center = total_height - dish_depth

    # Dish midpoint for exact spherical ThreePointArc
    dish_mid_r = dish_outer_r * 0.5
    z_dish_mid = _dish_sphere_z(dish_mid_r, total_height, dish_depth, dish_radius)

    # Inward tangent along the dish at dish_outer_r so the rounded rim blends smoothly
    dz_dr_dish = dish_outer_r / math.sqrt(dish_radius**2 - dish_outer_r**2)
    rim_inward_tx = -1.0
    rim_inward_tz = -dz_dr_dish

    with BuildPart() as joystick:
        # 1. Outer revolved mushroom thumbstick body
        with BuildSketch(Plane.XZ) as profile_sketch:
            with BuildLine():
                Line((0, 0), (r_base, 0))
                # Convex spherical dust dome skirt
                ThreePointArc(
                    (r_base, 0),
                    (
                        dome_radius * math.cos(ang_m),
                        dome_radius * math.sin(ang_m) + dome_center_z,
                    ),
                    (r_dome_top, z_dome_top),
                )
                # Smooth tangent blend from dome into vertical neck waist
                Spline(
                    (r_dome_top, z_dome_top),
                    (neck_r + 1.0, 5.55),
                    (neck_r, 6.7),
                    tangents=[(tx_dome, tz_dome), (0, 1)],
                )
                # Short neck waist
                Line((neck_r, 6.7), (neck_r, 8.2))
                # Mushroom cap underside flare out to widest perimeter
                Spline(
                    (neck_r, 8.2),
                    (neck_r + 1.35, 9.15),
                    (head_r - 0.45, 9.85),
                    (head_r, head_rim_z),
                    tangents=[(0, 1), (0, 1)],
                )
                # Smooth rounded outer lip meeting the concave thumb dish tangentially
                Spline(
                    (head_r, head_rim_z),
                    (head_r - 0.25, 11.75),
                    (dish_outer_r, z_dish_outer),
                    tangents=[(0, 1), (rim_inward_tx, rim_inward_tz)],
                )
                # Smooth concave thumb dish to center
                ThreePointArc(
                    (dish_outer_r, z_dish_outer),
                    (dish_mid_r, z_dish_mid),
                    (0, z_dish_center),
                )
                Line((0, z_dish_center), (0, 0))
            make_face()
        revolve(axis=Axis.Z)

        # 2. Hollow dome underside (clears the gimbal housing while preserving central stem)
        inner_dome_r = dome_radius - dome_wall
        z_cav_top = math.sqrt(inner_dome_r**2 - neck_r**2) + dome_center_z
        r_cav_base = math.sqrt(inner_dome_r**2 - dome_center_z**2)
        ang_cb = math.asin(-dome_center_z / inner_dome_r)
        ang_ct = math.acos(neck_r / inner_dome_r)
        ang_cm = (ang_cb + ang_ct) / 2.0

        with BuildSketch(Plane.XZ) as cav_sketch:
            with BuildLine():
                Line((neck_r, 0), (r_cav_base, 0))
                ThreePointArc(
                    (r_cav_base, 0),
                    (
                        inner_dome_r * math.cos(ang_cm),
                        inner_dome_r * math.sin(ang_cm) + dome_center_z,
                    ),
                    (neck_r, z_cav_top),
                )
                Line((neck_r, z_cav_top), (neck_r, 0))
            make_face()
        revolve(axis=Axis.Z, mode=Mode.SUBTRACT)

        # 3. Top screw counterbore & plug recess (omitted on solid-top square_stem)
        if variant in ("oem", "repair_sleeve"):
            # Plug recess measured from dish center downward
            with Locations((0, 0, z_dish_center + 0.5)):
                Cylinder(
                    radius=plug_recess_dia / 2.0,
                    height=(plug_recess_depth + 0.5) * 2,
                    mode=Mode.SUBTRACT,
                )
            # Screw head pocket below the plug recess
            with Locations((0, 0, z_dish_center - plug_recess_depth)):
                Cylinder(
                    radius=screw_head_dia / 2.0,
                    height=screw_head_depth * 2,
                    mode=Mode.SUBTRACT,
                )
            # Central M2 screw through-hole
            with Locations((0, 0, 0)):
                Cylinder(
                    radius=screw_hole_dia / 2.0,
                    height=total_height * 3,
                    mode=Mode.SUBTRACT,
                )

        # 4. Bottom shaft mounting socket
        if variant == "oem":
            with Locations((0, 0, 0)):
                Cylinder(
                    radius=bottom_socket_dia / 2.0,
                    height=bottom_socket_depth * 2,
                    mode=Mode.SUBTRACT,
                )
        elif variant == "repair_sleeve":
            with Locations((0, 0, 0)):
                Cylinder(
                    radius=sleeve_inner_dia / 2.0,
                    height=sleeve_depth * 2,
                    mode=Mode.SUBTRACT,
                )
        elif variant == "square_stem":
            with Locations((0, 0, 0)):
                Box(
                    square_shaft_size,
                    square_shaft_size,
                    6.0 * 2,
                    mode=Mode.SUBTRACT,
                )

    return joystick.part


def build_top_plug(
    plug_dia: float = 4.8,
    plug_depth: float = 0.85,
    total_height: float = 12.4,
    dish_depth: float = 0.65,
    dish_radius: float = 20.0,
) -> Part:
    """Builds a contoured snap-in cap whose top matches the joystick concave dish."""
    z_dish_center = total_height - dish_depth
    z_bottom = z_dish_center - plug_depth
    r_plug = plug_dia / 2.0
    z_edge = _dish_sphere_z(r_plug, total_height, dish_depth, dish_radius)
    z_mid = _dish_sphere_z(r_plug * 0.5, total_height, dish_depth, dish_radius)

    with BuildPart() as plug:
        with BuildSketch(Plane.XZ):
            with BuildLine():
                Line((0, 0), (r_plug - 0.15, 0))
                # Small lead-in chamfer at bottom of plug
                Line((r_plug - 0.15, 0), (r_plug, 0.2))
                Line((r_plug, 0.2), (r_plug, z_edge - z_bottom))
                # Exact concave dish top contour shifted to plug local Z=0
                ThreePointArc(
                    (r_plug, z_edge - z_bottom),
                    (r_plug * 0.5, z_mid - z_bottom),
                    (0, z_dish_center - z_bottom),
                )
                Line((0, z_dish_center - z_bottom), (0, 0))
            make_face()
        revolve(axis=Axis.Z)

    return plug.part


def build_blanking_cover(
    cover_outer_dia: float = 18.0,
    cover_above_panel: float = 2.2,
    roof_thickness: float = 1.1,
    hole_dia: float = 14.8,
    panel_thickness: float = 1.8,
    tab_wall: float = 1.1,
    tab_length: float = 3.8,
    detent_protrusion: float = 0.28,
    num_tabs: int = 4,
    slot_width: float = 2.2,
) -> Part:
    """Builds a snap-in blanking cover to seal the joystick gap if unused.

    Oriented upside-down (exposed top face flat at Z = 0) so it prints directly
    on the build plate with zero supports. Hollow interior leaves clearance over
    any remaining internal gimbal stub so it cannot deflect the potentiometer.
    """
    r_outer = cover_outer_dia / 2.0
    r_hole = hole_dia / 2.0
    r_barrel = r_hole - 0.12
    r_inner = r_barrel - tab_wall
    r_detent = r_hole + detent_protrusion

    z_flange_top = cover_above_panel
    z_detent_start = z_flange_top + panel_thickness - 0.15
    z_detent_peak = z_detent_start + (r_detent - r_barrel) + 0.15
    z_tip = z_flange_top + tab_length

    with BuildPart() as cover:
        # 1. Revolved cap flange + hollow snap-tab barrel
        with BuildSketch(Plane.XZ):
            with BuildLine():
                # Flat top face on build plate (Z = 0)
                Line((0, 0), (r_outer - 0.8, 0))
                # Soft rounded outer lip up to chassis seating plane
                Spline(
                    (r_outer - 0.8, 0),
                    (r_outer - 0.15, cover_above_panel * 0.35),
                    (r_outer, z_flange_top),
                    tangents=[(1, 0), (0, 1)],
                )
                # Chassis seating underside inward to barrel wall
                Line((r_outer, z_flange_top), (r_barrel, z_flange_top))
                Line((r_barrel, z_flange_top), (r_barrel, z_detent_start))
                # ~45-deg self-supporting ramp to snap detent peak, then insertion lead-in
                Line((r_barrel, z_detent_start), (r_detent, z_detent_peak))
                Line((r_detent, z_detent_peak), (r_barrel - 0.25, z_tip))
                # Tab tip flat inward to hollow interior wall
                Line((r_barrel - 0.25, z_tip), (r_inner, z_tip))
                # Deep hollow interior clearing broken gimbal stubs
                Line((r_inner, z_tip), (r_inner, roof_thickness + 0.5))
                Spline(
                    (r_inner, roof_thickness + 0.5),
                    (r_inner * 0.65, roof_thickness),
                    (0, roof_thickness),
                    tangents=[(0, -1), (-1, 0)],
                )
                Line((0, roof_thickness), (0, 0))
            make_face()
        revolve(axis=Axis.Z)

        # 2. Radial compliance slots dividing the barrel into flexible snap tabs
        with BuildSketch(Plane.XY.offset(z_flange_top + 0.15)):
            with PolarLocations(
                radius=(r_inner + r_detent) / 2.0,
                count=num_tabs,
                start_angle=45,
            ):
                Rectangle(r_detent - r_inner + 2.0, slot_width)
        extrude(amount=tab_length + 1.0, mode=Mode.SUBTRACT)

    return cover.part


if __name__ == "__main__":
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "builds")
    os.makedirs(output_dir, exist_ok=True)

    # 1. OEM Screw Mount variant
    joystick_oem = build_joystick(variant="oem")
    stl_oem = os.path.join(output_dir, "akai_mpk_mini_joystick_oem.stl")
    export_stl(joystick_oem, stl_oem)
    print(f"Exported OEM variant: {stl_oem} (Volume: {joystick_oem.volume:.2f} mm³)")

    # 2. Snapped Stem Repair Sleeve variant
    joystick_sleeve = build_joystick(variant="repair_sleeve")
    stl_sleeve = os.path.join(output_dir, "akai_mpk_mini_joystick_repair_sleeve.stl")
    export_stl(joystick_sleeve, stl_sleeve)
    print(f"Exported Sleeve variant: {stl_sleeve} (Volume: {joystick_sleeve.volume:.2f} mm³)")

    # 3. Universal Square Stem Press-Fit variant (solid seamless top)
    joystick_square = build_joystick(variant="square_stem")
    stl_square = os.path.join(output_dir, "akai_mpk_mini_joystick_square_stem.stl")
    export_stl(joystick_square, stl_square)
    print(f"Exported Square Stem variant: {stl_square} (Volume: {joystick_square.volume:.2f} mm³)")

    # 4. Contoured Top Plug
    top_plug = build_top_plug()
    stl_plug = os.path.join(output_dir, "akai_mpk_mini_joystick_top_plug.stl")
    export_stl(top_plug, stl_plug)
    print(f"Exported Top Plug: {stl_plug} (Volume: {top_plug.volume:.2f} mm³)")

    # 5. Chassis Blanking Cover (fill the gap if joystick is unused)
    blanking_cover = build_blanking_cover()
    stl_cover = os.path.join(output_dir, "akai_mpk_mini_joystick_cover.stl")
    export_stl(blanking_cover, stl_cover)
    print(f"Exported Blanking Cover: {stl_cover} (Volume: {blanking_cover.volume:.2f} mm³)")

    # Display OEM part in OCP viewer if active
    try:
        show(joystick_oem)
    except Exception:
        pass

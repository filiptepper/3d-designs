"""
Akai MPK Mini MK2 Replacement Joystick Generator (build123d)
============================================================
Parametric 3D printable replacement for the red 4-way pitch bend & modulation
thumbstick on the Akai MPK Mini MK2 (and MK3 / MPK Mini Play).

Includes multiple variants to address different failure modes:
1. OEM Screw Mount (Drop-in factory replacement, uses central M2 screw)
2. Repair Sleeve Mount (Reinforced deep socket to sleeve over a snapped stub)
3. Square Stem Press-Fit (Direct friction fit on standard 3.4x3.4mm Alps gimbals)
4. Snap-In Top Plug (Printable cosmetic cover for the screw counterbore)

Target Printer: Bambu Lab A1 (0.4mm nozzle, PETG or Tough PLA, 0.12mm layer height)
"""

import os
from build123d import *
from ocp_vscode import *


def build_joystick(
    variant: str = "oem",
    total_height: float = 14.5,
    skirt_dia: float = 15.2,
    skirt_height: float = 4.0,
    neck_dia: float = 6.8,
    head_dia: float = 12.0,
    head_height: float = 3.5,
    dish_depth: float = 0.8,
    screw_hole_dia: float = 2.2,
    screw_head_dia: float = 4.6,
    screw_head_depth: float = 2.2,
    plug_recess_dia: float = 5.4,
    plug_recess_depth: float = 1.0,
    bottom_socket_dia: float = 4.0,
    bottom_socket_depth: float = 3.5,
    sleeve_inner_dia: float = 4.3,
    sleeve_depth: float = 6.5,
    square_shaft_size: float = 3.4,
) -> Part:
    """Builds a parametric joystick cap for the specified mounting variant."""
    # For the repair sleeve variant, slightly beef up the neck for hoop strength
    effective_neck_dia = neck_dia + 0.8 if variant == "repair_sleeve" else neck_dia

    with BuildPart() as joystick:
        # 1. Outer profile (revolved along Z-axis)
        with BuildSketch(Plane.XZ) as profile_sketch:
            with BuildLine():
                r_base = skirt_dia / 2.0
                r_neck = effective_neck_dia / 2.0
                r_head = head_dia / 2.0

                # Base seating face
                Line((0, 0), (r_base - 1.0, 0))
                # Spherical / curved dust skirt contour
                Line((r_base - 1.0, 0), (r_base, 1.4))
                RadiusArc(
                    (r_base, 1.4),
                    (r_neck + 0.6, skirt_height),
                    radius=skirt_dia / 2.0,
                )
                # Neck column
                Line(
                    (r_neck + 0.6, skirt_height),
                    (r_neck, total_height - head_height),
                )
                # Flaring transition into ergonomic thumb dish
                RadiusArc(
                    (r_neck, total_height - head_height),
                    (r_head, total_height - 1.0),
                    radius=6.0,
                )
                # Outer head rim
                Line((r_head, total_height - 1.0), (r_head, total_height - 0.4))
                # Top perimeter chamfer
                Line(
                    (r_head, total_height - 0.4),
                    (r_head - 0.4, total_height),
                )
                # Top face to central axis
                Line((r_head - 0.4, total_height), (0, total_height))
                # Axis of rotation
                Line((0, total_height), (0, 0))
            make_face()
        revolve(axis=Axis.Z)

        # 2. Ergonomic concave thumb depression on the crown
        with Locations((0, 0, total_height + 15.0 - dish_depth)):
            Sphere(radius=15.0, mode=Mode.SUBTRACT)

        # 3. Concentric non-slip traction rings on the thumbpad
        for r_ring in [2.9, 4.1, 5.1]:
            with Locations((0, 0, total_height - 0.35)):
                Torus(major_radius=r_ring, minor_radius=0.22, mode=Mode.ADD)

        # 4. Internal mounting geometry based on failure mode variant
        # Common top cavities: cosmetic plug recess and screw head counterbore
        with Locations((0, 0, total_height)):
            Cylinder(
                radius=plug_recess_dia / 2.0,
                height=plug_recess_depth * 2,
                mode=Mode.SUBTRACT,
            )
        with Locations((0, 0, total_height - plug_recess_depth)):
            Cylinder(
                radius=screw_head_dia / 2.0,
                height=screw_head_depth * 2,
                mode=Mode.SUBTRACT,
            )

        # Central through-hole for M2 screw
        with Locations((0, 0, 0)):
            Cylinder(
                radius=screw_hole_dia / 2.0,
                height=total_height * 3,
                mode=Mode.SUBTRACT,
            )

        # Bottom interface specific to variant
        if variant == "oem":
            # OEM bottom counterbore to mate with the original gimbal shoulder
            with Locations((0, 0, 0)):
                Cylinder(
                    radius=bottom_socket_dia / 2.0,
                    height=bottom_socket_depth * 2,
                    mode=Mode.SUBTRACT,
                )

        elif variant == "repair_sleeve":
            # Deep reinforced socket to sleeve over a remaining snapped stub
            with Locations((0, 0, 0)):
                Cylinder(
                    radius=sleeve_inner_dia / 2.0,
                    height=sleeve_depth * 2,
                    mode=Mode.SUBTRACT,
                )

        elif variant == "square_stem":
            # Standard square socket (3.4 x 3.4 mm) for generic Alps potentiometer shafts
            with Locations((0, 0, 0)):
                Box(
                    square_shaft_size,
                    square_shaft_size,
                    6.0 * 2,
                    mode=Mode.SUBTRACT,
                )

    return joystick.part


def build_top_plug(
    cap_dia: float = 5.2,
    cap_thickness: float = 1.0,
    peg_dia: float = 4.4,
    peg_height: float = 1.2,
) -> Part:
    """Builds a small flush snap-in cap to conceal the screw head."""
    with BuildPart() as plug:
        # Outer cap disc
        Cylinder(
            radius=cap_dia / 2.0,
            height=cap_thickness,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        )
        # Underside friction peg
        with Locations((0, 0, cap_thickness)):
            Cylinder(
                radius=peg_dia / 2.0,
                height=peg_height,
                align=(Align.CENTER, Align.CENTER, Align.MIN),
            )
        # Chamfer the bottom lead-in edge for easy press-in
        chamfer(plug.edges().sort_by(Axis.Z)[-1], length=0.3)
        # Soft fillet on the exposed top edge
        fillet(plug.edges().sort_by(Axis.Z)[0], radius=0.25)

    return plug.part


if __name__ == "__main__":
    output_dir = os.path.dirname(os.path.abspath(__file__))

    # 1. Generate OEM Screw Mount variant
    joystick_oem = build_joystick(variant="oem")
    stl_oem = os.path.join(output_dir, "akai_mpk_mini_joystick_oem.stl")
    export_stl(joystick_oem, stl_oem)
    print(f"Exported OEM variant: {stl_oem} (Volume: {joystick_oem.volume:.2f} mm³)")

    # 2. Generate Snapped Stem Repair Sleeve variant
    joystick_sleeve = build_joystick(variant="repair_sleeve")
    stl_sleeve = os.path.join(output_dir, "akai_mpk_mini_joystick_repair_sleeve.stl")
    export_stl(joystick_sleeve, stl_sleeve)
    print(f"Exported Sleeve variant: {stl_sleeve} (Volume: {joystick_sleeve.volume:.2f} mm³)")

    # 3. Generate Square Stem Press-Fit variant
    joystick_square = build_joystick(variant="square_stem")
    stl_square = os.path.join(output_dir, "akai_mpk_mini_joystick_square_stem.stl")
    export_stl(joystick_square, stl_square)
    print(f"Exported Square Stem variant: {stl_square} (Volume: {joystick_square.volume:.2f} mm³)")

    # 4. Generate Cosmetic Top Plug
    top_plug = build_top_plug()
    stl_plug = os.path.join(output_dir, "akai_mpk_mini_joystick_top_plug.stl")
    export_stl(top_plug, stl_plug)
    print(f"Exported Top Plug: {stl_plug} (Volume: {top_plug.volume:.2f} mm³)")

    # Display OEM part in OCP viewer if active
    try:
        show(joystick_oem)
    except Exception:
        pass

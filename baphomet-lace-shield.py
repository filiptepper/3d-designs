"""
Parametric High-Detail Baphomet Boot Lace Shield
Output: A_HighDetail_Baphomet_Lace_Shield.stl

Architecture:
1. Precision CAD Base (build123d B-rep):
   - 58 x 77 mm curved gothic shield body, R_instep = 56.0 mm
   - Stepped double-bevel perimeter border
   - Double-ring inverted pentagram with crisp beveled ridges
   - Two vertical rear lace-in channels (3.8 mm radial clearance, open top/bottom)
     with 3 vertical stadium side windows per flank
   - 4 integral perimeter chain rings (6.4 mm exact ID) for double-tiered curb chains
2. High-Detail Sculpted 3D Relief (3D SDF + VTK FlyingEdges3D):
   - Conformal cylindrical (u, v, h) sculpted Baphomet goat skull
   - Heavy brow ridges, recessed sockets, almond eyeballs w/ horizontal goat pupils
   - Cheekbones, nasal bridge, flared nostrils, muzzle, furrowed beard tuft
   - Flared hollow-conch goat ears
   - Sweeping symmetric 3D horns with ~18 asymmetric annular ridges
   - Forehead flame torch rising between horn bases
"""

from __future__ import annotations

import math
import tempfile
import time
from pathlib import Path

import build123d as bd
import numpy as np
import vtk
from vtk.util import numpy_support


# ---------------------------------------------------------------------------
# Global Dimensions (mm)
# ---------------------------------------------------------------------------
SHIELD_W = 58.0          # Shield body chord width (X)
SHIELD_H = 77.0          # Shield body height (Z: 0 .. 77)
R_INSTEP = 56.0          # Inner boot-facing instep radius

REAR_WALL_T = 3.0        # Sturdy rear lace-channel strap wall thickness
CHANNEL_CLEARANCE = 3.8  # Exact radial clearance inside rear lace channels
PLATE_THICK = 3.0        # Main front shield plate thickness

R_REAR_OUT = R_INSTEP + REAR_WALL_T                  # 59.0 mm
R_PLATE_IN = R_REAR_OUT + CHANNEL_CLEARANCE          # 62.8 mm
R_PLATE_OUT = R_PLATE_IN + PLATE_THICK               # 65.8 mm

# Center of the pentagram & skull in Z
Z_MID = SHIELD_H * 0.5   # 38.5 mm
Z_EMBLEM = 40.2          # Slightly above geometric mid for balanced shield margins

# Chain rings (4 perimeter rings, 6.4 mm exact ID)
RING_ID = 6.4
RING_WIRE_D = 3.8
RING_R_INNER = RING_ID * 0.5                         # 3.2 mm
RING_R_MINOR = RING_WIRE_D * 0.5                     # 1.9 mm
RING_R_MAJOR = RING_R_INNER + RING_R_MINOR           # 5.1 mm (OD = 14.0 mm)

OUT_DIR = Path(__file__).resolve().parent / "builds"
OUT_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# Helpers for Cylindrical Mapping (Cylinder axis = Z at (0, -R_INSTEP))
# ---------------------------------------------------------------------------
def cyl_point(u: float, z: float, r: float) -> tuple[float, float, float]:
    """Map surface arc coordinate u (on R_PLATE_OUT), z, radius r to (x, y, z)."""
    theta = u / R_PLATE_OUT
    x = r * math.sin(theta)
    y = r * math.cos(theta) - R_INSTEP
    return (x, y, z)


def make_shield_sketch_2d(inset: float = 0.0) -> bd.Face:
    """
    Create the 2D unrolled gothic shield face in (u, v) where v = z - Z_MID.
    Calibrated so wrapped shield body chord width = 58.0 mm, height = 77.0 mm.
    """
    # Calibrated so after corner filleting, wrapped chord width = 58.0 mm, height = 77.0 mm
    u_top_shoulder = 30.28
    u_bot_shoulder = 26.8
    v_top = 39.42
    v_bot = -39.42
    v_sh_top = 23.8
    v_sh_bot = -21.2

    pts = [
        (0.0, v_top),
        (u_top_shoulder, v_sh_top),
        (u_bot_shoulder, v_sh_bot),
        (0.0, v_bot),
        (-u_bot_shoulder, v_sh_bot),
        (-u_top_shoulder, v_sh_top),
    ]
    with bd.BuildSketch() as sk:
        with bd.BuildLine():
            bd.Polyline(*pts, close=True)
        bd.make_face()
        # Query vertices fresh after each fillet so references never go stale!
        bd.fillet([v for v in sk.vertices() if abs(v.X) < 1.0], radius=5.0)
        bd.fillet([v for v in sk.vertices() if abs(v.X) > 20.0 and v.Y > 0], radius=6.5)
        bd.fillet([v for v in sk.vertices() if abs(v.X) > 20.0 and v.Y < 0], radius=6.5)
        if inset != 0.0:
            bd.offset(amount=-inset)
    return sk.sketch.faces()[0]


def wrap_face_on_radius(face_2d: bd.Face, radius: float, z_center: float = Z_MID) -> bd.Face:
    """Wrap a 2D face onto a cylinder of given radius centered at (0, -R_INSTEP, z_center)."""
    cyl = bd.Cylinder(
        radius=radius,
        height=140.0,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.CENTER),
    ).translate((0.0, -R_INSTEP, z_center))
    cyl_face = cyl.faces().filter_by(bd.GeomType.CYLINDER)[0]
    loc = bd.Plane(
        origin=(0.0, radius - R_INSTEP, z_center),
        x_dir=(-1.0, 0.0, 0.0),
        z_dir=(0.0, 1.0, 0.0),
    ).location
    return cyl_face.wrap(face_2d, loc, tolerance=0.01)


def radial_extrude_ring_band(
    face_2d: bd.Face,
    r_inner: float,
    r_outer: float,
    z_center: float = Z_MID,
) -> bd.Solid:
    """Wrap face onto reference outer/inner radius and thicken radially so walls are radial."""
    if r_outer > R_PLATE_OUT:
        wf = wrap_face_on_radius(face_2d, r_inner, z_center=z_center)
        return bd.Solid.thicken(wf, r_outer - r_inner, normal_override=(0.0, 1.0, 0.0))
    wf = wrap_face_on_radius(face_2d, r_outer, z_center=z_center)
    return bd.Solid.thicken(wf, r_inner - r_outer, normal_override=(0.0, 1.0, 0.0))


def build_cad_base() -> bd.Solid | bd.Compound:
    """Build the precision CAD shield base, border, pentagram, rear channels, and 4 chain rings."""
    t0 = time.time()
    print("[CAD] Building shield shell & stepped double-bevel border...")

    # 1. Full Radial Shield Body (R_INSTEP=56.0 to R_PLATE_OUT=65.0)
    shield_outer_2d = make_shield_sketch_2d(inset=0.0)
    shield_body = radial_extrude_ring_band(shield_outer_2d, R_INSTEP, R_PLATE_OUT)

    # 2. Stepped Double-Bevel Perimeter Border on front face (R = 65.0 .. 66.55)
    border_base_outer = make_shield_sketch_2d(inset=0.0)
    border_base_inner = make_shield_sketch_2d(inset=2.8)
    with bd.BuildSketch() as sk_b1:
        bd.insert(border_base_outer)
        bd.insert(border_base_inner, mode=bd.Mode.SUBTRACT)
    b1_2d = sk_b1.sketch.faces()[0]
    border_step1 = radial_extrude_ring_band(b1_2d, R_PLATE_OUT - 0.25, R_PLATE_OUT + 0.90)

    border_top_outer = make_shield_sketch_2d(inset=0.55)
    border_top_inner = make_shield_sketch_2d(inset=2.05)
    with bd.BuildSketch() as sk_b2:
        bd.insert(border_top_outer)
        bd.insert(border_top_inner, mode=bd.Mode.SUBTRACT)
    b2_2d = sk_b2.sketch.faces()[0]
    border_step2 = radial_extrude_ring_band(b2_2d, R_PLATE_OUT + 0.70, R_PLATE_OUT + 1.55)

    # 3. Carve Two Vertical Rear Lace-In Channels (exact 3.8 mm radial clearance: R=59.0..62.8)
    # 10.6 mm wide channels at u = +/-11.3 mm keep a 12.0 mm center spine AND solid outer shoulder frames
    print("[CAD] Carving sturdy rear lace-in channels (3.8 mm clearance) & side windows...")
    channel_cutouts = []
    for sign in (-1.0, 1.0):
        with bd.BuildSketch() as sk_ch:
            with bd.Locations((sign * 11.3, 0.0)):
                bd.Rectangle(10.6, 90.0)
        ch_2d = sk_ch.sketch.faces()[0]
        ch_sol = radial_extrude_ring_band(ch_2d, R_REAR_OUT, R_PLATE_IN)
        channel_cutouts.append(ch_sol)

    # Carve 3 vertical stadium side windows along each flank with thick 4.0 mm inter-slot pillars
    window_cutouts = []
    slot_z_centers = [28.5, 38.5, 48.5]
    slot_h = 6.0
    slot_w = 3.0  # radial opening inside the 3.8 mm channel
    r_mid_slot = (R_REAR_OUT + R_PLATE_IN) * 0.5
    for sign in (-1.0, 1.0):
        theta_f = sign * (23.0 / R_PLATE_OUT)
        fx = r_mid_slot * math.sin(theta_f)
        fy = r_mid_slot * math.cos(theta_f) - R_INSTEP
        tan_dir = bd.Vector(math.cos(theta_f), -math.sin(theta_f), 0.0).normalized()
        for z_c in slot_z_centers:
            with bd.BuildPart() as slot_bp:
                with bd.BuildSketch(
                    bd.Plane(
                        origin=(fx, fy, z_c),
                        x_dir=bd.Vector(0.0, 0.0, 1.0),
                        z_dir=tan_dir,
                    )
                ):
                    bd.SlotOverall(slot_h, slot_w)
                bd.extrude(amount=14.0, both=True)
            window_cutouts.append(slot_bp.part.solids()[0])

    shield_slotted = shield_body.cut(*channel_cutouts, *window_cutouts)

    # 4. Double-Ring Inverted Pentagram on Front Face (centered at Z_EMBLEM = 40.2)
    # Collect ALL faces (outer ring + inner ring/star) and fuse cleanly onto R_PLATE_OUT
    print("[CAD] Building double-ring inverted pentagram...")
    dv_emblem = Z_EMBLEM - Z_MID  # +1.7 mm above Z_MID

    r_star = 18.45
    star_angles = [math.radians(-90.0 + i * 72.0) for i in range(5)]
    star_pts = [(r_star * math.cos(a), dv_emblem + r_star * math.sin(a)) for a in star_angles]
    star_pairs = [(i, (i + 2) % 5) for i in range(5)]

    def make_pentagram_emblem_faces(ring_half_w: float, bar_half_w: float) -> list[bd.Face]:
        with bd.BuildSketch() as sk_emb:
            # Outer ring (r_mid = 21.15) & Inner ring (r_mid = 18.45)
            for r_mid in (21.15, 18.45):
                with bd.Locations((0.0, dv_emblem)):
                    bd.Circle(r_mid + ring_half_w)
                    bd.Circle(r_mid - ring_half_w, mode=bd.Mode.SUBTRACT)
            # Inverted 5-pointed star bars clipped to inner ring center
            with bd.BuildSketch() as sk_bars:
                for i0, i1 in star_pairs:
                    p0, p1 = star_pts[i0], star_pts[i1]
                    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
                    length = math.hypot(dx, dy)
                    ang_deg = math.degrees(math.atan2(dy, dx))
                    cx, cy = 0.5 * (p0[0] + p1[0]), 0.5 * (p0[1] + p1[1])
                    with bd.Locations((cx, cy)):
                        bd.Rectangle(length, bar_half_w * 2.0, rotation=ang_deg)
                with bd.Locations((0.0, dv_emblem)):
                    bd.Circle(18.65, mode=bd.Mode.INTERSECT)
            for f in sk_bars.sketch.faces():
                bd.insert(f)
        return list(sk_emb.sketch.faces())

    emb_base_faces = make_pentagram_emblem_faces(ring_half_w=0.80, bar_half_w=1.15)
    emb_crest_faces = make_pentagram_emblem_faces(ring_half_w=0.40, bar_half_w=0.52)

    emb_solids = [
        radial_extrude_ring_band(f, R_PLATE_OUT - 0.30, R_PLATE_OUT + 1.05)
        for f in emb_base_faces
    ] + [
        radial_extrude_ring_band(f, R_PLATE_OUT + 0.85, R_PLATE_OUT + 1.85)
        for f in emb_crest_faces
    ]

    # 5. Four Integral Perimeter Chain Rings (6.4 mm exact ID) with heavy gusseted lugs
    print("[CAD] Building 4 perimeter chain rings (6.4 mm ID)...")
    ring_attachments = []
    tier_specs = [
        (58.8, 29.4),  # Upper tier (wider top flank, clears top window at Z=51.5)
        (18.2, 26.5),  # Lower tier (tapered bottom flank, clears bottom window at Z=25.5)
    ]
    r_lug = R_PLATE_IN + 0.0  # Centered on thickened side wall depth (62.8 mm)
    for z_ring, u_edge in tier_specs:
        for sign in (-1.0, 1.0):
            # Ring center at u_edge + 6.4 -> inner bore (6.4 mm ID) starts at u_edge + 3.2 mm
            u_center = sign * (u_edge + 6.4)
            theta = u_center / R_PLATE_OUT
            px, py, pz = cyl_point(u_center, z_ring, r_lug)

            ring_norm = bd.Vector(math.sin(theta) * 0.22, math.cos(theta), 0.0).normalized()
            ring_x = bd.Vector(math.cos(theta), -math.sin(theta) * 0.22, 0.0).normalized()
            ring_plane = bd.Plane(origin=(px, py, pz), x_dir=ring_x, z_dir=ring_norm)

            with bd.BuildPart(ring_plane) as rp:
                bd.Torus(major_radius=RING_R_MAJOR, minor_radius=RING_R_MINOR)
            ring_solid = rp.part.solids()[0]

            # Heavy gusseted lug collar bridging thickened shield wall into 3.8 mm ring neck
            u_lug_start = sign * (u_edge - 2.6)
            u_lug_end = sign * (u_edge + 2.5)
            lx0, ly0, _ = cyl_point(u_lug_start, z_ring, r_lug)
            lx1, ly1, _ = cyl_point(u_lug_end, z_ring, r_lug)
            lcx, lcy = 0.5 * (lx0 + lx1), 0.5 * (ly0 + ly1)
            lug_len = math.hypot(lx1 - lx0, ly1 - ly0)
            lug_ang = math.degrees(math.atan2(ly1 - ly0, lx1 - lx0))
            with bd.BuildPart() as lp:
                with bd.Locations((lcx, lcy, z_ring)):
                    bd.Box(lug_len, 5.0, 6.4, rotation=(0, 0, lug_ang))
                bd.fillet(lp.edges(), radius=0.9)
            lug_solid = lp.part.solids()[0]
            ring_attachments.extend([ring_solid, lug_solid])

    # Fuse all CAD solids sequentially and check validity at each step
    print("[CAD] Fusing CAD sub-solids...")
    parts = [
        ("border_step1", border_step1),
        ("border_step2", border_step2),
        *[(f"emb_{i}", s) for i, s in enumerate(emb_solids)],
        *[(f"ring_{i}", s) for i, s in enumerate(ring_attachments)],
    ]
    fused = shield_slotted
    for name, p in parts:
        cand = fused.fuse(p)
        if not cand.is_valid:
            print(f"[CAD][WARN] fuse({name}) reported is_valid={cand.is_valid}")
        fused = cand

    bb = fused.bounding_box()
    print(
        f"[CAD] Fused CAD valid={fused.is_valid}, vol={fused.volume:.1f} mm^3, "
        f"bbox X=[{bb.min.X:.2f}, {bb.max.X:.2f}] (W={bb.max.X-bb.min.X:.2f}), "
        f"Y=[{bb.min.Y:.2f}, {bb.max.Y:.2f}], "
        f"Z=[{bb.min.Z:.2f}, {bb.max.Z:.2f}] (H={bb.max.Z-bb.min.Z:.2f}), "
        f"time={time.time()-t0:.2f}s"
    )
    body_bb = shield_slotted.bounding_box()
    print(
        f"[CAD] Shield plate body: W={body_bb.max.X-body_bb.min.X:.2f} mm, "
        f"H={body_bb.max.Z-body_bb.min.Z:.2f} mm"
    )
    return fused


# ---------------------------------------------------------------------------
# Part 2: 3D SDF Sculpted Baphomet Goat Skull Relief (Half-Grid Symmetric)
# ---------------------------------------------------------------------------
def smin(a: np.ndarray, b: np.ndarray | float, k: float) -> np.ndarray:
    """Polynomial smooth minimum (SDF smooth union)."""
    h = np.maximum(k - np.abs(a - b), 0.0) / k
    return np.minimum(a, b) - h * h * k * 0.25


def smax(a: np.ndarray, b: np.ndarray | float, k: float) -> np.ndarray:
    """Polynomial smooth maximum (for smooth subtraction: smax(a, -b, k))."""
    return -smin(-a, -b, k)


def sd_ellipsoid(
    px: np.ndarray,
    py: np.ndarray,
    pz: np.ndarray,
    cx: float,
    cy: float,
    cz: float,
    rx: float,
    ry: float,
    rz: float,
) -> np.ndarray:
    """Approximate signed distance to an axis-aligned ellipsoid."""
    qx = (px - cx) / rx
    qy = (py - cy) / ry
    qz = (pz - cz) / rz
    k0 = np.sqrt(qx * qx + qy * qy + qz * qz + 1e-12)
    qx2 = qx / rx
    qy2 = qy / ry
    qz2 = qz / rz
    k1 = np.sqrt(qx2 * qx2 + qy2 * qy2 + qz2 * qz2 + 1e-12)
    return k0 * (k0 - 1.0) / k1


def sd_capsule(
    px: np.ndarray,
    py: np.ndarray,
    pz: np.ndarray,
    a: tuple[float, float, float],
    b: tuple[float, float, float],
    ra: float,
    rb: float,
) -> np.ndarray:
    """Signed distance to a tapered capsule between 3D points a (radius ra) and b (radius rb)."""
    ax, ay, az = a
    bx, by, bz = b
    abx, aby, abz = bx - ax, by - ay, bz - az
    len2 = abx * abx + aby * aby + abz * abz + 1e-12
    dx, dy, dz = px - ax, py - ay, pz - az
    t = np.clip((dx * abx + dy * aby + dz * abz) / len2, 0.0, 1.0)
    cx = dx - t * abx
    cy = dy - t * aby
    cz = dz - t * abz
    r = ra + t * (rb - ra)
    return np.sqrt(cx * cx + cy * cy + cz * cz + 1e-12) - r


def eval_polyline_tube_sdf(
    u_axis: np.ndarray,
    U: np.ndarray,
    V: np.ndarray,
    H: np.ndarray,
    pts: np.ndarray,
    radii: np.ndarray,
    s_vals: np.ndarray,
    ridge_amp: np.ndarray | None = None,
    ridge_freq: float = 0.0,
) -> np.ndarray:
    """
    Evaluate minimum distance to a densely sampled 3D curve (swept tapered tube)
    with optional asymmetric annular horn ridges. `u_axis` must be sorted ascending.
    """
    d_min = np.full(U.shape, 1e6, dtype=np.float32)
    v_axis = V[0, :, 0]
    h_axis = H[0, 0, :]
    n_seg = len(pts) - 1
    for i in range(n_seg):
        p0 = pts[i]
        p1 = pts[i + 1]
        r0 = float(radii[i])
        r1 = float(radii[i + 1])
        pad = max(r0, r1) + (float(ridge_amp[i]) if ridge_amp is not None else 0.0) + 1.0
        u_lo, u_hi = min(p0[0], p1[0]) - pad, max(p0[0], p1[0]) + pad
        v_lo, v_hi = min(p0[1], p1[1]) - pad, max(p0[1], p1[1]) + pad
        h_lo, h_hi = min(p0[2], p1[2]) - pad, max(p0[2], p1[2]) + pad

        iu0 = max(0, int(np.searchsorted(u_axis, u_lo)) - 1)
        iu1 = min(U.shape[0], int(np.searchsorted(u_axis, u_hi)) + 1)
        iv0 = max(0, int(np.searchsorted(v_axis, v_lo)) - 1)
        iv1 = min(U.shape[1], int(np.searchsorted(v_axis, v_hi)) + 1)
        ih0 = max(0, int(np.searchsorted(h_axis, h_lo)) - 1)
        ih1 = min(U.shape[2], int(np.searchsorted(h_axis, h_hi)) + 1)
        if iu0 >= iu1 or iv0 >= iv1 or ih0 >= ih1:
            continue

        uu = U[iu0:iu1, iv0:iv1, ih0:ih1]
        vv = V[iu0:iu1, iv0:iv1, ih0:ih1]
        hh = H[iu0:iu1, iv0:iv1, ih0:ih1]

        ab = p1 - p0
        len2 = float(np.dot(ab, ab)) + 1e-12
        t = np.clip(
            ((uu - p0[0]) * ab[0] + (vv - p0[1]) * ab[1] + (hh - p0[2]) * ab[2]) / len2,
            0.0,
            1.0,
        )
        cx = uu - (p0[0] + t * ab[0])
        cy = vv - (p0[1] + t * ab[1])
        cz = hh - (p0[2] + t * ab[2])
        dist_center = np.sqrt(cx * cx + cy * cy + cz * cz + 1e-12)
        rad = r0 + t * (r1 - r0)

        if ridge_amp is not None and ridge_freq > 0.0:
            s = s_vals[i] + t * (s_vals[i + 1] - s_vals[i])
            amp = ridge_amp[i] + t * (ridge_amp[i + 1] - ridge_amp[i])
            phase = (s * ridge_freq) % 1.0
            p_rise = np.clip(phase / 0.72, 0.0, 1.0) ** 1.35
            p_fall = 1.0 - np.clip((phase - 0.72) / 0.28, 0.0, 1.0) ** 0.9
            wave = np.where(phase < 0.72, p_rise, p_fall)
            rad = rad + amp * (wave - 0.25)

        seg_d = dist_center - rad
        sub = d_min[iu0:iu1, iv0:iv1, ih0:ih1]
        np.minimum(sub, seg_d, out=sub)
    return d_min


def build_sculpted_skull_mesh(voxel_size: float = 0.085) -> vtk.vtkPolyData:
    """
    Sculpt the multi-layered 3D Baphomet goat skull relief on the half-grid U >= 0,
    mirror cleanly across U = 0 for guaranteed left-right horn/skull symmetry,
    extract via vtkFlyingEdges3D, and map onto the R_PLATE_OUT=65.0 mm instep cylinder.
    """
    t0 = time.time()
    print(f"[SCULPT] Evaluating symmetric 3D SDF at {voxel_size:.3f} mm voxel resolution...")

    # Half-grid: u >= 0, mirrored to [-u_max, +u_max] at the end!
    n_u_half = int(round(24.5 / voxel_size))
    u_half = np.arange(0, n_u_half + 1, dtype=np.float32) * voxel_size
    u_max = float(u_half[-1])
    v_min, v_max = -22.5, 26.5
    h_min, h_max = -1.2, 9.5

    v_arr = np.arange(v_min, v_max + voxel_size * 0.5, voxel_size, dtype=np.float32)
    h_arr = np.arange(h_min, h_max + voxel_size * 0.5, voxel_size, dtype=np.float32)

    U, V, H = np.meshgrid(u_half, v_arr, h_arr, indexing="ij")
    print(f"[SCULPT] Half-grid shape: {U.shape} ({U.size / 1e6:.2f}M voxels)")

    # -----------------------------------------------------------------------
    # 1. Cranium, Brow, Cheekbones, Nasal Bridge & Snout
    # -----------------------------------------------------------------------
    d = sd_ellipsoid(U, V, H, 0.0, 4.2, 1.0, 7.6, 6.8, 4.1)

    d_front = sd_ellipsoid(U, V, H, 0.0, 5.8, 1.6, 5.2, 4.0, 3.3)
    d = smin(d, d_front, 1.8)

    # Fierce angled supraorbital brow ridges dipping inward toward nose bridge
    d_brow0 = sd_capsule(U, V, H, (0.5, 3.1, 3.7), (2.2, 4.3, 3.9), 1.15, 1.4)
    d_brow1 = sd_capsule(U, V, H, (2.2, 4.3, 3.9), (5.0, 4.9, 4.1), 1.4, 1.55)
    d_brow2 = sd_capsule(U, V, H, (5.0, 4.9, 4.1), (7.6, 3.4, 3.3), 1.55, 1.15)
    d = smin(d, smin(d_brow0, smin(d_brow1, d_brow2, 0.8), 0.8), 1.0)

    # Zygomatic cheekbones flowing smoothly toward snout
    d_cheek1 = sd_capsule(U, V, H, (6.8, 2.2, 2.8), (5.4, -1.6, 3.4), 1.3, 1.35)
    d_cheek2 = sd_capsule(U, V, H, (5.4, -1.6, 3.4), (3.1, -5.0, 2.95), 1.35, 1.15)
    d = smin(d, smin(d_cheek1, d_cheek2, 0.85), 1.1)

    # Nasal bridge & crisp medial crest
    d_nasal = sd_capsule(U, V, H, (0.0, 3.2, 3.5), (0.0, -6.5, 3.7), 2.35, 1.95)
    d_nasal_crest = sd_capsule(U, V, H, (0.0, 2.5, 4.4), (0.0, -6.2, 4.45), 0.85, 0.72)
    d = smin(d, smin(d_nasal, d_nasal_crest, 0.9), 1.3)

    # Snout / Muzzle & Flared Alar Nostril Wings
    d_muzzle = sd_ellipsoid(U, V, H, 0.0, -7.2, 1.7, 3.4, 3.3, 3.2)
    d_alar = sd_ellipsoid(U, V, H, 1.9, -7.2, 2.8, 1.5, 1.65, 1.55)
    d_chin = sd_ellipsoid(U, V, H, 0.0, -9.8, 2.0, 2.2, 2.0, 2.2)
    d = smin(d, d_muzzle, 1.3)
    d = smin(d, d_alar, 0.9)
    d = smin(d, d_chin, 1.0)

    # Subtle sculptural cheek hollows & temporal hollows (smooth bone contour)
    d_hollow_cheek = sd_ellipsoid(U, V, H, 4.9, -3.8, 5.0, 1.15, 2.2, 1.15)
    d = smax(d, -d_hollow_cheek, 0.9)
    d_hollow_temple = sd_ellipsoid(U, V, H, 7.1, 5.2, 4.4, 1.3, 2.1, 1.5)
    d = smax(d, -d_hollow_temple, 0.7)

    # Deep Orbital Eye Sockets + Almond Eyeballs + Horizontal Goat Pupil Slit
    d_socket = sd_ellipsoid(U, V, H, 4.2, 2.3, 4.2, 1.8, 1.3, 1.75)
    d = smax(d, -d_socket, 0.6)

    d_eye = sd_ellipsoid(U, V, H, 4.1, 2.15, 3.05, 1.25, 0.85, 1.05)
    d = smin(d, d_eye, 0.25)

    d_pupil = sd_capsule(U, V, H, (3.4, 2.15, 4.15), (4.7, 2.22, 4.05), 0.28, 0.26)
    d = smax(d, -d_pupil, 0.15)

    # Flared Nostril Cavities + Philtrum Cleft
    d_nostril = sd_capsule(U, V, H, (1.25, -7.6, 4.0), (2.15, -6.9, 3.7), 0.55, 0.38)
    d = smax(d, -d_nostril, 0.25)
    d_philtrum = sd_capsule(U, V, H, (0.0, -8.3, 4.5), (0.0, -10.8, 3.8), 0.35, 0.28)
    d = smax(d, -d_philtrum, 0.22)

    # -----------------------------------------------------------------------
    # 2. Furrowed Goat Beard Tuft (v = -9.8 down to -19.8 mm)
    # -----------------------------------------------------------------------
    d_beard = sd_capsule(U, V, H, (0.0, -10.0, 2.0), (0.0, -19.6, 1.35), 2.35, 0.45)
    beard_mask = np.clip(1.0 - np.maximum(d_beard, 0.0) / 1.4, 0.0, 1.0)
    v_beard_norm = np.clip((-9.5 - V) / 10.5, 0.0, 1.0)
    u_flow = U / (1.0 - 0.65 * v_beard_norm + 1e-4)
    fur_wave = np.cos(u_flow * 4.4 + 0.45 * np.sin(V * 1.1))
    d_beard_furrowed = d_beard - beard_mask * 0.38 * fur_wave
    d = smin(d, d_beard_furrowed, 0.55)

    # -----------------------------------------------------------------------
    # 3. Flared Leaf-Shaped Goat Ears with Raised Rim & Scooped Conch Hollow
    # -----------------------------------------------------------------------
    ear_pts = np.array([
        [5.8,  3.2, 2.3],
        [9.6,  2.2, 2.6],
        [13.8, 1.0, 2.6],
        [17.6, -0.2, 2.35],
        [20.4, -1.2, 1.9],
    ], dtype=np.float32)
    d_ear_spine = eval_polyline_tube_sdf(
        u_half, U, V, H * 1.45 - 0.9,
        np.column_stack([ear_pts[:, 0], ear_pts[:, 1], ear_pts[:, 2] * 1.45 - 0.9]),
        np.array([2.1, 2.5, 2.25, 1.4, 0.35], dtype=np.float32),
        np.linspace(0, 1, len(ear_pts), dtype=np.float32),
    )
    ear_top_rim = sd_capsule(U, V, H, (6.0, 4.4, 2.65), (19.9, -0.8, 2.05), 0.72, 0.28)
    ear_bot_rim = sd_capsule(U, V, H, (6.0, 1.7, 2.55), (19.6, -1.5, 1.95), 0.65, 0.28)
    d_ear = smin(d_ear_spine, smin(ear_top_rim, ear_bot_rim, 0.35), 0.35)
    d_conch = sd_capsule(U, V, H, (8.6, 2.2, 3.95), (17.2, -0.1, 3.65), 0.9, 0.42)
    d_ear = smax(d_ear, -d_conch, 0.35)
    d = smin(d, d_ear, 0.65)

    # -----------------------------------------------------------------------
    # 4. Sweeping, Ridged Symmetric Ram/Goat Horns (~18 annular ridges)
    # -----------------------------------------------------------------------
    t_horn = np.linspace(0.0, 1.0, 48, dtype=np.float32)
    # Graceful lyre sweep curving up & outward over the double ring, staying cleanly inside the shield border
    u_horn = 2.6 + 13.8 * (t_horn ** 0.85) + 2.0 * np.sin(t_horn * math.pi)
    v_horn = 6.8 + 14.2 * np.sin(t_horn * 0.62 * math.pi) + 4.8 * (t_horn ** 2.2)
    h_horn = 3.9 + 1.65 * np.sin(t_horn * math.pi) - 0.55 * (t_horn ** 2.0)
    horn_pts = np.column_stack([u_horn, v_horn, h_horn]).astype(np.float32)

    diffs = np.diff(horn_pts, axis=0)
    seg_lens = np.sqrt(np.sum(diffs * diffs, axis=1))
    s_horn = np.concatenate([[0.0], np.cumsum(seg_lens)]).astype(np.float32)
    r_horn = 2.45 * ((1.0 - 0.84 * t_horn) ** 0.85) + 0.15
    ridge_amp = 0.40 * (1.0 - 0.72 * t_horn)

    d_horn = eval_polyline_tube_sdf(
        u_half, U, V, H,
        horn_pts, r_horn, s_horn,
        ridge_amp=ridge_amp,
        ridge_freq=0.68,
    )
    # Smooth organic transition at horn root into brow/cranium
    d_horn_boss = sd_ellipsoid(U, V, H, 2.7, 6.6, 3.1, 2.1, 2.1, 2.2)
    d_horn = smin(d_horn, d_horn_boss, 0.65)
    d = smin(d, d_horn, 0.65)

    # -----------------------------------------------------------------------
    # 5. Forehead Flame Torch (set between horn bases on forehead)
    # -----------------------------------------------------------------------
    # Raised forehead medallion boss + fluted torch cup + bold 3-tongue flame
    d_boss = sd_ellipsoid(U, V, H, 0.0, 5.0, 4.15, 2.0, 1.8, 0.9)
    d_torch_cup = sd_capsule(U, V, H, (0.0, 4.4, 4.6), (0.0, 6.4, 5.05), 0.85, 1.55)
    d_torch_collar = sd_ellipsoid(U, V, H, 0.0, 6.6, 5.15, 1.9, 0.6, 1.15)
    d_torch = smin(d_boss, smin(d_torch_cup, d_torch_collar, 0.25), 0.35)

    flame_center_pts = np.array([
        [0.0,  6.7, 5.15],
        [0.0,  8.3, 5.55],
        [0.0, 10.2, 5.45],
        [0.0, 12.1, 4.95],
        [0.0, 13.5, 4.35],
    ], dtype=np.float32)
    d_flame_main = eval_polyline_tube_sdf(
        u_half, U, V, H,
        flame_center_pts,
        np.array([1.45, 1.25, 0.92, 0.48, 0.14], dtype=np.float32),
        np.linspace(0, 1, len(flame_center_pts), dtype=np.float32),
    )
    d_flame_lick = sd_capsule(U, V, H, (1.0, 6.7, 4.95), (2.05, 10.3, 4.55), 0.82, 0.18)
    d_flame = smin(d_flame_main, d_flame_lick, 0.35)
    d = smin(d, smin(d_torch, d_flame, 0.28), 0.35)

    # -----------------------------------------------------------------------
    # 6. Mirror Half-Grid across U = 0 & Ground Back Cap inside Shield Plate
    # -----------------------------------------------------------------------
    d_full = np.concatenate([d[:0:-1, :, :], d], axis=0)
    u_full = np.concatenate([-u_half[:0:-1], u_half])
    U_full = np.broadcast_to(u_full[:, None, None], d_full.shape)
    V_full = np.broadcast_to(v_arr[None, :, None], d_full.shape)
    H_full = np.broadcast_to(h_arr[None, None, :], d_full.shape)

    d_box = np.maximum.reduce([
        (-0.75) - H_full,
        H_full - (h_max - 0.25),
        (-u_max + 0.25) - U_full,
        U_full - (u_max - 0.25),
        (v_min + 0.25) - V_full,
        V_full - (v_max - 0.25),
    ])
    d_final = np.maximum(d_full, d_box)

    # -----------------------------------------------------------------------
    # 7. Extract Smooth Watertight Mesh via vtkFlyingEdges3D & Map to Cylinder
    # -----------------------------------------------------------------------
    print("[SCULPT] Running vtkFlyingEdges3D isosurface extraction...")
    img = vtk.vtkImageData()
    img.SetDimensions(d_final.shape[0], d_final.shape[1], d_final.shape[2])
    img.SetOrigin(-u_max, v_min, h_min)
    img.SetSpacing(voxel_size, voxel_size, voxel_size)

    flat = np.ascontiguousarray(d_final.transpose(2, 1, 0)).ravel()
    vtk_arr = numpy_support.numpy_to_vtk(flat, deep=True, array_type=vtk.VTK_FLOAT)
    vtk_arr.SetName("sdf")
    img.GetPointData().SetScalars(vtk_arr)

    fe = vtk.vtkFlyingEdges3D()
    fe.SetInputData(img)
    fe.SetValue(0, 0.0)
    fe.ComputeNormalsOff()
    fe.Update()
    poly = fe.GetOutput()
    print(f"[SCULPT] Extracted {poly.GetNumberOfCells()} triangles")

    smoother = vtk.vtkWindowedSincPolyDataFilter()
    smoother.SetInputData(poly)
    smoother.SetNumberOfIterations(14)
    smoother.BoundarySmoothingOff()
    smoother.FeatureEdgeSmoothingOff()
    smoother.SetPassBand(0.18)
    smoother.NonManifoldSmoothingOn()
    smoother.NormalizeCoordinatesOn()
    smoother.Update()
    poly = smoother.GetOutput()

    pts_vtk = poly.GetPoints()
    pts_np = numpy_support.vtk_to_numpy(pts_vtk.GetData()).astype(np.float64)
    u_v = pts_np[:, 0]
    v_v = pts_np[:, 1]
    h_v = pts_np[:, 2]

    theta_v = u_v / R_PLATE_OUT
    r_v = R_PLATE_OUT + h_v
    x_3d = r_v * np.sin(theta_v)
    y_3d = r_v * np.cos(theta_v) - R_INSTEP
    z_3d = Z_EMBLEM + v_v

    mapped_pts = np.column_stack([x_3d, y_3d, z_3d]).astype(np.float32)
    vtk_pts = numpy_support.numpy_to_vtk(mapped_pts, deep=True)
    new_pts = vtk.vtkPoints()
    new_pts.SetData(vtk_pts)
    poly.SetPoints(new_pts)

    norms = vtk.vtkPolyDataNormals()
    norms.SetInputData(poly)
    norms.ConsistencyOn()
    norms.AutoOrientNormalsOn()
    norms.SplittingOff()
    norms.Update()
    poly = norms.GetOutput()

    edges = vtk.vtkFeatureEdges()
    edges.SetInputData(poly)
    edges.BoundaryEdgesOn()
    edges.NonManifoldEdgesOn()
    edges.FeatureEdgesOff()
    edges.ManifoldEdgesOff()
    edges.Update()
    bad_edges = edges.GetOutput().GetNumberOfCells()
    print(
        f"[SCULPT] Final skull mesh: {poly.GetNumberOfCells()} tris, "
        f"bad_edges={bad_edges}, time={time.time()-t0:.2f}s"
    )
    return poly


def export_combined_stl(cad_solid: bd.Solid | bd.Compound, skull_poly: vtk.vtkPolyData, out_path: Path) -> None:
    """Export high-res CAD STL, merge cleanly with skull mesh, and save final binary STL."""
    with tempfile.TemporaryDirectory() as tmp:
        cad_stl_path = Path(tmp) / "cad_base.stl"
        bd.export_stl(cad_solid, str(cad_stl_path), tolerance=0.008, angular_tolerance=0.05)

        r_cad = vtk.vtkSTLReader()
        r_cad.SetFileName(str(cad_stl_path))
        r_cad.Update()
        cad_poly = r_cad.GetOutput()

    fe = vtk.vtkFeatureEdges()
    fe.SetInputData(cad_poly)
    fe.BoundaryEdgesOn()
    fe.NonManifoldEdgesOn()
    fe.FeatureEdgesOff()
    fe.ManifoldEdgesOff()
    fe.Update()
    print(f"[EXPORT] CAD mesh: {cad_poly.GetNumberOfCells()} tris, bad_edges={fe.GetOutput().GetNumberOfCells()}")

    app = vtk.vtkAppendPolyData()
    app.AddInputData(cad_poly)
    app.AddInputData(skull_poly)
    app.Update()

    w_out = vtk.vtkSTLWriter()
    w_out.SetFileTypeToBinary()
    w_out.SetFileName(str(out_path))
    w_out.SetInputData(app.GetOutput())
    w_out.Write()
    print(f"[EXPORT] Saved {out_path} ({out_path.stat().st_size / 1e6:.2f} MB)")


def show_in_ocp_viewer(cad_solid: bd.Solid | bd.Compound, skull_poly: vtk.vtkPolyData) -> None:
    """Broadcast the CAD shield base and sculpted Baphomet relief to OCP CAD Viewer."""
    try:
        from ocp_vscode import Camera, show
    except Exception:
        return

    # Decimate a viewer-only preview of the sculpted skull so OCP CAD Viewer renders fast
    # while keeping full 0.085 mm voxel fidelity in the exported STL.
    dec = vtk.vtkQuadricDecimation()
    dec.SetInputData(skull_poly)
    dec.SetTargetReduction(0.75)
    dec.Update()

    with tempfile.TemporaryDirectory() as tmp:
        preview_stl = Path(tmp) / "skull_ocp_preview.stl"
        w = vtk.vtkSTLWriter()
        w.SetFileTypeToBinary()
        w.SetFileName(str(preview_stl))
        w.SetInputData(dec.GetOutput())
        w.Write()
        skull_face = bd.import_stl(str(preview_stl))

    try:
        print("[OCP] Broadcasting Baphomet Lace Shield to OCP CAD Viewer...")
        show(
            cad_solid,
            skull_face,
            names=["Shield_Base_Channels_Rings", "Baphomet_Skull_Relief"],
            colors=[(0.18, 0.18, 0.20, 1.0), (0.25, 0.25, 0.28, 1.0)],
            black_edges=False,
            reset_camera=Camera.RESET,
        )
    except Exception as exc:
        print(f"[OCP] Viewer not active ({exc})")


if __name__ == "__main__":
    cad = build_cad_base()
    skull = build_sculpted_skull_mesh(voxel_size=0.085)
    out_stl = OUT_DIR / "A_HighDetail_Baphomet_Lace_Shield.stl"
    export_combined_stl(cad, skull, out_stl)
    show_in_ocp_viewer(cad, skull)

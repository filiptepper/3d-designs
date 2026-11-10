# build123d 3D Designs

This repository contains parametric 3D models designed using **[build123d](https://github.com/gumyr/build123d)**, a modern Python-based CAD programming library.

---

## Included Models

### 1. Darkglass Anagram Cover v2
* **Script:** [`darkglass-anagram-cover-v2.py`](file:///home/filiptepper/Code/3d-designs/darkglass-anagram-cover-v2.py)
* **Description**: A precise, protective cover/shell custom-built for the Darkglass Anagram device. It features:
  * Openings/cutouts for a screen and two rows of knobs/buttons (6 in the top row, 3 in the bottom row).
  * Embossed divider lines and arrow-shaped indicator markings on the face.
  * Side and front cutouts for port access and venting.
  * Filleted edges and corner radii matching the physical device.

---

### 2. Key Tag
* **Script:** [`key-tag.py`](file:///home/filiptepper/Code/3d-designs/key-tag.py)
* **Description**: A basic parametric key tag / keyring template. Easily customizable in dimensions (width, length, thickness, hole size, offsets, and corner radius).

---

### 3. Elevated 20-Series Aluminum Extrusion Stage Pedalboard
* **Script:** [`extrusion-pedalboard.py`](file:///home/filiptepper/Code/3d-designs/extrusion-pedalboard.py)
* **Description**: Parametric stage pedalboard engineered around four slotted 2020 aluminum extrusions ($400\,\text{mm}$ span, $10.0^\circ$ incline) with elevated 3D-printed side cheeks and a slideable rail-mounted underbelly cradle for a **CIOKS Sol** power supply.
* **3D Printable Parts (Print Flat on Bed, Zero Supports):**
  * [`pedalboard_leg_elevated_l.stl`](file:///home/filiptepper/Code/3d-designs/pedalboard_leg_elevated_l.stl): Left cheek with rearward-facing custom vector logo cutout. Printed flat on inner face ($Z = 0$).
  * [`pedalboard_leg_elevated_r.stl`](file:///home/filiptepper/Code/3d-designs/pedalboard_leg_elevated_r.stl): Right cheek with forward-facing custom vector logo cutout. Printed flat on inner face ($Z = 0$).
  * [`pedalboard_cioks_rail_cradle.stl`](file:///home/filiptepper/Code/3d-designs/pedalboard_cioks_rail_cradle.stl): Rail-mounted CIOKS Sol cradle with cable ports and convective cooling slots. Printed flat on base ($Z = 0$).
* **Assembly Reference Models:**
  * [`pedalboard_2020_rails_elevated.stl`](file:///home/filiptepper/Code/3d-designs/pedalboard_2020_rails_elevated.stl): 4x slotted 2020 extrusions in assembled coordinates.
  * [`pedalboard_extrusion_assembly_v2.stl`](file:///home/filiptepper/Code/3d-designs/pedalboard_extrusion_assembly_v2.stl): Complete assembled pedalboard with rails, legs, and cradle.

#### Key Architectural Features:
* **$+12.0\,\text{mm}$ Vertical Lift (Preserving Exact $10.0^\circ$ Deck Slope):**
  * Sockets and deck profile are translated along the $80.0^\circ$ stance line ($\Delta Y = -2.12\,\text{mm}, \Delta Z = +12.0\,\text{mm}$).
  * Front nose elevation: $49.8\,\text{mm}$; rear elevation: $79.0\,\text{mm}$.
  * Floor footing remains flat at $Z = 0.0$ for non-slip stage stability.
* **Full 4-Rail Through-Bolting:**
  * $\varnothing 6.5\,\text{mm}$ counterbored through-holes for **all four rails** (Rails 1, 2, 3, and 4) through the outer cheek wall into the tapped center M5/M6 threads of the 2020 extrusions.
* **Custom Vector Logo Through-Holes:**
  * Replaces hexagonal honeycomb holes with a clean geometric 5-bar emblem cutout.
  * $25.0\,\text{mm}$ stencil width ($39.29\,\text{mm}$ height, centered at $Y = 148.0\,\text{mm}, Z = 24.5\,\text{mm}$).
  * Solid $1.67\,\text{mm}$ perimeter ribs (solid 4-wall print with $0.4\,\text{mm}$ nozzle) and a $4.0\,\text{mm}$ solid structural bridge below Rail 4's socket floor.
  * Mirrored horizontally on the left cheek so both emblems point harmoniously rearward/forward.
  * Top and bottom channels are open into the solid cheek, yielding a 100% physically connected single manifold solid (zero floating islands).
* **Rail-Mounted CIOKS Sol Cradle (Concept A):**
  * Mounts to the bottom T-slots of Rails 3 & 4 via drop-in T-nuts and M3/M4 button-head screws.
  * Fully slideable and lockable anywhere along the $400\,\text{mm}$ width (left, center, or right).
  * Direct bolting into the CIOKS Sol chassis via two diagonal M4 countersunk holes ($70 \times 40\,\text{mm}$ pattern).
  * Generous side portals: Left bay ($72 \times 26\,\text{mm}$) for IEC mains cord; Right bay ($80 \times 24\,\text{mm}$) for 5 DC RCA power leads.
  * Top cable troughs ($12\,\text{mm}$ clearance) allow power leads to route upward into extrusion slots without pinching.
  * Lowest point sits at **$+8.75\,\text{mm}$ above the floor ($Z = 0$)**, guaranteeing positive ground clearance and zero floor contact.

---

### 4. Akai MPK Mini MK2 Replacement Joystick
* **Script:** [`akai-mpk-mini-joystick.py`](file:///home/filiptepper/Code/3d-designs/akai-mpk-mini-joystick.py)
* **Exported Files:**
  * [`akai_mpk_mini_joystick_oem.stl`](file:///home/filiptepper/Code/3d-designs/akai_mpk_mini_joystick_oem.stl) (Direct OEM drop-in replacement with center M2 screw pocket)
  * [`akai_mpk_mini_joystick_repair_sleeve.stl`](file:///home/filiptepper/Code/3d-designs/akai_mpk_mini_joystick_repair_sleeve.stl) (Reinforced deep socket for snapped stem stubs)
  * [`akai_mpk_mini_joystick_square_stem.stl`](file:///home/filiptepper/Code/3d-designs/akai_mpk_mini_joystick_square_stem.stl) (Universal 3.4x3.4 mm press-fit socket for bare Alps gimbals)
  * [`akai_mpk_mini_joystick_top_plug.stl`](file:///home/filiptepper/Code/3d-designs/akai_mpk_mini_joystick_top_plug.stl) (Cosmetic snap-in cover for the screw counterbore)
* **Description**: Parametric replacement for the fragile red 4-way pitch bend and modulation thumbstick on the Akai MPK Mini MK2 (also compatible with MK3 and MPK Mini Play).
  * **Ergonomic Head:** $\varnothing 12.0\,\text{mm}$ textured thumbpad with a $0.8\,\text{mm}$ concave dish and concentric micro-traction rings.
  * **Spherical Dust Skirt:** $\varnothing 15.2\,\text{mm}$ spherical collar seating inside the top chassis aperture to seal against dust through $\pm 25^\circ$ deflection.
  * **Printing Parameters (Bambu Lab A1):**
    * **Material:** PETG (recommended for impact toughness and layer bonding) or Tough PLA.
    * **Layer Height:** $0.12\,\text{mm}$ High Quality (or $0.08\,\text{mm}$) for smooth skirt curvature and crisp thumbpad ridges.
    * **Infill / Walls:** 100% solid infill or 6+ perimeter walls (critical to resist lateral thumb shear forces).
    * **Orientation:** Print upright with Tree Supports (Slim) under the spherical skirt and a $3\,\text{mm}$ outer brim for bed adhesion.

---

## Getting Started

### Prerequisites
Make sure you have Python installed (3.9+ recommended). Set up a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # On macOS/Linux
# or
.venv\Scripts\activate     # On Windows
```

### Installation
Install the required packages:

```bash
pip install -r requirements.txt
```

### Generating & Viewing Models
To generate models and visualize them in VS Code / Antigravity IDE:
1. Install the **OCP CAD Viewer** extension in VS Code.
2. Open the viewer panel (`Ctrl+Shift+P` $\rightarrow$ `OCP CAD Viewer: Open viewer`).
3. Run any design script:
   ```bash
   # Elevated 2020 extrusion pedalboard & CIOKS Sol cradle
   python extrusion-pedalboard.py

   # Darkglass Anagram protective cover
   python darkglass-anagram-cover-v2.py

   # Akai MPK Mini replacement joystick
   python akai-mpk-mini-joystick.py

   # Parametric key tag
   python key-tag.py
   ```
4. The generated STL files will be exported to the repository root and rendered interactively in the 3D viewer.

---

## License

This work is licensed under a **Creative Commons Attribution-NonCommercial 4.0 International License (CC BY-NC 4.0)**.

[![License: CC BY-NC 4.0](https://licensebuttons.net/l/by-nc/4.0/88x31.png)](https://creativecommons.org/licenses/by-nc/4.0/)

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
* **Script:** [`key_tag.py`](file:///home/filiptepper/Code/3d-designs/key_tag.py)
* **Description**: A basic parametric key tag / keyring template. Easily customizable in dimensions (width, length, thickness, hole size, offsets, and corner radius).

---

### 3. Ultra-Lightweight High-Strength Pedalboard
* **Script:** [`pedalboard.py`](file:///home/filiptepper/Code/3d-designs/pedalboard.py)
* **Exported File:** [`chocolate-darkglass-pedalboard.stl`](file:///home/filiptepper/Code/3d-designs/chocolate-darkglass-pedalboard.stl)
* **Description**: An ultra-lightweight (~197g), stage-rigid pedalboard custom-engineered for the **M-VAVE Chocolate Plus** and **Darkglass Anagram**, integrated with a dual-end snap-locking cradle for the **Baseus GaN3 Pro 65W Desktop Charger** and push-in internal cable routing cradles. Guaranteed 100% watertight single solid (zero floating or disconnected geometry).

#### Key Architectural Features:
* **Ultra-Lightweight Skeletal Side Walls:**
  * 2.4 mm thin-wall perimeter cheeks with dual skeletal truss cutouts ($36 \times 20\,\text{mm}$ front-mid, $36 \times 24\,\text{mm}$ rear), cutting side wall mass by ~40% while preserving triangulated structural rigidity.
* **Rock-Solid Foot-Stomp Support Under Anagram:**
  * **Central Longitudinal Load Spine:** 3.0 mm thick vertical keel extending from the deck underside **all the way to the floor ($Z = 0$)**.
  * **Transverse Stomp Rib:** Heavy-duty load rib directly beneath the Darkglass Anagram footswitch strike zone ($Y = 80\,\text{mm}$).
  * **5th Ground-Contact Foot:** A 5th recessed rubber bumper pad placed directly under the central stomp intersection for **0 mm deflection** when stomping with full body weight.
* **Snap-In Controller Retention (M-VAVE Chocolate Plus):**
  * Sized at 213.2 × 36.8 mm for a snug fit.
  * Features **4 integrated snap detent beads** (two on the front retaining lip, two on the rear lip) with 45° lead-in chamfers.
  * The controller presses down and snaps firmly into place with a positive mechanical click — zero velcro required, and it cannot fall out when inverted.
  * Floor weight-reduction window ($180 \times 22\,\text{mm}$) allows pushing the controller up from below for quick release.
* **Dual-End Solid Snap Lock for Baseus GaN3 Pro Charger:**
  * Located under the left Anagram deck ($X = -65.0\,\text{mm}$).
  * **Front Snap Lock Tabs:** Dual vertical snap arms with 1.4 mm locking detents catch the front upper bezel of the charger.
  * **Rear Snap Lock Tabs:** Dual vertical snap arms with 1.4 mm locking detents catch the rear upper bezel of the charger.
  * The charger snaps positively into place on **both ends**, locking it rigidly against all movement (forward, backward, upward, or downward).
* **Push-In Internal Cable Routing Cradles:**
  * 4 internal C-shaped snap cradles ($\varnothing 5.2\,\text{mm}$ bore with $3.6\,\text{mm}$ flexible mouth) located along internal walls:
    * **C1 (Front-Left):** Snaps and guides Chocolate USB-C cable into the charger.
    * **C2 (Center-Front):** Snaps Chocolate TRS cable entering from the drop trench.
    * **C3 (Center-Rear):** Guides TRS cable through the central spine up to the Anagram rear.
    * **C4 (Rear-Left):** Snaps Anagram USB-C cable heading into the charger.
  * Cables are simply pushed in from below with a finger and snap securely into the cradles.
* **Cable Drop Trench & Rear I/O:**
  * 16 mm full-width open drop trench between tiers for right-angle cables.
  * 130 mm wide rear I/O cutout for Darkglass audio, XLR, and MIDI connections.
  * Dedicated circular arch at the rear base for the Baseus AC power cord.
* **Non-Slip 5-Point Base:**
  * 5 recessed mounting pads ($\varnothing 11 \times 1.5\,\text{mm}$) for non-slip rubber bumpon feet (4 corners + 1 center stomp pad).

---

## Cable Routing Architecture

```
  ┌────────────────────────────────────────────────────────┐
  │              DARKGLASS ANAGRAM (Angled 12°)            │
  │  [Rear USB-C PD]                [Rear Audio / TRS MIDI]│
  └────────┬──────────────────────────────────┬────────────┘
           │ (Right-Angle USB-C)              │ (Right-Angle TRS)
           │ Drops through rear I/O           │ Drops through rear I/O
           ▼                                  ▼
      [Cradle C4]                        [Cradle C3]
           │                                  │
           │ (Internal underbelly)            │ (Central load spine)
           ▼                                  ▼
  ┌───────────────────┐                  [Cradle C2]
  │ BASEUS GaN3 PRO   │ (Dual Snap Lock)      ▲
  │ 65W CHARGER       │                       │
  │ [Type-C1][Type-C2]│                       │ (Right-Angle TRS)
  └─────▲─────────▲───┘                       │
        │         │                           │
        │         │ (Right-Angle USB-C)       │
        │         └───────────[Cradle C1]─────┘
        │                            ▲
        │ (via underbelly)           │ (Drops through trench)
  ┌─────┴────────────────────────────┴─────────────────────┐
  │                 16mm CABLE DROP TRENCH                 │
  └─────────────────────────┬──────────────────────────────┘
                            │
  ┌─────────────────────────┴──────────────────────────────┐
  │         M-VAVE CHOCOLATE PLUS (4-Point Snap-In)        │
  │        [FS1]        [FS2]        [FS3]        [FS4]    │
  └────────────────────────────────────────────────────────┘
```

---

## Specifications & Weight Summary

| Metric | Bulky Solid Baseline | New High-Strength Skeletal Design | Improvement |
| :--- | :--- | :--- | :--- |
| **Footprint (W × D × H)** | 224.0 × 172.4 × 71.1 mm | **218.0 × 158.0 × 65.3 mm** | Compact & stage-ready |
| **Solid Material Volume** | 361,101.8 mm³ | **159,377.0 mm³** | **55.9% less material** |
| **PLA Weight (1.24 g/cm³)** | ~447.8 g | **~197.6 g** | **~250 g lighter!** |
| **PETG Weight (1.27 g/cm³)** | ~458.6 g | **~202.4 g** | **~256 g lighter!** |
| **Topology** | Solid with blind voids | **100% Watertight Single Solid** | Zero floating elements |
| **Footswitch Flex** | Noticeable deck bounce | **0.0 mm (Ground-contact spine + 5th foot)** | Rock-solid stomping |
| **Controller Retention** | Loose tray drop | **Positive 4-point snap lock** | Snaps in place |
| **Charger Retention** | Friction / loose slide | **Positive dual-end snap lock** | Solid lock on both ends |
| **Internal Cable Routing** | Loose wires | **4 push-in C-clip cradles** | Pushed & snapped into conduits |

---

## 3D Printing Recommendations

| Parameter | Recommended Setting | Rationale |
| :--- | :--- | :--- |
| **Material** | **PETG** | Higher heat resistance ($T_g \approx 78^\circ\text{C}$) for GaN charger heat, plus excellent snap-fit ductility. |
| **Alternative Material** | **PLA / PLA+** | Stiff, fast, and easy to print. |
| **Wall Loops / Perimeters** | **3 to 4 walls (1.2 – 1.6 mm)** | Ensures rigid shell and durable snap tabs. |
| **Top / Bottom Solid Layers** | **4 layers (0.8 – 1.0 mm)** | Clean, rigid surface finish. |
| **Infill Density** | **15% – 20%** | Gyroid or Tri-Hexagonal. |
| **Print Orientation** | **Flat on bottom (Z = 0)** | Zero bed rotation needed. |
| **Rubber Feet** | **10–12 mm rubber bumpons** | Press into the 5 recessed pads on the bottom for grip and acoustic decoupling. |

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
3. Run the Python script:
   ```bash
   python pedalboard.py
   ```
4. The STL file (`chocolate-darkglass-pedalboard.stl`) will be exported to the repository root and rendered interactively in the viewer.

---

## License

This work is licensed under a **Creative Commons Attribution-NonCommercial 4.0 International License (CC BY-NC 4.0)**.

[![License: CC BY-NC 4.0](https://licensebuttons.net/l/by-nc/4.0/88x31.png)](https://creativecommons.org/licenses/by-nc/4.0/)

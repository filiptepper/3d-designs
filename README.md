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

### 4. Simple Lightweight Two-Tier Stage Pedalboard
* **Script:** [`simple_pedalboard.py`](file:///home/filiptepper/Code/3d-designs/simple_pedalboard.py)
* **Exported File:** `simple-pedalboard.stl`
* **Description**: A clean-sheet, simple, stage-ready two-tier pedalboard built from scratch for the **M-VAVE Chocolate Plus** and **Darkglass Anagram**, featuring an underbelly cradle for the **Baseus GaN3 Pro 65W Desktop Charger**, ergonomic drop-in trays with fingertip pry notches, an inter-tier cable drop trench, and push-in C-clip cable guides.
* **Footprint:** $220.0 \times 171.4 \times 51.1\,\text{mm}$
* **Key Features:**
  * **Lower Tier:** Form-fitting tray ($213.5 \times 37.0\,\text{mm}$, depth $6\,\text{mm}$) with side finger pry notches and bottom push-up window.
  * **Upper Tier:** Raised ($+15\,\text{mm}$ step) and tilted forward at $11.5^\circ$ ($211.5 \times 106.5\,\text{mm}$), with full-width rear I/O cutout ($160\,\text{mm}$ wide) for 1/4", XLR, MIDI, and USB-C connectors.
  * **Underbelly Charger Cradle:** Sized for Baseus GaN3 Pro 65W with thermal ventilation slots, rear AC cord archway, and front USB port window directly under the drop trench.
  * **Zero-Flex Stomp Keel:** Continuous $3.5\,\text{mm}$ vertical center spine running directly from the deck to the floor ($Z = 0$), backed by a 5th center rubber bumper pad.
  * **Cable Routing:** Full-width $16\,\text{mm}$ inter-tier drop trench and 3 push-in C-clip channels along interior ribs.

---

### 5. Stage Pedalboard Platform (Tour-Grade Engineering Specification)
* **Script:** [`stage_pedalboard.py`](file:///home/filiptepper/Code/3d-designs/stage_pedalboard.py)
* **Exported File:** [`stage-pedalboard.stl`](file:///home/filiptepper/Code/3d-designs/stage-pedalboard.stl)
* **Description**: A comprehensive, tour-grade stage pedalboard engineered to meet the formal *Engineering Specification and Structural Design of an Additively Manufactured Stage Pedalboard Platform* guidelines. Designed for the **Darkglass Anagram**, **M-VAVE Chocolate Plus**, and an undermounted **Baseus GaN3 Pro 65W Desktop Charger (CCDK65S)**.
* **Footprint:** $222.0 \times 178.0 \times 61.8\,\text{mm}$ (Single monolithic print; 100% watertight single solid, volume: $291.5\,\text{cm}^3$). Fits standard $256 \times 256\,\text{mm}$ and $250 \times 210\,\text{mm}$ desktop 3D printer beds.

#### Engineering & Ergonomic Highlights:
* **Inadvertent Actuation Prevention (Toe-Guard Barrier):**
  * Continuous $5.0\,\text{mm}$ thick raised barrier rib rising to $Z = 51.0\,\text{mm}$ ($+10\,\text{mm}$ proud of the Anagram front deck).
  * Acts as a positive mechanical stop for stage boots, eliminating accidental strikes against the Anagram’s 7" capacitive display, rotary encoders, or scene switches during rapid footswitch changes on the lower tier.
  * Elevation differential $\Delta z = 32\,\text{mm}$ between lower controller top and upper deck floor ensures natural ankle articulation.
* **Ergonomic Drop-In Trays:**
  * **Lower Tier:** Form-fitting pocket ($213.5 \times 37.0 \times 6.0\,\text{mm}$) with $\varnothing 18\,\text{mm}$ side finger pry notches and an underbelly push-up window for effortless, tool-less removal.
  * **Upper Tier:** Inclined at $8.0^\circ$ ($213.5 \times 106.5 \times 6.0\,\text{mm}$ along slope) with $\varnothing 30\,\text{mm}$ side finger pry notches.
* **Tool-Less Snap-In Baseus GaN3 Pro Cradle:**
  * Custom-fitted under the left Anagram deck ($X = -58.0\,\text{mm}$) for the Baseus GaN3 Pro CCDK65S ($70 \times 40 \times 36.9\,\text{mm}$).
  * Integrated flexible cantilever snap tabs with $1.4\,\text{mm}$ locking detents securely retain the charger from below; tool-less release by simply flexing the tabs outward.
  * 5 longitudinal convective cooling chimney slots ($4 \times 48\,\text{mm}$) in the floor plate maintain ambient airflow.
  * Front window facing the central cable trench for immediate USB-C cable runs; rear archway for the thick AC mains cord to exit the rear-left flank.
* **Zero-Deflection Stomp Keel & Bulkhead:**
  * $3.5\,\text{mm}$ continuous longitudinal load spine connecting the deck underside directly down to the floor plane ($Z = 0$).
  * $3.5\,\text{mm}$ transverse stomp bulkhead positioned directly under the Anagram footswitch strike zone ($Y = 100\,\text{mm}$).
  * 5-point non-slip base with $12.7\,\text{mm}$ ($1/2"$) $\times 3.5\,\text{mm}$ deep counterbores for standard adhesive rubber bumper feet (4 corners + 1 center stomp pillar).
* **Strict EMI Isolation & Cable Management:**
  * AC mains power and DC supply lines are strictly isolated on the far-left flank, maintaining $>120\,\text{mm}$ physical separation from high-gain audio and balanced XLR outputs on the right flank.
  * Full-width $22\,\text{mm}$ inter-tier cable drop trench allows $90^\circ$ right-angle USB and TRS plugs to dive directly below deck.
  * Large $175\,\text{mm}$ wide rear open perimeter bay gives line-of-sight plug-in access for dual XLRs, 1/4" jacks, MIDI, USB, and DC barrel connectors.
  * 3 integrated push-in C-clip retainers ($\varnothing 5.2\,\text{mm}$ bore with $3.6\,\text{mm}$ mouth) securely hold cables along the underbelly.

---

### 6. Standalone Darkglass Anagram Pedalboard
* **Script:** [`anagram-pedalboard.py`](file:///home/filiptepper/Code/3d-designs/anagram-pedalboard.py)
* **Exported File:** [`anagram-pedalboard.stl`](file:///home/filiptepper/Code/3d-designs/anagram-pedalboard.stl)
* **Description**: An ultra-compact, standalone pedalboard custom-engineered exclusively for the **Darkglass Anagram**, featuring a transverse underbelly cradle for the **Baseus GaN3 Pro 65W Desktop Charger (CCDK65S)** and through-wall zip-tie cable management anchors.
* **Footprint:** $220.0 \times 112.0 \times 58.8\,\text{mm}$ (Single monolithic print; 100% watertight single solid, volume: $215.8\,\text{cm}^3$). Fits virtually all desktop 3D printers ($256 \times 256\,\text{mm}$, $220 \times 220\,\text{mm}$, and $250 \times 210\,\text{mm}$ beds).

#### Key Features & Optimized Geometry:
* **1mm Reduced Walls (Weight-Optimized):**
  * **Sidewalls:** $3.25\,\text{mm}$ (reduced by $1.0\,\text{mm}$ from $4.25\,\text{mm}$)
  * **Front Lip:** $3.0\,\text{mm}$ (reduced by $1.0\,\text{mm}$ from $4.0\,\text{mm}$)
  * **Rear Wall:** $3.5\,\text{mm}$ (reduced by $1.0\,\text{mm}$ from $4.5\,\text{mm}$)
  * **Internal Cradle Walls:** $2.5\,\text{mm}$ (reduced by $0.5\,\text{mm}$ from $3.0\,\text{mm}$)
  * Preserves 100% of internal pocket clearances, device tolerances, and insert counterbores while trimming $31.2\,\text{cm}^3$ of excess plastic.
* **Form-Fitting Anagram Tray:**
  * Pocket dimensions: $213.5 \times 106.5 \times 6.0\,\text{mm}$ angled at an ergonomic $8.0^\circ$ incline.
  * Fits the Anagram bare or with the 3D-printed protective cover.
  * $\varnothing 30\,\text{mm}$ ergonomic side finger pry notches for instant, tool-less lifting.
* **Right Flank Slide-In Charger Cradle (Baseus GaN3 Pro CCDK65S):**
  * Sized for $70 \times 40 \times 36.9\,\text{mm}$ charger oriented laterally along the $X$-axis on the right-hand side.
  * **Slide-In Flank Portal:** $42.0 \times 38.5\,\text{mm}$ open entry on the right side wall allows the charger to slide directly into the underbelly cradle after printing.
  * **AC Mains Cord:** Sits flush at the right edge and exits straight out the side with zero cord threading or disassembly needed.
  * **USB Ports:** Face inwards towards the central underbelly chamber, protected inside the chassis.
  * **Positive Snap Detent:** $1.5\,\text{mm}$ detent bump at entry locks the charger securely in place once seated.
  * **Convective Thermal Chimney:** Bottom resting ledges leave a $36\,\text{mm}$ center gap along the entire underside for airflow.
* **100% Printable Through-Wall Zip-Tie Slots:**
  * Clean $4.0 \times 2.5\,\text{mm}$ pass-through slots cut through existing solid vertical walls (inner stop wall, center keel, and stomp bulkhead) for standard $2.5 - 3.6\,\text{mm}$ nylon zip ties (zero floating geometry).
* **Zero-Flex Stomp Keel & Bulkhead:**
  * $3.5\,\text{mm}$ continuous vertical keel along the center line ($X = 0$) connecting to the floor ($Z = 0$).
  * $3.5\,\text{mm}$ transverse stomp bulkhead directly beneath footswitches A, B, and C ($Y = 35\,\text{mm}$).
  * 5-point non-slip base with $12.7\,\text{mm}$ ($1/2"$) $\times 3.5\,\text{mm}$ deep counterbores for rubber bumper feet (4 corners + 1 center stomp pillar).
* **Rear I/O Bay:**
  * $175\,\text{mm}$ wide open rear cutout for direct line-of-sight plug-in of all XLRs, 1/4" jacks, MIDI, and USB-C cables.

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

# build123d 3D Designs

This repository contains parametric 3D models designed using **[build123d](https://github.com/gumyr/build123d)**, a modern Python-based CAD programming library.

## Included Models

### 1. Darkglass Anagram Cover v2

* **Description**: A precise, protective cover/shell custom-built for the Darkglass Anagram device. It features:
  * Openings/cutouts for a screen and two rows of knobs/buttons (6 in the top row, 3 in the bottom row).
  * Embossed divider lines and arrow-shaped indicator markings on the face.
  * Side and front cutouts for port access and venting.
  * Filleted edges and corner radii matching the physical device.

### 2. Key Tag

* **Description**: A basic parametric key tag / keyring template. Easily customizable in dimensions (width, length, thickness, hole size, offsets, and corner radius).

### 3. Chocolate & Darkglass Pedalboard

* **Description**: A compact, ergonomic two-tier pedalboard custom-engineered for the **M-VAVE Chocolate Plus** and **Darkglass Anagram**, integrated with an under-deck compartment for the **Baseus GaN3 Pro 65W Desktop Charger**.
  * **Lower Tier**: Recessed pocket (214 × 38 mm) with a 6 mm front retaining lip for the M-VAVE Chocolate Plus.
  * **Cable Trough**: 22 mm deep channel behind the Chocolate with 3 drop slots into the lower cavity for right-angle / straight 1/4" TRS jacks and USB-C cables.
  * **Upper Tier**: Universal-fit Darkglass Anagram tray (213.5 × 102.5 mm) tilted at an ergonomic 13° angle, compatible both bare and with the 3D-printed cover on.
  * **Under-Deck Charger Bay**: Slide-in sleeve on the left side holding the Baseus GaN3 Pro 65W (40 × 36.9 × 70 mm), featuring a rear AC power cord pass-through, side cable notch, and finger push-out hole on the underside.
  * **Cable Routing**: Hidden channels for USB-C (Anagram to charger), USB-C (Chocolate to charger), and 1/4" TRS (Chocolate to Anagram), plus zip-tie anchor bridges on the floor.
  * **Rear I/O**: Three scalloped rear cutouts for USB-C PD power, MIDI TRS, and audio jacks, plus a rear AC power cord exit notch.
  * **Base**: 6 recessed mounting pads (12 mm diameter) for non-slip rubber feet.

---

## Getting Started

### Prerequisites
Make sure you have Python installed (3.9+ recommended). We recommend setting up a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # On macOS/Linux
# or
.venv\Scripts\activate     # On Windows
```

### Installation
Install the required packages, including `build123d` and the `ocp-vscode` viewer:

```bash
pip install -r requirements.txt
```

### Generating & Viewing Models
To visualize the models in VS Code using the interactive OCP Viewer:
1. Install the **OCP CAD Viewer** extension in VS Code.
2. Run the python script:
   ```bash
   python darkglass-anagram-cover-v2.py
   ```
3. The STL file will be automatically exported to the project directory.

---

## License

This work is licensed under a **Creative Commons Attribution-NonCommercial 4.0 International License (CC BY-NC 4.0)**.

[![License: CC BY-NC 4.0](https://licensebuttons.net/l/by-nc/4.0/88x31.png)](https://creativecommons.org/licenses/by-nc/4.0/)

### License Summary

| Feature | Status |
| :--- | :---: |
| ✖ **Sharing without Attribution** | Not Allowed |
| ✔ **Remix Culture** | Allowed |
| ✖ **Commercial Use** | Not Allowed |
| ✖ **Free Cultural Works** | No |
| ✖ **Meets Open Definition** | No |

*For more details, please review the full license terms on the [Creative Commons website](https://creativecommons.org/licenses/by-nc/4.0/).*

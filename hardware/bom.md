# M-1 Reader — Bill of Materials

The requested ₹4,900–₹10,100 figure is retained as a **target prototype envelope**, not as a current vendor quotation. The v4.1/v4.2 technical report gives a more conservative Raspberry Pi prototype estimate of roughly ₹7,700–₹10,400 using a Camera Module 3, while recommending the Sony IMX219 Camera V2 when matching published reader evidence. Prices must be refreshed before procurement.

| Subsystem | Proposed component | Target cost (₹) | Engineering role | Status |
|---|---|---:|---|---|
| Compute | Raspberry Pi Zero 2 W | 2,200–2,800 | Local image processing, control and audit ledger | Selected architecture |
| Camera | Sony IMX219 / Pi Camera V2 | 1,800–2,800 | Fixed optical geometry and repeatable colour capture | Selected direction; verify current availability |
| Thermal bed | Kapton thin-film heater + thermistor | 250–600 | Controlled cartridge incubation | Prototype target |
| Heat spreader | 2 mm aluminium spreader | 250–500 | Uniform thermal distribution | Proposed |
| Climate sensor | Sensirion SHT31-D | 300–400 | Temperature/humidity feedback | Selected |
| Illumination | High-CRI white LED ring + driver | 200–400 | Controlled spectral illumination | Selected |
| Optical enclosure | PETG light-tight housing + baffles | 400–900 | Ambient-light rejection and fixed geometry | Proposed |
| Diffusion | Matte/holographic diffusion layer | 100–300 | Reduce LED spatial non-uniformity | Proposed; validate optically |
| Power | USB-C PD 5 V / 3 A stage + protection | 500–1,000 | Stable reader/heater supply | Proposed |
| Storage/wiring | microSD, PCB, wiring, fasteners | 400–800 | System integration | Estimate |
| **Target envelope** | **Prototype reader** | **₹4,900–₹10,100** | **Cost target for design trade-off** | **To validate** |

### Why the architecture uses these parts

- **Pi Zero 2 W:** enough local compute for deterministic OpenCV/NumPy/SciPy processing while keeping the reader independent of a phone or cloud service.
- **IMX219:** matches the Camera V2 sensor used in the published Pi-reader evidence discussed in the technical report. Exposure, focus and white balance should be fixed rather than left to automatic camera processing.
- **SHT31-D + heater:** the reaction environment is controlled by feedback rather than assuming ambient temperature is constant. The exact assay set point must be established experimentally; 40 °C is a current engineering target, not a validated assay condition.
- **Aluminium spreader:** prevents a small heater footprint from creating a strong thermal gradient across the cartridge.
- **High-CRI LED ring + sealed bay:** fixes the illumination spectrum and geometry, removing phone-to-phone and room-light variability.
- **PETG housing:** practical for rapid mechanical iteration. Internal surfaces should be matte and non-reflective; external housing material is not part of the analytical validation.
- **USB-C PD:** simplifies field power and allows the reader/heater load to be supplied from a standard power bank or regulated adapter.

### Procurement note

The technical report's earlier quoted BOM was approximately ₹7,700–₹10,400 and explicitly marked several items as estimates. The lower ₹4,900 boundary should therefore be treated as an aggressive target achieved only through component substitution/volume pricing, not as an established build cost.

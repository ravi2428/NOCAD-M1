# Thermal and Optical Engineering Specification

## 1. Optical chamber

The reader should use a **zero-ambient-light measurement bay** rather than trying to computationally remove arbitrary room lighting. A fixed card slot defines the camera-to-card distance and orientation; internal black/matte surfaces and labyrinth-style baffles suppress stray reflections.

### Proposed stack

```text
Camera / IMX219
      ↓
  matte black baffle
      ↓
 high-CRI LED ring
      ↓
 diffusion layer
      ↓
 sealed cartridge plane
```

The optical design target is repeatable irradiance and colour, not maximum brightness. The LED current should be regulated, exposure should be fixed, and the camera should not silently apply auto-white-balance or auto-exposure between reads.

A **holographic/micro-diffuser film** is a proposed refinement for homogenizing the LED ring. It is not required by the current report and must be experimentally screened for spectral transmission, haze, hot-spot suppression and long-term stability before being locked into the design.

## 2. Four-point geometric normalization

Four high-contrast fiducials on the cartridge define the projective transform. The software uses `cv2.getPerspectiveTransform()` followed by `cv2.warpPerspective()` to map the observed card into a fixed analysis plane. This makes the measurement regions independent of moderate card rotation and camera tilt.

The production reader should still constrain the mechanics so the software is correcting residual geometry, not compensating for gross mechanical misalignment.

## 3. Colour measurement

The pipeline converts the corrected image into CIELAB and computes CIE76 ΔE values against printed/reference regions. The blank/reference zone is used as a differential measurement to reduce common matrix/background colour effects.

This is a **matrix compensation mechanism**, not proof that turbidity has been completely removed. Buffalo milk, high-fat milk, dilution and abnormal protein composition must be part of the validation matrix.

## 4. Thermal incubation

### Current engineering target

- Nominal reader set point: **40.0 °C**
- Closed-loop feedback: SHT31-D + heater control
- Thermal interface: Kapton heater bonded to an aluminium spreader
- Design objective: keep the cartridge reaction zone within a narrow, experimentally validated band rather than relying on ambient temperature.

The v4.2 report notes that published AFM1 work uses different conditions, including approximately 37 °C and 45 °C. Therefore **40 °C is not a claimed literature-derived optimum**. The actual M-1 set point must be selected by a dose-response/robustness study on the final cartridge.

### Control strategy

1. Verify cartridge insertion.
2. Check ambient temperature/humidity.
3. Ramp the spreader toward set point.
4. Reject the run if the measured temperature is outside the validated operating window.
5. Start assay timing only after the thermal condition is stable.
6. Capture Lane B at its validated early read window.
7. Capture Lane A at its validated final read window.

## 5. Thermal design checks

Before using the reader on real cartridges, measure:

- warm-up time;
- spatial temperature gradient across the cartridge;
- overshoot and settling time;
- sensor-to-assay-plane offset;
- heater duty cycle at 15–45 °C ambient;
- worst-case battery voltage;
- enclosure internal temperature;
- repeatability across at least three reader assemblies.

The final acceptance limits should come from assay validation, not from arbitrary electronics tolerances.

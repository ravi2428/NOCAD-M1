# NOCAD - M1

**Embedded multi-spectral point-of-care optical reader and offline validation engine for rapid food safety screening.**

[![Tests](https://img.shields.io/badge/Tests-229%20Passing-brightgreen)](#validation-status) [![Edge Latency](https://img.shields.io/badge/Edge%20Latency-0.7s%20Local%20%28ARMv8%29-blue)](#performance-note) [![Compliance](https://img.shields.io/badge/Compliance-FSSAI%20RAFT%20Pathway-orange)](#regulatory-position) [![Zero Cloud](https://img.shields.io/badge/Zero--Cloud-100%25%20Offline-black)](#architecture)

> **Engineering status:** idea-stage proof of work. The current software is validated against mock card images and deterministic test data. No NOCAD reader hardware or physical M-1 cartridge exists yet. Thresholds, calibration coefficients and performance on real milk remain laboratory-validation items.

## What is M-1?

M-1 is the flagship milk cartridge in a reusable reader platform. The cartridge has two analytical lanes:

- **Lane A — competitive nanoparticle immunoassay:** a gold-nanoparticle lateral-flow measurement intended for aflatoxin M1 screening around the 0.5 µg/kg regulatory cutoff.
- **Lane B — colourimetric spot array:** a multiplex array intended to screen selected common milk adulterants, with an optical blank/reference zone used for matrix-aware interpretation.

The reader standardizes the measurement environment with a light-tight optical bay, fixed camera geometry, controlled illumination and a heated cartridge interface. The software runs locally on the reader: image quality and matrix validity are checked **before** quantitation or a screening verdict.

## Architecture

```text
M-1 cartridge
  ├── Lane A: competitive AFM1 strip
  └── Lane B: colourimetric adulterant array + blank
                │
                ▼
      controlled optical reader
      ├── fixed geometry / dark bay
      ├── high-CRI illumination
      ├── camera capture
      └── temperature / humidity checks
                │
                ▼
      deterministic offline pipeline
      ├── 4-point perspective unwarp
      ├── illumination + colour correction
      ├── CIELAB / ΔE measurement
      ├── matrix validity gate
      └── lot-specific 4PL quantitation
                │
                ▼
      PASS / RETEST / SUSPECT / INVALID
                │
                ▼
      SHA-256 hash chain + Ed25519 signature
```

The architecture is deliberately **not described as trained AI**. The current out-of-distribution step is a Mahalanobis statistical distance check fitted from mock valid runs. A future validated model can be introduced only if an independent dataset justifies it.

### Project links

- [Hardware BOM](hardware/bom.md)
- [Thermal and optical specifications](hardware/thermal_optical_specs.md)
- [20-question technical defence](docs/defense_notes_20q.md)
- [Live architecture](docs/index.html)

## Validation status

The repository contains **229 automated software tests** covering perspective correction, matrix rejection, cutoff/grey-zone logic and cryptographic ledger integrity. This number is a software regression count; it is **not** a claim of 229 laboratory samples.

The software build report records mock-data observations: 14 mock sample photos produced their expected verdicts; 17 mock concentration cards followed their drawn levels; 60 mock valid runs were used for the statistical model; and the complete suite reported 229 passing tests. These results establish software behaviour on controlled inputs, not analytical accuracy in real milk.

## Performance note

The software report measured approximately **0.7 s per photo on a laptop**. The repository badge preserves the requested ARMv8 target wording, but **0.7 s on Raspberry Pi Zero 2 W is a design target, not a measured result**.

## Regulatory position

M-1 is a **rapid screening system**, not a replacement for official laboratory analysis. A `SUSPECT` result should trigger formal sampling and confirmatory analysis under the applicable FSSAI process. The FSSAI RAFT pathway is a regulatory development pathway, not a statement that this prototype is already approved or certified.

## Repository layout

```text
NOCAD - M1/
├── README.md
├── requirements.txt
├── hardware/
│   ├── bom.md
│   └── thermal_optical_specs.md
├── src/
│   ├── __init__.py
│   ├── vision_pipeline.py
│   ├── validity_gate.py
│   ├── quant_engine.py
│   └── crypto_audit.py
├── tests/
│   ├── __init__.py
│   └── test_suite.py
└── docs/
    ├── defense_notes_20q.md
    └── index.html
```

## Quick start

Python 3.10+ is recommended.

```bash
python -m venv .venv
python -m pip install -r requirements.txt
python -m pytest -q
```

Expected result for this repository revision: **229 passed**.

## Design guardrails

1. **No real-device claim:** Raspberry Pi, camera, heater and sensor interfaces are the target hardware architecture; driver integration is not yet hardware-validated.
2. **No real-milk accuracy claim:** all current regression tests use mock/deterministic data.
3. **No invented calibration:** 4PL coefficients and Mahalanobis model parameters in a production lot must come from laboratory-generated validation data.
4. **No legal overclaim:** `PASS` means screened within the validated cartridge scope; `SUSPECT` means follow-up, not legal proof.
5. **No cloud dependency:** measurement and audit logic is designed to run without network access.

## Development roadmap

- Build the first optical/thermal reader prototype.
- Characterize IMX219 optics, exposure, flat-field correction and illumination uniformity.
- Validate sample pretreatment and membrane choice on cow, buffalo and high-fat milk.
- Establish lot-specific 4PL curves and independent grey-zone boundaries.
- Fit the Mahalanobis model from real, blinded validation data.
- Add protected key storage/secure element and an external ledger anchor.
- Run independent performance validation for the intended FSSAI/RAFT pathway.

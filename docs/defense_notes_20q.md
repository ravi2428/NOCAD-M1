# M-1 Technical Defence — 20 Questions

These answers are deliberately phrased for a technical review. Where a parameter is not yet experimentally established, the answer says so instead of presenting a design target as a measured result.

## 1. Why use a Raspberry Pi Zero 2 W instead of a phone?
A phone introduces uncontrolled camera processing, lens geometry, exposure, white balance and device-to-device variation. The Pi lets us lock the camera, illumination and processing path. The phone can remain an interface later; the measurement decision belongs on the controlled reader.

## 2. Why the Sony IMX219?
The IMX219 is the sensor used by Raspberry Pi Camera V2, and the technical report selected that direction because published compact Pi optical readers used this camera family. It is not being claimed as uniquely superior. The requirement is repeatable optics, fixed exposure and stable colour response.

## 3. Why a dark optical chamber?
The simplest way to control ambient-light error is to block it mechanically. A sealed bay, matte internal surfaces and baffles make the illumination source and geometry predictable, reducing a major source of measurement variance.

## 4. Why high-CRI LEDs?
The camera is measuring colour, so illumination spectrum matters. A high-CRI source gives a broad, stable visible spectrum. The exact LED part and intensity still need to be locked by optical calibration.

## 5. Why use a diffusion layer or holographic diffuser?
The LED ring can create local hot spots. A diffuser spreads the source and makes card illumination more uniform. A holographic/micro-diffuser is a proposed option, not a proven requirement.

## 6. Why heat the cartridge at all?
Lateral-flow and colour reactions are temperature dependent. Field temperature varies substantially, so a fixed thermal environment can make reaction timing more reproducible.

## 7. Why are we using 40 °C?
40 °C is the current engineering target, not a claim that 40 °C is universally optimal. The reviewed literature includes approximately 37 °C and 45 °C AFM1 workflows. The final set point must come from dose-response, specificity, stability and robustness experiments.

## 8. Why use an aluminium heat spreader under the Kapton heater?
A thin Kapton heater can have a concentrated heat footprint. Aluminium spreads heat laterally and reduces thermal gradients across the cartridge.

## 9. Why does the cartridge need a milk pre-filter?
Milk is not an optical buffer. Fat globules, proteins and suspended material can alter flow and optical background. A **0.45 µm PES membrane is a proposed candidate**, not a validated M-1 specification; it must be tested for flow, analyte recovery, nanoparticle loss and high-fat/buffalo-milk performance.

## 10. Why specifically test buffalo milk?
Buffalo milk can have higher fat and protein content than typical cow milk. These differences can change flow, nonspecific interactions and optical background. Buffalo, mixed and high-fat milk therefore belong in validation.

## 11. Why trehalose or a sugar-glass stabilizer?
The conjugate has to survive drying, humidity and elevated field temperatures. Trehalose and related sugars are established stabilizing excipients for dried biomolecular systems. A sugar-glass formulation alone does not prove six-month shelf life at 45 °C.

## 12. Can we claim reagent survival at 45 °C?
Not yet. 45 °C is a design validation condition, not a demonstrated shelf-life result. The formulation and packaging should undergo real-time and accelerated ageing on the actual cartridge.

## 13. Why use a Mahalanobis validity gate?
Before quantifying a contaminant, the reader must decide whether the image resembles the validated milk/card population. Mahalanobis distance accounts for correlated optical features and is lightweight enough for offline edge computation.

## 14. Why is the validity limit d² ≤ 15.0?
15.0 is the current software gate. It is not a universal statistical constant or laboratory-validated limit. The final threshold must be selected using independent validation data.

## 15. Why does water give INVALID instead of a contaminant result?
The reader should refuse to quantify a sample that does not resemble the validated matrix. In the mock model, water produces approximately d² = 401.7, far outside the valid region. This demonstrates intended software behaviour, not universal real-world performance.

## 16. Why use 4PL regression for AFM1?
Competitive lateral-flow response is nonlinear: as analyte concentration rises, test-line response falls toward a lower asymptote. A four-parameter logistic model captures the upper asymptote, lower asymptote, midpoint and slope.

## 17. Why is there a 0.42–0.58 µg/kg RETEST band around 0.5?
Near a decision threshold, small optical and chemical variation can change classification. A grey zone prevents the reader from claiming more precision than the assay supports. The band must be confirmed using real-cartridge repeatability data.

## 18. What does PASS actually mean?
PASS means **screened within the validated scope** of that cartridge and reader method. It is not a guarantee of safety or a legal laboratory certificate.

## 19. How does the system support legal custody under Section 47?
The screening record is a traceability aid, not the legal sample itself. A SUSPECT result records the run and metadata and prompts the responsible officer to obtain the original food sample through the applicable statutory sampling process and confirm it in an official laboratory.

## 20. What does the cryptographic ledger actually prove?
Each record contains the previous record's hash, its own canonical content hash and an Ed25519 signature. This makes edits, middle-of-chain deletion, reordering and altered payloads detectable when the verification key is trusted. It does not make the record magically immutable; protected key storage and an external anchor are future hardening steps.

## Claims we will not make

- “229 laboratory samples passed.” — False. 229 is the automated software test count.
- “0.7 s on Raspberry Pi Zero 2 W.” — Not measured; the reported timing is on a laptop.
- “FSSAI certified/approved.” — Not true at this stage; RAFT is the intended pathway.
- “AI detects adulteration.” — Current implementation is deterministic image processing plus statistical distance checking.
- “0.45 µm PES is proven optimal.” — Candidate specification awaiting real-milk validation.
- “45 °C storage for six months is proven.” — Validation target only.

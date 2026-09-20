# MagTouch RA three dimensional contact reconstruction

Offline data and models for a five-node soft magnetic tactile sensor. This repository accompanies the manuscript **Magnetic spatial encoding for submillimetre localization and three dimensional contact tracking with a five node soft tactile sensor**.

Repository: https://github.com/googo2025/MagTouch-RA-3d-trajectory-recon

## Reproduce the main numbers

Python 3.10 or newer and NumPy are sufficient. No sensor, printer, camera, serial port, GPU, training service or external dataset is required.

```bash
python -m pip install -r requirements.txt
python scripts/verify_release.py
```

This refits the frozen static regressors and recomputes the dynamic recorded-output metrics. Successful execution ends in `PASS`. It does not control any hardware or overwrite source data.

| Evaluation | Result | Interpretation |
|---|---|---|
| Continuous static planar mean error | 0.288394 mm | 441 contacts in a reserved repeated record |
| Static X / Y / Z MAE | 0.163169 / 0.205812 / 0.031477 mm | Same continuous model and test contacts |
| Sparse 2 mm calibration planar error | 0.349467 mm | Same source pool and reserved record |
| Discrete calibrated-node error | 0.073113 mm | 412 / 441 nodes correct; a different task and training pool |
| XYZ motion mean error | 0.568934 mm | S20260920_A Trial 032; 99.91% valid output coverage |
| Eight-direction planar error | approximately 0.453 mm | Trial 017; causal decoder; full coverage |
| Segmented circle planar error | approximately 0.407 mm | Trial 018 movement only; full-contact error approximately 0.390 mm |

Planar error is mean Euclidean XY distance, not an axis MAE. Motion references are reconstructed from recorded stage commands and segment timing. The circle contains 128 linear segments and inter-segment waits; it is not a constant-speed circle. Different dynamic conditions and models must not be pooled into a single universal accuracy claim.

## Contents

- `data/static/`: contact-level 15-channel delta-B, held-out contact identities, frozen weights and a refitting script.
- `data/dynamic/`: all 39 reviewed records, predictions, command references, invalid counts and the numerical metric checker.
- `models/`: resolved coefficient snapshots and matched configuration diagnostics. These are documented research snapshots, not a hardware-control application.
- `scripts/predict_static.py`: portable continuous static inference and tests against the frozen model.
- `paper/`: editable English manuscript, supplementary methods, rendered PDFs and figures.
- `docs/`: specimen diagrams, model provenance and scope of reproducibility.
- `media/`: supplied original specimen photographs and two clips of recorded-experiment replay.

The compact dynamic export reproduces metrics from logged predictions; it is **not** the full raw magnetic time-series archive and does not by itself rerun the original dynamic acquisition pipeline. The static data do support refitting the two frozen continuous models. Static held-out testing must use the frozen snapshots, not later deployment models that include the test record.

## Scientific naming

CCA: concentric alternating-polarity disc array (internal name 19C).
CPA: checkerboard alternating-polarity disc array (internal name 5x5).
PSM-L / PSM-H: parallel-stripe magnetized sheet with nominal 2.5 / 4.5 mm silicone isolation (internal flot1650 variants).

There are three layouts and four structural configurations. The contact-end diameter is 1 mm. Historical `flat_d6mm` strings do not mean a 6 mm contacting tip. The 121 and 441 labels count calibration positions; there are five electronic sensing nodes in both cases.

## Publication and rights status

This is an anonymous manuscript-preparation release, not a peer-reviewed publication. Author, funding, formulation details and release DOI placeholders remain in the manuscript. See `docs/PUBLICATION_CHECKLIST.md` before submission. No DOI or acceptance is implied.

The author has not yet selected a software/data/media redistribution licence. See `RIGHTS.md`; public availability alone does not grant an MIT or Creative Commons licence. Original replay clips may contain acquisition-interface labels and experiment paths visible in pixels; review the clips before public upload.

## Citation

Until author metadata and an archival release are assigned, cite the repository title, URL, access date and the commit used. Do not invent author names or a DOI. A formal citation file can be added after author approval.

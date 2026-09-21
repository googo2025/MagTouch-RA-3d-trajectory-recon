# MagTouch RA three-dimensional contact reconstruction

Evidence package for the revised manuscript **Magnetic spatial encoding and command-referenced three-dimensional contact trajectory reconstruction with a five-node soft magnetic tactile interface**.

Repository: https://github.com/googo2025/MagTouch-RA-3d-trajectory-recon

The public scope is deliberately the manuscript evidence chain. It includes every record used for a table, figure or numerical claim, but it is not a dump of the complete development history. Aborted trials, exploratory parameter attempts and unpublished configurations remain internal research assets.

## Reproduce the reported results

Python 3.10 or newer and NumPy are sufficient. No sensor, printer, camera, serial port, GPU, training service or external dataset is required.

```bash
python -m pip install -r requirements.txt
python scripts/verify_release.py
```

The command refits the frozen static regressors, checks all 441 reserved contacts, recomputes metrics for the 17 manuscript-used Session III records, verifies the Trial 153/154 repeat-response comparison, recomputes the short unloaded-window statistics, and checks the controlled Trial 178/201 reseating summary. It does not control hardware or overwrite data.

| Evaluation | Result | Scope |
|---|---:|---|
| Continuous static planar mean error | 0.288394 mm | One frozen 441-node DC-RBF; all 441 contacts of reserved Trial 154 at calibrated coordinates and 0.4 mm command depth |
| Static X / Y / Z MAE | 0.163169 / 0.205812 / 0.031477 mm | Same model and test contacts |
| Sparse 2 mm calibration planar error | 0.349467 mm | Same source acquisition and the same test contacts |
| Calibrated-node classification | 412 / 441 correct; 0.073113 mm node error | Separate DPL task and training pool; not continuous resolution |
| Representative XYZ action, Trial 32 | 0.568934 mm | Command-referenced three-dimensional mean error; 99.91% coverage |
| Eight reported representative XYZ actions | 0.569–0.796 mm | Trials 26, 28, 30, 31, 32, 34, 35 and 36; 98.74–100% coverage; not a prospective all-direction benchmark |
| Eight-direction planar action | 0.453 mm | Trial 17; causal decoder; command-referenced |
| Segmented 2 mm circle | 0.407 mm | Trial 18 movement-only value; full-contact value 0.390 mm |

Planar error is mean Euclidean XY distance, not an axis MAE. Motion references are reconstructed from recorded platform commands and timing. These are command-referenced trajectory reconstruction errors, not independently metrologized absolute positioning accuracy. Different tasks and frozen parameter instances are not pooled into one universal accuracy value.

## Contents

- `data/manuscript_record_manifest.json`: machine-readable mapping from manuscript claims to released records and files.
- `data/static/`: contact-level 15-channel delta-B data, held-out identities, frozen models, the Trial 153/154 repeat-response summary and a refitting script.
- `data/dynamic/`: only the 17 Session III records used in the revised manuscript, including all eight representative XYZ actions.
- `data/acquisition/`: per-trial MLX90393 register snapshots and the exact short unloaded windows behind the noise/rate summary.
- `data/depth_repeat/`: recorded predictions, commands and events for S20260919_A Trials 133 and 134.
- `data/remount/`: controlled Trial 178/201 reseating comparison plus the filtered 398-record metadata audit and reassembly timeline.
- `models/`: resolved coefficient snapshots and matched configuration diagnostics. The RBF-labelled branches share one core mapping implementation but use different training pools and frozen parameters; WD-Causal additionally contains a history-residual branch.
- `paper/Manuscript.docx`: revised editable manuscript. `paper/Manuscript.md` and `paper/Supplementary_material.md` provide repository-readable text.
- `scripts/`: portable static inference, release verification and figure generation.
- `docs/` and `media/`: specimen diagrams, reproducibility notes, original photographs and the supplied replay clips cited in the supplementary material.

The compact dynamic export contains recorded predictions and command-derived references rather than every original magnetic time stream. That level is sufficient to reproduce the reported recorded-output metrics. Static data support direct refitting of the two frozen continuous models.

## Scientific naming and hardware snapshot

CCA is the concentric alternating-polarity disc array (internal label 19C), CPA the checkerboard alternating-polarity disc array (internal label 5x5), and PSM-L / PSM-H the parallel-stripe sheet with nominal 2.5 / 4.5 mm isolation. The 121 and 441 labels count calibration positions; all experiments use five electronic sensing nodes.

The 67 successfully decoded per-device snapshots record MLX90393 GAIN 5, HALLCONF 12, RES X/Y/Z 0, DIG FILT 0, OSR/OSR2 0 and TCMP disabled; acquisition logs record a 400 kHz I2C clock. Another 23 readback entries contain diagnostic status errors and are preserved without interpreting them as register values. The decoded snapshots supersede a legacy profile comment that mentioned gain 7.

## Selection and interpretation boundary

The eight compound-action records are representative demonstrations chosen for reporting from the completed research archive. They are not described as preregistered or prospectively defined, and no all-direction success rate is inferred from them. Repeating those same actions could add repeatability evidence but would not remove action-set selection effects. A future confirmatory benchmark would require an independently defined action set and unconditional reporting of that new set.

## Rights and citation

No software, data or media licence is inferred merely from public availability. See `RIGHTS.md`. Until an archival DOI is assigned, cite the repository URL and the release tag `sna-a-revision-2026-09-21`. Author metadata and journal-controlled declarations remain subject to author confirmation.

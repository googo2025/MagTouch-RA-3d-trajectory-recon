# Reproducibility scope

Run:

```bash
python -m pip install -r requirements.txt
python scripts/verify_release.py
```

The offline verification performs five evidence checks:

1. refits the frozen 121- and 441-position continuous static models and evaluates all 441 Trial 154 contacts;
2. verifies the portable static predictor and calibrated-node result;
3. recomputes metrics and coverage from the recorded predictions and command-derived references for the 17 Session III records used by the manuscript;
4. recomputes effective grouped rates and short unloaded-window noise/shift summaries, verifies 67 decoded register snapshots and retains 23 diagnostic readback errors without interpreting them as register values; and
5. checks the released controlled Trial 178/201 reseating comparison.

The Trial 153/154 unit-response comparison is also recomputed from the released contact-level static data. The two Session II z-path folders preserve the recorded predictions, commands and events used for the local depth comparison.

The dynamic export does not retrain the deployed model or regenerate predictions from full raw magnetic streams. It checks the recorded-output metrics actually reported in the paper. The static export does support refitting the two frozen continuous models. The release boundary is documented in `data/manuscript_record_manifest.json`.

`python -m pip install -r requirements-figures.txt` followed by `python scripts/make_figures.py` regenerates the five numerical/geometry figure sets and graphical abstract from released data. Figures distinguish qualitative polarity schematics from measured results.

Motion errors are referenced to programmed and time-interpolated platform trajectories. No independent external position instrument was used, so the release does not claim absolute metrological positioning accuracy. The eight representative XYZ actions are not a preregistered all-direction benchmark.

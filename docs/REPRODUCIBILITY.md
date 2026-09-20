# Reproducibility scope

`python scripts/verify_release.py` refits the two frozen continuous static models,
checks all 441 reserved contacts and verifies the portable prediction function.
It also recomputes 236 quantities from 39 recorded dynamic experiments.

`python -m pip install -r requirements-figures.txt` followed by
`python scripts/make_figures.py` regenerates all five English numerical/geometry
figures and the graphical abstract from the released data and nominal dimensions.

Dynamic models are included as parameter snapshots. Dynamic metric reproduction
uses recorded prediction arrays and command-derived references, not fresh raw-field
inference. No original source videos are converted into numerical ground truth.
Original experiment folders and full magnetic streams are not distributed here.

Frozen static model identifiers `current_only121` and `current_only441` correspond
to SC-RBF and DC-RBF in the reserved-repeat test. Later similarly named production
models have different training sets. See Supplementary Table S1 before reusing them.

The figures distinguish qualitative polarity schematics from measured responses.
Videos S1 and S2 are original clips of the experiment replay interface, not
synthetic demonstrations or new acquisition runs.

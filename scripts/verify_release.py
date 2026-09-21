"""Run all offline checks; no hardware or network operations."""
import os
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS'):os.environ[key]='4'
import json
import subprocess
import sys
from pathlib import Path
import numpy as np
from predict_static import predict

ROOT=Path(__file__).resolve().parents[1]
for script in [
    'data/static/reproduce_static_results.py',
    'data/dynamic/reproduce_motion_metrics.py',
    'data/acquisition/reproduce_acquisition_summary.py',
    'data/remount/reproduce_remount_summary.py',
]:
    subprocess.run([sys.executable,str(ROOT/script)],check=True)
models=json.loads((ROOT/'data/static/frozen_static_model_parameters.json').read_text(encoding='utf8'))
contacts=json.loads((ROOT/'data/static/static_reproduction_contacts.json').read_text(encoding='utf8'))['test_contacts']
d=[r['delta'] for r in contacts];q=np.array([[r['x'],r['y'],r['depth']] for r in contacts])
p=predict(d,models['current_only441']);axis=np.abs(p-q).mean(axis=0)
assert np.allclose(axis,[.163168897,.205812498,.031477144],atol=1e-8,rtol=0)
for bad in ([0]*15,[1]*14,[float('nan')]*15):
    try:predict(bad,models['current_only441'])
    except ValueError:pass
    else:raise AssertionError('Invalid decoder input accepted')
assert len(contacts)==441
manifest=json.loads((ROOT/'data/manuscript_record_manifest.json').read_text(encoding='utf8'))
assert [r['trial_id'] for r in manifest['session_iii_dynamic']]==[4,5,17,18,19,20,26,28,30,31,32,34,35,36,37,38,39]
assert (ROOT/'paper/Manuscript.docx').is_file()
assert (ROOT/'data/depth_repeat/S20260919_A_Trial_133/live_predictions.csv').is_file()
assert (ROOT/'data/depth_repeat/S20260919_A_Trial_134/live_predictions.csv').is_file()
print('PASS: revised manuscript evidence package and all offline checks.')

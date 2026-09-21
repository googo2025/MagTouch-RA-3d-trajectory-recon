"""Offline recomputation from exported recorded predictions and command references.

This verifies the reported metrics. It does not retrain or re-run inference,
connect hardware, or modify the original acquisition data. Requires NumPy.
"""
from pathlib import Path
import json
import numpy as np

rows=json.loads((Path(__file__).resolve().parent/'analysis_results.json').read_text(encoding='utf-8'))
checks=0
for row in rows:
    for key in ('motion','arc_with_command_holds'):
        m=row.get(key,{})
        if not m.get('n'):continue
        segments=[s for s in m['segments'] if s['n']]
        p=np.vstack([s['prediction'] for s in segments]);q=np.vstack([s['reference'] for s in segments])
        e=p-q
        values={'xy_mae':np.linalg.norm(e[:,:2],axis=1).mean(),'z_mae':np.abs(e[:,2]).mean(),
                'xyz_mae':np.linalg.norm(e,axis=1).mean(),'coverage':len(p)/sum(s['total'] for s in m['segments'])}
        for name,value in values.items():
            assert np.isclose(value,m[name],atol=1e-10,rtol=0),(row['trial_id'],key,name,value,m[name])
            checks+=1
        if row['trial_id'] in (17,18,20,26,28,30,31,32,34,35,36):
            print(f"Trial {row['trial_id']:03d} {key}: XYZ={values['xyz_mae']:.6f} mm, coverage={values['coverage']:.6%}")
    hs=row.get('hold_summary')
    if hs:
        h=[s for s in row['holds'] if s.get('predicted_xyz_mm') is not None]
        e=np.array([s['predicted_xyz_mm'] for s in h])-np.array([s['truth_xyz_mm'] for s in h])
        assert np.isclose(np.linalg.norm(e[:,:2],axis=1).mean(),hs['xy_mae'],atol=1e-10)
        assert np.isclose(np.abs(e[:,2]).mean(),hs['z_mae'],atol=1e-10)
        checks+=2
expected={4,5,17,18,19,20,26,28,30,31,32,34,35,36,37,38,39}
assert len(rows)==17
assert {r['trial_id'] for r in rows}==expected
assert all(r['disposition']=='reported_in_manuscript' for r in rows)
print(f'PASS: {checks} numerical checks; 17 manuscript-used Session III records.')

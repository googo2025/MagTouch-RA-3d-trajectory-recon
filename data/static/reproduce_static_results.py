"""Offline reproduction: only NumPy and the two neighboring JSON files.

Fits the preserved 121/441 models at frozen hyperparameters and tests all 441
reserved contacts. Does not connect hardware, require the project, or edit files.
"""
import os
for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS'):
    os.environ[name]='4'
import json
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parent
models=json.loads((ROOT/'frozen_static_model_parameters.json').read_text(encoding='utf-8'))
fixture=json.loads((ROOT/'static_reproduction_contacts.json').read_text(encoding='utf-8'))

def arrays(rows):
    d=np.array([r['delta'] for r in rows],float)
    a=np.linalg.norm(d,axis=1)
    return d,d/np.maximum(a[:,None],1e-12),np.array([[r['x'],r['y']] for r in rows]),np.array([r['depth'] for r in rows])

def z_features(delta,kind):
    a=np.linalg.norm(delta,axis=1);u=delta/np.maximum(a[:,None],1e-12);v=np.log(np.maximum(a,1e-6))
    if kind=='unit_logamp':return np.c_[u,v,v*v,u*v[:,None]]
    if kind=='delta_logamp':return np.c_[delta,v,v*v]
    raise ValueError(kind)

def predict(mx,mz,delta):
    a=np.linalg.norm(delta,axis=1);u=delta/np.maximum(a[:,None],1e-12)
    centers=np.array(mx['centers']);dist=np.sum((u[:,None]-centers[None])**2,axis=2)
    xy=np.exp(-mx['gamma']*dist)@np.array(mx['alpha'])
    f=z_features(delta,mz['feature'])
    z=np.c_[(f-np.array(mz['mean']))/np.array(mz['scale']),np.ones(len(f))]@np.array(mz['coef'])
    return np.c_[xy,z]

td,tu,txy,tz=arrays(fixture['test_contacts'])
truth=np.c_[txy,tz]
train_ids={r['trial'] for r in fixture['training_pool']}
assert train_ids.isdisjoint({r['trial'] for r in fixture['test_contacts']})
assert len(td)==441
for name in ('current_only121','current_only441'):
    rows=fixture['training_pool']
    if name=='current_only121':rows=[r for r in rows if abs(r['x']%2)<1e-9 and abs(r['y']%2)<1e-9]
    d,u,xy,z=arrays(rows);hp=models[name]['hyperparameters']
    nodes=np.unique(xy,axis=0)
    centers=np.array([u[np.all(xy==p,axis=1)].mean(axis=0) for p in nodes])
    centers/=np.linalg.norm(centers,axis=1)[:,None]
    K=np.exp(-hp['xy_gamma']*np.sum((centers[:,None]-centers[None])**2,axis=2))
    alpha=np.linalg.solve(K+hp['xy_lambda']*np.eye(len(K)),nodes)
    f=z_features(d,hp['z_feature']);mean=f.mean(axis=0);scale=f.std(axis=0);scale[scale<1e-6]=1
    T=np.c_[(f-mean)/scale,np.ones(len(f))];D=np.eye(T.shape[1]);D[-1,-1]=0
    coef=np.linalg.solve(T.T@T+hp['z_lambda']*D,T.T@z)
    mx={'gamma':hp['xy_gamma'],'centers':centers,'alpha':alpha}
    mz={'feature':hp['z_feature'],'mean':mean,'scale':scale,'coef':coef}
    pred=predict(mx,mz,td)
    saved=predict(models[name]['continuous_xy_model'],models[name]['continuous_z_model'],td)
    assert np.max(np.abs(pred-saved))<1e-7
    err=pred-truth
    metrics={'model':name,'train_contacts':len(rows),'test_contacts':len(td),
        'axis_mae_mm':np.abs(err).mean(axis=0).tolist(),'xy_mae_mm':float(np.linalg.norm(err[:,:2],axis=1).mean())}
    print(json.dumps(metrics,ensure_ascii=False))

p=models['DPL'];nodes=np.array(p['nodes']);cal=np.array(p['amplitude_depth_slope_intercept'])
scores=np.column_stack([(tu@np.array(bank).T).max(axis=1) for bank in p['unit_template_banks']])
j=scores.argmax(axis=1);xy=nodes[j];z=(np.linalg.norm(td,axis=1)-cal[j,1])/np.maximum(cal[j,0],1e-9)
print(json.dumps({'model':'DPL','test_contacts':len(td),'correct_nodes':int(np.all(xy==txy,axis=1).sum()),
    'xy_mae_mm':float(np.linalg.norm(xy-txy,axis=1).mean()),'z_mae_mm':float(np.abs(z-tz).mean())},ensure_ascii=False))
print('PASS: frozen fitting and all reserved contacts reproduced without hardware access.')

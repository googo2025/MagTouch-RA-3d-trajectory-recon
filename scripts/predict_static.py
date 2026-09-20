"""Portable frozen continuous decoder. Input: N x 15 baseline-subtracted uT."""
import argparse
import json
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]

def predict(delta,model):
    d=np.asarray(delta,dtype=float)
    if d.ndim==1:d=d[None,:]
    if d.ndim!=2 or d.shape[1]!=15 or not np.all(np.isfinite(d)):
        raise ValueError('Expected finite N x 15 baseline-subtracted magnetic channels.')
    a=np.linalg.norm(d,axis=1)
    if np.any(a<=1e-12):raise ValueError('Zero-amplitude input has no reliable contact direction.')
    u=d/a[:,None];mx=model['continuous_xy_model'];mz=model['continuous_z_model']
    centres=np.asarray(mx['centers']);xy=np.exp(-mx['gamma']*((u[:,None]-centres[None])**2).sum(axis=2))@np.asarray(mx['alpha'])
    v=np.log(np.maximum(a,1e-6));kind=mz['feature']
    if kind=='unit_logamp':f=np.c_[u,v,v*v,u*v[:,None]]
    elif kind=='delta_logamp':f=np.c_[d,v,v*v]
    else:raise ValueError('Unsupported frozen depth feature: '+kind)
    f=(f-np.asarray(mz['mean']))/np.asarray(mz['scale'])
    z=np.c_[f,np.ones(len(f))]@np.asarray(mz['coef'])
    return np.c_[xy,z]

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input',type=Path,help='JSON array with one or more 15-channel delta-B vectors')
    parser.add_argument('--model',choices=['current_only121','current_only441'],default='current_only441')
    args=parser.parse_args()
    bank=json.loads((ROOT/'data/static/frozen_static_model_parameters.json').read_text(encoding='utf8'))
    d=json.loads(args.input.read_text(encoding='utf8'))
    print(json.dumps(predict(d,bank[args.model]).tolist()))

if __name__=='__main__':main()

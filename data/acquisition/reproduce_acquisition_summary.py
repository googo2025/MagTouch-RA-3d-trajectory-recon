"""Recompute grouped rates and short unloaded-window statistics."""
from pathlib import Path
import json
import numpy as np

ROOT=Path(__file__).resolve().parent
data=json.loads((ROOT/'baseline_windows_and_hardware.json').read_text(encoding='utf-8'))
reported=data['summary']
total_decoded_configs=0;total_diagnostic_errors=0
for session in reported:
    rates=[];sds=[];shifts=[];windows=0;decoded_configs=0;diagnostic_errors=0
    for record in data['records']:
        if record['session']!=session:continue
        rates.append(record['effective_grouped_rate_hz'])
        configs=record['sensor_configs']
        assert len(configs)==5
        for c in configs:
            if 'error' in c:
                diagnostic_errors += 1
                continue
            assert (c['gain'],c['hallconf'],c['res_x'],c['res_y'],c['res_z'],c['filter'],c['osr'],c['osr2'],c['tcmp'])==(5,12,0,0,0,0,0,0,False)
            decoded_configs += 1
        for window in record['windows']:
            v=np.asarray(window['values_uT'],float);windows+=1
            assert v.ndim==2 and v.shape[1]==15 and len(v)>=6
            sds.extend(np.std(v,axis=0,ddof=1))
            n=max(2,len(v)//3)
            shifts.extend(np.abs(np.median(v[-n:],axis=0)-np.median(v[:n],axis=0)))
    got={
        'records':len(rates),'windows':windows,
        'effective_grouped_rate_hz':{'median':float(np.median(rates)),'min':float(np.min(rates)),'max':float(np.max(rates))},
        'within_window_channel_sd_uT':{'median':float(np.median(sds)),'p95':float(np.percentile(sds,95))},
        'short_window_channel_shift_uT':{'median':float(np.median(shifts)),'p95':float(np.percentile(shifts,95))},
    }
    for key in ('records','windows'):assert got[key]==reported[session][key]
    for group in ('effective_grouped_rate_hz','within_window_channel_sd_uT','short_window_channel_shift_uT'):
        for key,value in got[group].items():assert np.isclose(value,reported[session][group][key],atol=1e-9,rtol=0)
    print(session,json.dumps(got,ensure_ascii=False),f'decoded_configs={decoded_configs}',f'diagnostic_errors={diagnostic_errors}')
    total_decoded_configs += decoded_configs
    total_diagnostic_errors += diagnostic_errors
assert total_decoded_configs == 67 and total_diagnostic_errors == 23
print('PASS: 67 decoded hardware snapshots, 23 recorded diagnostic readback errors, effective rates and short unloaded-window statistics reproduced.')

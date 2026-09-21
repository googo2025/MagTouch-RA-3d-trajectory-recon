"""Verify the released controlled 19C reseating summary."""
from pathlib import Path
import csv,json
import numpy as np

ROOT=Path(__file__).resolve().parent
comparison=json.loads((ROOT/'comparison.json').read_text(encoding='utf-8'))
paired=json.loads((ROOT/'paired_contacts.json').read_text(encoding='utf-8'))
with (ROOT/'summary_metrics.csv').open(encoding='utf-8-sig',newline='') as fh:
    summary={row['metric']:row for row in csv.DictReader(fh)}
assert comparison['old']['contacts']==126 and comparison['new']['contacts']==126
assert comparison['old']['positions']==63 and comparison['new']['positions']==63
assert len(paired)==126
assert np.isclose(float(summary['response_amplitude_median']['old_not_seated']),comparison['old']['response_amplitude_uT']['median'],atol=5e-4)
assert np.isclose(float(summary['response_amplitude_median']['new_repressed']),comparison['new']['response_amplitude_uT']['median'],atol=5e-4)
assert comparison['old']['magnitude_fall_90_10_ms']['n']==2
assert comparison['new']['magnitude_fall_90_10_ms']['n']==126
ratio=np.median([row['new_over_old_amplitude'] for row in paired])
assert np.isclose(ratio,float(summary['new_over_old_response_amplitude']['new_repressed']),atol=5e-5)
print('PASS: controlled Trial 178/201 reseating comparison summary verified.')

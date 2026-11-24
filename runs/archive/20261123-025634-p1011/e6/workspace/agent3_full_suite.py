"""Recompute agent3's exact algebraic certificates from their generators.
This suite does not claim to computationally verify elliptic theorems.
"""
from pathlib import Path
from time import perf_counter
from hashlib import sha256
import json
scripts=['agent3_source_kernel_checks.py','agent3_odd_gram_checks.py','agent3_symbolic_q2_generate.py','agent3_symbolic_trans_generate.py','agent3_seed19_checks.py','agent3_seed19_alln_checks.py']
report=[]
for name in scripts:
 p=Path('workspace')/name
 source=p.read_text();start=perf_counter()
 exec(compile(source,str(p),'exec'),{'__name__':'__main__','__file__':str(p)})
 elapsed=perf_counter()-start
 report.append({'script':name,'sha256':sha256(source.encode()).hexdigest(),'passed':True,'seconds':elapsed})
 print('PASSED',name,elapsed,flush=True)
Path('workspace/agent3_full_suite_report.json').write_text(json.dumps(report,indent=2)+'\n')
print('All agent3 exact algebra certificates passed after full regeneration.')

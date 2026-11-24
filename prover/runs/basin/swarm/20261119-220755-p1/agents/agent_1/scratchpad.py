from pathlib import Path
import json,hashlib,zipfile,runpy,os
r=Path('workspace');mp=r/'PROOF_MANIFEST.json';man=json.loads(mp.read_text());f='agent2_rational_positive_eq_0.4.npz';man[f]=hashlib.sha256((r/f).read_bytes()).hexdigest();mp.write_text(json.dumps(dict(sorted(man.items())),indent=2))
with zipfile.ZipFile(r/'restarted_cg_threshold_proof.zip','w',zipfile.ZIP_DEFLATED) as z:
 for f in sorted(list(man)+['PROOF_MANIFEST.json']):z.write(r/f,arcname='workspace/'+f)
base=(r/'reproduction_check').resolve()
with zipfile.ZipFile(r/'restarted_cg_threshold_proof.zip') as z:z.extractall(base)
os.chdir(base)
for f,sha in man.items():assert hashlib.sha256(Path('workspace',f).read_bytes()).hexdigest()==sha
runpy.run_path('workspace/run_final_checks.py',run_name='__main__')
print('STANDALONE ARCHIVE REPRODUCTION PASS:',len(man),'SHA256 entries verified.')
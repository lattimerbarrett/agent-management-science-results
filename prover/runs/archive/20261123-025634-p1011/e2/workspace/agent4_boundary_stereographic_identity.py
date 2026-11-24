from pathlib import Path
import contextlib, io, hashlib, json
files=['agent2_n21_standalone_certificate.py','agent2_center_decomposition.py','agent2_dtn_ode_check.py','agent4_boundary_stereographic_identity.py','agent3_graph_metric_checks.py','agent4_kernel_prefactors.py','agent4_general_moments.py']
manifest=[]
for name in files:
 p=Path('workspace')/name;src=p.read_text();out=io.StringIO()
 with contextlib.redirect_stdout(out):exec(compile(src,str(p),'exec'),{'__name__':'__main__'})
 row={'file':str(p),'sha256':hashlib.sha256(src.encode()).hexdigest(),'stdout':out.getvalue(),'status':'passed'}
 manifest.append(row)
 print(name+': PASSED')
 print(out.getvalue().strip())
Path('workspace/agent1_final_verification.json').write_text(json.dumps(manifest,indent=2))

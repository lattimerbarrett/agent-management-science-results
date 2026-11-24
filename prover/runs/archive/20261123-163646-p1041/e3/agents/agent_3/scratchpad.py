from pathlib import Path
p=Path('workspace/agent3_final_global_proof.txt');s=p.read_text().replace('The consolidated ambient14 proof is being saved by agent4 as well.','The complete consolidated proof, including the odd-puncture moment proof,\nis agent4_m14_unconditional_proof.txt; its independent arithmetic checker\nis agent4_verify_m14_unconditional.py.');p.write_text(s)
import runpy,time,contextlib,io,hashlib,json
files=['agent1_final_certificate.py','agent3_verify_low.py','agent2_verify_central.py','agent2_verify_relative_gaps.py','agent4_group_algebra.py','agent2_verify_bootstrap15.py','agent4_verify_derivative_bootstrap.py','agent4_verify_m14_unconditional.py','agent3_verify_three_flat.py','agent1_verify_min256_lemma.py']
manifest=[]
for name in files:
 p=Path('workspace')/name;buf=io.StringIO();start=time.time()
 with contextlib.redirect_stdout(buf):runpy.run_path(str(p),run_name='__main__')
 entry=dict(file=name,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),seconds=time.time()-start,status='PASS',stdout=buf.getvalue());manifest.append(entry);print(name,'PASS',round(entry['seconds'],3),flush=True)
proofs={n:hashlib.sha256((Path('workspace')/n).read_bytes()).hexdigest() for n in ['agent3_final_global_proof.txt','agent4_m14_unconditional_proof.txt','agent2_constantQ15_unconditional_proof.txt']}
Path('workspace/agent3_final_audit_manifest.json').write_text(json.dumps(dict(status='COMPLETE proof integration; all executed checks PASS. Classical strictKT/KTA numeric theorems explicitly external, not codeword enumeration.',checks=manifest,proof_hashes=proofs),indent=2))
print('FINAL MANIFEST SAVED')

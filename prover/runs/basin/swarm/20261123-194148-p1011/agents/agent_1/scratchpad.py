from pathlib import Path
p=Path('workspace/agent1_global_reduction.md');t=p.read_text();t=t.replace('If an interior bubble has boundary distance d_i->0 but d_i/epsilon_i->infinity, rescale by d_i.','For an interior center drifting to boundary use the MINIMUM of its nearest-\nneighbor distance and its boundary distance as the intermediate scale. If the\nneighbor distance is smaller/comparable the multipole argument applies first;\notherwise the boundary-distance rescaling is isolated. In the latter case,\nif d_i->0 and d_i/epsilon_i->infinity, rescale by d_i.')
p.write_text(t)
# Refresh the assembled proof with all peercheck corrections.
out=Path('workspace/final');parts=['agent1_geometric_lemmas.md','agent1_shape_taylor_bounds.md','agent2_local_sign_lemma.md','agent1_global_reduction.md','agent4_construction_lemma.md']
old=(out/'boundary_yamabe_proof.md').read_text();intro=old.split('\n\n---\n\n')[0];appendix=old[old.rfind('\n\n---\n\n# Algebraic certificates'):]
text=intro+''.join('\n\n---\n\n'+(Path('workspace')/f).read_text() for f in parts)+appendix
(out/'boundary_yamabe_proof.md').write_text(text)
import zipfile
runner="from pathlib import Path\nexec(compile(Path('workspace/agent3_run_all_checks.py').read_text(),'workspace/agent3_run_all_checks.py','exec'),{'__name__':'__main__'})\nexec(compile(Path('workspace/agent1_exact_finite_minima.py').read_text(),'workspace/agent1_exact_finite_minima.py','exec'),{'__name__':'__main__'})\nprint('ALL CHECKS PASSED')\n"
with zipfile.ZipFile(out/'boundary_yamabe_certificates.zip','w',zipfile.ZIP_DEFLATED) as z:
 z.writestr('run_checks.py',runner);z.writestr('proof.md',text)
 for q in Path('workspace').glob('*.py'):z.write(q,'workspace/'+q.name)
 for f in parts:z.write(Path('workspace')/f,'workspace/'+f)
print('Final assembled proof:',len(text),'characters; zip refreshed with all corrected scripts.')
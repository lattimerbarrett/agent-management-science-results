from pathlib import Path
src=Path('workspace/agent1_purity_connected_search.py').read_text()
src=src.replace("print('encoded',len(s.assertions()),flush=True);start=time.time()",'''# Facet-ridge adjacency must be connected for a shellable input.
fl=[z3.Int('facetlevel%d'%i) for i in range(len(F))]
s.add(fl[0]==0)
for i,g in enumerate(F):
    if i==0:continue
    s.add(fl[i]>=1,fl[i]<=len(F))
    s.add(z3.Implies(X[i],z3.Or([z3.And(X[j],fl[j]<fl[i]) for j,h in enumerate(F) if j!=i and (h&g).bit_count()==3])))
print('encoded',len(s.assertions()),flush=True);start=time.time()''')
src=src.replace('for it in range(100):','for it in range(10000):')
# Quiet unless model edge-KD succeeds, avoiding excessive log.
src=src.replace("print('result',res,'time',time.time()-start,flush=True)","print('result',res,'time',time.time()-start,flush=True) if it%100==0 or res!=z3.sat else None")
src=src.replace("print('facets',len(fs),'kd?',kd(fs,1),flush=True)","print('facets',len(fs),'kd?',kd(fs,1),flush=True) if it%100==0 else None")
Path('workspace/agent1_purity_strong_search.py').write_text(src)
exec(compile(src,'workspace/agent1_purity_strong_search.py','exec'))

from pathlib import Path
import json,itertools as it
record=json.loads(Path('workspace/agent4_partial_cover_saturation.json').read_text())[0]
cores=list(map(set,record['cores']));H=list(map(set,record['family']));V=set(range(record['n']));t=4
owner=[]
for E in H:
 src=[j for j,X in enumerate(cores) if X<=E];assert len(src)==1;owner.append(src[0])
cs=[set(C) for C in it.combinations(V,t) if all(set(C)&E for E in H)]
cert=[];count=0
for C in cs:
 for i,X in enumerate(cores):
  if 2<=len(C&X)<len(X):
   for v in C&X:
    choices=[j for j,E in enumerate(H) if E&C=={v}];assert choices
    for ej in choices:
     E=H[ej];j=owner[ej];assert j!=i
     for u in X-C:
      replacement=(E-{v})|{u}
      gs=[g for g,G in enumerate(H) if not G&replacement]
      assert gs
      g=gs[0];G=H[g];l=owner[g]
      assert E&G=={v} and len({i,j,l})==3
      cert.append({'cover':sorted(C),'core':i,'v':v,'u':u,'E':sorted(E),'G':sorted(G),'owners':[i,j,l]});count+=1
Path('workspace/agent2_partial_cover_private_checks.py').write_text(Path('scratchpad.py').read_text());Path('workspace/agent2_partial_cover_private_checks.json').write_text(json.dumps({'minimum_covers':len(cs),'cases':count,'certificates':cert},indent=2));print('mincovers',len(cs),'all_private_replacement_cases',count);print(cert[:2])

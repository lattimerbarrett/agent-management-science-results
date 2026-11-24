import sys,json,pickle
sys.path.insert(0,'workspace')
import agent2_all_loop_cubic as a
from agent2_cubic_source import magnus3
from agent2_sparse_closure import apply
import sympy as S
from sympy.matrices.normalforms import smith_normal_form
from sympy.polys.domains import ZZ
from collections import Counter
L=a.d.L;added=0
for rec in json.load(open('workspace/agent3_magnus_as_nielsen.json'))['words']:
    t=rec['generator_index'];images=a.image(tuple(rec['endo_word']))
    for u in range(9):
        P=images[u];Q={w:c for w,c in magnus3((t+1,u+1,-t-1),9).items() if w}
        e={w:c for w,c in P.items() if len(w)==1};assert e=={w:c for w,c in Q.items() if len(w)==1}
        R={w:P.get(w,0)-Q.get(w,0) for w in P.keys()|Q.keys()};r2={w:c for w,c in R.items() if len(w)==2 and c}
        for w,c in r2.items():
            for v,d in e.items():R[w+v]=R.get(w+v,0)-c*d
        added+=L.insert(a.d.vector(R))
print('Peiffer identity rows added',added,flush=True)
idx=0
while idx<len(L.queue):
    v=L.queue[idx];idx+=1
    for k in range(9):L.insert(a.d.comm(v,k))
    for act in a.d.acts:L.insert(apply(act,v))
C={p-81:{i-81:c for i,c in v.items()} for p,v in L.b.items() if p>=81};M=S.zeros(729,len(C))
for j,v in enumerate(C.values()):
    for i,c in v.items():M[i,j]=c
D=smith_normal_form(M,domain=ZZ);ds=[abs(D[i,i]) for i in range(len(C))]
print('PEIFFER SOURCE cubic rank',len(C),'SNF',dict(Counter(ds)),flush=True)
pickle.dump(C,open('workspace/agent2_peiffer_cubic.pkl','wb'))

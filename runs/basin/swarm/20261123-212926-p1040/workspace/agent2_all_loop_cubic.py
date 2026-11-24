import sys,json,time,pickle
sys.path.insert(0,'workspace')
import agent2_direct_lpres_cubic as d
from functools import lru_cache
from itertools import product
from agent2_cubic_source import magnus3
from agent2_sparse_closure import apply
import sympy as S
from sympy.matrices.normalforms import smith_normal_form
from sympy.polys.domains import ZZ
from collections import Counter
N=9;data=json.load(open('workspace/agent3_aut_action_loops.json'));start=time.time()
def mul(a,b):
    v={}
    for x,c in a.items():
        for y,e in b.items():
            if len(x)+len(y)<=3:v[x+y]=v.get(x+y,0)+c*e
    return {x:c for x,c in v.items() if c}
actions=[]
for e in d.data['endomorphisms']:
    qs=[{u:c for u,c in magnus3(tuple(w[::-1]),N).items() if u} for w in e['images']]
    A={}
    for i in range(N):A[(i,)]=qs[i]
    for i,j in product(range(N),repeat=2):A[i,j]=mul(qs[i],qs[j])
    for i,j,k in product(range(N),repeat=3):A[i,j,k]=mul(A[i,j],qs[k])
    actions.append(A)
def transform(A,p):
    out={}
    for u,c in p.items():
        for v,e in A[u].items():out[v]=out.get(v,0)+c*e
    return {v:c for v,c in out.items() if c}
@lru_cache(None)
def image(word):
    if not word:return tuple({(i,):1} for i in range(N))
    A=actions[word[-1]]
    return tuple(transform(A,p) for p in image(word[:-1]))
added=0
for idx,(wa,wb) in enumerate(data['loops']):
    pa=image(tuple(wa));pb=image(tuple(wb))
    for k in range(N):
        e={u:c for u,c in pa[k].items() if len(u)==1}
        assert e=={u:c for u,c in pb[k].items() if len(u)==1}
        p={u:pa[k].get(u,0)-pb[k].get(u,0) for u in pa[k].keys()|pb[k].keys()}
        p2={u:c for u,c in p.items() if len(u)==2 and c}
        for u,c in p2.items():
            for v,a in e.items():p[u+v]=p.get(u+v,0)-c*a
        if d.L.insert(d.vector(p)):added+=1
    if idx%500==0:print('loops',idx,'added',added,'cache',image.cache_info(),'secs',time.time()-start,flush=True)
print('Loops added',added,flush=True)
idx=0
while idx<len(d.L.queue):
    v=d.L.queue[idx];idx+=1
    for k in range(N):d.L.insert(d.comm(v,k))
    for act in d.acts:d.L.insert(apply(act,v))
C={p-81:{i-81:c for i,c in v.items()} for p,v in d.L.b.items() if p>=81};M=S.zeros(729,len(C))
for j,v in enumerate(C.values()):
    for i,c in v.items():M[i,j]=c
Diag=smith_normal_form(M,domain=ZZ);ds=[abs(Diag[i,i]) for i in range(len(C))]
print('ALL-LOOP SOURCE cubic rank',len(C),'SNF',dict(Counter(ds)),'time',time.time()-start,flush=True)
pickle.dump(C,open('workspace/agent2_all_loop_cubic.pkl','wb'))

import sys,pickle,time
sys.path.insert(0,'workspace')
from agent2_cubic_source import IntegralLattice,magnus3,compose
from agent2_cubic_nonlinear_closure import actions
from agent2_source_relations import generators,extend,inv
from agent2_sparse_closure import apply
from itertools import combinations
import sympy as S
from sympy.matrices.normalforms import smith_normal_form
from sympy.polys.domains import ZZ
from collections import Counter
N=9;off=81;G=generators(3);unit=((1,),(2,),(3,));start=time.time()
seen={unit:()};layer=[(unit,())]
for d in range(1,4):
    nxt=[]
    for A,w in layer:
        for a,g in enumerate(G):
            B=extend(A,g,1);ww=w+(a+1,)
            if B not in seen:seen[B]=ww;nxt.append((B,ww))
    layer=nxt
print('positive ball3 size',len(seen),flush=True)
L=IntegralLattice()
for v in pickle.load(open('workspace/agent2_ia3_mixed_relations.pkl','rb')).values():L.insert(v)
for v in pickle.load(open('workspace/agent2_ia3_cubic_relations.pkl','rb')).values():L.insert({i+off:c for i,c in v.items()})
count=0;added=0
for (A,u),(B,v) in combinations(seen.items(),2):
    if compose(A,B)!=compose(B,A):continue
    count+=1;p=magnus3(u+v+inv(u)+inv(v),N);vec={}
    for w,c in p.items():
        if len(w)==2:vec[w[0]*N+w[1]]=c
        elif len(w)==3:vec[off+(w[0]*N+w[1])*N+w[2]]=c
    if L.insert(vec):added+=1
print('commuting pairs',count,'added',added,'rank',len(L.b),'time',time.time()-start,flush=True)
acts=actions();idx=0
while idx<len(L.queue):
    v=L.queue[idx];idx+=1
    for act in acts:L.insert(apply(act,v))
C={p-off:{i-off:c for i,c in v.items()} for p,v in L.b.items() if p>=off}
M=S.zeros(729,len(C))
for j,v in enumerate(C.values()):
    for i,c in v.items():M[i,j]=c
D=smith_normal_form(M,domain=ZZ);ds=[abs(D[i,i]) for i in range(len(C))]
print('FINAL cubic rank',len(C),'SNF',dict(Counter(ds)),'time',time.time()-start,flush=True)
pickle.dump(L.b,open('workspace/agent2_ia3_mixed_plus_commuting.pkl','wb'))

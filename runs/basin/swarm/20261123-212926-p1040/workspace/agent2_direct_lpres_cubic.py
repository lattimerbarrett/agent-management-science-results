import json,sys,pickle,time
sys.path.insert(0,'workspace')
from agent2_cubic_source import magnus3,IntegralLattice
from agent2_sparse_closure import apply
from itertools import product
import sympy as S
from sympy.matrices.normalforms import smith_normal_form
from sympy.polys.domains import ZZ
from collections import Counter
N=9;off=81;data=json.load(open('workspace/agent4_gap_ia3_data.json'))
def vector(p):
    v={}
    for u,c in p.items():
        if len(u)==2:v[u[0]*N+u[1]]=c
        if len(u)==3:v[off+(u[0]*N+u[1])*N+u[2]]=c
    return v

def action(ws):
    ps=[magnus3(tuple(w[::-1]),N) for w in ws]
    lin=[{u:c for u,c in p.items() if len(u)==1} for p in ps]
    quad=[{u:c for u,c in p.items() if len(u)==2} for p in ps]
    act=[]
    for i,j in product(range(N),repeat=2):
        p={}
        for P,Q in [(lin[i],lin[j]),(quad[i],lin[j]),(lin[i],quad[j])]:
            for x,c in P.items():
                for y,d in Q.items():p[x+y]=p.get(x+y,0)+c*d
        act.append(vector(p))
    for i,j,k in product(range(N),repeat=3):
        p={}
        for x,c in lin[i].items():
            for y,d in lin[j].items():
                for z,e in lin[k].items():p[x+y+z]=p.get(x+y+z,0)+c*d*e
        act.append(vector(p))
    return act

def comm(v,k):
    ans={}
    for i,c in v.items():
        if i>=off:continue
        a,b=divmod(i,N);j=off+(a*N+b)*N+k;l=off+(k*N+a)*N+b
        ans[j]=ans.get(j,0)+c;ans[l]=ans.get(l,0)-c
    return ans
start=time.time();L=IntegralLattice()
for r in data['rels']:
    p=magnus3(tuple(r['word'][::-1]),N)
    assert not any(len(u)==1 for u in p)
    L.insert(vector(p))
acts=[action(e['images']) for e in data['endomorphisms']];idx=0
while idx<len(L.queue):
    v=L.queue[idx];idx+=1
    for k in range(N):L.insert(comm(v,k))
    for act in acts:L.insert(apply(act,v))
for iteration in range(10):
    changed=0
    for v in list(L.b.values()):
        for k in range(N):changed+=L.insert(comm(v,k))
        for act in acts:changed+=L.insert(apply(act,v))
    print('stability',iteration,'changes',changed,flush=True)
    if not changed:break
C={p-off:{i-off:c for i,c in v.items()} for p,v in L.b.items() if p>=off}
M=S.zeros(729,len(C))
for j,v in enumerate(C.values()):
    for i,c in v.items():M[i,j]=c
D=smith_normal_form(M,domain=ZZ);ds=[abs(D[i,i]) for i in range(len(C))]
print('Direct LPRES mixed rank',len(L.b),'pure cubic rank',len(C),'SNF',dict(Counter(ds)),'secs',time.time()-start,flush=True)
pickle.dump(C,open('workspace/agent2_direct_lpres_cubic.pkl','wb'))

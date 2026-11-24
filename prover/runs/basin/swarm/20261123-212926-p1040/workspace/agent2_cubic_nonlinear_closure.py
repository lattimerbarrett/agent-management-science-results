import sys,pickle,time
sys.path.insert(0,'workspace')
from agent2_cubic_source import IntegralLattice,magnus3
from agent2_source_relations import generators
from agent2_sparse_closure import apply
from itertools import product,combinations
import sympy as S
from sympy.matrices.normalforms import smith_normal_form
from sympy.polys.domains import ZZ

def actions():
    N=9;off=N*N;lifts=pickle.load(open('workspace/agent2_nielsen_lifts_complete.pkl','rb'));out=[]
    words=[[lifts[a,b,k] for k in range(N)] for a in range(3) for b in range(3) if a!=b]
    inverse=pickle.load(open('workspace/agent2_inversion_lifts.pkl','rb'))
    words.append([inverse[k] for k in range(N)])
    for ws in words:
        ps=[magnus3(w,N) for w in ws]
        lin=[{u:c for u,c in p.items() if len(u)==1} for p in ps]
        quad=[{u:c for u,c in p.items() if len(u)==2} for p in ps]
        act=[]
        for i,j in product(range(N),repeat=2):
            v={}
            for P,Q in [(lin[i],lin[j]),(quad[i],lin[j]),(lin[i],quad[j])]:
                for x,c in P.items():
                    for y,d in Q.items():
                        w=x+y;k=w[0]*N+w[1] if len(w)==2 else off+(w[0]*N+w[1])*N+w[2]
                        v[k]=v.get(k,0)+c*d
            act.append({k:c for k,c in v.items() if c})
        for i,j,k in product(range(N),repeat=3):
            v={}
            for x,c in lin[i].items():
                for y,d in lin[j].items():
                    for z,e in lin[k].items():v[off+(x[0]*N+y[0])*N+z[0]]=c*d*e
            act.append(v)
        out.append(act)
    return out

def run():
    start=time.time();B=pickle.load(open('workspace/agent2_ia3_mixed_relations.pkl','rb'));L=IntegralLattice()
    for v in B.values():L.insert(v)
    H=pickle.load(open('workspace/agent2_ia3_GL_relations.pkl','rb'));N=9;off=81;P=list(combinations(range(N),2))
    for col in range(H.cols):
        p={}
        for r,(i,j) in enumerate(P):
            c=int(H[r,col])
            if c:p[(i,j)]=c;p[(j,i)]=-c
        for k in range(N):
            v={}
            for (i,j),c in p.items():
                a=off+(i*N+j)*N+k;b=off+(k*N+i)*N+j
                v[a]=v.get(a,0)+c;v[b]=v.get(b,0)-c
            L.insert(v)
    acts=actions();idx=0
    while idx<len(L.queue):
        v=L.queue[idx];idx+=1
        for act in acts:L.insert(apply(act,v))
    C={p-off:{i-off:c for i,c in v.items()} for p,v in L.b.items() if p>=off}
    print('Mixed relation rank',len(L.b),'pure cubic rank',len(C),'time',time.time()-start,flush=True)
    M=S.zeros(729,len(C))
    for j,v in enumerate(C.values()):
        for i,c in v.items():M[i,j]=c
    D=smith_normal_form(M,domain=ZZ);ds=[abs(D[i,i]) for i in range(len(C))]
    from collections import Counter
    print('SNF',dict(Counter(ds)),flush=True)
    assert len(C)==197 and all(d==1 for d in ds)
    pickle.dump(C,open('workspace/agent2_ia3_cubic_primitive_relations.pkl','wb'))
    return C
if __name__=='__main__':run()

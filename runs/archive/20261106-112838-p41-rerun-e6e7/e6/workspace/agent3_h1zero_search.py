from itertools import combinations
from pathlib import Path
import z3,time,json

def solve(n,timeout=60000):
    tris=list(combinations(range(n),3)); tindex={T:i for i,T in enumerate(tris)}
    Ts=[z3.Bool('t%d'%i) for i in range(len(tris))]
    facets=list(combinations(range(n),4));Fs=[z3.Bool('f%d'%i) for i in range(len(facets))]
    s=z3.Solver();s.set(timeout=timeout)
    for F,b in zip(facets,Fs):
        facebool=[Ts[tindex[T]] for T in combinations(F,3)]
        s.add(b==z3.And(facebool))
        s.add(z3.Sum([z3.If(q,1,0) for q in facebool])!=3)
    for T,b in zip(tris,Ts):s.add(z3.Implies(b,z3.Or([f for F,f in zip(facets,Fs) if set(T)<=set(F)])))
    for e in combinations(range(n),2):s.add(z3.Or([f for F,f in zip(facets,Fs) if set(e)<=set(F)]))
    nt=z3.Sum([z3.If(q,1,0) for q in Ts]);nf=z3.Sum([z3.If(q,1,0) for q in Fs])
    s.add(nt>=(n-2)**2,nf>=nt-(n*(n-1)//2-n+1),nf<len(facets))
    s.add(Fs[0])
    # In K_n with star spanning tree rooted at0, cycle space has coordinates
    # the edges on1..n-1. Every coordinate must lie in span of present triangles.
    edges=list(combinations(range(1,n),2))
    def xor(q):
        ans=z3.BoolVal(False)
        for b in q:ans=z3.Xor(ans,b)
        return ans
    for k,target in enumerate(edges):
        coeff=[z3.Bool('c%d_%d'%(k,j)) for j in range(len(tris))]
        for c,t in zip(coeff,Ts):s.add(z3.Implies(c,t))
        for edge in edges:
            s.add(xor([c for c,T in zip(coeff,tris) if set(edge)<=set(T)])==(edge==target))
    start=time.time();out=s.check();print(n,out,'seconds',time.time()-start,flush=True)
    if out==z3.sat:
        m=s.model();res={'n':n,'triangles':[T for T,b in zip(tris,Ts) if z3.is_true(m[b])],'facets':[F for F,b in zip(facets,Fs) if z3.is_true(m[b])]}
        Path('workspace/agent3_h1zero_blocked_n%d.json'%n).write_text(json.dumps(res));print('counts',len(res['triangles']),len(res['facets']),flush=True)
    return out

if __name__=='__main__':
    solve(9,timeout=180000)
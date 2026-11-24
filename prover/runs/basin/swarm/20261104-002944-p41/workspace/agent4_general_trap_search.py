from itertools import combinations
import z3,time,json

def search(n,seconds=180):
    fs=list(combinations(range(n),4));N=len(fs)
    R={f:z3.Int('R'+str(f)) for f in fs}
    s=z3.Solver();s.set(timeout=1000*seconds)
    for f in fs:s.add(R[f]>=0,R[f]<=N)
    for f,g in combinations(fs,2):s.add(z3.Or(R[f]==N,R[g]==N,R[f]!=R[g]))
    H={}
    for q in [1,2,3]:
      for h in combinations(range(n),q):
        hset=set(h);rr=[R[f] for f in fs if hset<=set(f)]
        hh=z3.Int('H'+str(h));H[h]=hh
        s.add(hh>=0,hh<=N,z3.Or([hh==r for r in rr]))
        s.add([hh<=r for r in rr])
        if q==1:s.add(hh<N)
    s.add(R[(0,1,2,3)]==0,R[(0,1,2,4)]==1)
    for v in range(4,n-1):s.add(H[(v,)]<H[(v+1,)])
    s.add(z3.Or([R[f]==N for f in fs]))
    for f in fs:
        rs=list(combinations(f,3))
        # Exact shelling of the selected facets.
        s.add(z3.Implies(R[f]<N,z3.Or(R[f]==0,*[H[r]<R[f] for r in rs])))
        for q in [1,2]:
          for h in combinations(f,q):
            covers=[H[r]<R[f] for r in rs if set(h)<=set(r)]
            s.add(z3.Implies(z3.And(R[f]<N,H[h]<R[f]),z3.Or(covers)))
        # If missing, at least one existing vertex/edge must be uncovered by boundary triangles.
        bad=[]
        for q in [1,2]:
          for h in combinations(f,q):
            cov=[H[r]<N for r in rs if set(h)<=set(r)]
            bad.append(z3.And(H[h]<N,z3.Not(z3.Or(cov))))
        s.add(z3.Or(R[f]<N,*bad))
    tm=time.time();ans=s.check();print('GENERAL n',n,ans,'seconds',time.time()-tm,flush=True)
    if ans==z3.sat:
        m=s.model();fac=sorted([f for f in fs if m.eval(R[f]).as_long()<N],key=lambda f:m.eval(R[f]).as_long())
        print(fac,flush=True)
        json.dump(fac,open('workspace/agent4_generaltrap'+str(n)+'.json','w'))
        # Independently check shelling and inadmissibility of EVERY missing facet.
        faces=set();selected=set()
        for f in fac:
            ff=set(f);old=[g for g in faces if set(g)<=ff]
            ridges=[g for g in old if len(g)==3]
            if selected:assert ridges and all(any(set(g)<=set(r) for r in ridges) for g in old)
            selected.add(f)
            faces.update(g for q in range(5) for g in combinations(f,q))
        for f in set(fs)-selected:
            old=[g for g in faces if set(g)<=set(f)];rr=[g for g in old if len(g)==3]
            assert not rr or any(not any(set(g)<=set(r) for r in rr) for g in old)
        print('INDEPENDENTLY VERIFIED shelling and all blockedmissingfacets',flush=True)
    return ans
if __name__=='__main__':
    search(7,180)
    search(8,300)

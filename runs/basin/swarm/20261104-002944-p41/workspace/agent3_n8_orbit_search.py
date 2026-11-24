from itertools import combinations
import z3,json,time

def search(n,seconds=60,missing=(0,1,4),second=None):
    V=range(n); ff=list(combinations(V,4)); tt=list(combinations(V,3)); N=len(ff)
    S={t:z3.Bool('S'+str(t)) for t in tt}
    T={f:z3.Int('t'+str(f)) for f in ff}
    sol=z3.Solver();sol.set(timeout=1000*seconds)
    for f in ff:
        rs=list(combinations(f,3))
        sol.add(z3.Sum([z3.If(S[r],1,0) for r in rs])!=3)
        sol.add(T[f]>=0,T[f]<=N)
        sol.add((T[f]<N)==z3.And([S[r] for r in rs]))
    for f,g in combinations(ff,2):sol.add(z3.Or(T[f]==N,T[g]==N,T[f]!=T[g]))
    H={}
    for q in [1,2,3]:
        for h in combinations(V,q):
            hs=set(h);ts=[T[f] for f in ff if hs<=set(f)]
            a=z3.Int('h'+str(h));H[h]=a
            sol.add(a>=0,a<=N,z3.Or([a==x for x in ts]))
            sol.add([a<=x for x in ts])
            if q<3:sol.add(a<N)
            else:sol.add(S[h]==(a<N))
    sol.add(z3.Not(S[missing]))
    sol.add(T[(0,1,2,3)]==0)
    if second is not None:sol.add(T[second]==1)
    p=z3.Sum([z3.If(T[f]<N,1,0) for f in ff])
    for f in ff:sol.add(z3.Implies(T[f]<N,T[f]<p))
    for f in ff:
        rs=list(combinations(f,3))
        sol.add(z3.Implies(T[f]<N,z3.Or(T[f]==0,*[H[r]<T[f] for r in rs])))
        for q in [1,2]:
            for h in combinations(f,q):
                cover=[H[r]<T[f] for r in rs if set(h)<=set(r)]
                sol.add(z3.Implies(z3.And(T[f]<N,H[h]<T[f]),z3.Or(cover)))
    tm=time.time();ans=sol.check();print('n',n,'result',ans,'seconds',time.time()-tm,flush=True)
    if ans==z3.sat:
        m=sol.model();facets=sorted([f for f in ff if m.eval(T[f]).as_long()<N],key=lambda f:m.eval(T[f]).as_long())
        print(facets,flush=True)
        json.dump(facets,open('workspace/agent3_orbit_trap'+str(n)+'.json','w'))
    return ans


if __name__=="__main__":
 cases=[((4,5,6),None),((0,4,5),None),((0,3,4),(0,1,2,4)),((0,1,5),(0,1,2,4))]
 for missing,second in cases:
  print("case",missing,second,flush=True)
  ans=search(8,1800,missing,second)
  assert ans==z3.unsat, (missing,second,ans)

from itertools import combinations
import z3,time,json

def search(n,s,seconds):
    ff=list(combinations(range(n),4));tt=list(combinations(range(n),3));N=len(ff)
    FS={f:set(f) for f in ff};S={t:z3.Bool('S'+str(t)) for t in tt}
    X={f:z3.Bool('X'+str(f)) for f in ff};T={f:z3.Int('t'+str(f)) for f in ff}
    sol=z3.Solver();sol.set(timeout=seconds*1000)
    root=tuple(list(range(s))+list(range(3,7-s)))
    assert len(root)==4
    sol.add(X[root],T[root]==0,z3.Not(S[(0,1,2)]))
    for i,f in enumerate(ff):
        rs=list(combinations(f,3))
        sol.add(z3.Sum([z3.If(S[r],1,0) for r in rs])!=3)
        sol.add(X[f]==z3.And([S[r] for r in rs]))
        sol.add(z3.If(X[f],z3.And(T[f]>=0,T[f]<N),T[f]==N+i))
    sol.add(z3.Distinct(list(T.values())))
    for t in tt:
        sol.add(S[t]==z3.Or([X[f] for f in ff if set(t)<=FS[f]]))
    for e in combinations(range(n),2):
        sol.add(z3.Or([X[f] for f in ff if set(e)<=FS[f]]))
    for f in ff:
        adj=[g for g in ff if len(FS[f]&FS[g])==3]
        sol.add(z3.Implies(z3.And(X[f],T[f]!=0),z3.Or([T[g]<T[f] for g in adj])))
        for g in ff:
            h=FS[f]&FS[g]
            if not h or len(h)>2:continue
            es=[e for e in adj if h<=FS[e]]
            sol.add(z3.Implies(z3.And(X[f],X[g],T[g]<T[f]),z3.Or([T[e]<T[f] for e in es])))
    tm=time.time();ans=sol.check();print('n',n,'s',s,'ans',ans,'time',time.time()-tm,flush=True)
    if ans==z3.sat:
        m=sol.model();facets=sorted([f for f in ff if z3.is_true(m.eval(X[f]))],key=lambda f:m.eval(T[f]).as_long())
        print(facets,flush=True);json.dump(facets,open('workspace/agent1_sat2_trap'+str(n)+'.json','w'))
    return ans
if __name__=='__main__':
    for s in [0,1,2]:search(8,s,90)

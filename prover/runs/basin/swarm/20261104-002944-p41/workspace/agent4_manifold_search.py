from itertools import combinations
import z3,time,json

def search(n,seconds=60):
    fs=list(combinations(range(n),4)); ts=list(combinations(range(n),3))
    F={f:z3.Bool('F'+str(f)) for f in fs}
    T={t:z3.Bool('T'+str(t)) for t in ts}
    s=z3.Solver();s.set(timeout=1000*seconds)
    for t in ts:
        cnt=z3.Sum([z3.If(F[f],1,0) for f in fs if set(t)<=set(f)])
        s.add(z3.Or(cnt==0,cnt==2),T[t]==(cnt==2))
    for f in fs:
        s.add(z3.Or(F[f],z3.Sum([z3.If(T[t],1,0) for t in combinations(f,3)])<=2))
    for v in range(n):
        s.add(z3.Sum([z3.If(F[f],1,0) for f in fs if v in f])==2*n-6)
    for e in combinations(range(n),2):
        s.add(z3.Or([F[f] for f in fs if set(e)<=set(f)]))
    s.add(F[(0,1,2,3)],F[(0,1,2,4)])
    tm=time.time();a=s.check();print('n',n,'answer',a,'time',time.time()-tm,flush=True)
    if a==z3.sat:
        m=s.model();fac=[f for f in fs if z3.is_true(m.eval(F[f]))]
        print(fac,flush=True)
        json.dump(fac,open('workspace/agent4_flagmanifold'+str(n)+'.json','w'))
    return a
if __name__=='__main__':
    for n in range(7,12):search(n,60)

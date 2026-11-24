from itertools import combinations
import z3,time,json

def search(n,seconds=30,maxmodels=100):
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
    seed=json.load(open('workspace/agent4_flagmanifold'+str(n)+'.json'))
    rootfac={tuple(f) for f in seed if 0 in f}
    for f in fs:
        if 0 in f:s.add(F[f]==(f in rootfac))
    from sage.all import Matrix,GF,QQ,SimplicialComplex
    es=list(combinations(range(1,n),2)); ix={e:i for i,e in enumerate(es)}
    def row(t):
        a,b,c=t;r=[0]*len(es)
        for e,val in [((a,b),1),((a,c),-1),((b,c),1)]:
            if e in ix:r[ix[e]]=val
        return r
    rows={t:row(t) for t in ts}
    tm=time.time()
    for it in range(maxmodels):
        a=s.check();print('n',n,'model',it,'answer',a,'elapsed',time.time()-tm,flush=True)
        if a!=z3.sat:return
        m=s.model();fac=[f for f in fs if z3.is_true(m.eval(F[f]))]
        tr=[t for t in ts if z3.is_true(m.eval(T[t]))]
        cuts=0
        for p in [2,3,5,7,11,0]:
            ring=GF(p) if p else QQ
            ker=Matrix(ring,[rows[t] for t in tr]).right_kernel().basis()
            if ker:
                print('  H1 mod',p,'dimension',len(ker),flush=True)
                for alpha in ker:
                    violating=[T[t] for t in ts if sum(a*b for a,b in zip(alpha,rows[t]))!=0]
                    assert violating
                    s.add(z3.Or(violating));cuts+=1
                break
        if cuts:continue
        ss=SimplicialComplex(fac);print('INTEGRALHOMOLOGY',ss.homology(),flush=True)
        json.dump(fac,open('workspace/agent4_homologysphere'+str(n)+'.json','w'))
        return
if __name__=='__main__':search(15,120,100)

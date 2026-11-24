from itertools import combinations
import z3,time,json

def basis(rows):
    B={}
    for r in rows:
        while r:
            p=r.bit_length()-1
            if p not in B:B[p]=r;break
            r^=B[p]
    return B

def reduce(r,B):
    while r:
        p=r.bit_length()-1
        if p not in B:return r
        r^=B[p]
    return 0

def nulls(rows,n):
    B=basis(rows)
    for j in range(n):
        if j in B:continue
        w=1<<j
        for p,r in sorted(B.items()):
            if (r&w).bit_count()%2:w^=1<<p
        yield w

def components(V,E):
    adj={v:set() for v in V}
    for a,b in E:adj[a].add(b);adj[b].add(a)
    cs=[];left=set(V)
    while left:
        C={left.pop()};todo=list(C)
        while todo:
            v=todo.pop()
            for w in adj[v]&left:left.remove(w);C.add(w);todo.append(w)
        cs.append(C)
    return cs

def cycle_null(edges,triangles):
    ix={e:i for i,e in enumerate(edges)};B={}
    for i,t in enumerate(triangles):
        r=sum(1<<ix[e] for e in combinations(t,2));c=1<<i
        while r:
            p=r.bit_length()-1
            if p not in B:B[p]=(r,c);break
            a,b=B[p];r^=a;c^=b
        if not r:yield c

def solve(n,limit=10000,seconds=180):
    V=range(n);tt=list(combinations(V,3));ff=list(combinations(V,4));ee=list(combinations(V,2))
    S={t:z3.Bool('s'+str(t)) for t in tt};X={f:z3.Bool('x'+str(f)) for f in ff}
    sol=z3.Solver();sol.set(timeout=30000)
    sol.add(z3.Not(S[(0,1,2)]))
    for f in ff:
        rr=list(combinations(f,3))
        sol.add(z3.Sum([z3.If(S[t],1,0) for t in rr])!=3)
        sol.add(X[f]==z3.And([S[t] for t in rr]))
    for t in tt:sol.add(S[t]==z3.Or([X[f] for f in ff if set(t)<=set(f)]))
    for e in ee:sol.add(z3.Or([X[f] for f in ff if set(e)<=set(f)]))
    f2=z3.Sum([z3.If(S[t],1,0) for t in tt]);f3=z3.Sum([z3.If(X[f],1,0) for f in ff])
    sol.add(f2>=(n-2)**2,f3>=f2-len(ee)+n-1)
    for v in V:
        tv=z3.Sum([z3.If(S[t],1,0) for t in tt if v in t]);cv=z3.Sum([z3.If(X[f],1,0) for f in ff if v in f])
        sol.add(tv>=2*n-5,cv>=tv-n+2)
    for e in ee:
        te=z3.Sum([z3.If(S[t],1,0) for t in tt if set(e)<=set(t)]);ce=z3.Sum([z3.If(X[f],1,0) for f in ff if set(e)<=set(f)])
        sol.add(ce>=te-1)
    tm=time.time();counts={}
    for it in range(limit):
        ans=sol.check()
        if ans!=z3.sat:print('END',n,it,ans,counts,time.time()-tm,flush=True);return
        m=sol.model();T=[t for t in tt if z3.is_true(m.eval(S[t]))];F=[f for f in ff if z3.is_true(m.eval(X[f]))]
        # Global H1: gauge all edges at vertex 0 to zero.
        ge=list(combinations(range(1,n),2));gi={e:i for i,e in enumerate(ge)}
        row=lambda t:sum(1<<gi[e] for e in combinations(t,2) if e in gi)
        ns=list(nulls([row(t) for t in T],len(ge)))
        if ns:
            for w in ns:sol.add(z3.Or([S[t] for t in tt if (row(t)&w).bit_count()%2]))
            why='H1'
        else:
            why=None
            # Edge links connected. Use a partition of all possible link vertices.
            for e in ee:
                U=[v for v in V if v not in e and tuple(sorted((*e,v))) in T]
                E=[tuple(v for v in f if v not in e) for f in F if set(e)<=set(f)]
                C=components(U,E)
                if len(C)>1:
                    A=C[0];a=next(iter(A));b=next(iter(C[1]));allU=set(V)-set(e)
                    cross=[X[tuple(sorted((*e,u,v)))] for u in A for v in allU-A]
                    sol.add(z3.Or(z3.Not(S[tuple(sorted((*e,a)))]),z3.Not(S[tuple(sorted((*e,b)))]),*cross))
                    why='edge-link';break
            if why is None:
                # Global H2 using explicit cycle + separating cocycle.
                ti={t:i for i,t in enumerate(T)}
                br=[sum(1<<ti[t] for t in combinations(f,3)) for f in F]
                BB=basis(br)
                for cyc in cycle_null(ee,T):
                    if reduce(cyc,BB):
                        w=next(w for w in nulls(br,len(T)) if (w&cyc).bit_count()%2)
                        kill=[X[f] for f in ff if sum(1 for t in combinations(f,3) if t in ti and w>>ti[t]&1)%2]
                        remove=[z3.Not(S[t]) for i,t in enumerate(T) if cyc>>i&1]
                        sol.add(z3.Or(*(kill+remove)));why='H2';break
            if why is None:
                # Vertex links: H0 and H1, including explicit cycle clauses.
                for v in V:
                    U=[x for x in V if x!=v]
                    E=[tuple(x for x in t if x!=v) for t in T if v in t]
                    L=[tuple(x for x in f if x!=v) for f in F if v in f]
                    C=components(U,E)
                    if len(C)>1:
                        A=C[0]
                        sol.add(z3.Or([S[tuple(sorted((v,a,b)))] for a in A for b in set(U)-A]));why='vertex-H0';break
                    # H1 witness as a cycle in edge space outside triangle boundaries.
                    ei={e:i for i,e in enumerate(E)}
                    br=[sum(1<<ei[e] for e in combinations(t,2)) for t in L];BB=basis(br)
                    # Kernel of graph boundary, computed by same tracked elimination.
                    B={};cycs=[]
                    for j,e in enumerate(E):
                        r=sum(1<<x for x in e);c=1<<j
                        while r:
                            p=r.bit_length()-1
                            if p not in B:B[p]=(r,c);break
                            a,b=B[p];r^=a;c^=b
                        if not r:cycs.append(c)
                    for cyc in cycs:
                        if reduce(cyc,BB):
                            w=next(w for w in nulls(br,len(E)) if (w&cyc).bit_count()%2)
                            kill=[X[tuple(sorted((v,*t)))] for t in combinations(U,3) if sum(1 for e in combinations(t,2) if e in ei and w>>ei[e]&1)%2]
                            remove=[z3.Not(S[tuple(sorted((v,*e)))]) for j,e in enumerate(E) if cyc>>j&1]
                            sol.add(z3.Or(*(kill+remove)));why='vertex-H1';break
                    if why:break
            if why is None:
                print('CM CANDIDATE',n,it,len(F),F,flush=True)
                json.dump(F,open('workspace/agent1_cm_candidate'+str(n)+'.json','w'))
                return F
        counts[why]=counts.get(why,0)+1
        if it%100==0:print(n,it,counts,'time',round(time.time()-tm,1),flush=True)
        if time.time()-tm>seconds:print('TIME',n,it,counts,flush=True);return
if __name__=='__main__':
    solve(8,seconds=120)
    solve(9,seconds=120)

from itertools import combinations, count
from functools import lru_cache

def bits(x):
    while x:
        b = x & -x
        yield b
        x ^= b

def canonical(facets):
    return tuple(sorted(set(facets)))

@lru_cache(None)
def certificate(facets, k):
    if len(facets) == 1:
        return ('simplex', facets[0])
    candidates = set()
    for f in facets:
        s = f
        while s:
            if s.bit_count() <= k + 1:
                candidates.add(s)
            s = (s - 1) & f
    for s in sorted(candidates, key=lambda x:(x.bit_count(),x)):
        deletion = tuple(f for f in facets if f & s != s)
        if not deletion:
            continue
        if any(not any(((f ^ v) & g) == (f ^ v) for g in deletion)
               for f in facets if f & s == s for v in bits(s)):
            continue
        link = canonical(f ^ s for f in facets if f & s == s)
        cd = certificate(deletion, k)
        if cd is None:
            continue
        cl = certificate(link, k)
        if cl is not None:
            return ('split', s, cd, cl)
    return None

def prefix_order(cert):
    if cert[0] == 'simplex':
        return [cert[1]]
    _, s, cd, cl = cert
    return prefix_order(cd) + [s | f for f in prefix_order(cl)]

def vertices(facets):
    u = 0
    for f in facets:
        u |= f
    return u

def all_facets(vmask, cardinality):
    return {sum(c) for c in combinations(list(bits(vmask)), cardinality)}

def complete(facets, k, fresh):
    """Returns (ordered added facets, mask of new vertices).
    The input facets have exact vertex ground set, and k >= 1.
    """
    assert k >= 1
    facets = canonical(facets)
    assert certificate(facets, k) is not None
    d = facets[0].bit_count() - 1
    V = vertices(facets)
    if d <= 1:
        return sorted(all_facets(V, d+1) - set(facets)), 0
    if d == 2:
        current = set(facets)
        additions = []
        edges = {sum(c) for f in facets for c in combinations(list(bits(f)),2)}
        missing = all_facets(V,2) - edges
        while missing:
            chosen = None
            for e in sorted(missing):
                u,v = list(bits(e))
                for w in bits(V ^ e):
                    if (u|w) in edges and (v|w) in edges:
                        chosen = (e, e|w)
                        break
                if chosen is not None:
                    break
            assert chosen is not None, 'The input graph was not connected'
            e,f = chosen
            assert f not in current
            current.add(f); additions.append(f)
            edges.add(e); missing.remove(e)
        additions += sorted(all_facets(V,3) - current)
        return additions, 0
    # Add an apex over the ridge skeleton in a decomposable-prefix order.
    a = 1 << next(fresh)
    ridge = canonical(f ^ v for f in facets for v in bits(f))
    cr = certificate(ridge, k)
    assert cr is not None
    additions = [a | r for r in prefix_order(cr)]
    lower_additions, B = complete(ridge, k, fresh)
    additions += [a | r for r in lower_additions]
    additions += sorted(all_facets(V|B,d+1) - set(facets))
    return additions, a|B

def check(facets,k):
    facets = canonical(facets)
    d = facets[0].bit_count()-1
    V = vertices(facets)
    additions,A = complete(facets,k,count(V.bit_length()))
    assert A.bit_count() == max(0,d-2)
    assert not (V&A)
    current = set(facets)
    for i,f in enumerate(additions):
        assert f.bit_count() == d+1
        assert f not in current
        current.add(f)
        assert certificate(canonical(current),k) is not None, (i,f)
    assert current == all_facets(V|A,d+1)
    print('checked', {'dimension':d,'k':k,'initial_facets':len(facets),
                      'new_vertices':A.bit_count(),'added_facets':len(additions)},flush=True)

if __name__ == '__main__' and False:
    for d in range(2,6):
        check(((1<<(d+1))-1,),1)
    # Find a genuine non-vertex-decomposable, 1-decomposable example in dimension 2.
    fs = sorted(all_facets((1<<6)-1,3))
    import random
    random.seed(104729)
    for _ in range(100000):
        f = canonical(random.sample(fs,random.randint(8,14)))
        if certificate(f,1) is not None and certificate(f,0) is None:
            print('non-VD example found:',f,flush=True)
            check(f,1)
            # Coning preserves non-VD: its apex link is the example.
            cone=canonical(g|64 for g in f)
            assert certificate(cone,1) is not None
            assert certificate(cone,0) is None
            check(cone,1)
            break
    else:
        raise AssertionError('No example found')

def fast_solver(n,k):
    vs=[1<<v for v in range(n)]
    full=(1<<(1<<n))-1
    containing={v:(full//((1<<v)+1))<<v for v in vs}
    for size in range(2,k+2):
        for c in combinations(vs,size):
            mask=full
            for v in c:mask &= containing[v]
            containing[sum(c)]=mask
    calls=[0]
    import time
    started=time.time()
    def vertex_mask(F):
        return sum(v for v in vs if F & containing[v])
    @lru_cache(maxsize=20000)
    def shadow(F):
        return sum_shadow(F)
    def sum_shadow(F):
        result=0
        for v in vs:
            result |= (F & containing[v]) >> v
        return result
    @lru_cache(maxsize=20000)
    def kd(F):
        calls[0]+=1
        if calls[0]%10000==0:print('calls',calls[0],'time',time.time()-started,'facets',F.bit_count(),flush=True)
        if calls[0]>200000:raise RuntimeError('search limit')
        if not F:return False
        if F&(F-1)==0:return True
        first=(F&-F).bit_length()-1
        d=first.bit_count()-1
        if d==0:return True
        V=vertex_mask(F)
        if d==1:
            reached=V&-V
            todo=reached
            while todo:
                v=todo&-todo;todo^=v
                edges=F & containing[v]
                new=0
                while edges:
                    b=edges&-edges;edges^=b
                    new|=(b.bit_length()-1)^v
                new&=~reached;todo|=new;reached|=new
            return reached==V
        # Vanishing H_1 over F_2 is necessary in every dimension >= 2.
        ed=shadow(F) if d==2 else shadow(shadow(F))
        tr=F if d==2 else shadow(F)
        target=ed.bit_count()-V.bit_count()+1
        bas={}
        ff=tr
        while ff and len(bas)<target:
            q=ff&-ff;ff^=q;f=q.bit_length()-1
            row=0
            for v in bits(f):row |= 1<<(f^v)
            while row:
                h=row.bit_length()-1
                if h in bas:row^=bas[h]
                else:bas[h]=row;break
        if len(bas)<target:return False
        if d==3:
            target3=tr.bit_count()-target
            bas={};ff=F
            while ff and len(bas)<target3:
                q=ff&-ff;ff^=q;f=q.bit_length()-1
                row=0
                for v in bits(f):row |= 1<<(f^v)
                while row:
                    h=row.bit_length()-1
                    if h in bas:row^=bas[h]
                    else:bas[h]=row;break
            if len(bas)<target3:return False
        # A cone with full-boundary facets added preserves decomposability.
        for v in bits(V):
            R=F & containing[v];D=F^R;L=R>>v
            if not (shadow(D)&~L) and kd(L):return True
        # Every link of a k-decomposable complex is k-decomposable.
        for v in bits(V):
            if not kd((F & containing[v]) >> v):return False
        # Nonnegative h-vector is necessary; in these dimensions use its last entry.
        sh=shadow(F)
        if d==2 and F.bit_count()-sh.bit_count()+V.bit_count()-1<0:return False
        if d==3:
            edges=shadow(sh)
            if F.bit_count()-sh.bit_count()+edges.bit_count()-V.bit_count()+1<0:return False
        for s in sorted(containing,key=lambda s:(s.bit_count(),(F&containing[s]).bit_count())):
            if s.bit_count()>k+1:continue
            R=F & containing[s]
            D=F ^ R
            if not R or not D:continue
            req=0
            for v in bits(s):req|=R>>v
            if req & ~shadow(D):continue
            if kd(R>>s) and kd(D):return True
        return False
    return kd

if __name__=='__main__' and False:
    import random,time,pickle
    kd=fast_solver(8,1)
    lower=(7,11,14,21,26,37,44,49,50,56)
    initial=canonical([f|64 for f in lower]+[f|128 for f in lower])
    fs=all_facets(255,4)
    start=time.time()
    for trial in range(10000):
        cur=set(initial);rem=list(fs-cur);random.shuffle(rem)
        while rem:
            found=False
            for f in rem:
                cand=canonical(cur|{f})
                if kd(sum(1<<g for g in cand)):
                    cur.add(f);rem.remove(f);found=True;break
            if not found:break
        if rem:
            print('STUCK 1DEC',trial,len(cur),sorted(cur),flush=True)
            pickle.dump(sorted(cur),open('stuck1.pkl','wb'));break
        if trial%100==0:
            print(trial,time.time()-start,kd.cache_info(),flush=True)
            kd.cache_clear()

if __name__=='__main__' and False:
    import z3,time,pickle
    for n in range(7,14):
        start=time.time()
        triples=list(combinations(range(n),3))
        quads=list(combinations(range(n),4))
        T={t:z3.Bool('t_'+str(t)) for t in triples}
        D={q:z3.Bool('d_'+str(q)) for q in quads}
        s=z3.Solver();s.set(timeout=60000)
        for q in quads:
            ts=[T[t] for t in combinations(q,3)]
            s.add(D[q]==z3.And(ts))
            s.add(z3.Sum([z3.If(t,1,0) for t in ts])!=3)
        for t in triples:
            s.add(z3.Implies(T[t],z3.PbEq([(D[q],1) for q in quads if set(t)<=set(q)],2)))
        for e in combinations(range(n),2):
            s.add(z3.PbGe([(D[q],1) for q in quads if set(e)<=set(q)],4))
        for v in range(n):
            s.add(z3.PbEq([(D[q],1) for q in quads if v in q],2*n-6))
            s.add(z3.PbEq([(T[t],1) for t in triples if v in t],3*n-9))
        s.add(D[quads[0]])
        ans=s.check();print('n',n,ans,time.time()-start,flush=True)
        if ans==z3.sat:
            m=s.model();fac=[sum(1<<v for v in q) for q in quads if z3.is_true(m.eval(D[q]))]
            print('candidate',fac,flush=True)
            pickle.dump((n,fac),open('sat_candidate_'+str(n)+'.pkl','wb'))

if __name__=='__main__' and False:
    from sage.all import Graph
    from collections import deque
    import pickle,time
    n=10
    init={tuple(sorted((u,v,w))) for u in (0,1) for v,w in [(v,2+(v-1)%(n-2)) for v in range(2,n)]}
    def edge_set(tris):
        return {e for t in tris for e in combinations(t,2)}
    def canon(tris):
        return Graph(list(edge_set(tris))).canonical_label(algorithm='sage').graph6_string()
    seen={canon(init)};todo=deque([init]);flag=[];start=time.time()
    while todo:
        tris=todo.popleft();edges=edge_set(tris)
        if all(t in tris for t in combinations(range(n),3) if all(e in edges for e in combinations(t,2))):
            flag.append(sorted(tris))
        for a,b in edges:
            old=[t for t in tris if a in t and b in t]
            assert len(old)==2
            x,y=[next(v for v in t if v not in (a,b)) for t in old]
            if tuple(sorted((x,y))) in edges:continue
            new=(tris-set(old))|{tuple(sorted((x,y,a))),tuple(sorted((x,y,b)))}
            key=canon(new)
            if key not in seen:seen.add(key);todo.append(new)
    print('2sphere vertices',n,'total',len(seen),'flag',len(flag),'time',time.time()-start,flush=True)
    pickle.dump(flag,open('flag_spheres_'+str(n)+'.pkl','wb'))

if __name__=='__main__' and False:
    import z3,pickle,time
    n=12
    links=pickle.load(open('flag_spheres_11.pkl','rb'))
    triples=list(combinations(range(n),3));quads=list(combinations(range(n),4));pairs=list(combinations(range(n),2))
    T={t:z3.Bool('t'+str(t)) for t in triples};D={q:z3.Bool('d'+str(q)) for q in quads}
    s=z3.Solver();s.set(timeout=60000)
    for q in quads:
        ts=[T[t] for t in combinations(q,3)]
        s.add(D[q]==z3.And(ts),z3.Sum([z3.If(t,1,0) for t in ts])!=3)
    for t in triples:
        s.add(z3.Implies(T[t],z3.PbEq([(D[q],1) for q in quads if set(t)<=set(q)],2)))
    for e in pairs:s.add(z3.PbGe([(D[q],1) for q in quads if set(e)<=set(q)],4))
    for v in range(n):
        s.add(z3.PbEq([(D[q],1) for q in quads if v in q],2*n-6))
        s.add(z3.PbEq([(T[t],1) for t in triples if v in t],3*n-9))
    start=time.time()
    for j,L in enumerate(links):
        s.push()
        LE={e for t in L for e in combinations(t,2)}
        for a,b in combinations(range(1,n),2):s.add(T[(0,a,b)] == ((a-1,b-1) in LE))
        for a,b,c in combinations(range(1,n),3):s.add(D[(0,a,b,c)] == ((a-1,b-1,c-1) in L))
        for attempt in range(10):
            ans=s.check();print('link',j,'attempt',attempt,ans,'time',time.time()-start,flush=True)
            if ans!=z3.sat:break
            m=s.model();fac=[q for q in quads if z3.is_true(m.eval(D[q]))]
            tris=[t for t in triples if z3.is_true(m.eval(T[t]))]
            pi={p:i for i,p in enumerate(pairs)};basis={}
            for t in tris:
                row=sum(1<<pi[p] for p in combinations(t,2))
                while row:
                    h=row.bit_length()-1
                    if h in basis:row^=basis[h]
                    else:basis[h]=row;break
            betti1=len(pairs)-n+1-len(basis)
            print('candidate betti1(F2)',betti1,'facets',len(fac),flush=True)
            if betti1==0:
                print('HOMOLOGY SPHERE CANDIDATE',fac,flush=True)
                pickle.dump((n,fac),open('homology_sphere_candidate.pkl','wb'))
            s.add(z3.Or([T[t]!=m.eval(T[t]) for t in triples]))
        s.pop()

if __name__=='__main__' and False:
    from sage.all import Graph
    from collections import deque
    import pickle,time
    for n in (11,12):
        init={tuple(sorted((u,v,w))) for u in (0,1) for v,w in [(v,2+(v-1)%(n-2)) for v in range(2,n)]}
        def edge_set(tris):return {e for t in tris for e in combinations(t,2)}
        def canon(tris):return Graph(list(edge_set(tris))).canonical_label(algorithm='sage').graph6_string()
        seen={canon(init)};todo=deque([init]);flag=[];start=time.time()
        while todo:
            tris=todo.popleft();edges=edge_set(tris)
            if all(t in tris for t in combinations(range(n),3) if all(e in edges for e in combinations(t,2))):flag.append(sorted(tris))
            for a,b in edges:
                old=[t for t in tris if a in t and b in t]
                x,y=[next(v for v in t if v not in (a,b)) for t in old]
                if tuple(sorted((x,y))) in edges:continue
                new=(tris-set(old))|{tuple(sorted((x,y,a))),tuple(sorted((x,y,b)))}
                key=canon(new)
                if key not in seen:seen.add(key);todo.append(new)
        print('2sphere vertices',n,'total',len(seen),'flag',len(flag),'time',time.time()-start,flush=True)
        pickle.dump(flag,open('flag_spheres_'+str(n)+'.pkl','wb'))

if __name__=='__main__' and False:
    import pickle
    from sage.all import SimplicialComplex
    n,fac=pickle.load(open('homology_sphere_candidate.pkl','rb'))
    C=SimplicialComplex(fac)
    print('f-vector',C.f_vector(),flush=True)
    print('homology',C.homology(algorithm='dhsw'),flush=True)

if __name__=='__main__' and False:
    import z3,time,pickle
    from sage.all import matrix,ZZ,GF,SimplicialComplex
    n=9
    triples=list(combinations(range(n),3));pairs=list(combinations(range(1,n),2));pi={p:i for i,p in enumerate(pairs)}
    T={t:z3.Bool('t'+str(t)) for t in triples}
    rows={}
    for t in triples:
        row=[0]*len(pairs)
        for j in range(3):
            edge=t[:j]+t[j+1:]
            if edge in pi:row[pi[edge]]=(-1)**j
        rows[t]=row
    s=z3.Solver();s.set(timeout=60000)
    for q in combinations(range(n),4):s.add(z3.PbLe([(T[t],1) for t in combinations(q,3)],2))
    for e in combinations(range(n),2):s.add(z3.PbGe([(T[t],1) for t in triples if set(e)<=set(t)],2))
    s.add(z3.PbEq([(T[t],1) for t in triples],len(pairs)))
    s.add(T[(0,1,2)])
    start=time.time()
    for attempt in range(100000):
        ans=s.check()
        if ans!=z3.sat:
            print('RESULT',ans,'attempt',attempt,'time',time.time()-start,flush=True);break
        m=s.model();ts=[t for t in triples if z3.is_true(m.eval(T[t]))]
        M=matrix(ZZ,[rows[t] for t in ts])
        K=M.change_ring(GF(2)).right_kernel()
        if K.dimension():
            z=K.basis()[0];p=2
        else:
            det=M.det()
            if abs(det)==1:
                print('ACYCLIC CORNER FREE',ts,flush=True)
                C=SimplicialComplex(ts)
                print('fundamentalgroup',C.fundamental_group().simplified(),flush=True)
                pickle.dump((n,ts),open('acyclic_cornerfree.pkl','wb'))
                break
            p=int(abs(det).prime_divisors()[0])
            z=M.change_ring(GF(p)).right_kernel().basis()[0]
        s.add(z3.Or([T[t] for t in triples if sum(a*b for a,b in zip(rows[t],z))!=0]))
        if attempt%100==0:print('attempt',attempt,'field',p,'time',time.time()-start,flush=True)

if __name__=='__main__':
    import pickle,time
    n,H=pickle.load(open('acyclic_cornerfree.pkl','rb'));H=set(H)
    fac=[]
    for q in combinations(range(2*n),4):
        proj=tuple(sorted({v//2 for v in q}))
        if len(proj)<=2 or proj in H:fac.append(sum(1<<v for v in q))
    F=sum(1<<f for f in fac)
    print('fat complex',2*n,'vertices',len(fac),'facets',flush=True)
    kd=fast_solver(2*n,1)
    print('1-decomposable?',kd(F),flush=True)

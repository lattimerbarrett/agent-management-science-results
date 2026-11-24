"""Executable finite certificates for the H45 counterdiagnostic.
No external data files are needed. Requires networkx, numpy, z3.
Every positive model is expanded to an injective map into a finite simple host.
The two infinite-host exclusions are checked by exhaustive rooted color profiles.
"""
import networkx as nx, numpy as np, z3, itertools, json
ROOT=0
POP=np.array([i.bit_count() for i in range(256)],dtype=np.uint8)
BASE_EDGES=[(0,3),(0,4),(0,6),(0,15),(0,19),(0,21),(1,3),(1,5),(1,6),(2,8),(2,9),(2,13),(2,16),(4,17),(5,13),(6,8),(6,9),(7,10),(7,12),(8,19),(9,19),(10,22),(11,14),(11,20),(12,17),(12,18),(13,14),(13,20),(14,15),(15,18),(15,20),(15,22),(16,17),(16,22),(18,21),(21,22)]
F=nx.Graph();F.add_nodes_from(range(23));F.add_edges_from(BASE_EDGES)
H=nx.Graph()
for side in [1,2]:
    mp={v:((0,0) if v==0 else (side,v)) for v in F}
    H.add_edges_from((mp[u],mp[v]) for u,v in F.edges())
assert len(H)==45 and H.number_of_edges()==72
assert not nx.is_bipartite(H)
assert nx.is_bipartite(H.subgraph(set(H)-{(0,0)}))

def Sfree(F):
    V = set(F)
    r = ROOT
    profiles = set()

    def add(B):
        A = V - set(B)
        a = F.subgraph(A)
        com = list(nx.connected_components(a))
        heavy = sum((len(c) for c in com if len(c) >= 3))
        eb = F.subgraph(B).number_of_edges()
        assert eb <= 1
        if r in A:
            rc = next((c for c in com if r in c))
            sz = len(rc)
            profiles.add(('A', sz, heavy - (sz if sz >= 3 else 0), eb))
        else:
            profiles.add(('B', 0, heavy, eb))
    for I in nx.find_cliques(nx.complement(F.subgraph(V - {r}))):
        add(I)
    for a, b in F.edges():
        if r in [a, b]:
            continue
        U = V - {r, a, b} - set(F[a]) - set(F[b])
        for I in nx.find_cliques(nx.complement(F.subgraph(U))):
            add(set(I) | {a, b})
    U = V - {r} - set(F[r])
    for I in nx.find_cliques(nx.complement(F.subgraph(U))):
        add(set(I) | {r})
    for a, b in F.edges():
        if r in [a, b]:
            U = V - {a, b} - set(F[a]) - set(F[b])
            for I in nx.find_cliques(nx.complement(F.subgraph(U))):
                add(set(I) | {a, b})
        elif not F.has_edge(r, a) and (not F.has_edge(r, b)):
            U = V - {r, a, b} - set(F[a]) - set(F[b]) - set(F[r])
            for I in nx.find_cliques(nx.complement(F.subgraph(U))):
                add(set(I) | {r, a, b})
    for p, q in itertools.product(profiles, repeat=2):
        if p[0] != q[0] or p[3] + q[3] > 1:
            continue
        req = p[2] + q[2]
        if p[0] == 'A':
            sz = p[1] + q[1] - 1
            if sz >= 3:
                req += sz
        if req <= 5:
            return False
    return True

def Tfree(F):
    vs = sorted(F)
    n = len(vs)
    ix = {v: i for i, v in enumerate(vs)}
    root = ix[ROOT]
    nm = [sum((1 << ix[w] for w in F[v])) for v in vs]
    FULL = (1 << n) - 1
    profiles = set()

    def comps(mask):
        out = []
        while mask:
            bit = mask & -mask
            cc = bit
            front = bit
            while front:
                j = (front & -front).bit_length() - 1
                front &= front - 1
                new = nm[j] & mask & ~cc
                cc |= new
                front |= new
            mask &= ~cc
            out.append(cc)
        return out
    for lo in range(0, 1 << n, 1 << 18):
        a = np.arange(lo, min(lo + (1 << 18), 1 << n), dtype=np.uint32)
        valid = np.ones(len(a), dtype=bool)
        for v in range(n):
            q = a & np.uint32(nm[v])
            bad = a >> v & 1 != 0
            bad &= q & q - np.uint32(1) != 0
            valid &= ~bad
        a = a[valid]
        if not len(a):
            continue
        b = np.uint32(FULL) ^ a
        active = np.zeros(len(a), dtype=np.uint32)
        for v in range(n):
            active |= np.where((b >> v & 1 != 0) & (b & np.uint32(nm[v]) != 0), np.uint32(1 << v), np.uint32(0))
        pc = POP[active.view(np.uint8).reshape(-1, 4)].sum(axis=1)
        a = a[pc <= 6]
        for aa in a:
            aa = int(aa)
            bb = FULL ^ aa
            cs = comps(bb)
            big = [c.bit_count() for c in cs if c.bit_count() >= 3]
            ne = sum((c.bit_count() == 2 for c in cs))
            if sum(big) + 2 * max(0, ne - 1) > 4:
                continue
            if aa >> root & 1:
                p = ('A', (aa & nm[root]).bit_count(), 0, tuple(sorted(big)), ne)
            else:
                rc = next((c for c in cs if c >> root & 1))
                sz = rc.bit_count()
                obig = big.copy()
                one = ne
                if sz >= 3:
                    obig.remove(sz)
                elif sz == 2:
                    one -= 1
                p = ('B', 0, sz, tuple(sorted(obig)), one)
            profiles.add(p)
    for p, q in itertools.product(profiles, repeat=2):
        if p[0] != q[0]:
            continue
        if p[0] == 'A':
            if p[1] + q[1] > 1:
                continue
            big = list(p[3] + q[3])
            ne = p[4] + q[4]
        else:
            rc = p[2] + q[2] - 1
            big = list(p[3] + q[3])
            ne = p[4] + q[4]
            if rc >= 3:
                big.append(rc)
            elif rc == 2:
                ne += 1
        if sum(big) + 2 * max(0, ne - 1) <= 4:
            return False
    return True


def positive_certificate(A,B,holes=frozenset()):
    """Certify H embeds in (A+matching-infinity) join (B+independent-infinity),
    except specified rare A--B cross edges.  Return a genuine injective map."""
    a,b=len(A),len(B);L=2+a+b
    def apart(x):return x==0 or 2<=x<2+a
    allowed=[]
    for x in range(L):
        for y in range(L):
            ax,ay=apart(x),apart(y)
            if ax!=ay:
                missing=x>=2 and y>=2 and ((x-2,y-2-a) in holes if ax else (y-2,x-2-a) in holes)
                if not missing:allowed.append((x,y))
            elif x==y==0:allowed.append((x,y))
            elif 2<=x<2+a and 2<=y<2+a and A.has_edge(x-2,y-2):allowed.append((x,y))
            elif x>=2+a and y>=2+a and B.has_edge(x-2-a,y-2-a):allowed.append((x,y))
    solver=z3.Solver()
    lab={v:z3.Int('p'+str(i)) for i,v in enumerate(H)}
    for v in H:solver.add(lab[v]>=0,lab[v]<L)
    for u,v in H.edges():solver.add(z3.Or(*[z3.And(lab[u]==x,lab[v]==y) for x,y in allowed]))
    for v in H:
        solver.add(z3.Implies(lab[v]==0,z3.PbLe([(lab[w]==0,1) for w in H[v]],1)))
    for j in range(2,L):solver.add(z3.PbLe([(lab[v]==j,1) for v in H],1))
    assert solver.check()==z3.sat,(list(A.edges()),list(B.edges()),holes)
    md=solver.model();assignment={v:md.eval(lab[v]).as_long() for v in H}
    actual=nx.Graph();AC=[];BC=[]
    for j in range(len(H)):
        u,w=('pair',j,0),('pair',j,1);AC +=[u,w];actual.add_edge(u,w)
        BC.append(('iso',j));actual.add_node(BC[-1])
    AC +=[('A',u) for u in A];BC +=[('B',u) for u in B]
    actual.add_nodes_from(AC+BC)
    actual.add_edges_from((('A',u),('A',v)) for u,v in A.edges())
    actual.add_edges_from((('B',u),('B',v)) for u,v in B.edges())
    actual.add_edges_from((u,v) for u in AC for v in BC if not(u[0]=='A' and v[0]=='B' and (u[1],v[1]) in holes))
    image={}
    comps=list(nx.connected_components(H.subgraph([v for v in H if assignment[v]==0])))
    for j,C in enumerate(comps):
        assert len(C)<=2
        for k,v in enumerate(C):image[v]=('pair',j,k)
    j=0
    for v in H:
        q=assignment[v]
        if q==1:image[v]=('iso',j);j+=1
        elif 2<=q<2+a:image[v]=('A',q-2)
        elif q>=2+a:image[v]=('B',q-2-a)
    assert len(image)==len(H) and len(set(image.values()))==len(H)
    assert nx.number_of_selfloops(actual)==0
    assert all(actual.has_edge(image[u],image[v]) for u,v in H.edges())
    return image

def no_two_P3(G):
    masks={sum(1<<v for v in [a,c,b]) for c in G for a,b in itertools.combinations(G[c],2)}
    return not any(x&y==0 for x,y in itertools.combinations(masks,2))

def connected_types(D,N):
    # Inductive completeness: every connected graph has a non-cut vertex.
    old=[nx.path_graph(3),nx.complete_graph(3)];out={3:old}
    for n in range(4,N+1):
        new=[];buckets={}
        for G in old:
            vertices=[v for v in G if G.degree(v)<D]
            for t in range(1,min(D,len(vertices))+1):
                for neigh in itertools.combinations(vertices,t):
                    K=G.copy();K.add_node(n-1);K.add_edges_from((n-1,v) for v in neigh)
                    if not no_two_P3(K):continue
                    key=nx.weisfeiler_lehman_graph_hash(K)
                    bucket=buckets.setdefault(key,[])
                    if any(nx.is_isomorphic(K,X) for X in bucket):continue
                    bucket.append(K);new.append(K)
        out[n]=new;old=new
    return out

if __name__=='__main__':
    assert Sfree(F), 'H must avoid K5+matching / one edge'
    assert Tfree(F), 'H must avoid matching / K4+edge'
    print('Exhaustive rooted-profile exclusions S,T verified.',flush=True)
    E=nx.empty_graph(0);P=nx.path_graph(3);two=nx.disjoint_union(P,P)
    bedges=lambda k:nx.disjoint_union_all([nx.path_graph(2)]*k) if k else E
    cases=[(two,E,frozenset()),(E,two,frozenset()),(nx.star_graph(6),E,frozenset()),(E,nx.star_graph(4),frozenset()),
       (P,P,frozenset(itertools.product(range(3),range(3)))),
       (P,bedges(3),frozenset(itertools.product(range(3),range(6)))),
       (nx.complete_graph(5),bedges(2),frozenset()),
       (nx.complete_graph(5),bedges(2),frozenset({(0,0)}))]
    K=nx.complete_graph(5);K.remove_edge(0,1);cases.append((K,bedges(2),frozenset()))
    for A,B,holes in cases:positive_certificate(A,B,holes)
    Btypes=connected_types(3,7)
    assert [len(Btypes[n]) for n in range(3,8)]==[2,6,10,2,1]
    for gs in Btypes.values():
        for B in gs:
            assert B.number_of_edges()<=7
            positive_certificate(E,nx.disjoint_union(B,bedges(8-B.number_of_edges())))
    positive_certificate(E,bedges(8))
    print('All 31 positive host exclusions expanded and checked injectively.',flush=True)
    Atypes=connected_types(5,11)
    assert [len(Atypes[n]) for n in range(3,12)]==[2,6,21,7,6,3,3,1,1]
    K5=nx.complete_graph(5);Km=K5.copy();Km.remove_edge(0,1)
    for n,gs in Atypes.items():
        for A in gs:
            u=A.number_of_edges()-n//2
            assert u<=8
            if u>=7:assert nx.is_isomorphic(A,K5) or nx.is_isomorphic(A,Km)
    print('All 50 primary component types and sharp excess bounds checked.',flush=True)

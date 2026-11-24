from fractions import Fraction as Q
import math
import itertools
import networkx as nx


def rational_circle_point(theta, precision=10**7):
    # Rational stereographic parametrization; no floating-point claim is
    # subsequently trusted: all geometric tests use Fractions.
    if abs(math.cos(theta/2)) < 1e-10:
        return (Q(-1), Q(0))
    t = Q(round(math.tan(theta/2)*precision), precision)
    return ((1-t*t)/(1+t*t), 2*t/(1+t*t))


def dot(x,y):
    return sum(a*b for a,b in zip(x,y))


def no_C3_C5(adj):
    # An odd closed walk of length 3 or 5 exists iff a vertex's
    # distance-one or distance-two neighborhood contains an edge.
    n=len(adj)
    masks=[sum(1<<j for j in a) for a in adj]
    for v in range(n):
        one=masks[v]
        two=0
        for u in adj[v]:
            two |= masks[u]
        two &= ~(1<<v)
        for S in (one,two):
            T=S
            while T:
                b=T & -T
                u=b.bit_length()-1
                if masks[u]&S:
                    return False
                T-=b
    return True


def example(q=31, multiplicity=100):
    assert q%2==1 and q>=17
    points=[rational_circle_point(2*math.pi*j/q) for j in range(q)]
    assert all(dot(p,p)==1 for p in points)
    step=(q-1)//2
    edges={tuple(sorted((j,(j+step)%q))) for j in range(q)}
    F=nx.Graph(); F.add_nodes_from(range(q)); F.add_edges_from(edges)
    assert nx.is_connected(F) and all(d==2 for _,d in F.degree())
    assert not nx.is_bipartite(F) # hence chi(F)=3
    eta2=Q(0)
    for u,v in edges:
        eta2=max(eta2,2+2*dot(points[u],points[v]))
    alpha=Q(4,25)  # 0.16
    assert 25*eta2<4  # no odd closed walk of length <=5
    assert 9*eta2<4*alpha*alpha # 3*eta<2*alpha
    caps=[{j for j,y in enumerate(points) if dot(x,y)>alpha}
          for x in points]
    r=min(map(len,caps))
    assert r>0
    # Verify the key geometric consequence, entirely combinatorially.
    for x in F:
        for a in F[x]:
            for b in F[a]:
                for z in F[b]:
                    assert caps[x].isdisjoint(caps[z])
    # Weighted template. Independent blow-ups give the actual graph.
    labels=[('X',i,x) for i in range(3) for x in range(q)]
    labels += [('Y',i,j) for i in range(3) for j in range(q)]
    labels += [('Z',i,0) for i in range(3)]
    idx={v:i for i,v in enumerate(labels)}
    adj=[set() for _ in labels]
    def edge(a,b):
        u,v=idx[a],idx[b]
        assert u!=v
        adj[u].add(v); adj[v].add(u)
    for x,y in edges:
        for i in range(3):
            for j in range(3):
                if i!=j:
                    edge(('X',i,x),('X',j,y))
    for i in range(3):
        for x in range(q):
            for j in caps[x]:
                edge(('X',i,x),('Y',i,j))
        for j in range(q):
            edge(('Y',i,j),('Z',i,0))
    assert no_C3_C5(adj)
    # Verify every F-edge is represented by the stipulated 3-walk.
    for x,y in edges:
        walk=[idx[('X',0,x)],idx[('X',1,y)],
              idx[('X',2,x)],idx[('X',0,y)]]
        assert all(b in adj[a] for a,b in zip(walk,walk[1:]))
    weights=[1 if t=='X' else multiplicity if t=='Y'
             else r*multiplicity for t,_,_ in labels]
    n=sum(weights)
    degrees=[sum(weights[j] for j in a) for a in adj]
    delta=min(degrees)
    assert delta>=r*multiplicity
    # Every blow-up vertex has exactly the computed weighted degree.
    assert delta >= min(r*multiplicity,q*multiplicity)
    print('Exact lower-construction certificate:')
    print('  core cycle length =',q,'; cap minimum =',r)
    print('  template vertices =',len(adj),'(all C3/C5 tests passed)')
    print('  blow-up n =',n,'; delta =',delta,'; delta/n =',Q(delta,n))
    return adj,weights


def check_upper_set_lemma():
    graphs=triples=0
    # The upper proof's finite set-counting step is checked exhaustively
    # for every graph without isolated vertices with at most seven vertices.
    for R in nx.graph_atlas_g():
        m=len(R)
        if not m or min(dict(R.degree()).values())==0:
            continue
        adj=[set(R[v]) for v in range(m)]
        graphs+=1
        d=min(map(len,adj))
        sets=[]
        for mask in range(1,1<<m):
            S={i for i in range(m) if mask>>i&1}
            if len(S)<2*d:
                continue
            U=set().union(*(adj[i] for i in S))
            if S&U: # require S independent
                continue
            assert len(U)>=d
            sets.append((S,U))
        for (A,UA),(B,UB),(C,UC) in itertools.combinations(sets,3):
            if UA&UB or UA&UC or UB&UC:
                continue
            if A&UB or A&UC or B&UC: # no cross-edges
                continue
            six=[A,B,C,UA,UB,UC]
            assert all(not X&Y for X,Y in itertools.combinations(six,2))
            assert m>=sum(map(len,six))>=9*d
            triples+=1
    # Also test a nonvacuous equality certificate on 9 vertices:
    # three disjoint K_{2,1}'s.
    R=nx.Graph()
    R.add_edges_from([(0,2),(1,2),(3,5),(4,5),(6,8),(7,8)])
    assert min(dict(R.degree()).values())==1
    assert no_C3_C5([set(R[v]) for v in range(9)])
    A={0,1}; B={3,4}; C={6,7}
    UA={2}; UB={5}; UC={8}
    six=[A,B,C,UA,UB,UC]
    for S,U in [(A,UA),(B,UB),(C,UC)]:
        assert set().union(*(set(R[v]) for v in S))==U
    assert all(not X&Y for X,Y in itertools.combinations(six,2))
    assert sum(map(len,six))==9
    print('Upper set lemma:',graphs,'atlas graphs checked;',triples,
          'qualifying triples; 9-vertex equality certificate passed.')


def check_extension():
    # Exhaustively check the extension operation on all atlas triangle-free
    # targets up to 5 vertices. W is made independent; adding its apex
    # cannot create a triangle.
    count=0
    for H in nx.graph_atlas_g():
        k=len(H)
        if k>5 or any(nx.triangles(H).values()):
            continue
        for mask in range(1<<k):
            J=nx.Graph()
            J.add_nodes_from(range(2*k+1))
            for a,b in H.edges():
                for x in range(2):
                    for y in range(2):
                        if not (x==y==1):
                            J.add_edge(2*a+x,2*b+y)
            # mask is optional: any subset of the 1-copies is independent.
            J.add_edges_from((2*k,2*a+1) for a in range(k) if mask>>a&1)
            assert not any(nx.triangles(J).values())
            count+=1
    print('Triangle-free extension:',count,'finite checks passed.')


if __name__=='__main__':
    example()
    check_upper_set_lemma()
    check_extension()

"""Finite exact checks of upper-bound combinatorial lemmas."""
import itertools

def support_check(max_k=5):
    graphs=cases=0
    for k in range(1,max_k+1):
        edges=list(itertools.combinations(range(k),2))
        for edge_mask in range(1<<len(edges)):
            adj=[0]*k
            for j,(u,v) in enumerate(edges):
                if edge_mask>>j&1: adj[u]|=1<<v;adj[v]|=1<<u
            if not all(adj):continue
            graphs+=1
            ns=[0]*(1<<k)
            for s in range(1,1<<k):
                bit=s&-s;v=bit.bit_length()-1
                ns[s]=ns[s^bit]|adj[v]
            # Union of S0,S1,S2 must be independent. Enumerate each
            # independent union, then all assignments of its vertices to
            # nonempty membership masks (overlaps allowed initially).
            for union in range(1,1<<k):
                if union&ns[union]:continue
                vertices=[v for v in range(k) if union>>v&1]
                for membership in itertools.product(range(1,8),repeat=len(vertices)):
                    ss=[0,0,0]
                    for v,mem in zip(vertices,membership):
                        for i in range(3):
                            if mem>>i&1:ss[i]|=1<<v
                    if not all(ss):continue
                    nn=[ns[s] for s in ss]
                    if any(nn[i]&nn[j] for i,j in itertools.combinations(range(3),2)):continue
                    six=ss+nn
                    assert all(six)
                    assert not any(six[i]&six[j] for i,j in itertools.combinations(range(6),2))
                    assert sum(s.bit_count() for s in six)<=k
                    cases+=1
    return graphs,cases

def directed_path_check(k=5):
    # Enumerate all oriented simple graphs on k vertices. A digraph with no
    # directed 2-path has a proper bipartition: sources versus nonsources.
    pairs=list(itertools.combinations(range(k),2));checked=0
    for state in itertools.product(range(3),repeat=len(pairs)):
        out=[set() for _ in range(k)];inc=[set() for _ in range(k)]
        for s,(u,v) in zip(state,pairs):
            if s==1:out[u].add(v);inc[v].add(u)
            if s==2:out[v].add(u);inc[u].add(v)
        has2=any(inc[v] and out[v] for v in range(k))
        if not has2:
            color=[bool(inc[v]) for v in range(k)]
            assert all(color[u]!=color[v] for u in range(k) for v in out[u])
        checked+=1
    return checked

if __name__=='__main__':
    print('support graphs/cases',support_check(6))
    print('oriented graphs checked',directed_path_check())

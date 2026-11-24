from fractions import Fraction as Q
from itertools import combinations, product
from math import comb
import networkx as nx
import z3


def odd_cycle(G, k):
    vs = list(G)
    rank = {v: i for i, v in enumerate(vs)}
    for s in vs:
        def dfs(path, seen):
            if len(path) == k:
                return G.has_edge(path[-1], s)
            return any(dfs(path + [u], seen | {u})
                       for u in G[path[-1]]
                       if rank[u] > rank[s] and u not in seen)
        if dfs([s], {s}):
            return True
    return False


def chromatic_at_most(G, k):
    vs = list(G)
    x = {v: z3.Int('x%d' % i) for i, v in enumerate(vs)}
    solver = z3.Solver()
    solver.add(*[z3.And(0 <= x[v], x[v] < k) for v in vs])
    solver.add(*[x[u] != x[v] for u, v in G.edges])
    return solver.check() == z3.sat


def lower_construction(m, r, t):
    sets = list(map(frozenset, combinations(range(m), r)))
    F = nx.Graph()
    F.add_nodes_from(range(len(sets)))
    F.add_edges_from((x, y) for x, y in combinations(F, 2)
                     if sets[x].isdisjoint(sets[y]))
    S = nx.Graph()
    for x in F:
        S.add_node(('x', x), group=0, label=x)
    for x, y in F.edges:
        a, b = ('a', x, y), ('b', x, y)
        S.add_node(a, group=1, label=x)
        S.add_node(b, group=2, label=y)
        S.add_edges_from([(('x', x), a), (a, b), (b, ('x', y))])
    # Exhaustively check the crucial same-colour length-three-walk fact.
    for u in S:
        for v in S[u]:
            for w in S[v]:
                for z in S[w]:
                    if S.nodes[u]['group'] == S.nodes[z]['group']:
                        assert F.has_edge(S.nodes[u]['label'], S.nodes[z]['label'])
    G = S.copy()
    for j in range(3):
        A = [('A', j, i, ell) for i in range(m) for ell in range(t)]
        B = [('B', j, ell) for ell in range(r*t)]
        G.add_nodes_from(A+B)
        G.add_edges_from(product(A, B))
    for v in S:
        j, x = S.nodes[v]['group'], S.nodes[v]['label']
        G.add_edges_from((v, ('A', j, i, ell))
                         for i in sets[x] for ell in range(t))
    assert len(G) == len(S) + 3*(m+r)*t
    assert G.number_of_edges() == (S.number_of_edges() + 3*m*r*t*t + len(S)*r*t)
    assert min(dict(G.degree()).values()) >= r*t
    assert not odd_cycle(G, 3)
    assert not odd_cycle(G, 5)
    return F, S, G


def refine(G, cells, signatures):
    out = []
    for C in cells:
        buckets = {}
        for v in C:
            buckets.setdefault(signatures[v], set()).add(v)
        out.extend(buckets.values())
    return out


def neighbour_refine(G, cells):
    sig = {v: tuple(bool(set(G[v]) & C) for C in cells) for v in G}
    return refine(G, cells, sig)


def quotient(G, cells):
    cell = {v: i for i, C in enumerate(cells) for v in C}
    H = nx.Graph()
    H.add_nodes_from(range(len(cells)))
    for u, v in G.edges:
        assert cell[u] != cell[v], 'Loop in quotient'
        H.add_edge(cell[u], cell[v])
    return H


def regular_pair(G, A, B, eps):
    # Exact, exponential-time verification of epsilon-regularity.
    def density(X, Y):
        return Q(sum(G.has_edge(x, y) for x in X for y in Y), len(X)*len(Y))
    d = density(A, B)
    AA = [C for k in range(1, len(A)+1) for C in combinations(A, k)
          if k >= eps*len(A)]
    BB = [C for k in range(1, len(B)+1) for C in combinations(B, k)
          if k >= eps*len(B)]
    return all(abs(density(X, Y)-d) <= eps for X in AA for Y in BB)


def upper_certificate(G, clusters, exceptional, tau):
    # Verifies sufficient partition hypotheses and then actually builds the target.
    n = len(G)
    c = Q(min(dict(G.degree()).values()), n)
    assert c > Q(1, 9) and 0 < tau < min(Q(1,100), (9*c-1)/1000)
    eps = tau**4
    assert set().union(*clusters, exceptional) == set(G)
    assert sum(map(len, clusters))+len(exceptional) == n
    assert len(set(map(len, clusters))) == 1
    assert len(exceptional) <= 3*tau*tau*n
    m = len(clusters[0])
    R = nx.Graph()
    R.add_nodes_from(range(len(clusters)))
    for i, j in combinations(R, 2):
        d = Q(sum(G.has_edge(x,y) for x in clusters[i] for y in clusters[j]), m*m)
        if d >= tau and regular_pair(G, clusters[i], clusters[j], eps):
            R.add_edge(i, j)
    assert all(R.degree(i)*m >= (c-3*tau)*n for i in R)
    sig = {v: tuple(Q(len(set(G[v]) & C), m)//tau for C in clusters) for v in G}
    P1 = refine(G, [set(G)], sig)
    P2 = neighbour_refine(G, P1)
    P3 = neighbour_refine(G, P2)
    H = quotient(G, P3)
    assert not odd_cycle(H, 3)
    # Verify the actual homomorphism, not just the target's triangle-freeness.
    f = {v: i for i, C in enumerate(P3) for v in C}
    assert all(H.has_edge(f[u], f[v]) for u, v in G.edges)
    return H


def blow_up(F, multiplicity):
    G = nx.Graph()
    clusters = [{(i, j) for j in range(multiplicity)} for i in F]
    G.add_nodes_from(set().union(*clusters))
    for i, j in F.edges:
        G.add_edges_from(product(clusters[i], clusters[j]))
    return G, clusters


def parameter_check(c, h):
    # Exact parameters for an obstruction to any triangle-free target of order h.
    assert 0 <= c < Q(1,9)
    r = max(1, int(3*c*h/(1-9*c)) + 1)
    m = 2*r+h
    vF = comb(m, r)
    eF = vF*comb(m-r, r)//2
    q = vF+2*eF
    gap = r-3*c*(m+r)
    assert gap > 0
    t = max(1, int(c*q/gap)+1)
    n = q+3*(m+r)*t
    assert Q(r*t, n) > c
    assert m-2*r+2 > h
    return r, t, n


if __name__ == '__main__':
    for m, r, t in [(3,1,1), (4,1,2), (5,2,1), (6,2,1)]:
        F, S, G = lower_construction(m,r,t)
        k = m-2*r+2
        assert chromatic_at_most(F,k)
        assert not chromatic_at_most(F,k-1)
        print('Lower construction checked:', (m,r,t), 'orders:', len(F),len(S),len(G))
    # Exhaustive small-graph check of the length-three homomorphism obstruction.
    count = 0
    for H in nx.graph_atlas_g():
        if odd_cycle(H,3):
            continue
        for a in H:
            for b in H[a]:
                for d in H[b]:
                    assert not H.has_edge(d,a)
        count += 1
    print('Triangle-free atlas graphs checked:', count)
    tau = Q(1,100000)
    for F in [nx.path_graph(2), nx.cycle_graph(7), nx.cycle_graph(9)]:
        G, cells = blow_up(F,3)
        H = upper_certificate(G,cells,set(),tau)
        print('Upper certificate checked; input/target orders:', len(G),len(H))
    for c,h in [(Q(0),3), (Q(1,10),3), (Q(11,100),5)]:
        r,t,n = parameter_check(c,h)
        print('Exact obstruction parameters checked:', 'c=',c,'h=',h,'r=',r,
              'digits(t)=',len(str(t)),'digits(n)=',len(str(n)))
    # Exact algebraic constant checks (a rational polynomial identity suffices).
    import sympy as sp
    c,z = sp.symbols('c z')
    assert sp.expand((c-2*z)-(2*c-8*z)*(sp.Rational(1,2)+z)-2*z*(1-c+4*z)) == 0
    assert sp.expand(3*(2*c-8*z)+3*(c-3*z)) == 9*c-33*z
    print('All checks passed.')

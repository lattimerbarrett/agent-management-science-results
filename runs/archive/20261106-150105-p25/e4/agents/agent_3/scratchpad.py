import itertools, networkx as nx
from z3 import *

def directed_path_check(n):
    es=list(itertools.combinations(range(n),2))
    total=0
    # Graph orientations with neither a directed 2path nor an undirected odd cycle.
    for vals in itertools.product(range(3),repeat=len(es)):
        out=[set() for _ in range(n)]; inc=[set() for _ in range(n)]
        G=nx.Graph();G.add_nodes_from(range(n))
        for (u,v),x in zip(es,vals):
            if x:
                if x==2:u,v=v,u
                out[u].add(v);inc[v].add(u);G.add_edge(u,v)
        has2=any(any(u!=w for u in inc[v] for w in out[v]) for v in range(n))
        if not has2:assert nx.is_bipartite(G)
        total+=1
    return total

def support_check(k):
    s=Solver()
    R=[[Bool(f'r_{k}_{i}_{j}') for j in range(k)] for i in range(k)]
    S=[[Bool(f's_{k}_{p}_{i}') for i in range(k)] for p in range(3)]
    for i in range(k):
        s.add(Not(R[i][i]),Or(R[i]))
        for j in range(k):s.add(R[i][j]==R[j][i])
    T=[[Or([And(S[p][j],R[j][i]) for j in range(k)]) for i in range(k)]for p in range(3)]
    for p in range(3):
        s.add(Or(S[p]))
        for i in range(k):
            for j in range(k):s.add(Not(And(S[p][i],S[p][j],R[i][j])))
    for p,q in itertools.combinations(range(3),2):
        # G edges imply no common R-neighbor of support sets.
        for i in range(k):s.add(Not(And(T[p][i],T[q][i])))
        # G length-two paths imply no R-edge between support sets.
        for i in range(k):
            for j in range(k):s.add(Not(And(S[p][i],S[q][j],R[i][j])))
    allsets=S+T
    for a,b in itertools.combinations(range(6),2):
        s.push();s.add(Or([And(allsets[a][i],allsets[b][i])for i in range(k)]))
        assert s.check()==unsat,(k,a,b)
        s.pop()
    return 15

def partitions(n):
    a=[0]*n
    def rec(i,m):
        if i==n:yield tuple(a);return
        for v in range(m+2):
            a[i]=v;yield from rec(i+1,max(m,v))
    yield from rec(1,0)

def witness_check():
    count=0
    for a in partitions(7):
        if len({a[0],a[3],a[6]})<3:continue
        if any(a[i]==a[i+1]for i in range(6)):continue
        G=nx.Graph();G.add_edges_from(zip(a,a[1:]))
        # Matrix walk counts detect an odd closed walk of length3/5.
        import numpy as np
        A=nx.to_numpy_array(G,dtype=int)
        if any(np.trace(np.linalg.matrix_power(A,l)) for l in (3,5)):continue
        assert a[1]!=a[4] and a[2]!=a[5]
        # These are odd length3 witnesses within q and r respectively.
        assert all(G.has_edge(a[i],a[i+1])for i in (1,2,3,4))
        count+=1
    return count

if __name__=='__main__':
    from pathlib import Path
    Path('workspace/agent3_upper_checks.py').write_text(Path(__file__).read_text())
    print('Oriented graphs checked:',sum(directed_path_check(n)for n in range(1,6)))
    print('Six-set intersection implications:',sum(support_check(k)for k in range(2,9)))
    print('Walk vertex-identification cases:',witness_check())
    Path('workspace/agent3_upper_proof.md').write_text(r'''# Complete upper-bound argument

Fix c>1/9. Put t=(9c-1)/1000, epsilon=t^2. Use the equitable regularity lemma with precision epsilon, lower bound k0>=1/epsilon, and cluster size at least 20/t^2 (the latter follows by requiring n sufficiently large once the lemma's upper bound on k0 is known). Write the initial clusters as V1,...,Vk0, all size m, with exceptional set at most epsilon n. At most epsilon k0^2 unordered pairs are irregular.

Move to the exceptional set all clusters incident with more than t k0 irregular pairs. There are at most 2t k0 such clusters. Write k for the remaining number of clusters and E for the enlarged exceptional set. Thus |E|<=(epsilon+2t)n. Define R on these k clusters by retaining the epsilon-regular pairs of density at least t. For each remaining cluster, average the original minimum-degree bound over its vertices. Edges to E contribute at most |E| per vertex; internal edges at most m<=epsilon n; irregular pairs contribute at most t k0 m<=tn; pairs of density below t contribute at most tkm<=tn on average; all remaining edges contribute at most d_R(i)m. Consequently

 d_R(i)m >= (c-4t-2epsilon)n >= (c-6t)n >= (c-6t)km.

In particular R has no isolated vertices.

For every vertex v of G, including exceptional vertices, define its profile
 S(v)={i: |N_G(v) intersect Vi|>=tm}.
Outside the clusters in S(v), v has at most |E|+tkm<=4tn neighbors. Therefore |S(v)|>=(c-4t)k. Define J on V(G) by joining distinct vertices if there is a G-walk of length 1 or 3 between them. If uv is an edge of J, then N_G(u) and N_G(v) are disjoint: a common neighbor together with the odd walk would give an odd closed walk of length 3 or 5, and hence a C3 or C5. In particular, if u,v have the same profile S and uv is a J-edge, then

 |S|m >= |N(u) union N(v)|-8tn >=2(c-4t)n >=2(c-4t)km.       (1)

Call such a profile bad.

The following elementary regular-pair connector consequences hold, for all original vertices, not just typical vertices:

(a) S(v) is independent in R. Otherwise the two large subsets N(v) intersect Vi and N(v) intersect Vj are connected by an edge of their regular pair, giving a triangle.

(b) If xy is a G-edge, then N_R(S(x)) and N_R(S(y)) are disjoint. For otherwise, choose a common R-neighbor j of i in S(x) and l in S(y). The two regular pairs ij and lj connect x to y by a length-four path x-a-b-d-y. Together with xy this gives a C5. This also works if i=l: almost every b in Vj has at least (t-epsilon)tm neighbors in both large endpoint subsets, and these neighbors can be selected distinct.

(c) If x-z-y is a G-path of length two with x!=y, then there is no R-edge between S(x) and S(y): such an edge connects x and y by a length-three path, making a C5 together with x-z-y.

All these connectors can avoid the finitely many prescribed original vertices. Indeed remove those (at most three) vertices from endpoint subsets first; the subsets remain larger than epsilon m. Regularity supplies their required edges, or supplies a central vertex good for both endpoint subsets; each good central vertex has at least (t-epsilon)(tm-3)>3 available neighbors. The bound m>=20/t^2 ensures all these inequalities. Thus the constructed cycles have genuinely distinct vertices. Finally (b) implies S(x) and S(y) are disjoint when xy is a G-edge, since any common cluster has a neighbor in R. It follows that each profile class is independent in G.

There are M<=2^k profiles. Fix a profile p. For each J-edge xy inside its class, choose a length-three witnessing path x-a-b-y, orient the edge x->y, and color it by the ordered pair of profiles (q,r) of a,b. The witnessing path is simple, since a repeated vertex would imply xy is already a G-edge. There are at most M^2 edge colors.

Suppose chi(J[p])>2^(M^2). If every one-color subgraph were bipartite, the product of their two-colorings would properly color J[p] with at most 2^(M^2) colors. Hence some one-color subgraph is nonbipartite. Any orientation of a nonbipartite graph contains a directed two-edge path x0->x1->x2: otherwise no vertex has both an incoming and an outgoing edge, and sources/sinks give a bipartition. Its witnesses concatenate to

 x0-a0-b0-x1-a1-b1-x2,

with profiles p,q,r,p,q,r,p. The endpoints x0,x1,x2 are distinct. Also a0!=a1 and b0!=b1, since equality would give a triangle in the corresponding length-three subwalk. Consequently p,q,r are all bad: the subwalks x0-a0-b0-x1, a0-b0-x1-a1 and b0-x1-a1-b1 are J-edges within these profiles. The profiles are distinct, since successive ones occur on G-edges.

Put Sp=p,Sq=q,Sr=r and Ti=N_R(Si). These six sets are pairwise disjoint. Indeed G-edges occur between every pair of the three profiles, so (b) gives pairwise disjoint Ti and also pairwise disjoint Si. The displayed length-six walk contains genuine length-two paths between every pair of profiles: p-q-r, q-r-p, and r-p-q. Thus (c) prohibits every R-edge between different Si; (a) prohibits edges within each Si. Hence every Si is disjoint from every Tj.

By (1), each Si has at least 2(c-4t)k vertices; each Ti has at least delta(R)>=(c-6t)k vertices since Si is nonempty. Therefore

 k >= sum_i(|Si|+|Ti|) >= [6(c-4t)+3(c-6t)]k = (9c-42t)k >k,

a contradiction. We conclude chi(J)<=M*2^(M^2), uniformly bounded in n (because k is bounded by the regularity lemma).

To finish, for any q-coloring gamma of J, define a finite target W_q whose vertices are pairs (i,A), i in [q], A subset [q] minus {i}; join (i,A) to (j,B) exactly when i in B, j in A and A intersect B is empty. Map v to (gamma(v),{gamma(u):u in N_G(v)}). For a G-edge xy the two neighbor-color sets are disjoint, since a shared color would give equally colored endpoints of a length-three G-walk. Thus this is a homomorphism. W_q is triangle-free: in a purported triangle, the first coordinate of the third vertex belongs to both neighbor-color sets of the first two, contradicting their disjointness. For the finitely many n below the regularity threshold, add to W_q one disjoint copy of every C3,C5-free graph of those orders. The resulting fixed finite target is triangle-free and receives every required G.
''')

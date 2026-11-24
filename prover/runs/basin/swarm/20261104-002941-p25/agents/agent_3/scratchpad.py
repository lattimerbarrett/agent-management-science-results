from pathlib import Path
p=Path('workspace/agent3_upper_checks.py')
p.write_text('''import itertools
import networkx as nx

def odd_cube(G):
    F=nx.Graph();F.add_nodes_from(G)
    for x in G:
        reach=set(G[x])
        for a in G[x]:
            for b in G[a]:
                reach.update(G[b])
        assert x not in reach
        F.add_edges_from((x,y) for y in reach)
    return F

def universal(k):
    V=[(a,mask) for a in range(k) for mask in range(1<<k) if not(mask>>a&1)]
    H=nx.Graph();H.add_nodes_from(V)
    for (a,A),(b,B) in itertools.combinations(V,2):
        if (B>>a&1) and (A>>b&1) and not(A&B):H.add_edge((a,A),(b,B))
    assert not any(nx.triangles(H).values())
    return H

def verify_map(G):
    F=odd_cube(G)
    col=nx.coloring.greedy_color(F,strategy='largest_first')
    k=max(col.values(),default=-1)+1
    images={v:(col[v],sum(1<<a for a in {col[w] for w in G[v]})) for v in G}
    for x,y in G.edges():
        a,A=images[x];b,B=images[y]
        assert a!=b and B>>a&1 and A>>b&1 and not(A&B)

def main():
    for k in range(1,6):
        H=universal(k)
        print('Universal target',k,H.number_of_nodes(),H.number_of_edges(),'triangle-free')
    count=0
    for G in nx.graph_atlas_g():
        if len(G)==0:continue
        # exact closed-odd-walk test by adjacency matrix integer powers
        import numpy as np
        A=nx.to_numpy_array(G,dtype='int64')
        if np.trace(A@A@A) or np.trace(A@A@A@A@A):continue
        verify_map(G);count+=1
    print('Odd-cube and target-map checks on all',count,'C3,C5-free atlas graphs through 7 vertices')
    # Exhaustively verify six-set disjointness from the reduced-graph constraints.
    count=0;k=4
    pairs=list(itertools.combinations(range(k),2))
    for bits in range(1<<len(pairs)):
        nbr=[0]*k
        for j,(a,b) in enumerate(pairs):
            if bits>>j&1:nbr[a]|=1<<b;nbr[b]|=1<<a
        def N(S):
            ans=0
            for i in range(k):
                if S>>i&1:ans|=nbr[i]
            return ans
        for S,T,U in itertools.product(range(1,1<<k),repeat=3):
            sets=(S,T,U); ns=tuple(map(N,sets))
            if any(not z for z in ns):continue
            if any(a&b for a,b in itertools.combinations(sets,2)):continue
            if any(a&b for a,b in itertools.combinations(ns,2)):continue
            union=S|T|U
            if union&(ns[0]|ns[1]|ns[2]):continue
            allsets=sets+ns
            assert all(not(a&b) for a,b in itertools.combinations(allsets,2))
            assert sum(z.bit_count() for z in allsets)<=k
            count+=1
    print('Exhaustive six-set count for all reduced graphs through 4 nodes:',count)
if __name__=='__main__':main()
''')
exec(compile(p.read_text(),str(p),'exec'))
Path('workspace/agent3_upper_proof.txt').write_text(r'''UPPER BOUND
Fix c>1/9. Choose 0<epsilon<eta, d>epsilon and epsilon<1/2 such that a=c-d-2epsilon-eta>1/9. Use the degree form of Szemeredi regularity: for n>=n0 there is a partition V0,V1,...,Vk, |V0|<=epsilon n, |Vi|=m, k<=M, and G' subset G with no edges inside Vi for i>0, every bulk pair epsilon-regular of density zero or at least d, and d_G'(v)>=d_G(v)-(d+epsilon)n for every vertex. Edges touching V0 may be retained. The reduced graph R consists of the positive-density bulk pairs. Set w(I)=m|I|/n. Each reduced vertex has neighborhood weight at least b=c-d-2epsilon: a vertex in its cluster has at least (c-d-epsilon)n G' neighbors, at most epsilon n in V0, and all remaining neighbors lie in reduced neighbor clusters.

For every v, its support s(v) comprises the clusters Vi with |N_G'(v) intersect Vi|>=eta m. At least an neighbors of v lie in its support, by deleting V0 (epsilon n), small pieces (eta n), and the degree-form loss ((d+epsilon)n). Thus w(s(v))>=a>0.

The following consequences of regularity are exact. A support is independent in R (an R-edge inside it would give a closed odd walk of length3 in G). For a G-edge xy, N_R(s(x)) and N_R(s(y)) are disjoint: a common reduced neighbor B of support clusters A,C supplies a bulk length4 walk between x,y, yielding a closed odd walk of length5. To see the walk exists, each endpoint neighborhood of size>=eta m has neighbors at all but epsilon m vertices of B, since its corresponding pair is epsilon-regular of density>=d>epsilon; these two sets intersect. In particular, supports of adjacent vertices are disjoint, since a common support cluster has a nonempty reduced neighborhood. For a G-length2 walk x-z-y, there is no R-edge between s(x),s(y): regularity supplies a bulk length3 walk between x,y, closing a length5 odd walk. Closed odd walks of length3 or5 cannot occur in a C3,C5-free graph, even with repeated vertices.

Let F have an edge between endpoints of each G-walk of length1 or3. It has no loops. For any F-edge xy, the actual neighborhoods N_G(x),N_G(y) are disjoint, since a common neighbor closes a length3 or5 odd walk. Therefore if w(S)<2a, the vertices with support S form an independent set in F.

Color each v by the ordered pair (s(v), {s(w):w adjacent to v in G}). This uses at most K=2^M 2^(2^M) colors. Suppose x,y have the same color and form an F-edge. They cannot form a G-edge because their equal nonempty supports would be disjoint. Thus choose a length3 walk x-p-q-y and let S=s(x)=s(y), T=s(p), U=s(q). Necessarily w(S)>=2a. If w(T)<2a, the matching neighbor-support profiles of x,y provide p' adjacent to y with s(p')=T. Then p-q-y-p' is a length3 walk, contradicting the F-independence of support T. Thus w(T)>=2a, and likewise w(U)>=2a. From the three actual edges x-p,p-q,q-y, the three reduced neighborhoods N_R(S),N_R(T),N_R(U) are pairwise disjoint; so are S,T,U. The walks x-p-q and p-q-y rule out reduced edges between S,U and T,S. As x and y have matching neighbor-support profiles, x has some neighbor q' of support U; then p-x-q' rules out reduced edges between T,U. Each support is itself independent, so S union T union U is independent in R. Consequently the six sets S,T,U,N_R(S),N_R(T),N_R(U) are pairwise disjoint. The first three each have weight>=2a; the last three each have weight>=b>=a, because each support is nonempty. Their total weight is at least 6a+3b>=9a>1, contradiction. This proves the coloring proper on F. Small graphs n<n0 have a proper F-coloring with n0 colors, so a uniform finite K works for every n.

Finally define U_K with vertices (i,A), i in [K], A subset [K] excluding i; join (i,A),(j,B) when i in B, j in A and A intersect B empty. A triangle is impossible: the first coordinate of any triangle vertex belongs to the second-coordinate sets of both other vertices, contradicting their adjacency. For a proper F-coloring t, put f(v)=(t(v),{t(w):w adjacent to v in G}). The latter set excludes t(v). If uv is a G-edge, each first coordinate belongs to the other neighbor-color set. The two neighbor-color sets are disjoint, since any equal-colored neighbors x of u and y of v are endpoints of the length3 walk x-u-v-y. Hence f is a homomorphism to the fixed finite triangle-free U_K. This completes the upper bound.
''')
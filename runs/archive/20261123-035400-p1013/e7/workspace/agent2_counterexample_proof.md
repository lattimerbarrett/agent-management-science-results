# Counterexample to the supplied answer: 1/3 belongs to S_2

Let H have vertex set {0,...,7} and edge set
04,06,07,16,17,26,27,34,35,47,57,67.
It has triangles and H-7 is the tree with path 6-0-4-3-5 and two additional leaves 1,2 at 6. Hence chi(H)=3.

Write F_a for a disjoint union of floor(a/3) copies of P3, together with one isolate if a=1 mod3, or a K2 if a=2 mod3. Define G(a,b)=F_a join I_b, and
f(n)=max_{0<=a<=n}[a(n-a)+floor(2a/3)].

## G(a,b) is H-free
If vertex7 of H mapped into the independent side, all its neighbors would map into F_a. But H[N_H(7)] contains the claw with center6 and leaves0,1,2, impossible since Delta(F_a)<=2.
If7 maps into F_a, at most two of its H-neighbors map there. These at most two vertices must form a vertex cover of H[N_H(7)], whose nontrivial edges are 04,06,16,26. The only covers of size at most2 are {6,0} and {6,4}. The first makes triangle7,6,0 inside F_a, impossible. Thus6,4 are the two F_a-neighbors of7, and 0,1,2,5 lie in I_b. Vertex3 is adjacent to5, so maps into F_a. It is adjacent to4, but4 is already a leaf in the P3 with center7 and other leaf6, contradiction. Thus ex(n,H)>=f(n).

## High-minimum-degree lemma
For every n>=10000, every H-free graph G with e(G)>=f(n) and delta(G)>=n/2-10 has e(G)<=f(n), and every equality graph is some complete-cross graph with one part independent and the other a disjoint union of P3, K2, and isolated vertices.

Proof (entirely elementary). Put T=H-7, a tree on seven vertices. Every neighborhood G[N(v)] is T-free, since v joined to T contains H. Every T-free graph is5-degenerate: a subgraph with minimum degree at least6 contains every tree on7 vertices by a greedy embedding. Consequently
 e(G[N(v)])<=5d(v).
Write a=d(v). Every vertex in N(v) has at least delta(G)-(n-a)>=a-n/2-10 neighbors in N(v). Therefore
 a(a-n/2-10)<=2e(G[N(v)])<=10a,
which implies a<=n/2+20 (the zero-degree case is irrelevant under the minimum-degree assumption).

Fix any v and let A=N(v), B=V(G)-A. Since a>=n/2-10 and e(G[A])<=5a,
 e(A,B)>=a delta(G)-2e(G[A])>=a(n/2-20)
 >=(n/2-10)(n/2-20)>=n^2/4-15n.
Now choose a maximum cut A,B. It therefore has at least n^2/4-15n cross edges. Its missing-cross count is at most15n, and each part differs from n/2 by less than4 sqrt(n). For a vertex x with internal degree s, maximum-cut optimality gives at least s opposite-part neighbors. The edges between these two sets are all in N(x), so
 s^2-15n <= e(G[N(x)]) <=5d(x)<=5n.
Thus every internal degree is less than5 sqrt(n). The minimum-degree assumption gives missing-cross degree at most10+9 sqrt(n), uniformly over vertices. Consequently any four fixed vertices in one part have at least
 n/2-40 sqrt(n)-40 >=960
common opposite-part neighbors when n>=10000.

The following explicit partitions of H show that any internal claw, P4, or triangle forces an H copy by choosing the remaining vertices in the common cross neighborhoods:
* claw: A_H={7,4,5,6}, B_H={0,1,2,3};
* P4: A_H={4,6,7,3}, B_H={0,1,2,5};
* triangle plus one isolate: A_H={0,6,7,3}, B_H={1,2,4,5}.
For the triangle case choose one additional vertex in the same host part first. Thus both internal graphs have maximum degree2 and have no triangle or P4; every component is P3, K2, or an isolate.

Since all vertices have internal degree at most2, delta>=n/2-10 gives ||A|-n/2|<=12, and every vertex misses at most24 cross neighbors. Since e>=f(n)>=t2(n)+n/3-2, some part, say A, has at least n/6-1>96 internal edges. If B has any internal edge, map H's vertices6,7 onto its endpoints. H has the defect coloring
A_H={0,4,1,2,5}, B_H={6,7,3},
with sole internal edges04 and67. Choose an internal A-edge for04 avoiding the at most48 forbidden neighbors of the fixed B-edge endpoints; possible because Delta(G[A])<=2 and excluding48 vertices removes at most96 internal edges. Choose1,2,5 in the large common cross neighborhood of6,7, then3 in the large common cross neighborhood of4,5. This embeds H. Consequently B has no internal edges.

It follows that e(G)<=|A||B|+floor(2|A|/3)<=f(n). Equality forces no missing cross edges and equality in the forest-component edge bound. QED.

## Removing the minimum-degree condition
For all n,
t2(n)+n/3-2 <= f(n) <= t2(n)+n/3+1,
so f(n)-f(n-1)>=n/2-4. Suppose e(G)>f(n) and n>=10^8. As long as the current order m>10000, the high-minimum-degree lemma supplies a vertex of degree less than m/2-10. Delete it. The integer defect e-f(m) increases by more than6 on every deletion. It remains positive, so the process cannot stop at order >=10000 with minimum degree >=m/2-10. At order10000, the defect is less than binom(10000,2)<5*10^7, whereas it has increased by more than6(n-10000)>5*10^8. Contradiction. Hence ex(n,H)=f(n) for every n>=10^8.

Moreover, every edge-extremal graph at such n has minimum degree at least f(n)-f(n-1)>=n/2-4 (delete one vertex and use the exact upper bound at n-1). The high-minimum-degree lemma therefore classifies all edge-extremal graphs.

For n=6k=2m, m=3k,
a(n-a)+floor(2a/3)=m^2+2m/3 + floor(2t/3)-t^2, t=a-m.
The final expression is uniquely maximized at t=0. Equality in the internal edge bound at a=m=0 mod3 forces every component to be P3. Thus every edge-extremal graph is isomorphic to G(m,m).

In particular ex(n,H)<=t2(n)+n/3+1 for all sufficiently large n.

## Exact cycle formula and strict comparison
Let q_b(a)=[x^b](1+9x+7x^2+x^3)^{floor(a/3)} R(x), where R=1,1+x,1+4x+x^2 for a mod3=0,1,2 respectively. This polynomial enumerates collections of vertex-disjoint oriented paths in F_a, with unused vertices allowed, by their number of path blocks. A nontrivial path has weight2 (its orientations), a singleton weight1.

A cycle meeting I_b uses k>=1 vertices there and k path-blocks in F_a. For k>=2 its count is
q_k(a) (b)_k (k-1)!/2.
For k=1 subtract the degenerate two-vertex walks, giving
c(G(a,b))=b(q_1(a)-a)/2 + sum_{k=2}^{min(a,b)} q_k(a)(b)_k(k-1)!/2.
This is verified against independent DFS cycle enumeration in the Python artifact.

Let m be a multiple of3 and normalize by L_m=m!(m-1)!/2. For fixed ell,
q_{a-ell}(a)=((7/3)a)^ell/ell!+O(a^{ell-1})
when a=m or m+1. Indeed the reversed P3 polynomial is1+7z+9z^2+z^3. Coefficientwise this is at most(1+3z)^3, hence
q_{a-ell}(a)<=binom(a,ell)3^ell.

For a=b=m the normalized k=m-ell summand is bounded by
(ell+1)3^ell/(ell!)^2,
and tends to (7/3)^ell/(ell!)^2.
For a=m+1,b=m-1 the normalized k=a-ell summand (ell>=2) is bounded by
(ell+1)3^ell/[ell!(ell-2)!],
and tends to (7/3)^ell/[ell!(ell-2)!]. Both majorants are summable. The k=1 term is polynomial in m and negligible compared to L_m. Thus dominated convergence gives
c(G(m,m))/L_m -> S0=sum_{j>=0}(7/3)^j/(j!)^2,
c(G(m+1,m-1))/L_m -> S1=sum_{j>=0}(7/3)^{j+2}/[j!(j+2)!].

These limits satisfy a rigorous rational strict inequality. The first three terms of S1 sum to21217/3888. The first three terms of S0, together with a geometric bound on its tail (the ratio after the next term is at most(7/3)/16), give S0<=67849/13284. Their difference is55709/159408>0. Thus S1>S0.

Therefore for all sufficiently large multiples n=6k, the H-free graph G(m+1,m-1) has strictly more cycles than every edge-extremal n-vertex graph G(m,m). This proves1/3 belongs to S2, contradicting the supplied answer S2=[1/2,infinity).

## Executable checks
`workspace/agent2_counterexample_checks.py` checks H's explicit residual partitions, enumerates all2^8 possible one-part assignments, performs literal GraphMatcher monomorphism checks on small hosts, verifies the exact cycle formula against independent DFS, checks f(n) arithmetic for n<=400, and proves the rational series inequality using Fraction. It prints exact cycle ratios for m=6,12,30,60,120; the last three exceed1.

## Thresholds
The preceding elementary proof gives the explicit edge bound and exact extremal value for every n>=10^8. For classification of all edge-extremal graphs use n>=10^8+1 so that the deletion upper bound at n-1 is available. Every local greedy inequality is already valid for n>=10000. The infinite cycle comparison follows from the stated exact rational limiting gap; it does not depend on an uncomputed assumption about small n.

# Direct edge-extremizer audit for the projection-rendered counterexample

This argument avoids BOTH Simonovits' exact decomposition theorem and the cycle-maximizer structural reduction. Its only graph stability input is ordinary Erdos--Simonovits stability.

Assume the rendered fixed graph H has chi(H)=4, a color-critical vertex, and the exact complete-tripartite bounded-internal-degree realization of the payloads
 K1,11; P12 disjoint union P11; FORK5; each C3,...,C22; one internal edge in each of two distinct classes.
Here FORK5 is the tree with arm lengths 2,1,1. The renderer uses a cell size h>30, so ANY 3-coloring of H with maximum monochromatic degree <=10 is a coordinate projection on the core; the extra root excludes the proper coordinate, leaving precisely the payload tests.

Let G be ANY edge-extremal H-free graph on sufficiently many n vertices. The balanced complete tripartite graph is H-free, so e(G)>=t_3(n). Ordinary stability gives three classes of size n/3+o(n) with o(n^2) internal edges and missing cross-edges. The color-critical-vertex greedy embedding argument allows reassignment of o(n) exceptional vertices so that maximum internal degree is eta*n=o(n), while total missing cross-edges M=o(n^2).

Choose tau->0 with eta=o(tau), M/n^2=o(tau^2), and let B contain vertices with at least tau*n missing cross-neighbors. Then b=|B|<=2M/(tau*n)=o(tau*n). Delete all internal edges incident with B and fill all cross-edges incident with B, obtaining G*. This remains H-free: any new H-copy replaces every new ordinary vertex by a fresh old good vertex in the same class; all required same-class edges incident with new vertices are absent, and every required cross-edge can be secured greedily since good vertices miss only tau*n=o(n) cross-neighbors. The operation gains at least (1-o(1))*tau*n*b missing cross-edges and loses at most eta*n*b+b^2=o(tau*n*b) internal edges. Edge extremality forces B empty. Thus G has maximum missing cross-degree o(n).

Now every SINGLE-CLASS payload can be tested directly by greedy completion: choose its vertices in one class and fill all remaining H-vertices in their prescribed classes, avoiding at most |H|*o(n) nonneighbors. Hence every internal graph avoids K1,11, FORK5, C3,...,C22, and P12 disjoint union P11. Every longer cycle contains the last forest on 23 vertices, so the internal graphs are forests. A tree which is neither a path nor a star contains FORK5: choose a degree>=3 vertex adjacent to a nonleaf. Consequently EVERY internal component is a star on at most 11 vertices or a path on at most 22 vertices.

G is H-saturated by edge maximality. There are finitely many internal component types. Any type occurring linearly many times is cross-complete to EVERY vertex: otherwise add a missing cross-edge incident with one copy; in the created H-copy replace its selected component vertices by a fresh identical component avoiding the o(n) prohibited cross-nonneighbors. This would yield H already in G. Each class therefore has an unlimited reservoir of vertices cross-complete to every other class.

For any internal component C, delete its at most 21 internal edges and fill all its missing cross-edges. This operation is H-free: vertices of the newly independent C can be replaced by fresh reservoir vertices from different components of the same class in any alleged new H-copy. Edge extremality forces C to have at most 21 missing cross-edges. The fresh-copy saturation argument now shows that every type with more than 21|H|+|H| copies is cross-complete to all vertices. All rarer types together form a bounded set R.

The explicit candidate A below has positive linear surplus, so G contains linearly many internal edges. Since R is bounded, some class has a nontrivial repeated normal component; call it active. Its normal edge is cross-complete to all vertices. If either other class had ANY internal edge, the two-class matching payload would embed, using that edge and the active normal edge; all remaining H-vertices are filled from reservoirs. Thus the other two classes are independent.

At this point max internal degree<=10 and there is only one active class. Fill ALL remaining cross-nonedges. The resulting graph is still H-free: by renderer rigidity an H-copy would have to use a coordinate payload, but every single-class payload is absent by the established internal restrictions and the two-class payload is impossible. Hence G already had all cross-edges.

Write m for its active-class size. There can be at most one path component of order >=12; it has order at most 22, and if present every other path has order at most 10. All star components have order at most 11. For large m, the maximum internal edge count is exactly
 f(m)=m-ceil(m/11)+1.
Indeed a component of order<=22 together with all other components of order<=11 forces at least ceil((m-22)/11)+1=ceil(m/11)-1 components, and the bound is attained by one path of order 12,...,22 plus stars of order<=11.

For n=33q put m0=11q. If the three part sizes are m0+d,m0+a,m0+b, with d+a+b=0 and first class active, then relative to balanced classes the edge difference is
 -(d^2+a^2+b^2)/2+d-ceil(d/11).
It is strictly negative unless d=a=b=0: for d>=1 use ceil(d/11)>=1 and a^2+b^2>=d^2/2; for d<=-1 the internal difference d-ceil(d/11)<0 already. Thus the balanced partition is uniquely optimal.

For active size 11q, attaining f(11q)=10q+1 requires exactly q-1 components. One must have order 22 and all remaining q-2 components order 11. The order-22 component is P22; its presence forbids any other P11, so all remaining components are 11-vertex stars. Therefore EVERY edge extremizer is isomorphic to
 A_q=K_{11q,11q,11q} with internal P22 disjoint union (q-2)K1,10 in one class.
In particular ex(n,H)<=t_3(n)+(10/33)n+O(1), and ex(33q,H)=t_3(33q)+10q+1.

The rival B_q puts q copies of P11 in one balanced class. It is H-free by renderer rigidity, and has one fewer edge. The rigorous cycle comparison in agent3_countercycle_comparison.md gives
 33q*(c(B_q)/c(A_q)-1) ->21/11>0.
Thus for all sufficiently large q, NO edge-extremizer is a cycle maximizer. If the renderer is valid, this contradicts the requested exclusion for a=10/33<1/3.

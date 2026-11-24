# Cycle comparison for the W7 construction

Let H=K_1 join C_6. The following is conditional only on the standard exact odd-wheel extremal classification: for sufficiently large n=2m, ex(n,H)=m^2+m+1 and every extremal graph is complete bipartite between A,B, where (|A|,|B|) is (m,m) or (m+1,m-1), with a 2-regular P5-free graph in A and exactly one edge in B. (Thus the graph in A is a disjoint union of triangles and quadrilaterals.)

Set L_m=m!(m-1)!/2. Let M_m be K_{m,m} with perfect matchings inserted into both classes, for even m. M_m is H-free: for any vertex v, N(v) consists of the opposite matching plus one same-class vertex, whose induced graph has no C6. Indeed a C6 would have to visit the unique same-class vertex and then traverse a P5 in a matching.

For a graph J on a vertices, define q_J(b) as follows. Choose a subset U of V(J), then a spanning linear forest F in J[U]. Weight F by 2 to the number of its nontrivial path components, and count it if it has b components, including singleton components. For a complete-cross graph with internals J_A,J_B, cycles meeting both sides correspond to choosing such forests with a common number b of blocks, and cyclically alternating their blocks. For b>=2 their number is exactly q_A(b)q_B(b)b!(b-1)!/2. The b=1 formula also works after removing the configurations consisting of one singleton in each side. Add cycles wholly contained in a side. These exceptional contributions are O(n^O(1)) when the internal components have bounded size and therefore negligible compared with L_m.

Coefficient lemma: if J has a vertices, maximum degree at most a fixed D, and e(J)=da/2+O(1), then for every fixed l,
q_J(a-l)=((1+d)a)^l/l!+O(a^(l-1)).
To see this, the leading contributions use l mutually disjoint primitive operations, each either deleting a vertex (a choices) or inserting one oriented edge (2e(J) choices). Every overlap reduces the number of free choices by at least one power of a. Moreover
q_J(a-l)<=binom(a,l)(D+1)^l.
Orient every nontrivial path; assign each vertex which is absent or has an outgoing successor pointer to a deficit set of size l. Each such vertex has at most D+1 choices (absence or a neighbor). This encoding is injective.

For an edge-extremal graph write a=m+s,b=m-s with s in {0,1}. The coefficient lemma gives, with l=a-b_blocks fixed,
q_A(a-l)~(3m)^l/l!,
q_B(a-l)~m^(l-2s)/(l-2s)!,
and hence the normalized cycle contribution tends to 3^l/[l!(l-2s)!]. The coefficient bound above bounds each normalized summand by (l+1)9^l/[l!(l-2s)!], a summable sequence. Thus dominated convergence gives uniformly across all edge-extremal graphs
c(G)/L_m -> B_s := sum_{l>=2s} 3^l/[l!(l-2s)!].
Uniformity follows because the coefficient-lemma error constants depend only on D=2, not on the mix of C3/C4 components. Here B_0=I_0(2sqrt3), B_1=3I_2(2sqrt3).

For M_m, both internals are perfect matchings. The same argument, with d=1 on each side, yields
c(M_m)/L_m -> A:=sum_{l>=0}4^l/(l!)^2=I_0(4).

A>B_0 follows term by term. A>B_1 has a rational certificate. The script workspace/agent4_cycle_checks.py sums the first 17 terms of A and bounds the tail of B_1 geometrically, proving A-B_1>23/100 with exact fractions. Therefore for all sufficiently large even m, M_m has more cycles than every edge-extremal H-free graph, while e(M_m)=m^2+m is one fewer than ex(2m,H). This establishes the required nonintersection for infinitely many n, conditional on the exact wheel extremal theorem stated above.

The exact ex asymptotic is t_2(n)+n/2+O(1), so H witnesses every a>=1/2.

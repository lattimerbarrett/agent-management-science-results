# Cycle/edge lattice comparison in bounded-tree templates
For r>=3 put K=r/(r-2). Suppose one active Turan part carries bounded components, with internal edge density rho<1, and all other internal edges are O(1). Fix a repeated tree type maximizing the admissible edge/vertex ratio, and compare to a balanced template F using that same type. The active part can be chosen among largest balanced parts because forest-packing internal edge number increases by at most one when its size increases by one, whereas leaving balance costs at least one cross-edge.

Write Delta e=e(G)-e(F), delta for the increase in active-part size, and Q for the increase in sum of squared part deviations. The contraction/local-CLT expansion gives

n log(c(G)/c(F)) = r/((r-1)(r-2)) [2(r-2) Delta e - Q +4 rho delta]+o(1).

When delta<=0, Q>=0 makes the displayed bracket strictly negative if Delta e<=-1. When delta>=1, the minimum quadratic cost occurs by removing vertices only from other currently largest parts. Thus Q>=delta^2+delta>=4 delta-2, the last inequality being (delta-1)(delta-2)>=0 for integral delta. Consequently if Delta e<=-1 the bracket is at most

4(rho-1)delta+2-2(r-2)<0

for all r>=3 and rho<1. Therefore no strict edge loser can maximize cycles within such a template class.

The inequality is uniform if rho is bounded away from one. Since there are finitely many bounded tree types, and max rho<1, this is automatic. Boundedly many exceptional internal components contribute to the 1/n expansion only through their edge count: conflicts with the linear family have probability O(n^-2), as do choices of two edges in any fixed exceptional component.

At fixed maximum density below one, a connected component of maximum edge/vertex ratio is a tree, with a uniquely determined order k (ratio (k-1)/k). Thus any two possible repeated component types have the same vertex count and edge count. The type with the most favorable cycle correction can be chosen in F without changing edge extremality.

For r=2 and ex<t_2+n/3-Omega(n), the repeated tree has order at most2 (otherwise repeating a P3 subgraph produces a free host with slope>=1/3). Exact Bessel/Skellam coefficient inequalities in agent2_cycles.py show balanced parts and, for odd n, putting the matching in the larger part maximize the leading cycle term. Among templates with those part sizes, the first nonvanishing bounded-edit term is positive constant times number of internal edges/n. Thus an edge/cycle common optimizer exists.

WARNING: this proves the comparison ONCE the global bounded-tree-template reduction is available. It does not prove that reduction.

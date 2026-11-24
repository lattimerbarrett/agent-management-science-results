# Tensor-clique projectivity (complete proof)
Let r>=3 and k>=1, and let X have vertex set [r]^k, with x adjacent to y iff x_i != y_i for every i. Every proper r-coloring of X has the form sigma(x_i), for one coordinate i and one permutation sigma.

Write N=r^k and d=(r-1)^k. The adjacency matrix is (J_r-I_r)^{tensor k}. Its eigenvalues are (-1)^s(r-1)^{k-s}, s=0,...,k, with multiplicity binom(k,s)(r-1)^s. Since r>2, its least eigenvalue tau=-(r-1)^{k-1} occurs only at s=1. Its eigenspace consists exactly of functions sum_i g_i(x_i), with sum_a g_i(a)=0.

For an independent set S of size alpha, let z=1_S-(alpha/N)1. Then z perpendicular to 1, ||z||^2=alpha-alpha^2/N, and
0=1_S^T A 1_S=d alpha^2/N+z^T A z >= d alpha^2/N+tau(alpha-alpha^2/N).
Rearranging gives alpha <= N(-tau)/(d-tau)=N/r. Equality implies z lies in the tau eigenspace.

A proper r-coloring partitions X into r independent sets. Therefore each color class has size N/r and its indicator has form f(x)=1/r+sum_i g_i(x_i). Such a binary-valued additive function depends on at most one coordinate. Indeed, if g_i and g_j were both nonconstant, fix all other coordinates and choose minima and maxima in these two coordinates. The four values would be a,a+u,a+v,a+u+v with u,v>0; all cannot belong to {0,1}, since the first and third/fourth strictly increase twice. Thus the class is determined by one coordinate. Having size N/r, it is precisely one coordinate fiber {x:x_i=c}. Fibers in different coordinates intersect, so all r disjoint color classes use the same coordinate. This proves the claim.

## Checked independently
`agent2_projectivity.py` enumerates every maximal independent set for (r,k)=(3,2),(3,3),(4,2),(5,2), and verifies that maximum sets are exactly the coordinate fibers. It also checks the exact spectrum formula and multiplicities.

## Robust finite blowup consequence (complete-cross hosts only)
Blow up each vertex of X to M twins. Suppose this graph is embedded into a complete-cross r-partite host with maximum internal degree D, where M>rD. In each base fiber choose a majority host-part color. Adjacent fibers cannot share majority color: otherwise every vertex of one majority subset would have at least M/r>D internal neighbors. Thus majority colors give a dictator coloring of X. An individual off-majority-colored vertex of a fiber p would have at least M/r internal neighbors in an adjacent fiber q of its own color: choose q_i to be that color and q_j != p_j for j != i. Therefore every fiber is monochromatic and the coloring is exactly a dictator.

This statement does NOT prove a global extremal-graph structure theorem: a general dense H-free host need not be complete-cross, and exceptional pockets remain uncontrolled.

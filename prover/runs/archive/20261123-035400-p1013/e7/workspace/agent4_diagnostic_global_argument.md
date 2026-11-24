# Audit of the diagnostic H: a contradiction to the requested threshold

H has vertex set {0,1,2,3,4,5,7,8} and edges
04,07,08,17,18,27,28,34,35,48,58,78.
H contains triangle 078 and H-8 is a tree, so chi(H)=3.
Explicit color patterns:
- independent B={0,1,2,3}, residual A={8,4,5,7} is K1,3;
- independent B={0,1,2,5}, residual A={4,7,8,3} is P4;
- independent B={1,2,4,5}, residual A={0,7,8,3} is K3 plus an isolate;
- A={7,8,3}, B={0,4,1,2,5} has precisely one edge in each part.
The direct H-freeness proof for any complete-cross graph whose first internal graph is a P3/P2/isolate union and whose second part is independent is supplied by agent_2; alternatively ALL 256 possible preimage partitions are checked in agent4_diagnostic_counter_checks.py.

Put f(n)=max_a[a(n-a)+floor(2a/3)]. Claim ex(n,H)=f(n) for all sufficiently large n; for n divisible 6, the only extremal graph up to isomorphism is K_{n/2,n/2} plus a P3-factor in one part.

Fix C=10 and consider H-free G with e>=f(n), delta>=n/2-C. Standard Erdos--Simonovits stability and a maximum-cross bipartition A,B imply balanced parts and o(n^2) missing cross edges. Since H is a subgraph of K1 join K_{8,8}, no vertex has linearly many neighbors in both parts: their cross graph would contain K_{8,8} inside its neighborhood. Maximum-cross then implies every internal degree=o(n). The minimum-degree hypothesis implies every vertex misses o(n) cross edges.

The explicit star pattern now forbids an internal K1,3: map its four vertices to the internal star and choose the remaining four vertices in their common opposite-part neighborhood. Similarly the P4 and triangle patterns forbid any internal P4 or triangle. Thus every internal component in either part is P3, P2 or an isolate, and in particular internal maximum degree<=2.

As in the W7 proof, minimum degree forces both part sizes n/2+O(C) and cross-missing degree O(C) at EVERY vertex. Since e>=f(n)=t2(n)+n/3+O(1), one part, say A, has linearly many internal edges. If B has any internal edge, choose an A-edge both of whose endpoints are adjacent to both B-edge endpoints; the constant cross-missing-degree bound guarantees such a choice. Map the fixed edges in the displayed two-edge pattern to these edges; choose the remaining vertices successively in common cross-neighborhoods, all of which have linear size. This embeds H, contradiction. Hence B is independent.

It follows e(G)<=ab+floor(2a/3)<=f(n). Equality implies no missing cross edges and the usual maximum-edge P3/P2/isolate packing in A. For n=6k the objective has its unique maximum at a=3k; equality in e_A<=2a/3 forces a P3-factor.

The minimum-degree condition is removed by EXACTLY the progressive-deletion argument proved for W7: f(m)-f(m-1)=m/2+O(1), so deleting a vertex of degree<m/2-C increases e-f by at least a fixed positive constant. A counterexample cannot stop above the high-minimum-degree threshold, and cannot delete down to a fixed order N if its initial order is arbitrarily large, since its growing defect would exceed binom(N,2). Thus ex(n,H)<=f(n) eventually; the P3-packing construction attains f(n), so equality holds. The same deletion upper bound gives delta(extremal)>=f(n)-f(n-1)>=n/2-O(1), proving the extremal classification.

The exact cycle calculation in agent4_diagnostic_counter_checks.py shows that for n=6k, the edge-extremal graph (balanced P3-factor template) has fewer cycles for all sufficiently large k than K_{3k+1,3k-1} with a P3-factor on 3k vertices plus one internal isolate in the larger class. The latter remains H-free. Normalizing by L_m=m!(m-1)!/2, m=3k, limits are respectively
S0=sum_{j>=0}z^j/(j!)^2,
S1=sum_{j>=0}z^(j+2)/(j!(j+2)!), z=7/3,
and the exact rational-tail certificate proves S1>S0.

Finally f(n)<=t2(n)+n/3+1, so this H witnesses a=1/3 in S2, contrary to the user-supplied S2=[1/2,infinity). Every step above needs careful independent audit before concluding the problem statement is inconsistent; all team agents presently see no gap.

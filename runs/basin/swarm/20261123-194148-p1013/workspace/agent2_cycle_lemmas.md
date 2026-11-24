# Verified cycle lemmas

Let h_m=m!(m-1)!/2 be the Hamilton-cycle count of K_{m,m}, and I_j(2x)=sum_{k>=0} x^{2k+j}/(k!(k+j)!).

For a graph made from K_{m,m} by adding bounded-size components in its first part, with rho*m+O(1) internal edges and maximum component size fixed,

 c(G)/h_m -> I_0(2 sqrt(1+2rho)).

Proof: Fix the number j of used internal edges. Configurations involving adjacent internal edges number O(m^{j-1}) and vanish after normalizing (a path of j edges contracts j vertices). Thus only j disjoint internal edges matter; there are (rho*m)^j/j!+O(m^{j-1}) choices. If s unused vertices remain on the first side after accounting for 2j endpoints, alternation forces s+j unused vertices on the second side. The normalized contribution tends (2rho)^j/(j!s!(s+j)!). Sum over s,j. With k=s+j the inner binomial identity yields sum_k (1+2rho)^k/(k!)^2. Uniform domination can be obtained from the exact component-polynomial formulas; factorial denominators control all tails.

With independent bounded-component additions of densities rho_A and rho_B in both parts, the analogous limit is I_0(2 sqrt((1+2rho_A)(1+2rho_B))). Indeed the normalized coefficient with d contracted/omitted vertices on each side is sum_{j,l<=d} (2rho_A)^j(2rho_B)^l/[j!l!(d-j)!(d-l)!].

For the universal join U=K_1 join K_{m-1,m},

 c(U)/h_m -> 2 I_0(2)+I_1(2).

Proof: cycles avoiding the universal vertex are negligible at this scale. Cycles using it correspond bijectively to unoriented alternating paths in K_{m-1,m}. Paths with even vertex count contribute 2 I_1(2); paths with odd vertex count contribute I_0(2)+I_2(2). Use I_0(2)-I_2(2)=I_1(2).

Consequently triangle or C4 packing in one part beats the universal join:

 I_0(2sqrt3)>2I_0(2)+I_1(2).

The difference series has kth term [3^k-2-1/(k+1)]/(k!)^2. The first three terms sum to 1/6, and all later terms are positive. Matchings in both parts beat it still more strongly, giving I_0(4).

For r>=3, balanced complete r-partite graphs satisfy the fixed contraction ratio h(T with D prescribed vertices deleted)/h(T)~[r/((r-1)n)]^D. This follows from the multivariate local central limit theorem for the irreducible aperiodic Markov chain on r colors that moves uniformly to a different color; its covariance is positive definite on the zero-sum subspace exactly when r>=3. Thus c(T)/h(T)->exp(r/(r-1)); a matching of n/(2r)+O(1) edges in one part multiplies c by exp(1/(r-1)); adding a universal vertex to T_{n-1,r} multiplies c by (r/(r-1))^2, NOT r/(r-1). This correction is essential: matching in ONE part does not beat the universal join. Triangle/C4 packing (density one in a single part) does beat it, since its multiplier exp(2/(r-1)) exceeds (1+1/(r-1))^2. The second factor arises because Hamilton paths in the core close to cycles with probability q=(r-1)/r. The old missing-q insertion argument was incorrect.

All exact finite counting formulas are in agent2_cycles.py and are checked there against exhaustive enumeration on small graphs. The asymptotic statements are mathematical derivations, not claimed proved by numerical evidence.

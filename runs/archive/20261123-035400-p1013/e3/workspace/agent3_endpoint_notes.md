# Endpoint construction and cycle lemmas (agent 3)

## Finite-template realization, r >= 3
A decoration pattern is an r-tuple of finite graphs, prescribing required edges inside the r parts; cross edges are all available. Suppose a finite list of forbidden patterns has all constituent graphs 3-colorable, and includes a one-part star. There exists an explicitly constructible graph H of chromatic number r+1, with a critical vertex, such that:
* H embeds in each sufficiently large complete r-partite graph decorated with one of the patterns.
* In a complete join of r graphs whose components have at most L vertices, H embeds only if one forbidden pattern occurs (up to a permutation of the parts).

Construction: put one disjoint soft copy of every constituent graph, with its vertices called ports. For every pattern i choose one port assignment rho_i: all edges of the selected pattern are monochromatic in their prescribed parts; every other soft graph is properly r-colored. Thus every rho_i has a monochromatic soft edge. With k patterns let D=K_r^{tensor k}, whose vertices are functions [k]->[r]. Replace each vertex by an independent hard cluster of size M>rL. Port p has reference vertex h_p=(rho_1(p),...,rho_k(p)). For each p take a private clique of r-1 additional hard clusters; make it complete to h_p's cluster and to p. Include the soft edges.

Every proper r-coloring of D is a coordinate projection followed by a color permutation. Proof: the eigenvalues are (r-1)^{k-j}(-1)^j; for r>=3 the least eigenvalue is -(r-1)^{k-1}, with eigenspace consisting of sums of one-coordinate mean-zero functions. Hoffman's bound gives alpha(D)<=r^{k-1}. Every color class of an r-coloring attains equality. Its indicator is a constant plus a sum of one-coordinate functions. A {0,1}-valued such sum can have at most one nonconstant summand (otherwise two independently varied coordinates yield at least three values). Hence every color class is a coordinate slice; slices on different coordinates intersect, so the whole coloring is one coordinate projection.

Consequently H is not r-colorable: the hard coloring chooses some rho_i, and each private clique forces its port's color to equal the reference color, leaving a monochromatic edge. It is (r+1)-colorable: color D with r colors, properly color every soft graph with r colors, and color each private (r-1)-clique from the r+1 colors avoiding the reference and port colors. There are at least r-1 such colors. If the selected pattern is a one-part star, deleting its center port allows the corresponding rho_i to be a proper r-coloring, so this center is critical.

For the embedding implication into a bounded-component host, choose a majority host part for each hard cluster. It contains >L vertices from that cluster. Adjacent hard clusters cannot have the same chosen part, since that would create a connected internal graph with >L vertices. Thus the chosen colors give a proper coloring of D. The private clique clusters use all colors except the reference color, and a port cannot lie in any of their majority parts (it would have >L neighbors in one internal component). Therefore its actual host part is forced to equal its reference's majority color, and a forbidden pattern occurs. Conversely the intended coordinate coloring supplies an embedding into the decorated host, using fresh vertices for all hard clusters and auxiliary ports. No component bound is needed for this forward embedding.

## Explicit hereditary endpoint class
Fix s>=3 and K>=2, and put L=Ks. S consists of star forests with at most one component of order>s, and that component of order<=L. P consists of linear forests with sum of the orders of components larger than s at most L-1. Let C=S union P. This is hereditary. It has the following finite forbidden family:
1. all trees on L+1 vertices;
2. all cycles of lengths 3,...,L+1;
3. all trees of order<=L which are neither stars nor paths;
4. claw disjoint-union P4;
5. two disjoint copies of K_{1,s};
6. all path forests with every component order at least s+1 and total order in [L,2L-1].
After 1,2 every component is a tree of order<=L. Item 3 makes each a star or a path, and 4 excludes a nonpath star and nonstar path coexisting. For star forests 5 is precisely the condition on the number of large components. For path forests 6 is precisely the total-large-order budget: take the shortest prefix exceeding L-1 to get total less than 2L.
Add the r-part pattern having one edge in each of two distinct parts. The realization construction therefore gives a fixed H whose sufficiently large complete-join free graphs have exactly one active part and decoration in C.

For large m, the maximum internal edge counts in these branches are
E_S(m)=m-1-ceil((m-L)/s),
E_P(m)=m-1-ceil((m-L+1)/s).
These follow by minimizing the number of tree components. A single maximal exceptional component minimizes that number; its subgraphs give all smaller cases needed to attain the formula.

For n divisible by rs, let m0=n/r=ks. At m0 the unique edge-optimal S-decoration is one star of order L and k-K stars of order s, with E0=k(s-1)+K-1. For a shift d in active-part size and optimally balanced other parts, write Q=sum x_i^2. We have Q/2>=|d|. The S edge difference is -Q/2+d-ceil(d/s), strictly negative if d!=0. The P difference is -Q/2+d-ceil((d+1)/s), always negative. Hence the complete-join edge optimum is unique up to isomorphism.

The competitor has active part m0+1, other part sizes m0-1,m0,...,m0, and decoration one P_{L-1}, k-K copies of P_s, and one P2. Its internal count is E0 and it loses exactly one total edge.

## First-order cycle comparison lemma
Let r>=3. Consider two sequences A_n,B_n, each a complete join of r internal graphs of uniformly bounded maximum degree. Part sizes are n/r+x_i with bounded x_i, internal edge counts E_i=alpha_i n/r+O(1), and internal wedges W_i=sum_v binom(d_i(v),2)=beta_i n/r+O(1). Suppose the alpha_i agree between sequences, and E(B)-E(A)=Delta E is constant. Then
n log(c(B)/c(A)) ->
  2r/(r-1) Delta E
 -r/(r-2) (sum (x_i^B)^2-sum (x_i^A)^2)
 +4r/((r-1)(r-2)) sum alpha_i(x_i^B-x_i^A)
 -2r/(r-1)^2 sum (beta_i^B-beta_i^A).

Derivation: enumerate omitted vertices and vertex-disjoint internal paths, orient each nontrivial path, and contract each to one vertex. What remains is a Hamilton cycle in a complete multipartite graph. The fixed-offset Hamilton count obeys
h(n_1,...,n_r)=B_n[1+(a_r-r/(r-2) sum x_i^2)/n+O(n^-2)],
B_n~(n-1)!/2 ((r-1)/r)^n (r/(r-2))^{(r-1)/2}.
This follows by Fourier inversion of the color-count distribution of the stationary Markov chain with transition probabilities 1/(r-1) off the diagonal. Its covariance on the sum-zero subspace is (r-2)/r^2 times the identity; Stirling's formula for prod n_i! changes the Gaussian coefficient to r/(r-2). The ordinary Edgeworth expansion gives the displayed uniform fixed-offset error. For k total contractions/omissions, its ratio is rho^-k n^-k times [1+{k(k+1)/2-kappa(Q'-Q)}/n+O(n^-2 poly(k))].
The leading omission sums are independent Poisson weights with means 1/(r-1) per part; the internal-edge sums have means 2 alpha_i/(r-1). Thus the Q'-Q term yields the stated imbalance cross term. For a graph with E edges and W wedges the generating polynomial of oriented linear forests has logarithm 2Ez-2(E+W)z^2+O(n z^3), with z=r/((r-1)n). Indeed a pair of disjoint edges has weight4, an adjacent pair weight2; all other first-order terms depend only on alpha_i, so cancel in the comparison. This yields the wedge term.
Uniformity of summation follows by restricting total omissions/contractions to O(log n), using the uniform Edgeworth expansion there, and bounding the remaining sum by a factorial tail; for counts >=epsilon n a crude cycle count loses a superexponential factorial factor. This also gives full fixed-order expansions to any order for bounded internal component orders.

For the constructed pair, alpha=(s-1)/s, Q_B-Q_A=2, Delta E=0, and wedge-density advantage is D=(s-2)(s-3)/(2s). The limiting comparison is
Delta(r,s)=-2r/(r-2)+4r(s-1)/(s(r-1)(r-2))+r(s-2)(s-3)/(s(r-1)^2).
In particular Delta(3,s)=3(s^2-5s-2)/(4s), Delta(4,s)=4(s-8)/9,
Delta(r,2r)=-(r-4)/((r-2)(r-1)),
Delta(r,2r+1)=6r/((r-2)(r-1)(2r+1)).
Thus s6 works for r3 and s=2r+1 works for r>=5.

For r4 take s8 and increase K. The first-order comparison is zero. In the second-order coefficient of log(c(P)/c(S)), the difference in wedges of the fixed exceptional gadgets has a positive quadratic K contribution. Specifically W_S-W_P=(s^2/2)K^2+O(K), and its coefficient is 2r^2/(r-1)^2. Every other K-dependent term is at most linear: the internal edge offsets are identical K-1, and bounded-gadget moments beyond wedges enter only at order n^-3. Therefore the second-order coefficient is [r^2 s^2/(r-1)^2]K^2+O(K), positive for some fixed K. Exact checks with K2 already show positivity for n128,256,512,1024, but that finite check is not the proof of eventual positivity.

## What this note does not supply
The global conversion of edge extremizers to complete-join form uses the Simonovits bounded-block theorem plus exceptional-vertex cleanup, discussed separately by agents1/4. The universal lower-threshold half additionally needs a corresponding global structure theorem for cycle maximizers, which is NOT proved by this note.

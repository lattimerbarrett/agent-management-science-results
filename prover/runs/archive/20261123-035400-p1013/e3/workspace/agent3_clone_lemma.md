# Uniform analytic clone lemma (r>=3)

Fix r>=3 and degree bounds D,B. There is a neighborhood U of u=(1/r,...,1/r) and positive analytic functions theta_i(p), w_ij(p), A(p), such that for any graph G with a partition V_i, p_i=|V_i|/n in U, maximum internal degree <=D, and maximum missing-cross degree <=B,

log c(G) = log h(K_{|V_1|,...,|V_r|}) + A(p)
 + sum_i 2 theta_i(p) E_i/n - sum_{i<j} w_ij(p) M_ij/n + O_{r,D,B}(1/n).    (1)

Here E_i counts internal edges and M_ij missing cross edges. The error is uniform over all such graphs. At u,
theta_i(u)=r/(r-1), w_ij(u)=2r/(r-1), A(u)=r/(r-1).

Proof details. Let Q(z) have entries sqrt(z_i z_j) off the diagonal and zero diagonal; its simple Perron eigenvalue lambda(z) is analytic near z=(1,...,1). On the hyperplane sum log z_i=0, the Hessian of log lambda is the positive definite covariance matrix of the non-looping r-state chain. At z=1 this covariance has eigenvalue (r-2)/r^2 on the sum-zero space. Thus the implicit-function theorem gives an analytic saddle z(p) for p near u. Perron spectral separation on the Fourier torus gives a uniform local central limit/Edgeworth expansion, by Taylor expansion at the saddle and exponentially small tails outside its neighborhood. Consequently
h(n_i)= C(p) n^{-1} n! exp(n Phi(p)) [1+O(1/n)]
with analytic C>0 and Phi, and full expansions with derivatives, uniform on a compact subset of U. On the simplex,
Phi(u)=log((r-1)/r),
D^2 Phi(u)|_{sumzero}= -2r/(r-2) I.
(The latter follows by adding Stirling's sum p_i log p_i to the Legendre transform of log lambda.)
The ratio obtained by deleting one fixed labeled vertex of part i is theta_i(p)/n [1+O(1/n)], where theta_i>0 is analytic. For any k fixed vertex deletions/contractions its ratio is the product of these factors, times 1+O(k^C/n), uniformly for k<=O(log n). The probability of a fixed cross edge ij in a uniformly random Hamilton cycle is w_ij(p)/n[1+O(1/n)], also analytic; w_ij=2q_ij/(p_i p_j), where q_ij is the stationary directed transition frequency in the saddlepoint Markov chain.

Now enumerate cycles by their omitted vertices and maximal internal paths, orienting each nonsingleton internal path, and exclude missing cross edges by inclusion-exclusion. For systems of k vertex-disjoint selected exceptional edges and omitted vertices, the Hamilton-cycle ratio is the product of the one-object factors times 1+O(k^C/n). Systems with overlaps have total weight O(1/n): bounded exceptional degree gives O(n) adjacent pairs, each of weight O(n^-2); a connected cluster of at least two selected edges has at most O(n) embeddings and weight O(n^-2) or smaller. Summing disjoint systems exponentiates:
A(p)=sum_i p_i theta_i(p),
internal contribution sum_i 2 theta_i E_i/n,
missing contribution -sum_{i<j} w_ij M_ij/n.
The sum of absolute exceptional activities is bounded in terms of D+B, so inclusion-exclusion cancellations do not spoil the uniform O(1/n) relative error (the limiting exponential is bounded away from zero). Tails beyond O(log n) are uniformly bounded by factorial tails. For a linear fraction of chosen edges/omissions, the elementary bound binom(n,p) binom(Cn,k) C^k (n-p-k)! relative to n! exp(-O(n)) is superexponentially small; intermediate tails use the saddle ratio bound C^{k+p} n^{-k-p}. This proves (1).

## Moving a vertex between parts
Let F be obtained from G by deleting v's incident edges and making it a pure independent-class clone in part j, whereas v belonged to part i in G. The new partition has n_i-1,n_j+1. Both graphs satisfy the same bounded internal/missing-cross degree conditions. All exceptional edge counts change by O(D+B), and p changes by O(1/n), so the analytic correction in (1) changes by O(1/n). Therefore

log(c(F)/c(G)) = log(h(new parts)/h(old parts)) + O(1/n).       (2)

By symmetry, partial_i Phi-partial_j Phi is divisible analytically by p_i-p_j. Its value divided by p_i-p_j tends to -2r/(r-2) as p->u. Hence shrinking U if necessary,

log(h(new parts)/h(old parts)) >= c_r (n_i-n_j)/n - C_r/n

whenever n_i is a largest and n_j a smallest part. Combining with (2), a cycle maximizer in this class has all part differences bounded by a constant depending only on r,D,B.

The clone operation is H-free whenever G is H-free and n is large: any new embedding must use v, which has no neighbors in its new part. Replace v by a fresh old vertex of part j adjacent to all the at most h(H)-1 required neighbors; at most (h(H)-1)B candidates are excluded by missing cross edges. This yields an embedding into G, contradiction.

Thus after the combinatorial repair lemma supplies bounded internal degree and bounded missing-cross degree, the part sizes are n/r+O_H(1), without assuming bounded imbalance in advance.

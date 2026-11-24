# Uniform near-balanced cycle estimate and O(1) imbalance, r>=3

Fix r>=3 and q=(r-1)/r, K=r/(r-2). Let n_i=n/r+delta_i with sum delta_i=0 and max|delta_i|=o(n). Start with the complete r-partite graph on these parts, add an internal graph of maximum degree at most a fixed D and M=O(n) edges, and delete at most a fixed L crossedges. Internal components may be assumed bounded (as in the finite-template application), although the estimate below only uses degree control and ignores negligible all-internal cycles. There is a quantity B_r(n), independent of the part deviations and internal graph, such that

 log c(G) = B_r(n) + 2M/(qn) - K*(sum delta_i^2)/n
             + O_{r,D,L}((1+||delta||)/n + ||delta||^3/n^2).       (U)

All norms in fixed dimension are equivalent. The constants are UNIFORM throughout any fixed sufficiently small neighborhood of uniform part proportions. In particular the statement is valid for every delta=o(n), not merely fixed delta.

## 1. A uniform, explicit saddle estimate for proper color words

Let A(t) have entries A(t)_{ij}=1_{i!=j} exp(t_j), with t_r=0. For real t near zero this is primitive and nonnegative (r>=3), with simple positive Perron eigenvalue lambda(t). Its logarithm and spectral projection are analytic. The generating function for proper CYCLIC color words of length n with a distinguished first position is tr(A(t)^n).

Let p=(n_1/n,...,n_{r-1}/n). At t=0, grad log lambda=(1/r,...,1/r). The Hessian is positive definite: in the full r-coordinate zero-sum space its covariance form is

 Sigma=(r-2)/r^2 * (I-J/r).

To see this directly, the proper-color Markov chain has transition 1/(r-1) off the diagonal. Its nontrivial eigenvalue is rho=-1/(r-1). The one-time covariance is (I-J/r)/r, and summing lag correlations multiplies this by (1+rho)/(1-rho)=(r-2)/r. Thus the implicit-function theorem gives a unique analytic saddle t=t(p) near zero.

We give the needed UNIFORM coefficient estimate rather than invoke a local CLT. Fourier coefficient inversion on the torus, with the contour tilted to exp(t), gives

 a(n_1,...,n_r) = (2pi n)^(-(r-1)/2) det(H_t)^(-1/2)
                 *lambda(t)^n exp(-sum_{i<r}t_i n_i)
                 *(1+O_r(n^-1)),                                (S)

uniformly for p in a fixed neighborhood, where H_t is the Hessian in the first r-1 coordinates.

Here are all analytic details needed for (S). Equality in the complex Perron modulus inequality away from the origin would require phases beta_i and phi satisfying theta_j=phi+beta_i-beta_j for EVERY i!=j. For r>=3, comparing two destinations using a third source gives theta_j+beta_j constant, hence theta_i=phi for every i. Since theta_r=0, all theta_i and phi vanish modulo 2pi. Thus zero is the UNIQUE maximum-modulus Fourier point. Compactness gives a uniform strict spectral gap outside a small ball, also for all sufficiently small real tilts. Inside the ball the simple eigenvalue is analytic and all others are uniformly smaller. Its logarithm expands as

 log lambda(t+i theta)=log lambda(t)+i p.theta -theta^T H_t theta/2
                      +i O(||theta||^3)+O(||theta||^4).

The cubic term is odd and imaginary and integrates to zero in the symmetric Gaussian neighborhood; the quartic and squared-cubic errors integrate to relative O(n^-1). All derivative bounds and positive Hessian bounds are uniform on a compact tilt neighborhood. Outside ||theta||<=n^(-2/5) the Gaussian/spectral-gap estimates are exponentially small. This proves (S), including its uniform error. The Perron projection has trace one, so no additional leading eigenvector factor occurs.

Let h(n_1,...,n_r) count Hamilton cycles in the complete multipartite graph. Labeling each color word gives

 h = a(n_1,...,n_r) product_i n_i! /(2n).

Apply uniform Stirling to the factorials and Taylor-expand the analytic saddle exponent about uniform proportions. The color-word quadratic term is

 -r^2/(2(r-2)n) *sum delta_i^2,

whereas the factorial quadratic term is +r/(2n)*sum delta_i^2. Their sum is -K sum delta_i^2/n. Every cubic remainder is O(||delta||^3/n^2), the analytic prefactor changes by O(||delta||/n), and the Stirling/saddle errors are O(n^-1). Hence

 log h(n_1,...,n_r)=B_r^H(n)-K sum delta_i^2/n
                    +O((1+||delta||)/n+||delta||^3/n^2).          (H)

For nonintegral n/r, B_r^H(n) can simply be defined using the analytic uniform-proportion expression with Gamma(n/r+1); the actual balanced integer deviation is O(1), absorbed in the error.

## 2. Bounded-degree internal edges

Choose internal edges used by a cycle. Unless the whole cycle is internal (negligible on the factorial scale), they form a linear forest. Contract its j edges and give each nontrivial path its two orientations. For j=O(log n), taking ratios in the UNIFORM saddle estimate yields

 h(n_1-j_1,...,n_r-j_r)/h(n_1,...,n_r)
 =(qn)^(-j) [1+O_r((j+j^2+j||delta||)/n)
                       *exp(O_r((j^2+j||delta||)/n))].            (C)

The bound is uniform over all nonnegative j_i summing to j. It follows either by differentiating the analytic exponent/prefactor in (S) or by Taylor expansion of (H) before coarsening its remainder; one must use the analytic saddle formula here, not subtract two unrelated O(||delta||^3/n^2) errors.

For M internal edges and maximum degree D, the weighted j-edge linear-forest count satisfies

 S_j=2^j binom(M,j)+O_D(C_D^j n^(j-1)/(j-2)!),

uniformly, by excluding adjacent selected pairs (at most O_D(n)) and summing their possible completions. Summing (C) against S_j therefore gives the internal factor

 exp(2M/(qn)) * [1+O_{r,D}((1+||delta||)/n)].

All moments of the effective bounded Poisson parameter 2M/(qn) are uniformly bounded, so the j-polynomial errors in (C) sum to the stated bound. Replacing binomial(M,j) by M^j/j! costs O_D(n^-1) after summing.

The uniform joint omission/contraction factorial tail is proved below using the ORIGINAL fixed tilt. It justifies truncating j at log n, without any estimate depending on the part proportions after omissions.

## 3. Omitted vertices and finitely many holes

Sum over omitted-vertex counts d_i. The same tilted saddle shows that choosing d_i omitted vertices and taking the smaller Hamilton kernel has, for bounded d_i, a product factor

 product_i a_i(p)^(d_i)/d_i! *[1+O((D_0+D_0^2)/n)],

where D_0=sum d_i and the a_i(p) are positive analytic functions of the part proportions; at uniform p every a_i=1/(r-1). The bounded-degree internal edge count changes by O_D(D_0), which adds only O_D(D_0/n) to its factor. Thus all cycles multiply the Hamilton/internal expression by

 exp(sum_i a_i(p)) *[1+O_{r,D}(n^-1)].

The logarithm of this analytic factor differs from its uniform value by O(||delta||/n), giving no additional quadratic Q/n term. Its uniform-proportion value can be absorbed in B_r(n).

Here is a single genuinely UNIFORM joint tail bound, including when omissions make the induced part proportions highly unbalanced. Keep the original tilt t=t(p), and put rho_i=exp(t_i)/lambda(t). Nonnegative coefficient extraction gives the upper bound

 W(n-b-j, a-b-j) <= r*lambda(t)^(n-b-j)*exp(-t.(a-b-j)),

where W is the rooted proper-word coefficient, b=sum b_i counts omitted vertices and j=sum j_i internal contracted edges. The denominator W(n,a) is bounded below by a constant times n^(-(r-1)/2)*lambda(t)^n*exp(-t.a), by (S). After choosing omissions, the exact factorial-label ratio is

 product_i 1/[b_i!*(a_i-b_i)_{j_i}].

In an induced part of size a_i-b_i, the weighted j_i-edge linear-forest count is at most [D*(a_i-b_i)]^j_i/j_i!, since there are at most D*(a_i-b_i)/2 edges and orientation weight is at most 2^j_i. For every A>=j, the descending factorial satisfies (A)_j >=(A/e)^j: the geometric mean of the top j factors is at least that of A!, which is at least A/e. Thus the complete joint contribution divided by the original Hamilton kernel is at most

 n^C * product_i [rho_i^b_i/b_i!]*[(D*e*rho_i)^j_i/j_i!].

The polynomial includes rooting-length ratios (at most n) and harmless exceptional contracted words of length two. All-internal cycles have only bounded length in the bounded-component application, and are negligible on the Hamilton scale. The rho_i stay in a fixed compact positive interval, so the sum where b or j exceeds log n is superpolynomially small. This establishes the uniform joint tail, permits every preceding termwise saddle expansion, and needs no balancing assumption on induced subsets.

Finally deleting at most L crossedges changes c by a factor 1+O_{r,D,L}(n^-1). One can use the elementary two-Pósa edge-usage upper bound in the fully cross-regular regime; equivalently expose the finitely many selected internal paths and use within-part symmetry for ordinary endpoints, with the probability a specified vertex is an internal-path endpoint O_D(n^-1). A prescribed crossedge is then used with probability O_r(n^-1), uniformly near balanced proportions. This proves (U).

## 4. Consequence: cycle-extremal templates have O(1) imbalance

Suppose the preceding structural reduction gives one active part, internal components of order at most k except a fixed rare context, and abundant admissible copies of a k-vertex tree T. Put rho=(k-1)/k. Then M<=rho*n_active+O_H(1).

There is an H-free competitor in the SAME finite context with balanced parts: keep the rare context, replace the active forest by disjoint copies of T and one connected subtree of any required leftover size (every tree has a connected subtree of every smaller order). Thus its edge count is >=rho*n_active,balanced-O_H(1). It is H-free by the abundance remapping argument: any new H-copy uses at most |H| components of each abundant type and remaps them to fresh old copies; rare vertices and their holes stay fixed.

Apply (U) to the original graph and this competitor. The ORIGINAL minus COMPETITOR internal-edge term is at most O_H((1+||delta||)/n), using M<=rho*n_active+O_H(1) and M_bal>=rho*n_active,balanced-O_H(1). This is a ONE-SIDED bound, which is all maximality needs; absolute control would require the already-repacked efficient forest. Since delta=o(n), the cubic remainder is o(sum delta_i^2/n) whenever ||delta|| tends to infinity. Cycle extremality therefore implies

 sum delta_i^2 <= C_H(1+||delta||)+o(sum delta_i^2),

forcing ||delta||=O_H(1). This proves the missing bounded-imbalance step without extrapolating the fixed-deviation first-order formula.

## Executed checks
workspace/agent3_uniform_imbalance_checks.py checks the exact covariance/factorial quadratic coefficient -r/(r-2) for r3..20. An exact integer Hamilton color-word DP verifies balancing improves the count for r3,m4,8,16 and r4,m4,8; n log(h_shift/h_bal) approaches the independently derived limits -6 and -4. These checks support, but do not replace, the uniform saddle proof.

# Uniform cycle expansion for the canonical hosts (proof block)
Throughout r>=3. Put D=r/(r-1), A=r/(r-2). Let n_i=n/r+s_i, sum s_i=0, min n_i=Theta(n). Start with complete r-partite graph; add an internal graph of bounded maximum degree in class1, together with O(1) internal edges in the other classes, and delete O(1) cross-edges. All constants are fixed. Write E for total added internal edges MINUS deleted cross-edges, W=sum_v binom(d_F(v),2) for the class1 internal graph. Suppose E=rho*n_1+delta, delta=O(1), rho fixed. Bounded exceptional cycles or exceptional components are harmless in the statements below.

Define lambda=2rho/(r-1),
 L_r(lambda)=lambda*(1/2-2D-A/2)-A*lambda^2/2.
There is K_{r,n}, depending only on r,n, such that for bounded offsets,
 log c(G)=log K_{r,n}+lambda + (1/n)*{
 -A sum_i s_i^2 + [2*r^2*rho/((r-1)*(r-2))]s_1 +2D*delta
 +L_r(lambda)-2D^2*W/n }+o(1/n).
The o(1/n) is uniform over all bounded-degree internal graphs, with bounded offsets and bounded exceptional data.
Equivalently, except for terms depending only on r,n,rho, the normalized cycle objective is
 Q=-1/2 sum s_i^2 +[r/(r-1)]rho*s_1+[(r-2)/(r-1)]delta
   -[r*(r-2)/(r-1)^2]W/n.

For s_i=o(n), the weaker UNIFORM moderate-deviation form is
 log c(G)=log K_{r,n}+2D*E/n-A sum s_i^2/n
  +O((1+max|s|)/n+sum|s_i|^3/n^2),
provided E=O(n). This is enough for balancing: in a finite regime E<=rho*(n/r+s_1)+O(1), and a bounded-offset feasible host in the same regime has logcycles>=logK+2rho/(r-1)-O(1/n). Since s=o(n), the cubic remainder is absorbed in half the negative quadratic term; maximality forces sum s_i^2=O(max|s_i|+1), hence s_i=O(1).

## A. Cross-cycle saddle, including its justification
The number of Hamilton cycles in a complete multipartite graph is
 (prod_i n_i!)/(2n) * [z_1^{n_1}...z_r^{n_r}] tr M(z)^n,
where M(z)_{ij}=z_j for i!=j and0 for i=j. Its Perron eigenvalue solves
 sum_i z_i/(lambda+z_i)=1.
Set lambda=1 and y_i=z_i/(1+z_i). Then sum y_i=1 and the saddle proportions are
 p_i=y_i(1-y_i)/sum_j y_j(1-y_j).
The map y->p is analytically invertible near uniform p, since its contrast derivative is(r-2)/(r-1). The other eigenvalues have modulus strictly less than the Perron root, uniformly near this point (r>=3). Fourier coefficient extraction, on a fixed complex neighborhood of this positive saddle, therefore gives the usual Gaussian saddle expansion with analytic coefficients, uniformly for p in a fixed neighborhood of uniform. This can be proved directly as follows: split the torus into a small neighborhood of its diagonal phase, on whose complement the spectral radius is smaller by a fixed factor; on that neighborhood Taylor-expand loglambda through the needed even order and rescale theta=x/sqrt(n); truncate at |x|<=n^epsilon, bound the remaining Gaussian tail, and integrate each Taylor monomial by Gaussian moments. The covariance on contrast coordinates is positive definite; at uniform it is(r-2)/r^2 times identity on the contrast subspace. All Taylor remainders and their derivatives are uniformly bounded on a smaller compact neighborhood. Thus any prescribed fixed-order expansion, with an error bounded by a polynomial in bounded/lower-logarithmic offsets times the next inverse power of n, follows. There are no hidden non-Gaussian saddle points because M(e^{it}z) has Perron modulus only when all t_i are equal: equality in the triangle inequality on every proper walk, including2- and3-cycles, forces all phases equal when r>=3.

Combining the saddle Gaussian with Stirling yields, for bounded s,
 log h(parts)=log K^H_{r,n}-A sum s_i^2/n+O(n^-2),
 K^H_{r,n}=C_r Gamma(n)((r-1)/r)^n(1+O(1/n)).
Deleting l_i vertices and summing binomial(n_i,l_i)h(n_i-l_i) shows the total cross-cycle count is h(parts)*[exp(sum_i z_i)+O(1/n)], uniformly near balanced p; all omitted-vertex tails are factorially bounded. In particular K_{r,n}=C'_r Gamma(n)((r-1)/r)^n(1+O(1/n)), and the same imbalance Hessian holds. Also the probability that a specified class1 vertex is omitted from a cross cycle is D/n+O(n^-2).

Consequently, if e bounded class1 contractions and p mandatory distinguished vertices are imposed, the ratio to K_{r,n} is
 (D/n)^e * [1+P_1(e,p)/n+O(n^-2)],
 P_1(e,p)= -A sum s_i^2 +2A e*s_1 +(1/2-D)e -(A/2)e^2
when p=e; in general replace -De by -Dp. This follows by applying the cross saddle to n-e and offsets s'_i=s_i-e(1_{i=1}-1/r), then inclusion-exclusion on the p mandatory vertices. More explicitly the unrestricted first coefficient is e(e+1)/2-A sum(s'_i)^2, and mandatory inclusion subtracts pD.

## B. Internal linear-forest contraction and summation
For any selected internal linear forest with e edges and p nontrivial path components, contract each selected path; its two directions give weight2^p, and its p contracted vertices must be in the cross cycle. This is an EXACT enumeration, apart from entirely internal cycles, whose number is exponentially negligible under bounded degree compared to the factorial lower bound. Subsets with a cyclic component and additional edges cannot occur in a simple cycle using cross-edges. Bounded internal edges in other parts are handled identically, with their own contractions; since there are O(1), all their interactions affect only O(n^-2).

Put R=D/n. The weighted selected-forest polynomial at leading order has logarithm
 2R*m -2R^2*m -2R^2*W +O(n^-2)
for class1 internal edge count m. The -2R^2*m term is the no-repeat correction from choosing each edge0or1 times. A pair of disjoint internal edges has orientation weight4, whereas an adjacent pair has weight2, giving -2R^2*W. Connected edge clusters of size>=3 have total countO(n) under the bounded-degree hypothesis and weightO(n^-3), hence O(n^-2). The same fact follows by direct inclusion-exclusion of edge subsets or expanding the logarithm of the finite-range polymer generating polynomial.

The leading selected edge count is Poisson(lambda), and leading path-component count equals edge count. Thus E[e]=lambda, E[e^2]=lambda^2+lambda. Taking the expectation of P_1, then adding the no-repeat correction -D*lambda and the adjacent-pair term, gives exactly L_r(lambda) and the displayed expansion. Bounded deleted cross-edges are incorporated by inclusion-exclusion: each costs2D/n+O(n^-2), the same leading weight as an internal edge. Hence E is the NET edge addition, including all exceptional edges and holes.

## C. Uniform summation/tail control
One need not assume selected e is literally bounded. Truncate at T=C logn/loglogn. Apply the positive coefficient bound to the FINITE word polynomial tr M(z)^N at the cross saddle (not directly to the divergent logarithmic cycle EGF). Equivalently evaluate that EGF at (1-1/n)z, costing only a polynomial/logarithmic factor. This gives contraction ratios at most n^{O(1)}(C_0/n)^e, uniformly0<=e<=n_1. Indeed word coefficients are bounded by their positive saddle evaluations, the denominator has its Gaussian lower bound, and (n_1-e)!/n_1!<=(euler/n_1)^e. Summing omitted vertices adds only a constant exponential factor because their counts have factorial denominators. There are at most binom(O(n),e) edge subsets and at most2^e orientations, so the tail is bounded by n^{O(1)} sum_{e>T} C_1^e/e!, which is O(n^-M) for any prescribed M after enlarging C. On e<=T the uniform saddle expansion error is polynomial in T times the next inverse power of n; this is o(n^-1), or o(n^-2) for the second-order calculation. This justifies all Poisson summations and all displayed little-o errors, uniformly over bounded-degree internal graphs.

## D. Complete r4 second-order calculation
See agent4_second_order_derivation.md plus the exact SymPy programs agent4_edgeworth.py, agent4_second_order.py. Those implement the same Fourier-Gaussian expansion through degree4 and the contraction expansion through the cubic component polynomial. For the prescribed star/path hosts the exact relative second coefficient is760/27>0.

# Uniform prescribed-endpoint path systems, r >= 3

Let fixed r>=3, K,B>0. Let N=sum n_i, |n_i-N/r|<=B sqrt(N log N), and 1<=k<=K log N. Fix k ordered endpoint pairs, with 2k distinct labeled core vertices, and let t_i be endpoint multiplicities by class. In complete r-partite graph with n_i labeled vertices, let W(n; endpoints) count ordered oriented vertex-disjoint paths connecting those pairs, covering every core vertex, with each path containing >=2 vertices. Then there is a positive common W_0(n,k), independent of endpoint colors, such that W/W_0=1+O_{r,K,B}(log^6 N/sqrt N). This is the aperiodic r>=3 lemma. Below is a self-contained proof route using the elementary iid local limit theorem; no general multivariate singularity theorem is needed.

Exact generating function. Let x=(x_1,...,x_r), D=1-sum x_i/(1+x_i). For endpoint colors a,b, the ordinary generating function for the internal color word is
 F_ab(x) = 1/((1+x_a)(1+x_b)D) - 1[a=b]/(1+x_a).
This follows by summing B+BXB+BXBXB+..., B=J-I, X=diag(x), and Sherman-Morrison. Consequently
 W=prod_i(n_i-t_i)! [x^(n-t)] prod_(a,b) F_ab.

Put Q=prod_i(1+x_i)D=1-P, where
 P(x)=sum_{S subset [r], |S|>=2} (|S|-1)prod_{i in S}x_i.
All coefficients of P are positive. The support vectors 1_S affinely span R^r and have lattice span Z^r when r>=3 (pairs and triples suffice). At x_0=(1/(r-1),...,1/(r-1)), P(x_0)=1. For m=n+O(log N) there is a unique nearby positive x satisfying P(x)=1 and mu(x) parallel m, where Pr(Z=1_S)=(|S|-1)x^S and mu=EZ. This follows by the implicit function theorem: covariance Sigma=Cov(Z) is positive definite; restricting the logarithmic x coordinates to the hypersurface P=1 gives an invertible map to directions of mu. The chosen x differs from x_0 by O(sqrt(log N/N)).

Renewal coefficient estimate. Set l_0=|m|/E|Z| and a=mu^T Sigma^{-1}mu. Uniformly for 1<=q<=K log N,
 [x^m] Q(x)^(-q)
 = x^(-m) l_0^(q-1-(r-1)/2)
   /((q-1)!(2pi)^((r-1)/2) sqrt(det(Sigma)*a))
   * (1+O(log^6 N/sqrt N)).
Moreover multiplication by g(x)=prod_i(1+x_i)^(b_i), |b_i|<=O(log N), multiplies the displayed main term by g(x), with the same error after increasing its constant.

Proof of estimate. Expand Q^(-q)=sum_{l>=0} binom(l+q-1,q-1) P^l. Tilting at x gives [x^m]P^l=x^(-m)Pr(Z_1+...+Z_l=m). Outside |l-l_0|<=sqrt(N)log N, Chernoff bounds give exp(-c log^2 N) tails. Inside this interval apply an ADDITIONAL exponential tilt theta_l with mean m/l; the tilt has norm O(log N/sqrt N). Central finite-support multivariate iid LLT at that mean has relative error O(N^(-1/2)); restoring the tilt and expanding its rate through quadratic order gives relative error O(log^3 N/sqrt N), uniformly even at the edges of the window. (A plain untilted additive LLT would not justify a relative error there.) Fourier inversion, cubic Taylor expansion on ||theta||<=log N/sqrt N, and exponential decay outside prove this central LLT. The resulting estimate is
 Pr(S_l=m)=(2pi l)^(-r/2)(det Sigma)^(-1/2)
 exp(-(l-l_0)^2 a/(2l_0))*(1+O(log^4 N/sqrt N)).
The binomial coefficient is l_0^(q-1)/(q-1)! times 1+O(log^3 N/sqrt N), uniformly in this window. Summing the one-dimensional Gaussian gives sqrt(2pi l_0/a), proving the formula. For analytic g, use the same Fourier inversion with integrand multiplied by g(x exp(i theta))/g(x). In the local window its logarithm is O(log N ||theta||), and hence it is 1+O(log^2 N/sqrt N). Outside, its magnitude is at most N^C since x_i<=3/4 eventually, whereas characteristic-function decay is exp(-c log^2 N). Chernoff tails similarly remain negligible. This proves the multiplied version. Details on the tails can equivalently be obtained by a radial Cauchy deformation; all possible poles of g lie at x_i=-1, a fixed distance beyond the positive saddle.

Application to endpoints. In prod F_ab, the main term is Q^(-k)prod_i(1+x_i)^(k-t_i). Every other term, with j endpoint-diagonal corrections, has pole order k-j; the renewal formula bounds its absolute relative contribution by O((k/N)^j) times a constant^j. Summing over choices of j gives O(k^2/N). The case k-j=0 is instead exponentially negligible by Cauchy bounds on any fixed torus of radius R between 1/(r-1) and 1: the remaining factor is analytic there, while the principal coefficient grows at rate (r-1)^N up to exp(O(log^2 N)) factors. For the leading term apply the coefficient estimate with m=n-t. Changing m by O(log N) multiplies the coefficient by x^t(1+o(1)), with a uniform error O(log^6 N/sqrt N), since the saddle changes O(log N/N). Finally
 prod_i(n_i-t_i)!/prod_i n_i! = prod_i n_i^(-t_i)*(1+O(k^2/N)).
The endpoint-dependent factor is therefore
 prod_i [x_i/((1+x_i)n_i)]^(t_i).
Each bracket equals (1/N)*(1+O(sqrt(log N/N))), so their product is N^(-2k)*(1+O(k sqrt(log N/N))). Everything else depends only on n and k. This proves the path-system lemma.

Caveat: to turn this into a global cycle-max theorem one must still write out the summation over omitted vertices, exceptional-exceptional adjacencies, and the finite-template first-order expansion. This file establishes only the path-system analytic component, not the user-requested construction.

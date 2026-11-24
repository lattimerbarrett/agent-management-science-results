# Cycle expansion for bounded internal components, r >= 3

Notation: q=(r-1)/r, K=r/(r-2). The part sizes are n_i=n/r+delta_i, sum delta_i=0, with fixed deviations (working on a residue class). In one distinguished part a insert a bounded-degree graph F with m=alpha*n+O(1) edges and bounded component order. Write w=sum_v binom(deg_F(v),2). There may also be a fixed finite collection of extra edge changes/cross-holes.

The following terms of log c(G) are the only terms depending on the internal SHAPE, part deviations, and fixed edge changes at order 1/n:

 log c(G) = common(n,m) - K*sum(delta_i^2)/n
            + 2*K*lambda*delta_a/n - 2*w/(q^2*n^2)
            + 2*(fixed net edge changes)/(q*n) + O(n^-2),
 lambda=2m/(q*n).

Here common(n,m) depends on the exact m and r but not the internal shape or fixed part deviations. Its leading internal term is lambda. Consequently, for two templates with the same limiting alpha,

 n*log(c(G)/c(F)) = (2/q)*Delta e - [r/((r-1)(r-2))]*Delta Q
                  + [4*r*rho/((r-1)(r-2))]*Delta delta_a
                  - 2*Delta w/(q^2*n) + o(1),

where rho=r*alpha and Delta e is the TOTAL edge difference after the Turan-part imbalance penalty; Q=sum delta_i^2. (Equivalently retain (2/q)*Delta m - K*Delta Q + 2*K*lambda*Delta delta_a.) This includes bounded cross-holes with their negative edge sign. WARNING: the wedge term does not cancel between different repeated component shapes.

## Hamilton-cycle contraction derivation

The proper cyclic color-word transfer matrix is A(z) with A_ij=z_j for i!=j and zero diagonal. Its Perron root is analytic at z=(1,...,1), equals r-1 there, and its stationary chain moves uniformly to a different color. The covariance on the zero-sum color-count subspace is (r-2)/r^2 times identity. Fourier expansion around the unique saddle (aperiodic because r>=3) gives

 h(T(n_1,...,n_r)) = [r/(r-2)]^((r-1)/2) * n!*q^n/(2n)
                    * exp(-K*sum(delta_i^2)/n)*(1+A_r/n+O(n^-2))

for fixed deviations; the constant A_r is immaterial, since it cancels in ratios. The usual analytic saddle expansion is uniform for deviations O(log n), with polynomial-logarithmic error in the displayed O(n^-2).

If j specified internal edges form a path forest with p nontrivial components, contracting its paths gives exactly 2^p*h(T(n_a-j, other n_i)) Hamilton cycles. For fixed j (and uniformly with the standard polynomial errors for j<=log n),

 R_j = h(T(n_a-j,...))/h(T(n_i))
     = (nq)^(-j) * [1+(j-K*j^2+4*K*delta_a*j)/(2n)+O(j^C/n^2)].

Indeed the factorial/prefactor ratio contributes j(j+1)/(2n); the changed imbalance contributes [2*K*delta_a*j-K*q*j^2]/n. Since 1/2-K*q=-K/2 this is the stated expression.

Among all j-edge subsets of F, the leading exceptional configurations are those with exactly one adjacent pair. There are
 w*binom(m-2,j-2)+O(C^j*n^(j-2)/(j-4)!)
such configurations; all other multiple-overlap configurations are lower order. A disjoint pair has four orientations while a two-edge path has two. Hence the total orientation-weighted number of path forests is

 S_j=2^j*binom(m,j)-2^(j-1)*w*binom(m-2,j-2)
     + O(C^j*n^(j-2)/(j-4)!).

Multiplying S_j by R_j and summing gives exp(lambda) and, from the adjacent-pair correction, precisely -2*w/(q^2*n^2) in its logarithm. The part-deviation correction is 2*K*lambda*delta_a/n. All other order-1/n terms depend only on m and r.

## Why the expansions can be summed

There is no unsupported interchange of an infinite sum here. Bregman's permanent inequality, Stirling's bound, and concavity of f(p)=p*log(1-p) give a uniform upper bound

 h(T(n_i-j_i))/h(T(n_i)) <= poly(n)*(C/n)^j*exp(O(j^2/n))

for contractions in a single part, 0<=j<=n/r. The bound follows because sum_i p_i*log(1-p_i)<=log q for any r-part proportions. Also S_j<=2^j*binom(m,j)<=(2m)^j/j!. As j^2/n<=j/r, all j>log n contribute less than n^-A for any fixed A, after increasing n. Thus one can expand only j<=log n and sum the polynomial-error terms against a Poisson factorial majorant.

For all cycles, sum over omitted vertex sets. Any s-vertex induced subgraph has at most t_r(s)+D*s/2 edges, where D bounds the internal degree. Bregman plus the uniform factorial-root envelope gives c(G[S])<=poly(s)*(q*s/e)^s. Dividing the resulting choose(n,d) bound by the Hamilton-cycle baseline gives omission tail at most poly(n)*sum_{d>log n} q^-d/d!, again superpolynomially small. For fixed omissions the chosen internal-edge counts have first moments depending only on m and the omitted part counts; the wedge count changes by O(1). Therefore the wedge and delta-dependent coefficients above are unchanged when passing from Hamilton cycles to ALL cycles. The leading factor c/h tends exp(1/q).

A fixed cross-edge lies in (2/(qn)+O(n^-2)) of the cycles, by the same stationary cyclic-color calculation; a bounded number of cross-holes therefore contributes only its negative net edge count at order 1/n.

## Independent exact checks

agent2_r3_shape.py computes complete tripartite Hamilton color-word tables by integer DP, contracts every path forest in repeated stars/paths, and counts ALL cycles exactly. It is brute-force checked on small graphs. For k=6 and r=3, n*(c(path)/c(star)-1) rises from 0.93025 at n36 to 1.29119 at n144, consistent with the rigorously derived limit 1.5. These values are checks, not the proof of the asymptotic statement.

This lemma does not prove that arbitrary H-free cycle extremizers belong to these templates, nor does it prove that competing maximum-order component shapes are possible/impossible under a common H. Those remain separate structural questions.

# Extreme dual-root ordering lemma

Let nu be a positive measure on finitely many distinct real nodes, with at least d+1 nodes. Let f be its monic degree-d orthogonal polynomial. Let g be any monic degree-d polynomial with simple real roots c_1<...<c_d, none a node, and let h be the monic degree-d orthogonal polynomial for mu_i=nu_i f(lambda_i)^2/g(lambda_i)^2. Assume f also has no root at a node.

If the smallest roots a_1 of f and c_1 of g occupy the same open spectral gap and c_1<a_1, then the smallest root b_1 of h satisfies b_1<c_1. Analogously, if the largest roots a_d,c_d occupy the same spectral gap and c_d>a_d, then b_d>c_d.

Proof: The roots of h are the eigenvalues of compression of multiplication by x to polynomials of degree<d in L2(mu); equivalently the minimum and maximum of its Rayleigh quotient are b_1,b_d. Test with ell=g/(x-c_1). Then
  integral (x-c_1) ell(x)^2 dmu = integral f(x)^2/(x-c_1) dnu.
The right side is S(c_1), where S(t)=sum_i nu_i f(lambda_i)^2/(lambda_i-t). On the open gap containing a_1,c_1, S is strictly increasing. Orthogonality gives S(a_1)=integral f(x) [f(x)/(x-a_1)] dnu=0. Thus S(c_1)<0, so the test Rayleigh quotient is <c_1, hence b_1<c_1. The maximum-root proof is identical with the inequalities reversed. The nonstrict versions hold when c_1=a_1 or c_d=a_d.

Application to restart weights: let I(w)_i be proportional to 1/(Delta'(lambda_i)^2 w_i), and let f_k be the monic degree d=n-s-1 orthogonal polynomial for I(w_k). Exact reciprocal duality yields
  f_(k+2) = OP_d( I(w_k) f_k^2/f_(k+1)^2 ).
For d<=2, if each root eventually stays in a fixed spectral gap, the smallest root can switch from increasing to decreasing at most once; the largest can switch from decreasing to increasing at most once. Thus each root converges monotonically after finitely many exceptions and has finite total variation.

Under this eventual-gap hypothesis, normalized even weights converge. Indeed exact two-step ratios satisfy
 log(w_(k+2,i)/w_(k+2,l))-log(w_(k,i)/w_(k,l))
 =2 sum_j [log|lambda_i-t_(k+1,j)|-log|lambda_i-t_(k,j)|
          -log|lambda_l-t_(k+1,j)|+log|lambda_l-t_(k,j)|].
For nodes distinct from every limiting t_j, the right sides are absolutely summable, so their even weight ratios converge to finite positive limits. Any node equal to a limiting t_j must have weight tending to zero: at any cluster two-cycle, w_i p_i=f_i/Delta'_i (up to positive scale), whereas p_i q_i=H_infinity^2>0 on active nodes. Thus f_i=0 precludes an active node. Normalizing remaining weights proves their convergence. Eventual signs on surviving coordinates then follow from convergence of the two-step residual multiplier to +1.

IMPORTANT: This does not establish the eventual-gap hypothesis in general, nor reduction of an arbitrary larger-support orbit to d<=2. Those remain missing global steps.

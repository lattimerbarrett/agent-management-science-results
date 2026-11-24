# Exact differential/reflection structure (checked)

Let distinct spectral nodes be lambda_i and positive weights w_i. Let p be the
monic degree-s orthogonal polynomial, H=sum w_i p_i^2, and T(w)_i=w_i p_i^2/H.
On projective logweight coordinates u_i=log w_i, set X_ij=lambda_i^j, j<s,
K=X(X^T W X)^(-1)X^T. Differentiating orthogonality gives

    dp = -K diag(w p) du.

Therefore, modulo global scale,

    D(log T) = I - 2 diag(1/p) K diag(w p) = I-2P,
    P^2=P, rank(P)=s, P 1=0.

Consequently D(log T) is a reflection, with determinant (-1)^s on projective
logweight space. T preserves absolute Lebesgue volume in logweight-ratio
coordinates wherever no p_i vanishes. This is an EXACT identity, not an
asymptotic statement.

For n=2s and a full-support stationary two-cycle with consecutive monic
polynomials p,q, Lyapunov equality gives p_i q_i=H on all nodes, equivalently
p q=chi+H. Write A,B for the two logarithmic differentials. Their +1
eigenspace is the SAME space

    E={du: sum_i w_i p_i lambda_i^j du_i=0, 0<=j<s}/constants,

of dimension s-1. (At the next weight vector w'_i=w_i p_i^2/H, the
orthogonality functional w'_i q_i is exactly w_i p_i.) Thus if N=BA-I,
N maps into E and vanishes on E, hence N^2=0.

The rank has a useful exact classification. The common -1 eigenspace of A,B
consists of vectors a_i/p_i=b_i/q_i modulo constants, with a,b degree<s.
This amounts to a q-b p=c H after using pq=chi+H. If gcd(p,q)=1, Bezout
with degree bounds gives a one-dimensional solution space (parameter c).
If gcd(p,q) has degree m>=1, c must be zero and a=t p/g,b=t q/g, deg t<m;
then that common -1 eigenspace has dimension m. Since the two rank-s
reflections have the same +1 space, the rank of BA-I is

    rank N = s - max(1,deg gcd(p,q)).

In particular for s=2 the only full-support rank-degenerate factorization
is p=q. A single shared root does NOT lower rank. For s=3 one needs at least
two common roots for rank degeneracy.

At maximal rank, the local fixed manifold has dimension s (one polynomial
level parameter H, plus s-1 linear weight parameters), and N is injective
on its normal quotient. Then the standard bounded-curvature lemma excludes
convergence of a nonstationary orbit to an interior regular fixed point:
with d_k=z_{k+1}-z_k, one has ||d_{k+1}-d_k||<=C||d_k||^2; if nonzero,
||d_k|| is bounded below by c/k. But unit directions change by at most
2C times arclength, so an infinite-length tail cannot stay in arbitrarily
small balls. Thus convergence implies eventual stationarity.

These facts alone DO NOT prove either global s=2 convergence or the s=3
counterexample. Endpoint scattering and rank-degenerate fixed cells remain.

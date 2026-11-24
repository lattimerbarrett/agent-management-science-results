# Fixed smooth geometric assembly (agent 1)

Let D>=2 and n>2D. Let h=P2 f(|x'|^2), P2=x1^2-x2^2, and f(0)=1,
with total polynomial degree D. This lemma only assembles geometry and
scales; the analytic gluing implication remains a separate theorem.

Start from the round unit hemisphere M0 in S^n. In a stereographic chart
near a boundary point p (not the stereographic pole), its boundary is a
plane z=0 and the hemisphere is z>=0. The ambient round metric is
Omega^2 delta. Choose an ambient smooth positive conformal factor equal
to Omega^(-(n-2)/2) on a smaller chart V, extended using a cutoff in its
logarithm. The resulting ambient g0 is exactly delta in V and globally
conformal to the round metric. Therefore g0|M0 has positive conformal
Robin quadratic form. In fact Q_g0(v)=Q_round(phi v), and multiplication
by phi is an H1 isomorphism, so Q_g0(v)>=a0||v||_H1^2 for some a0>0.

Choose q_i=2^(-i)e1, rho_i=2^(-i-4), mu_i=exp(-i^2),
lambda_i=exp(-i^4), and discard finitely many initial i. Their supports
B_(2rho_i)(q_i) are disjoint and lie in V. With a fixed smooth cutoff chi
one on B1 and zero outside B2, put

b_i(x')=mu_i lambda_i^D h((x'-q_i)/lambda_i) chi((x'-q_i)/rho_i),
b=sum_i b_i, b(0)=0.

For every derivative order k, polynomial differentiation and lambda<=rho
give ||D^k b_i||_infinity<=C_k mu_i rho_i^(D-k). On the support of b_i,
|x'| is comparable to 2^(-i). Thus for every k,N,
|D^k b_i(x')|/|x'|^N<=C exp(-i^2) 2^(i(k-D+N))->0.
All derivatives extend by zero at p; induction on k proves b is smooth
and has zero jet of every order at p. In addition ||b||_C2 tends to zero
when the initial retained index tends to infinity.

Take a vertical graph diffeomorphism, cut off in z, carrying M0 to a
smooth compact domain M_b with boundary z=b(x') in V and unchanged
elsewhere. This proves smoothness, compactness, connectedness and
nonempty boundary directly. Use the ambient metric g0 restricted to M_b.
It remains locally conformally flat everywhere, including the boundary,
since the ambient metric is conformal to the round metric.

Pull the domain back to M0. The volume/gradient forms depend continuously
in operator norm on b in C1, while the boundary Robin form depends
continuously on b in C2, by the graph formulas and the trace inequality.
Thus |Q_b(v)-Q_0(v)|<=C||b||_C2 ||v||_H1^2. For a sufficiently large
initial retained index, this is <=a0||v||_H1^2/2, and Q_b is coercive.
In particular the smallest Robin eigenvalue in the question is positive.

At q_i, b=Db=0 and D2b=2mu_i lambda_i^(D-2) diag(1,-1,0,...,0).
Since g0 is Euclidean there, the second fundamental form equals this
matrix (up to the irrelevant simultaneous choice of normal sign).
It has nonzero tracefree part. Under ghat=e^(2omega)g the covariant
tracefree second fundamental form is e^omega II_g^0. Therefore M_b,g0
cannot be conformally equivalent to the round hemisphere, whose boundary
is umbilic.

Finally set t_i=mu_i lambda_i^(D-1), R_i=rho_i/lambda_i,
s_i=mu_i rho_i^(D-1), and eta_i=(lambda_i/rho_i)^((n-2)/2).
Then s_i->0, R_i->infinity, and
log(eta_i/t_i)=-(n-2D)i^4/2+i^2+O(i)->-infinity.
Thus eta_i=o(t_i), exactly the cutoff-vs-shape condition used in the
proposed analytic gluing lemma. This assembly works for n19,D8 as well
as n>=21,D6; geometry alone cannot settle the sharp dimension issue.

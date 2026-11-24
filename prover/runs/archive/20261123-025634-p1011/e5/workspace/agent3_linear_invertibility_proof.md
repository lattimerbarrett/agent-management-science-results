# Halfspace Jacobi inverse lemma (proved)
Let a=(n-2)/2, U(x)=(1+|x|^2)^(-a), H={x_n>0}. Put
E(v,z)=integral_H grad v.grad z and
Q(v,z)=E(v,z)-n(n+2) integral_H U^(4/(n-2))vz.
On D^{1,2}(H), let K be the span of d_lambda U_lambda|lambda=1
and d_{x_j}U, j=1,...,n-1. Define T by E(Tv,z)=Q(v,z).
Then T preserves K-perpendicular and its restriction there is invertible,
with inverse norm exactly (n+4)/4 in the E norm.

Proof. Stereographic compactification has conformal factor
Omega=2/(1+|x|^2). Set v=Omega^a w. Conformal covariance/integration
by parts, first for compactly supported v and then by density, gives
 E(v,v)=integral_Splus (|grad w|^2+n(n-2)w^2/4),
 Q(v,v)=integral_Splus (|grad w|^2-nw^2).
The missing stereographic point has zero H^1 capacity since n>=3;
cutoffs on a ball of radius epsilon cost O(epsilon^(n-2)). Thus this
is an isometric isomorphism onto H^1 of the hemisphere with the
indicated energy norm (no Dirichlet condition at the boundary).

Reflect evenly across the equator. Restrictions of the reflection-even
spherical harmonics form a complete orthogonal basis, with eigenvalues
mu_k=k(k+n-1), k=0,1,... . Completeness follows from density of polynomial
restrictions and their harmonic decomposition. On degree k, T acts by
 rho_k=(mu_k-n)/(mu_k+n(n-2)/4).
Degree one contributes exactly the n equator-tangent coordinate functions;
these pull back to K. Degree zero has rho_0=-4/(n-2). For k=2+j, j>=0,
 rho_k-4/(n+4)=4jn(j+n+3)/[(n+4)(2j+n+2)(2j+n+4)]>=0.
Hence every nonzero eigenvalue has absolute value at least 4/(n+4).
The bound is attained in degree two. Inverting the diagonal expansion
proves the assertion, including exact inverse norm. QED.

Corollary. If a bounded bilinear perturbation changes T by operator norm
less than 2/(n+4), its projection on the transported kernel complement
is invertible with norm at most (n+4)/2 (Neumann series). This statement
alone does not handle global domain cutoff errors; those need estimates.

Code: agent3_linear_invertibility.py checks all symbolic spectral identities.

# All-dimensional s=3 convergence when the limiting monic polynomials have gcd degree2

This lemma uses the team's proved global reduction and bounded-variation tail estimate. Write the limiting even and odd monic cubics as q,r, put Q=qr, and H=lim h_k>0. Assume gcd(q,r)=c is monic of degree2. Its roots alpha1,alpha2 are distinct real roots, since each individual limiting cubic remains a degree3 orthogonal polynomial for a measure with positive monic norm H. Let D_k=H-h_k.

The global BV identity gives

    ||q_k-q_parity|| <= C D_k.

Let S be the set of ALL retained spectral nodes satisfying Q(lambda)=H, including nodes whose weights may tend to0. All omega-limit supports are subsets of S. If |S|<=4, its weights are uniquely determined by sum w=1 and the three orthogonality equations for q, so convergence is immediate. It remains to consider p=|S|=5 or6. Let P0=prod_{lambda in S}(z-lambda) and define the monic polynomial L by

    Q-H=P0 L,      deg L=6-p.

All initially retained nodes outside S with |Q(lambda)|<H decay exponentially and may be projected away; every smooth algebraic identity below then has exponentially small error. Such errors do not affect the estimates or the one-sided variation argument below. The remaining external nodes beta satisfy Q(beta)=-H. Their total mass eta_k is summable. None is a root of q or r, and none lies in a limiting Dirichlet gap. Put E(z)=prod_external(z-beta).

Let M_k/P0E be the Stieltjes transform of the retained weights. Perform polynomial division

    q_k M_k = a_k P0 E + t_k.

Here a_k is monic quadratic. The s=3 orthogonality relations give deg t_k=p+deg E-4 and leading coefficient h_k. Split its roots into the p-4 persistent Dirichlet roots and the external roots:

    t_k=h_k tau_k U_k,
    deg tau_k=p-4,  U_k=E+O(eta_k).

The estimate for U follows from smoothness of simple Stieltjes-remainder roots: setting an external weight to0 gives an exact factor z-beta, and its persistent Dirichlet roots remain uniformly separated from the beta's. All limiting measures have positive3-by3 moment Gram matrix, uniformly on the compact omega-limit set. Consequently the roots of a_k remain simple, and persistent roots match distinct roots of a_k. At limits,

    a=L tau,       M=r tau E.

The persistent tau roots lie in gaps not occupied by q or r roots; this follows from interlacing of M=r tau E with the core nodes and from qr=H on those nodes.

Define the quadratic normal polynomial

    N_k=H a_k-h_k L tau_k.

Its leading coefficient is D_k, up to the exponentially small projection error.

For either common root alpha of q,r one has M_k(alpha)=O(D_k+eta_k). Indeed on every core node,

    1/(alpha-lambda)=-q(lambda)[r(z)/(z-alpha)]_{z=lambda}/H.

The polynomial r(z)/(z-alpha) has degree2, so orthogonality of q_k and the BV tail bound show that the core Stieltjes transform at alpha is O(D_k+eta_k); the external contribution is O(eta_k). Since q_k(alpha)=O(D_k), polynomial division, evaluated at alpha, gives

    N_k(alpha)=O(D_k^2+eta_k).

In detail, P0(alpha)L(alpha)=-H, and division yields

    H a_k(alpha)-h_k L(alpha)tau_k(alpha)
      =-L(alpha)q_k(alpha)M_k(alpha)/E(alpha)
        +h_k L(alpha)tau_k(alpha)(U_k(alpha)/E(alpha)-1).

All denominators are nonzero and uniformly bounded away from0, because negative-level external nodes cannot equal a common root.

A quadratic with leading coefficient D_k whose values at alpha1,alpha2 are O(D_k^2+eta_k) must satisfy

    N_k(z)=D_k c(z)+O(D_k^2+eta_k)

coefficientwise.

Let zeta_j be a persistent root of tau_k, and eta_j the matched root of a_k. Write R_j=zeta_j-eta_j. If a_k=(z-eta_j)A_j, then

    R_j=N_k(zeta_j)/(H A_j(zeta_j))
       =D_k c(zeta_j)/(H A_j(zeta_j))+O(D_k^2+eta_k).

The coefficient c(zeta_j)/(H A_j(zeta_j)) has a fixed sign and modulus bounded away from0 uniformly near the limiting polytope: c has roots only in the q/r bands, not in persistent Dirichlet gaps, and A_j has roots uniformly separated from zeta_j. Thus the wrong-sign part of R_j is bounded by C eta_k plus an exponentially small error; the O(D_k^2) term is absorbed into the leading nonzero multiple of D_k.

Finally the exact new-pole evaluation identity from the team's compression/pole analysis gives

    zeta_{j,k+1}-zeta_{j,k}=C_{j,k} R_{j,k+1},
    0<=C_{j,k}<=C,

up to exponentially small projection error. Therefore the wrong-direction variation of each persistent pole is summable. A bounded real sequence with summable variation in one direction converges. All persistent poles converge; hence tau_k, M_k, the weights, and finally the even normalized residual vectors converge.

This proves the gcd-degree2 case for s=3 in arbitrary dimension. The argument is quantitative and does not invoke a generic summable-noise theorem.

# s=3 global case reduction: proved cases and precise remaining step

Notation follows agent3_global_reduction.md and agent1_global_polynomial_proof.md. The even and odd monic cubics converge with bounded total variation to q,r; H=lim h>0; Q=qr. After discarding a finite initial segment all retained spectral coordinates are nonzero. Let Splus be ALL retained nodes with Q(lambda)=H (not merely the union of limiting positive-weight supports). Off Splus, weights are summable. Those with |Q|<H are exponentially small, while the only remaining external nodes satisfy Q(beta)=-H.

## Already proved

1. If |Splus|<=4 then the limiting weights are unique from the three q-orthogonality equations and normalization, hence convergence.

2. If q=r, convergence for every dimension follows from agent2_equal_limit_polynomials.md. BV-tail distance of q_k from q is O(H-h_k), while the projection identity makes it quadratic in that distance plus exponentially small external weights; absorption gives exponential convergence.

3. If deg gcd(q,r)=2, convergence for every dimension follows from agent3_s3_gcd2_lemma.md, independently audited by agent1 (#267). The quadratic normal polynomial is D*c+O(D^2+eta), so persistent residues have fixed signs modulo summable wrong-sign parts.

4. If there are NO negative-level external nodes, all external weights decay exponentially. Project onto the at-most-six core nodes. Exact core pole recurrences plus exponentially small perturbations prove convergence, as follows.
   - Five-node core: a is monic quadratic and t=h(z-zeta). The scalar residue R=zeta-eta satisfies R_next=C R, C->1 positive, by the constant-B determinant identity. Exponentially small errors are handled by the scalar integrating-factor lemma.
   - Six-node core: a and t/h are monic quadratics. Each residue has the exact recurrence R_j,next=C_j R_j-D_j K, with C_j->1 positive, D_1>0 and D_2<0; K=h_next-h>=0. The same integrating-factor lemma gives eventual sign or an exponentially small wrong-sign part. B-compression/interlacing gives the nonnegative bounded new-pole coefficient, so both poles converge.
   See agent2_B_compression_proof.md and the team's exact pole recurrences.

## Entropies for negative external nodes

For a full simple six-node core lambda1<...<lambda6, let ell_i be its Lagrange interpolation polynomials. For Q(beta)=-H,

    L_beta=log w_beta + sum_i ell_i(beta) log w_i

is eventually strictly increasing, with increment at least c(H-h_k). BV-tail control makes every Taylor remainder O((H-h_k)^2), whereas the leading term is positive of order H-h_k. If beta is in band B_j=(lambda_{2j-1},lambda_{2j}), its negative core coefficients are:

    B1: i=3,5;     B2: i=2,5;     B3: i=2,4.

Thus any negative external node forces the omega-limit set onto a proper union of two adjacent edges of the fixed square. Negative external nodes cannot occupy all three bands (positive Stieltjes/entropy-cone certificate, agent1 #198).

### Two occupied outer bands: convergence is proved

Suppose beta in B1 and gamma in B3. Let xi=lambda3 or lambda4 and take positive a,b with

    a/(z-beta)+b/(z-gamma)=(z-xi)/((z-beta)(z-gamma)).

Then c_i=a ell_i(beta)+b ell_i(gamma) equals

    2H(lambda_i-xi)/[(lambda_i-beta)(lambda_i-gamma)P'(lambda_i)].

For xi=lambda3, all c_i are nonnegative except c_4<0 (c_3=0). Monotonicity of aL_beta+bL_gamma and w_beta,w_gamma->0 therefore force w_4->0. Choosing xi=lambda4 forces w_3->0. Only four core nodes remain, so the limiting weights are unique. An exact algebraic instance of both certificates is checked in agent3_s3_entropy_middle_check.py.

### One occupied middle band: convergence is proved by extremal poles

If negative external nodes occur only in B2, the two persistent Dirichlet poles are respectively the leftmost and rightmost non-exponentially-decaying t-poles. At a zero residue, B has that pole as a root; interlacing with the next t polynomial makes residue crossings one-way. Regularity holds for gcd<=1, while gcd2 is handled independently above. The one-sided scalar integrating-factor argument, with exponentially small discarded modes, then gives convergence of both poles.

### Outer empty band: exact remaining geometry

Suppose the only possible occupied bands are B1,B2 and B3 is empty. A positive two-node Stieltjes certificate with numerator z-lambda2 or z-lambda3 has all nonnegative core coefficients except c5<0. Therefore w5->0, confining the omega-limit set to the fixed edge w5=0. The right persistent pole tends lambda5 and has bounded variation by its extremal-pole barrier. If only B1 is occupied, the same conclusion is needed only when that extremal pole tends its outward endpoint lambda5; other limiting positions force the second pole to an endpoint via the single entropy and yield convergence directly. The reflected configuration is identical.

On the edge, let u be the remaining persistent pole, let g=w5, and let R1,R2 be the two residues. Put D=H-h. The proved BV estimate gives |R_j|<=C D. Analytic-ideal factorization yields, for the exact six-node core,

    R1,next = a_k R1 - g R2^2 B_k,       B_k>=0,

after absorbing terms divisible by R1 into a_k. Negative external nodes add signed linear forcing: the far band B1 has positive coefficient and the nearer B2 negative coefficient. On every compact OPEN edge segment, entropy comparison shows the near-band mass is a higher power of the far-band mass, hence is negligible. The ghost forcing gR2^2 has tail o(D), because g is comparable to the outward pole's remaining distance and that pole is monotone.

The team has established pole-energy and residue-BV lemmas (agent2_pole_residue_BV_lemma.md), and bounded homogeneous transport on compact open edge segments. A tail-energy absorption would close convergence if far-band dominance were uniform for the entire future orbit.

## Precise unresolved point

The entropy dominance is NOT uniform near the endpoint where another core weight vanishes: a logarithmic term can diverge and permit the near external band to revive. Also off-face transport has a possible boundary-layer g/(u-endpoint) term. Therefore the current work does NOT yet exclude infinitely many edge excursions with deep vertex visits. One needs a local no-return/energy argument across such visits, or a globally uniform corrected transport/entropy invariant. No assertion of a complete s=3 proof is made here.

The case |Splus|=5 can be regarded as an edge with the sixth positive-level root a permanently zero virtual coordinate when that root is distinct. If Q-H has a double positive-level root, one must explicitly use the confluent-factor version (or remain in the five-node a/t formulation); this should not be silently omitted.

# Conditional all-dimensional Green-mass positivity using a finite spin cover

Assume compact connected LCF (up to boundary) M has positive first eigenvalue
for -L with B=0. Let p be a boundary point with a normalized positive boundary
Green function G_p. Assume its conformal blow-up metric G_p^(4/(n-2))g is
asymptotically flat with noncompact boundary, with the decay/regularity needed
for the spin positive-mass theorem and well-defined mass m_g(p). Assume the
same local AF hypotheses for its lifts to finite covers. These are real
hypotheses: this note does NOT derive them from arbitrary blow-up jets.

Classical input: the spin positive-mass theorem with noncompact boundary
(R>=0,H>=0, appropriate AF decay), including zero-mass rigidity to Euclidean
half-space; for example the theorem of Almaraz--Barbosa--de Lima.

Then m_g(p)>=0, and m_g(p)>0 unless (M,g) is conformally equivalent to the
round hemisphere.

Proof. Take the finite connected spin cover pi:Mhat->M from
agent2_finite_spin_cover.md. Positive Yamabe type lifts. Indeed if v>0 is the
base first eigenfunction and vhat its lift, integration by parts gives,
for every smooth phi on Mhat,
 Q_hat(phi)=integral vhat^2 |grad(phi/vhat)|^2
             +lambda_1 integral phi^2.
The Robin boundary terms cancel exactly by B vhat=0. Thus lambda_1hat>0.

Let p_1,...,p_d be the lifts of p. Let Ghat_j be the normalized single-pole
boundary Green function with pole p_j. Positivity follows from coercivity and
the maximum principle. Uniqueness of the Green problem gives
    G_p composed with pi = sum_j Ghat_j.
For each j, Ghat_j^(4/(n-2))ghat is scalar-flat and has minimal boundary.
It is complete, since the original manifold is compact, Ghat_j is strictly
positive away from its pole, and the assumed AF pole is at infinite distance.
It is spin. The noncompact-boundary spin PMT therefore gives its mass mhat_j>=0.

At p_1, the difference sum_(j!=1)Ghat_j is smooth, with positive value S if
cover degree d>1. The local leading singularity normalization is identical
under a covering local isometry. Adding a smooth function of value S changes
the inverted asymptotic conformal factor by 1+S R^(2-n)+o(R^(2-n)); consequently
it changes the mass by a positive dimensional constant times S (by 2S in the
usual Schwarzschild normalization). Therefore
    m_g(p)=mhat_1+C_n S, with C_n>0.
This proves strict positivity if d>1. If d=1, PMT gives nonnegativity directly.
If its mass is zero, spin PMT rigidity makes the Green metric Euclidean
half-space. Adding back the Green pole gives the smooth conformal hemisphere
compactification. Thus zero mass forces the excluded conformal hemisphere.

Scope. The finite-cover/spin issue is resolved by this argument. The sharp
boundary blow-up estimates, required AF jet decay, existence and precise
local expansion of the boundary Green function, and identification of its
mass in the blow-up Pohozaev limit are NOT supplied by it.

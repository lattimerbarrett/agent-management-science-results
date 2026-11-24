# Proved scalar-Liouville lemma (NOT a full Oka theorem)

Let n>=2, K be a compact smooth domain, and suppose its outward Levi form has at least one positive complex-tangent direction at every boundary point. Then every continuous bounded-above plurisubharmonic function on Y=C^n minus K is constant, provided Y is connected.

1. Exterior of a Euclidean ball is scalar-Liouville. Through any p outside the ball, the affine complex lines in directions v near a Hermitian-orthogonal direction to p miss the ball. Choose n complex-linearly independent such directions; they remain safe through all points in a small neighborhood of p. Bounded subharmonic Liouville on each whole line makes u invariant under sufficiently small translations in each of these directions. Thus u is locally constant, and the exterior of the ball is connected.

2. Let u be continuous bounded-above psh on Y. By (1), u=c outside a sufficiently large ball containing K. If u is nonconstant, the maximum principle says it never attains its supremum M, so M>c. A maximizing sequence has a subsequence tending to a point q of boundary K; an interior limit would attain M.

3. Let p_j be that subsequence, q_j its nearest boundary point. Write p_j=q_j+t_j N_j, where t_j>0 tends to0, and choose smoothly varying complex normal vectors with partial rho(q_j)N_j=1. Choose a smoothly varying complex tangent vector v_j with Levi_rho(q_j;v_j)>=lambda>0. Put H_j=sum rho_zkzl(q_j) v_jk v_jl and

    d_j(zeta)=p_j+zeta v_j-(H_j/2) zeta^2 N_j.

The pure quadratic Taylor terms cancel. Uniform Taylor bounds give

    rho(d_j(zeta)) >= 2t_j+lambda |zeta|^2
                         -C(t_j^2+t_j |zeta|+|zeta|^3).

Choose a fixed small r>0 so Cr<min(1/2,lambda/2), then j large so Ct_j<1/2. For |zeta|<=r,

    rho(d_j(zeta)) >= t_j+(lambda/2)|zeta|^2 >0.

Thus all discs lie in Y. Their boundary circles lie in one fixed compact subset E of Y, because rho there has the uniform positive lower bound lambda r^2/2.

4. Since u never attains M, its maximum m on E satisfies m<M. The submean inequality yields u(p_j)<=m, contradicting u(p_j)->M.

Therefore u is constant.

Applications: both the quartic mixed-Levi examples and sufficiently small strongly pseudoconvex Rudin Klein-bottle tubes are scalar-Liouville. Thus neither can be shown non-Oka by a bounded continuous psh function on the BASE exterior. The lemma is much weaker than CAP and supplies no missing full-Oka theorem.

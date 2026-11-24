# Complete convergence proof for s=2, arbitrary finite dimension

This proof uses the team's established global BV lemma: after discarding the finite initial segment before the last support deletion, all retained spectral weights are positive; h_k=E_w q_k^2 increases to H>0; consecutive monic quadratics converge by parity to q,r and obey ||q_k-q_parity||<=C(H-h_k); F=qr equals H on every omega-limit support; every retained initial node satisfies |F(lambda)|<=H. Nodes with |F|<H have exponentially decreasing weights, and nodes with F=-H have weights tending to zero (indeed summably). The even residual sequence is asymptotically regular.

Let U be the union of the supports of all even cluster measures, and let S be the retained initial nodes with F=H. Then U is contained in S and |S|<=4. If |U|<=3, every even cluster measure is uniquely determined by q-orthogonality and total mass on U. For three nodes, q(lambda_i)w_i is the one-dimensional null vector of the two-row Vandermonde matrix, and positivity and normalization fix its scale; q cannot vanish at a supporting node. Measures with fewer than three nodes have h_2=0 and cannot be limiting measures. Thus the even weights converge in this case.

Henceforth assume |U|=4, so U=S. Write its nodes lambda1<lambda2<lambda3<lambda4. Put P0(z)=prod_i(z-lambdai); then F=P0+H. Each of q,r has one root in each band (lambda1,lambda2),(lambda3,lambda4), and both are strictly negative throughout the closed central gap [lambda2,lambda3]. This follows from positivity and the degree-two orthogonality, or from the sign alternation in its Vandermonde null vector. Every other retained node is in one of these two bands, since |F|<=H implies -2H<=P0<=0.

## 1. A negative-neutral external node forces loss of one core node

Let ell_i be the cubic Lagrange basis on S. For a node beta with F(beta)=-H define
 L_beta(k)=log w_{k,beta}+sum_i ell_i(beta)log w_{k,i}.
All these weights are positive. Write F_k=q_k q_{k+1} and D_k=H-h_k. The exact two-block update gives
 L_beta(k+2)-L_beta(k)
 =2[log|F_k(beta)|+sum_i ell_i(beta)log F_k(lambdai)]-2log(h_k h_{k+1}).
The BV tail bound gives ||F_k-F||<=C D_k. Its degree is at most three. Taylor expansion and Lagrange interpolation therefore cancel all linear terms:
 Delta L_beta=-2log(h_k h_{k+1}/H^2)+O(D_k^2)>=D_k/H>=0
eventually. (If D_k=0, the orbit already has T^2y=y.)

If beta lies in the left band, ell_1(beta),ell_2(beta),ell_4(beta)>0 and ell_3(beta)<0. Therefore
 L_beta(k)<=log w_{k,beta}+ell_3(beta)log w_{k,3}.
The left side is eventually bounded below, and log w_{k,beta}->-infinity. Consequently w_{k,3}->0. If beta is in the right band, the same argument forces w_{k,2}->0, since only ell_2(beta) is negative there. Thus the presence of any negative-neutral external node reduces the actual limiting support to at most three nodes, and the previous Vandermonde uniqueness argument proves convergence.

It remains to consider the case with no negative-neutral nodes. Then every node outside S has exponentially decreasing weight.

## 2. Exact four-node scalar identities

First consider an exact four-node weight step. Let M=P0 sum_i w_i/(z-lambdai) be its monic cubic Stieltjes numerator. Divide
 q_w M=(z-eta)P0+h(z-zeta),
where q_w is the monic orthogonal quadratic and h=E_w q_w^2. The restart identity is
 M_next=q_w(z-zeta).
Put primes on next-step quantities, K=h'-h>=0 and R=zeta-eta. Polynomial elimination gives
 h'(z-zeta')(z-eta)-h(z-eta')(z-zeta)=K q_w(z),
 K[h q_w(zeta)+q_w(eta)P0(zeta)]=-h R^2 P0(zeta),
 R'-R=(K/R)[q_w(eta)/h-q_w(zeta)/h'].
The last formula extends continuously to R=0. Near the compact limiting two-cycle set, the denominator in the second identity tends to q(zeta)^2 r(zeta), or r(zeta)^2 q(zeta), and is bounded away from zero. Consequently K=R^2 C0(w), with C0 bounded analytic. In the third identity the bracket is O(R)+O(K), so
 R'=R+R^2 A(w),
where A is uniformly bounded. This conclusion does not require R to be a regular coordinate and remains valid when q=r.

There is a second useful exact identity. Evaluate q_next M_next=(z-eta')P0+h'(z-zeta') at zeta', using M_next=q_w(z-zeta):
 zeta'-zeta=R' C(w),
 C(w)=P0(zeta')/[q_w(zeta')q_next(zeta')].
For sufficiently late steps, q_w and q_next are negative throughout the central gap, and zeta' lies in that gap. Thus 0<=C(w)<=C uniformly.

## 3. Exponentially perturbed four-node orbits

Project the original weights onto S and renormalize. Their exact update differs from the four-node map by O(rho^k), rho<1. The monic moment Gram matrix stays uniformly positive definite, since limiting supports contain at least three distinct nodes, and h is bounded below. The quantities eta,zeta,R are smooth functions of the four weights near the compact limiting set. Thus, for the projected sequence,
 R_{k+1}=a_k R_k+epsilon_k,
 a_k=1+O(R_k)->1, |epsilon_k|<=C rho^k,
and
 zeta_{k+1}-zeta_k=C_k R_{k+1}+delta_k,
 0<=C_k<=C, |delta_k|<=C rho^k.
Here R_k->0, since every cluster measure is a two-cycle and its Stieltjes numerator has the form r(z-zeta), or q(z-zeta), making eta=zeta.

For completeness, the elementary scalar perturbation argument is as follows. Choose K so a_k>0 thereafter and put A_K=1,A_{k+1}=a_k A_k. Then A_k=exp(o(k)), and
 u_k=R_k/A_k
has exponentially summable increments epsilon_k/A_{k+1}; hence u_k converges. If its limit is nonzero, R_k has eventually constant sign. If its limit is zero, then
 |R_k|<=A_k sum_{j>=k}|epsilon_j|/A_{j+1}<=C sigma^k
for some sigma<1. The latter estimate follows by bounding a_j between 1-delta and 1+delta, with delta sufficiently small relative to rho.

If R eventually has constant sign, the pole's variation in the opposite direction is exponentially summable. If R decays exponentially, its entire pole variation is summable. Since zeta is bounded, it converges in either case.

All even cluster measures now have the same Stieltjes numerator r(z-zeta_infinity) on S, hence the same weights. The even spectral weights converge. At each persistent spectral component the signed normalized two-step multiplier tends to F(lambda)/H=1; its sign is therefore eventually constant. All other components vanish. This proves Euclidean convergence of y_{2k} for arbitrary n when s=2.

Exact identities are checked in agent2_s2_pole_checks.py. The interpolation cancellation and Lagrange sign certificates are checked in agent2_s2_entropy_checks.py. The argument relies only on those identities and the independently proved global BV lemma.

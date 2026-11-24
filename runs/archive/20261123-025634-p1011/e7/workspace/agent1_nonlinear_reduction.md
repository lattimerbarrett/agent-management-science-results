# Uniform nonlinear reduction and boundary blowup from a reduced minimum

Assumptions: fixed smooth compact (M,g), Robin quadratic form Q coercive on H=H1(M), N=n(n-2), n>=7, p=(n+2)/(n-2) in (1,2). Let T:L^(2n/(n+2))(M)->H be the variational solution operator Q(Tf,w)=integral f w. Sobolev gives boundedness. Let W_{j,s}>=0 be smooth cut-off bubbles with parameter s=(lambda,xi) in a fixed compact neighborhood, K_{j,s} the span of parameter derivatives Z_a=partial_a W, and Pi_perp the Q-orthogonal projection.

Assume (i) the Gram matrices Q(Z_a,Z_b) are uniformly positive definite and ||Z_a||_H,||partial_b Z_a||_H bounded; (ii) projected operators L_{j,s}v=Pi_perp[v-T(Np W^(p-1)v)] on K_perp are uniformly invertible; (iii) e_j=sup_s||W-T(NW^p)||_H tends to0. These are explicit hypotheses, not conclusions of this document.

For F(t)=t_+^p, concavity of t^(p-1) gives |F'(a)-F'(b)|<=p|a-b|^(p-1). Hence the integral mean-value formula proves
|F(W+v)-F(W)-F'(W)v|<=|v|^p,
and the corresponding difference is bounded by C(|v|^(p-1)+|w|^(p-1))|v-w|. Holder and Sobolev imply that applying T maps these remainders to H with norm at most C||v||_H^p, and differences at most C(||v||_H^(p-1)+||w||_H^(p-1))||v-w||_H.

Thus the projected equation Pi_perp[W+v-T(NF(W+v))]=0 is equivalent to a contraction on ||v||<=C0 e_j for C0 sufficiently large and j large. There is a unique small correction v_{j,s} in K_perp with ||v||<=C0 e_j. If W,Z depend C1 on s, the Nemytskii map is C1 in these Banach spaces (its derivative is Holder), and the derivative of the projected equation is an invertible O(e_j^(p-1)) perturbation of L; the implicit function theorem gives C1 dependence of v.

Define E(u)=Q(u,u)/2-N/(p+1) integral (u_+)^(p+1), and J_j(s)=E(W+v). The projected equation says E'(W+v) has Q-Riesz representative in K. Differentiation gives partial_b J=sum_a c_a Q(Z_a,partial_bW+partial_bv). Orthogonality yields Q(Z_a,partial_bv)=-Q(partial_bZ_a,v)=O(e_j). The matrix on the right is Gram+O(e_j), hence invertible. Therefore every critical point of J_j gives a genuine weak solution of the full equation.

In particular, assume the additional uniform energy expansion J_j(s)=C_j+mu_j^2 F0(s)+o(mu_j^2) on a closed parameter ball, where F0 has a strict local minimum at its center and e_j=O(mu_j). Choose the ball small enough that F0 on its boundary exceeds its value at the center by a fixed gap. The uniform little-o implies J_j attains its minimum in the interior for large j. Since J_j is C1, this is a critical point and hence yields a true weak solution. No C1 remainder estimate is needed for this minimum argument.

Positivity and smoothness: test Q(u,w)=N integral(u_+)^p w with w=u_-=max(-u,0). The left side is -Q(u_-,u_-), right side0, so coercivity implies u>=0. The solution is nonzero because ||v|| tends to0 while ||W|| stays bounded below. Brezis-Kato iteration (including the smooth Robin boundary via local charts) first gives all finite Lq norms, then elliptic Lq estimates give continuity and boundedness. The strong maximum principle and Robin Hopf lemma give u>0 on the closure. Standard elliptic bootstrap now gives C-infinity, since u is strictly positive and real powers are smooth on (0,infinity).

Boundary blowup needs no pointwise estimate on v. Let q_b=2(n-1)/(n-2). The global trace inequality gives ||v||_L^(q_b)(boundary)<=C||v||_H=o(1). For the bubble centered at p_j with scale epsilon_j, the rescaled traces epsilon_j^((n-2)/2) W(p_j+epsilon_j y) converge on a unit boundary disc to the nonzero model trace U_s(y,0); its L^(q_b) norm is scale invariant. The rescaled correction has L^(q_b) norm o(1), since ((n-2)/2)q_b=n-1. Hence max_boundary u_j >=c epsilon_j^(-(n-2)/2) ->infinity.

This proves the nonlinear/positivity/minimum-to-solution implication under (i)-(iii) and the stated energy expansion. It does not assert those analytic hypotheses or the n>=7 reduced minimum needed by the original task.

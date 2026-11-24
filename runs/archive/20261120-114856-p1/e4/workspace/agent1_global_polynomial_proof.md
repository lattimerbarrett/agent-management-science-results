# Global polynomial convergence for every restart length

Let λ_1<...<λ_m be distinct active eigenvalues, and w_i=y_i² their spectral weights (combine eigenspaces). On a nonterminating orbit the support has at least s+1 points. Let q_w be the monic degree-s orthogonal polynomial and h(w)=Σw_i q_w(λ_i)². Then the weight map is T(w)_i=w_i q_w(λ_i)²/h(w). The actual unit residual map has the fixed overall sign (-1)^s.

For consecutive q=q_w and r=q_Tw, orthogonality gives E_w(qr)=h(w). Therefore
h(Tw)-h(w)=E_w[(qr-h(w))²]/h(w)≥0.
The corresponding unit-residual identity is
<y,T_res²y>=sqrt(h(w)/h(Tw)).
Hence h_k→H>0, every cluster point is a normalized two-cycle, and ||y_(k+2)-y_k||→0. Compactness and h≥h_0>0 ensure every cluster support has at least s+1 nodes, so the polynomial and residual maps remain continuous there.

Fix z<λ_1. Define Z_z(w)=Σw_i/(λ_i-z), u_i=y_i/[sqrt(λ_i-z)*sqrt(Z_z(w))], and p_w(t)=q_w(t)/q_w(z). Then p_w uniquely minimizes E_u p² among degree≤s polynomials p(z)=1, because every feasible difference has form (t-z)l(t), deg l<s, and E_u[p_w(t)(t-z)l(t)]=0. Write γ_z(w)=||p_w(A)u||>0. The transformed next normalized residual is p_w(A)u/γ_z(w), with no ambiguous sign since q_w(z) has fixed sign (-1)^s.

For p=p_w and p'=p_Tw, their common normalization p(z)=p'(z)=1 and orthogonality imply E_u(pp')=E_u(p²)=γ_z(w)². Also E_u[(pp')²]=γ_z(w)² γ_z(Tw)². Cauchy therefore proves γ_z(Tw)≥γ_z(w). Thus γ_z(w_k) converges to G_z>0.

At any two-cycle cluster point with polynomials q,r, the identity qr=H holds at every node in its support. Consequently p p'=H/[q(z)r(z)] on that support. Since equality holds in the preceding Cauchy argument at a two-cycle, γ_z²=H/[q(z)r(z)]. Hence every cluster pair has the same product value q(z)r(z)=H/G_z², for each fixed z<λ_1. Choosing 2s distinct such z determines the monic degree-2s product polynomial uniquely. Call it F.

The even cluster set is connected: it is the cluster set of a bounded sequence with successive even differences tending to zero. Its continuous image under w↦q_w is connected and is contained in the finite set of monic degree-s real factors of F. It is therefore a singleton. Thus q_(2k)→q and q_(2k+1)→r coefficientwise, qr=F, for every restart length s.

Every node carrying positive weight at any cluster point satisfies F(λ_i)=H. Thus the union of limiting supports is contained in the fixed set S={i:F(λ_i)=H}, of size≤2s. For i outside S, coefficient convergence implies |q_k(λ_i)q_(k+1)(λ_i)-h_k|≥c_i>0 eventually. The Lyapunov difference formula gives Σ_k w_i(k)<∞. (This is true even for a missing node with F(λ_i)=-H.)

This does NOT establish convergence of the weights on S. They may approach the fixed polytope {w≥0:Σw=1,Σw_i q(λ_i)λ_i^j=0,0≤j<s}. That final convergence/nonconvergence issue is exactly the remaining obstacle for s=2,3 versus s=4.

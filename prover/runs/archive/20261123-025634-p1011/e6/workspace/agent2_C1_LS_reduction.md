# Uniform derivative estimates and conditional C1 corrected reduction

This proves analytic implications from explicit differentiated source/operator
hypotheses. It does not establish unrestricted blow-up extraction or a
new dimension18 seed.

Use the fixed-Hilbert-space setup of agent2_reverse_LS_lemma.md. Let a_i>0
be independent of theta and tend to0. Suppose the ordinary projected LS
branch u_i=W_i+v_i exists on a compact parameter ball, with
 ||v_i||<=Ca_i, ||r_i||+||d_theta r_i||<=Ca_i,
where r_i=T(W_i). Assume uniformly bounded C1 projections P_i onto the Jacobi
spaces, uniformly bounded compressed inverses at W_i, and
 |d_theta W_i(x)|<=C W_i(x) pointwise.
The last condition holds for ordinary nonnegative bubbles with a fixed
parameter-independent cutoff and scaled parameters in a compact set.
Set sigma=min(2,p)>1.

## 1. Uniform parameter derivative of the correction
Since the projected equation holds, T(u_i) belongs to K_i and has norm O(a_i).
Differentiating P_i^perp T(u_i)=0 and P_i v_i=0 gives
 P_i^perp A_(u_i)(W_i,theta+v_i,theta)=P_i,theta T(u_i),
 P_i v_i,theta=-P_i,theta v_i=O(a_i),
where A_u=I-kappa p S((u_+)^(p-1) .).

The elementary scalar inequality, valid for w>=0 and all p>1,
 w |(w+b)_+^(p-1)-w^(p-1)|
 <=C[w^(p-1)|b|+|b|^p]
shows by Holder that
 ||(A_(W_i+v_i)-A_(W_i))W_i,theta||<=Ca_i.
Indeed |W_i,theta|<=CW_i, ||W_i||_q<=C, and ||v_i||<=Ca_i.
Also A_(W_i)W_i,theta=r_i,theta=O(a_i). The compressed A_(W_i+v_i)
is an o(1) operator-norm perturbation of the uniformly invertible compressed
A_(W_i), by C1 continuity of the critical Nemytskii map. Project off the
already controlled K component of v_i,theta and invert to obtain
 ||v_i,theta||<=Ca_i.
This proof uses no separate differentiation of a singular W_i^(p-1) at zero.

## 2. Difference from the linear correction in C1
Let l_i in K_i^perp solve P_i^perp A_(W_i)l_i=-P_i^perp r_i.
It has ||l_i||+||l_i,theta||<=Ca_i. The derivative assertion follows by
trivializing the moving complements; their projections have bounded C1 norm,
and A_(W_i) has bounded C1 norm because
 |W_i^(p-2) W_i,theta|<=C W_i^(p-1).

Put N(W,v)=(W+v)_+^p-W^p-pW^(p-1)v. Standard scalar Taylor estimates give
 ||S N(W_i,v_i)||<=C a_i^sigma.
The SAME order holds for its total theta derivative. For 1<p<=2, the
weighted pure-W derivative estimate is
 w |(w+b)_+^(p-1)-w^(p-1)-(p-1)w^(p-2)b|<=C|b|^p.
For p>=2 use C(w^(p-2)b^2+|b|^p) instead. These bounds follow by splitting
|b|<=w/2 and its complement, and scaling b/w. Multiplication by
|W_i,theta|<=CW_i plus Holder controls the pure parameter derivative;
the v derivative has norm <=C(||v_i||+||v_i||^(p-1)) times ||v_i,theta||.
Thus ||S N(W_i,v_i)||_C1<=C a_i^sigma.

The exact projected identity is
 v_i-l_i=kappa [P_i^perp A_(W_i)|_(K_i^perp)]^(-1)
                           P_i^perp S N(W_i,v_i).
The inverse and projection have uniformly bounded C1 norms, so
 ||v_i-l_i||_C1<=C a_i^sigma=o(a_i).

## 3. Function-Taylor remainder in C1
For the fixed-domain action J, write
 J(W_i+v_i)=J(W_i)+E(r_i,v_i)
                       +E(A_(W_i)v_i,v_i)/2+R_i.
Then
 ||R_i||_C1<=C[a_i^(p+1)+a_i^3]=o(a_i^2),
where in the range p<=2 the a_i^3 term can be omitted.
For values use the scalar Taylor remainder of x_+^(p+1). For derivatives in
v pair N(W_i,v_i)=O(a_i^sigma) with v_i,theta=O(a_i). For the pure W derivative,
multiplication by |W_i,theta|<=CW_i improves the apparent singular power:
if 1<p<=2 its absolute value is <=C|v_i|^(p+1); if p>=2 it is bounded by
C(W_i^(p-2)|v_i|^3+|v_i|^(p+1)). The proof again splits |v_i|<=W_i/2 and its
complement. Holder has total degree p+1 in all these integrands.

Replacing v_i by l_i now changes the quadratic terms by o_C1(a_i^2).
Since l_i is orthogonal to K_i,
 E(A_(W_i)l_i,l_i)=-E(r_i,l_i)
exactly, and hence
 J(W_i+v_i)=J(W_i)-E(A_(W_i)l_i,l_i)/2+o_C1(a_i^2).

## 4. Passing a C1 linear-response limit through varying bubble charts
A sufficient precise transfer criterion is the following. Let z_theta be a
C1 family in the limit halfspace Hilbert space. Approximate z_theta AND its
first parameter derivatives uniformly by a finite-dimensional family
z_theta^epsilon of functions in C_c^infinity(overline{R_+^n}), smooth up to the boundary,
compactly supported in the CLOSED halfspace and with unrestricted boundary
trace. Interior-supported zero-trace test functions are NOT the density class.
This is possible because their images are compact sets and the indicated
closed-halfspace class is dense in the Neumann Dirichlet-energy space: apply a
fixed finite-rank projection approximating both compact images.
Let I_i transfer compact test functions into the physical bubble chart,
independently of theta, and project their images to K_i^perp. Suppose the
transferred residual
 P_i^perp A_(W_i)P_i^perp I_i z_theta^epsilon
                           +P_i^perp r_i/a_i
has C1 H norm <=C epsilon+o_i(1), and transferred quadratic forms converge
in C1 on every such finite-dimensional compact family. These are local
coefficient/source convergence statements on smooth compact tests; source
tails are controlled in the global dual norm. Bounded C1 inverse norms then
give ||l_i/a_i-P_i^perp I_i z_theta^epsilon||_C1<=C epsilon+o_i(1).
Let i->infinity and then epsilon->0. In particular
 E(A_(W_i)l_i,l_i)/a_i^2 -> Q_theta(z_theta,z_theta) in C1.

Combining with a raw action expansion
 J(W_i)=C_i+a_i^2 D(theta)+o_C1(a_i^2)
gives the corrected expansion
 J(W_i+v_i)=C_i+a_i^2[D(theta)-Q_theta(z_theta,z_theta)/2]+o_C1(a_i^2).

For polynomial flat-graph cores with n>2d, the C1 raw/source bounds in
agent4's differentiated graph lemma and the same exterior polynomial-tail
bounds supply the transfer criterion: the pullback chart is independent of
bubble parameters, and compact-support coefficient convergence may be
differentiated because all parameter derivatives of bubble profiles have
the same decay envelope. This is still an expansion for that specified
core setting, not a theorem reducing arbitrary blow-up to such cores.

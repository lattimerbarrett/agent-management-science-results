# Finite spin cover of a compact locally conformally flat manifold

Lemma. Every compact smooth locally conformally flat manifold of dimension
n>=3, with or without smooth boundary and with conformal flatness up to the
boundary, has a finite connected orientable spin cover.

Classical inputs: Liouville's theorem/developing-map construction for conformal
structures in dimension >=3; residual finiteness of finitely generated linear
groups over characteristic zero (Malcev's theorem); the spin obstruction w2.

Proof. First pass to the orientation double cover if needed. Oriented
conformal transition maps are restrictions of elements of Conf^+(S^n),
identified with SO^+(n+1,1) acting on positive null rays. The developing map
and holonomy representation rho:pi1(M)->SO^+(n+1,1) define a flat Lorentzian
vector bundle E of rank n+2. The developing map specifies a positive null
line subbundle L of E. An oriented real line bundle is trivial. The
conformal derivative identifies TM with Hom(L,L^perp/L). As L is trivial,
L^perp/L is isomorphic to TM. Splitting these vector-bundle short exact
sequences (using any auxiliary positive-definite bundle metric) gives
E isomorphic to TM plus two trivial real line bundles.

The holonomy image Gamma is finitely generated because pi1(M) is. Its full
inverse image Gamma_tilde under Spin^+(n+1,1)->SO^+(n+1,1) is finitely
generated: lift finitely many generators and adjoin the central element -1.
The spin group is a linear group, via its Clifford-algebra representation.
By residual finiteness there is a finite-index subgroup H of Gamma_tilde
not containing -1. Projection is injective on H. Thus Gamma'=image(H) is
finite-index in Gamma and its inclusion in SO^+(n+1,1) lifts to the spin
group, using the inverse of projection restricted to H.

The finite connected cover M' associated to rho^{-1}(Gamma') has a flat spin
lift of E'. Consequently w2(E')=0. Since E' is TM' plus two trivial lines,
w2(TM')=0. M' is oriented, so this is precisely the spin obstruction; hence
M' is spin. Boundary charts cause no change in the bundle construction.

Scope: this lemma alone is not a positive-mass theorem. For a Green blow-up
on M', completeness, AF boundary-end decay, scalar/mean-curvature signs,
and the hypotheses and rigidity of a spin positive-mass theorem with
noncompact boundary must still be verified. Finite covers at least avoid
infinitely many uncontrolled/incomplete universal-cover ends.

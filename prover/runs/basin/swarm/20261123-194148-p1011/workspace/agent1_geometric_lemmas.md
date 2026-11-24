# Geometric side conditions and conformal invariance
Let n>=3 and c=(n-2)/(4(n-1)). The quadratic form of the boundary spectral problem is
Q_g(v)=int_M (|dv|_g^2+c R_g v^2) dv_g+2c int_boundary H_g v^2 ds_g.
This follows from integration by parts with outward normal and B_g v=0.

If (Omega,delta) is a smooth bounded connected Euclidean domain with H>=0 everywhere
and H>0 on a nonempty open subset of its boundary, Q(v)>0 for every v!=0,
and the first eigenvalue is strictly positive. To prove the uniform spectral gap,
suppose int v_j^2=1 and Q(v_j)->0. Poincare's inequality gives v_j-a_j->0 in H1,
and a subsequence a_j converges to a nonzero constant a. The trace theorem gives
boundary L2 convergence, forcing int H v_j^2->a^2 int H>0, contradiction.
The first eigenvalue depends continuously on the metric/domain in C2, by pulling
back to a fixed domain and comparing the quadratic forms and L2 norms. Therefore
positive Yamabe type persists under sufficiently small C2 graph perturbations.

A smooth convex bounded Euclidean domain with an open planar boundary patch and
with H>0 elsewhere can be made by smoothing a convex body having one flat face;
Q positivity follows as above. Such a fixed domain is a convenient unperturbed
background for all local graph constructions.

Under ghat=exp(2f)g, nuhat=exp(-f)nu, and the conformal connection formula yields
IIhat=exp(f)(II+nu(f)g_T),
Hhat=exp(-f)(H+(n-1)nu(f)),
IIhat^0=exp(f)II^0.
In particular a single nonumbilic point rules out conformal equivalence with the
hemisphere. Every Euclidean domain, with its Euclidean metric, is locally
conformally flat up to the boundary by definition.

Conformal covariance, with ghat=w^(4/(n-2))g, is
L_ghat(v)=w^(-(n+2)/(n-2)) L_g(wv),
B_ghat(v)=w^(-n/(n-2)) B_g(wv).
Thus u solves the required nonlinear equation for g iff u/w solves it for ghat.
Since w is fixed smooth positive on a compact manifold, boundary blowup is
preserved by this correspondence. The quadratic forms satisfy Q_ghat(v)=Q_g(wv),
so positivity of the first eigenvalue is conformally invariant as well.


# Virtually spin reduction for conformally flat manifolds
Pass first to the orientable finite cover. A conformally flat structure has a
developing map dev:Mtilde->S^n and holonomy rho:pi1(M)->SO^+(n+1,1).
The holonomy image Gamma is finitely generated because M is compact. Its inverse
image Gamma_tilde in Spin(n+1,1) is a finite extension of Gamma, hence finitely
generated, and is a linear group over characteristic zero. Malcev residual
finiteness supplies a finite-index normal subgroup K not containing the central
nontrivial element -1. The projection K->Gamma is therefore injective, and its
image Gamma' has finite index. The finite cover associated to rho^{-1}(Gamma')
has holonomy lifted to Spin(n+1,1). Pulling the standard conformal spin structure
of S^n through dev and this lifted action gives a spin structure on that cover.
This argument does not require dev to be injective.

Consequently a Green-function blowup of a compact conformally flat manifold can
be lifted to a finite spin cover. If the Green metric is scalar-flat, minimal on
the boundary, complete asymptotically flat with the usual rate and integrability,
apply the spin version of the asymptotically-flat boundary positive mass theorem
to each lifted end. A boundary pole lifts to finitely many boundary ends, with
unchanged individual masses. Zero mass rigidity forces the covering Green
manifold to be a Euclidean halfspace, hence to have exactly one end. Thus if the
cover has degree greater than one all individual masses are strictly positive.
If its degree is one, zero mass implies that the original compactification is
conformally a hemisphere (extension across the missing pole follows from the
smooth conformally flat compactification). This is the strict-mass conclusion
needed in the compactness argument.

The positive-mass input here is the spin case of Almaraz--Barbosa--de Lima,
'A positive mass theorem for asymptotically flat manifolds with a non-compact
boundary', Communications in Analysis and Geometry 24 (2016), 673--715.
One must FIRST establish the Green metric AF regularity and mass identity from
the blowup/jet analysis; the spin-cover argument alone does not establish them.

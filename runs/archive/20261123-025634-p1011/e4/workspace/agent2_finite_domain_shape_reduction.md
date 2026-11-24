# Finite-domain shape reduction: precise auxiliary proposition

This is a proposed analytic lemma with its proof mechanism spelled out; it is NOT a fixed-manifold gluing theorem, nor a low-dimensional compactness theorem. In particular its dimension assumption is n>16, not n>=20.

Fix n>16, q=2n/(n-2), beta=(n-2)/(2(n-1)), a0=2^{-(n-2)/2}. Let N be the unit round hemisphere. Let h_R be smooth functions on its equator, obtained by stereographically truncating a degree-eight Euclidean graph profile H_2(z)p(|z|^2) after multiplication by 2/(1+|z|^2). Thus near the truncation pole, with stereographic radius r, assume uniformly

  |h_R| <= C(1+r)^6, |grad h_R| <= C(1+r)^7,
  |Hess h_R| <= C(1+r)^8, h_R=0 for r>=2R.

Assume h_R converges to h in W^{2,p} for p=2(n-1)/n and in H^1 on the equator (these follow from these bounds and a standard radial cutoff when n>16). Let t->0, R->infinity, and delta=t R^7->0. Let N_{t,R} have boundary the latitude graph s=t h_R, interior toward increasing latitude.

For the critical action

 I(v)=1/2[ integral(|grad v|^2+c_n R v^2)+beta integral_boundary H v^2]
      - n(n-2)/q integral(v_+)^q,

the projected Euler-Lagrange equation, after removing the n-dimensional hemisphere Jacobi kernel K (tangential coordinate functions), has a unique correction w=t z+o(t) in H^1 near a0. Here z is the K-orthogonal solution of

 (-Delta-n)z=0, partial_nu z=-beta*a0*(Delta_boundary+n-1)h.

The projected action satisfies

 I(a0+w)=I_N(a0) - (beta*a0)^2 t^2/2 * Q(h) + o(t^2),

where Q(h)=<Dh, DN^{-1}Dh>, D=Delta_boundary+n-1, with degree-zero response assigned boundary value zero and degree-one defect zero. Estimates are uniform over any fixed compact set of polynomial-profile parameters with the stated derivative bounds.

## Proof mechanism, with estimates

1. Pull the normal graph back by a collar diffeomorphism. Metric and volume coefficients differ from round by O(delta) in L-infinity. The boundary Robin form differs by O(delta), because H has L^{n-1} norm O(t R^7), and the critical trace inequality controls integral H v w.

2. The limiting Hessian is A=-Delta-n with Neumann boundary. Its only kernel is K; on K-perpendicular it has a bounded H^1-to-H^{-1} inverse. This follows directly from the hemisphere spherical-harmonic spectrum. The constant negative mode is not excluded and is invertible. A form perturbation of norm O(delta) preserves this inverse.

3. The exact graph curvature, W=(1+sec^2(s)|grad s|^2)^{1/2}, is

 H=(n-1)tan(s)/W + sec^2(s)Delta(s)/W
   +sec^2(s)|grad s|^2 tan(s)/W^3
   -sec^4(s)Hess(s)(grad s,grad s)/W^3.

Consequently ||H-tDh_R||_Lp <= C delta^2 t (||h_R||_Lp+||Hess h_R||_Lp)=o(t).
The uniform W^{2,p} bound requires exactly n>16, since spherical measure at infinity is asymptotic to r^{-n}dr and the Hessian is O(r^8).
The constant a0 solves the interior equation exactly; its residual is therefore beta*a0*H on the boundary. It is O(t) in H^{-1}, converging after division by t to beta*a0*Dh.

4. The critical nonlinearity gives a gradient remainder bounded by C||w||_{H1}^{1+alpha}, alpha=min(1,4/(n-2))>0. Uniform inverse plus contraction gives w=O(t), and the resolvent identity gives w/t->z strongly in H1.

5. The constant-function action has zero first and second shape derivatives at the equator. For the first derivative, the volume and total-mean-curvature contributions cancel; the second derivative vanishes by equatorial reflection. To make this uniform for h_R, the exact graph formulas bound the remainder by

 C t^3 integral (|h_R|^3+|h_R||grad h_R|^2+|Hess h_R||grad h_R|^2).

The integral is at most C[1+R^{max(23-n,0)}+log R]. Division by t^2 tends to zero since t R^7->0 and n>16. Higher denominator/Taylor errors are absorbed by delta^2.

6. Expansion in w gives residual(w)+1/2<A w,w>+o(t^2); since Az=-residual/t, this equals minus one half of the response quadratic form. Boundary spherical degree ell>=2 has DN multiplier

 mu_ell=2 Gamma((ell+n+1)/2)Gamma(ell/2)/[Gamma((ell-1)/2)Gamma((ell+n)/2)].

The ell=0 response has zero boundary trace (normal-coordinate solution), and D annihilates ell=1.

## What still needs care before citing this as a completed lemma

* Write the collar pullback and projected spaces explicitly, checking uniform constants including boundary measure transport.
* Establish the quoted nonlinear estimates with this pullback and positive-part action, rather than treating them as standard.
* Verify the exact uniform constant-action remainder estimate from graph area/curvature, including integration measures.
* Explain parameter differentiability or use strict-minimum stability at the continuous reduced-energy level.

Even completion of all these finite-domain details does not supply the fixed-domain infinite-bump gluing step: other bumps and cutoff errors must be controlled by o(t_i^2) uniformly in each local reduction. Nor does it prove any n<=19 compactness result. Current exact algebra has a strict formal minimum at n19, so concealing this would be incorrect.


## Addendum: closing the finite-domain technical estimates

The four finite-domain qualifications above can be addressed as follows (they do not address infinite gluing).

* Choose a smooth regularized distance rho(y) to the stereographic pole, comparable to (1+r)^(-1), with bounded gradient. Extend h_R by E h_R(y,s)=chi(s/rho(y))h_R(y), in a collar. Then ||D(E h_R)||_infinity <= C R^7. The graph map (y,s)->(y,s+t E h_R) is a diffeomorphism for tR^7 small. Its metric/volume forms differ by O(tR^7); its boundary Robin form has norm O(tR^7) by Holder with H in L^{n-1} and the critical trace embedding. This gives an explicit fixed Hilbert space on which to apply the Neumann-series inverse and contraction.

* The pointwise critical gradient remainder is bounded by C|w|^p for p=(n+2)/(n-2)<2. Sobolev and Holder give its H^{-1} norm <=C||w||_{H1}^p. The same estimate for differences proves contraction on an O(t) ball. The derivative is Holder continuous, enough for the C1 implicit function theorem with respect to any finite smooth bubble-parameter family.

* Exact total-curvature density, m=n-1, s=t h_R, is

 H dA = [m tan(s)cos^m(s) + cos^(m-2)(s)Delta s
  +cos^(m-2)(s)|grad s|^2 tan(s)/W^2
  -cos^(m-4)(s)Hess s(grad s,grad s)/W^2] d_sigma.

Integrating the Delta term by parts proves the previously quoted cubic bound, with coefficient functions uniformly bounded for ||s||C1 small. The linear action coefficient is zero because -(n-2)/4+beta*m/2=0. The integrated curvature cubic coefficient is

 m(1/3-m/2) h^3+(m-1)h|grad h|^2-Hess h(grad h,grad h).

The symbolic identities, including the exact cubic coefficient before and after integration by parts, are checked in agent2_total_curvature_action_checks.py. The bound O(t^3[1+R^{max(23-n,0)}+log R]) is o(t^2) for n>16 and tR^7->0.

* Compact parameter sets retain identical growth bounds and dominating radial weights. Thus the energy expansion is uniform in parameters. A strict reduced local minimum persists under the uniform o(t^2) perturbation, without requiring second derivatives of the nonlinear reduction. The kernel-to-bubble-parameter matrix is invertible at t=0 because conformal automorphism derivatives span the n-dimensional Neumann kernel, and remains invertible for small perturbations. Consequently an interior critical point of the reduced action gives a full solution. Positivity follows by testing the positive-part equation on its negative part, using positivity of the conformal Robin quadratic form on these small deformations, then the strong maximum principle and boundary point lemma.

These details provide a finite-domain perturbation argument, not the fixed-background sequence required in the question. The remote-bump/cutoff error must still be proved o(t_i^2) in a common fixed domain. The currently certified formal n19 strict minimum would also fall within this local argument; therefore it cannot be suppressed in any claimed compactness proof.

# Uniform bounded-form estimates for localized shape Taylor expansion

Write s=(1+|y|^2+t^2)^(1/2), choose chi(t/(1+|y|)) supported where
t<=2(1+|y|), and Phi_F(y,t)=(y,t+chi F(y)). Work with additive MATERIAL
H1 correction z and comparison bubble U o Phi_F, rather than composing z.
Define
 delta(F)=sup[|DF|+|F|/(1+|y|)+(1+|y|)|D2F|+(1+|y|)^2|D3F|]
and
 N(F)^2=int_{halfspace} U^2[|D2F|^2+|DF|^2/s^2+|F|^2/s^4] on the extension strip.
For the dilation direction DFgen=y.gradF-F include its analogous seminorms;
for finite jets of bounded degree these are bounded by fixed multiples.
For a scaled smooth tangent graph on radius R=r/eps, delta<=C r.

The following direct coefficient estimates justify functional Taylor uniformly
in R. The cutoff deformation is assumed to vanish before the outer cap.

* D Phi-I=O(delta), and s D2Phi=O(delta).
* The pulled-back Dirichlet matrix and volume density are analytic functions
  of D Phi when delta<1/2. Their first variations in the graph/dilation
  directions are O(delta); subsequent directional variations gain another
  graph factor. They multiply grad z.grad z or |U+z|^q, controlled by D-energy
  and Sobolev, uniformly in R.
* H_F dS_F=(delta_ab-F_a F_b/(1+|DF|^2)) F_ab dy. Its difference from Delta F
  is bounded by C|DF|^2|D2F|. Boundary coefficients are bounded by
  C delta/(1+|y|). The trace Hardy inequality controls the quadratic z term.
* On the extension strip |D^j U|<=C_j U s^(-j). Consequently
  ||(Phi_F-Id).gradU||_D<=C N(F), and each extra graph derivative contributes
  delta. This also controls all material terms from U o Phi_F.
* Direct fixed-ambient-U energy is odd under F->-F, so its second graph
  derivative at0 vanishes EXACTLY. The remaining cubic graph derivative is
  bounded by C delta N(F)^2. For example the boundary cubic coefficient is
  |DF|^2|D2F|U^2; after one graph factor is bounded by delta, its remaining
  weighted quadratic integral is bounded by N(F)^2 by tangential integration
  by parts and Cauchy-Schwarz. Bulk terms are treated by the previous U bounds.
* The mixed graph-u derivative at0 is the boundary source S_F, by the exact
  integration-by-parts identity in Slack193. Its variation away from0 is bounded
  by C delta N(F)||z||_D; the second-z shape derivative is bounded by
  C delta||z||_D^2. The energy nonlinearity has C^(2,alpha) modulus,
  alpha=min(1,4/(n-2)), giving O(||z||_D^(2+alpha)); for low n use cubic.

Thus after the EXACT full first-shape rim subtraction the localized Ward
expansion has leading mixed term <S_DFgen,z>, with error bounded by
 C delta [N(F)^2+N(F)||z||_D+||z||_D^2]
 +o(N(F)^2+||z||_D^2).
No derivative/composition of a general H1 correction is taken.

For F=sum eps^(k-1)F_k plus physical Taylor remainder of degree d+1,
radial integration gives
 N(F)<=C[eta+eps^((n-2)/2)r^(d+1-n/2)].
Indeed the degree-k squared radial integrand is r^(2k-n-1), yielding finite
energy for2k<n and logR for2k=n. The remainder has degree d+1 and yields exactly
the stated positive power of physical r. These are the same majorants as the
boundary-source estimates, so the Ward estimate is compatible with the
projected-inverse/cross estimates already established.

Outer matching h must NOT be treated only through its full D norm at the fine
stage. First use the coarse C_r eps^(n-2) bound to force vanishing jets. Then
pass to the normalized Green limit and use F=O(r^(d+1)), G-pole=O(r^(d+2-n))
to bound cap/high-graph quadratic terms by O(r^(2d+2-n)), cubic by
O(r^(3d+2-n)); both tend to0. Full linear terms are retained in the exact rim.

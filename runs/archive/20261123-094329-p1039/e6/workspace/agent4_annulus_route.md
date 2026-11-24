# Non-polynomially-convex example: sufficiency route
This is a SPECIAL CASE, not the requested universal theorem.

Let K={(|z|^2-2)^2+|w|^2<=1/4} in C^2, r=sqrt(3/2).
K is Reinhardt, and log K is convex: on the allowed radial interval,
(t,s)->(exp(2t)-2)^2+exp(2s) is convex, since its t-second derivative
is 16 exp(2t)(exp(2t)-1)>0. K is complete in w. Thus K is holomorphically
convex in X_0=C* x C, by the Laurent/Reinhardt hull criterion.

Fix 0<|a|<r/2. I claim K is holomorphically convex also in
X_a=(C minus {a}) x C. For q in X_a minus K:
* If |q_z-a|<r-|a|, the function 1/(z-a) separates q from K.
* Otherwise |q_z-a|>=r-|a|>|a|. Also |z-a|>=r-|a|>|a| on K.
  Laurent polynomials in z,w separating q from K in X_0 can be
  approximated uniformly on K union {q} by functions holomorphic on X_a,
  using 1/z=sum_{k>=0}(-a)^k/(z-a)^(k+1). This gives separation.
At equality of the first comparison the second argument applies.

X_a has density property. In coordinates u=z-a !=0,w, complete fields
A_k=u^k d/dw, B_k=u^k w d/dw (k any integer),
C_l=u w^l d/du (l>=0) satisfy
[A_k,C_{l+1}]-[B_k,C_l]=u^(k+1)w^l d/du.
So all Laurent monomial u-fields are generated. Bracketing
u^k w^l d/du with u d/dw gives
u^k w^l d/dw - l u^(k+1)w^(l-1)d/du,
so all Laurent monomial w-fields are generated too. Laurent polynomial
fields are dense in holomorphic vector fields on C* x C. The exact
bracket identities were checked in agent4_density_check.py.

Now invoke TWO STANDARD DEEP Oka results explicitly:
(1) Kusakabe: a holomorphically convex compact in a Stein manifold with
    the density property has Oka complement.
(2) Zariski localization: a complex manifold covered by Zariski-open
    Oka subsets is Oka.
Result (1) makes X_0 minus K and X_a minus K Oka. They are Zariski-open
subsets of Y=C^2 minus K and cover Y because a!=0. Hence (2) makes Y Oka.

This does not handle general pseudoconvex K; there need not be a
coordinate puncture making a general compact holomorphically convex.

# Exact Euclidean Robin critical Pohozaev identity

Let Omega be a smooth Euclidean domain, u>0 solve
 Delta u+n(n-2)u^((n+2)/(n-2))=0,
 partial_nu u+b H u=0,
where b=(n-2)/(2(n-1)) and H=div_boundary nu is the trace mean curvature.
Put a=(n-2)/2, F(u)=(n-2)^2 u^(2n/(n-2))/2, X=x,
s=X.nu, X_T=X-s nu. At a regular intersection radius r set
 Gamma=boundary Omega intersect B_r,
 S=Omega intersect boundary B_r,
and let eta be the outward conormal of boundary Gamma inside Gamma.
Then, writing grad_Gamma for tangential gradient,

 P(u,r):=integral_S [(a u+r partial_r u) partial_r u
                         -r(|grad u|^2/2-F(u))]
 = integral_Gamma {s[|grad_Gamma u|^2/2-F(u)
                         -b(b-1)H^2u^2/2]
                   -(b/2)(X_T.grad_Gamma H+H)u^2}
   +(b/2)integral_boundaryGamma H u^2 X_T.eta.

Proof. Define
 J=(X.grad u+a u)grad u-X(|grad u|^2/2-F(u)).
Direct differentiation gives
 div J=(X.grad u+a u)(Delta u+F'(u))+nF(u)-a u F'(u)=0;
the last equality uses a*(2n/(n-2))=n. Its flux on S is P.
On Gamma use partial_nu u=-bHu to obtain
 J.nu=-(b/2)H X_T.grad_Gamma(u^2)-abH u^2
       +s[b^2H^2u^2/2-|grad_Gamma u|^2/2+F(u)].
Tangential divergence gives div_Gamma X_T=n-1-Hs, hence integration by parts
changes the first term into
 (b/2)integral_Gamma [X_T.grad_Gamma H+(n-1)H-H^2s]u^2
 -(b/2)integral_boundaryGamma H u^2 X_T.eta.
Combining the H terms uses n-1-2a=1. The divergence theorem now gives the
stated identity, including its edge sign.

No sign is asserted for the right side. Establishing the sharp asymptotic
sign under boundary blow-up is precisely an unresolved step in this team's
attempt at the requested dimension theorem.

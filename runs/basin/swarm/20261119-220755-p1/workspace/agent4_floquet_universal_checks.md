# Universal Floquet checks for the logtime blowup field

Let F=E+V, where E=(0,w,2Z) is the weighted Euler vector field and V is the
homogeneous physical-time blowup field. V has weighted degree +1, so
[E,V]=V (bracket convention [X,Y]=DY*X-DX*Y). Along any F-flow orbit,

    d/dt V(gamma(t)) = DF(gamma(t))*V(gamma(t))+V(gamma(t)).

Therefore exp(-t)*V(gamma(t)) is a variational solution. A nonconstant periodic
orbit has the exact multipliers 1 (tangent) and exp(-T). These two variational
solutions are independent: if V and F are collinear all along the orbit, then
E is collinear with F, hence the h coordinate is constant and Z,w move along
a positive scaling ray, which cannot make a nonconstant closed orbit.

For t=1 base m=s+2, the exact invariant density for the logtime vector field is

    sigma(h,w,Z)=constant*abs(f(theta)/P_m(theta))/prod(Z_i), theta=-h,

and its divergence is

    div(F)+grad(log sigma) dot F = s.

One derivation uses the exact two-block map's projective logweight Jacobian 1.
The coordinate map base logweights -> (h,u) has determinant proportional to

    Res(H,f_u) / [prod_i H(lambda_i)*f_u(lambda_i)] .

At u=0, all f_u(lambda_i) are constant, Res(x-theta,f)=f(theta), so the
limiting density in (h,w,Z) after u=epsilon*w, z=epsilon^2*Z is
constant*epsilon^s*abs(f(theta)/P_m(theta))/prod(Z_i). Since
 epsilon_next=epsilon/(1+epsilon), invariance of exact-map volume gives the
above density divergence after dividing by epsilon and passing to epsilon=0.
Equivalently this identity is checked directly by differentiating the finite
rational blowup formula.

Liouville's formula on a period, with periodic density cancelling, gives

    determinant(Monodromy)=exp(s*T).

After removing the tangent multiplier 1 and homogeneous-time multiplier
exp(-T), the remaining d-2 multipliers have product exp((s+1)*T).

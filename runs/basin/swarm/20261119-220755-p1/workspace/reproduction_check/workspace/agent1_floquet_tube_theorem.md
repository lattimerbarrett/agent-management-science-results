# Explicit Floquet-tube existence certificate

Let G be C2 autonomous on R^(d+1). Let gamma(s), P(s) be periodic, piecewise C2/C1 respectively, P invertible; piecewise smoothness with finitely many knots suffices. Fix D=diag(0,Dn), with Dn real block diagonal, each block either a nonzero real scalar or [[u,-v],[v,u]] with u nonzero. Use the maximum of scalar absolute values and Euclidean norms of the 2D blocks, including the scalar phase block. Then exp(t Dn) on stable/unstable blocks has exact exponential rate, and the whole-line/periodic Green operator for d/ds-Dn has norm at most 1/alpha, alpha=min |Re spec Dn|.

Define
 a=P^-1 gamma', B=P^-1 P', d=P^-1(G(gamma)-gamma'),
 E=P^-1(DG(gamma) P-P')-D.
All bounds below are in the indicated block norm and its induced multilinear norms, on every s in [0,1]. Suppose
 ||d||<=delta, ||E[:,normal]||<=e, a_0>=astar>0, ||a_normal||<=anorm,
 ||B[:,normal]||<=b, ||Dn||<=dmax,
and ||P^-1 D2G(gamma+P(0,eta))[P(0,u),P(0,v)]||<=H||u||||v|| for ||eta||<=rho.

Set
 r=delta+e*rho+H*rho^2/2,
 qbar=r/(astar-b*rho),
 qLip=(e+H*rho+b*qbar)/(astar-b*rho),
 Nbar=r+(anorm+(b+dmax)*rho)*qbar,
 fbar=Nbar/(1-qbar),
 LipN=e+H*rho+(b+dmax)*qbar+(anorm+(b+dmax)*rho)*qLip,
 Lipf=LipN/(1-qbar)+Nbar*qLip/(1-qbar)^2.

**Certificate inequalities:**
 b*rho<astar, qbar<1, fbar<alpha*rho, Lipf<alpha.
Then G has a periodic orbit entirely in the tube gamma(s)+P(s)(0,eta), ||eta||<rho. It has exactly the one neutral multiplier associated to phase; all normal multipliers are off the unit circle. If the theta-component range of gamma exceeds twice rho*sup ||theta-row(P_normal)||, theta on this orbit is nonconstant.

## Proof, including phase correction
Write x=gamma(s)+P(s)v with v=(0,eta), and let dot denote physical G-time. Taylor's theorem gives
 vdot+(a+Bv)(sdot-1)=d+(D+E)v+R(s,eta),
 ||R||<=H||eta||^2/2, ||Deta R||<=H||eta||.
The first component imposes sdot=1+q, where
 q=[d0+(Ev)0+R0]/[a0+(Bv)0].
The displayed bounds give |q|<=qbar and ||Deta q||<=qLip. In particular phase is strictly increasing. Dividing normal equation by sdot yields
 deta/ds=Dn eta+f(s,eta),
 f=[dn+(Ev)n+Rn-(an+(Bn+Dn)eta)q]/(1+q).
Here Bn+Dn means B restricted to normal columns/normal output plus Dn. Quotient and product rules give ||f||<=fbar and ||Deta f||<=Lipf as displayed.

On the Banach space of continuous periodic normal functions of norm<=rho, solve eta=Green(f(.,eta)). The map sends the closed ball strictly inside itself and is a strict contraction. Its unique fixed point is piecewise C1. Its image x(s) is an actual smooth G-orbit after the strictly positive time change; period equals integral_0^1 (1+q(s,eta(s)))^-1 ds. Knot regularity causes no issue because x solves the same autonomous ODE on adjacent intervals.

For normal hyperbolicity, the variational equation in the phase coordinate has the form z'=(Dn+Delta(s))z with ||Delta||<=Lipf<alpha. For any 0<beta<alpha-Lipf, the stable-past/unstable-future Green operator in the exponentially beta-weighted norm has norm <=1/(alpha-beta), so perturbation by Delta is a contraction. This constructs an exponential dichotomy, hence excludes all unit-circle normal multipliers. Phase contributes exactly one neutral multiplier. Positive time changes preserve the normal return map.

## Convenient exact tangent column
Taking P[:,0]=gamma' makes a=e0 exactly, so astar=1 and anorm=0. Gamma can be C2 periodic Hermite/quintic and P can have this exact polynomial derivative as its first column. If instead a is merely close to e0, use the general bounds above.

## Converting coordinate infinity bounds
For one real 2D rotational Floquet block, ||z||_infty<=||z||_block<=sqrt(2)||z||_infty. Thus safe block bounds for vectors, operators, and the stated Hessian are sqrt(2) times their coordinate-infinity bounds (inputs of block norm<=1 have coordinate-infinity norm<=1). The scalar a0 lower bound is unchanged. Bounds on dmax can be computed directly blockwise: |lambda| for real blocks and sqrt(u^2+v^2) for rotational blocks.

# Explicit pseudoconvex worm geometry (no non-Oka claim)
Fix mu>0. Put t=log|w|² and eta(t)=0 for |t|<=mu, eta(t)=exp(8-1/(|t|-mu)) otherwise. Define Omega={w!=0: |z-exp(it)|² < 1-eta(t)}.

The cutoff is C-infinity and flat where it first becomes positive. Its relevant range eta<=1 occurs for |t|<=mu+1/8, so Omega is bounded and its closure avoids w=0. Its base is an annulus and its nonempty fibers are discs with continuous centers and radii. Thus Omega is connected and nonempty. Every boundary point is a limit of fiber interiors, including collapsed end fibers, so K=closure(Omega) is the displayed closed sublevel.

For rho=|z|²-2 Re(z exp(-it))+eta(t), the only way its z gradient can vanish is z=exp(it). On rho=0 this forces eta=1, where eta'(t) has absolute value 64. Hence d rho never vanishes on the boundary, which is C-infinity.

Write z exp(-it)=x+iy, h=eta(t), p=eta'(t), q=eta''(t). On the boundary (x-1)²+y²=1-h; hence x>=0 and 0<=h<=1. The Levi form on the standard nonzero tangent vector (rho_w,-rho_z), multiplied by |w|², is L=p²-2py+(2x+q)(1-h). The script differentiates rho and checks this identity.

For h=0, p=q=0 and L=2x>=0. For 0<h<=1/3, set a=|t|-mu, so 0<a<=1/8, p²=h²/a^4 and q=h(1-2a)/a^4. Consequently q/p²>=(3/4)/h>=h/(1-h)². The last inequality follows from 3(1-h)²-4h²>=8/9 on [0,1/3]. The exact boundary identity
L=(1-h)(y-p/(1-h))²+(1-h)x²+h(1-h)+(1-h)q-hp²/(1-h)
proves L>=0. For 1/3<=h<=1, q>=1024>1, and L=(p-y)²+(2x+q)(1-h)-y²>=0, because y²<=1-h. Thus the boundary is pseudoconvex with the problem's orientation.

These geometric calculations are verified in agent2_worm_geometry.py. There is presently NO proof here that this domain has non-Oka complement.

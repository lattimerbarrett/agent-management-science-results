# Quadratic-polynomial coordinates for s=3 edge flight and pulses
Let f,g be monic cubics, fg-N=P5(x)(x-c), H=x-theta, with f(theta),g(theta)<0 on the hard gap. Define
 ell_w=rem_f[(x-c)g(x)w(x)]=ell0+ell1*x+C*x^2,
 q_w=rem_f[(x-theta)ell_w]=rem_f[(x-theta)(x-c)g(x)w(x)].
Then
 q_w(x)=A*x^2+(B-theta*A)*x+(sqrt(fg(theta))*K-theta*B),
 A=ell1-(f2+theta)C,
 B=ell0-(f1+f2*theta+theta^2)C,
 K=C/sqrt(g(theta)/f(theta)).
In particular q_w(theta)=-f(theta)C=sqrt(fg(theta))*K.

For any negative mode z, put alpha_z=f(z)^2/N and Q_z(x)=(f(x)+alpha_z*g(x))/(x-z), a quadratic. The numerator vanishes at z because f(z)g(z)=-N.
In the f-root coordinates zeta_j, the exact Gaussian representation gives
 F_z(zeta_j)=-4f(z)^2/[(z-zeta_j)(zeta_j-c)(zeta_j-theta)].
Therefore q_(F_z)(zeta_j)=4f(z)^2*g(zeta_j)/(zeta_j-z)=4N Q_z(zeta_j).
Both sides are quadratics, so q_(F_z)=4N Q_z EXACTLY, for every theta (not only at the walls). The force directions in q-space are constant.
At a wall theta=e, the growth covector is
 L_z(w)=-4q_w(z)/[N(z-c)(z-e)].
Consequently the complete one-charge wall pulse acts as the endpoint-independent reflection
 q -> q-2 Q_z*q(z)/Q_z(z).

## Exact intrinsic connection
In f-root coordinates the intrinsic flight has
 dw(zeta_j)/dtheta=-f(theta)*C/[2g(theta)(zeta_j-c)(zeta_j-theta)^2].
Differentiating q_w(zeta_j) and using q(theta)=-f(theta)C gives the polynomial identity
 partial_theta q(x)=-(q(x)-q(theta))/(x-theta)
 +(q(theta)/2)*[(f(x)-f(theta))/((x-theta)f(theta))
             +(g(x)-g(theta))/((x-theta)g(theta))].
Its evaluation at x=theta shows q(theta)/sqrt(fg(theta))=K is constant.
For every fixed z, the connection also gives
 d/dtheta[q(z)/(z-theta)]
 =q(theta)/(2(z-theta)^2)*[f(z)/f(theta)+g(z)/g(theta)].
For a negative mode z and u=sqrt(g(theta)/f(theta))>0 this is
 =-K*f(z)/2 *[u-N/(f(z)^2*u)]/(z-theta)^2.
This recovers the two-Cauchy-integral formulas for the transported growth rows.

These identities are rigorous structural reductions only: they do not yet prove the required cooperative-kernel k<1 bound.

## Modified charge identity throughout the gap
The exact homogeneous negative-mode growth is
 ell_z=-4q_w(z)/[N(z-c)(z-theta)]-thetadot/(z-theta).
To verify, use the interpolation expansion of gw+f dg-A, substitute Ctop=-(B+cA)/N-thetadot/2, and fg(theta)=N+P5(theta)(theta-c). All remaining terms proportional to C combine to -thetadot/(z-theta). Thus the positive modified weight p_z/abs(z-theta) has logarithmic growth -4q_w(z)/[N(z-c)(z-theta)], equal to the wall formula but valid throughout the gap. This identity by itself does not prove a monotonicity sign for the far probe; the geometric correction between ell_z and modified growth must not be dropped.

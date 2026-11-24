# Exact scalar-dual s=3 canonical flight and wall formulas
Let f,g be monic cubics with f g-N=P5(x)(x-c), N>0; the hard dual gap is a<theta<b with c<a, ftheta,gtheta<0. All polynomials below are in ASCENDING coefficient convention only in code; f2 denotes the x^2 coefficient. Let Mtheta,Mptheta be base moment Gram matrices, w degree<=2, dg=-Mp^-1 M w, A=delta N, and btheta w=thetadot.

Define the FIXED linear coefficient map
 ell_w(x)=rem_f[(x-c)g(x)w(x)]=ell0+ell1*x+C*x^2.
Set R(theta)=gtheta/ftheta>0 and
 A=ell1-(f2+theta)C,
 B=ell0-(f1+f2*theta+theta^2)C,
 K=C/sqrt(R(theta)).
The displayed A is exactly the norm derivative (same symbol on purpose).

## Derivation of the fixed coefficient map
The first-order product polynomial q=gw+f*dg-A has degree<=5 and values q(lambda_i)=-N*thetadot/[2(lambda_i-theta)] on the five base nodes. Hence
 q(x)=Ctop*P5(x)-(N*thetadot/2)*[1-P5(x)/P5(theta)]/(x-theta).
At any f-root zeta, use P5(zeta)=-N/(zeta-c) and fg=N+P5(x)(x-c). Multiplying q(zeta)+A=g(zeta)w(zeta) by zeta-c gives
 ell_w(x)=A(x-c)-N*Ctop-N*thetadot/2+C*(f(x)-ftheta)/(x-theta),
 where comparing leading coefficients yields C=N*thetadot*gtheta/[2P5(theta)]. The polynomial identity is exact, not just modulo f, as both sides have degree<=2. Comparing coefficients gives A,B above and
 Ctop=-(B+cA)/N-thetadot/2.
In particular thetadot=2P5(theta)C/[N*gtheta].


## Resource and individual growth identity
Write v=thetadot and define

 I=-(c*A+B)+sqrt(f(theta)*g(theta))*K/(theta-c).

Since f,g<0 on the theta gap and K=C/sqrt(g/f), this equals

 I=N*Ctop-N^2*v/[2*P5(theta)*(theta-c)].

All expressions have continuous endpoint extensions because v is divisible
by P5(theta). For a negative-level node z, P5(z)*(z-c)=-2N, and

 ell_z=2*(w(z)/f(z)+dg(z)/g(z))-2*A/N=-2*q(z)/N-4*A/N.

Substitution of the displayed interpolation formula for q gives exactly

 ell_z=-4*A/N+4*I/[N*(z-c)]
        +v*(f(theta)*g(theta)+N)/[P5(theta)*(theta-c)*(z-theta)].

This is a linear identity in w and therefore needs no invertibility of
the coefficient map w -> (A,B,K). In particular common roots of f,g cause
no problem. All denominator factors used here are nonzero on the base
chart, except the explicitly cancelled endpoint factor P5(theta).

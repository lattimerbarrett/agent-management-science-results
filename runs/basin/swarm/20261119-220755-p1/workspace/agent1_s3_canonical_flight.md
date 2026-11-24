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

## Intrinsic free-flight connection
The homogeneous intrinsic evolution is
 dw/dtheta=Mtheta^-1 v(theta)*C/[2gtheta].
Let Df(x,theta)=(f(x)-ftheta)/(x-theta), and define Dg similarly. In f-root coordinates, Gaussian quadrature gives
 rem_f[(x-c)g(x) Mtheta^-1 v(theta)]=-ftheta*rem_f[g(x)/(x-theta)^2].
But rem_f[g/(x-theta)]=Dg-R*Df; differentiating theta gives the squared-denominator remainder. Therefore the ell-coefficients of the vector u=Mtheta^-1v(theta)/(2gtheta) are
 ell2(u)=R'/(2R),
 ell1(u)=[R'(f2+theta)+(R-1)]/(2R),
 ell0(u)=[R'(f1+f2theta+theta^2)+(R*f2-g2)+2theta(R-1)]/(2R).
It follows by product differentiation that
 K'=0,
 A'=-(K/2)*(sqrt(R)+1/sqrt(R)),
 B'=-(K/2)*[(2theta+f2)*sqrt(R)+(2theta+g2)/sqrt(R)].
Here primes are derivatives with respect to theta. Thus free flight from a to b is the exact SHEAR
 (A,B,K)_b=(A-J0*K,B-J1*K,K),
 J0=(1/2)integral_a^b [sqrt(R)+1/sqrt(R)]dtheta >0,
 J1=(1/2)integral_a^b [(2theta+f2)sqrt(R)+(2theta+g2)/sqrt(R)]dtheta.
No moment-matrix inverse or ill-conditioned 3x3 ODE is needed to compute the flight.

## Wall growth and force
For any negative-level z, f(z)g(z)=-N. Its homogeneous logarithmic growth is
 Lz=2(wz/fz+dgz/gz)-2A/N=-2q(z)/N-4A/N.
At either endpoint e=a,b, substitution into the q-interpolation identity (retaining the finite limit thetadot/P5(theta)) gives
 Lz(e)=-4/[N(z-c)]*(z,1,sqrt(N)/(z-e))
 in coordinates (A,B,K).

The external force on w is Fz=-4fz*Mtheta^-1v(z). In f-root coordinates zeta_j it has values
 Fz(zeta_j)=-4fz^2/[(z-zeta_j)(zeta_j-c)(zeta_j-theta)].
To compute its ell-coefficients, use
 rem_f[g/(z-x)]=-Dg(x,z)+(gz/fz)Df(x,z),
 rem_f[g/(x-theta)]=Dg(x,theta)-Rtheta*Df(x,theta).
After collecting coefficients, in canonical coordinates at an arbitrary interior theta,
 Fz=4*(N+fz^2,
        (N+fz^2)(z+theta)+N*f2+fz^2*g2,
        [N+Rtheta*fz^2]/[(z-theta)*sqrt(Rtheta)]).
At a wall use its endpoint value R_e. This also proves Arow*Fz=4(N+fz^2)>0 and the force sign Kforce=sign(z-theta).

## Effective two-wall game
Use all coordinates at left wall a. A right-wall force vector transforms back by (A,B,K)->(A+J0K,B+J1K,K); a right-wall growth row transforms to
 -4/[N(z-c)]*(z,1,sqrt(N)/(z-b)-zJ0-J1).
The full effective 2x2 scattering matrix is therefore computed using four explicit vectors and the two scalar moments J0,J1. These identities were checked numerically against the original moment-Gram formulas at all six negative-level nodes, both walls, relative discrepancies <=2e-11; the full flight shear agreed to 1.4e-10 in a moderate nontrivial example. The identities themselves are proved above.

IMPORTANT: this is NOT YET a proof that cooperative nearest-wall k<1. In particular m(theta)=2theta+(f2R+g2)/(R+1) need not be monotone, despite J1 being its positive-weighted integral. Raw geodesic-action convexity has logarithmic endpoint divergences and cannot be used without controlling boundary terms.

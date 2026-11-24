# Fully explicit strongly pseudoconvex Rudin-Klein-bottle neighborhood

This is candidate geometry and a rational-hull pocket, NOT a proved non-Oka example.

On z!=0, set r=sqrt(|z|), c=r-2, u=|w|^2/|z|, v=Re(w^2/z), b=Im(w^2/z), and

    R(z,w) = [ (u+v)/2 + c^2-1 ]^2
             +(1/2+2c^2)u+(-1/2+2c^2)v-2cb.

Although the final three terms need not visibly look nonnegative, in holomorphic double-cover coordinates z=s^2,w=s q (s!=0), writing x=Re q,y=Im q, this is

    F1=c^2+x^2-1,  F2=y-2cx,  c=|s|-2,
    R=F1^2+F2^2.

Under (s,q)->(-s,-q), F1 is fixed and F2 changes sign. Therefore R is invariant and is a well-defined smooth real function on z!=0. Its zero set is precisely Rudin's Klein bottle M (agent2's parametrization/proof).

Define epsilon=1/16384, Omega={z!=0:R(z,w)<epsilon}, and K={z!=0:R(z,w)<=epsilon}.

BOUNDEDNESS. On R<=1/16, |F1|,|F2|<=1/4, so c^2+x^2<=5/4. Hence 1/2<|s|<7/2 and |x|<3/2. Also |y|<=1/4+2|cx|<19/4, whence |q|<5. Thus |z| is bounded above and bounded away from0 and |w|<35/2. The displayed K is consequently compact in C^2.

EXPLICIT LEVI POSITIVITY. In the (s,q) coordinates let J=(partial F_i/partial z_j), z_j=(s,q). It is

    J=[[c exp(-i theta), x],[-x exp(-i theta),-c-i/2]],

where s=|s| exp(i theta). Writing f=F1, one has

    |det J|^2=4[c^2-(15+16f)/32]^2+(31+32f)/256 >=23/256

on R<=1/16, while tr(J*J)<=11/4. Thus the least eigenvalue of 2J*J is at least23/352. The Levi matrices of F1 and F2 are

    H1=diag(1-1/r,1/2),
    H2=[[-x/(2r),-exp(-i theta)/2],[-exp(i theta)/2,0]],

whose operator norms there are <=1 and <=2 respectively. The product rule therefore gives

    H_R=2 J^T conjugate(J)+2F1 H1+2F2 H2
       >= [23/352-2 sqrt(5) sqrt(R)] I.

On R<=epsilon, the lower bound is 23/352-sqrt(5)/64>0. Thus R is strictly plurisubharmonic throughout a neighborhood of K, since strict positivity persists slightly beyond its compact sublevel.

REGULARITY. The same determinant bound makes dF1,dF2 linearly independent over R throughout R<=1/16. Therefore dR=2F1 dF1+2F2 dF2 can vanish there only when F1=F2=0. Since epsilon>0, dR!=0 on its level epsilon. The domain has smooth strongly pseudoconvex boundary and K=closure(Omega).

CONNECTEDNESS. Each component of Omega has compact closure. Its minimum of R is attained in its interior, since R=epsilon on the boundary, and must be critical, hence must lie in M. But the connected set M lies in a single component of Omega, so all components coincide.

EXCLUDED HULL POINT. At p=(4,0), r=2,q=0,c=0, so R(p)=1>epsilon. On the other hand p belongs to the rational hull of M by agent2's argument principle. Since Omega is an open neighborhood of compact M, it contains all sufficiently small translates M+a. Translation equivariance and monotonicity of rational hulls give a whole open neighborhood of p inside r(K), disjoint from K after shrinking that neighborhood.

Every algebraic identity and the explicit positive Levi lower bound were verified with SymPy in agent1_rudin_explicit_tube_checks.py. No theorem turning the rational-hull pocket into failure of CAP has been verified, so K is only a candidate for claim2.

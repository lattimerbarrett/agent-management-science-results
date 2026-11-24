# Nondegenerate entire maps can meet a compact rational hull while omitting the compact set

Use the explicit smooth pseudoconvex worm K from agent3_worm_geometry.md. Its support in log|w| lies in a finite interval [a,b]. The point p=(1,exp(pi/2)) is outside K but in its rational hull.

Let H(z,w)=(w/10,z/10+10w^2), and let Psi=(f,g):C^2 -> Omega be a parametrization of its attracting basin. The escape cone gives |g|<=max(|f|,2) everywhere. The bidisc of radius 1/100 lies in the basin, so arrange Psi(0)=(0,r), r=1/200, by source translation.

Choose B>=max(|a-pi/2|,|b-pi/2|), epsilon in (0,1), and lambda>0 so
1+epsilon*r^2-(1+epsilon)*lambda^2*B^2-4*epsilon>0.
Define
u=pi/2+f/lambda,
delta=1+epsilon*r^2-f^2-epsilon*g^2.
Whenever Re u lies in [a,b], writing f=X+iY yields
Re delta >= 1+epsilon*r^2-(1+epsilon)*X^2+(1-epsilon)*Y^2-4epsilon >0.
Therefore (u,delta) lies in D={Re u<a or Re u>b or Re delta>0}. The Jacobian determinant with respect to (f,g) is -2epsilon*g/lambda, nonzero at 0.

Now G(u,delta)=(-delta*exp(2iu),exp(u)) maps D into C^2 minus K: outside [a,b], w is outside K's support; inside, if t=Im u, then the worm defining function is
|delta|^2 exp(-4t)+2 Re(delta) exp(-2t)+eta(2 Re u)>0.
G is everywhere locally biholomorphic. At (u,delta)=(pi/2,1) its value is p.

Consequently G(u,delta):C^2 -> C^2 minus K is entire, nondegenerate at 0, and passes through p in rational hull(K) minus K. Thus nondegenerate-entire-map avoidance does NOT imply rational-hull avoidance, even for smooth pseudoconvex compact K in C^2.

This does NOT prove the worm complement is Oka, nor that it is strongly dominable at every point, and does not settle S or N.

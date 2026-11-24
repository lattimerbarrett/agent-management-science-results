# Verified generalized-worm geometry (not an Oka obstruction)

Fix mu>0. Let h(s)=0 for s<=0 and h(s)=integral_0^s exp(-1/u)du for s>0, and put eta(t)=h(t-mu)+h(-t-mu). Then eta is smooth, convex and nonnegative, eta=0 exactly on [-mu,mu], eta tends to infinity at both ends, and eta' is nonzero where eta=1. Smoothness follows because exp(-1/s) and every derivative tend to zero at 0+. For s>0, h'=exp(-1/s)>0 and h''=exp(-1/s)/s^2>0.

In C^n with coordinates (z,w,zeta), w!=0, define
rho=|z-exp(i t)|^2+||zeta||^2-1+eta(t), t=log|w|^2.
Let Omega={rho<0} and K={rho<=0}. Its projection to w is the annulus eta(log|w|^2)<1; each fiber is a ball in C^(n-1) of radius sqrt(1-eta), centered at (exp(i t),0). The base and fibers are connected, and the centers give a continuous section, proving connectedness. The base is bounded and bounded away from w=0; the fiber radius is at most 1 and its center has norm 1. Thus Omega is bounded, nonempty, and its closure lies in w!=0.

Boundary regularity: if rho_z and all rho_zeta vanish, then z=exp(i t), zeta=0. On rho=0 this gives eta(t)=1. At such a point rho_w=eta'(t)/w !=0. Thus d rho!=0 everywhere on rho=0. Therefore K=closure(Omega) has smooth boundary and belongs to K_n.

For Levi positivity put xi=z exp(-i t)=x+i y, A=exp(-i t)v_z, B=v_w/w and C=v_zeta. Write d=eta'-2y. Tangency means (bar(xi)-1)A+bar(zeta).C=-d B. The Levi form is
L=|A-i B|^2+||C||^2+(2x+eta''-1)|B|^2.
The vector ell=(bar(xi)-1,bar(zeta)) has norm squared R=1-eta on the boundary. For U=(A-i B,C), tangency gives ell.U=-(eta'-y+i(x-1))B. If R>0, Cauchy-Schwarz gives
R L >= N |B|^2,
N=(eta'-y)^2+(x-eta)^2+eta(1-eta)+eta''(1-eta)>=0.
If B=0 directly L=|A|^2+||C||^2>=0. If R=0, then xi=1,zeta=0, eta=1, and eta'!=0 forces B=0 by tangency. Thus all boundary Levi forms are nonnegative in the stated orientation.

The boundary is strictly pseudoconvex except on A={z=0,zeta=0, |log|w|^2|<=mu}. Indeed N>0 for 0<eta<1, eta=1 was handled separately, and when eta=0 its derivatives vanish and N=|xi|^2. Vanishing N then implies xi=0 and zeta=0. At A the Levi null space is exactly the w-direction.

For mu>pi, one can prove failure of a Stein neighborhood basis directly (agent4's moving-annulus argument). Let r=exp(-pi/2), R=exp(pi/2). Both boundary circles at w-moduli r,R have t=+-pi and hence fiber center exp(i t)=-1. Thus for every z in D(-1,1), both circles (z,w,0) lie in Omega. Meanwhile the full compact annulus A_0={(0,w,0):r<=|w|<=R} lies in K, since eta=0 and rho=0 there. Every neighborhood U of K therefore contains A_z for z sufficiently close to 0. Choose a negative real such z_0 in D(-1,1), and move z continuously along the segment to -1/2. The boundaries of all A_z remain in K, while the entire moving family remains in a fixed compact ambient set. If U is Stein, take a proper continuous psh exhaustion phi of U. Its supremum on K is finite. On every A_z already contained in U, the subharmonic maximum principle bounds phi by this same supremum. The set of parameters for which A_z is contained in U is open and closed: closedness follows because all A_z then lie in a single compact sublevel of phi. Hence the endpoint annulus also lies in U. In particular p=(-1/2,1,0) belongs to every Stein neighborhood U of K. But rho(p)=|-1/2-1|^2-1=5/4>0, so p is outside K. This proves that K has no Stein neighborhood basis, in every dimension.

IMPORTANT: No assertion that these complements are non-Oka has been established here. The missing bridge cannot be inferred from these Levi computations.

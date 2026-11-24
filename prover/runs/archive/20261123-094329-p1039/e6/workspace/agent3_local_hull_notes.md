# Smooth pseudoconvexity versus local polynomial convexity

This note establishes a geometric reduction, not the requested Oka theorem.

## Forward direction (using Docquier--Grauert)
Let K be the closure of a bounded smooth domain with Levi-pseudoconvex boundary.
The Levi problem implies that its interior is Stein. At a boundary point, choose
coordinates (xi,x_n) in R^(2n-1) x R with K locally given by x_n <= h(xi),
h(0)=0 and Dh(0)=0. Choose a small r>0 such that |h(xi)|<r on |xi|<=2r,
and all points z-t e_n with z in B_(2r), 0<=t<=4r, lie in the graph chart.
Define
    D_t = (int(K)+t e_n) intersect B_(2r).
These are Stein domains, increasing continuously with t, and D_(4r)=B_(2r).
They satisfy the semicontinuous holomorphic-extension hypotheses of the
Docquier--Grauert Runge-pair theorem. Hence each D_t is Runge in B_(2r).
For L=K intersect closed B_r and t>0, L is compactly contained in D_t.
Since B_(2r) is Runge in C^n, the polynomial hull of L lies in every D_t.
It also lies in closed B_r. Intersecting over t>0 yields hull(L) subset L.
Thus K is locally polynomially convex.

## Reverse direction (explicit analytic disc)
If the boundary has a negative Levi direction, a local holomorphic coordinate
change and multiplication of a defining function by a positive smooth factor give
    rho(z)=Re(z_n)-mu*|z_1|^2+R(z),  mu>0,
along the complex two-plane in question, with |R(z)|<=C*||z||^3.
Pure holomorphic quadratic terms are absorbed in z_n, and quadratic terms
involving the real normal are removed by the positive smooth factor. After
restricting to the selected tangential direction, the remaining tangential
Levi terms vanish. Equivalently one can retain normal quadratic terms and
absorb their O(a^3) contribution in the disc remainder bound below.
For sufficiently small a>0, take
    phi(zeta)=(a*zeta,0,...,0,mu*a^2/2), |zeta|<=1.
Choose mu*a<=1 and 27*C*a<=mu. Then ||phi||<=3a/2 and |R(phi)|<=mu*a^2/8.
Consequently rho(phi(zeta))<=-3*mu*a^2/8 on |zeta|=1, whereas
rho(phi(0))>=3*mu*a^2/8>0. The circle lies in K and the center outside K.
For every polynomial P, the maximum principle applied to P composed with phi
places phi(0) in the polynomial hull of the boundary circle. Therefore K is
not locally polynomially convex.

The exact bounds were checked in workspace/agent3_disc_check.py.

## Missing step, stated explicitly
To conclude the user's theorem from this reduction one would need a verified
Oka-complement criterion for compact sets in terms of local polynomial convexity,
or an appropriate restricted version for regular smooth compact domains.
No such theorem/proof/source has yet been established by this team. Merely
naming that criterion would not constitute a proof of the requested result.

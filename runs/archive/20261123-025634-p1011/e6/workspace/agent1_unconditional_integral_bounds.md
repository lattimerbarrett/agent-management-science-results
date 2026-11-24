# Unconditional weighted integral and source-Morrey bounds

Let (M,g) be one fixed compact connected smooth positive-Yamabe background as
in the question (LCF is not needed here). Write kappa=n(n-2),
p=(n+2)/(n-2). Let phi>0 be its first Robin eigenfunction, normalized by
int_M phi=1, with eigenvalue lambda1>0.

For every smooth positive solution u, Green's identity and the common Robin
condition imply

 kappa int_M phi u^p=lambda1 int_M phi u.

Indeed the boundary skew term u d_nu phi-phi d_nu u vanishes pointwise, since
both functions have normal derivative -2c_n H times their boundary value.
Writing A=int phi u and T=int phi u^p, Jensen gives T>=A^p. Since A>0,

 A<=(lambda1/kappa)^(1/(p-1)),
 T<=(lambda1/kappa)^(p/(p-1)).

The positive smooth phi has a positive minimum on the compact closure, so
this gives uniform unweighted L1 and Lp bounds, independent of the solution.
No critical L^(p+1) energy bound is asserted.

There is also an elementary uniform source Morrey bound

 int_(B_r(q) cap M) u^p <= C r^(2/p)

for all sufficiently small r>0 and q in the compact closure. To prove this,
use the positive Green kernel G for -L_g with B_g=0. Its positivity follows
from lambda1>0, and its standard local Robin parametrix gives, uniformly near
the diagonal including the smooth boundary,

 G(x,y)>=c dist(x,y)^(2-n).

The boundary leading term is the positive Neumann image parametrix; the
smooth Robin coefficient is lower order. The Green representation is
u(x)=kappa int_M G(x,y)u(y)^p dy. Put
M_r=int_(B_r(q) cap M)u^p. For x in
A_r=(B_(4r)(q) minus B_(2r)(q)) cap M and y in B_r(q), dist(x,y)<=5r,
so u(x)>=c M_r r^(2-n). Smooth compact boundary geometry gives |A_r|>=c r^n.
Consequently the already proved global Lp bound yields

 C>=int_(A_r)u^p>=c M_r^p r^(n+(2-n)p)=c M_r^p r^(-2),

which proves the claim. In particular no weak measure limit of u_i^p dV can
have an atom, even at a boundary point.

These are unconditional estimates but do NOT imply the desired compactness:
a critical bubble has vanishing source Lp mass, and its critical L^(p+1)
energy may concentrate. They do not provide isolated-simple extraction.


## Stronger scale-invariant source Morrey bound
The annulus proof in fact gives

 M_q(r)^p <= C r^2 M_q(4r),
 M_q(r)=int_(B_r(q) cap M)u^p,

because the annulus integral is at most M_q(4r), not merely the global bound.
Set a=2/(p-1)=(n-2)/2 and F_q(r)=r^(-a)M_q(r). Since ap=a+2, this becomes

 F_q(r)^p <= C 4^a F_q(4r).

Iterate until 4^j r lies in [r0/4,r0], where the global integral bound gives
F_q(4^j r)<=B uniformly in q,u. With C0=C4^a,

 F_q(r) <= C0^((1-p^(-j))/(p-1)) B^(p^(-j))
         <= max(1,C0^(1/(p-1))) max(1,B).

Therefore every solution satisfies the sharper uniform estimate

 int_(B_r(q) cap M) u^p <= C r^((n-2)/2).

This is consistent with a standard boundary or interior bubble, which has
source mass of precisely that order at its own scale. It still gives neither
a bound for int u^(p+1) nor compactness. It is an unconditional scale-invariant
concentration estimate on the source, useful as blow-up-analysis infrastructure.

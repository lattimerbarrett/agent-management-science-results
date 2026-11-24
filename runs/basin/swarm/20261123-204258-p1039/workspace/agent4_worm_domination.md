# Explicit entire domination of a rational-hull point of the worm
Let the worm be K={rho<=0}, rho=|z|^2-2Re(z exp(-it))+eta(t), t=log|w|^2,
with eta>=0 and eta(t)>1 outside a bounded interval [2a,2b].
Use a Hénon basin parametrization Psi=(f,g):C^2 -> Omega, Psi(0)=0, with
|g|<=max(|f|,2). Its existence and invertible derivative are proved in the shared basin notes.

Set u0=pi/2, A=max(|a|,|b|), B=exp(A^2)*(A+u0+3), c=1/(4B),
U=u0+f, Delta=1+c exp(U^2)g.
If a<=Re U<=b, writing U=X+iY gives
|exp(U^2)g| <= exp(A^2) exp(-Y^2)*(A+u0+2+|Y|) <= B,
since exp(-Y^2)<=1 and |Y| exp(-Y^2)<=1.
Thus Re Delta>=3/4 on this strip. Outside this strip eta(2Re U)>1.

Define H=(Z,W)=(-Delta exp(2iU), exp U).
Inside the strip, with t=2Re U,
rho(H)=|Delta|^2 exp(-4Im U)+2Re(Delta)exp(-2Im U)+eta(t)>0.
Outside the strip eta(t)>1 implies rho(H)>0 from the original squared-disc expression.
Hence H is entire with image in C^2 minus K.

At source0, U=pi/2 and Delta=1, so H(0)=(1,exp(pi/2)), the explicit point in
rational hull(K) from agent3_worm_geometry.md.
The map (f,g)->(U,Delta) has Jacobian c exp(U^2), and (U,Delta)->(Z,W)
has Jacobian exp((1+2i)U). Both are everywhere nonzero.
Thus det DH(0)!=0. In fact H is locally biholomorphic everywhere.

This disproves the proposed statement that a nondegenerate entire map omitting compact K
in C^2 must omit the rational hull of K. It DOES NOT prove that the entire worm exterior is Oka.
The Gaussian change-of-coordinate Jacobian and the target point are checked in agent4_levi_certificate.py.

# Explicit smooth compact mixed-Levi hole
For n>=3 split (z,w) in C x C^{n-1} and let
rho=(|z|^2-1)^2+||w||^2-2,
Omega={rho<0}, K={rho<=0}.

Boundedness: |z|^2<=1+sqrt(2), ||w||^2<=2 on K. Nonemptiness: rho(0,0)=-1.
Smooth boundary: partial_z rho=2(|z|^2-1) conjugate(z), partial_w rho=conjugate(w).
A zero gradient requires w=0 and z=0 or |z|=1, where rho=-1 or -2, never0.
Every rho=0 point is a boundary point by regularity, so K=closure(Omega).

Connectedness: K and Omega are star-shaped about0. Put s=|z|^2,t=||w||^2,u=lambda^2 in [0,1]. Then
rho(lambda z,lambda w)=u rho(z,w)+(1-u)rho(0,0)-s^2 u(1-u).
For rho(z,w)<0 the RHS is negative; hence Omega is connected.

Levi matrix (holomorphic coordinates z,w): diag(4|z|^2-2,1,...,1).
If w!=0, choose a nonzero v_w with sum conjugate(w_j)v_j=0 (possible since n-1>=2), and v_z=0.
This vector is complex tangent and its Levi value is ||v_w||^2>0.
If w=0, all pure w directions are tangent and have positive Levi value.
Thus every boundary point has a strictly positive tangential Levi direction.

At q=(z,w)=(0,1,0,...,0), rho=0 and complex tangency is v_{w_1}=0.
The z direction is tangent with Levi value -2, while w_2 is tangent with value+1.
Consequently K is not pseudoconvex in the orientation of the problem.

The code agent4_levi_certificate.py verifies the complex derivatives, tangent identities,
Levi signature, and auxiliary constructions exactly with SymPy.
THIS FILE DOES NOT CLAIM THAT THE COMPLEMENT IS OKA; a global Oka theorem is still needed.

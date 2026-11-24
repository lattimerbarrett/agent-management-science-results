# Verified candidate geometry (Oka complement NOT proved)
For n>=3 write z in C^(n-1), w in C, and let
rho(z,w)=||z||^2+(|w|^2-1)^2-2, Omega={rho<0}, K={rho<=0}.

Put u=||z||^2 and t=|w|^2. On K, u<=2 and t<=1+sqrt(2), so K is compact. The origin has rho=-1. Under real radial scaling by sqrt(lambda), rho becomes lambda*u+(lambda*t-1)^2-2, a convex function of lambda. Its endpoint values on [0,1] are nonpositive, and strictly negative for lambda<1. Thus Omega is star-shaped, nonempty and connected; K=closure(Omega).

The squared real gradient divided by four is u+4t(t-1)^2. This cannot vanish on rho=0: vanishing requires u=0 and t=0 or 1, which give rho=-1 or -2. Hence boundary is C-infinity. In fact, the outward radial derivative on boundary is u+2t(t-1)=1+t^2>0, so K is strictly star-shaped and diffeomorphic to a closed real ball.

The complex Levi matrix is diag(1,...,1,4t-2). At p=((1,0,...,0),0), rho=0 and partial rho/partial w=0. Thus the complex w-direction is tangential, with Levi value -2. Boundary is not pseudoconvex.

At every boundary point, the positive coordinate subspace C^(n-1) x {0} intersects the complex tangent hyperplane in dimension at least n-2. The Levi form there is the standard positive form. Thus K has at least n-2 positive tangential Levi eigenvalues everywhere, and its defining function has at least n-1 positive ambient Levi eigenvalues everywhere.

What is NOT established: C^n minus K is Oka. A full-CAP complement theorem for smooth compact domains with at least n-2 positive tangential Levi eigenvalues, in dimension n>=3, would imply it immediately. No such theorem is asserted here without proof/source.

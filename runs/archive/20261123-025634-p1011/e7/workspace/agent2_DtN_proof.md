# Exact hemisphere Neumann-to-Dirichlet operator

Let S^n_+ have unit round metric and let theta range from its north pole (0) to equator (pi/2). Write boundary data in equatorial spherical harmonics Y_l, with -Delta Y_l=l(l+n-2)Y_l. Solve (Delta+n)v=0, partial_nu v=g, orthogonally to the Neumann kernel spanned by the n equatorial coordinate functions. Solvability requires g_1=0.

For l>=2, set a=(l-1)/2, b=(l+n)/2, c=l+n/2. The regular radial solution is y_l(theta)=sin(theta)^l 2F1(a,b;c;sin(theta)^2). Substitution reduces the Jacobi ODE to the Gauss equation; the symbolic identity is checked in agent2_hemisphere_DtN_checks.py. The second radial solution is singular at theta=0, so regularity selects y_l up to scale.

Since c-a-b=1/2, the Gauss connection formula at z=1 gives y_l=A_l+B_l cos(theta)+O(cos(theta)^2), where
A_l=Gamma(c)sqrt(pi)/(Gamma(c-a)Gamma(c-b)),
B_l=-2sqrt(pi)Gamma(c)/(Gamma(a)Gamma(b)).
The outward derivative is therefore -B_l and the Dirichlet-to-Neumann multiplier is
kappa_l=2 Gamma((l+n+1)/2) Gamma(l/2) / (Gamma((l-1)/2) Gamma((l+n)/2)) > 0.
Thus the Neumann-to-Dirichlet trace is g_l/kappa_l for l>=2. For l=0, v=-g_0 cos(theta), so its trace is zero. For l=1, sin(theta)Y_1 is precisely the Neumann kernel, removed by the orthogonality choice. These formulas plus kappa_l~l yield the operator on smooth data by spherical harmonic convergence.

# Cubic Euclidean graphs and the threshold seven

Use stereographic equatorial coordinates x=y'/(1-y_n). A cubic harmonic Euclidean graph H_3(x) transforms under its normal displacement factor to F(y)=H_3(y')/(1-y_n)^2. Branching into the fixed H_3 sector gives F=H_3(y') sum_j b_j C_j^alpha(y_n), alpha=(n+4)/2. The angular norm factor independent of j can be discarded. Write h_j for the Gegenbauer norm and I_j for the coefficient numerator. Then
h_j=pi 2^(1-2alpha) Gamma(j+2alpha)/(j!(j+alpha)Gamma(alpha)^2),
I_j=integral_{-1}^1 (1-t^2)^(alpha-1/2)(1-t)^(-2) C_j^alpha(t)dt,
b_j=I_j/h_j.
The terminating Saalschutz summation gives
I_j=I_0 (j+1)(j+n+3)/(n+3).
Indeed insert C_j^alpha(1-2u)=(2alpha)_j/j! 2F1(-j,j+2alpha;alpha+1/2;u) and integrate each term against u^(alpha-5/2)(1-u)^(alpha-1/2). The resulting balanced terminating 3F2 sums to (2)_j/(2alpha-1)_j. This identity is also checked directly for j=0,...,8 and n=3,...,10 in agent2_cubic_spherical_hessian_checks.py.

The shape-Hessian weight from forcing (Delta_boundary+n-1)F is ((l-1)(l+n-1))^2/kappa_l, l=j+3. Stirling gamma ratios show I_j~C j^2, h_j~C' j^(n+2), and kappa_l~l. Consequently the positive norm underlying the negative reduced shape Hessian has summand comparable to j^(5-n). Its convergence is therefore equivalent to n>6.

This is an exact spectral integrability result. It does not prove the nonlinear noncompactness construction or any low-dimensional compactness theorem.

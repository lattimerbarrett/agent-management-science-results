# Positive exact-Robin unbounded-energy almost-solutions in every dimension

This is NOT a sequence of solutions of the interior PDE and NOT a
counterexample to any requested compactness theorem. It shows why integral
bounds plus qualitative dual residual control do not finish extraction.

Choose a fixed smooth Euclidean mean-convex compact domain with a planar
boundary patch; rounded convex bodies supply examples. Its Yamabe Robin
first eigenfunction phi is positive. On an interior subpatch place N=m^(n-1)
points on a regular grid of spacing ell comparable to m^-1=N^(-1/(n-1)).
Let a=(n-2)/2, epsilon=N^(-2/a), and let U_(epsilon,j) be the standard
halfspace bubble centered at the jth grid point. Multiply each by the same
fixed-shape radial cutoff supported in a half-ball of radius ell/10 and equal
to1 in radius ell/20. The half-ball supports are disjoint; the cutoffs are
even in the normal coordinate. Put W_N=sum_j chi_j U_(epsilon,j) and
u_N=W_N+N^-10 phi.

Every u_N is positive, smooth and satisfies the EXACT Robin boundary
condition: on the planar patch H=0 and both bubbles/cutoffs are even; outside
the patches the bumps vanish, and B phi=0. Their boundary maxima diverge.

Each bump has source mass O(epsilon^a)=O(N^-2) and critical energy converging
to the fixed positive halfspace bubble energy. The cutoff energy errors sum
to O(N(epsilon/ell)^(n-2))=O(N^(-2-1/(n-1)))=o(1). Thus
 int u_N^p=O(N^-1)+o(1),
 J(u_N)=N J_halfspace(U)+o(1)->infinity.
The positive background interaction is negligible by critical Holder.

The sharp source-Morrey bound is uniform. For r<epsilon use the peak density
O(epsilon^(-(n+2)/2)) times r^n; its ratio to r^a is maximized at epsilon and
is O(1). For epsilon<=r<ell a ball meets at most C(n) grid bumps, each of mass
O(epsilon^a)<=O(r^a). For ell<=r<=1 grid counting gives mass
O((r/ell)^(n-1)epsilon^a)=O(N^-1 r^(n-1))<=O(r^a).
The smooth N^-10 phi background only adds O(r^n).

Finally these are almost-solutions in the dual energy norm. The cutoff
commutator in gradient-divergence form has L2 vector-field norm at most
C N^(1/2)(epsilon/ell)^a. The remaining volume commutator is supported on
disjoint annuli, with L^(2n/(n+2)) norm at most
C N^((n+2)/(2n))(epsilon/ell)^a; the nonlinear cutoff tail is smaller by the
factor (epsilon/ell)^2. Consequently
 ||-L u_N-kappa u_N^p||_(H^-1_Robin)
 <=C[N^(1/2)+N^((n+2)/(2n))]N^-2 N^(a/(n-1))+o(1)->0.
The two N exponents are exactly -1-1/(2(n-1)) and
-1+(n-2)/(2n(n-1)), strictly negative for alln>=3.
The extra eigenfunction contributes O(N^-10) linearly and
O(N^-10 N^(2/n)+N^(-10p)) nonlinearly.

Thus even exact linear boundary condition, positivity, sharp source-Morrey,
and interior dual residual tending to zero coexist with divergent critical
energy in every dimension. These functions are NOT exact nonlinear solutions:
the unbalanced Jacobi/kernel equations remain and cannot be discarded.

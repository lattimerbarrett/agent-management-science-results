# Conditional sharp isolated-simple pointwise estimate (agent_2)

Let n>=3, a=(n-2)/2, p=(n+2)/(n-2), A=n(n-2).
Consider a fixed smooth metric and smooth boundary near a boundary point.
Assume a sequence of positive critical Robin solutions has boundary local maxima
p_i, heights M_i->infinity and scales eps_i=M_i^(-1/a). Assume:

1. Isolated bound u_i(x)<=C d(x,p_i)^(-a) for 0<d<rho_i, with eps_i/rho_i->0.
2. Bubble convergence eps_i^a u_i(p_i+eps_i y)->(1+|y|^2)^(-a) in C^2_loc.
3. In fixed smooth boundary normal/Fermi coordinates centered at p_i, the
   function r^a times the Euclidean hemispherical average of u_i has negative
   derivative on [R eps_i,rho_i], for every sufficiently large fixed R and large i.
   It suffices to assume this for one fixed large R.

Then, after replacing rho_i by min(rho_i,rho_0) for a fixed sufficiently small
rho_0, one has the UNIFORM SHARP estimate

             u_i(x)<=C M_i^(-1) d(x,p_i)^(2-n)

for 0<d(x,p_i)<=rho_i. The proof below requires only standard linear Harnack,
Schauder estimates, and a local harmonic Robin normalization, not Pohozaev sign.

## 1. Scalar-flat/minimal-boundary local normalization

The original local metric is flat after a smooth conformal change, by LCF.
On a sufficiently small fixed half-ball solve the linear mixed problem
Delta zeta=0, B_delta zeta=0 on its physical boundary, zeta=1 on the artificial
outer cap. For small radius, coercivity and the maximum principle give zeta>0;
standard elliptic regularity gives uniform C^m bounds on a smaller half-ball.
Potential corner regularity at the outer cap is irrelevant after shrinking.
The metric g0=zeta^(4/(n-2)) delta has R_g0=0,H_g0=0.
Write v_i=u_i/zeta (including the preceding flattening conformal factor).
After multiplying zeta by a constant, zeta(p_i)=1. Smooth positive factors change
M_i and eps_i by uniformly bounded factors. In boundary Fermi coordinates,
g0_ij=delta_ij+O(r), dvol_g0=(1+O(r))dy, and v_i satisfies
Delta_g0 v_i+A v_i^p=0, partial_t v_i=0 on t=0.

Changing smooth factors/coordinates perturbs hemispherical averages and their
first radial derivatives by O(r) relatively. Indeed annular gradient estimates
below give |Du_i|<=C u_i/r. Thus hypothesis 3 implies for the new average m_i
and w_i=r^a m_i:

   w_i(r)<=C w_original(R eps_i) on [R eps_i,rho_i],
   (d/d log r)w_i(rho_i)<=C rho_i w_i(rho_i).

No monotonicity of the transformed w_i throughout the annulus is required.

## 2. Annular Harnack and derivative bounds

From isolation, v_i^(p-1)<=C r^(-2). Rescale each annulus by r. Interior and
Neumann-boundary Harnack yield sup_annulus v_i<=C inf_annulus v_i. Schauder
estimates applied after this Harnack inequality give

       |D v_i|<=C r^(-1)m_i(r), |D^2 v_i|<=C r^(-2)m_i(r).

Constants are independent of i,r and rho_i. Use overlapping annuli for the
full hemispherical averages; their densities are uniformly comparable.

## 3. Weak decay via a one-dimensional comparison

In Euclidean Fermi coordinates, the Neumann condition at t=0 eliminates the
flat disk flux. Since g0=delta+O(r), its Christoffel symbols are O(1), and the
previous derivative bounds imply

 m_i''+(n-1)m_i'/r >= -C m_i^p-C r^(-1)m_i.

Equivalently, for t=log r,

          w_i,tt >= a^2 w_i-C w_i^p-C r w_i.

Bubble convergence at r=R eps_i gives w_i(R eps_i)<=C R^(-a).
By hypothesis 3 and the smooth normalization, w_i remains uniformly small on
the whole annulus when R is large. Given sufficiently small eta>0, first choose
R large and then rho_0 small to obtain

       w_i,tt >= b^2 w_i,   b=a-eta>0.

At T=log rho_i the endpoint inequality is w_i,t(T)<=kappa_i w_i(T), with
kappa_i=C rho_i<b/2. Comparison for d^2/dt^2-b^2 against the solution of
z''=b^2 z, z(t0)=w_i(t0), z'(T)=kappa_i z(T), gives

       w_i(t)<=C w_i(t0) exp[-b(t-t0)] (t0<=t<=T).

For completeness the comparison function is a positive multiple of
cosh(b(T-t))-(kappa_i/b)sinh(b(T-t)); the constant C is uniform when
kappa_i/b<=1/2. For a rigorous comparison, set y=w_i-z and multiply y''-b^2 y>=0 by y_+.
Integration gives integral[(y_+')^2+b^2 y_+^2]<=kappa_i y_+(T)^2, whereas
the elementary one-dimensional trace inequality (complete the square) gives
integral[(y_+')^2+b^2 y_+^2]>=b y_+(T)^2, since y_+(t0)=0.
As kappa_i<b, this forces y_+=0.
Consequently

       v_i(x)<=C eps_i^(a-eta) r^(2-n+eta).

## 4. Nonlinear mass bound

Choose eta so that p eta<2. The core ball r<=R eps_i contributes O(eps_i^a)
to integral v_i^p. On the remaining annulus the previous bound gives

 int v_i^p <= C eps_i^((a-eta)p)
                     int_(R eps_i)^rho_i r^(-3+p eta)dr
            <=C eps_i^((a-eta)p-2+p eta)=C eps_i^a,

because ap=a+2. Smooth volume densities are harmless.

## 5. Exact flux gives the sharp decay

Let F_i(r) be outward g0-normal flux through the coordinate hemisphere.
The physical boundary is minimal and v_i has homogeneous Neumann data, so

        F_i(r)=-A int_(B_r^+) v_i^p dvol_g0.

Thus 0<=-F_i(r)<=C eps_i^a. On the other hand, metric comparison and the gradient
bound give

 F_i(r)=|S_+^(n-1)| r^(n-1)m_i'(r)+O(r^(n-1)m_i(r)).

Hypothesis 3 transferred through the smooth normalization gives
r m_i'(r)+a m_i(r)<=C r m_i(r), hence for rho_0 small,

        F_i(r)<=-c r^(n-2)m_i(r).

It follows m_i(r)<=C eps_i^a r^(2-n); annular Harnack gives the desired pointwise
bound. The core r<=R eps_i follows directly from bubble convergence (and local
maximum/selection bounds). Transforming back preserves the estimate.

SCOPE: This proves the sharp estimate conditional on isolation, bubble profile,
and absence of a second critical radius. It does NOT prove those assumptions,
cluster exclusion, the nonlinear Pohozaev sign, or full compactness.

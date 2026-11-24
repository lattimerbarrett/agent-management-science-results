# Exact local model coefficients in dimensions five and six

These are linear boundary-Jacobi propositions. They do NOT prove arbitrary-solution blowup isolation, simple blowup, or a nonlinear Pohozaev expansion with controlled errors. In particular they are not by themselves a compactness proof.

## Dimension five: quadratic tracefree graph

Let f=H2 be a harmonic homogeneous quadratic on R4 and U=(1+|x|^2)^(-3/2) on R5_+. The first physical graph correction V solves
(Delta+35(1+|x|^2)^(-2))V=0,
V_t=-3 f(z)(1+|z|^2)^(-5/2) on t=0.
It belongs to D^(1,2), uniquely after projection off the usual bubble kernel. Existence follows by stereographic transfer: tangential angular degree2 excludes the negative constant mode and the degree1 kernel, so the Jacobi form is coercive there. Its exact Jacobi energy is
integral_[R5_+] (|DV|^2-35(1+|x|^2)^(-2)V^2)
=(2/pi+9pi/32) integral_[S3] f^2.

To compute it, the unit-hemisphere displacement is F(y)=H2(y')/(1-y5), up to an irrelevant sign. With alpha=7/2 the Gegenbauer coefficient numerator is I01=16/15. The exact base spectral weight equals (8 Gamma(alpha)^2/pi) times the moment weight used in agent2_quartic_all_dimensions_proof.md. The total moment is
M=(g0+g1)/(d-1)=pi/2+32/(9pi), d=3/2.
Conformal transfer from U to the unit round sphere has constant solution factor squared2^(-3), while the boundary-variation coefficient squared is (3/8)^2. Hence the energy constant is
2^(-3)(3/8)^2 I01^2 (8Gamma(7/2)^2/pi)M=2/pi+9pi/32.
The checker verifies this exact gamma simplification. The second-order reduced graph energy is minus half this positive quantity. Under bubble dilation its factor is lambda^2.

## Dimension six: cubic graph and logarithmic divergence

Let f=H3+|z|^2 L on R5, with H3 harmonic homogeneous cubic and L linear. Let U=(1+|x|^2)^(-2). The exact first physical Jacobi correction satisfies
(Delta+48(1+|x|^2)^(-2))V=0,
V_t=4[(Delta f)/10 (1+|z|^2)^(-2)-2f(1+|z|^2)^(-3)].
Since Delta(|z|^2L)=14L, its boundary data have leading term
-|z|^(-3)[8H3(z/|z|)+(12/5)L(z/|z|)]+O(|z|^(-5)).

Seek V0=r^(-2)Phi(omega). The harmonic equation at leading order is
(Delta_[S5]-4)Phi=0 on S5_+,
partial_nu Phi=8H3+(12/5)L on S4.
The signs follow because physical partial_t at the equator is minus the angular outward derivative divided by r.

For equatorial harmonic degree ell, the regular radial solution on S5_+ is
sin(theta)^ell 2F1((ell+2)/2,(ell+2)/2;ell+5/2;sin(theta)^2).
The hypergeometric connection formula gives the exact positive DtN multiplier
kappa_ell=2Gamma((ell+3)/2)^2/Gamma((ell+2)/2)^2.
In particular kappa1=8/pi and kappa3=128/(9pi). The checker verifies the angular ODE symbolically for arbitrary ell and these special gamma values exactly. Therefore
C6=integral_[S5_+] (|D_S Phi|^2+4Phi^2)
=(9pi/2)integral_[S4]H3^2+(18pi/25)integral_[S4]L^2.
This is strictly positive unless the entire cubic jet vanishes.

### Construction and error bound for the full correction

Choose a radial cutoff chi that vanishes near0 and equals1 beyond2. Put Q=chi r^(-2)Phi. Its bulk Jacobi residual is O(r^(-6)) at infinity, and its Neumann mismatch is O(r^(-5)). These are respectively in the dual critical bulk and trace spaces. Although Q itself has logarithmically divergent energy, all residual pairings against the bubble kernel converge, and integration by parts at infinity has zero flux against the kernel. The degree3 part is automatically orthogonal to all kernel modes. The degree1 part is orthogonal to translations because its exact radial integral is proportional to
28 integral_0^infinity r^6(1+r^2)^(-6)dr -12 integral_0^infinity r^8(1+r^2)^(-6)dr=0.
The checker verifies the beta-function cancellation exactly. The scale mode is excluded by odd angular parity.

On angular sectors1 and3, the bubble Jacobi form is coercive after removing its degree1 translation kernel: stereographic transfer excludes the negative constant eigenmode, and the next eigenvalue has a positive gap. Lax--Milgram on that complement therefore solves V=Q+eta with eta in D^(1,2), with the exact boundary data above. Solvability of the projected equation is the full equation because of the checked compatibility.

For completeness the remainder has eta=O(r^(-4)log r), Deta=O(r^(-5)log r). Under Kelvin inversion, eta becomes an H1 function near0 satisfying an elliptic equation with bounded potential and source O(r^(-2)), and Neumann datum O(r^(-1)). On a sufficiently small halfball, mixed Dirichlet/Neumann comparison is valid because the potential is dominated by the first mixed Laplacian eigenvalue. Barriers C log(1/r)-D t/r+C0 and their negatives dominate the source and Neumann datum: -Delta log(1/r)=4/r^2 and partial_nu(-t/r)=1/r on the flat boundary; choosing C large relative to D controls the O(r^(-2)) angular Laplacian contribution. Point capacity is zero, so the H1 weak comparison passes through0. This yields O(log(1/r)); annular elliptic boundary estimates yield its gradient bound. Kelvin inversion gives the stated remainder estimates.

Consequently the cross energy between Q and eta is integrable, as is the potential term 48(1+r^2)^(-2)V^2. The only logarithmic divergence is the Dirichlet energy of r^(-2)Phi. Thus
integral_[B_R^+] (|DV|^2-48(1+r^2)^(-2)V^2)=C6 log R+O(1).
The reduced graph energy has logarithmic coefficient -C6/2. Under cubic scaling it is proportional to -lambda^4 log(1/lambda), modulo lower-order finite terms.

## Missing compactness bridge

To apply these coefficients to arbitrary positive solutions, one still needs quantified boundary blowup selection, isolated/simple estimates uniform on expanding annuli, the nonlinear Pohozaev identity with errors small at the mass scale, and exclusion of clustering. None follows merely from the linear calculations above. The expected consequences (II vanishing at a dimension-five blowup point, cubic-jet vanishing at a dimension-six blowup point) are not asserted here without that bridge.

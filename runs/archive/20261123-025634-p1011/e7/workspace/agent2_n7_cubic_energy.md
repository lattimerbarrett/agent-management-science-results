# Dimension-seven finite cubic Jacobi energies

This is a precise linear-model proposition, NOT by itself an assertion of n7 compactness or an answer to the original classification problem.

Let S=1+|x|^2, U=S^(-5/2) on R7_+, and let f3(z)=H3(z)+|z|^2 L(z) on R6, with H3 harmonic homogeneous cubic and L linear. The physical boundary-graph correction is the unique center-normalized solution
 (Delta+63 S^(-2))Phi3=0,
 (Phi3)_t=5[(Delta f3)/12 S^(-5/2)-2 f3 S^(-7/2)].
Center normalization means Phi3(0)=0 and its tangential gradient at0 is zero; adding translation Jacobi fields enforces the latter and does not change its energy.

Then Phi3 is in D^(1,2), |D^k Phi3|<=C(1+r)^(-3-k) for k=0,1,2, and its exact Jacobi energy is
 L(Phi3,Phi3)=C3 integral_[S5] H3^2+C1 integral_[S5] L^2,
 C3=(675 pi^2+7168)/(576 pi)>0,
 C1=25(1024+117 pi^2)/(15552 pi)>0.
There is no H3/L cross term, by orthogonality of tangential harmonic degrees3 and1. For comparison, the degree2 correction has energy coefficient
 C2=25 pi/384+8/(27 pi)>0
per unit angular L2 norm.

## Existence, compatibility, decay

The boundary data are O(r^-4), hence belong to L^(12/7)(R6), the dual critical trace space. They have only tangential harmonic sectors1 and3. The negative spherical constant mode is excluded by odd tangential parity. The remaining Jacobi form is coercive after removing the translation kernel, by stereographic transfer to the hemisphere and its Neumann spectral gap.

The degree3 source is automatically orthogonal to translations. Since Delta(|z|^2 L)=16L, the degree1 source is (10/3)(2-|z|^2)L S^(-7/2). Its pairing against partial_a U is zero: for L=z_a the only radial integral is
 2 integral_0^infinity r^7(1+r^2)^(-7) dr
 - integral_0^infinity r^9(1+r^2)^(-7) dr
 =2/120-1/60=0.
Other tangent directions vanish by angular parity. The scale mode is even and therefore excluded. Lax--Milgram on the kernel complement gives Phi3.

Kelvin inversion preserves the Jacobi potential and transforms its boundary data to O(rho^-3) near0. The transformed solution is H1 near0 (Kelvin is an energy isometry). The barriers C rho^-2-D t rho^-3 have positive dominating interior and outward-Neumann terms, since -Delta rho^-2=6rho^-4 and Delta(t rho^-3)=-12t rho^-5. Mixed comparison on a sufficiently small halfball, followed by annular elliptic estimates, gives Kelvin solution O(rho^-2) with derivatives, equivalent to the stated decay at infinity. The potential term is bounded near0 and is dominated by the mixed Laplacian on a sufficiently small halfball. H1 comparison passes through0 by zero point capacity.

## Exact spectral calculation

Conformal transfer uses the unit round hemisphere, with U=2^(-5/2) Omega^(5/2), Omega=2/S. Its boundary displacement is
 F2=H2(y')/(1-t),
 F3=H3(y')/(1-t)^2,
 F1=L(y')(1+t)/(1-t),
where (y',t) lies on S6. Tangential harmonic degree ell has Gegenbauer parameter alpha=ell+5/2. Writing its coefficient numerator I_j and Gegenbauer norm h_j,
 h_j=pi 2^(1-2alpha) Gamma(j+2alpha)/[j!(j+alpha)Gamma(alpha)^2].

Rodrigues integration by parts gives, for a denominator (1-t)^p,
 I_j(p)=2^(2alpha-p) Gamma(alpha+1/2-p)Gamma(alpha+1/2)/Gamma(2alpha)
 *Gamma(2alpha+j)/Gamma(2alpha+1-p+j)*(p)_j/j!.
All boundary terms vanish for the cases used here. Consequently
 I_j^(2)=32/35 for all j>=0,
 I_j^(3)=(64/63)(j+1)(j+10)/10,
 I_j^(1)=32/15 for j>=1.
The omitted j=0 degree1 term is a conformal gauge mode and contributes zero energy.

At total spherical degree k, the inverse hemisphere DtN multiplier is 1/kappa_k, where
 kappa_k=2 Gamma((k+8)/2)Gamma(k/2)/[Gamma((k-1)/2)Gamma((k+7)/2)].
The positive energy weight is (k-1)^2(k+6)^2/kappa_k. Align all branches at the same total degree k=J+2. The ratios of I_j^2/h_j relative to the quadratic branch are
 cubic-harmonic: J(J+9), using j=J-1 and a zero term at J=0;
 trace-cubic: (J+1)(J+8)/9, using j=J+1.
These follow immediately from the displayed gamma norms. The checker additionally integrates the actual Gegenbauer polynomials exactly for J=0,...,7 and independently verifies both ratios.

Put x=(J+3)/2, d=5/2. Gamma duplication reduces the base quadratic spectral weight to 288 times
 w(x)=(2x+3/2)[Gamma(x)/Gamma(x+5/2)]^2.
The physical conformal/Robin prefactor is 2^-5 (5/12)^2=25/4608, so the total common factor is25/16. Therefore the three coefficients are25/16 times the moment sums of 1, J(J+9), and (J+1)(J+8)/9, respectively, against w.

## Exact summation, no infinite numerical truncation

For a polynomial P(J), find Q(x) satisfying
 Q(x)(x+3/2)^2-Q(x+1)x^2=(2x+3/2)P(2x-3).
Multiplication by [Gamma(x)/Gamma(x+5/2)]^2 telescopes. Summing on the interlaced lattices x=3/2,5/2,... and x=2,3,... gives
 M(P)=sum_(X=3/2,2) Q(X)[Gamma(X)/Gamma(X+3/2)]^2.
The tail is zero: deg Q<=2 while the gamma ratio squared is O(x^-3).

The exact telescopers are
 Q2=2/3,
 Q3=4(x-1)(2x+3),
 Q1=4(6x^2+3x-5)/27.
Their endpoint sums are
 M2=pi/24+128/(675pi),
 M3=(675pi^2+7168)/(900pi),
 M1=(1024+117pi^2)/(972pi).
Multiplying by25/16 proves the claimed constants. The checker constructs these polynomial identities by exact coefficient matching, verifies zero remainders, computes the gamma endpoints, verifies translation compatibility and the six-variable harmonic decomposition, and checks the direct spectral ratios described above. It was actually executed successfully.

## Independent mixed-stress identity and its sign

For a homogeneous degree-j graph f_j, write F=eta f and w=U+eta Phi. Use the exact graph flux (ambient tangential derivatives, evaluated on the graph)
 I=-beta T w[z.D_z w+F w_t+a w]-(Sgraph/2)|Dw|^2+(K/q)Sgraph w^q,
where Sgraph=z.DF-F, T=H d-sigma/dz, a=(n-2)/2, beta=(n-2)/(2(n-1)). The spherical Pohozaev flux is minus the integral of I. The direct eta^2 graph term is zero because I(F,U) is odd in F. The shape/Phi cross coefficient on the plane is exactly
 I2=-beta Delta f[(z.DU+2aU)Phi+U z.DPhi]
    -(j-1)f DU.DPhi+K(j-1)f U^p Phi.
Every derivative in this display is tangential. Integrating tangentially by parts gives
 integral I2=(j-1) integral[beta Delta f U+Df.DU-f U_tt]Phi
            =(j-1) integral g_f Phi
            =-(j-1)L(Phi,Phi).
Here g_f=Phi_t is the first graph Robin residual, and the last equality uses outward nu=-partial_t. The cancellation in the first line uses only
 (n-1+j-2)-2a=j-1,
and Delta_z U+K U^p=-U_tt. Thus the spherical Pohozaev coefficient is POSITIVE (j-1)L(Phi,Phi). For j=3,n=7 the tangential integration-by-parts edges are O(R^-1), so they vanish; the quadratic case decays faster. Consequently the cubic constants proved above enter the n7 Pohozaev flux with factor2, and the quadratic coefficient with factor1.

These constants strengthen the separate n7 diagnostic by proving strict positivity of every cubic jet component; they do not replace the required full nonlinear stress expansion or compactness bridge.

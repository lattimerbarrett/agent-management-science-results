# Exact degree-eight profile minima in dimensions 19 through31

This is a complete finite-dimensional spectral certificate. For nonlinear existence it must be combined with the uniform inverse, contraction, degree-eight C0 expansion and fixed-domain gluing estimates in the team's separate documents.

## Explicit profile

Let m=n-1, H2(x)=x1^2-x2^2, f_k(x)=|x|^(2k)H2(x), and
f=sum_(k=0)^3 a_k f_k,
(a0,a1,a2,a3)=(1,-4628/10000,5655/100000,-1408/1000000).
We prove the exact negative shape Hessian has a strict nondegenerate minimum in scale and all translations for each integer n=19,...,31.

## Exact spectral moments

Set d=(n-2)/2, J=2x-3, and suppress a common positive constant from all quadratic forms. The base m2-sector spectral weight is
w(J)=(2x+d-1)[Gamma(x)/Gamma(x+d)]^2,
where x runs over3/2,2,5/2,3,... (two interlaced unit lattices).
The ratio of the Gegenbauer coefficient for f_k to that for f_0 is
R2_k(J)=sum_(ell=0)^k binom(k,ell)2^ell(-1)^(k-ell) C_ell(J),
C_ell(J)=(J+1)_ell(J+n+2-ell)_ell/[ell! product_(r=1)^ell(n+1-2r)].
This follows from the same beta/Saalschutz formula proved in agent2_DtN_proof.md: physical f_k transforms to H2(y')(1+t)^k/(1-t)^(k+1); expand (1+t)^k=[2-(1-t)]^k and integrate each term.

Let M(P)=sum_J w(J)P(J). The exact Gram entries are G2_kl=M(R2_k R2_l). All sums converge for n>16. They are computed with no infinite numerical truncation: solve the polynomial identity
Q(x)(x+d-1)^2-Q(x+1)x^2=(2x+d-1)P(2x-3).
Multiplying by [Gamma(x)/Gamma(x+d)]^2 telescopes, so
M(P)=sum_(X=3/2,2) Q(X)[Gamma(X)/Gamma(X+d-1)]^2.
The script constructs Q by triangular coefficient matching and verifies the polynomial identity exactly. Its degree is at most12; its tail vanishes for n>=19 by gamma asymptotics.

The positive shape norm at zero translation and scale lambda, with z=lambda^2, is
Qscale(z)=sum_kl a_k a_l z^(k+l+1)G2_kl/G2_00.
Its negative, times a positive normalization, is the reduced energy coefficient.

## Translation moments

The derivative decomposition is
partial_i f_k=2k r^(2k-2)H3_i+2 a_i(m+2+2k)/(m+2) r^(2k)x_i,
where here a_i denotes the eigenvalues (1,-1,0,...) of H2, not the profile coefficients, and
H3_i=x_i H2-2a_i r^2 x_i/(m+2).
The angular norm factors, divided by the area of S^(m-1), are
N2=4/[m(m+2)],
N3_i=4/[m(m+2)(m+4)]+4a_i^2/[(m+2)^2(m+4)],
N1=1/m.
Only the H2 component of partial_ii f_k enters its pairing against f_l. Its parallel coefficient is
Cki=2k(m+2+2k)(1+2a_i^2)/(m+4).
These follow by elementary spherical moments of tracefree quadratic forms.

The m3-sector ratios relative to its base harmonic cubic are
R3_k(J)=sum_(ell=0)^k binom(k,ell)2^ell(-1)^(k-ell) C_ell(J)/(ell+1),
and its base weight relative to w(J) is J(J+n+2).
The m1-sector starts at k=1 (k0 is gauge). Relative to r^2 x_i its ratios are
R1_k(J)=sum_(ell=1)^k binom(k,ell)2^(ell-1)(-1)^(k-ell)
 *(J+2)_(ell-1)(J+n+2-ell)_(ell-1)
 /[(ell-1)! product_(r=1)^(ell-1)(n-1-2r)],
and its base weight relative to w(J) is 4(J+1)(J+n+1)/(n-1)^2.
All identities follow from the same beta/Saalschutz coefficient formula, with the total spherical harmonic degree held fixed; their base-weight cases agree with the independently checked q3,qtrace identities in agent4_mixed_spectral_exact.py.

Define G3_kl=M(J(J+n+2)R3_kR3_l) and G1_kl=M(4(J+1)(J+n+1)R1_kR1_l/(n-1)^2). All these are obtained by the identical exact polynomial telescoping routine.

For b=a_i^2 in {0,1}, the translation Taylor coefficient of the positive shape norm, normalized by G2_00, is
Hi(z)=[sum_(k>=1,l>=0) a_k a_l z^(k+l) Cki N2 G2_(l,k-1)
 +sum_(k,l>=1) a_k a_l z^(k+l){4kl N3_i G3_(k-1,l-1)
 +4b(m+2+2k)(m+2+2l)G1_kl/[m(m+2)^2]}]/G2_00.
Here profile coefficients a_k are the rational numbers displayed above. This is exactly Q(partial_i f,partial_i f)+Q(f,partial_ii f). The script uses the algebraically equivalent expanded Cki. Reflection symmetry makes the Hessian diagonal and eliminates mixed scale-translation derivatives.

## Exact finite certificates

The script agent2_profiles_n19_n31_certificates.py calls the exact moment helper agent2_polynomial_search.py separately for each dimension. For each n it proves:
* Qscale' positive at the lower endpoint and negative at the upper endpoint of a rational interval of width10^-10;
* Qscale'' strictly negative throughout that interval;
* H0 and H1 strictly negative throughout the interval.
All interval endpoints and all arithmetic in these assertions are exact rational numbers. Gamma endpoint values simplify to rational functions of pi. Rigorous pi bounds are obtained from Machin's formula and20/21-term alternating arctangent sums; recursive interval addition, multiplication and reciprocal evaluate the rational expressions. Numerical root finding only selects/prints the brackets; every conclusion is checked independently by exact inequalities. Both scripts were actually run successfully.

Thus the intermediate value theorem gives a simple scale root in the bracket, and all Hessian eigenvalues of the negative shape energy are positive there. The n19 root interval is [.9024309988,.9024309989] in z. The other root brackets are explicitly embedded in the checker. This establishes the full nondegenerate local minimum for every n=19,...,31.

## Fixed smooth gluing scales

For degree8 choose mu_j=epsilon_j^8. The physical graph mu_j epsilon_j f((x-p_j)/epsilon_j) has highest polynomial coefficient epsilon_j; all lower coefficients decay faster, so the same disjoint-support construction is C-infinity with epsilon_j superpolynomially small relative to rho_j. The leading energy is mu_j^2=epsilon_j^16. Bubble cutoff error is o(mu_j) precisely when epsilon_j^((n-18)/2)rho_j^(-(n-2)/2)->0, valid for every n>=19 with the team's exponential/quadratic sequences. Agent4's degree8 remainder estimates verify the required C0 energy expansion despite divergent higher-order unweighted tails. No assertion for n=7,...,18 follows from this profile.

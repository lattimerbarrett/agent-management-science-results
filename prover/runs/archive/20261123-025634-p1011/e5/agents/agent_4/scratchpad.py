from pathlib import Path
Path('workspace/agent4_genericL_note.md').write_text(r'''# Generic angular harmonic graph model
Let tangential dimension be m=n-1, let H_L be a harmonic homogeneous polynomial of degree L, and let h=H_L(x) sum_j a_j |x|^{2j}. Put t=(r²-1)/(r²+1), omega=x/r. The spherical normal displacement is
f_j=H_L(omega)(1-t²)^(L/2) (1+t)^j/(1-t)^(L+j-1).
The spherical harmonic expansion uses Gegenbauer parameter alpha_L=L+(n-2)/2. Its energy weight at total degree ell=k+L is
((ell-1)(ell+n-1))² kappa_ell / N_k(alpha_L),
where kappa is the verified Jacobi NtD multiplier and N is the Gegenbauer norm. Modes ell=0 and1 have zero energy (respectively zero trace and conformal kernel).

For s>=1, Rodrigues gives the moment ratio
T_s(alpha,k)=(k+1)_(s-1)(k+2alpha+1-s)_(s-1)/[(s-1)! product_{r=1}^{s-1}(2alpha-2r-1)].
Expansion of (1+t)^j=(2-(1-t))^j gives projection polynomial
P_j^L=sum_{b=max(0,2-L)}^j binom(j,b)2^b(-1)^(j-b) T_{L+b-1}(alpha_L,k).
The omitted terms are polynomial functions of t of degree<=1 and vanish in energy.

Set reference index v=ell-2>=0 and x=v+(n+2)/2, a=n/2. Then every T_s is an even polynomial in x:
T_s=product_{r=0}^{s-2}[x²-(alpha_L-1-r)²]/[(s-1)! product_{r=1}^{s-1}(2alpha_L-2r-1)].
With universal reference weight W_v=x(x²-a²)²[Gamma((v+1)/2)/Gamma((v+n+3)/2)]², common positive factor suppressed, the Gram entries are:
* L>=2: C_L sum W_v P_i^L P_j^L / D_L,
  C_L=product_{r=0}^{L-3}(n+1+2r)²,
  D_L=product_{r=0}^{L-3}[x²-(a+1+r)²].
  Each P contains D_L. Thus the quotient is a polynomial, and nonexistent v<L-2 terms vanish exactly.
* L=1: (n-1)^(-2) sum W_v (x²-a²)P_i^1P_j^1.
* L=0: [(n-3)²(n-1)²]^(-1) sum W_v (x²-a²)[x²-(a-1)²]P_i^0P_j^0.
  j=0,1 are identically zero-energy modes.

All sums telescope by the previously checked centered antidifference. The graph's scaling exponent is L+2j-1, so the scale derivative Gram weight is 2L+2i+2j-2. Physical degree D=L+2d requires n>2D.

Executable exact Gram construction: agent4_genericL_models.py. Exploratory eigenvalues, NOT interval sign certificates: agent4_genericL_results.json. These additional modes do not remove the exact L2,n19,d3 strict-minimum certificate.
''')
print('wrote generic angular model derivation')

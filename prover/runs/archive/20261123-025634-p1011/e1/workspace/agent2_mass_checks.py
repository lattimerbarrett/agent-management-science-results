import sympy as s
from pathlib import Path
n=s.symbols('n', positive=True, integer=True)
r=s.symbols('r', positive=True)
A,m=s.symbols('A m', real=True)
k=n-2
U=(1+r*r)**(-k/2)
lap=s.diff(U,r,2)+(n-1)/r*s.diff(U,r)
assert s.simplify((lap+n*k*(1+r*r)**(-(n+2)/2))*(1+r*r)**((n+2)/2))==0
G=A*r**(-k)+m
P_density=k*s.Rational(1,2)*G*s.diff(G,r)+r*s.Rational(1,2)*s.diff(G,r)**2
P_flux=s.simplify(s.expand(P_density)*r**(n-1))
assert s.simplify(P_flux+k*k*A*m/2)==0
# Inverted metric: G^(4/k) delta_x under y=x/|x|^2 is
# (A + m |y|^(2-n))^(4/k) delta_y. Normalize A=1.
# Half-space ADM flux: (d_j h_ij - d_i h_jj) nu_i = -(n-1) d_r F.
# Limiting unnormalized half-sphere flux / area(unit hemisphere)
# = 4(n-1)m. The usual 1/[2(n-1)|S^(n-1)|] gives m,
# since hemisphere area is |S^(n-1)|/2.
t=s.symbols('t', real=True)
F_lin=1+4*m/k*r**(-k)
flux_per_halfarea=s.simplify(-(n-1)*s.diff(F_lin,r)*r**(n-1))
assert s.simplify(flux_per_halfarea-4*(n-1)*m)==0
# Robin transformation coefficient 2c = k/[2(n-1)].
c=k/(4*(n-1))
assert s.simplify(2*c*(2*(n-1)/k))==1
# Euclidean graph mean curvature under x_n=f(x'), domain above graph:
# outward normal=(grad f,-1)/sqrt(1+|grad f|^2), so H=div(grad f/sqrt(...)).
# First variation H=Delta f. This sign is consistent with upper halfspace.
results={
 'bubble_residual':str(s.simplify(lap+n*k*(1+r*r)**(-(n+2)/2))),
 'green_Pohozaev_flux_per_unit_hemisphere_area':str(P_flux),
 'linearized_ADM_flux_per_unit_hemisphere_area':str(flux_per_halfarea),
 'normalization':'halfspace ADM constant 1/[2(n-1)|S^(n-1)|] gives mass m for (1+m*r^(2-n))^(4/(n-2))*delta',
}
print(results)
Path('workspace/agent2_mass_checks.py').write_text(Path(__file__).read_text())
Path('workspace/agent2_geometry.md').write_text(r'''# Checked conformal geometry and conditional mass endgame
Let c=(n-2)/(4(n-1)). For ghat=phi^{4/(n-2)}g,
L_ghat(w)=phi^{-(n+2)/(n-2)}L_g(phi*w),
B_ghat(w)=phi^{-n/(n-2)}B_g(phi*w).
Consequently u solves the problem for g iff u/phi solves it for ghat.
Since phi is fixed smooth positive on compact M, boundary blowup is invariant.

The Robin energy is E(v)=int_M(|dv|^2+cR v^2)+2c int_boundary H v^2.
If lambda_1>0 and phi is its positive eigenfunction, then
H_ghat=0 and R_ghat=(lambda_1/c)phi^{-4/(n-2)}>0.

Suppose (this is an additional hypothesis, NOT yet established for the problem)
a boundary Green pole p has in a flat-halfball chart the expansion
G=A*r^{2-n}+m+remainder, with sufficient derivative remainder bounds to
define asymptotic mass after inversion. Suppose also that its Green blowup
has the decay required for the positive mass theorem with noncompact boundary.
Then G^{4/(n-2)}g has R=0 and H=0 away from p. After A=1 normalization,
the halfspace ADM mass is m (using normalization 1/[2(n-1)|S^{n-1}|]).
The positive mass theorem with boundary gives m>=0. Its rigidity case
identifies the complete blown-up space with Euclidean halfspace; conformal
compactification then identifies (M,g) with a round hemisphere. Thus the
excluded-hemisphere hypothesis forces m>0 whenever this endgame applies.

For the Euclidean harmonic expansion A*r^{2-n}+m, the Pohozaev boundary
flux is exactly -(n-2)^2*A*m*|S^{n-1}_+|/2. Thus any separately established
local blowup inequality liminf P>=0 contradicts positive mass.
The accompanying Python file verifies the radial PDE and flux constants
symbolically in n. It does NOT establish the local blowup inequality,
jet vanishing, the Green expansion, or a positive mass theorem.
''')

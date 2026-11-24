# Checked conformal geometry and conditional mass endgame
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

import sympy as s
from pathlib import Path
v=s.symbols('v'); F=s.Function('F')(v)
y=4*v*(1-v)*F
L=s.expand(v*(1-v)*s.diff(y,v,2)+s.Rational(3,2)*(1-2*v)*s.diff(y,v)-(s.Rational(3,2)/(v*(1-v))+1)*y)
HG=v*(1-v)*s.diff(F,v,2)+(s.Rational(7,2)-7*v)*s.diff(F,v)-9*F
assert s.simplify(L-4*v*(1-v)*HG)==0
# Gauss second sum at1/2 and its derivative.
Fhalf=s.sqrt(s.pi)*s.gamma(s.Rational(7,2))/(s.gamma(2)**2)
Fprimehalf=9/s.Rational(7,2)*s.sqrt(s.pi)*s.gamma(s.Rational(9,2))/(s.gamma(s.Rational(5,2))**2)
D=s.simplify(Fprimehalf/(2*Fhalf))
assert s.simplify(D-8/s.pi)==0
# f=(1/2)z^T A z, traceA0; sphere S2 fourth moment.
sphere_area=4*s.pi; f2moment=sphere_area*s.Rational(1,4)*s.Rational(2,15)
energy_log=s.simplify(4/D*f2moment)
assert s.simplify(energy_log-s.pi**2/15)==0
assert s.Rational(40-16,40+8)==s.Rational(1,2)
print('n4 angular ODE, DtN8/pi, log coefficientpi²/15, Jacobi sector coercivity1/2 checked.')

proof=r'''# Dimension-four quadratic-graph logarithmic coefficient

This is a local linear and energy calculation. It does NOT prove compactness or the required Pohozaev sign for arbitrary blowup sequences.

Use flat coordinates (z,t) in R^3×R_+ with outward normal −∂t and graph t=δ f(z), where f=(1/2)z^T A z, A symmetric tracefree. The standard n4 bubble is U=(1+|z|²+t²)^−1. The physical first boundary variation is −2fU/(1+|z|²); hence its Jacobi correction Φ has boundary condition ∂t Φ=−2f/(1+|z|²)². Its leading far-field harmonic correction q must satisfy

Δq=0, ∂out q=2f(z)/|z|4, q homogeneous of degree−1.

## Exact harmonic angular solution

Write r=(|z|²+t²)^{1/2}, s=t/r, and f(z)=|z|²Y2(z/|z|). Seek q=r^−1 Y(s,ω). The angular equation on S³_+ is (Δ_{S³}−1)Y=0. On the boundary S², the forcing is 2Y2. Its degree-two Dirichlet-to-Neumann multiplier is exactly κ=8/π.

To verify this independently, the pole-regular angular radial function is

y(s)=(1−s²) 2F1(3,3;7/2;(1−s)/2).

It satisfies (1−s²)y''−3sy'−[6/(1−s²)+1]y=0. Gauss's second formula gives y(0)=15π/8 and −y'(0)=15, hence κ=−y'(0)/y(0)=8/π. Consequently

q(z,0)=(π/4) f(z)/|z|3.

The solution is unique among homogeneous degree−1 solutions with this angular symmetry; angular operator −Δ_{S³}+1 is coercive.

## Exact Dirichlet logarithm

For 1<r<R, integration by parts gives

∫_{annulus_+}|∇q|² =∫_{flat_annulus}q∂out q.

Indeed the radial boundary fluxes are equal and cancel, since q has degree−1 in dimension4. On the flat annulus,

q∂out q=(π/2)r^−3 Y2²,

so

∫_{annulus_+}|∇q|²=(π/2)log R ∫_{S²}Y2².

The fourth moment on S² and trA=0 give

∫_{S²}f²=(2π/15)|A|².

Therefore the exact logarithmic Dirichlet coefficient is

∫_{annulus_+}|∇q|²=(π²/15)|A|² log R.

The n4 bubble Jacobi potential is n(n+2)U^{4/(n−2)}=24U², decaying r^−4; its contribution against q² is integrable at infinity and changes no logarithmic coefficient.

## Actual bubble Jacobi correction

The full correction Φ exists with Φ=q+O(r^−2) and ∇Φ=∇q+O(r^−3). Here is a construction rather than an asymptotic assumption. Cut q off smoothly to zero near0 and equalq outside2, calling the result Q. Then the interior residual (Δ+24U²)Q is O(r^−5) at infinity and is smooth near0; the boundary mismatch from the desired condition ∂outΦ=2f/(1+|z|²)² is O(r^−4). Both belong to the energy dual: the interior exponent is4/3 and the dual trace exponent3/2.

Restrict to the tangential SO(3) angular-degree2 sector, which is invariant under the potential U². On this sector the form ∫|∇η|²−24U²η² is coercive with constant1/2 relative to ∫|∇η|². Indeed stereographic transfer maps it to ∫(|∇w|²−16w²) on the radius1/2 hemisphereS4; angular degree2 excludes spherical degrees0,1, so its Neumann spectrum starts at40. The original Dirichlet norm transfers to ∫(|∇w|²+8w²), and (40−16)/(40+8)=1/2. Lax-Milgram therefore yields η∈D^{1,2}, in this sector, correcting both residuals. Set Φ=Q+η.

For completeness the decay improvement does not need an assumed weighted inverse. Rescaled annular boundary elliptic estimates and η∈L4 first give η=O(r^−1), since the source is O(r^−5) and boundary data O(r^−4). Then (Δη) is O(r^−5), because U²η=O(r^−5). Its volume source and Neumann boundary data are integrable. The halfspace Neumann Newton representation has kernel C|x−y|^−2 (sum with the reflected image); convolution of an integrable O(r^−5) volume source or O(r^−4) boundary source is O(r^−2). Explicitly split each integral into |y|<|x|/2, |y−x|<|x|/2 and the remaining exterior; the first piece is bounded by |x|^−2 times the L1 norm and each of the other pieces by C|x|^−3. A possible harmonic homogeneous-Neumann remainder in D^{1,2} is zero by testing its equation. Thus η=O(r^−2); annular derivative estimates then give ∇η=O(r^−3), up to the boundary. In particular all cross/error terms with ∇q are integrable, and the claimed logarithmic coefficient for Φ is proved.

The physical reduced shape energy is negative one half of the Jacobi energy. Under that asymptotic, for a concentrating bubble of physical scale δ the leading local term is

−(π²/30)|II°|² δ² log(1/δ),

where II°=A at the flat-normalized base point.

## Pohozaev orientation for the first-corrected model

Use the critical stress current J=(x·∇u+u)∇u−x|∇u|²/2+2xu4. Its divergence is (x·∇u+u)(Δu+8u3), and the usual spherical Pohozaev P is its spherical flux. Thus for a solution P=−∫graph J·ν. In the tracefree quadratic graph model t=ε f, the boundary mean curvature starts at cubic order in ε. The orderε² logarithm in −J·ν for u=U+εΦ is therefore exactly +ε² f∇U·∇q. On the plane U~r^−2 and q~(π/4)f/r3, so this term equals (π/2)ε² f²/r7. Boundary radial integration gives the POSITIVE coefficient +(π²/15)|A|² ε²logR. The potential cross term is integrable and changes no logarithm. This algebra is checked in the script.

This identifies sign and constant for the model. Proving the same lower bound with a controlled remainder for an ARBITRARY nonlinear isolated-simple blowup requires annular closeness to this model and is NOT proved here; clustering/selection is also separate.

All explicit ODE/gamma/moment algebra is checked in agent4_n4_log_checks.py, which was actually executed successfully.
'''
Path('workspace/agent4_n4_log_proof.md').write_text(proof)
Path('workspace/agent4_n4_log_checks.py').write_text(Path(__file__).read_text())
print('Saved n4 local logarithmic proof and checker.')

# Umbilic-point cubic Green correction constants.
D=lambda ell:2*s.gamma(s.Rational(ell+1,2))*s.gamma(s.Rational(ell+3,2))/(s.gamma(s.Rational(ell,2))*s.gamma(s.Rational(ell+2,2)))
assert s.simplify(D(1)-4/s.pi)==0
assert s.simplify(D(3)-32/(3*s.pi))==0
assert s.simplify(4/D(3)-3*s.pi/8)==0
assert s.simplify(s.Rational(2,3)/D(1)-s.pi/6)==0
x,y,z=s.symbols('x y z'); r2=x*x+y*y+z*z
assert s.expand(sum(s.diff(r2*x,a,2) for a in (x,y,z))-10*x)==0
print('n4 cubic Green correction source and exact angular multipliers checked.')

greenproof=r'''# Dimension-four Green expansion at an umbilic boundary point

Assume n=4, positive Robin Yamabe type, local conformal flatness, and II°(p)=0. This proves a local Green expansion and identifies its AF mass. It does not show that an arbitrary nonlinear blowup point is umbilic, isolated, or simple.

## Flat normalization

Conformally flatten the metric nearp. A local Möbius factor can adjust the mean curvature atp while retaining flatness; since II°(p)=0, arrange II(p)=0. In flat graph coordinates the boundary is t=f3(z)+O(|z|4), with z∈R3, domain above the graph, and f3 homogeneous cubic. Write uniquely f3=H3+|z|²L1, with H3 harmonic cubic and L1 linear. Then Δf3=10L1.

The boundary operator is B=∂out+H/3. Direct graph expansion gives

B(r^−2)=−4f3/r4+(Δf3)/(3r²)+O(1).

Thus the homogeneous-degree0 correction q must be harmonic and satisfy

∂out q=4H3/r4+(2/3)L1/r² on t0.

## Exact angular correction

Write q=q(ω) on S³_+. Then Δ_{S³}q=0 with the above angular boundary data. These data are odd in z, so have zero boundary mean. The angular Neumann problem therefore has a unique odd solution (the otherwise free constant is fixed by oddness). Its boundary degree1 and3 Dirichlet-to-Neumann multipliers are respectively4/π and32/(3π). Consequently

q(z,0)=(3π/8)H3(z)/|z|3+(π/6)L1(z)/|z|.

The angular solution is smooth up to the hemisphere boundary, analytic locally through the equator, and odd under z↦−z. In particular its hemisphere average is zero. All multiplier/source constants are checked in agent4_n4_log_checks.py.

## Parametrix and regular remainder

Take a cutoff of G0=r^−2+q nearp. It is harmonic offp in the flat patch, including the thin part below the tangent plane after analytic continuation. On the actual curved boundary, B G0=O(1): the leading degree−1 defect cancels by construction; the quartic boundary Taylor term gives a bounded residual; geometric changes in q contribute only O(r). Away fromp all cutoff errors are smooth.

Invert the global coercive Robin form to correct these bounded boundary and smooth interior errors. Standard Robin W^{1,p} regularity gives the correction in W^{1,p} for every finitep, hence C^{0,α} for everyα<1. The result is the positive Green function with normalized leading coefficient1,

G=r^−2+q(ω)+A+O(r^α).

Annular boundary estimates give gradient remainderO(r^{α−1}). Positivity follows by applying the coercive-form negative-part argument away from a tiny ball, whose inner boundary value is positive.

## AF geometry and mass

The Green metric ĝ=G²g is complete, scalar-flat and minimal-boundary offp. Under inversion y=x/r², R=|y|,

ĝ=[1+(A+q(ω))/R²+O(R^{−2−α})]²δ.

The boundary is a graph y_n=b(y')+O(R^−2), with b=f3(y')/|y'|4 homogeneous degree−1 and odd. Thus flattening its end changes coordinates by a degree−1 vector field V with only normal leading component, odd in y'. Its metric gauge term has tangential-normal coefficients even and normal-normal coefficient odd in y'. Every bulk ADM flux of this gauge is odd after contraction with the radial normal, and the boundary correction integrand is odd as well; both integrate to zero. The q contribution is zero because its hemisphere average is zero. The remaining mass is a strictly positive conventional factor timesA.

The decay order is2>(4−2)/2=1; scalar curvature and boundary mean curvature vanish, so the usual noncompact-boundary positive mass theorem in dimension4 applies (or after taking the orientable cover if needed). It gives A>=0, and rigidity gives A=0 only for the Euclidean halfspace Green metric. Compactification and local conformal rigidity then identify the original manifold with the conformal round hemisphere. Under the problem's exclusion, therefore A>0.

This last paragraph explicitly invokes the standard boundary positive mass theorem, not a newly proved theorem. It is the terminal global mass step only; all nonlinear blowup selection and sign estimates remain separate.
'''
Path('workspace/agent4_n4_green_umbilic.md').write_text(greenproof)
print('Saved n4 umbilic Green expansion proof.')

# Positive Pohozaev logarithm from the boundary stress cross term.
r2=x*x+y*y+z*z; rr=s.sqrt(r2); ff=x*x-y*y
Ufar=1/r2; qtrace=s.pi*ff/(4*rr**3)
cross=s.simplify(ff*sum(s.diff(Ufar,a)*s.diff(qtrace,a) for a in (x,y,z)))
assert s.simplify(cross-s.pi*ff**2/(2*rr**7))==0
assert s.simplify(s.pi/2*f2moment-s.pi**2/15)==0
print('Positive boundary-stress logarithm coefficientpi²/15 checked.')

rateproof=r'''# Dimension-four umbilicity rate under isolated-simple blowup

This lemma proves umbilicity at an isolated-simple blowup limit using energy-norm modulation. It does NOT prove the full local Pohozaev nonnegativity required for compactness.

## Hypotheses

Let u_i be positive solutions on one fixed positive-Yamabe LCF manifold, p_i boundary blowup centers, M_i=u_i(p_i)→infinity, epsilon_i=M_i^−1 (n4). Assume local bubble convergence and isolated-simple strong decay through one fixed physical radius r0:

u_i(x)<=C M_i^−1 dist(x,p_i)^−2,
|∇u_i(x)|<=C M_i^−1 dist(x,p_i)^−3

outside a fixed multiple of epsilon_i and inside2r0. Flatten the metric conformally nearp_i and use a uniformly controlled local Möbius normalization to arrange H(p_i)=0. In the corresponding Euclidean graph chart its quadratic term is f2_i=(1/2)A_i[z,z], trA_i=0, with uniformly bounded higher jets.

## Conclusion

|A_i|² log(1/epsilon_i) is bounded. In particular II°(p_i)→0.

## Proof

1. Cut u_i off inside the physical r0-ball. Core bubble convergence and the strong gradient decay give H¹ closeness to a cut-off standard bubble: after rescaling, the gradient tail outside radiusR is bounded by C∫_R^infinity r^−3dr, uniformlyi. The lower-order and boundary form terms tend to zero. By finite-dimensional modulation choose a nearby center and scale delta_i, delta_i/epsilon_i→1 and center displacemento(epsilon_i), so

v_i=chi u_i=W_i+psi_i, psi_i Q-orthogonal to all bubble Jacobi modes, ||psi_i||H1=o(1).

This is the usual elementary implicit function theorem: the limiting Gram matrix of the bubble derivatives is positive definite. The changed A_i has the same limit and the same eventual logarithmic rate, since its changeiso(epsilon_i).

2. Let Phi_i be the physical quadratic correction constructed in agent4_n4_log_proof.md, and D_i=f2_i U_t. In graph pullback coordinates the material correction is B_i=D_i+Phi_i. It obeys

|B_i|<=C|A_i|(1+r)^−1,
|DB_i|<=C|A_i|(1+r)^−2,

and the first linear graph residual is cancelled exactly. Cut it off at R_i=r0/delta_i and transfer delta_i B_i back to the physical domain. Project off the finite-dimensional kernel and call the result b_i. Then

||b_i||H1<=C delta_i |A_i| sqrt(logR_i)+O(delta_i).

The projection changes the model by O(delta_i² logR_i), because its Euclidean angular projection is zero and the metric error paired with a Jacobi mode has normO(delta_i sqrt(logR_i)). This is o(delta_i), hence harmless below.

3. The corrected model m_i=W_i+b_i has full energy-dual residual O(delta_i), uniformlyi. Here are the required radial estimates, not just qualitative smallness:

* The cut-off B_i commutator has normO(1) on its outer annulus, since B_i~r^−1 and DB_i~r^−2; multiplying bydelta_i givesO(delta_i).
* The graph error beyond its quadratic first variation isO(delta_i²r²). Applied toDU~r^−3 or to the first correction it gives bulk coefficientsbounded byCdelta_i²r^−1, whose L² norm throughR_i isO(delta_i²R_i)=O(delta_i r0).
* The rescaled mean curvature isO(delta_i²r) becauseH(p_i)=0. Its boundary source againstU has dual trace normO(delta_i²R_i)=O(delta_i r0), and againstdelta_i B_i has normO(delta_i³R_i²)=O(delta_i r0²).
* Nonlinear remainder3U(delta_i B_i)² has L^{4/3} normO(delta_i²); the cubic remainder has normO(delta_i³(logR_i)^{3/4})=o(delta_i).

Higher metric terms are absorbed by the small fixed physical r0. Exactly the same estimates hold after bounded conformal normalizations.

4. The actual cut-off solution v_i has residualO(delta_i), supported only in its fixed physical outer annulus. The uniform projected inverse from agent4_uniform_inverse_proof.md and the small nonlinear Lipschitz constant on an o(1)H¹-ball therefore give

||v_i−m_i||H1<=C delta_i.

Indeed subtract their projected equations, invert the bubble linearization, and absorb its nonlinear derivative perturbation, which tends to zero. No annular pointwise approximation is used here.

5. Write x_i=|A_i|sqrt(logR_i). Let Z_i be the scale Jacobi mode with fixed physical cutoff. Its full linearized residual satisfies

||E''(W_i)Z_i||H*<=C delta_i(1+x_i).

The quadratic graph term contributesdelta_i|A_i|sqrt(logR_i) by the radial integral∫r^−1dr; the higher jets contributeO(delta_i) by the same estimates in step3. The actual cutoff residual paired withZ_i isO(delta_i²), because both u_i andZ_i and their gradients areO(delta_i) on the fixed physical outer annulus.

The nonlinear difference between v_i andm_i, paired withZ_i, isO(delta_i²(1+x_i)): n4 has cubic nonlinearity, and its derivative perturbation isO(||b_i||+||v_i−m_i||) in the energy-dual estimate. Combining with step4 yields

|E'(m_i)[Z_i]|<=C delta_i²(1+x_i).

6. The explicitly constructed model has scale energy

E(m_delta)=E0−(pi²/30)|A_i|² delta² log(1/delta)+O(delta²),

with a uniformly C¹-controlled remainder after differentiation bylogdelta. This follows from the exact graph energy: the sole logarithm is the quadratic Jacobi energy from agent4_n4_log_proof.md; every cubic/higher coefficient has the radial powers listed in step3 and givesO(delta²) after integration to r0/delta. The cutoff annulus givesO(delta²). The same power bounds apply after one logdelta derivative. The difference between the full logscale derivative ofm_delta andZ_delta has normO(delta |A_i|sqrt(logR)+delta), so pairing it with the O(delta)model residual changes the result by at mostCdelta²(1+x_i). Hence

(pi²/15)|A_i|² delta_i² logR_i <= C delta_i²(1+x_i).

Dividing bydelta_i² gives c x_i²<=C(1+x_i), forcingx_i bounded. This proves the rate and the vanishing conclusion.

## Explicit remaining gap

The estimate above controls the error only byO(1+x_i) after dividing the Pohozaev scale bydelta_i². Sincex_i may tend to a nonzero finite value, it does NOT establish the sharp nonnegative limiting Pohozaev sign. A further sectorwise/weighted remainder argument is necessary for that sign and for the ultimate positive-mass contradiction.
'''
Path('workspace/agent4_n4_umbilicity_rate.md').write_text(rateproof)
print('Saved n4 conditional isolated-simple umbilicity rate proof.')
Path('workspace/agent4_n4_log_checks.py').write_text(Path(__file__).read_text())

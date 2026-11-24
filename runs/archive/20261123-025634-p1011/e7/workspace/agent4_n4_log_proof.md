# Dimension-four quadratic-graph logarithmic coefficient

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

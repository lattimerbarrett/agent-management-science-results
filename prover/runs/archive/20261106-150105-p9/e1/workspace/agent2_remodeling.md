GEODESIC TORUS REMODELING LEMMA (A2)
Agent2: proved core torus weight bound; lacunary line transfer outlined below.

Input: finite binary martingale positive matrices W_leaf on {-,+}^N. For node v let A_v=E_v W and B_v=E_v W^{-1}, and suppose ||A_v^{1/2}B_v^{1/2}||²<=K for every node. Choose positive eps_j with sum<=1. On the circle choose smooth theta_j with 0<=theta<=1, theta=1 outside symmetric boundary strips of total measure eps_j, and theta vanishing to all orders at 0,1/2,1. Define recursively
 F_v(t_j,...,t_N)=A_v #_{theta_j(t_j)} F_{v sign(t_j)}(t_{j+1},...,t_N),
with F_leaf=W_leaf, where A#_sB=A^{1/2}(A^{-1/2}BA^{-1/2})^s A^{1/2}.
At half endpoints theta=0, so both branches equal A_v and glue smoothly.

Geometric mean facts:
 (A#_sB)^{-1}=A^{-1}#_sB^{-1};
 A#_sB <=(1-s)A+sB <=A+B.
Furthermore for ANY interval/arc averaging operator E_J,
 ||E_J||_{L²(A#_sF)} <= ||E_J||_{L²(F)}^s,
where A is a constant matrix. This follows from complex interpolation: after applying A^{1/2}, the endpoint weights are I and A^{-1/2}FA^{-1/2}, whose interpolant is its power s. Equivalently the A2 characteristic of the geometrically interpolated weight is at most the old characteristic to power s.

Moment induction. Put C_j=1+sum_{k>=j}eps_k<=2. Off strips F_v equals F_child. On strips it is at most F_child+A_v; the inverse is at most F_child^{-1}+A_v^{-1}. Averaging gives
 E F_v <= C_j A_v,
 E F_v^{-1} <= C_j B_v,
using A_v^{-1}<=B_v by operator Jensen. The induction uses exact equal halves and symmetric strips, so the baseline average of children is bounded by C_{j+1} A_v and C_{j+1}B_v.

Sectional A2 bound. Fix prefix t_1,...,t_{j-1}, and average over an arbitrary arc J of t_j and ALL suffix variables. Before outer wrappers, at each t_j,
 E_suffix F_v <= A_v+C_{j+1}A_child <=(1+2C_{j+1})A_v<=5A_v,
and similarly E_suffix F_v^{-1}<=5B_v. Thus the arc average has A2 at most25K. Outer fixed-prefix wrappers are successive fixed geometric means with constant matrices, and cannot increase averaging norm above max(1,sqrt(25K)). Therefore every sectional lexicographic arc has A2<=25K, uniformly in depth. This is a rigorous uniform bound, not a numerical conjecture.

Approximation. Outside boundary strips in all N coordinates, F_root exactly equals the original leaf weight. The exceptional measure is at most sum eps_j, which may be arbitrarily small. Since the finite tree has bounded matrices and inverses, weighted integrals of fixed bounded functions converge to their original martingale values as eps_j->0.

LACUNARY LINE TRANSFER
For smooth positive torus weight F(t_1,...,t_N), set W_L(x)=F(L_1x,...,L_Nx) with successively very separated integers L_j. Uniformly over real intervals, the two matrix averages of W_L and W_L^{-1} approach a sectional pair: low frequencies freeze, one active frequency traverses an arc, and higher frequencies average out. To prove rigorously, approximate F,F^{-1} uniformly by finite Fourier sums; choose gaps L_{j+1}/L_j huge. Classify interval lengths so L_{j-1}|I| is tiny and L_{j+1}|I| huge. Prefix freezing errors are bounded by a Lipschitz constant times L_{j-1}|I|. Every nonzero suffix Fourier frequency has magnitude at least L_{j+1}/2, so interval averaging errors are bounded by a finite coefficient sum divided by L_{j+1}|I|. Matrix positivity converts sufficiently small absolute errors to relative Loewner errors. Hence limsup [W_L]A2_standard <=25K (up to arbitrary 1+eta).

For a trigonometric polynomial f on T^N, frequencies with separated L_j have sign(sum k_j L_j)=sign(k_last nonzero). Therefore H_circle f(Lx)=(H_lex f)(Lx) exactly, where H_lex has multiplier -i sign of last nonzero frequency. Weighted norm integrals converge by the same finite Fourier approximation/no-resonance argument. A periodic weight/test can be transferred to the real line with smooth long cutoffs; nonzero Fourier modes are approximate eigenfunctions of real H, using its multiplier -i sign. The bounded positive weight makes the cutoff errors harmless. This reduces a lexicographic Hilbert-transform lower example on the martingale torus to an actual real Hilbert-transform lower example while controlling full-interval A2.

LIMITATION: an arbitrary martingale transform or Petermichl shift is NOT automatically H_lex. A separate embedding/coherence lemma is still required, and no such missing lemma is asserted here. General-p geodesic interpolation is promising but not written/proved here.

Numerical sanity checks in agent2_geodesic_checks.py verify300 genuinely complex positive-matrix interpolation examples and3600 Loewner bounds. These do not replace the analytic interpolation proof above.

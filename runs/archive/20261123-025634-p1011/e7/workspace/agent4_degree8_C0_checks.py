import sympy as s
from pathlib import Path
n=s.symbols('n',real=True)
# All divergent-tail exponents are largest at n=19.
assert 8-s.Rational(30-19,2)==s.Rational(5,2)>0
assert 16-(22-s.Rational(19,2))==s.Rational(7,2)>0
assert 8-(23-19)==4>0
assert s.simplify((n-2)/2-8-(n-18)/2)==0
assert s.simplify(n-2-16-(n-18))==0
assert s.simplify(n-9-8-(n-17))==0
# Radial powers derived independently from dimension, graph derivative degree.
assert s.expand((n-1)+2*(7+1-n))==15-n
assert s.expand((n-1)+2*(14+1-n))==29-n
assert s.expand((n-2)+(20+4-2*n))==22-n
assert s.simplify(22-n+s.Rational(1,2)*n)==22-n/2
print('Degree-eight source, remainder, cutoff and dominance exponents checked symbolically.')

proof=r'''# Degree-eight extension of the uniform C0 reduced-energy expansion

This extends agent2_C0_energy_expansion.md to a fixed degree-eight graph profile in dimensions n>=19. It is independent of whether a certified full parameter minimum has yet been found in a given dimension.

Let f(z)=H2(z) sum_{k=0}^3 a_k |z|^{2k}, where H2=z1²−z2², and let f_R=χ(z/R)f. Its derivatives obey |D^j f_R|<=C_j(1+|z|)^{8−j}, uniformly R. Let epsilon→0, rho→0, R=rho/epsilon→infinity, mu=epsilon^8, choosing epsilon=e^{−L−j²}, rho=2^{−j−5}. Let bubble parameters range in a fixed compact set with scales bounded away from0. Assume the uniform projected inverse and contraction lemma already proved in the named workspace files.

## Statement

The projected corrected energy satisfies, uniformly in these parameters,

E(V_jtheta+w_jtheta)=E_halfspace(U)+mu_j² F_f(theta)+o(mu_j²),

where F_f is exactly the second-order negative physical shape Hessian computed by the hemisphere spectral method. All estimates below hold for every n>=19. The proof does not assert existence of a parameter minimum; if one is certified, the fixed-domain minimization construction applies without further analytic changes.

## Exact energy and first-order cancellation

In rescaled vertical graph coordinates the exact energy is

E_mu(v)=1/2∫[|Dv|²−2mu f_a v_a v_t+mu²|Df|²v_t²] − [(n−2)²/2]∫(v_+)^q
 +c_n∫_{t=0}[mu Δf−mu³ f_a f_b f_ab/(1+mu²|Df|²)]v².

For every compact f_R, its first graph variation J1(U_theta) vanishes exactly, since

∫_0^∞ (U_theta)_a (U_theta)_t dt=−c_n ∂_a(U_theta(z,0)²).

The same holds in the polynomial limit after the estimates below. Thus the linear source S=J1'(U) annihilates the translation/scale Jacobi kernel.

## Leading source and direct quadratic term

Df=O(r7), Δf=O(r6), U=O(r^{2−n}), DU=O(r^{1−n}). The leading bulk source has coefficient Df DU=O(r^{8−n}); its squared radial tail is ∫r^{15−n}dr, finite for n>16. The boundary source Δf U has the same order; the dual trace exponent 2(n−1)/n gives the identical condition n>16. The quadratic direct energy J2(U)=(1/2)∫|Df|²U_t² is finite under the same condition. Consequently S_R→S in the energy dual and J2_R(U)→J2(U), uniformly in compact bubble-parameter sets.

## Divergent higher terms are still negligible

Higher coefficients need not be integrable without their powers of mu. Retain both R and mu:

* The second-order bulk residual has coefficient |Df|²DU=O(r^{15−n}); its dual norm is bounded by C[1+R^{max((30−n)/2,0)}], with sqrt(log R) at n30. Dividing its mu² factor by the target source scale mu leaves mu R^{max((30−n)/2,0)}. For n>=19 the power of epsilon is at least 8−11/2=5/2>0.

* Put K=f_a f_b f_ab=O(r20). The cubic boundary energy has coefficient K U² and radial integral bounded by C[1+R^{max(23−n,0)}], with log R at n23. Relative to mu² its factor is mu R^{max(23−n,0)}, whose epsilon power is at least8−4=4>0.

* The cubic boundary residual has coefficient K U=O(r^{22−n}); its dual trace norm is bounded by C[1+R^{max(22−n/2,0)}], with a logarithmic power at n44. Relative to mu it contributes mu²R^{max(22−n/2,0)}, whose epsilon power is at least16−25/2=7/2>0.

The remaining powers of rho are nonnegative in all three displayed remainder bounds, so they only improve convergence. Borderline logs are negligible against the strictly positive epsilon powers. The exact denominator 1+mu²|Df|² is harmless because mu R7=epsilon rho7→0.

On arbitrary energy-bounded test functions the full graph bilinear-form perturbation is O(mu R7+mu²R14+(mu R7)³)=o(1). The boundary estimate uses the L^{n−1} norm of mu Δf and the critical trace embedding.

## Bubble cutoffs

The usual cutoff energy error is O(R^{2−n}) and the dual residual is O(R^{−(n−2)/2}). Here

R^{−(n−2)/2}/mu=epsilon^{(n−18)/2}rho^{−(n−2)/2}→0,
R^{2−n}/mu²=epsilon^{n−18}rho^{2−n}→0.

These limits hold for the explicit exponential/quasi-exponential sequences above. The first graph energy variation of a cut-off bubble is O(R^{9−n}), by integrating the radial tail r^{8−n}. Its contribution relative to mu² is R^{9−n}/mu=epsilon^{n−17}rho^{9−n}→0. Thus no linear cutoff term survives.

## Correction and energy convergence

The preceding estimates give E'(V_j)=mu S+o(mu). The uniform inverse and critical p in(1,2) contraction imply ||w_j||=O(mu). Let W be the compatible halfspace Jacobi correction LW=−S, orthogonal to its kernel. Cut W off at a fixed fraction of R and transfer it into the jth patch. Its finite Dirichlet energy and compact-parameter continuity make all cutoff tails o(1), without any rate assumption. The graph form perturbation is o(1). Subtracting mu times this comparison correction from the actual projected correction, and applying the uniform inverse, gives

||w_j−mu W_j||=o(mu).

The nonlinear residual is O(mu^p)=o(mu), and the nonlinear energy Taylor remainder is O(mu^q)=o(mu²), where q=2n/(n−2)>2. Hence

F_f=J2(U)+S(W)+(1/2)L(W,W)=J2(U)−(1/2)L(W,W).

This proof is identical to the quartic case once the retained mu,R bounds replace unjustified integrability of higher terms.

## Identification with the physical shape Hessian

Let G_R=f_R U_t. For each compact f_R, the unchanged physical bubble pulled back from the moving domain is U+mu G_R+O(mu²). Its domain energy has zero quadratic shape coefficient by evenness of the bulk density in t and oddness of H dσ. Since E0'(U)=0, the second derivative of this function path contributes zero exactly, giving

J2_R+S_R(G_R)+(1/2)L(G_R,G_R)=0.

Now G_R converges in D^{1,2} to G=f U_t precisely when n>16 (its gradient is O(r^{8−n})). All three terms therefore converge; NO global D^{1,2} bound on f²U_tt is needed, because its coefficient was annihilated by E0'(U) BEFORE taking the limit. Consequently

F_f=−(1/2)L(W−G,W−G),

exactly the physical correction shape form previously diagonalized on the hemisphere. Kernel gauge changes leave this value unchanged.

## Fixed smooth graph realization

At the jth physical patch the profile is h_j(z)=epsilon_j mu_j f((z−p_j)/epsilon_j), cut off at rho_j. Its four polynomial coefficients scale respectively as epsilon_j^7,epsilon_j^5,epsilon_j^3,epsilon_j. Every derivative is bounded by sums of epsilon_j^{7−2k}rho_j^{2k+2−ell}. Thus the same disjoint-support/flat-accumulation geometry as in agent1_n32_construction.md is C∞, arbitrarily C²-small, and preserves positive Yamabe type. If a strict full parameter minimum is certified in a particular n>=19, this lemma and the existing inverse/contraction/trace argument give an actual fixed-domain blowup sequence in that dimension.

No part of this lemma treats n7 through18 or proves low-dimensional compactness.
'''
Path('workspace/agent4_degree8_C0_extension.md').write_text(proof)
Path('workspace/agent4_degree8_C0_checks.py').write_text(Path(__file__).read_text())
print('Saved degree8 C0 extension proof and executable exponent checks.')

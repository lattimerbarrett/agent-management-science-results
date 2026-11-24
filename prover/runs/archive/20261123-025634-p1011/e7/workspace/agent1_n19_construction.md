# Audited partial noncompactness theorem: every n>=19

Theorem proved by the assembled lemmas: for every integer n>=19 there is one fixed smooth compact connected Euclidean domain, with positive Yamabe type, locally conformally flat up to its smooth nonempty boundary and not conformally equivalent to the hemisphere, carrying smooth positive solutions of the equation in the question with boundary maximum tending to infinity.

This is a PARTIAL result. It does not prove the requested dimensions7 through18, or compactness in dimensions3 through6.

For n>=32 use the fully integrated construction in agent1_n32_construction.md. Its analytic ingredients and fixed geometry were independently audited by agents2 and4. For each remaining integer n=19,...,31 make the following replacements, with no other change in the proof.

## Certified fixed local profile

Set H2(z)=z1²−z2² and
f(z)=H2(z)[1−(4628/10000)|z|²+(5655/100000)|z|4−(1408/1000000)|z|6].

The exact second-order physical shape functional F_f(lambda,xi) has a strict nondegenerate local minimum at (sqrt(z_n),0). The root z_n is rigorously certified in the following rational intervals (endpoints displayed as numerator/10^10):

n19: [9024309988,9024309989]/10^10;
n20: [8587674198,8587674199]/10^10;
n21: [8449730421,8449730422]/10^10;
n22: [8373851342,8373851343]/10^10;
n23: [8324948173,8324948174]/10^10;
n24: [8291359557,8291359558]/10^10;
n25: [8267650668,8267650669]/10^10;
n26: [8250793059,8250793060]/10^10;
n27: [8238911685,8238911686]/10^10;
n28: [8230761131,8230761132]/10^10;
n29: [8225470901,8225470902]/10^10;
n30: [8222408623,8222408624]/10^10;
n31: [8221101098,8221101099]/10^10.

The exact proof and general formulas are in agent2_degree8_profile_proof.md. The actual executable certificate is agent2_profiles_n19_n31_certificates.py with helper agent2_polynomial_search.py. The certificate uses polynomial identities and rational interval arithmetic, not inferred floating-point roots. It verifies radial derivative sign change, radial second derivative, and all translation Hessian signs on each interval. The root approximations printed by the script are diagnostics only; the final assertions are rational certificates. Independent n19 translation computation is in agent4_n19_translation_numeric.py (corroboration, not the certificate).

## Fixed smooth realization

Use the seed Omega0, centers p_j, disjoint radii rho_j, and epsilon_j=exp(-L-j²) in agent1_fixed_domain_geometry.md. Put mu_j=epsilon_j^8 and replace the graph bumps by
h_j(z)=chi(|z−p_j|/rho_j) epsilon_j mu_j f((z−p_j)/epsilon_j).
The physical coefficients of homogeneous degrees2,4,6,8 scale as epsilon_j^7,epsilon_j^5,epsilon_j^3,epsilon_j. For each derivative order ell,
||D^ell h_j||<=C_ell sum_{k=0}^3 epsilon_j^(7−2k)rho_j^(2k+2−ell)
<=C'_ell epsilon_j rho_j^(8−ell),
for epsilon_j<rho_j. Thus the sum is C∞ and flat at the accumulation point, and arbitrarily C²-small when L is large. Positive Yamabe coercivity, exact Euclidean local conformal flatness, connectedness, and the preserved nonumbilic side point follow exactly as in the quartic construction.

## Quantitative analytic replacements

Let R_j=rho_j/epsilon_j. Then mu_jR_j7=epsilon_j rho_j7 ->0 and
R_j^(-(n−2)/2)/mu_j=epsilon_j^((n−18)/2)rho_j^(-(n−2)/2)->0,
R_j^(2−n)/mu_j²=epsilon_j^(n−18)rho_j^(2−n)->0,
for every n>=19. The exact degree8 C0 expansion is proved in agent4_degree8_C0_extension.md with executable exponent checks agent4_degree8_C0_checks.py. Crucially, higher polynomial tails are NOT assumed integrable: retaining their mu and R factors makes them negligible. The first source and quadratic energy are integrable for n>16, the only unconditional integrability needed. The worst extra epsilon exponents in the remainders at n19 are5/2,4,7/2, all positive.

The same uniform projected inverse from agent4_uniform_inverse_proof.md applies on the one fixed final domain. The contraction/positivity/smoothness/reduced-minimum/trace argument in agent1_nonlinear_reduction.md applies unchanged. Consequently the uniform expansion J_j=E_halfspace+mu_j²F_f+o(mu_j²) produces interior reduced minima, hence actual smooth positive solutions. Their boundary maxima are >=c epsilon_j^(-(n−2)/2) and diverge.

## Audit status

Agent1 independently executed all13 finite-dimension certificates and the degree8 exponent checker, exit0. Agents2 and4 independently audited the graph-energy identification, projection invariance, uniform inverse and C0 remainder. The theorem above is the resulting nonsharp high-dimensional existence result, not the full D={n>=7} theorem.

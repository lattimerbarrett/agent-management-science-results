# Agent 2 proof inventory (scope explicit)

The requested dimension theorem is NOT proved by these files.

## Proved geometric/analytic lemmas
- agent2_finite_spin_cover.md: compact LCF manifolds have finite spin cover;
  classical developing-map and Malcev inputs explicit, independently audited.
- agent2_robin_pohozaev_identity.md: exact flat-domain Robin critical identity.
- agent2_reverse_LS_lemma.md: quantitative modulation and reverse LS for alln,
  conditional on strong global single-bubble H1 approximation.
- agent2_C1_LS_reduction.md: differentiated correction and corrected C1 energy
  reduction under explicit residual/inverse/compact-transfer hypotheses.
  Density is smooth compact support in CLOSED halfspace, unrestricted trace.

## Conditional endgames (not unrestricted blow-up extraction)
- agent2_conditional_green_mass.md: positive AF boundary Green mass via finite
  spin cover, assuming AF/Green expansion and classical spin boundary PMT.
- agent2_conditional_interior_exclusion.md: excludes a single interior pole
  in a positive harmonic Neumann Green limit of smooth semilinear solutions.
- agent2_finite_cluster_exclusion.md: extends this to finite pole clusters.
- agent2_fixed_interior_exclusion.md: fixed interior simple Green blow-up,
  using compact-minimal-boundary spin PMT as an explicit classical input.

## Executable exact checks / independent audits
- agent2_even_low_gram_checks.py: all30 even-n<=16 subcritical polynomial
  angular dilation blocks, exact rational infinite-series sums and minors.
- agent2_audit_odd_checks.py: audits odd recurrence/Machin and all39 certified
  odd-n<=17 blocks (uses agent3 exact rational interval checker).
- agent2_pohozaev_checks.py, agent2_pohozaev_identity_checks.py:
  exact Green mass flux and critical stress algebra.
- agent2_interior_peak_flux_checks.py, agent2_neumann_image_force_checks.py:
  exact image-pole normal stress/force signs.
- agent2_cover_mass_checks.py: ground-state product and smooth Green addition.
- agent2_symbolic_ratio_checks.py: essential factorial in Jacobi ratios.
- agent2_audit_seed19_alln.py: independent alln>=19 seed certificate audit,
  strengthened strict n29 endpoint constants.
- agent2_reverse_LS_exponent_checks.py: alln critical Holder identities.

## Remaining gaps in requested task
1. Existence in ambient n=18 (team's complete construction only covers n>=19).
2. Unrestricted blow-up extraction/simple estimates in dimensions3..17.
3. Quantitative general boundary jet/Pohozaev and AF asymptotics tying actual
   arbitrary blow-up to the checked finite algebra and Green mass.
No precise recent source/theorem statement was supplied despite requests.

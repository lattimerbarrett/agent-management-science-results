# Exact extremal-cycle coefficient thresholds

The answer is S_2=[0,infinity), S_3=[5/18,infinity), S_4=[7/32,infinity),
and S_r=[2/(2r+1),infinity) for r>=5. Every finite endpoint is included.

## Reproduce the actual finite checks
Run `python run_checks.py` in an environment with Python 3, networkx, numpy,
sympy and z3-solver. No network calls or external programs are used.
The 12-program runner has been executed successfully; the included manifest
contains the scope, source SHA256, captured output, and timing of every test.
These tests supplement the general mathematical arguments; they are not
claimed as replacements for infinite-parameter proofs.

## Proof organization
1. `agent2_H17_complete_witness_proof.md`: the entire r=2 argument.
2. `agent2_tree_cycle_expansion.md` and `agent2_uniform_imbalance_lemma.md`:
   cycle asymptotics and the uniform Perron/Fourier proof including tails.
3. `agent3_rotation_transfer_lemma.md` and `agent4_finite_hole_template_lemma.md`:
   near-Turan cycle-extremizer regularization and bounded component/holes.
4. `agent2_phase_bound_proof.md` and `agent4_rge3_lower_assembly.md`:
   exact lattice optimization and the universal lower exclusion.
5. `agent3_profile_gadget_lemma.md` and `agent4_finite_phase_basis.md`:
   self-contained finite-graph realization of the sharp phase examples.
6. `agent2_endpoint_wedge_lemma.md` and `agent4_programmed_upper_theorem.md`:
   sharp examples, including the delicate r=4 endpoint.

The proof uses only two classical general results without reproving them:
Erdos--Simonovits stability (with Erdos--Stone) and Bregman's permanent
inequality. In particular it does not assume any unproved normality theorem
or any stronger Simonovits exact extremal classification.

The older scope warnings in individual component lemmas specify what those
lemmas prove individually, not a gap in the combined argument. The lower
assembly's uniform-imbalance step is supplied by the dedicated completed
uniform-imbalance file. All assignments are now complete.

# Complete proof and exact certificate

This directory contains a complete proof of the stated maximum-commute-time formula, including every degree and both parities. The proof is in PROOF.md; individual chapters and exact enumerators are in workspace/.

## Running the certificate

Use a Python interpreter with SageMath, NetworkX and SymPy available:

    python RUN_ALL.py

No external programs, downloads, nauty/geng, random searches, floating-point approximations, or assumed extrema are used. The default run recomputes EVERY proof-critical finite graph enumeration, including all one-port/two-port four-regular networks through order13. It also checks all small flow atoms, exact rational inequalities, all extremal modules, and full constructions at sample orders. All-order extensions are proved in PROOF.md by explicit series formulae and affine inequalities, not inferred from the samples.

The complete critical enumeration was rerun successfully: the local4 part took45.7seconds, and every other certificate including constructions took5.1seconds in our environment. These are observations, not timing requirements. --fast skips ONLY the order6..13 local4 enumeration; it is for convenience, not the complete certificate.

Finite enumeration coverage: graphs_degseq recursively processes vertices. Among unprocessed vertices, those with identical residual degree and identical previously processed neighbors are interchangeable. For each such class the next neighborhood can be chosen as a prefix of any specified size. Permuting within the class identifies every other choice with that prefix and preserves all completions. Induction proves that every graph with the degree sequence occurs up to relabeling. In role-sensitive uses, distinguished vertices are processed first, have different original degrees, have equal injection roles within each interchangeable class, or all roles are assigned exhaustively after generation. The degree inequalities used to prune are necessary counting inequalities. Hence no admissible network is omitted.

Each finite resistance/energy is obtained by inverting a reduced INTEGER Laplacian over QQ (or SymPy rationals). If j is the zero-sum prescribed injection and Z the grounded inverse, the exact energy is j_reduced^T Z j_reduced. There are no numerical tolerance tests.

The JSON files are records of actual completed runs, not substitutes for the executable enumerators. RUN_ALL.py recomputes the results rather than trusting the records.

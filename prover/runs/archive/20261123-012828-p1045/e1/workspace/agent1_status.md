# Status and rigorously proved pieces

1. Full lower half at every alpha and epsilon: agent2_lower_proof.md.
2. Exact all-blue diagonal weighted matrix sharp frontier: agent4_blue_loop_proof.md.
3. All-red diagonal case: agent3 all_red_loop_checks.py plus Goodman derivation.
4. Mixed diagonal case: below sqrt(a)+sqrt(b)=1, red-loop nodes form a pure red clique of weight at most a (a<=1/4); proved by nonnegative Hilbert two-row lemma.
5. Endpoint alpha=1: Goodman identity gives r(B_n,B_n)<=4n+2, random lower gives coefficient4. Exact and exhaustive checks agent1_goodman_checks.py.

GAP: No proof of the sharp upper bound for genuinely mixed internal-loop colors. Neither the pure-loop matrix lemma nor regularity allows one to discard these vertices without a new charging/variational lemma. A claimed complete proof that just invokes an all-blue regularity partition would be invalid.

All files have actually been written and the stated check scripts run. Current flag SDP searches seek a finite verifiable certificate, not yet found.

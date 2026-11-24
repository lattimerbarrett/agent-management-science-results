# Minimum-three-active-matching-parts obstruction

Write W=K_1 join C_4 (five vertices), Q=K_1 join P_4 (the gem), and J=K_1 join (W disjoint-union Q). Then chi(J)=4 and deleting its outermost cone vertex leaves a 3-colorable graph.

J is NOT contained in a complete tripartite graph with matchings inside at most two parts.
Proof: let x be its outer cone vertex. If x lies in an unmatched part, its neighborhood is complete bipartite with matchings in both parts. That graph is W-free: every vertex neighborhood is a cone over a matching, which has no C4. If x lies in a matched part, its neighborhood is a single universal vertex u joined to a complete bipartite graph with a matching in at most one part. Every W in the neighborhood must use u, since the latter bipartite-plus-matching graph is W-free. But then the disjoint gem must occur in the one-matching bipartite graph, which is gem-free: neighborhoods are either matchings or stars, neither containing P4. Contradiction.

J IS contained in the host with matchings in all three parts. Use one matched edge xu in the first part. Map the outer cone vertex to x and the hub of W to u; realize its rim C4 in the other two parts. Realize a disjoint gem in those same two parts, using one matching edge in each. All necessary edges from x and u are available. Explicit finite Z3 witness is saved in agent2_J3_checks.json.

J IS contained in the complete tripartite graph with a single internal P3: use its center as x and its two leaves as the separate hubs of W and Q. Embed the rim C4 and path P4 disjointly in the other two independent parts.

For r>3, join J to r-3 independent palettes of size L>2r. The matching-part threshold remains three. Indeed each palette has at least three vertices in one host part; since internal maximum degree is one, no vertex of any other joined palette or of J can occupy that reserved part. The palettes reserve distinct parts, leaving exactly three host parts for J. Conversely the construction embeds using one clean host part per palette. The single-P3 decomposition also persists, using clean parts for all palettes.

The executable agent2_J3_checks.py independently verifies the r=3 embedding/nonembedding assertions by injective Z3 constraints (not just color heuristics).

# H47 diagnostic: proof of the n/4 extremal upper bound without Simonovits D

This note concerns the fixed graph H from agent2_glue_b_vs_clique.json. The following facts suffice:
(A) H has chromatic number3 and H-v is bipartite for a vertex v.
(B) H embeds in the complete join of an independent set with sufficiently many disjoint P3's.
(C) H embeds in the complete join of two sufficiently large matchings (isolates may be added).
(D) The complete join of a matching and an independent set is H-free.
The actual finite embeddings for A--C have been checked separately; D follows, for example, from the independently certified larger H-free S-host.

## High-minimum-degree structural lemma
For every fixed constant C, an H-free graph G on n vertices with delta(G)>=n/2-C has, for sufficiently large n, a partition A,B such that
 |A|,|B|=n/2+O_{H,C}(1),
 max internal degree=O_H(1),
 max missing-cross degree=O_{H,C}(1),
 and e(G)<=t2(n)+n/4+O_{H,C}(1).

Proof. By ordinary Erdos--Simonovits stability, e(G)>=n^2/4-O_C(n) gives an initial near-balanced bipartition with o(n^2) internal edges and o(n^2) missing cross edges. Remove o(n) bad vertices, leaving a core whose maximum missing-cross degree is o(n). Every removed vertex has o(n) neighbors in one core part: otherwise it sees at least eta n vertices in both core parts for some eta>0, and these neighborhoods contain a fixed complete bipartite graph K_{h,h}, because every core vertex misses o(n) neighbors across the core partition. Together with that vertex, K_{h,h} contains H by (A). Assign the removed vertex to a core part where its degree is o(n). All new part sizes are n/2+o(n), and every vertex has o(n) internal degree. The lower degree bound then makes every vertex's missing-cross degree o(n).

By (A), H embeds into a complete bipartite graph with a fixed star added to one side (place the critical vertex at the center, and use a proper2-coloring of H-v). Hence an internal star of sufficiently large fixed order in either part, all of whose vertices now have o(n) cross defects, extends greedily to H. Therefore the maximum internal degree is bounded by a constant D_H.
If m is the larger part, any vertex there has degree at most n-m+D_H, so m<=n/2+C+D_H. Thus both part sizes differ from n/2 by a bounded constant. The degree lower bound now yields a bounded missing-cross degree B_{H,C}.

By (B), the internal graph in either part cannot contain more than a fixed number p_H of vertex-disjoint P3's. Indeed the other H-vertices can be chosen greedily in the opposite part, avoiding the bounded cross nonneighbors of the O_H(1) fixed vertices. Remove the vertices of a maximal P3-packing in each part; at most6p_H vertices are removed. Their internal incident edges are O_H(1), since internal degree is bounded. The remaining internal graphs are matchings.
If both matchings have at least a sufficiently large fixed number q_{H,C} of edges, choose the finitely many required edges in one part, and then choose the required matching edges in the other part avoiding their bounded cross nonneighbors. Fill isolated positions greedily. This embeds H by (C), a contradiction. Consequently only one matching can have unbounded size. The total number of internal edges is at most half of one part size plus O_{H,C}(1), namely n/4+O_{H,C}(1). Adding at most |A||B| cross edges proves the displayed upper bound.

## Progressive-record argument
Put g(n)=ex(n,H)-t2(n)-n/4. If g were unbounded above, it would have arbitrarily large record values. At a strict record n, every extremal G satisfies
 delta(G)>=ex(n,H)-ex(n-1,H)>floor(n/2)+1/4,
so delta(G)>=floor(n/2)+1. Apply the high-minimum-degree structural lemma with C=1. Its constant is uniform over these record graphs, giving g(n)<=C_H, contrary to unbounded record values. Hence there is a constant C_H with
 ex(n,H)<=t2(n)+n/4+C_H
for every sufficiently large n (and after increasing C_H, for every n).

By (D), a balanced complete bipartite graph with a maximum matching in one part is H-free, so ex(n,H)>=t2(n)+n/4-O(1). Combining lower and upper bounds shows EVERY edge extremizer has delta(G)>=n/2-O_H(1). Therefore the structural lemma applies to every edge extremizer, not merely to one chosen Simonovits extremizer.

Finally its abundant matching has size n/4-O(1). The actual H47 embedding A2P3 + matching-fillers, B independent, therefore implies each full part has P3-packing number at most1: any two P3's can be used in the finite embedding, and the matching fillers can be chosen from the abundant matching avoiding all bounded cross defects. Thus there is at most one nonmatching connected internal component in each part. The remaining, stronger actual embeddings give the degree and branch exclusions used in the counterdiagnostic. This part needs no cycle-maximizer structural theorem whatsoever.

## Why this matters
If the positive embedding certificates and the independently verified S/T-free certificates are sound, a failure to apply the Simonovits D-theorem cannot save the prescribed S2 answer: the exact n/4 slope upper bound follows from standard Turan stability and the above elementary argument alone.

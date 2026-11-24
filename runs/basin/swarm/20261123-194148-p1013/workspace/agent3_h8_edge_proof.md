# H8 exact edge theorem, using Simonovits's linear-forest structure theorem

H has V={0,...,7} and E={04,05,06,07,13,17,23,26,27,47,57,67}.
It has chromatic number3 and H-7 is a bipartite tree.

The standard Simonovits theorem needed is the following precise structural consequence:
If a fixed3chromatic F embeds in P_l join I_l, then every sufficiently large edge-extremal F-free graph has a bounded exceptional set X, outside which it is the join of two graphs A,B of orders n/2+O(1); each is a union of bounded-order connected components, with finitely many component types, each occurring either boundedly often (absorb in X) or linearly often. Adjacency from x in X to copies of a given component type is identical under the component identifications.
[This is a classical theorem to cite accurately, not proved here.]

H embeds P4 join I4 via internal vertex set{0,2,3,7}, so apply theorem.
For x in X, if it has any neighbors in linearly repeated types of both A,B, it has linearly many neighbors in each. H-7 is bipartite, hence embed it into these two neighborhood sets, mapping7 to x: forbidden. Thus x has no neighbors in bulk of at least one part; assign x to such a part.
If x misses any role in any repeated component type opposite its assigned part, it misses Theta(n) opposite vertices. Replace x with a vertex having all opposite-bulk neighbors and no other neighbors. This remains H-free: any new H using x maps x to an unused vertex in bulk of assigned part, since all its H-neighbors lie in opposite bulk. Edge number gains Theta(n)-O(1), contradiction. Therefore every exceptional vertex is complete to opposite bulk and anticomplete to own bulk.

H embeds in complete bipartite+P4, +claw, and +triangle onepart. Therefore each assigned internal graph (including exceptional vertices and their internal edges) has no P4/claw/triangle: use opposite bulk for independent side of these embeddings. Consequently each internal component is a path on at most3vertices.

There is a bulk internal edge, because otherwise allinternal edges lie in bounded exceptional sets, contradicting ex(n,H)>=t2(n)+n/3-O(1). H embeds a matching-one-edge-in-each-part host: internal partition{1,2,4,5,6} has soleedge26, and complement{0,3,7} has soleedge07. Consequently if onepart has a bulk internal edge, the oppositepart can have NO internal edge, including among exceptions: map those twoedges to witnessedges, use remaining bulk vertices, and allcross adjacencies needed are complete (atleast oneendpoint lies inbulk for each crosspair between witnessedges). Thus allinternal edges lie inonepart.
Now original graph is a subgraph of complete bipartite+P3union-onepart. The latter is H-free by the direct noembedding proof below. Edge extremality forces allcross edges present and maximum possible internal edges. Thus
ex(n,H)=max_a [a(n-a)+floor(2a/3)] for sufficiently large n.
At n=6k the unique optimizing a is3k, since difference at a=3k+d is -d^2+floor(2d/3), strictly negative for d!=0. Maximum internal packing on3k vertices is kP3.

Direct noembedding proof: Let B be independent and A induce P3union. If7 in B, all neighbors U={0,1,2,4,5,6} lie A, and0 has3 internal neighbors4,5,6. Otherwise7 in A; C=A intersect U has at most2 elements and is a vertex cover of H[U] (edges04,05,06,26). Every such cover is{0,6} or{0,2}. First produces triangle067. Second produces P3(0-7-2), with1 inB forcing3 inA, extending to a4vertex component by edge23. Contradiction.

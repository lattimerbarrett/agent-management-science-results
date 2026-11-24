# A bounded-excess odd-order witness: S_2=[0,infinity)

Let H consist of two vertex-disjoint double stars D_1,D_2, each with adjacent centers a_i,b_i and three pendant leaves U_i at a_i and three pendant leaves V_i at b_i, together with a vertex v adjacent to ALL twelve leaves and to no centers. Thus |H|=17. The graph H-v is bipartite. Each double star together with v contains a 5-cycle, and the two such 5-cycles meet only at v. Therefore chi(H)=3 and v is its UNIQUE critical vertex.

## Three exact embedding facts

1. H embeds into a complete bipartite graph with TWO disjoint internal edges in one part: put all four centers in that part, using the two edges, v in its pure bulk, and all twelve leaves in the opposite pure bulk.

2. H embeds into a complete bipartite graph with ONE internal star of six leaves. In every proper bipartition of each connected double star, exactly three of its leaves lie in each color class. Hence in EVERY proper bipartition of H-v, exactly six neighbors of v lie in each class. Put v at the star center, the corresponding six leaves at its internal neighbors, and all remaining source vertices into pure bulk according to that bipartition. Conversely H is FREE in complete bipartite plus ONE internal star with at most five leaves: deleting the host star center makes the host bipartite, so every H-copy would use that center and its preimage would be the UNIQUE critical vertex v; six internal neighbors are required.

3. H embeds into any complete-bipartite-bulk template with ONE internal edge in A and ONE internal 3-leaf star in B, EVEN IF arbitrary crossedges among the finitely many active vertices are missing. Put v into pure bulk A. The centers of D_1 occupy the A-edge, and all six leaves of D_1 occupy pure B bulk. In D_2, put b_2 at the B-star center and its three V_2-leaves at the B-star leaves. Put a_2 in pure A bulk and its three U_2-leaves in pure B bulk. Every required crossedge touches pure bulk, so no active-active crosshole matters.

## H-freeness of a triangle in EACH part

Let G be complete bipartite plus one triangle in each part, and suppose H embeds. By symmetry let the image of v lie in A.

If v occupies pure A bulk, all twelve leaves lie in B. A center in B would require three internal B neighbors, impossible in a triangle. Thus all four centers lie in A and their two disjoint edges would be internal A, impossible since its triangle has matching number one.

Otherwise v occupies an A-triangle vertex; at most two leaves can lie in A. If either double star has both centers in A, its center-edge consumes the other two A-triangle vertices. No A-leaf position remains; hence no center can lie in B, again forcing two disjoint A center-edges, impossible. Thus EACH double star has a B center. Every B center needs at least one A leaf, since its internal B degree is at most two. There are at most two A leaves in total, so there is exactly one B center and one A leaf per double star. Each B center then requires two B leaf-neighbors, giving TWO vertex-disjoint internal P3's in B, impossible in one triangle. This contradiction proves H-freeness.

## Exact edge-extremizers for all sufficiently large n

Use the genuine Simonovits linear-forest decomposition theorem (applicable by fact1): an edge-extremizer has a bounded exceptional set and complete bipartite bulk, with bounded symmetric internal components. Fact1 bounds the total internal matching number in EACH assigned part by one; fact2 bounds internal maximum degree by five. Standard assignment of exceptional vertices is justified as follows. An exceptional vertex joined to both bulk parts embeds H by criticality of v. One joined to neither bulk part can be replaced, simultaneously with all such vertices, by a pure vertex in an assigned part, gaining Omega(n) edges at bounded cost; every new H-copy remaps new pure vertices to unused old bulk. Hence every exception misses exactly one bulk part and is complete to the other. Assign it to its missed part; only exceptional-exceptional crossholes remain. All matching/star embeddings above use pure opposite bulk and remain valid despite these holes.

An internal graph of matching number at most one is a star, a triangle, or empty. If one part has no internal edges, the other contributes at most five edges. If both parts have internal edges, fact3 forces their internal maximum degrees to be at most two, so each contributes at most three edges, with equality ONLY a triangle. Therefore

 e(G)<=|A||B|+6<=t_2(n)+6.

The balanced graph with a triangle in each part is H-free and attains this bound. Equality forces balanced part sizes, BOTH triangles, and NO crossholes. Thus for every sufficiently large n,

 ex(n,H)=t_2(n)+6,

and every edge-extremizer is precisely T_{n,2} with one triangle in each part, up to isomorphism.

## Odd-order cycle separation

Put n=2m+1 and use K_{m,m+1} as baseline B_m. Write I_j=I_j(2)=sum_{s>=0}1/(s!(s+j)!). A single fixed internal edge in the smaller part contributes

 C_A=(m-2)!(m+1)! sum_{s=0}^{m-2}1/(s!(s+2)!),

and one in the larger part contributes

 C_B=(m-1)!m! sum_{s=0}^{m-1}1/(s!^2).

Meanwhile

 c(B_m)=m!(m+1)!/(2m) sum_{s=0}^{m-2} [m/(m-s)]/(s!(s+1)!).

Consequently C_A/c(B_m)=beta_A/m+O(m^-2), C_B/c(B_m)=beta_B/m+O(m^-2), where beta_A=2I_2/I_1 and beta_B=2I_0/I_1=beta_A+2. For any fixed internal graph, cycles using at least two internal edges contribute only O(m^-2) relative to baseline, by contracting its finitely many selected internal path forests; cycles wholly internal are negligible.

Thus edge-extremizers (three edges in each part) satisfy

 c(E_m)/c(B_m)=1+3(beta_A+beta_B)/m+O(m^-2).

The graph A_m obtained by putting ONE star with five leaves in the LARGER part is H-free by fact2, has t_2(n)+5 edges, and satisfies

 c(A_m)/c(B_m)=1+5beta_B/m+O(m^-2).

Their first-order difference is 5beta_B-3(beta_A+beta_B)=4-beta_A>0. Indeed I_1-2I_2=sum_{s>=0}s/[s!(s+2)!]>0, so beta_A<1. Therefore c(A_m)>c(E_m) for all sufficiently large m.

No edge-extremizer is a cycle-extremizer for these infinitely many odd orders. Since ex(n,H)=t_2(n)+6, the witness has slope a=0. All nonnegative larger slopes also qualify. Hence S_2=[0,infinity), with 0 INCLUDED.

The cycle formulas and all finite embeddings are checked independently by agent2_H17_odd_a0_checks.py and the team's exact cycle counters. This note supplies the short HUMAN finite-template classification, removing any reliance on unexplained CEGAR enumeration.

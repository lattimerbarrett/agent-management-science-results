# Construction and realization blocks (agent 3)

## 1. A finite coloured-profile realizer for r>=3

A profile consists of finitely many graphs assigned to prescribed host
parts, with NO edges required between different parts. Assume each profile
has a monochromatic edge, and all profile graphs are r-colourable. Suppose
one profile is the single-part star K_{1,L}. There is a fixed H, chi(H)=r+1,
with these properties, provided all parts are sufficiently large:

(A) In ANY r-partitioned graph with internal maximum degree <=L-1,
containing H implies containing one of the profiles internally.
(B) In a graph whose parts are n/r+O(1), internal degree <=L-1 and each
vertex has O(1) missing cross-neighbours, a profile extends to H.
(C) H embeds in a complete-cross host with only one internal K_{1,L}.

Construction and proof: take disjoint actual copies J_i of all profiles.
For each i, prescribe its actual vertices their profile colours, and
properly r-colour each J_j, j!=i. These assignments form R. Let
Q=K_r^{categorical |R|}; for actual vertex x, let t_x=(a(x):a in R).
Independently blow up every vertex of Q into M>r(L-1) clones. Join x to
all clones of all neighbours of t_x, and retain actual edges J_i.

Every proper r-colouring of Q is a coordinate projection followed by a
permutation. Indeed Q has degree (r-1)^m and unique least eigenvalue
-(r-1)^(m-1), whose eigenspace consists of sums of mean-zero one-coordinate
functions. Hoffman's bound shows every colour class has size r^(m-1),
with indicator 1/r+sum g_i(x_i). A binary additive function depends on
at most one coordinate: two nonzero coordinate differences would give
four values a,a+d,a+e,a+d+e all in {0,1}, impossible. Distinct coordinate
fibres intersect, so all colour classes use the same coordinate.

In an H-embedding choose a dominant host part for each clone cluster,
containing at least M/r clones. Adjacent clusters cannot have the same
dominant part, since internal degree would exceed L-1. Rigidity gives a
projection. Neighbours of t_x have every projected colour except its
own; thus x cannot occupy any other part, again by the internal-degree
bound. Its colours realize some assignment in R and hence a profile.
This proves (A), requiring NO cross-completeness. Conversely, fix the
actual active profile and place all other vertices according to that
projection. With bounded cross-deficit, greedy placement succeeds: there
are no required cross-edges between fixed profile vertices, and every
further vertex excludes only O(1) positions in each required part. This
proves (B), and with complete cross-edges proves (C).
Any proper r-colouring of H would give a projection and an active
monochromatic edge, contradiction. For an (r+1)-colouring activate the
star profile and recolour its leaves with a new colour; all other actual
profiles and all constraint edges stay proper. Thus chi(H)=r+1.

## 2. The r=2 realizer and exact allowed internal graphs

Use three profiles:
 P0: 2K2 in one part;
 P1: K_{1,5} in one part;
 P2: K_{1,4} in one part AND K2 in the other.
Profiles are interpreted up to swapping the two parts.
Take three independent variable gadgets (X_i,Y_i)=K_{10,10}, i modulo 3.
For each Pi take its actual copy. Bipartition the first-part component(s),
assigning their sides to variables X_i,X_{i+1}; bipartition second-part
components, assigning sides to Y_i,Y_{i+1}. A vertex assigned to X_j is
adjacent to all of Y_j, and vice versa. Retain all actual profile edges.
There are 60+4+6+7=77 vertices.

In an embedding with internal degree <=4, dominant variable colours are
opposite and actual vertices inherit assigned variable colours. Among
three bits, at least one cyclic adjacent pair agrees; its profile is
present internally. Conversely any Pi can be the UNIQUE active profile:
set its two endpoint bits equal and the third opposite. Hence (A)--(C)
hold with L=5, and chi(H)=3 follows by uniquely activating P1 and then
recolouring its leaves. The actual star centre is a colour-critical vertex.

The profile-free internal graph in each part has matching number <=1 and
maximum degree <=4. A graph with pairwise intersecting edges is either a
star or a triangle: if two edges xy,xz occur and any edge omits x, that
edge must be yz, and every further edge lies in xyz. Thus, ignoring
isolates, each internal graph is K_{1,j}, 1<=j<=4, or K3. If both parts
have an edge, P2 excludes K_{1,4}, so each has at most three edges.
Consequently the maximum total internal edge count is six, attained
precisely by a three-edge star or a triangle in EACH part. If just one
part is augmented, at most four edges are possible.

The global edge-cleaning lemma (agent2_edge_cleaning_lemma.md), whose
hypotheses (A)--(C) hold above, therefore proves, for every sufficiently
large n, ex(n,H)=t_2(n)+6 and every edge-extremal graph is balanced
complete bipartite with a three-edge star or triangle in each part.
On odd n=2m+1 the H-free competitor has K_{1,4} in the larger part and no
internal edges in the smaller. The cycle expansion proved separately is
 c/C0=1+2(e_A I0+e_B I2)/(m I1)+O(m^-2),
where I_j=sum_{l>=0}1/(l!(l+j)!). Its advantage over every edge-extremal
is 2(I0-3I2)/(m I1)+O(m^-2)>0, because I0-I2=I1 and I1/I0>2/3.
Thus no edge-extremal graph is cycle-extremal for all sufficiently large
odd n. This gives the endpoint a=0.

## 3. Profiles for r>=3 and exact edge-extremal graphs

Set k=6 for r=3, k=8 for r=4, and k=2r+1 for r>=5; put rho=(k-1)/k.
Take these single-part forbidden profiles:
 * every nonstar tree on k+1 vertices;
 * C3,C4,...,Ck;
 * K_{1,k+3};
 * 2K_{1,k};
 * P4 disjoint union K_{1,k}.
Also take the two-part profile (K2,K2), forbidding edges in two parts.
All are r-colourable, and a star profile is present, so section 1 applies.

A profile-free internal graph is a forest. Indeed a cycle of length <=k
is explicitly forbidden, and a longer cycle contains a nonstar tree on
k+1 vertices. Every nonstar tree component has order <=k, since its P4
can be extended to any smaller prescribed order. A star component has
at most k+3 vertices. At most one component has order >k (two would give
2K_{1,k}); if one does, every other component is a star, by the final
single-part profile. Conversely these conditions plainly suffice.

Only one part can have edges. On m sufficiently large vertices the exact
maximum internal edge number is
 E(m)=3+floor(rho*(m-3)).
Without a large star it is floor(rho*m). With a star on b vertices,
k+1<=b<=k+3, the maximum is b-1+floor(rho*(m-b)), nondecreasing in b,
so b=k+3 is best and gives the displayed formula, which is at least the
no-large-star value. This proves both the linear upper coefficient
rho/r and the matching lower construction. The global edge-cleaning
lemma consequently yields ex(N,H)<=t_r(N)+(rho/r)N+C and EXACT complete-
cross edge-extremal form for all large N.

For n=rkq+2r+2 put u=kq. EVERY edge-extremal graph, up to part permutation,
has sizes
 (u+3,u+3,u+2,...,u+2)
and its augmented part (one of size u+3) consists of
 (q-1) K_{1,k-1} disjoint union K_{1,k+2}.
Proof of the part-size claim: independent parts are balanced. Moving a
leaf from the augmented part to a smallest independent part shows the
augmented part is at most two larger; moving an independent vertex from
a largest other part to the augmented part as an isolate shows the other
parts are at most one larger. Thus the augmented size is u+2,u+3,or u+4.
Their internal maxima are respectively q(k-1)+2,q(k-1)+3,q(k-1)+3.
The first has the SAME maximum cross-edge count as the second, while
the third has one fewer cross-edge. Thus u+3 uniquely wins.
Here m=u+3 and E=q(k-1)+3, so a forest attaining E has exactly q
components. No-large-star components cover at most qk vertices, less
than m. With one large star, covering m=qk+3 vertices with q components
forces that star to have k+3 vertices and every other component exactly
k vertices. The latter must be stars. This proves the asserted uniqueness.

The H-free cycle competitor has part sizes
 (u+4,u+2,...,u+2)
and augmented graph qP_k disjoint union P4 (P_k denotes order k).
It has the SAME internal edge count but one fewer cross-edge.
The verified cycle expansions give strictly more cycles in this graph:
for r=3,k=6 the first-order gap is positive; for r>=5,k=2r+1 it is
positive; for r=4,k=8 the first-order gap vanishes but
 c(path competitor)/c(edge extremal)=1+(760/27)n^-2+o(n^-2).
Thus every endpoint b_r=rho/r is attained by a fixed H.

## 4. Checks

agent3_r2_realizer.py constructs all 77 vertices and 482 edges, checks all
8 variable orientations, certifies chi=3 by an explicit colouring and
non-bipartiteness, and exhaustively classifies admissible atlas gadgets.
agent3_r2_cycles.py computes exact INTEGER cycle counts for all four
edge-extremal types and confirms the competitor wins at n=321 and 641.
agent3_tensor_checks.py enumerates ALL proper colourings of K3^2,K3^3,
K4^2, confirming precisely the coordinate-permutation colourings.
These are independent checks, not substitutes for the proofs above.

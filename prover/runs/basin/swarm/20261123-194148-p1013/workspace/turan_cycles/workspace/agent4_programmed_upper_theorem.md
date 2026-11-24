# Programmed sharp upper constructions, r>=3 (no D-classification)

Use the following already proved lemmas:
* `agent3_profile_gadget_lemma.md` (equivalently `agent1_realization_lemma.md`): finite 3-colorable monochromatic partite-pattern obstructions are realized by one fixed graph H with chi(H)=r+1 and a critical vertex, using protected K_r-power color-profile gadgets; exact reverse implication holds in hosts of bounded internal degree.
* `agent4_finite_phase_basis.md`: a finite union of classes Down(R_i disjoint union infinitely many T_i), with R_i pseudoforests and T_i trees, has a finite forbidden-subgraph basis consisting of 3-colorable graphs.
* Edge version of `agent3_rotation_transfer_lemma.md` and `agent4_finite_hole_template_lemma.md`, proved in `agent4_rge3_lower_assembly.md` section 2: every edge extremizer for a fixed H having a critical vertex and a linear-forest decomposition has a partition with bounded internal components and all crossholes among boundedly many rare vertices. All abundant vertices are crosscomplete to every opposite-part vertex. This uses ordinary Erdos-Simonovits stability only, not Simonovits D.
* `agent2_tree_cycle_expansion.md`, `agent2_phase_bound_proof.md`, and `agent2_endpoint_wedge_lemma.md` for the cycle comparisons.

## General construction when A(r,k)>0
Fix r>=3,k>=2. Put rho=(k-1)/k, q=(r-1)/r,
 L=r/((r-1)(r-2)), B=2r/(r-1)^2,
 A(r,k)=-2/q+2L(2rho-1)+B*(k-2)(k-3)/(2k).
Assume A(r,k)>0. Choose a fixed integer U>=k+1. Let S_k be the k-vertex star and P_k the k-vertex path. Define the hereditary active-part class
 C = Down(C_U disjoint union infinity*S_k)
       union Down(C_{U-1} disjoint union infinity*P_k).
This class has maximum degree Q=k-1 and component order at most U. By the basis lemma it has a finite 3-colorable forbidden-subgraph basis F.

Prescribe the following partite forbidden patterns:
(i) each member of F wholly inside one part;
(ii) one internal edge in each of two distinct parts, with NO crossedge between their four terminals;
(iii) an internal star with D=Q+1 leaves, distinguished as the critical-root pattern.
Also include the redundant one-part path P_{U+1}, to make the linear-forest decomposition explicit. Pattern permutations among the host parts are automatic from global color permutations. Apply the profile realizer to obtain H.

The root-star profile gives chi(H)=r+1 and H-v r-colorable, hence H has a critical vertex. The P_{U+1} profile gives a linear-forest decomposition. Therefore the generic EDGE structure lemma applies to every large edge extremizer G. The critical star profile also gives global internal degree at most D-1=Q, either directly by the regular-core greedy embedding or by placing its auxiliary vertices in the crosscomplete abundant bulk.

In that finite-hole host, the realized profile equivalence is exact. Sufficiency maps the ACTIVE pattern terminals to the given internal obstruction; all other terminals and all protected auxiliary vertices go to fresh abundant vertices in their prescribed parts. Those vertices are crosscomplete, even if they are not internally isolated (extra host edges are harmless because subgraphs are not induced). Inactive patterns admit proper r-colorings since their chromatic numbers are <=3. The active pattern has only prescribed INTERNAL edges, so no missing crossedge between its terminals is ever required. Necessity follows from robust protected-gadget forcing at internal degree <=Q.

Consequently every edge extremizer has internal edges in at most one part, whose internal graph belongs to C. Conversely every complete r-partite graph with internal graph in C and no other internal edges is H-free. Crossholes do not affect this criterion; filling all of them is H-safe and increases edges. Thus ALL edge extremizers have COMPLETE crossedges and exactly the prescribed two-phase structure. This is the only structural input needed for the upper construction; nothing is asserted about cycle extremizers.

## Exact edge profiles
For a>=u>=k, the phase with cycle marker C_u has maximum internal count
 m_u(a)=a-ceil((a-u)/k).
It is attained by the full cycle and a maximum k-tree forest on the remaining vertices. Every proper nonempty cycle subgraph is a forest R on x<=u vertices with c>=1 components, giving at most
 a-c-ceil((a-x)/k) <= a-1-ceil((a-u)/k).
The empty marker loses at least floor(u/k)>=1. Hence the full marker is strictly required at fixed a. The remainder forest is a packing of full k-trees and one connected subtree of the leftover order.

In either phase m_u(a)<=rho*a+O_U(1). Therefore for all n
 ex(n,H)<=t_r(n)+(rho/r)*n+O_H(1),
because for delta=a-n/r the crossedge loss is at least delta^2/2 and rho*delta-delta^2/2 is bounded above. Values a<U have only bounded internal contribution and obey the same bound.

Select infinitely many n=rm with m=U mod k and m large; write m-U=kt. The star phase has the unique edge-optimal part sizes ALL equal to m. Indeed, at active size m+d its internal increment is d-ceil(d/k). For d>=1 this is <=d-1, whereas the crossedge loss is at least d; for d<=-1 the internal increment is nonpositive and the crossedge loss is positive. The inactive parts must be balanced for equality. At a=m the path phase has one fewer internal edge. At any other a its internal profile is no larger than the star profile, already at least one edge below the star optimum. Thus EVERY edge extremizer is, up to isomorphism,
 S: T_{rm,r} with C_U and t copies of S_k in one part.

The H-free competitor P has active part m+1, one other part m-1, and the others m, with internal graph
 C_{U-1} disjoint union t*P_k disjoint union P_2.
Its edge count is exactly one below that of S. Both graphs have exactly the same internal edge count M=t(k-1)+U. The first-order cycle expansion gives
 log(c(P)/c(S))=A(r,k)/n+O_H(n^-2)>0
for all sufficiently large selected n. Therefore no edge extremizer is cycle extremal at these infinitely many orders, and
 (k-1)/(kr) belongs to S_r whenever A(r,k)>0.

## The r=4,k=8 equality endpoint
Here A(4,8)=0. Keep the path phase, but replace the star marker C_U by X_U, a triangle with U-3 pendant leaves attached to one triangle vertex. Take U sufficiently large and fixed. The allowed class becomes
 Down(X_U disjoint union infinity*S_8)
    union Down(C_{U-1} disjoint union infinity*P_8).
Its maximum degree is Q=max(7,U-1), and it again has a finite 3-colorable basis by the pseudoforest basis lemma. Use D=Q+1 in the same realizer. All preceding edge-structure arguments apply unchanged.

Every subgraph R of X_U has e(R)<=v(R). Thus its edge profile is bounded above by m_U(a), attained by the full marker. At the selected balanced active size m=U mod 8, any proper cyclic subgraph on U-p vertices, p>0, loses at least
 ceil((m-U+p)/8)-(m-U)/8 >=1
edges after optimal bulk packing; a proper forest loses an additional edge, and deleting edges without vertices also loses edges. Thus EVERY edge extremizer still has exactly balanced part sizes and the ENTIRE X_U marker, together with t full S_8's.

The endpoint wedge lemma proves the cycle separation without any unknown second-order coefficient. For the REFERENCE cycle markers, maximum internal degree is seven independently of U, so its uniform error gives
 liminf n^2 log(c(P)/c(S_reference)) >= -16U/3-C
with an absolute C independent of fixed U. Replacing C_U by X_U changes the cycle logarithm by
 2(w(X_U)-U)/(q^2 n^2)+O_U(n^-3),
where q=3/4 and w(X_U)=binom(U-1,2)+2. Hence
 liminf n^2 log(c(P)/c(S_XU))
 >= (16/9)(U^2-8U+6)-C,
which is positive for sufficiently large fixed U. (Keeping the exact common constant gives U^2-8U+8 instead; either bound suffices.) Thus 7/32 belongs to S_4, including the equality endpoint.

## Numerical choices and resulting upper rays
The symbolic sign identity is
 A(r,k)=r*P_r(k)/(k(r-2)(r-1)^2).
At r=3 choose k=6, giving (k-1)/(kr)=5/18 and A>0.
At r=4 use the equality construction k=8, giving 7/32.
For r>=5 choose k=2r+1, giving 2/(2r+1), with P_r(2r+1)=6(r-1)>0.
Upward closure in the definition then gives every coefficient above these values. Together with `agent4_rge3_lower_assembly.md`, these are exactly S_r for r>=3.

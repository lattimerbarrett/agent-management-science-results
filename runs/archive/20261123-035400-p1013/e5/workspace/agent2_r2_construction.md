# Explicit bipartite-case construction: 0 belongs to S_2

## Forbidden graph
Start with four triangles v a_i b_i v, i=1,2,3,4. For every pair 1<=i<j<=3 add L=21 new vertices adjacent to a_i,a_j and L further new vertices adjacent to b_i,b_j; all these vertices are distinct and there are no other edges. Call the resulting 135-vertex graph H. It is 3-chromatic: triangles give the lower bound, while coloring v with color3, all a_i with color1, all b_i with color2, and each connector appropriately with a different color gives a 3-coloring.

H embeds into a complete bipartite graph plus a 4-star in one part (all a_i with v, all b_i opposite), and also plus a 4-matching in one part (all leaves opposite v). Thus the team's star/matching structural and peeling lemmas imply ex(n,H)=t_2(n)+O_H(1), all edge-extremals have minimum degree n/2-O_H(1), and every edge-extremal is an exact bounded-edit complete bipartite template. In such a template write A,B for internal graphs and D for the number of missing crossedges, all supported on boundedly many exceptional vertices. Each part also has arbitrarily many ordinary vertices with complete cross neighborhoods and no internal neighbors.

## Necessary template constraints
Ordinary vertices embed the 4-star and 4-matching configurations just described, so Delta(A),Delta(B),nu(A),nu(B)<=3. The Chvatal-Hanson bound gives e(A),e(B)<=f(3,3)=10. (Only this small instance and f(3,2)=7 are needed.)

For any internally active vertex x in A, the internal graph B induced by its cross-neighborhood has matching number at most2. Otherwise use x, one A-internal neighbor as triangle4's star leaf, and three B matching edges as triangles1,2,3; ordinary vertices supply every other leaf and every connector. Similarly, if d_A(x)=3, B induced by its cross-neighborhood is edgeless: use the three A neighbors as the star leaves for triangles1,2,3 and an opposite B-edge for triangle4. These statements hold symmetrically.

If nu(B)=3, each active A vertex must miss at least one B vertex, and every degree3 A vertex must miss a vertex cover of B, of size at least3. If a_j counts A vertices of internal degree j, then
 D>=a_1+a_2+3a_3 >= (a_1+2a_2+3a_3)/2=e(A).
Hence e(A)+e(B)-D<=e(B)<=10. Thus any template of net surplus at least12 has nu(A),nu(B)<=2.

Now e(A),e(B)<=f(3,2)=7. If e(A)=7 then Delta(A)=3 because Delta<=2,nu<=2 implies e<=6. A degree3 A vertex forces D>=tau(B)>=ceil(e(B)/3). Writing b=e(B)<=7 gives
 e(A)+e(B)-D<=7+b-ceil(b/3)<=11.
Thus net surplus at least12 forces e(A),e(B)<=6. It then forces e(A)=e(B)=6 and D=0. Since opposite internal edges exist, no degree3 vertex is allowed, so Delta(A),Delta(B)<=2. A graph with Delta<=2,nu<=2 and six edges is uniquely 2K3, as follows immediately by decomposing it into paths and cycles.

## Matching lower construction
Take balanced complete bipartite graph plus 2K3 inside each part. It is H-free. For if H embedded, total internal edges are12<21, so endpoints a_i,a_j of every L-fold connector must have the same bipartition color (otherwise each of 21 internally disjoint paths requires a distinct internal edge). Thus a_1,a_2,a_3 all have the same color, and so do b_1,b_2,b_3. The three main triangles consequently have either three star edges at v (impossible Delta=2) or three disjoint opposite internal edges (impossible nu=2); the possibility all their vertices share a color also has degree(v)>=6. Therefore no embedding exists.

The upper template bound and this lower construction give ex(n,H)=t_2(n)+12 eventually, and every edge-extremal graph is a balanced complete bipartite graph with exactly 2K3 inside each part.

## Lower-edge competitor
Let Q be K_{3,3} with one edge subdivided once. Then |V(Q)|=7, e(Q)=10, Delta(Q)=3, nu(Q)=3. For odd n=2m+1 put Q inside the larger part of K_{m+1,m}, leaving the other part independent. This graph is H-free: the connector argument again forces the first three triangles to be all star-type or all opposite-matching-type. If they are star-type, triangle4 would require either a fourth internal neighbor at v or an opposite internal edge; if matching-type, triangle4 would require a fourth matching edge or a star edge at v in the other part. Neither is possible. All-monochromatic triangle4 is covered by these same degree/matching obstructions.

## Cycle comparison
For a=m+1,b=m write C=c(K_{a,b}). For one fixed added A edge and one fixed added B edge respectively, the exact cycle gains are
 U_A=sum_{k=1}^{min(b,a-1)} (b)_k(a-2)_{k-1},
 U_B=sum_{k=1}^{min(a,b-1)} (a)_k(b-2)_{k-1}.
Also C=(1/2)sum_{k=2}^{min(a,b)}(a)_k(b)_k/k.
Direct factorial-ratio limits, dominated by reciprocal-factorial tails, give
 U_A/C=2 I_0(2)/(m I_1(2))+O(m^-2),
 U_B/C=2 I_2(2)/(m I_1(2))+O(m^-2),
where I_j(2)=sum_{l>=0}1/(l!(l+j)!).
For any fixed internal gadgets, cycles using >=2 internal edges contribute O(C/m^2); hence
 c(K_{a,b}+gadgets)=C+e(A)U_A+e(B)U_B+O(C/m^2).
For completeness, partition the used internal edges into their exact linear forest F; if F has ell edges and r_A,r_B path components and v_A,v_B incident vertices, its contribution is exactly
 2^(r_A+r_B) sum_{k>=max(1,r_A,r_B)} binom(a-v_A,k-r_A) binom(b-v_B,k-r_B) k!(k-1)!/2.
Factorial-ratio comparison with C gives O(C/m^ell); internal cycles entirely within the fixed gadget contribute only a bounded number. There are finitely many F. This justifies the error term.

An edge-extremal graph has six internal edges in each part, while the competitor has ten in the larger part and none in the smaller. Their cycle-count difference is
 4U_A-6U_B+O(C/m^2)
 = [2C/(m I_1(2))]*(4I_0(2)-6I_2(2))+O(C/m^2)>0
for large m. Indeed termwise I_2(2)<=I_0(2)/2, so 4I_0-6I_2>=I_0>0.
Thus no edge-extremal graph maximizes cycles for any sufficiently large odd n, proving 0 in S_2.

This construction does not resolve the stipulated all-r target: the team's separate aperiodic obstruction for r>=3 remains in force.

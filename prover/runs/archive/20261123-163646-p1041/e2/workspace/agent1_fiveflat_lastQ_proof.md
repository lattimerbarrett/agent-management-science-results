# The last five-flat Q-graph obstruction (agent 1)

This is a structural exclusion, NOT a proof of the user's main claim.
It concerns a putative genuinely new weight w in {322,326,330,334}
in ambient dimension 15 that is an XOR of FIVE minimum 7-flat indicators.
Previous team lemmas reduce its Q-graph to P3 plus two isolated vertices.
The argument below independently rules out that last graph without SAT.

## Inputs and notation

Write A_i=a_i+U_i, i=1,...,5, each an affine 7-flat in F2^15.
A Q-edge ij means U_i intersect U_j={0}. Its cross pair-parity contribution
is the indicator of the affine hyperplane A_i+A_j.
Assume Q is identically one and the only Q-edges are 12 and 23.
Assume the representation is minimal, so every nonempty pair intersection
has size at most 32: an intersection of size 64 collapses two minimum words
into one, and identical flats cancel.

The two Q-edge normals coincide, say n; let H=ker n. All U_1,U_2,U_3
are in H. The equation Q=1 gives n(a_1+a_3)=1. Thus A_1,A_3 occupy
opposite H-cosets. Relabel the two leaves if needed so A_2 occupies the
same coset as A_1. Complementary 7-directions inside H give
I_12=1, I_23=I_13=0, where I_ij=|A_i intersect A_j|.

For any point belonging to j of the five flats, its contribution to
(640-w)/2 is floor(j/2), at most binomial(j,2). Consequently
sum I_ij >= (640-w)/2 >=153.

## Elementary numerical bounds

If U_i intersect U_j=0 and A_v intersects both A_i,A_j, their direction
intersections inside U_v are disjoint. If U_v is arbitrary their dimensions
sum to at most 7; if U_v crosses H and i,j are in {1,2,3}, they are inside
U_v intersect H, of dimension 6, so the sum is at most 6.
Each nonempty actual intersection has dimension at most 5.
Empty intersections are assigned cap 0 with no extra constraint.

Direct enumeration, independently easy to check by hand, gives:
* max(2^a+2^b), a,b<=5, a+b<=7: 36;
* max(x_1+x_2+x_3), dimensions d_1+d_2,d_2+d_3<=7: 68;
* the same with both sums<=6: 66;
* the latter when x_1<=16: 50.
These include empty intersections. The executable exhaustive check is
workspace/agent1_fiveflat_lastQ_bounds.py, with its actual output JSON.

If A_4 lies in an H-coset, it can intersect at most one of A_1,A_3;
its total intersection with A_1,A_2,A_3 is <=36. The generic bound for
A_5 is 68. Including I_45<=32 and the single Q intersection gives
sum I_ij<=36+68+32+1=137<153. Hence A_4,A_5 both cross H.
Their three-intersection row bounds are now 66, so the total is <=165.
If I_45<=16, that total is <=66+66+16+1=149. If any one of
I_14,I_34,I_15,I_35 is <=16, the corresponding row is <=50,
so again the total is <=50+66+32+1=149. Therefore necessarily

 I_14=I_34=I_15=I_35=I_45=32.

The six-dimensional direction bounds then imply I_24,I_25<=2.

## Final contradiction

Remove the center A_2 and put T=A_1 XOR A_3 XOR A_4 XOR A_5.
There are exactly five nonempty pair intersections, all size32;
A_1 intersect A_3 is empty. Thus

 wt(T)=192+4(t_145+t_345).

Each nonempty triple t_145 or t_345 is the intersection of two affine
5-flats inside the affine7-flat A_4, and hence has size at least8.
Also |T intersect A_2| <=1+0+2+2=5.
If either triple is nonempty, wt(T)>=224 and

 w=wt(T)+128-2|T intersect A_2| >=342>334.

If both triples are empty, wt(T)=192 and w<=192+128=320<322.
Both cases contradict the specified critical weight.

Thus the last Q-graph cannot occur. Combined with the team's previous
Q-degree and edge-count cuts, no genuinely new critical word has a
representation by at most five minimum words. This does not rule out
six or more minimum words and supplies no actual new-weight witness.

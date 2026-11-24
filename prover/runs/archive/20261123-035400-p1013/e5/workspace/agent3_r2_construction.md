# Explicit constant-excess construction proving 0 belongs to S_2

## H (135 vertices)
Start with F_4: center v and triangles v a_i b_i, i=1,2,3,4. For every pair 1<=i<j<=3 add 21 new vertices adjacent precisely to a_i,a_j, and another 21 new vertices adjacent precisely to b_i,b_j. All auxiliary vertices are distinct. Thus |H|=1+8+6*21=135. H is 3-chromatic: it contains a triangle; assign v and all auxiliary vertices color0, all a_i color1, all b_i color2.

H embeds in a complete bipartite graph with one internal 4-star: put v and all a_i on one side and all b_i on the other, and put auxiliary vertices opposite their two endpoints. It also embeds with one internal 4-matching: put v on one side, all a_i,b_i on the other, and all auxiliary vertices on v's side. Thus the structural gap lemma (star+matching decomposition plus ES stability and low-degree peeling) gives ex(n,H)<=t_2(n)+O_H(1). Every sufficiently large edge-extremal graph has minimum degree n/2-O_H(1), hence by the structural/completion lemmas is an exact bounded-edit complete bipartite template. Let its two internal graphs be A,B, let D count missing cross edges, and put q=e(A)+e(B)-D.

## Robust necessary local constraints
Ordinary vertices outside the bounded exceptional set permit all unused vertices of H to be chosen greedily.
1. Each of A,B has maximum degree <=3 and matching number <=3 (the star4 and matching4 embeddings).
2. For each internally nonisolated vertex x in A, the internal B graph induced on its cross-neighbors has matching number <=2. Otherwise use x and one internal neighbor for triangle4 (the singleton index), use an opposite matching3 for triangles1,2,3, and choose all remaining vertices ordinary. All connector endpoints in each corresponding triple have the same side, so the 21 auxiliary paths are realized with ordinary vertices. Symmetrically for B.
3. For each internal degree3 vertex x in A, its cross-neighborhood in B is independent in B. Otherwise use its three internal neighbors for triangles1,2,3 and an opposite internal edge for triangle4. Again all remaining vertices are ordinary. Symmetrically for B.

## Numerical extremal bound
The needed small bounds have a short Tutte--Berge proof. Choose S with nu=|S|+sum_C floor(|C|/2), summing over components of G-S. At most3|S| edges touch S. A component of size2j has <=3j edges; one of size2j+1 has <=3j edges, except possibly if j>=2, when <=3j+1. There are at most floor((nu-|S|)/2) exceptional components. Thus for Delta<=3,
 e<=3nu+floor(nu/2),
giving nu3 ->e<=10 and nu2 ->e<=7. For Delta<=2, paths/cycles give e<=3nu, hence nu2 ->e<=6, with equality only2K3.
If nu(B)=3, every active x in A loses at least one cross-neighbor; every degree3 x loses at least three (an opposite vertex cover has size >=nu(B)=3). Writing n_j for the number of vertices of internal degree j in A,
 D >= n_1+n_2+3n_3 >= (n_1+2n_2+3n_3)/2=e(A).
Thus q<=e(B)<=10. Therefore q>=12 forces nu(A),nu(B)<=2.
Now e(A),e(B)<=7. If e(A)=7, then Delta(A)=3, since (Delta,nu)<=(2,2) gives <=6 edges. A degree3 vertex forces D>=tau(B)>=ceil(e(B)/3). Hence
 q <=7+b-ceil(b/3)<=11 for 0<=b<=7.
Thus q>=12 forces e(A),e(B)<=6, and then q=12 forces e(A)=e(B)=6,D=0. Since both parts have internal edges, constraint3 excludes degree3. Each internal graph has Delta<=2,nu<=2,e6; its components are paths/cycles, and the unique possibility is two disjoint triangles.

## Construction attaining q=12
Take balanced complete bipartite graph and place 2K3 inside EACH part. It is H-free. Indeed, if H embedded, every connector with endpoints in opposite bipartition classes would force one distinct internal edge on each of its21 length2 paths, while the target has only12 internal edges total. Consequently a_1,a_2,a_3 all lie in one class and b_1,b_2,b_3 all lie in one class. For the three triangles indexed1,2,3, their center then either has three internal neighbors (if the two leaf classes differ), lies opposite a three-edge matching (if both leaf classes are opposite the center), or has six internal neighbors (if all lie with center). Each case contradicts Delta=nu=2 for the internal graphs.
Thus ex(n,H)>=t_2(n)+12. Combined with the bound on eventual extremal templates, ex(n,H)=t_2(n)+12 for all sufficiently large n; every edge-extremal graph is balanced complete bipartite with2K3 in each part.

## A lower-edge graph with more cycles for odd n
Let n=2m+1, with larger part m+1. Inside the larger part put Q obtained by subdividing one edge of K3,3. Then Q has7 vertices,10 edges,Delta3,nu3. This graph is F4-free: a fan center in the larger part would need >=4 distinct internal neighbors, and a fan center in the other part would need internal matching4. Hence it is H-free.

Let C=c(K_{m+1,m}). Direct enumeration of alternating cycles and paths gives
 C=((m+1)!m!)/2 * sum_{j=0}^{m-2} 1/((j+1)!j!(m-j)),
 U_A=m!(m-1)! * sum_{j=0}^{m-1}1/(j!j!),
 U_B=(m+1)!(m-2)! * sum_{j=0}^{m-2}1/((j+2)!j!).
Factorial tails justify termwise limits (split the sums at j=m/2 if desired). Hence the gains U_A from one fixed internal edge in the larger part and U_B from one in the smaller part satisfy
 U_A/C ~ 2 I_0(2)/(m I_1(2)),
 U_B/C ~ 2 I_2(2)/(m I_1(2)),
where I_j(2)=sum_{t>=0}1/(t!(t+j)!). For any fixed bounded collection of internal edges, interactions contribute O(C/m^2). Therefore competitor minus ANY edge-extremal graph has
 4 U_A-6 U_B+O(C/m^2)
 = [2C/(m I_1(2))]*(4I_0(2)-6I_2(2))+o(C/m).
The coefficient is strictly positive: termwise I_2(2)<=I_0(2)/2, so4I_0-6I_2>=I_0>0. Thus every edge-extremal graph has fewer cycles than this H-free lower-edge competitor for every sufficiently large odd n.

Conclusion: this fixed135-vertex H proves0 in S_2. It does not lift to r>=3 because the endpoint-color period disappears and internal/cross edge marginals become uniform.

# Topological steps (agent 4)

## Simple connectivity
Let J be the join of the m four-point column sets. It is (m-2)-connected. K_m and J have identical 1-skeleta. Each triangle of J absent from K_m consists of three vertices in a single row whose capacity is 2 (including row 4 when m=7). Choose an unused column and a different row, and let v be that vertex. The three triangles coning its boundary to v lie in K_m: each has at most two vertices in the repeated row and one in the other row. Thus every missing triangular relation in the edge-path presentation of pi_1(J) already holds in pi_1(K_m). Since J is simply connected, so is K_m.

## Collapse of the top dimension
Set capacities c=(2,2,2,m-5), whose sum is m+1. Every face with m vertices occupies all columns, and its deficit vector c_i-|F_i| has sum one. Let r be its uniquely deficient row. Since c_r>=2, row r of F is nonempty. Delete one vertex v from that row. Any extension of F\{v} must occupy v's column, and all rows except r are saturated. Hence its unique extension is v. This is a free codimension-one face. Such chosen free faces belong to unique top-dimensional simplices, so all the corresponding elementary collapses can be carried out successively. The resulting complex has dimension at most m-2.

## Homology implies the required connectivity
If reduced integral homology vanishes through degree m-4, simple connectivity and the Hurewicz theorem applied to the first hypothetical nonzero homotopy group imply that K_m is (m-4)-connected.

## Splitting lemma
Suppose n>=2, X is (n-1)-connected, and its only nonzero reduced integral homology groups are H_n(X)=Z^a plus the direct sum of cyclic groups Z/t_i, and H_{n+1}(X)=Z^b. Then X is homotopy equivalent to the wedge of a copies S^n, one M(Z/t_i,n) for each i, and b copies S^{n+1}.

Here is a proof needing no classification theorem for CW complexes. Hurewicz identifies pi_n(X) with H_n(X), so choose maps representing all the indicated generators. A torsion generator alpha of order t extends from S^n over the degree-t Moore space, since t alpha=0 in pi_n(X).

Also pi_{n+1}(X)->H_{n+1}(X) is onto. To see this, choose f:Y=vee S^n ->X surjective on H_n, replace f by the inclusion into its mapping cylinder Z, and consider the pair (Z,Y). This pair is n-connected. Relative Hurewicz is therefore an isomorphism pi_{n+1}(Z,Y)->H_{n+1}(Z,Y). Given z in H_{n+1}(Z), lift its image to a relative homotopy element. Its boundary has zero Hurewicz image in H_n(Y), so vanishes in pi_n(Y). Hence the relative element lifts to pi_{n+1}(Z). Its Hurewicz image is exactly z, because H_{n+1}(Y)=0 makes H_{n+1}(Z)->H_{n+1}(Z,Y) injective.

Now choose sphere maps representing a basis of H_{n+1}(X), and wedge them with the chosen sphere and Moore maps. The resulting map induces isomorphisms on all integral homology groups. Both spaces are simply connected, so the homological Whitehead theorem makes it a homotopy equivalence.

For the present problem take n=m-3>=4.

# Vertex-decomposable complexes complete with no new vertices
Prove the stronger statement that a vertex-decomposable pure complex C, and a finite prescribed ground set W containing its vertices, admit a vertex-decomposability-preserving facet completion to the full pure skeleton on W. Ghost vertices in W may enter through added facets.

First introduce any ghost vertex w by a facet wH, where H is a ridge of some existing facet. Deleting w returns C (H already belongs to C), and its link is the simplex 2^H, so the new complex is vertex-decomposable. Repeat for all ghosts. Dimension zero is immediate by adding singletons. In dimension minus one there is nothing to add, regardless of prescribed ground set.

Now the complex has vertex set W. If it is a simplex, it is already full. Otherwise select a shedding vertex v with deletion D and link L. The vertex set of D is exactly W minus v: any vertex other than v survives deletion, and purity of D ensures it occurs in a facet. Inductively complete D on W minus v, adding the same facets to C. Throughout, v remains shedding, its link is L and its deletion follows the certified completion of D.

After the deletion is full, inductively complete L on the prescribed ground set W minus v (possibly introducing ghost vertices as above), lifting every added facet H to vH. The deletion of v remains the full d-skeleton: every face H introduced downstairs is already contained in a facet of that deletion. Its link follows the vertex-decomposable completion of L. This reaches the full skeleton on W.

Induct lexicographically on (dimension, cardinality of W). Ghost introduction is a finite preliminary operation on the same prescribed W. The deletion call keeps dimension and reduces cardinality of W; the link call reduces dimension. This proves both termination and the induction rigorously.

Consequently, if Delta is k-decomposable and its ridge skeleton is vertex-decomposable, adjoining one vertex suffices: first build the near-cone preserving k-decomposability; by the cone-saturation lemma that near-cone is vertex-decomposable; then apply the zero-extra completion just proved. This is only a conditional criterion, not a proof of the general claimed one-extra bound for k=1 or2.

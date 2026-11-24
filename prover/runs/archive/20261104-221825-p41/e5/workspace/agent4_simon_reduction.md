# Exact reduction of the zero-new-vertex case to Simon extendability

Let S_d(V)={G subset V: |G|<=d+1}. Let shellable mean pure shellable, with each new facet intersecting the preceding complex in a pure codimension-one subcomplex.

## Lemma 1
For a pure d-complex C, d-decomposability is equivalent to shellability. Consequently k-decomposability for any k>=d is equivalent to shellability.

Proof: A shelling's final facet F has a unique minimal new face R, and its new faces are exactly the Boolean interval [R,F]. If the shelling has more than one facet, R is nonempty. Thus del_R(C) is the preceding shellable complex, and lk_R(C)=2^(F\R). Induction proves d-decomposability.
Conversely suppose sigma is a decomposing face. First shell D=del_sigma(C). Then take a shelling H_1,...,H_m of L=lk_sigma(C) and append sigma union H_1,...,sigma union H_m. The intersection when appending sigma union H_i consists of (boundary sigma)*2^H_i together with 2^sigma times the intersection of 2^H_i with the preceding link facets. Every maximal face has size d. This is a shelling. The simplex cases and zero-dimensional links obey the same argument.

## Lemma 2
If C is pure d-dimensional and C'=C union 2^F is shellable, where F is a new (d+1)-set, then I=C intersect 2^F is pure (d-1)-dimensional.

Proof: If not, choose an inclusion-maximal face G of I with |G|<=d-1. Since G is maximal, no vertex of F\G belongs to lk_G(C). Moreover lk_G(C')=lk_G(C) union 2^(F\G). These two complexes have disjoint nonempty vertex sets and no cross edge. The first has vertices because C is pure and G is a face; the second has at least two vertices. Thus lk_G(C') is disconnected and has dimension d-|G|>=1, contradicting that links in a pure shellable complex are shellable and that a positive-dimensional pure shellable complex is connected.

## Corollary
For k>=d, the universal property in the question with r=0 is equivalent to the statement that S_d(V) is extendably shellable for every finite V.

Indeed every intermediate k-decomposable complex is shellable by Lemma 1. Lemma 2 says each new facet can be appended to any chosen shelling of C. Conversely a shelling extension gives shellable, hence k-decomposable, prefixes.

In particular the requested assertion b(3,3)>=1 demands the existence of a 3-skeleton of a simplex which is not extendably shellable: a counterexample to the dimension-three case of Simon's conjecture. No such counterexample was constructed by this team. This reduction is not a proof or disproof of the requested formula.

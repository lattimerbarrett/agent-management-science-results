# Equivalence with Simon's conjecture

Fix d and k>=d. A pure d-dimensional finite complex is k-decomposable iff it is shellable.

Forward direction: induct on decomposition. Shell the deletion first, then append sigma joined to the link facets in a shelling order. The intersection of a newly appended sigma*G with previous facets is the union of (boundary sigma)*G and sigma*(the previous link intersection), which is pure codimension one. Reverse direction: in any shelling with more than one facet, let F be the last facet and R its restriction face. The new faces of F are precisely the interval [R,F], with R nonempty. Thus deletion at R is exactly the preceding pure shellable prefix, while the link at R is the simplex on F\R. Since |R|<=d+1<=k+1, this gives a k-decomposition recursively.

Append lemma: Let C be pure d-dimensional, F a new (d+1)-set, and suppose C and C'=C union 2^F are shellable. Then H=C intersect 2^F is pure dimension d-1. Indeed, if T is a maximal face of H of cardinality <=d-1, then lk_T(C') is the disjoint union of lk_T(C) and the simplex 2^(F\T): maximality of T in H says no vertex of F\T occurs in lk_T(C). Both pieces have vertices, and both have dimension d-|T|>=1 because C is pure. This is disconnected, contradicting the fact that positive-dimensional links of pure shellable complexes are connected. (T can be empty, with the same argument.) All maximal faces of H therefore have cardinality d. Hence ANY shelling of C can be followed by F.

Consequently b(d,k)=0 iff every shelling of every pure shellable d-complex on a fixed vertex set can be extended to a shelling of the entire d-skeleton of that vertex set. Forward: b=0 provides intermediates, all shellable, and append lemma makes the provided facet sequence append to any original shelling. Reverse: any such shelling completion has shellable intermediates, hence k-decomposable intermediates. This is precisely Simon's extendable-shellability conjecture for simplex d-skeleta.

Thus establishing a positive value of b(d,k) for k>=d would disprove Simon's conjecture in dimension d, whereas b=0 would prove it there. This equivalence does not settle either alternative.

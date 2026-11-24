# Finite-valued root lemma

Suppose M:R->GL(2,C) takes exactly K essential values M_1,...,M_K. Let A be its matrix A_p characteristic (equivalently use W=(M* M)^(p/2)). Then

||M H M^(-1)||_(Lp->Lp) <= C_p K^2 (2K)^(K-1) A^((K-1)/p).

Proof. Put an undirected edge ij when some interval I has both proportions |I cap E_i|/|I| and |I cap E_j|/|I| at least 1/(2K). This graph is connected: for any nontrivial cut of the colors, the union E of one side and its complement both have density points. Translate a sufficiently short interval between two such points. Its E-density is continuous in the translation parameter and crosses 1/2. At that interval some color from each side has proportion >=1/(2K).

For an edge ij, the characteristic on its witnessing interval is at least alpha_i alpha_j^(p-1) ||M_i M_j^(-1)||^p. Thus both directed matrix norms on this edge are <=2K A^(1/p). A path of length <=K-1 and submultiplicativity yield the same pair bound with exponent K-1 for arbitrary i,j (A>=1).

Finally M H M^(-1)=sum_(i,j) M_i M_j^(-1) 1_(E_i) H 1_(E_j). Multiplication by an indicator is contractive on unweighted Lp and the componentwise Hilbert transform is bounded there with a p-dependent constant. Sum the K^2 bounds.

Consequences: K=2 gives exponent1/p; K=3 gives exponent2/p, hence linear for p=2. No three-fixed-root-value construction can yield the sharp A2 exponent3/2. The lemma does NOT cover finitely many eigenvector directions with continuously varying eigenvalues.

For each \(q\in\{5,7,9,11\}\), let \(K=\mathbb F_{q^2}\) and regard \(V=K^2\) as a four-dimensional vector space over \(\mathbb F_q\). The points and lines of \(PG(V)\) are its one-dimensional and two-dimensional \(\mathbb F_q\)-subspaces, respectively. Define
\[
J(\infty)=\{(0,x):x\in K\},\qquad J(k)=\{(x,kx):x\in K\}\quad(k\in K),
\]
and fix the spread \(\mathcal S_q=\{J(k):k\in K\cup\{\infty\}\}\). Here a spread is a collection of projective lines partitioning the projective points.

A regulus is a set \(R\) of \(q+1\) pairwise disjoint projective lines such that every projective line meeting three members of \(R\) meets all its members. Its opposite regulus \(R^{\mathrm{opp}}\) is the set of projective lines meeting every member of \(R\).

A connected \(t\)-nest in \(\mathcal S_q\) is a set \(N\) of \(t\) distinct reguli contained in \(\mathcal S_q\) satisfying both of the following conditions:
* Every line of \(\mathcal S_q\) belongs to either zero or exactly two members of \(N\).
* The graph whose vertices are the members of \(N\), with two vertices adjacent when the corresponding reguli share a line, is connected.

Call \(N\) hemi-replaceable if, for every \(R\in N\), one can choose a subset \(H_R\subseteq R^{\mathrm{opp}}\) of size \((q+1)/2\) such that
\[
\left(\mathcal S_q\setminus\bigcup_{R\in N}R\right)\cup\bigcup_{R\in N}H_R
\]
is a spread. Two nests are equivalent if an invertible semilinear transformation of the \(\mathbb F_q\)-vector space \(V\), acting projectively and preserving \(\mathcal S_q\) setwise, maps one nest onto the other.

Let \(a_{q,t}\) be the number of equivalence classes of connected \(t\)-nests in \(\mathcal S_q\) that are not hemi-replaceable. For commuting indeterminates \(X,Y\), determine the exact polynomial
\[
F(X,Y)=\sum_{q\in\{5,7,9,11\}}\sum_{t=1}^{q}a_{q,t}X^qY^t.
\]

The answer was proved recently, so it is not an open problem: your task is to find it and prove it, completely, and to write Python that really computes or checks every step that can be checked. Printing what you believe is not evidence. Arriving at an answer that settles less than the question asks (a partial or conditional answer, "not known") is not acceptable, and neither is conceding: when an approach fails, try another.

Proving it means showing that the answer is right in every case the question covers, and that no other answer is.

Stop only when your proof is complete. When you stop, write in that response what you proved, and what is left.
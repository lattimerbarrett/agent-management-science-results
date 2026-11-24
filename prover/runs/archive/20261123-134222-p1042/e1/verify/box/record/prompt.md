Let \(m\geq7\) be an integer and write \([m]=\{1,\ldots,m\}\). Define a finite simplicial complex \(K_m\) on the vertex set \(\{1,2,3,4\}\times[m]\) by declaring that a subset \(F\) is a face precisely when
\[
\left|F\cap(\{i\}\times[m])\right|\leq2\quad(i=1,2,3),\qquad
\left|F\cap(\{4\}\times[m])\right|\leq m-5,
\]
and
\[
\left|F\cap(\{1,2,3,4\}\times\{j\})\right|\leq1\quad(j\in[m]).
\]
For integers \(t\geq2\) and \(n\geq2\), let \(M(\mathbb Z/t\mathbb Z,n)\) denote the Moore space obtained from \(S^n\) by attaching one \((n+1)\)-cell along a map \(S^n\to S^n\) of degree \(t\). A wedge identifies chosen basepoints, and a wedge with zero summands is a point.

Determine the homotopy type of the geometric realization \(|K_m|\) for every \(m\geq7\), expressed as a finite wedge of spheres and Moore spaces, with every dimension, cyclic order, and multiplicity given explicitly as a function of \(m\).

The answer is \displaystyle |K_m|\simeq\left(\bigvee^{\frac{m(m-1)(m-2)(m-7)}{24}}S^{m-3}\right)\vee M(\mathbb Z/2\mathbb Z,m-3)\vee\left(\bigvee^{\frac{m^4+2m^3+11m^2+10m+12}{12}}S^{m-2}\right),\qquad m\ge7.. This was proved recently, so it is not an open problem: your team's task is to prove it, completely, and to write Python that really computes or checks every step that can be checked. Printing what you believe is not evidence. Arriving at any other answer is not acceptable, and neither is conceding: when an approach fails, try another.

Proving it takes showing that, for every integer \(m\ge7\), \(|K_m|\) is homotopy equivalent to a wedge of exactly \(\frac{m(m-1)(m-2)(m-7)}{24}\) copies of \(S^{m-3}\), one Moore space \(M(\mathbb Z/2\mathbb Z,m-3)\), and exactly \(\frac{m^4+2m^3+11m^2+10m+12}{12}\) copies of \(S^{m-2}\). Split the work, and the pieces of each part, between you on Slack.

Stop only when the team's proof is complete. Before you stop, post on Slack what you proved, and what is left.
Let \(q\ge 3\) be an integer. For a finite simple undirected graph \(G\), let \(V(G)\) be its vertex set, let \(d_G(v)\) be the number of neighbors of a vertex \(v\), and define the number of distinct vertex degrees by
\[
w(G)=\bigl|\{d_G(v):v\in V(G)\}\bigr|.
\]
Let \(\chi(G)\) denote the least number of colors in a vertex coloring in which adjacent vertices receive different colors. Define
\[
M(q)=\sup\left\{|V(G)|:\ G\text{ is a finite simple undirected graph with at least two vertices},\ \chi(G)\le q,\ |V(G)|-w(G)=7\right\},
\]
with \(M(q)=+\infty\) if the permitted graph orders are unbounded. Determine \(M(q)\) exactly for every integer \(q\ge3\).

The answer was proved recently, so it is not an open problem: your task is to find it and prove it, completely, and to write Python that really computes or checks every step that can be checked. Printing what you believe is not evidence. Arriving at an answer that settles less than the question asks (a partial or conditional answer, "not known") is not acceptable, and neither is conceding: when an approach fails, try another.

Proving it means showing that the answer is right in every case the question covers, and that no other answer is.

Stop only when your proof is complete. When you stop, write in that response what you proved, and what is left.
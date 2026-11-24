Let \(S^1=\{z\in\mathbb C:|z|=1\}\). A stable complex structure on a closed smooth real \(2n\)-manifold \(M\) means a complex vector-bundle structure \(J\) on
\[
E=TM\oplus(M\times\mathbb R^{2k})
\]
for some integer \(k\ge0\). Here closed means compact without boundary. For a smooth \(S^1\)-action on \(M\), require that its derivative action on \(TM\), extended by the trivial action on the stabilizing \(\mathbb R^{2k}\) fibers, commute with \(J\). Orient \(M\) using the complex orientation of \((E,J)\) and the standard orientation of the stabilizing real summand, and write \(c_j(M,J)=c_j(E,J)\).

Define \(\mathcal E\) to be the set of even integers \(2n\ge16\) for which there exist such an \(M\), an invariant stable complex structure \(J\), and a smooth \(S^1\)-action satisfying both of the following conditions:

1. The set \(M^{S^1}=\{p\in M:z\cdot p=p\text{ for every }z\in S^1\}\) consists of exactly four isolated points.
2. At least one Chern number
\[
\left\langle c_{i_1}(M,J)\cdots c_{i_r}(M,J),[M]\right\rangle,
\qquad r\ge1,\quad i_j\ge1,\quad i_1+\cdots+i_r=n,
\]
is nonzero.

Manifolds may be disconnected, and actions need not be effective. Determine \(\mathcal E\) explicitly.

The answer was proved recently, so it is not an open problem: your task is to find it and prove it, completely, and to write Python that really computes or checks every step that can be checked. Printing what you believe is not evidence. Arriving at an answer that settles less than the question asks (a partial or conditional answer, "not known") is not acceptable, and neither is conceding: when an approach fails, try another.

Proving it means showing that the answer is right in every case the question covers, and that no other answer is.

Stop only when your proof is complete. When you stop, write in that response what you proved, and what is left.
All graphs are finite, simple, and undirected. A graph is $H$-free if it contains no subgraph, not necessarily induced, isomorphic to $H$. Write $e(G)$ for the number of edges of $G$, and $c(G)$ for its number of simple cycles of length at least three, counted without orientation or a chosen starting vertex. For a fixed graph $H$, define
\[
\operatorname{ex}(n,H)=\max\{e(G):|V(G)|=n,\ G\text{ is }H\text{-free}\},
\qquad
\operatorname{cyc}(n,H)=\max\{c(G):|V(G)|=n,\ G\text{ is }H\text{-free}\}.
\]
Let $\chi(H)$ denote the minimum number of colors in a proper vertex coloring of $H$. Let $T_{n,r}$ be the complete $r$-partite graph on $n$ vertices whose part sizes differ by at most one, allowing empty parts, and put $t_r(n)=e(T_{n,r})$.

For each integer $r\ge2$, let $\mathcal S_r$ be the set of real numbers $a\ge0$ for which there exist a fixed graph $H$ with $\chi(H)=r+1$, a constant $C\ge0$, and a positive integer $N_0$ satisfying both conditions:

1. For every integer $N\ge N_0$,
\[
\operatorname{ex}(N,H)\le t_r(N)+aN+C.
\]
2. For infinitely many positive integers $n$, there is no $n$-vertex $H$-free graph $G$ satisfying simultaneously
\[
e(G)=\operatorname{ex}(n,H)
\quad\text{and}\quad
c(G)=\operatorname{cyc}(n,H).
\]

The choices of $H,C,N_0$ may depend on $r$ and $a$, but not on $N$ or $n$. Determine $\mathcal S_r$ explicitly for every integer $r\ge2$, including whether its finite boundary points belong to it.

The answer is \mathcal S_2=[1/3,\infty),\quad \mathcal S_3=[5/18,\infty),\quad \mathcal S_4=[7/32,\infty),\quad \mathcal S_r=[2/(2r+1),\infty)\ \text{for }r\ge5.. This was proved recently, so it is not an open problem: your team's task is to prove it, completely, and to write Python that really computes or checks every step that can be checked. Printing what you believe is not evidence. Arriving at any other answer is not acceptable, and neither is conceding: when an approach fails, try another.

Proving it takes two halves, for every \(r\ge2\), with \(b_2=\frac13\), \(b_3=\frac5{18}\), \(b_4=\frac7{32}\), and \(b_r=\frac2{2r+1}\) for \(r\ge5\): some fixed graph \(H\) with \(\chi(H)=r+1\) and constants \(C\ge0,N_0\ge1\) satisfy \(\operatorname{ex}(N,H)\le t_r(N)+b_rN+C\) for every integer \(N\ge N_0\), while for infinitely many \(n\) no \(n\)-vertex \(H\)-free graph attains both \(\operatorname{ex}(n,H)\) edges and \(\operatorname{cyc}(n,H)\) cycles; and for every \(0\le a<b_r\), every fixed graph \(H\) with \(\chi(H)=r+1\) satisfying \(\operatorname{ex}(N,H)\le t_r(N)+aN+C\) for some \(C\ge0\) and all sufficiently large \(N\) has, for every sufficiently large \(n\), an \(n\)-vertex \(H\)-free graph attaining both \(\operatorname{ex}(n,H)\) edges and \(\operatorname{cyc}(n,H)\) cycles. Split the work, and the pieces of each part, between you on Slack.

Stop only when the team's proof is complete. Before you stop, post on Slack what you proved, and what is left.
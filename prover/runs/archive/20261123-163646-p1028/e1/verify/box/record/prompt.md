Let \(n\) be an integer that is either even with \(n\ge 10\) or odd with \(n\ge 15\). Let \(\mathcal R_n\) be the class of finite connected simple undirected graphs on \(n\) vertices in which all vertices have the same degree; this common degree may vary between graphs in \(\mathcal R_n\). Here simple means that loops and multiple edges are forbidden.

For \(G\in\mathcal R_n\), let \((X_k)_{k\ge0}\) be the discrete-time random walk that moves at each step to a uniformly chosen neighbor of its current vertex. For \(v\in V(G)\), set
\[
T_v=\inf\{k\ge0:X_k=v\},
\]
and let \(\mathbb E_u\) denote expectation when \(X_0=u\). Define
\[
\tau(G)=\max_{u,v\in V(G)}\bigl(\mathbb E_uT_v+\mathbb E_vT_u\bigr),
\qquad
 t_n=\max_{G\in\mathcal R_n}\tau(G).
\]
Determine an explicit exact formula for \(t_n\) as a function of \(n\) throughout the stated domain.

The answer is \displaystyle t_n=\begin{cases}\frac{3n(2n-9)}4,&n\equiv2\pmod4,\\[2pt]\frac{3n(2n-11)}4,&n\equiv0\pmod4,\\[2pt]n^2-\frac{28}{5}n,&n\text{ odd},\ n\equiv0,3\pmod5,\\[2pt]n^2-\frac{23}{5}n,&n\text{ odd},\ n\equiv1\pmod5,\\[2pt]n^2-\frac{596}{115}n,&n\text{ odd},\ n\equiv2\pmod5,\\[2pt]n^2-\frac{278}{45}n,&n\text{ odd},\ n\equiv4\pmod5.\end{cases}. This was proved recently, so it is not an open problem: your team's task is to prove it, completely, and to write Python that really computes or checks every step that can be checked. Printing what you believe is not evidence. Arriving at any other answer is not acceptable, and neither is conceding: when an approach fails, try another.

Proving this formula takes two halves, for every even \(n\ge10\) and every odd \(n\ge15\): every \(G\in\mathcal R_n\) has \(\tau(G)\) at most the stated piecewise value for \(n\), and some \(G\in\mathcal R_n\) has \(\tau(G)\) exactly equal to that value. Split the work, and the pieces of each part, between you on Slack.

Stop only when the team's proof is complete. Before you stop, post on Slack what you proved, and what is left.
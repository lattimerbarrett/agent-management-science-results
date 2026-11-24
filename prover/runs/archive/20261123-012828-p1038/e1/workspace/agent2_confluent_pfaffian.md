# Confluent elliptic Schur--Pfaffian corollary

Use the notation and proven identity of `agent2_elliptic_pfaffian.md`. Parameterize the positive real branch by any increasing real-analytic coordinate $s$, and set
\[
L(s,t)=\frac{y(t)-y(s)}{\sqrt{q z(s)z(t)}(1+x(s)x(t))},\qquad z=y/x.
\]
Then $L(s,t)>0$ for $s<t$, and its diagonal slope
\[
\kappa(s)=\partial_tL(s,t)|_{t=s}
=\frac{y'(s)}{\sqrt q\,z(s)(1+x(s)^2)}>0.
\]
For increasing distinct points $s_1<\cdots<s_j$ and positive multiplicities $d_i$ whose sum is $2N$, form the skew matrix indexed lexicographically by $(i,p)$, $0\le p<d_i$,
\[
\mathcal L_{(i,p),(j,q)}=
\frac{1}{p!q!}\partial_s^p\partial_t^qL(s,t)|_{s=s_i,t=s_j}.
\]
The confluent Schur--Pfaffian formula is
\[
\boxed{\operatorname{Pf}\mathcal L
=\prod_i\kappa(s_i)^{\binom{d_i}{2}}
\prod_{i<j}L(s_i,s_j)^{d_id_j}>0.}
\]

Proof: replace each $s_i$ by $d_i$ ordered nearby points $s_i+\epsilon u_{ip}$. Apply the ordinary normalized Schur--Pfaffian identity. The Taylor coefficient matrix is a block Vandermonde congruence of the jet matrix, so division of the Pfaffian by the product of the intracluster Vandermondes converges to the displayed jet Pfaffian (Taylor factorials explain the chosen normalization). On the product side, intracluster factors tend to $\kappa(s_i)(t-s)$, and all cross-cluster factors tend to the corresponding $L(s_i,s_j)$. Thus the claimed formula follows. Strict positivity follows because the positive branch is nonsingular and $y'(s)>0$.

This proves positivity for every even mixed-point confluent skew moment matrix, not merely ordinary principal Pfaffians. It still does not identify the Atiyah determinant with one of these matrices.

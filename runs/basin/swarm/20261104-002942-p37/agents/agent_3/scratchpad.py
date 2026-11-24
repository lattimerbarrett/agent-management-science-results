from pathlib import Path
text=r'''# Lower bound and exact finite certificates

For $n\ge3$, suppose $Q_n$ has a realizer of size $t$. Restrict its orders to its singleton vertices, obtaining permutations $\pi_1,\dots,\pi_t$. For distinct vertices $x,y$ put
\[
S(x,y)=\{i:y<_{\pi_i}x\}.
\]
Each $S(x,y)$ is nonempty, since distinct singleton vertices are incomparable in $Q_n$. For distinct $x,y,z$, the realizer reverses the incomparable ordered pair $(\{x\},\{y,z\})$ in some order, so $S(x,y)\cap S(x,z)\ne\varnothing$. Consequently the family of all $S(x,y)$ for fixed $x$ is intersecting. Extend it to a maximal intersecting family $\mathcal F_x$ on $[t]$. If $x\ne y$, then $S(y,x)=[t]\setminus S(x,y)$, so $\mathcal F_x\ne\mathcal F_y$. Thus $n\le\lambda(t)$.

The function $\lambda$ is nondecreasing: a maximal intersecting family $\mathcal F$ on $[t]$ lifts injectively to the maximal intersecting family $\{A\subseteq[t+1]:A\cap[t]\in\mathcal F\}$. Therefore $\dim Q_d\ge d$, since its number of vertices is $\lambda(d-1)+1$.

Let $S_3$ have elements $a_1,a_2,a_3,b_1,b_2,b_3$ and comparabilities $a_i<b_j$ exactly when $i\ne j$. Any linear extension can reverse at most one of the three pairs $(a_i,b_i)$; otherwise the comparabilities between two indices create a cycle. Hence $\dim S_3\ge3$. For each $i$, put all $a_j$ with $j\ne i$ first, then $b_i,a_i$, then all remaining $b_j$. The three orders form a realizer (use the same increasing order of indices within the two exterior blocks), so $\dim S_3=3$. Fixing any element of $S_3$ gives an induced copy of $Q_d$ in $S_3\times Q_d$. Hence
\[
\dim(S_3\times Q_d)-\dim S_3\ge d-3.
\]

Executable finite certificates:
* `agent3_lower_checks.py`: all 48 linear extensions of $S_3$, its displayed realizer, small maximal intersecting families, and all suitable systems of 3/4 permutations on 3 vertices.
* `agent3_D7.py`: computes $D(7)=2414682040998$ from all 168 ideals of $B_4$. Viewing $B_7=B_3\times B_4$, an ideal corresponds to an isotone map $B_3\to J(B_4)$ (reverse the first factor if necessary). For prescribed bottom/top $B\subseteq T$, the middle six points form $S_3$. Set $C_{xy}=|\{z\in[B,T]:x\cup y\subseteq z\}|$. Their isotone-map count is $\operatorname{tr}(C^3)$. Sum over all 7581 intervals. All computations are nonnegative integers and each per-interval expression is bounded by $168^6<2^{63}$.
* `agent3_lambda7.py`: generates all 7581 upsets of $B_5$ and counts pairs $F_0\subseteq F_1$ with $F_0\cap\overline{F_1}=\varnothing$, where bar complements individual ground-set subsets. These are exactly intersecting upsets of $B_6$. It computes $\lambda(7)=1422564$ and $D(6)=7828354$.
* `agent3_d9.py`: for a partition of 9 coordinates into three 3-blocks, the 81 safe 4-subsets have 36 containing a distinguished coordinate. Let $I$ be those 36 and $J$ the other 45. For every intersecting $T\subseteq J$ of size at most 3, count all $2^{36-|N_I(T)|}$ possible accompanying subsets of $I$. This gives 3682229813248 distinct intersecting families, exceeding the independently computed $D(7)+1$. The exact four summands are 68719476736, 347892350976, 1019517861888, 2246100123648.
'''
Path('workspace/agent3_lower_proof.md').write_text(text)
print('saved lower proof and certificate explanations')

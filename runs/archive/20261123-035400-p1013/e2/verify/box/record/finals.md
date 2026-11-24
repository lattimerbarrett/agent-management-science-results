# agent_1: last reply

The prescribed answer is inconsistent with the definitions in the question. In fact,
\[
\boxed{\frac13\in\mathcal S_2,}
\]
which contradicts the stipulated \(\mathcal S_2=[1/2,\infty)\).

Below is a counterexample, including its extremal analysis and exact Python checks. Thus this is not merely an objection that the requested proof is difficult.

## 1. The forbidden graph

Let \(H\) have vertex set \(\{0,\ldots,7\}\) and edge set
\[
\begin{split}
E(H)=\{&
03,04,06,07,\,
13,15,17,\,
25,27,\,
37,47,67
\}.
\end{split}
\]
Here \(i j\) denotes the unordered edge \(\{i,j\}\).

The vertices \(0,3,7\) form a triangle. Also, \(H-7\) is bipartite, with bipartition
\[
\{0,1,2\},\qquad \{3,4,5,6\}.
\]
Consequently, \(\chi(H)=3\).

Define
\[
f(n)=\max_{0\le a\le n}
\left\{a(n-a)+\left\lfloor\frac{2a}{3}\right\rfloor\right\}.
\]
We will prove that, for all sufficiently large \(n\),
\[
\operatorname{ex}(n,H)=f(n).
\tag{1}
\]

Completing the square, or checking the nearest integer to \(n/2+1/3\), gives
\[
f(n)=t_2(n)+
\left\lfloor\frac{n+(n\bmod 2)}3\right\rfloor.
\tag{2}
\]
In particular,
\[
f(n)\le t_2(n)+\frac n3+1.
\tag{3}
\]

### An \(H\)-free construction

Start with \(K_{a,n-a}\). In its \(a\)-vertex part, put disjoint copies of \(P_3\), with an additional edge or isolated vertex if necessary. This adds \(\lfloor2a/3\rfloor\) edges.

Every graph obtained this way is \(H\)-free. Here is a direct verification.

Suppose \(V(H)=A\cup B\), where \(B\) is independent and every component of \(H[A]\) is a subgraph of \(P_3\).

* If \(7\in B\), then \(0,3,4,6\in A\), giving a claw centered at \(0\).
* If \(7\in A\) and \(0\in B\), then \(3,4,6\in A\), giving a claw centered at \(7\).
* Suppose \(0,7\in A\). Avoiding a triangle forces \(3,4,6\in B\), and hence \(1\in A\). Avoiding a claw centered at \(7\) forces \(2\in B\), and hence \(5\in A\). But then
  \[
  0-7-1-5
  \]
  is a \(P_4\) in \(H[A]\).

Each case is impossible. Thus
\[
\operatorname{ex}(n,H)\ge f(n).
\tag{4}
\]

## 2. The extremal upper bound

We use the standard Erdős–Simonovits stability theorem in its chromatic-number-three form:

> If a fixed graph \(F\) has \(\chi(F)=3\), then every \(F\)-free graph with \(n^2/4-o(n^2)\) edges has a bipartition with \(o(n^2)\) internal edges.

The following consequence supplies both the upper bound and the needed characterization of all edge-extremal graphs.

### Dense-graph lemma

For every fixed \(K\), sufficiently large \(H\)-free graphs \(G\) satisfying
\[
\delta(G)\ge n/2-K,\qquad e(G)\ge f(n)
\tag{5}
\]
have a partition \(A\cup B\) such that:

* \(G[B]\) is edgeless;
* every component of \(G[A]\) is \(P_1,P_2\), or \(P_3\).

In particular, \(e(G)\le f(n)\).

#### Proof

Choose a maximum cut \(A\cup B\). Stability implies
\[
|A|,|B|=n/2+o(n),
\]
with \(o(n^2)\) missing cross-edges and \(o(n^2)\) internal edges.

First, uniformly over all vertices,
\[
d_{\mathrm{internal}}(v)=o(n).
\tag{6}
\]
Indeed, otherwise some vertex \(v\) has at least \(\varepsilon n\) internal neighbors. By maximality of the cut, it also has at least \(\varepsilon n\) cross-neighbors.

All but \(o(n)\) vertices miss fewer than \(\varepsilon n/10\) cross-neighbors. Choose three such internal neighbors of \(v\). They have at least four common neighbors in the cross-neighborhood of \(v\). These vertices, together with \(v\), contain \(K_{1,3,4}\), and hence \(H\), a contradiction.

Combining (5) and (6), every vertex misses only \(o(n)\) vertices in the opposite part:
\[
|B\setminus N(v)|=o(n)\quad(v\in A),
\qquad
|A\setminus N(v)|=o(n)\quad(v\in B).
\tag{7}
\]

The following three explicit partitions of \(H\) now show that neither internal graph can contain a claw, a \(P_4\), or a triangle:
\[
\begin{array}{c|c|c}
S&H[S]&H[V(H)\setminus S]\\ \hline
\{0,1,2,7\}&K_{1,3}&\text{edgeless}\\
\{0,1,5,7\}&P_4&\text{edgeless}\\
\{0,3,5,7\}&K_3\cup P_1&\text{edgeless}.
\end{array}
\tag{8}
\]
For example, given an internal triangle, choose an additional vertex in that part to represent vertex \(5\). Equation (7) supplies all required vertices in the opposite part. The other two extensions work identically.

Thus both internal graphs are unions of \(P_1,P_2,P_3\).

Moreover,
\[
e(G[A])+e(G[B])
\ge f(n)-|A||B|
\ge n/3-O(1).
\tag{9}
\]
One part, say \(A\), therefore contains linearly many internal edges.

If \(G[B]\) has an edge, its endpoints have only \(o(n)\) cross-nonneighbors. Since \(\Delta(G[A])\le2\), we can choose an internal edge of \(A\) whose endpoints are adjacent to both endpoints of that fixed edge of \(B\).

Now use the partition
\[
A_H=\{0,5,7\},\qquad B_H=\{1,2,3,4,6\}.
\tag{10}
\]
The only edge in \(H[A_H]\) is \(07\), and the only edge in \(H[B_H]\) is \(13\). Map those two edges to the chosen internal edges. Equation (7) supplies the remaining vertices and all required cross-edges. This embeds \(H\), a contradiction.

Hence \(G[B]\) is edgeless, and
\[
e(G)
\le |A||B|+\left\lfloor\frac{2|A|}{3}\right\rfloor
\le f(n).
\]
This proves the lemma. \(\square\)

### Progressive pruning proves (1)

Formula (2) implies
\[
f(n)-f(n-1)\ge n/2-\tfrac12.
\tag{11}
\]

Let \(M\) be large enough for the dense-graph lemma with \(K=1\). Suppose an \(n\)-vertex \(H\)-free graph has more than \(f(n)\) edges.

As long as its current order \(k\ge M\), it must contain a vertex of degree at most
\[
f(k)-f(k-1)-1;
\]
otherwise the lemma would give at most \(f(k)\) edges.

Deleting such a vertex increases the integer surplus \(e(G)-f(k)\) by at least one. Continuing down to order \(M-1\) would produce surplus at least \(n-M+2\), impossible for sufficiently large \(n\). This proves (1).

Furthermore, once (1) holds at \(n\) and \(n-1\), every edge-extremal graph satisfies
\[
\delta(G)\ge f(n)-f(n-1).
\]
Thus the dense-graph lemma applies to **every** sufficiently large edge-extremal graph.

## 3. All edge-extremal graphs at orders divisible by six

Write \(n=2m\), with \(3\mid m\). If \(|A|=m+d\), then
\[
\begin{split}
|A||B|+\left\lfloor\frac{2|A|}{3}\right\rfloor
&=m^2+\frac{2m}{3}
+\left\lfloor\frac{2d}{3}\right\rfloor-d^2.
\end{split}
\]
For every nonzero integer \(d\),
\[
\left\lfloor\frac{2d}{3}\right\rfloor-d^2<0.
\]
Consequently, equality forces \(|A|=|B|=m\), all cross-edges present, and the internal graph to be a \(P_3\)-factor.

Hence, for all sufficiently large \(m\) divisible by three, there is a unique edge-extremal graph up to isomorphism:
\[
X_m=K_{m,m}
+\text{ a \(P_3\)-factor in one part}.
\tag{12}
\]

Consider instead
\[
Y_m=K_{m+1,m-1}
+\text{ \(m/3\) disjoint \(P_3\)'s and one isolate in the larger part}.
\tag{13}
\]
It is \(H\)-free by the earlier argument, and
\[
e(Y_m)=e(X_m)-1.
\tag{14}
\]

We next prove that \(Y_m\) nevertheless has more cycles.

## 4. The strict cycle comparison

Put
\[
B_m=\frac{m!(m-1)!}{2},
\qquad z=\frac73.
\]
Then
\[
\lim_{\substack{m\to\infty\\3\mid m}}\frac{c(X_m)}{B_m}
=
A:=\sum_{t\ge0}\frac{z^t}{(t!)^2},
\tag{15}
\]
whereas
\[
\lim_{\substack{m\to\infty\\3\mid m}}\frac{c(Y_m)}{B_m}
=
D:=\sum_{t\ge0}\frac{z^{t+2}}{t!(t+2)!}.
\tag{16}
\]

Here is a derivation, including convergence justification.

In a cycle, the selected internal edges in the decorated part form a linear forest. Contract its path components. If \(s\) decorated-part vertices and \(t\) opposite-part vertices are omitted, and \(i\) internal edges are used, the resulting alternating cycle requires
\[
i+s=t \quad\text{for }X_m,
\qquad
i+s=t+2 \quad\text{for }Y_m.
\tag{17}
\]

For fixed \(s,i\), the number of choices of omitted vertices and oriented internal forests is
\[
\frac{m^{s+i}(4/3)^i}{s!\,i!}
+O(m^{s+i-1}).
\tag{18}
\]
Indeed, there are \(2m/3\) internal edges, and choices containing adjacent selected edges or an omitted endpoint contribute only the lower-order term.

If \(k\) vertices are selected in the opposite part, the contracted-cycle factor is \(k!(k-1)!/2\). Including the choices of omitted opposite-part vertices and normalizing by \(B_m\), each fixed term tends to
\[
\frac{(4/3)^i}{s!\,i!\,t!}.
\]
Summing over (17), using \(1+4/3=7/3\), gives (15)–(16).

For completeness, the limit can be interchanged with the sums. For \(k\ge m/2\), use
\[
W(s,i)\le \frac{(2m)^s}{s!}\frac{(4m/3)^i}{i!},
\qquad
\binom bt\le\frac{m^t}{t!},
\qquad
\frac{k!(k-1)!}{m!(m-1)!}
\le(2/m)^{2(m-k)}.
\]
After imposing (17), these give summable majorants proportional to
\[
\frac{(40/3)^t}{(t!)^2}
\quad\text{and}\quad
\frac{4^t(10/3)^{t+2}}{t!(t+2)!}.
\]
For \(k<m/2\), the cycle length is at most \(3m/2+1\). The crude upper bound
\[
(2m)^{3m/2+O(1)}=o(B_m)
\]
handles this remaining range.

Finally, the strict inequality \(D>A\) has a short entirely rational certificate:
\[
D\ge\sum_{t=0}^{2}\frac{z^{t+2}}{t!(t+2)!}
=\frac{21217}{3888},
\]
while a geometric bound on the tail gives
\[
A\le
\sum_{t=0}^{2}\frac{z^t}{(t!)^2}
+\frac{z^3/(3!)^2}{1-z/16}
=\frac{67849}{13284}.
\]
And
\[
\frac{21217}{3888}-\frac{67849}{13284}
=\frac{55709}{159408}>0.
\tag{19}
\]

Therefore, for all sufficiently large \(m\) divisible by three,
\[
c(Y_m)>c(X_m).
\tag{20}
\]

Since every edge-extremal graph is isomorphic to \(X_m\), no edge-extremal graph can maximize the number of cycles at those orders.

Together with (3), this proves
\[
\boxed{\frac13\in\mathcal S_2.}
\]

## 5. Executable exact checks

The following code checks the finite embedding certificates, all \(256\) relevant vertex partitions of \(H\), the extremal-function arithmetic, the cycle-counting formula against independent DFS enumeration, and the rational strict inequality. It also checks the exact finite comparison \(c(Y_{24})>c(X_{24})\).

```python
from collections import defaultdict
from fractions import Fraction as F
from math import factorial as fac
import networkx as nx

E = [(0,3),(0,4),(0,6),(0,7),(1,3),(1,5),(1,7),
     (2,5),(2,7),(3,7),(4,7),(6,7)]
H = nx.Graph(E)

# chi(H)=3: a triangle, and deleting 7 leaves a bipartite graph.
assert nx.is_bipartite(H.subgraph(set(H) - {7}))
assert all(H.has_edge(*e) for e in [(0,3),(0,7),(3,7)])

certs = [
    ({0,1,2,7}, nx.star_graph(3)),
    ({0,1,5,7}, nx.path_graph(4)),
    ({0,3,5,7},
     nx.disjoint_union(nx.cycle_graph(3), nx.empty_graph(1)))
]
for S, D in certs:
    assert H.subgraph(set(H) - S).number_of_edges() == 0
    assert nx.is_isomorphic(H.subgraph(S), D)

def edges(G):
    return {frozenset(e) for e in G.edges()}

S = {0,5,7}
assert edges(H.subgraph(S)) == {frozenset((0,7))}
assert edges(H.subgraph(set(H)-S)) == {frozenset((1,3))}

# No independent-complement partition leaves a union of P1,P2,P3.
for mask in range(256):
    S = {v for v in H if mask >> v & 1}
    if H.subgraph(set(H)-S).number_of_edges():
        continue
    J = H.subgraph(S)
    assert any(len(C) > 3 or J.subgraph(C).number_of_edges() > 2
               for C in nx.connected_components(J))

def f(n):
    return max(a*(n-a) + (2*a)//3 for a in range(n+1))

for n in range(1,501):
    assert f(n) == n*n//4 + (n+n%2)//3
    assert 2*(f(n)-f(n-1)) >= n-1

for m in range(3,151,3):
    vals = [a*(2*m-a)+(2*a)//3 for a in range(2*m+1)]
    assert [a for a,v in enumerate(vals) if v == max(vals)] == [m]

# Per component:
# (selected vertices, contracted path blocks) -> oriented weight.
P = {
    1: {(0,0):1, (1,1):1},
    2: {(0,0):1, (1,1):2, (2,2):1, (2,1):2},
    3: {(0,0):1, (1,1):3, (2,2):3, (2,1):4,
        (3,3):1, (3,2):4, (3,1):2}
}

def cycles(a,b):
    q = {(0,0):1}
    components = [3]*(a//3) + ([a%3] if a%3 else [])
    for size in components:
        p = defaultdict(int)
        for (v,k), c in q.items():
            for (w,l), d in P[size].items():
                p[v+w,k+l] += c*d
        q = p

    twice = sum(c*fac(k-1)*fac(b)//fac(b-k)
                for (v,k),c in q.items()
                if 1 <= k <= b and v+k >= 3)
    assert twice % 2 == 0
    return twice//2

def host(a,b):
    G = nx.complete_bipartite_graph(a,b)
    for j in range(a//3):
        G.add_edges_from([(3*j,3*j+1),(3*j+1,3*j+2)])
    if a%3 == 2:
        G.add_edge(a-2,a-1)
    return G

def brute_cycles(G):
    total = 0
    for start in G:
        def dfs(v, seen):
            ans = int(len(seen) >= 3 and G.has_edge(v,start))
            for w in G[v]:
                if w > start and w not in seen:
                    ans += dfs(w, seen | {w})
            return ans
        total += dfs(start, {start})
    assert total % 2 == 0
    return total//2

for a,b in [(3,3),(4,2),(6,4),(6,5),(7,4)]:
    assert cycles(a,b) == brute_cycles(host(a,b))

z = F(7,3)
Aupper = (sum(z**t/fac(t)**2 for t in range(3))
          + (z**3/fac(3)**2)/(1-z/16))
Dlower = sum(z**(t+2)/(fac(t)*fac(t+2)) for t in range(3))

assert Aupper == F(67849,13284)
assert Dlower == F(21217,3888)
assert Dlower - Aupper == F(55709,159408)
assert cycles(25,23) > cycles(24,24)

print("All finite certificates passed.")
print("Exact n=48 cycle ratio:",
      float(F(cycles(25,23), cycles(24,24))))
```

This runs successfully; the final ratio is approximately \(1.007495627245093\).

Thus the requested conclusion cannot be proved as written: already at \(r=2\), a value strictly below the asserted boundary satisfies both defining conditions.

# agent_2: last reply

Independent review is complete. The team has a rigorous counterexample to the prescribed answer: the eight-vertex graph encoded by `GE\`cFs` satisfies
\[
\frac13\in\mathcal S_2,
\]
contradicting the claimed \(\mathcal S_2=[1/2,\infty)\).

I checked the structural extremal argument, exact integer optimization, uniqueness of edge extremizers on the relevant subsequence, and the cycle-count comparison. The computation and proof certificates have been shared with agent_1 for the final exposition.

# agent_3: last reply

Independent review confirms the complete cycle-limit proof. No additional gap was found; the counterexample contradicts the prescribed answer.

# agent_4: last reply

The prescribed conclusion is inconsistent with the definitions. Our team found and independently checked an eight-vertex graph \(H\) for which
\[
\chi(H)=3,\qquad
\operatorname{ex}(n,H)\le t_2(n)+\frac n3+1
\]
for all sufficiently large \(n\), yet infinitely many orders have no graph simultaneously maximizing edges and cycles. Thus
\[
\boxed{\frac13\in\mathcal S_2},
\]
contradicting the required assertion \(\mathcal S_2=[1/2,\infty)\).

The complete structural argument and executable independent checks are in:

- `workspace/agent4_H8_structure_proof.txt`
- `workspace/agent4_H8_certificate.py`

The coordinating agent has the full proof, including the rigorously certified cycle comparison.
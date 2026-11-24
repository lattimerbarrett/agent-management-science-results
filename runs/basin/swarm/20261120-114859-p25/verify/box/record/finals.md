# agent_1: last reply

\[
\boxed{\frac19}
\]

There are two genuinely different parts: constructing counterexamples below \(1/9\), and proving that every \(c>1/9\) works.

I give both proofs. The only general theorems used are the classical **Szemerédi regularity lemma** and **Kneser’s theorem**
\[
\chi\bigl(KG(m,k)\bigr)=m-2k+2.
\]
No homomorphism-threshold theorem is used as a black box.

## 1. Replacing the homomorphism problem by a coloring problem

For a triangle-free graph \(G\), let \(P(G)\) be the graph on \(V(G)\) in which two vertices are adjacent if there is a walk of length three between them.

There are no loops in \(P(G)\), since a closed walk of length three would be a triangle. Also, every edge of \(G\) is an edge of \(P(G)\), by backtracking.

### Lemma 1
For every positive integer \(q\), there is a finite triangle-free graph \(U_q\) such that
\[
\chi(P(G))\le q\quad\Longrightarrow\quad G\longrightarrow U_q.
\]

**Proof.** The vertices of \(U_q\) are the pairs
\[
(i,S),\qquad i\in[q],\quad S\subseteq[q]\setminus\{i\}.
\]
Put an edge between \((i,S)\) and \((j,T)\) precisely when
\[
i\in T,\qquad j\in S,\qquad S\cap T=\varnothing.
\]

This graph is triangle-free. Indeed, if \((i,S),(j,T),(k,W)\) formed a triangle, adjacency to the first vertex would give
\[
i\in T\cap W,
\]
contradicting adjacency between the other two vertices.

Now take a proper \(q\)-coloring \(a\) of \(P(G)\), and define
\[
f(v)=\bigl(a(v),\{a(w):w\in N_G(v)\}\bigr).
\]
For \(uv\in E(G)\), the required cross-memberships hold. The two sets of neighbor-colors are disjoint: otherwise there would be \(x\in N(u)\), \(y\in N(v)\) with \(a(x)=a(y)\), although \(x,u,v,y\) is a length-three walk. The possibility \(x=y\) would itself give a triangle in \(G\). Thus \(f\) is a homomorphism. ∎

We will also repeatedly use the following elementary observation:
\[
\boxed{\text{If \(G\) has no \(C_3,C_5\), and \(xy\in E(P(G))\), then }
N_G(x)\cap N_G(y)=\varnothing.} \tag{1}
\]
Otherwise a length-three walk from \(x\) to \(y\), followed by a common neighbor, gives a closed odd walk of length five. Every such walk contains a triangle or a \(5\)-cycle.

---

## 2. The lower bound: every \(c<1/9\) fails

Fix \(c<1/9\), and let \(H\) be any finite triangle-free graph. Write \(h=|V(H)|\), assuming \(h\ge1\).

Choose an integer \(k\) sufficiently large that
\[
\frac{k}{9k+3h}>c,
\]
and put
\[
m=2k+h,\qquad F=KG(m,k).
\]
Thus vertices of \(F\) are the \(k\)-subsets of \([m]\), adjacent when disjoint. Kneser’s theorem gives
\[
\chi(F)=m-2k+2=h+2>h. \tag{2}
\]

### 2.1 A sparsely subdivided core

Orient every edge of \(F\) arbitrarily. Replace each oriented edge \(S\to T\) by
\[
x_S-a_{ST}-b_{ST}-x_T.
\]
Call the resulting graph \(Q\). Partition its vertices into three independent sets:
\[
Q_0=\{x_S\},\qquad Q_1=\{a_{ST}\},\qquad Q_2=\{b_{ST}\}.
\]
Assign each vertex a \(k\)-element label:
\[
L(x_S)=S,\qquad L(a_{ST})=S,\qquad L(b_{ST})=T.
\]

These labels have the crucial property
\[
u,v\in Q_i,\ uv\in E(P(Q))
\quad\Longrightarrow\quad L(u)\cap L(v)=\varnothing. \tag{3}
\]

To verify this, a length-three walk with both ends in the same class must traverse the three classes cyclically.

* In \(Q_0\), its ends correspond to an edge \(ST\) of \(F\).
* In \(Q_1\) or \(Q_2\), it comes from two consecutively oriented edges of \(F\), in one direction or the other.

In each case the two labels are endpoints of an edge of \(F\), hence are disjoint.

Also, \(Q\) has no cycle shorter than nine: it is the three-subdivision of a simple graph.

### 2.2 Adding dense reservoirs

Choose a positive integer \(t\). For each \(i\in\{0,1,2\}\), add:

* \(R_i=[m]\times[t]\), of size \(mt\);
* an independent set \(Z_i\), of size \(kt\);
* all edges between \(R_i\) and \(Z_i\);
* for \(v\in Q_i\), all edges from \(v\) to
  \[
  L(v)\times[t]\subseteq R_i.
  \]

There are no other edges. Denote this graph by \(G_t\).

Every vertex has degree at least \(kt\):

* each core vertex has \(kt\) reservoir neighbors;
* each vertex of \(R_i\) has all \(kt\) neighbors in \(Z_i\);
* each vertex of \(Z_i\) has \(mt\ge kt\) neighbors in \(R_i\).

Writing \(s=|V(Q)|\), we obtain
\[
|V(G_t)|=s+3(m+k)t
\]
and
\[
\frac{\delta(G_t)}{|V(G_t)|}
\ge
\frac{kt}{s+3(m+k)t}
\longrightarrow
\frac{k}{3(m+k)}
=
\frac{k}{9k+3h}>c. \tag{4}
\]
Thus sufficiently large \(t\) gives the required minimum degree.

### 2.3 Checking the forbidden cycles

There are no \(3\)- or \(5\)-cycles wholly inside \(Q\).

A \(5\)-cycle containing a vertex of \(Z_i\) would have the form
\[
Z_i-R_i-Q_i-Q_i-R_i-Z_i,
\]
forcing an edge inside \(Q_i\), which is impossible. A triangle containing \(Z_i\) is also impossible.

Consider a short odd cycle containing reservoir vertices but no \(Z_i\).

* A triangle would force an edge inside some \(Q_i\).
* A \(5\)-cycle with one reservoir vertex would give a length-three path in \(Q\), with ends in the same \(Q_i\) whose labels have a common element. This contradicts (3).
* A \(5\)-cycle with two reservoir vertices has the form
  \[
  r-x-r'-y-z-r.
  \]
  The common neighbor \(x\) forces \(r,r'\in R_i\) for the same \(i\); then \(y,z\in Q_i\), again forcing an edge inside \(Q_i\).

Hence \(G_t\) has no \(C_3\) or \(C_5\).

### 2.4 Why it cannot map to \(H\)

Suppose \(f:G_t\to H\) were a homomorphism. For every edge \(ST\) of \(F\), its subdivided path gives a length-three walk in \(H\) from \(f(x_S)\) to \(f(x_T)\).

These two endpoints cannot be equal, since \(H\) is triangle-free. Therefore
\[
S\longmapsto f(x_S)
\]
would properly color \(F\) with at most \(h\) colors, contradicting (2).

Thus every \(c<1/9\) fails.

---

## 3. The upper bound: every \(c>1/9\) works

Fix \(c>1/9\), and set
\[
\tau=\frac{c-1/9}{10}.
\]
In particular,
\[
9c-15\tau>1. \tag{5}
\]

We prove that \(\chi(P(G))\) is bounded in terms of \(c\).

### 3.1 The regularity setup

We need the following standard consequence of the regularity lemma.

### Regularity consequence
For fixed \(c,\tau>0\), and sufficiently small fixed \(\varepsilon>0\), every sufficiently large graph with minimum degree at least \(cn\) has a partition
\[
V(G)=V_0\cup V_1\cup\cdots\cup V_k
\]
such that:

1. \(|V_0|\le\tau n\);
2. \(|V_1|=\cdots=|V_k|=M\);
3. \(k\le K\), where \(K\) depends only on the fixed parameters;
4. there is a reduced graph \(R\) on \([k]\) with
   \[
   \delta(R)\ge(c-\tau)k, \tag{6}
   \]
   whose edges represent \(\varepsilon\)-regular pairs of density at least \(d=\tau/4\).

Here \(\varepsilon\) can be chosen as small as needed relative to \(\tau,d\).

For completeness, the minimum-degree assertion follows by starting with a much finer regularity parameter \(\eta\). Move to \(V_0\) every cluster incident with more than \(\sqrt\eta\,k\) irregular pairs; at most \(2\sqrt\eta\,k\) clusters are moved. Discard irregular pairs and pairs of density below \(d\). For each remaining cluster, average its vertices’ degrees. The losses are at most
\[
d+O(\sqrt\eta)+O(1/k)
\]
as a proportion of all clusters. Taking \(\eta\) sufficiently small and the initial number of clusters sufficiently large gives (6), as well as \(|V_0|\le\tau n\).

For each vertex \(v\in V(G)\), define its **profile**
\[
I(v)=\{i\in[k]: |N_G(v)\cap V_i|\ge\tau M\}.
\]
There are at most \(2^K\) profiles.

The number of neighbors of \(v\) outside the clusters indexed by \(I(v)\) is at most
\[
|V_0|+\tau kM\le2\tau n. \tag{7}
\]
Consequently every occurring profile is nonempty.

### 3.2 Three restrictions on profiles

Write \(N_R(I)=\bigcup_{i\in I}N_R(i)\). Regularity and the absence of \(C_3,C_5\) give:

\[
\begin{array}{ll}
\text{(A)} & I(v)\text{ is independent in }R;\\[2mm]
\text{(B)} & uv\in E(G)\Longrightarrow
N_R(I(u))\cap N_R(I(v))=\varnothing;\\[2mm]
\text{(C)} & u-w-v\text{ is a length-two walk in }G\\
&\hspace{13mm}\Longrightarrow
\text{there is no \(R\)-edge between }I(u)\text{ and }I(v).
\end{array} \tag{8}
\]

Here are the embedding details.

* An \(R\)-edge between two clusters in \(I(v)\) supplies an edge between two neighbors of \(v\), giving a triangle.
* If \(uv\in E(G)\) and some reduced vertex is adjacent to a cluster in \(I(u)\) and a cluster in \(I(v)\), regularity supplies a length-two path between a neighbor of \(u\) and a neighbor of \(v\). Together with \(uv\), this is a \(5\)-cycle.
* An \(R\)-edge between clusters in \(I(u)\) and \(I(v)\), together with \(u-w-v\), similarly gives a \(5\)-cycle. If \(u=v\), use (A).

These applications only involve endpoint subsets of size at least \(\tau M\). Taking \(\varepsilon\ll\tau,d\) guarantees the requisite edges. For the length-two path, all but at most \(2\varepsilon M\) vertices in its middle cluster have many neighbors in both prescribed endpoint subsets. Taking \(M\) sufficiently large allows all previously specified vertices to be avoided, so the cycles are genuine subgraphs.

### 3.3 Profiles containing an edge of \(P(G)\) are large

Suppose \(x,y\) have the same profile \(I\) and \(xy\in E(P(G))\). By (1), their neighborhoods are disjoint. By (7), each has at least \((c-2\tau)n\) neighbors in the clusters of \(I\). Hence
\[
|I|M\ge2(c-2\tau)n,
\]
and therefore
\[
|I|\ge2(c-2\tau)k. \tag{9}
\]

### 3.4 A six-set packing argument

Fix an occurring profile \(I\), and let \(F_I\) be the subgraph of \(P(G)\) induced by the vertices with profile \(I\).

Orient every edge of \(F_I\) according to any fixed vertex ordering. For each oriented edge \(x\to y\), choose a witnessing length-three walk
\[
x-a-b-y
\]
and give that oriented edge the color
\[
\bigl(I(a),I(b)\bigr).
\]
There are at most
\[
(2^K)^2
\]
colors.

We claim that no color class contains a directed length-two path.

Suppose otherwise. We have two witnesses
\[
x-a-b-y,\qquad y-a'-b'-z
\]
whose profile sequences are
\[
I,J,L,I,\qquad I,J,L,I.
\]

From the three edges of the first witness, (B) gives pairwise disjointness of
\[
N_R(I),\quad N_R(J),\quad N_R(L). \tag{10}
\]

From the length-two walks
\[
x-a-b,\qquad a-b-y,\qquad b-y-a',
\]
condition (C) says that there are no reduced edges between any two of \(I,J,L\). Each is itself independent by (A). Thus
\[
I\cup J\cup L\text{ is independent in }R. \tag{11}
\]

Since \(R\) has positive minimum degree, (10) also forces \(I,J,L\) to be pairwise disjoint: a reduced vertex in two of them would have a neighbor lying in two of the sets in (10).

It follows from (10)–(11) that the six sets
\[
I,\ J,\ L,\ N_R(I),\ N_R(J),\ N_R(L)
\]
are pairwise disjoint.

Moreover, each of \(I,J,L\) contains the ends of an edge of \(P(G)\):

* \(x,y\) have profile \(I\);
* \(a,b,y,a'\) is a length-three walk with endpoint profile \(J\);
* \(b,y,a',b'\) is one with endpoint profile \(L\).

The endpoints in these walks are distinct; otherwise there would be a triangle. Applying (9), and then (6), gives
\[
\begin{aligned}
k
&\ge |I|+|J|+|L|
   +|N_R(I)|+|N_R(J)|+|N_R(L)|\\
&\ge 6(c-2\tau)k+3(c-\tau)k\\
&=(9c-15\tau)k\\
&>k,
\end{aligned}
\]
a contradiction.

This proves the claim.

An oriented graph containing no directed length-two path is bipartite: every nonisolated vertex is exclusively a source or exclusively a sink. Therefore every color class in \(F_I\) is bipartite.

A graph whose edges are the union of \(r\) bipartite graphs is \(2^r\)-colorable, by recording one bipartition bit for each graph. Consequently, with \(T=2^K\),
\[
\chi(F_I)\le2^{T^2}
\]
and
\[
\chi(P(G))\le T\,2^{T^2}. \tag{12}
\]

This bound depends only on \(c\). Graphs below the fixed size required by the regularity argument can be accommodated by increasing the bound.

Lemma 1 now supplies a single finite triangle-free target for all such \(G\). Thus every \(c>1/9\) works.

Together with the lower bound, this proves the claimed infimum.

---

## 4. Python verification

The following is executable Python, using NumPy, NetworkX and Z3. It checks:

* explicit instances of the lower-bound construction;
* the absence of \(C_3,C_5\), using exact integer closed-walk counts;
* the same-class label condition;
* small Kneser chromatic numbers, independently with Z3;
* a nonexistence-of-homomorphism instance;
* the universal-target reduction on **all 172 triangle-free graphs in NetworkX’s atlas**;
* exact arithmetic for counterexample parameters arbitrarily close to \(1/9\).

The finite checks supplement, rather than replace, the proofs of the infinite assertions.

```python
import itertools as it
from fractions import Fraction
from math import comb

import networkx as nx
import numpy as np
from z3 import Solver, Int, Or, And, sat


def kneser(m, k):
    labels = [frozenset(S) for S in it.combinations(range(m), k)]
    F = nx.Graph()
    F.add_nodes_from(range(len(labels)))
    for u, v in it.combinations(F, 2):
        if labels[u].isdisjoint(labels[v]):
            F.add_edge(u, v)
    return F, labels


def construction(m, k, t=1):
    F, sets = kneser(m, k)
    Q = nx.Graph()
    group, label = {}, {}

    for v in F:
        x = ("x", v)
        Q.add_node(x)
        group[x], label[x] = 0, sets[v]

    for u, v in F.edges:
        a, b = ("a", u, v), ("b", u, v)
        Q.add_edges_from([
            (("x", u), a), (a, b), (b, ("x", v))
        ])
        group[a], group[b] = 1, 2
        label[a], label[b] = sets[u], sets[v]

    G = Q.copy()
    for i in range(3):
        R = [("r", i, j, ell)
             for j in range(m) for ell in range(t)]
        Z = [("z", i, ell) for ell in range(k*t)]
        G.add_nodes_from(R + Z)
        G.add_edges_from(it.product(R, Z))
        for v in Q:
            if group[v] == i:
                G.add_edges_from(
                    (v, ("r", i, j, ell))
                    for j in label[v] for ell in range(t)
                )

    return F, Q, G, group, label


def walk_power3_and_check_cycles(G):
    V = list(G)
    A = nx.to_numpy_array(G, nodelist=V, dtype=np.int64)
    A2, A3 = A @ A, A @ A @ A

    # Exact nonnegative closed-walk counts.
    assert np.trace(A3) == 0
    assert np.sum(A2 * A3) == 0  # trace(A^5), by symmetry

    P = nx.Graph()
    P.add_nodes_from(V)
    for i, j in zip(*np.where(np.triu(A3 > 0, 1))):
        P.add_edge(V[i], V[j])
    return P


def colorable(F, q):
    color = {v: Int("c" + str(i)) for i, v in enumerate(F)}
    s = Solver()
    for v in F:
        s.add(color[v] >= 0, color[v] < q)
    for u, v in F.edges:
        s.add(color[u] != color[v])
    return s.check() == sat


def hom_exists(G, H):
    hv = list(H)
    index = {v: i for i, v in enumerate(hv)}
    image = {v: Int("f" + str(i)) for i, v in enumerate(G)}
    arcs = []
    for u, v in H.edges:
        arcs += [(index[u], index[v]), (index[v], index[u])]

    s = Solver()
    for v in G:
        s.add(image[v] >= 0, image[v] < len(H))
    for u, v in G.edges:
        s.add(Or(*[
            And(image[u] == a, image[v] == b) for a, b in arcs
        ]))
    return s.check() == sat


for m, k, t in [(5, 2, 1), (5, 2, 4), (6, 1, 1), (8, 2, 1)]:
    F, Q, G, group, label = construction(m, k, t)

    PQ = walk_power3_and_check_cycles(Q)
    for u, v in PQ.edges:
        if group[u] == group[v]:
            assert label[u].isdisjoint(label[v])

    walk_power3_and_check_cycles(G)
    assert len(G) == len(Q) + 3*(m+k)*t
    assert min(dict(G.degree()).values()) >= k*t

    expected = m - 2*k + 2
    assert colorable(F, expected)
    assert not colorable(F, expected-1)

    print("construction", (m, k, t),
          "vertices", len(G),
          "minimum degree", min(dict(G.degree()).values()),
          "checks passed")

    if (m, k, t) == (6, 1, 1):
        assert not hom_exists(G, nx.cycle_graph(5))
        print("  no homomorphism to C5: independently checked by Z3")


# Check Lemma 1 on every triangle-free graph in the graph atlas.
count = 0
for G in nx.graph_atlas_g():
    if len(G) == 0 or sum(nx.triangles(G).values()):
        continue

    V = list(G)
    A = nx.to_numpy_array(G, nodelist=V, dtype=np.int64)
    A3 = A @ A @ A
    P = nx.Graph()
    P.add_nodes_from(V)
    for i, j in zip(*np.where(np.triu(A3 > 0, 1))):
        P.add_edge(V[i], V[j])

    color = nx.coloring.greedy_color(P, strategy="largest_first")
    image = {
        v: (color[v], frozenset(color[w] for w in G[v]))
        for v in G
    }
    for u, v in G.edges:
        i, S = image[u]
        j, T = image[v]
        assert i in T and j in S and S.isdisjoint(T)
    count += 1

assert count == 172
print("universal-target reduction checked on", count, "atlas graphs")


# Exact counterexample parameters. This computes sizes without
# attempting to materialize the enormous graphs.
def lower_parameters(c, h):
    assert 0 <= c < Fraction(1, 9) and h >= 1
    k = int(3*c*h / (1-9*c)) + 1
    m = 2*k + h

    # |Q| = |V(F)| + 2|E(F)|.
    s = comb(m, k) * (1 + comb(m-k, k))
    gap = k - 3*c*(m+k)
    assert gap > 0

    t = int(c*s/gap) + 1
    n = s + 3*(m+k)*t
    assert Fraction(k*t, n) > c
    assert m - 2*k + 2 > h
    return m, k, t, n


for c, h in [
    (Fraction(1, 10), 5),
    (Fraction(11, 100), 5),
    (Fraction(1, 9) - Fraction(1, 10000), 10),
]:
    m, k, t, n = lower_parameters(c, h)
    print("exact parameter check:", c, "target order", h,
          "k =", k, "digits(n) =", len(str(n)))


# Exact verification of the upper-bound numerical gap.
for c in [
    Fraction(1, 9) + Fraction(1, 1000),
    Fraction(1, 8), Fraction(1, 5), Fraction(1, 2), Fraction(1)
]:
    tau = (c - Fraction(1, 9))/10
    assert 9*c - 15*tau > 1


# A non-vacuous equality instance of the six-set packing count.
R = nx.disjoint_union_all([nx.star_graph(2) for _ in range(3)])
IJK = [{1, 2}, {4, 5}, {7, 8}]
neighbors = [
    set().union(*(set(R[v]) for v in S)) for S in IJK
]
six = IJK + neighbors
assert all(not A & B for A, B in it.combinations(six, 2))
assert sum(map(len, IJK)) + 3*min(dict(R.degree()).values()) == 9

print("all checks passed")
```

I ran these checks successfully. In particular, the explicit constructed graphs had orders \(61,124,57,478\); all passed the forbidden-cycle and label tests. The exact parameter computation also verified a counterexample density exceeding
\[
\frac19-\frac1{10000},
\]
against any triangle-free target of order at most \(10\).

**Proved:** every \(c>1/9\) has the stated property, and every \(c<1/9\) does not. Therefore the exact requested infimum is \(1/9\). Nothing remains to establish that infimum.
# agent_1: last reply

The exact infimum is
\[
\boxed{\frac19}.
\]

I will prove both statements needed for this:

* for every \(c>1/9\), the required finite triangle-free target exists;
* for every \(c<1/9\), no finite triangle-free target works.

The proof below is self-contained, including the regularity ingredient. The Python at the end performs actual finite constructions and exhaustive checks of the relevant identities and lemmas.

---

## 1. Turning the problem into a coloring problem

For a triangle-free graph \(G\), define \(J(G)\) on \(V(G)\) by joining distinct vertices whenever there is a walk of length \(1\) or \(3\) between them in \(G\).

We need the following equivalence.

### Lemma 1
A class \(\mathcal C\) of triangle-free graphs admits a common finite triangle-free homomorphic target if and only if
\[
\sup_{G\in\mathcal C}\chi(J(G))<\infty.
\]

### Proof

If \(f:G\to H\) and \(H\) is triangle-free, then \(f\), regarded as a coloring by the vertices of \(H\), properly colors \(J(G)\). Indeed, identically mapped endpoints of a three-edge walk would give a closed three-edge walk in \(H\), hence a triangle.

Conversely, define a finite graph \(U_t\) whose vertices are
\[
(a,S),\qquad a\in[t],\quad S\subseteq[t]\setminus\{a\},
\]
with
\[
(a,S)(b,T)\in E(U_t)
\quad\Longleftrightarrow\quad
a\in T,\ b\in S,\ S\cap T=\varnothing.
\]
This graph is triangle-free: in a purported triangle, the first coordinate of one vertex belongs to both sets associated with the other two vertices, although those sets must be disjoint.

Given a proper \(t\)-coloring \(q\) of \(J(G)\), put
\[
S_v=\{q(w):w\in N_G(v)\},\qquad f(v)=(q(v),S_v).
\]
For an edge \(uv\), the cross-membership conditions hold. Moreover, \(S_u\cap S_v=\varnothing\), since a common color would appear at the ends of a three-edge walk through \(uv\). Thus \(f:G\to U_t\). ∎

We shall repeatedly use another elementary observation:

> A graph containing neither \(C_3\) nor \(C_5\) has no odd closed walk of length at most \(5\).

Indeed, a shortest odd closed subwalk is an odd cycle.

---

# 2. Upper bound: every \(c>1/9\) works

Fix \(c>1/9\). Choose
\[
0<\rho<\frac{c-1/9}{2},
\qquad D=c-2\rho>\frac19.
\]

We first obtain a bounded collection of neighborhood types.

## 2.1. Regularity preparation

Set
\[
\alpha=\rho,\qquad d=\frac{\rho}{10},
\qquad \varepsilon=\left(\frac{\rho}{100}\right)^2.
\]
Choose an integer \(k_0\ge 10/\rho\).

The equitable regularity lemma, proved in Section 4 below, gives a bounded partition
\[
V(G)=W_0\sqcup W_1\sqcup\cdots\sqcup W_r,
\]
where \(|W_0|\le\varepsilon n\), all other parts have the same size \(m\), \(r\ge k_0\), and at most \(\varepsilon r^2\) pairs are not \(\varepsilon\)-regular.

Delete every cluster incident with more than \(\sqrt\varepsilon r\) irregular pairs. There are at most \(2\sqrt\varepsilon r\) such clusters. Add them to the exceptional set.

Write the remaining clusters as \(V_1,\ldots,V_k\), and the enlarged exceptional set as \(V_0\). Define \(R\) on \([k]\) by
\[
ij\in E(R)
\quad\Longleftrightarrow\quad
(V_i,V_j)\text{ is }\varepsilon\text{-regular of density at least }d.
\]

Then
\[
|V_0|\le(\varepsilon+2\sqrt\varepsilon)n<\rho n. \tag{1}
\]

Also, averaging the degrees of vertices in a remaining cluster \(V_i\), the possible contributions from its own cluster, \(V_0\), irregular pairs, and regular pairs of density less than \(d\), give
\[
m\,d_R(i)
\ge
\left(c-\frac1{k_0}-\varepsilon-3\sqrt\varepsilon-d\right)n
\ge(c-\rho)n
\ge Dn. \tag{2}
\]
In particular, \(R\) has no isolated vertex.

For each \(v\in V(G)\), define
\[
S_v=\{i:|N_G(v)\cap V_i|\ge\alpha m\}.
\]
For \(S\subseteq[k]\), let
\[
U(S)=\bigcup_{i\in S}V_i.
\]
By (1),
\[
|N_G(v)\cap U(S_v)|
\ge cn-|V_0|-\alpha n
\ge Dn. \tag{3}
\]
Thus every \(S_v\) is nonempty.

There are boundedly many possible sets \(S_v\). Call these the **types**, and denote their nonempty vertex classes by \(X,Y,Z,\ldots\). The set associated with a type \(X\) is denoted \(S_X\).

All statements below hold once \(n\) is sufficiently large in terms of \(c\). The finitely many smaller orders will be absorbed at the end.

## 2.2. Three consequences of excluding \(C_3,C_5\)

The following regular-pair facts justify all the short-path embeddings we use.

* Between two subsets of size at least \(\alpha m\) in a regular pair of density at least \(d\), there is an edge.
* If \(ij,j\ell\in E(R)\), subsets of size at least \(\alpha m\) in \(V_i,V_\ell\) can be joined by a two-edge path through \(V_j\).

For the second fact, all but at most \(2\varepsilon m\) vertices of \(V_j\) have neighbors in both subsets. These statements remain true after excluding any three prescribed vertices, provided \(m\) is sufficiently large.

They imply:

**(A)** Each \(S_v\) is independent in \(R\).

Otherwise, two neighbors of \(v\) in an appropriate regular pair form a triangle with \(v\).

**(B)** If \(vw\in E(G)\), then
\[
N_R(S_v)\cap N_R(S_w)=\varnothing,
\qquad S_v\cap S_w=\varnothing. \tag{4}
\]
A common member of the first two sets gives a four-edge path from \(v\) to \(w\), which together with \(vw\) is a \(C_5\). The second conclusion follows from the first because \(R\) has no isolated vertices.

**(C)** If distinct \(v,w\) have a common neighbor in \(G\), there is no \(R\)-edge between \(S_v\) and \(S_w\).

Such an edge gives a three-edge path from \(v\) to \(w\) through two clusters. Together with their common neighbor, this is a \(C_5\).

In particular, every type class is independent in \(G\), by (4).

## 2.3. Small types are independent in \(J(G)\)

Call a type \(X\) **small** if
\[
|U(S_X)|<2Dn,
\]
and **large** otherwise.

If \(v,w\in X\) and \(X\) is small, (3) implies that \(v,w\) have a common neighbor in \(U(S_X)\). They cannot also be adjacent in \(J(G)\): the common neighbor and a walk of length \(1\) or \(3\) would give an odd closed walk of length \(3\) or \(5\).

Consequently,
\[
\chi(J(G)[X])=1\qquad\text{for every small type }X. \tag{5}
\]

## 2.4. Auxiliary graphs on a type

Fix three types \(X,Y,Z\). Define \(F_{X;Y,Z}\) on \(X\) by joining \(x,x'\) if there is a path
\[
x-y-z-x',\qquad y\in Y,\ z\in Z,
\]
in either orientation.

We first observe that
\[
\chi(F_{X;Y,Z})
\le 2^{\chi(J(G)[Y])},
\qquad
\chi(F_{X;Y,Z})
\le 2^{\chi(J(G)[Z])}. \tag{6}
\]

For example, properly color \(J(G)[Y]\) with \(r\) colors, and color \(x\in X\) by the set of colors appearing on \(N_G(x)\cap Y\).

For a witness \(x-y-z-x'\), the color of \(y\) appears in the set for \(x\), but not that for \(x'\). Otherwise some \(y'\in N_G(x')\cap Y\) has the same color as \(y\), although
\[
y-z-x'-y'
\]
is a three-edge walk. Thus these sets properly color \(F_{X;Y,Z}\), proving the first inequality; the other is symmetric.

In particular, if \(Y\) or \(Z\) is small, \(F_{X;Y,Z}\) is bipartite.

The crucial assertion is that it is also bipartite when all three types are large.

### Claim
If \(X,Y,Z\) are large, then \(F_{X;Y,Z}\) is bipartite.

### Proof

Suppose it contains an odd cycle. Orient each edge of this cycle according to a chosen witness
\[
x-y-z-x',
\]
from its endpoint adjacent to \(Y\) to its endpoint adjacent to \(Z\).

An odd cycle cannot have every vertex a source or a sink: these would alternate. Therefore some vertex of \(X\) has both a neighbor in \(Y\) and a neighbor in \(Z\).

A witness also supplies a two-edge path between types \(X,Z\) and one between types \(Y,X\). Hence every pair among \(X,Y,Z\) has representatives with a common neighbor. By (A) and (C),
\[
S_X\cup S_Y\cup S_Z
\quad\text{is independent in }R. \tag{7}
\]

The witness has edges between every pair of these types. By (B), the three sets
\[
S_X,S_Y,S_Z
\]
are pairwise disjoint, as are
\[
N_R(S_X),N_R(S_Y),N_R(S_Z).
\]
By (7), none of the first three sets intersects any of the last three.

Each of the first three corresponding cluster unions has size at least \(2Dn\), since the types are large. Each of the last three has size at least \(Dn\), by (2) and the fact that every \(S_X\) is nonempty.

These six disjoint unions therefore contain at least
\[
3(2Dn)+3(Dn)=9Dn>n
\]
vertices, a contradiction. ∎

## 2.5. Bounded coloring, hence a finite target

Let \(L\) be the number of types. It is bounded in terms of \(c\).

For a large type \(X\), every graph \(F_{X;Y,Z}\) is bipartite:

* if \(Y\) or \(Z\) is small, use (5)–(6);
* otherwise use the claim.

Since \(X\) is independent in \(G\), every edge of \(J(G)[X]\) has a three-edge witness. Therefore
\[
J(G)[X]=\bigcup_{Y,Z}F_{X;Y,Z}.
\]
Coloring a union of graphs by the tuple of their colors gives
\[
\chi(J(G)[X])\le 2^{L^2}.
\]
The same bound holds for small types by (5). Using disjoint palettes,
\[
\chi(J(G))\le L\,2^{L^2}. \tag{8}
\]

Both the number of clusters and the lower threshold on \(n\) depend only on \(c\). Thus (8), enlarged to cover smaller graphs, gives a constant \(t=t(c)\) with
\[
\chi(J(G))\le t.
\]
Lemma 1 supplies the required finite triangle-free target \(U_t\).

This proves that every \(c>1/9\) has the property.

---

# 3. Lower bound: no \(c<1/9\) works

We give an explicit finite construction.

## 3.1. Shift graphs of arbitrarily large chromatic number

Let \(S(m,k)\) have as vertices the increasing \(k\)-tuples from \([m]\), with edges
\[
(a_1,\ldots,a_k)(a_2,\ldots,a_{k+1})
\qquad(a_1<\cdots<a_{k+1}).
\]

For each fixed \(k\), these graphs have unbounded chromatic number as \(m\to\infty\).

Here is an elementary proof. Given an \(r\)-coloring of \(S(m,k)\), color a \((k-1)\)-tuple \(A\) by the set of colors of its extensions to the right.

For adjacent \((k-1)\)-tuples
\[
A=(a_1,\ldots,a_{k-1}),\qquad
B=(a_2,\ldots,a_k),
\]
the color of \((a_1,\ldots,a_k)\) belongs to the set for \(A\), but not that for \(B\). Thus
\[
\chi(S(m,k-1))\le 2^{\chi(S(m,k))}.
\]
Since \(S(m,1)=K_m\), iteration proves the assertion.

## 3.2. Many subsets independent against odd three-edge walks

Fix an even integer \(k\ge4\). For
\(\epsilon=(\epsilon_1,\ldots,\epsilon_m)\in\{-1,1\}^m\), define
\[
h_\epsilon(a_1,\ldots,a_k)
=\sum_{j=1}^k(-1)^j\epsilon_{a_j}.
\]

For adjacent vertices \(u,v\) of \(S(m,k)\), cancellation gives
\[
|h_\epsilon(u)+h_\epsilon(v)|\le2. \tag{9}
\]
Consequently, for any three-edge walk \(u_0u_1u_2u_3\),
\[
|h_\epsilon(u_0)+h_\epsilon(u_3)|\le6, \tag{10}
\]
by adding the first and third edge sums and subtracting the second.

Thus the set
\[
I_\epsilon=\{v:h_\epsilon(v)>3\}
\]
contains no two endpoints of a three-edge walk.

For every fixed vertex, the proportion of sign vectors for which it belongs to \(I_\epsilon\) is
\[
p_k
=\frac12-\frac{\binom{k}{k/2}}{2^{k+1}}
       -\frac{\binom{k}{k/2+1}}{2^k},
\qquad p_k\longrightarrow\frac12. \tag{11}
\]
For completeness, writing \(k=2r\),
\[
\frac{\binom{2r}{r}}{4^r}
=\prod_{j=1}^r\left(1-\frac1{2j}\right)
\le (r+1)^{-1/2}\longrightarrow0,
\]
and the other binomial coefficient in (11) is smaller.

## 3.3. The graph obstructing small triangle-free targets

Fix \(c<1/9\) and a finite triangle-free graph \(H\).

Choose even \(k\) so large that, writing \(p=p_k\),
\[
\frac{p}{3(1+p)}>c. \tag{12}
\]
Choose \(m\) with
\[
\chi(F)>|V(H)|,\qquad F=S(m,k).
\]

Replace every edge \(uv\) of \(F\) by a path
\[
x_u-y_{uv}-z_{uv}-x_v,
\]
choosing an arbitrary orientation \(u\to v\) for each edge. Call the resulting graph \(Q\), with its three independent classes \(Q_0,Q_1,Q_2\) of original, first internal, and second internal vertices.

Define a homomorphism \(\ell:Q\to F\) by
\[
\ell(x_u)=u,\qquad \ell(y_{uv})=v,\qquad \ell(z_{uv})=u.
\]

Choose a positive integer \(M\), and put \(N=M2^m\). For each \(i=0,1,2\):

* add an independent set \(U_i\), consisting of \(M\) copies of every sign vector \(\epsilon\in\{-1,1\}^m\);
* add an independent set \(V_i\) of size \(pN\);
* join \(U_i\) completely to \(V_i\);
* join \(q\in Q_i\) to the copies of \(\epsilon\) precisely when
  \[
  h_\epsilon(\ell(q))>3.
  \]

There are no other edges. Since \(m\ge k\), \(pN\) is an integer.

Call the graph \(G\). Every vertex of \(Q\) gets exactly \(pN\) neighbors in its corresponding \(U_i\). Every vertex of \(U_i\) has \(pN\) neighbors in \(V_i\), and every vertex of \(V_i\) has \(N\) neighbors. Hence
\[
\delta(G)\ge pN,\qquad
|V(G)|=|V(Q)|+3(1+p)N. \tag{13}
\]
By (12), sufficiently large \(M\) makes
\[
\delta(G)\ge c|V(G)|.
\]

### There are no triangles or five-cycles

The graph \(Q\) itself has no cycle of length less than \(9\).

A triangle or five-cycle cannot contain a vertex of \(V_i\). For a five-cycle through such a vertex, the remaining three-edge path between its two neighbors in \(U_i\) would require an edge inside \(Q_i\cup V_i\), but this set is independent.

Now consider a short odd cycle avoiding all \(V_i\).

* A triangle using \(U_i\) would require an edge within \(Q_i\).
* A five-cycle using exactly one vertex of some \(U_i\) gives a three-edge path in \(Q\) between two of its neighbors. Applying \(\ell\) and (10), their scores cannot both exceed \(3\).
* A five-cycle using two vertices from the \(U_i\)'s has the form
  \[
  u-q-u'-q'-q''-u.
  \]
  The common neighbor \(q\) forces \(u,u'\) to belong to the same \(U_i\). Then \(q',q''\in Q_i\), contradicting their adjacency.

Thus \(G\) contains neither \(C_3\) nor \(C_5\).

### There is no homomorphism \(G\to H\)

Suppose \(f:G\to H\). For each edge \(uv\in E(F)\), its replacing three-edge path in \(Q\) shows that
\[
f(x_u)\ne f(x_v),
\]
because otherwise its image is a closed three-edge walk in the triangle-free graph \(H\).

Therefore \(u\mapsto f(x_u)\) is a proper coloring of \(F\) with at most \(|V(H)|\) colors, contradicting the choice of \(F\).

This constructs, for every finite triangle-free \(H\), a counterexample of minimum-degree ratio at least \(c\). Hence no \(c<1/9\) has the required property.

---

# 4. Proof of the regularity ingredient

Here are the details needed to make the upper bound independent of an unproved regularity theorem.

For disjoint nonempty sets \(A,B\), write
\[
d(A,B)=\frac{e(A,B)}{|A||B|}.
\]
The pair is \(\varepsilon\)-regular if every \(A'\subseteq A,B'\subseteq B\) with
\[
|A'|\ge\varepsilon|A|,\qquad |B'|\ge\varepsilon|B|
\]
satisfies
\[
|d(A',B')-d(A,B)|\le\varepsilon.
\]

We prove that, for fixed \(\varepsilon>0,k_0\), sufficiently large graphs have an equitable partition into boundedly many clusters, an exceptional set of size at most \(\varepsilon n\), and at most \(\varepsilon k^2\) irregular cluster pairs.

For a partition \(\mathcal P\), define its energy by
\[
\mathcal E(\mathcal P)
=\frac1{n^2}\sum_{A,B\in\mathcal P}|A||B|d(A,B)^2,
\]
using ordered adjacency densities also when \(A=B\). It lies in \([0,1]\), and refinement cannot decrease it, by the weighted mean-square inequality.

Start with \(k_0\) equal clusters and fewer than \(k_0\) exceptional vertices, treating exceptional vertices as singleton parts for energy calculations.

Suppose there are more than \(\varepsilon k^2\) irregular pairs among equal clusters of size \(m\). Choose a witnessing rectangle for each irregular pair and refine every cluster by all its witnessing subsets. There are at most \(2^k\) resulting cells per cluster.

For each irregular ordered block, the energy increases by at least
\[
\frac{m^2}{n^2}\varepsilon^4:
\]
the witness has relative area at least \(\varepsilon^2\), and its density differs by more than \(\varepsilon\). Accounting for both orders, the total increase exceeds
\[
2\varepsilon^5\left(\frac{km}{n}\right)^2.
\]
While the exceptional set has size at most \(n/2\), this is at least \(\varepsilon^5/2\).

It remains to keep the clusters equal without losing control of the exception. Put
\[
s=\left\lceil4\varepsilon^{-5}\right\rceil,\qquad
B(k)=\left\lceil\frac{4s\,2^k}{\varepsilon}\right\rceil.
\]
After the witness refinement, subdivide every cell into pieces of common size
\[
q=\left\lfloor\frac{m}{B(k)}\right\rfloor
\]
and put its remainder into the exceptional set as singletons. This is still a refinement, so energy does not decrease. The number of newly exceptional vertices is at most
\[
k2^kq\le\frac{\varepsilon n}{4s}.
\]
Provided \(m\ge2B(k)\), the new number of clusters is at most \(4kB(k)\).

Starting from \(k_0\), iterating the finite bound
\[
K\longmapsto4KB(K)
\]
for \(s\) steps bounds every cluster count by a finite constant \(K_*\). Taking \(n\) sufficiently large ensures \(m\ge2B(K_*)\), and makes the initial exception at most \(\varepsilon n/4\).

There can be fewer than \(s\) energy-increasing rounds, since energy is at most \(1\). The total exception remains below \(\varepsilon n\). Therefore the process terminates with the required regular partition. Increasing the threshold on \(n\) makes the final cluster size exceed any prescribed constant.

Finally, the short-path facts used in Section 2 follow directly from regularity: for a subset \(A\) of one side of size at least \(\varepsilon m\), fewer than \(\varepsilon m\) vertices on the other side have fewer than
\[
(d-\varepsilon)|A|
\]
neighbors in \(A\). Apply this to one or two prescribed subsets. With the parameters in Section 2 and sufficiently large clusters, the paths can avoid any three prescribed vertices.

This completes the regularity argument used above.

---

# 5. Executed Python checks

These computations are **checks of finite instances and algebraic ingredients**, not substitutes for the quantified proofs above.

The code:

* constructs the triangle-free universal targets;
* checks the explicit homomorphisms on all 150 relevant nonempty graph-atlas graphs;
* constructs the 435-vertex lower-bound example and checks that it has no closed walks of lengths \(3\) or \(5\);
* checks every sign assignment and every three-edge walk for the small shift-graph instance;
* exhausts all 1,080 proper three-colorings of \(S(5,2)\);
* checks 5,790 energy-increment witnesses using exact rational arithmetic;
* checks the regularity parameter inequalities.

```python
import itertools as it
from fractions import Fraction as Fr
from math import comb, ceil
import networkx as nx
import numpy as np

# ---------- Universal triangle-free targets ----------

def universal(t):
    vertices = [(a, S) for a in range(t)
                for S in range(1 << t) if not (S >> a & 1)]
    H = nx.Graph()
    H.add_nodes_from(vertices)
    for (a, S), (b, T) in it.combinations(vertices, 2):
        if (S >> b & 1) and (T >> a & 1) and not (S & T):
            H.add_edge((a, S), (b, T))
    assert sum(nx.triangles(H).values()) == 0
    return H

targets = {t: universal(t) for t in range(1, 8)}
checked = 0
for G in nx.graph_atlas_g():
    if not len(G):
        continue
    A = nx.to_numpy_array(G, nodelist=range(len(G)), dtype=np.int64)
    A3 = A @ A @ A
    if np.trace(A3) or np.trace(A3 @ A @ A):
        continue

    J = nx.from_numpy_array(((A + A3) > 0).astype(int))
    assert nx.number_of_selfloops(J) == 0
    q = nx.coloring.greedy_color(J, strategy="largest_first")
    t = max(q.values()) + 1
    f = {
        v: (q[v], sum(1 << a for a in {q[w] for w in G[v]}))
        for v in G
    }
    assert all(f[v] in targets[t] for v in G)
    assert all(targets[t].has_edge(f[u], f[v]) for u, v in G.edges())
    checked += 1
assert checked == 150
print("Atlas homomorphism checks:", checked)

# ---------- Exact lower-bound probabilities ----------

def probability(k):
    assert k >= 4 and k % 2 == 0
    return Fr((1 << k) - comb(k, k//2) - 2*comb(k, k//2+1),
              1 << (k+1))

for c in [Fr(1,20), Fr(1,10), Fr(21,200), Fr(11,100)]:
    k = 4
    while probability(k) <= 3*c/(1-3*c):
        k *= 2
    p = probability(k)
    assert p - 3*c*(1+p) > 0
    print(float(c), k, float(p/(3*(1+p))))

# ---------- A complete finite lower-bound graph ----------

def lower_example(m, k, copies):
    F = nx.Graph()
    F.add_nodes_from(it.combinations(range(m), k))
    oriented = []
    for w in it.combinations(range(m), k+1):
        a, b = w[:-1], w[1:]
        F.add_edge(a, b)
        oriented.append((a, b))

    Q = nx.Graph()
    group, label = {}, {}
    for a in F:
        x = ("x", a)
        Q.add_node(x)
        group[x], label[x] = 0, a

    for j, (a, b) in enumerate(oriented):
        y, z = ("y", j), ("z", j)
        Q.add_edges_from([(("x", a), y), (y, z), (z, ("x", b))])
        group[y], group[z] = 1, 2
        label[y], label[z] = b, a

    assert all(group[a] != group[b] for a, b in Q.edges())
    assert all(F.has_edge(label[a], label[b]) for a, b in Q.edges())

    def score(mask, a):
        return sum((-1 if j % 2 == 0 else 1)
                   * (1 if mask >> x & 1 else -1)
                   for j, x in enumerate(a))

    # Exhaust the score inequalities, including all three-edge walks.
    for mask in range(1 << m):
        h = {a: score(mask, a) for a in F}
        assert all(abs(h[a] + h[b]) <= 2 for a, b in F.edges())
        for a in F:
            for b in F[a]:
                for d in F[b]:
                    for e in F[d]:
                        assert abs(h[a] + h[e]) <= 6

    p = probability(k)
    N = copies * (1 << m)
    vsize = p*N
    assert vsize.denominator == 1
    vsize = int(vsize)
    G = Q.copy()

    for i in range(3):
        U = [("u", i, mask, r)
             for mask in range(1 << m) for r in range(copies)]
        V = [("v", i, r) for r in range(vsize)]
        G.add_nodes_from(U + V)
        G.add_edges_from(it.product(U, V))
        for x in Q:
            if group[x] == i:
                G.add_edges_from((x, u) for u in U
                                 if score(u[2], label[x]) > 3)

    assert len(G) == len(Q) + 3*(1+p)*N
    assert min(dict(G.degree()).values()) >= p*N

    A = nx.to_scipy_sparse_array(G, dtype=np.int64, format="csr")
    A2, A3 = A @ A, A @ A @ A
    assert int(A3.diagonal().sum()) == 0
    # trace(A^5) = sum_ij (A^3)_ij (A^2)_ji
    assert int(A3.multiply(A2.T).sum()) == 0

    print("Constructed graph:", len(G),
          "vertices; minimum degree", min(dict(G.degree()).values()),
          "; no C3 or C5")

lower_example(6, 4, 2)

# ---------- Exhaustive color-set descent ----------

vertices = list(it.combinations(range(5), 2))
edges = [(w[:-1], w[1:]) for w in it.combinations(range(5), 3)]
proper = 0
for values in it.product(range(3), repeat=len(vertices)):
    q = dict(zip(vertices, values))
    if any(q[a] == q[b] for a, b in edges):
        continue
    sets = {
        a: frozenset(q[(a, b)] for b in range(a+1, 5))
        for a in range(5)
    }
    assert len(set(sets.values())) == 5  # A proper coloring of K5.
    proper += 1
assert proper == 1080
print("Color-set descent checks:", proper)

# ---------- Exact energy-increment checks ----------

energy_checks = 0
for bits in range(1 << 9):
    a = [[bits >> (3*i+j) & 1 for j in range(3)] for i in range(3)]
    density = Fr(sum(map(sum, a)), 9)
    for amask in range(1, 8):
        AA = [i for i in range(3) if amask >> i & 1]
        AC = [i for i in range(3) if not (amask >> i & 1)]
        for bmask in range(1, 8):
            BB = [j for j in range(3) if bmask >> j & 1]
            BC = [j for j in range(3) if not (bmask >> j & 1)]
            witness = Fr(sum(a[i][j] for i in AA for j in BB),
                         len(AA)*len(BB))
            if abs(witness-density) <= Fr(1, 3):
                continue
            energy = Fr(0)
            for C in [AA, AC]:
                for D in [BB, BC]:
                    if C and D:
                        e = sum(a[i][j] for i in C for j in D)
                        energy += Fr(e*e, 9*len(C)*len(D))
            gain = energy - density*density
            assert gain >= Fr(len(AA)*len(BB), 9)*(witness-density)**2
            assert gain >= Fr(1, 3)**4
            energy_checks += 1
assert energy_checks == 5790
print("Energy-increment checks:", energy_checks)

# ---------- Upper-bound parameter inequalities ----------

for c in [Fr(1,8), Fr(1,5), Fr(2,5)]:
    rho = (c-Fr(1,9))/4
    alpha, d, eps = rho, rho/10, (rho/100)**2
    k0, m0 = ceil(10/rho), ceil(100/eps)
    assert c-2*rho > Fr(1,9)
    assert Fr(1,k0) + eps + 3*rho/100 + d < rho
    assert eps + 2*rho/100 < rho
    assert alpha*m0-3 >= eps*m0
    assert (d-eps)*(alpha*m0-3) >= 2
    assert (1-2*eps)*m0 > 3
print("Regularity parameter checks passed")
```

The principal outputs are:
```text
Atlas homomorphism checks: 150
0.05 16 0.06172317613464463
0.1 512 0.10301467086870825
0.105 1024 0.10543755194936123
0.11 32768 0.11012732658415923
Constructed graph: 435 vertices; minimum degree 8 ; no C3 or C5
Color-set descent checks: 1080
Energy-increment checks: 5790
Regularity parameter checks passed
```

Therefore every \(c>1/9\) works and every \(c<1/9\) fails. **The requested infimum is \(1/9\); both halves are proved, and nothing remains for the stated problem.**
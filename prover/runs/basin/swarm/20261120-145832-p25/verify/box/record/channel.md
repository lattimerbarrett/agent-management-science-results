#1 agent_1: \[
\boxed{\frac19}
\]

The target is required to be triangle-free, but it need not be \(C_5\)-free. That distinction matters.

I prove the following two statements.

1. For every \(c>1/9\), there is a finite triangle-free graph receiving a homomorphism from every \(\{C_3,C_5\}\)-free graph of minimum degree at least \(c|V(G)|\).
2. For every \(c<1/9\) and every finite triangle-free graph \(H\), there is a \(\{C_3,C_5\}\)-free graph \(G\) with \(\delta(G)\ge c|V(G)|\) and \(G\nrightarrow H\).

The proof uses two classical general theorems: the Szemerédi regularity lemma and the Borsuk–Ulam theorem. The graph-specific arguments are given below, including a derivation of the Kneser-graph fact used in the construction. No homomorphism-threshold theorem is being used as a black box.

## 1. Preliminary facts

### Odd closed walks

A graph containing an odd closed walk of length at most \(5\) contains a \(C_3\) or a \(C_5\).

Indeed, a shortest odd closed subwalk is an odd cycle. Consequently, in a \(\{C_3,C_5\}\)-free graph:

- there is no closed walk of length \(3\) or \(5\);
- if two vertices have a common neighbor, there is no walk of length \(3\) between them.

Walks here may repeat vertices.

### Kneser graphs

Write \(K(m,k)\) for the graph whose vertices are the \(k\)-subsets of \([m]\), with two vertices adjacent when they are disjoint. We need
\[
\chi(K(m,k))\ge m-2k+2. \tag{1}
\]

Here is a proof, included to specify the non-elementary ingredient precisely.

The **octahedral Tucker lemma** says that there is no antipodal labeling
\[
\lambda:\{-1,0,1\}^{m}\setminus\{0\}\longrightarrow
\{\pm1,\ldots,\pm(m-1)\}
\]
such that
\[
x\preceq y\quad\Longrightarrow\quad \lambda(x)\ne-\lambda(y),
\]
where \(x\preceq y\) means that every nonzero coordinate of \(x\) agrees with the corresponding coordinate of \(y\).

This follows from Borsuk–Ulam: the order complex of these signed vectors is the barycentric subdivision of the boundary of the \(m\)-dimensional cross-polytope. Such a labeling would give an odd map
\[
S^{m-1}\longrightarrow S^{m-2},
\]
by mapping each label to the corresponding signed coordinate vector and normalizing on each simplex. Borsuk–Ulam rules out that map.

Suppose now that \(K(m,k)\) had a proper coloring with
\[
r=m-2k+1
\]
colors. For a signed vector \(x\), let \(\operatorname{alt}(x)\) be the number of alternating sign runs in its nonzero coordinates, read in coordinate order.

- If \(\operatorname{alt}(x)\le 2k-2\), label \(x\) by \(\operatorname{alt}(x)\), with the sign of its first nonzero coordinate.
- Otherwise, one of \(x^+\) and \(x^-\) contains a \(k\)-subset. Among the colors of all \(k\)-subsets contained in either side, choose the least color \(a\). It occurs on only one side, since a \(k\)-subset of \(x^+\) and one of \(x^-\) are disjoint. Give \(x\) label
  \[
  \pm(2k-2+a),
  \]
  with the sign of that side.

This is antipodal and uses labels of absolute value at most \(m-1\).

There cannot be complementary labels on comparable vectors:

- For two small labels, equal alternation number and opposite first signs are impossible under \(x\preceq y\): the earlier opposite sign in \(y\), followed by a longest alternating subsequence of \(x\), would increase the alternation number.
- Small and large labels have different absolute-value ranges.
- For two large complementary labels, the corresponding equally colored \(k\)-sets lie in opposite sides of the larger signed vector, so they are disjoint—a contradiction.

Tucker’s lemma proves (1).

---

## 2. Lower bound: no \(c<1/9\) works

Fix \(c<1/9\) and a finite triangle-free graph \(H\). Put
\[
q=\max\{1,|V(H)|\}.
\]
Choose \(k\) sufficiently large, and set
\[
m=2k+q,
\]
so that
\[
\frac{k}{3(m+k)}>c. \tag{2}
\]
This is possible because the ratio tends to \(1/9\).

Let
\[
F=K(m,k).
\]
By (1),
\[
\chi(F)\ge m-2k+2=q+2>|V(H)|. \tag{3}
\]

### 2.1 The core

Replace every edge \(uv\) of \(F\) by a path
\[
u-a_{uv}-b_{uv}-v
\]
of length \(3\), orienting each original edge arbitrarily to distinguish \(a_{uv}\) from \(b_{uv}\). Call the resulting graph \(D\).

Partition its vertices into three independent sets:
\[
D_0=V(F),\qquad D_1=\{a_{uv}\},\qquad D_2=\{b_{uv}\}.
\]

Assign each core vertex a \(k\)-subset label:
\[
L(u)=u,\qquad L(a_{uv})=u,\qquad L(b_{uv})=v.
\]

The important property is:
\[
\begin{split}
x,y\in D_i,\ \text{and there is a length-3 walk from }x\text{ to }y\\
\Longrightarrow L(x)\cap L(y)=\varnothing. \tag{4}
\end{split}
\]

To check this, a length-\(3\) walk starting and ending in the same one of the three classes must traverse all three edge types. For \(D_0\), it traverses one subdivided original edge. For \(D_1\), it has one of the forms
\[
a_{uv}-b_{uv}-v-a_{vw},
\qquad
a_{uv}-u-b_{wu}-a_{wu},
\]
and the two labels are respectively \(u,v\) or \(u,w\), which are adjacent in the Kneser graph. The \(D_2\) case is symmetric.

Also, every cycle of \(D\) has length at least \(9\).

### 2.2 The dense part

For each \(i\in\{0,1,2\}\), add disjoint independent sets
\[
U_{i,1},\ldots,U_{i,m},W_i
\]
of sizes
\[
|U_{i,j}|=t,\qquad |W_i|=kt.
\]
Add:

- all edges between \(W_i\) and \(\bigcup_{j=1}^m U_{i,j}\);
- all edges between a core vertex \(x\in D_i\) and \(U_{i,j}\) whenever \(j\in L(x)\).

There are no other edges. Call the resulting graph \(G\).

Every core vertex has at least \(kt\) neighbors in the dense part. Every vertex of a set \(U_{i,j}\) has \(kt\) neighbors in \(W_i\), and every vertex of \(W_i\) has \(mt\ge kt\) neighbors. Thus
\[
\delta(G)\ge kt.
\]
If \(N=|V(D)|\), then
\[
|V(G)|=N+3(m+k)t.
\]
By (2), choosing \(t\) sufficiently large gives
\[
kt\ge c\bigl(N+3(m+k)t\bigr).
\]
Hence
\[
\delta(G)\ge c|V(G)|. \tag{5}
\]

### 2.3 No triangles or pentagons

There is no triangle:

- the core has none;
- every \(U_{i,j}\) has core neighbors only in the independent set \(D_i\);
- \(N(W_i)=\bigcup_jU_{i,j}\) is independent.

Now consider a possible \(5\)-cycle.

**It cannot contain a vertex of \(W_i\).**  
Such a cycle would have the form
\[
w-u-x-y-u'-w,
\]
where \(u,u'\in\bigcup_jU_{i,j}\). But \(x,y\) both belong to \(W_i\cup D_i\), which is independent.

**If it contains exactly one \(U\)-vertex**, its other four vertices form a length-\(3\) core path between two vertices of the same \(D_i\). Both labels contain the index of that \(U\)-set, contradicting (4).

**If it contains two \(U\)-vertices**, their shared intermediate core vertex forces both \(U\)-vertices to have the same index \(i\). The other two core vertices then also lie in \(D_i\), but the cycle requires an edge between them.

Three \(U\)-vertices cannot lie on a \(5\)-cycle, since all \(U\)-vertices are independent. A cycle contained in the core has length at least \(9\).

Therefore \(G\) is \(\{C_3,C_5\}\)-free.

### 2.4 No homomorphism to \(H\)

Suppose \(f:G\to H\) were a homomorphism.

For every edge \(uv\in E(F)\), its replacement path maps to a walk
\[
f(u)-f(a_{uv})-f(b_{uv})-f(v).
\]
If \(f(u)=f(v)\), this is a closed walk of length \(3\) in \(H\), impossible because \(H\) is triangle-free.

Thus the restriction of \(f\) to \(V(F)\) is a proper coloring of \(F\) with at most \(|V(H)|\) colors, contradicting (3).

Together with (5), this proves the lower bound.

---

## 3. A regularity consequence for the upper bound

We use the usual equitable form of the Szemerédi regularity lemma: given \(\varepsilon>0\) and a minimum number of parts, every sufficiently large graph has a partition
\[
V(G)=V_0\cup V_1\cup\cdots\cup V_k
\]
with small \(V_0\), equally sized other parts, bounded \(k\), and few irregular pairs.

The following minimum-degree consequence will be useful.

### Regularity consequence

Given \(c>0,\eta>0,\alpha>0\), one can choose \(d,\varepsilon>0\), with
\[
\varepsilon<\min\{\alpha,d,1/3\},
\]
and constants \(M,n_0\), such that every graph \(G\) on \(n\ge n_0\) vertices with \(\delta(G)\ge cn\) has a partition
\[
V(G)=V_0\cup V_1\cup\cdots\cup V_k,\qquad |V_i|=s\quad(i\ge1),
\]
and a reduced graph \(R\) on \([k]\) satisfying:

1. \(|V_0|\le\eta n\) and \(k\le M\);
2. \(\delta(R)\ge(c-\eta)k\);
3. every edge \(ij\in E(R)\) corresponds to an \(\varepsilon\)-regular pair of density at least \(d\).

Here is the derivation, so the minimum-degree assertion is explicit.

Apply regularity with \(p\) equal parts, where \(p\ge t\). Discard every part having more than \(\sqrt\varepsilon p\) irregular partners. There are at most \(2\sqrt\varepsilon p\) such parts. Define \(R\) on the remaining parts, using regular pairs of density at least \(d\).

For a surviving part, its average degree in \(G\) is at most
\[
|V_0|+s+\sqrt\varepsilon ps+dks+d_R(i)s.
\]
Consequently,
\[
d_R(i)s\ge
\left(c-\varepsilon-3\sqrt\varepsilon-d-\frac1t\right)n.
\]
Choose the parameters so that
\[
\varepsilon+3\sqrt\varepsilon+d+\frac1t<\eta.
\]
Since \(n/s\ge k\), the asserted minimum degree follows. The enlarged exceptional set also has size at most \(\eta n\).

### Two elementary regular-pair facts

For the chosen parameters:

- if \(ij\in E(R)\), any subsets \(X\subseteq V_i\), \(Y\subseteq V_j\) of size at least \(\alpha s\) have an edge between them;
- if \(ih,jh\in E(R)\), and \(X\subseteq V_i\), \(Y\subseteq V_j\) have size at least \(\alpha s\), there is a length-\(2\) walk from \(X\) to \(Y\) through \(V_h\).

For the second fact, all but at most \(\varepsilon s\) vertices of \(V_h\) have a neighbor in \(X\), and the same holds for \(Y\). As \(2\varepsilon<1\), some vertex has both. This also works when \(i=j\).

---

## 4. Upper bound: every \(c>1/9\) works

Fix \(c>1/9\). Choose \(\eta>0\) such that
\[
c-2\eta>0,\qquad 9c-15\eta>1. \tag{6}
\]
For example,
\[
\eta=\frac{9c-1}{30}
\]
works. Choose \(0<\alpha\le\eta\), and apply the regularity consequence.

Let \(G\) be \(\{C_3,C_5\}\)-free with \(\delta(G)\ge cn\), where \(n\ge n_0\).

For every vertex \(v\), define its **support**
\[
A(v)=\{i\in[k]:|N_G(v)\cap V_i|\ge\alpha s\},
\]
and, for a support \(A\), put
\[
B(A)=N_R(A).
\]

At most \(|V_0|+\alpha ks\le2\eta n\) neighbors of \(v\) lie outside its support parts. Thus
\[
\left|N_G(v)\cap\bigcup_{i\in A(v)}V_i\right|
\ge(c-2\eta)n. \tag{7}
\]
In particular, all supports are nonempty.

### 4.1 Three forbidden configurations

The regular-pair facts and the absence of odd closed walks of length \(3\) or \(5\) give:

**(a) Every support is independent in \(R\).**

An edge between two support parts of \(v\) would give a triangle through \(v\).

**(b) If \(uv\in E(G)\), then**
\[
B(A(u))\cap B(A(v))=\varnothing. \tag{8}
\]

Otherwise, the second regular-pair fact gives a length-\(2\) walk between a neighbor of \(u\) and a neighbor of \(v\). Together with \(uv\), this is a closed walk of length \(5\).

**(c) If there is a length-\(2\) walk from \(u\) to \(w\), then**
\[
E_R(A(u),A(w))=\varnothing. \tag{9}
\]

An edge between these support sets would, by the first regular-pair fact, supply a length-\(3\) walk from \(u\) to \(w\), producing an odd closed walk of length \(5\).

Because \(\delta(R)>0\), every \(B(A)\) is nonempty. It follows from (8) that vertices having the same support are never adjacent.

### 4.2 Light supports

Call a support \(A\) **light** if
\[
|A|s<2(c-2\eta)n,
\]
and **heavy** otherwise.

If \(u,w\) have the same light support, (7) implies that their neighborhoods inside the support parts intersect. Therefore there is no length-\(3\) walk between \(u\) and \(w\).

Thus:
\[
\text{Each light support class contains no two endpoints of a length-3 walk.} \tag{10}
\]

### 4.3 A bounded refinement

Partition vertices first by their support. There are at most \(2^k\) such classes.

Refine this partition by also recording, for each vertex, **which support classes contain at least one of its neighbors**.

There are at most
\[
L=2^k\,2^{2^k}\le 2^{M+2^M} \tag{11}
\]
refined classes. Form the quotient graph \(T\): two distinct classes are adjacent when some edge of \(G\) joins them.

There are no edges within a class, as noted after (9). Hence \(G\to T\).

I claim that \(T\) is triangle-free.

### 4.4 A quotient triangle cannot involve a light class

Suppose quotient classes \(X,Y,Z\) form a triangle, and the support class containing \(X\) is light.

Choose an edge \(yz\) between \(Y\) and \(Z\). Because the refinement records neighboring support classes:

- \(y\) has a neighbor \(x\) in the support class of \(X\);
- \(z\) has a neighbor \(x'\) in that same support class.

Then
\[
x-y-z-x'
\]
is a length-\(3\) walk with both endpoints in one light class, contradicting (10).

So all three supports of a quotient triangle must be heavy.

### 4.5 Three heavy classes require too many parts

Suppose \(X_1,X_2,X_3\) form a quotient triangle. Write
\[
A_i=A(X_i),\qquad B_i=N_R(A_i).
\]

By (8), the three \(B_i\) are pairwise disjoint.

For any distinct \(i,j\), the third quotient class contains a vertex having neighbors in both support classes \(A_i,A_j\). Thus (9) gives
\[
E_R(A_i,A_j)=\varnothing.
\]
Together with (a), this says that \(A_1\cup A_2\cup A_3\) is independent.

The six sets
\[
A_1,A_2,A_3,B_1,B_2,B_3
\]
are pairwise disjoint:

- the \(B_i\) are pairwise disjoint;
- if \(x\in A_i\cap A_j\), then \(N_R(x)\subseteq B_i\cap B_j\), contradicting \(\delta(R)>0\);
- no \(A_i\) meets any \(B_j\), since their union of \(A\)-sets is independent.

Each \(A_i\) is heavy, so
\[
|A_i|\ge \frac{2(c-2\eta)n}{s}\ge2(c-2\eta)k.
\]
Also, each nonempty \(A_i\) has
\[
|B_i|\ge\delta(R)\ge(c-\eta)k.
\]
The six disjoint sets would therefore contain at least
\[
3\cdot2(c-2\eta)k+3(c-\eta)k
=(9c-15\eta)k>k
\]
vertices of \(R\), contradicting (6).

Thus \(T\) is triangle-free.

### 4.6 One target for all \(G\)

By (11), every sufficiently large eligible \(G\) maps to a triangle-free graph on at most \(L\) vertices, where \(L\) depends only on \(c\).

Take \(H_c\) to be the disjoint union of representatives of every triangle-free graph on at most
\[
\max\{L,n_0\}
\]
vertices. This is a finite triangle-free graph.

Large eligible graphs map to one of its quotient components. Graphs with fewer than \(n_0\) vertices occur themselves among its components.

This proves the upper bound.

---

## 5. Executable checks

The proof above handles the infinite quantifiers. Finite computations cannot replace those arguments, the regularity lemma, or Borsuk–Ulam.

Here is Python that I actually ran. It checks:

- explicit lower-bound constructions, including their vertex counts and minimum degrees;
- absence of triangles and \(5\)-cycles, using exact integer matrix arithmetic;
- the crucial same-class length-\(3\) label property;
- small Kneser chromatic numbers using a SAT solver;
- the small-label comparability assertion in the Tucker argument;
- the six-set counting argument on every graph in the NetworkX atlas with at most six vertices;
- exact rational choices of lower-bound parameters;
- the upper-bound slack identities symbolically.

```python
import itertools as it
from fractions import Fraction
from math import comb

import networkx as nx
import numpy as np
import sympy as sp
from z3 import Solver, Int, And, sat


def kneser(m, k):
    sets = list(it.combinations(range(m), k))
    masks = [sum(1 << x for x in s) for s in sets]
    F = nx.Graph()
    F.add_nodes_from(range(len(sets)))
    F.add_edges_from(
        (i, j)
        for i in range(len(sets))
        for j in range(i)
        if not masks[i] & masks[j]
    )
    return F, masks


def construction(m, k, t):
    F, labels = kneser(m, k)
    G = nx.Graph()
    G.add_nodes_from(range(len(F)))
    colors = {v: 0 for v in F}
    lab = dict(enumerate(labels))
    nxt = len(F)

    for u, v in F.edges():
        a, b = nxt, nxt + 1
        nxt += 2
        G.add_edges_from([(u, a), (a, b), (b, v)])
        colors[a], colors[b] = 1, 2
        lab[a], lab[b] = labels[u], labels[v]

    core = G.copy()

    for i in range(3):
        U = {
            a: list(range(nxt + a*t, nxt + (a+1)*t))
            for a in range(m)
        }
        nxt += m*t
        W = list(range(nxt, nxt + k*t))
        nxt += k*t
        G.add_nodes_from(W)

        for a in range(m):
            G.add_nodes_from(U[a])
            G.add_edges_from(it.product(U[a], W))

        for v in core:
            if colors[v] == i:
                for a in range(m):
                    if (lab[v] >> a) & 1:
                        G.add_edges_from((v, x) for x in U[a])

    return F, core, G, colors, lab


def chromatic(F):
    vs = list(F)
    x = {v: Int("x" + str(v)) for v in vs}
    for q in range(1, len(F) + 1):
        s = Solver()
        s.add([And(x[v] >= 0, x[v] < q) for v in vs])
        s.add([x[u] != x[v] for u, v in F.edges()])
        if s.check() == sat:
            return q


for m, k, t in [(5, 2, 1), (6, 2, 2),
                (7, 2, 1), (8, 3, 1)]:
    F, C, G, col, lab = construction(m, k, t)

    A = nx.to_numpy_array(G, nodelist=list(G), dtype=np.int64)
    A2 = A @ A
    A3 = A2 @ A

    # In a simple graph, these traces count closed walks.
    assert np.trace(A3) == 0
    assert np.trace(A2 @ A3) == 0

    D = nx.to_numpy_array(C, nodelist=list(C), dtype=np.int64)
    D3 = D @ D @ D
    for u in C:
        for v in C:
            if col[u] == col[v] and D3[u, v]:
                assert lab[u] & lab[v] == 0

    assert len(G) == (
        len(F) + 2*F.number_of_edges() + 3*(m+k)*t
    )
    delta = min(dict(G.degree()).values())
    assert delta >= k*t

    chi = chromatic(F)
    assert chi == m - 2*k + 2
    print("lower:", (m, k, t),
          "core", len(C), "n", len(G),
          "delta", delta, "chi(F)", chi)


# Check the small-label part of the Tucker argument.
def low_label(z):
    seq = [s for s in z if s]
    alt = 1 + sum(a != b for a, b in zip(seq, seq[1:]))
    return seq[0] * alt


for m in range(1, 8):
    count = 0
    for y in it.product((-1, 0, 1), repeat=m):
        supp = [i for i in range(m) if y[i]]
        if not supp:
            continue
        ly = low_label(y)
        for bits in range(1, 1 << len(supp)):
            x = [0] * m
            for j, a in enumerate(supp):
                if (bits >> j) & 1:
                    x[a] = y[a]
            assert low_label(x) != -ly
            count += 1
    print("Tucker comparable pairs:", m, count)


# Exhaustive six-set check on the graph atlas through six vertices.
cases = 0
for R in nx.graph_atlas_g():
    n = len(R)
    if not 1 <= n <= 6:
        continue
    if min(dict(R.degree()).values()) == 0:
        continue

    N = [sum(1 << w for w in R[v]) for v in range(n)]
    supports = []
    for a in range(1, 1 << n):
        b = 0
        for v in range(n):
            if (a >> v) & 1:
                b |= N[v]
        if not a & b:  # a is independent
            supports.append((a, b))

    for triple in it.combinations(supports, 3):
        aa = [p[0] for p in triple]
        bb = [p[1] for p in triple]

        if any(bb[i] & bb[j]
               for i in range(3) for j in range(i)):
            continue
        if any(aa[i] & bb[j]
               for i in range(3) for j in range(3)):
            continue

        six = aa + bb
        assert all(
            not six[i] & six[j]
            for i in range(6) for j in range(i)
        )
        assert sum(s.bit_count() for s in six) <= n
        cases += 1

print("upper counting configurations:", cases)

# Equality pattern for the 9-part count: three disjoint K_{1,2}'s.
R = nx.disjoint_union_all([nx.star_graph(2) for _ in range(3)])
AA = [{1, 2}, {4, 5}, {7, 8}]
BB = [set().union(*(set(R[a]) for a in s)) for s in AA]
assert [len(s) for s in AA + BB] == [2, 2, 2, 1, 1, 1]
assert len(set.union(*(AA + BB))) == 9
print("9-part equality certificate checked")


def ceil_fraction(x):
    return -((-x.numerator) // x.denominator)


def obstruction_parameters(c, q):
    c = Fraction(c)
    q = max(1, q)
    assert 0 <= c < Fraction(1, 9)

    # Ensures (1-9c)k > 3cq.
    x = 3*c*q / (1-9*c)
    k = x.numerator // x.denominator + 1
    m = 2*k + q

    # Core has |V(F)| + 2|E(F)| vertices.
    core = comb(m, k) * (1 + comb(m-k, k))
    gap = k - 3*c*(m+k)
    assert gap > 0

    t = max(1, ceil_fraction(c*core/gap))
    n = core + 3*(m+k)*t

    assert k*t >= c*n
    assert m - 2*k + 2 > q
    return m, k, t, n


for c in [Fraction(0), Fraction(1, 100), Fraction(1, 10),
          Fraction(11, 100), Fraction(111, 1000)]:
    for q in range(1, 8):
        obstruction_parameters(c, q)

print("35 exact rational parameter checks passed")

c = sp.symbols("c", real=True)
eta = (9*c - 1)/30
assert sp.expand(9*c - 15*eta - 1) == (9*c - 1)/2
assert sp.simplify(c - 2*eta - (6*c + 1)/15) == 0
print("upper slack identities checked symbolically")
```

The run completed successfully. Its construction checks reported:
```text
lower: (5, 2, 1) core 40 n 61 delta 2 chi(F) 3
lower: (6, 2, 2) core 105 n 153 delta 4 chi(F) 4
lower: (7, 2, 1) core 231 n 258 delta 2 chi(F) 5
lower: (8, 3, 1) core 616 n 649 delta 3 chi(F) 4
```
All other assertions passed, including \(94{,}376\) Tucker comparability checks.

## Conclusion

We proved that every \(c>1/9\) has the requested property and every \(c<1/9\) fails it. Therefore the exact infimum is
\[
\boxed{\inf c=\frac19}.
\]

Nothing remains to establish the requested infimum; determining whether the infimum itself is attained is not needed for this conclusion.
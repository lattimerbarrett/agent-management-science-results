# agent_1: last reply

\[
\boxed{\displaystyle \frac19}
\]

More precisely:

* for every \(c>1/9\), the required finite triangle-free target exists;
* for every \(c<1/9\), no such target exists.

The value of the property at the endpoint is not needed to determine its infimum.

I give both proofs. The only general theorems used are the degree form of Szemerédi’s regularity lemma and the Borsuk–Ulam theorem. All the consequences specific to this problem are proved below. The Python at the end performs exact, nontrivial checks of the constructions and the finite combinatorial parts of the proof.

## 1. Preliminaries

Write \(N_J(S)=\bigcup_{v\in S}N_J(v)\).

We will repeatedly use the following elementary fact:

> A simple graph has an odd closed walk of length at most five if and only if it contains a \(C_3\) or a \(C_5\).

Indeed, a shortest odd closed subwalk of an odd closed walk is an odd cycle.

Here is another useful observation.

### Extension lemma

Suppose \(I\subseteq V(G)\), both \(I\) and \(N_G(I)\) are independent, and \(G-I\) maps to a triangle-free graph on \(h\) vertices. Then \(G\) maps to a triangle-free graph on at most \(2h+1\) vertices.

**Proof.** Let \(f:G-I\to H\). Replace every vertex \(a\in V(H)\) by two vertices \((a,0),(a,1)\). Put an edge between \((a,b)\) and \((a',b')\) when \(aa'\in E(H)\), except that edges with \(b=b'=1\) are omitted. Add a new vertex adjacent to all the \(1\)-copies.

The resulting graph is triangle-free: triangles not using the new vertex would project to triangles in \(H\), and the new vertex has an independent neighborhood.

Map \(x\in G-I\) to
\[
\bigl(f(x),\mathbf1_{x\in N_G(I)}\bigr),
\]
and map all of \(I\) to the new vertex. This is a homomorphism. ∎

## 2. A regularity support lemma

This is the regularity consequence needed for the upper bound.

### Support lemma

Fix \(0<q<c\). There are constants \(M,n_0\) such that every \(\{C_3,C_5\}\)-free graph \(G\) with
\[
n\ge n_0,\qquad \delta(G)\ge cn
\]
has the following objects:

* disjoint sets \(V_1,\ldots,V_m\), each of size \(L\), where \(m\le M\);
* a graph \(R\) on \([m]\), with \(\delta(R)\ge qm\);
* for every \(v\in V(G)\), a set \(S_v\subseteq[m]\);

satisfying:

1. \(v\) has at least \(qmL\) neighbors in \(\bigcup_{i\in S_v}V_i\);
2. \(S_v\) is independent in \(R\);
3. if \(vw\in E(G)\), then
   \[
   N_R(S_v)\cap N_R(S_w)=\varnothing;
   \]
4. if \(v,x,w\) is a two-edge path in \(G\), then there are no \(R\)-edges between \(S_v\) and \(S_w\).

**Proof.** Choose positive constants
\[
\varepsilon\ll d,\rho\ll c-q.
\]
Apply degree-form regularity. Thus there is an exceptional set \(V_0\), of size at most \(\varepsilon n\), and equal-sized clusters \(V_1,\ldots,V_m\), such that the reduced graph \(R\) consists of \(\varepsilon\)-regular pairs of density at least \(d\), and
\[
\delta(R)\ge(c-d-2\varepsilon)m\ge qm.
\]

Define
\[
S_v=\{i:|N_G(v)\cap V_i|\ge \rho L\}.
\]
The neighbors not counted in these support clusters number at most
\[
|V_0|+\rho mL.
\]
Consequently, by our choice of constants,
\[
\left|N_G(v)\cap\bigcup_{i\in S_v}V_i\right|
 \ge cn-|V_0|-\rho mL\ge qmL.
\]

We verify the remaining assertions. The elementary regular-pair facts used here are:

* two subsets of size at least \(\rho L\) in a regular pair contain an edge;
* given such a subset \(A\) in one cluster of a regular pair, all but \(\varepsilon L\) vertices of the other cluster have many neighbors in \(A\).

These follow immediately from the definition of regularity, since \(\varepsilon\ll d,\rho\). Taking \(n_0\) large lets us avoid any fixed collection of already specified vertices.

If \(ij\in E(R)\) with \(i,j\in S_v\), an edge between the corresponding subsets of \(N_G(v)\) gives a triangle. Thus \(S_v\) is independent.

Suppose \(vw\in E(G)\), and a cluster \(t\) belongs to both \(N_R(S_v)\) and \(N_R(S_w)\). Choose
\[
i\in S_v,\quad j\in S_w,\quad it,jt\in E(R).
\]
Regularity supplies distinct vertices
\[
a\in N_G(v)\cap V_i,\quad b\in V_t,\quad
a'\in N_G(w)\cap V_j
\]
with \(ab,ba'\in E(G)\), avoiding \(v,w\). This also works when \(i=j\). Then
\[
v,a,b,a',w,v
\]
is a \(C_5\), a contradiction.

Finally, suppose \(v,x,w\) is a two-edge path and \(ij\in E(R)\), where \(i\in S_v\) and \(j\in S_w\). An edge
\[
ab,\qquad a\in N_G(v)\cap V_i,\quad b\in N_G(w)\cap V_j,
\]
chosen to avoid \(v,x,w\), gives the \(C_5\)
\[
v,x,w,b,a,v.
\]
This proves the lemma. ∎

## 3. Upper bound: every \(c>1/9\) works

Fix
\[
\frac19<q<c
\]
and apply the support lemma.

Partition the vertices according to their support \(S_v\). There are at most \(2^M\) classes.

Call a support class **small** if its support \(S\) satisfies
\[
|S|<2qm.
\]

### Small classes can be removed and later restored

If \(u,v\) belong to the same small class, each has at least \(qmL\) neighbors in a set of size less than \(2qmL\). Thus \(u,v\) have a common neighbor.

It follows that the class \(I\) is independent: an edge within it would give a triangle.

Moreover, there cannot be a three-edge walk from one vertex of \(I\) to another. Combining that walk with a common neighbor would give an odd closed walk of length five. Therefore \(N_G(I)\) is independent.

The extension lemma consequently permits us to remove all small classes and restore them afterward, at a bounded cost in target size.

Let \(W\) be the set of remaining vertices. Every support occurring in \(W\) has size at least \(2qm\).

### A bounded triangle-free quotient of \(G[W]\)

Refine the support partition on \(W\) by assigning \(v\in W\) the label
\[
\left(
 S_v,\ 
 \{S_u:u\in N_G(v)\cap W\}
\right).
\]
There are boundedly many labels. Let \(Q\) be the quotient graph: two labels are adjacent if some \(G\)-edge joins their classes.

No class contains an edge. Indeed, if \(uv\) were an edge with \(S_u=S_v=S\), property 3 of the support lemma would say
\[
N_R(S)\cap N_R(S)=\varnothing,
\]
impossible because \(S\ne\varnothing\) and \(\delta(R)>0\).

Thus \(G[W]\to Q\). We show that \(Q\) is triangle-free.

Suppose three refined classes form a triangle, with supports \(S_1,S_2,S_3\), and put
\[
U_i=N_R(S_i).
\]
Property 3 gives
\[
U_1,U_2,U_3\quad\text{pairwise disjoint}. \tag{1}
\]

The refinement ensures that, for every pair \(i\ne j\), there is an actual two-edge path in \(G\) whose endpoint supports are \(S_i,S_j\): choose its middle vertex in the third refined class. Property 4 therefore gives
\[
E_R(S_i,S_j)=\varnothing\qquad(i\ne j). \tag{2}
\]
Each \(S_i\) is itself independent.

Also, the \(S_i\) are pairwise disjoint. Otherwise a vertex in \(S_i\cap S_j\) would have an \(R\)-neighbor, which would belong to \(U_i\cap U_j\), contradicting (1).

By (2) and independence,
\[
(S_1\cup S_2\cup S_3)\cap(U_1\cup U_2\cup U_3)=\varnothing.
\]
Hence the six sets
\[
S_1,S_2,S_3,U_1,U_2,U_3
\]
are pairwise disjoint. But
\[
|S_i|\ge2qm,\qquad |U_i|\ge\delta(R)\ge qm.
\]
Consequently
\[
m\ge\sum_{i=1}^3(|S_i|+|U_i|)
  \ge9qm>m,
\]
a contradiction.

So \(Q\) is triangle-free.

There are boundedly many refined classes and boundedly many deleted small classes. Repeated use of the extension lemma produces a triangle-free target of bounded order for \(G\).

Finally, a single target independent of \(G\) is obtained by taking the disjoint union of all triangle-free graphs up to that order. Include also all triangle-free graphs on fewer than \(n_0\) vertices to handle the finitely many small orders.

This proves the required property for every \(c>1/9\).

## 4. Geometric graphs for the lower bound

We need the following finite construction.

### Geometric lemma

For every integer \(t\) and every \(a<1/2\), there are a finite graph \(F\), an integer \(M\), and sets
\[
A_v\subseteq[M]\qquad(v\in V(F))
\]
such that:

1. \(\chi(F)>t\);
2. \(F\) contains neither \(C_3\) nor \(C_5\);
3. \(|A_v|\ge aM\) for every \(v\);
4. if a three-edge walk in \(F\) has endpoints \(u,v\), then
   \[
   A_u\cap A_v=\varnothing.
   \]

**Proof.** Work on a sphere \(S^d\), where \(d\ge\max(1,t)\).

Choose sufficiently small \(\eta>0\), with \(5\eta<2\), and set \(\alpha=2\eta\). We may make \(\eta\) so small that a uniform random point \(y\in S^d\) satisfies
\[
\Pr(\langle x,y\rangle>\alpha)>a
\]
for every unit vector \(x\). This probability is independent of \(x\) and tends to \(1/2\) as \(\alpha\downarrow0\).

Take a finite \(\eta/4\)-net \(P\subseteq S^d\), and define
\[
pq\in E(F)\quad\Longleftrightarrow\quad \|p+q\|<\eta.
\]

We first check its chromatic number. If \(F\) had a \(t\)-coloring, the unions of the open \(\eta/3\)-balls around each color class would cover \(S^d\), and no such union could contain an antipodal pair. Indeed, such a pair would yield same-colored \(p,q\) with
\[
\|p+q\|<2\eta/3<\eta.
\]
This contradicts the Borsuk–Ulam covering theorem: \(S^d\) cannot be covered by at most \(d+1\) open sets, none containing an antipodal pair.

For completeness, that covering formulation follows from Borsuk–Ulam by taking a partition of unity \((\phi_i)\) subordinate to the cover and applying it to the odd map
\[
x\longmapsto(\phi_i(x)-\phi_i(-x))_i,
\]
whose values lie in the hyperplane with coordinate sum zero.

For any odd walk \(p_0,\ldots,p_\ell\) in \(F\), the triangle inequality gives
\[
\|p_0+p_\ell\|<\ell\eta.
\]
An odd closed walk of length three or five would therefore give \(2<5\eta\). Thus \(F\) has neither forbidden cycle.

Choose sufficiently many directions \(y_1,\ldots,y_M\in S^d\) so that, simultaneously for every \(p\in P\),
\[
\bigl|\{j:\langle p,y_j\rangle>\alpha\}\bigr|\ge aM.
\]
Such a finite choice exists by independent sampling and the law of large numbers, since \(P\) is finite. Define
\[
A_p=\{j:\langle p,y_j\rangle>\alpha\}.
\]

If a three-edge walk joins \(p\) to \(q\), then \(\|p+q\|<3\eta\). A direction belonging to both associated sets would give
\[
3\eta>\|p+q\|
 \ge\langle p+q,y_j\rangle
 >2\alpha=4\eta,
\]
a contradiction. ∎

## 5. Lower bound: no \(c<1/9\) works

Fix \(c<1/9\) and an arbitrary finite triangle-free graph \(H\). Put \(h=|V(H)|\).

Choose \(a<1/2\), sufficiently close to \(1/2\), that
\[
c<\frac{a}{3(1+a)}.
\]
Apply the geometric lemma with \(t=h\).

Construct \(G\) as follows.

### The core

For every \(v\in V(F)\), make three vertices
\[
(v,0),(v,1),(v,2).
\]
Join \((u,i)\) to \((v,j)\) exactly when
\[
uv\in E(F),\qquad i\ne j.
\]

### The reservoirs

For each \(i\in\{0,1,2\}\), take:

* an independent set \(Y_i=\{y_{i,1},\ldots,y_{i,M}\}\);
* an independent set \(Z_i\) of size \(L=\lfloor aM\rfloor\).

Put all edges between \(Y_i\) and \(Z_i\). Join \((v,i)\) to \(y_{i,j}\) exactly when \(j\in A_v\). There are no other edges.

We may replicate all reservoir directions as many times as desired before choosing \(L\).

### Minimum degree

Every core vertex has at least \(aM\) neighbors in its reservoir; every \(Y_i\)-vertex has at least \(L\) neighbors; every \(Z_i\)-vertex has \(M\) neighbors. Hence
\[
\delta(G)\ge L.
\]
Also
\[
|V(G)|=3|V(F)|+3M+3L.
\]
Under reservoir replication,
\[
\frac{\delta(G)}{|V(G)|}
 \ \ge\
\frac{\lfloor aM\rfloor}
 {3|V(F)|+3M+3\lfloor aM\rfloor}
 \longrightarrow \frac{a}{3(1+a)}>c.
\]
Thus a sufficiently large finite choice has \(\delta(G)\ge c|V(G)|\).

### No triangles or pentagons

A forbidden cycle entirely in the core would project to an odd closed walk of length three or five in \(F\), which is impossible.

A triangle using a reservoir vertex is also impossible.

For a \(C_5\):

* If it contains a vertex of \(Z_i\), its two neighbors lie in \(Y_i\). A three-edge path between those neighbors, avoiding that \(Z_i\)-vertex, would require an edge between two core vertices having the same second coordinate \(i\), which does not exist.
* If it contains exactly one \(Y\)-vertex and no \(Z\)-vertex, the other four vertices form a three-edge core path whose endpoints have the same second coordinate and have a common reservoir neighbor. Its projection contradicts property 4 of the geometric lemma.
* If it contains two \(Y\)-vertices and no \(Z\)-vertex, their common intervening core vertex forces their indices to agree. The remaining two core vertices then also have that same index and would have to be adjacent, impossible.

These exhaust the possibilities. So \(G\) is \(\{C_3,C_5\}\)-free.

### Why \(G\) cannot map to \(H\)

Define \(H^{[3]}\) to have an edge between vertices joined by a three-edge walk in \(H\). Since \(H\) is triangle-free, \(H^{[3]}\) has no loops.

For every \(uv\in E(F)\), the core contains the walk
\[
(u,0),(v,1),(u,2),(v,0).
\]
Therefore a homomorphism \(G\to H\) would induce a homomorphism
\[
F\longrightarrow H^{[3]}.
\]
But \(H^{[3]}\) is a loopless graph on \(h\) vertices, whereas
\[
\chi(F)>h.
\]
This is impossible.

As \(H\) was arbitrary, no finite triangle-free target works for \(c<1/9\).

Combining the two halves proves the claimed infimum.

## 6. Python verification

The infinite assertions above are established by the proof, not by numerical experiments. The following program nevertheless checks substantive finite instances and proof components:

* constructs an exact rational geometric example;
* checks all required geometric inequalities using `Fraction`;
* verifies the three-walk/disjoint-cap condition;
* constructs and checks a weighted finite lower-bound example;
* checks absence of \(C_3,C_5\) without relying on induced-cycle routines;
* checks the upper-bound set argument on every graph of order at most seven, and its nine-vertex equality configuration;
* checks the triangle-free extension operation on all triangle-free targets of order at most five.

Floating point is used only to propose rational circle points; every property subsequently used is checked exactly.

```python
from fractions import Fraction as Q
import math
import itertools
import networkx as nx


def rational_circle_point(theta, precision=10**7):
    # Rational stereographic parametrization.
    if abs(math.cos(theta / 2)) < 1e-10:
        return (Q(-1), Q(0))
    t = Q(round(math.tan(theta / 2) * precision), precision)
    return ((1-t*t)/(1+t*t), 2*t/(1+t*t))


def dot(x, y):
    return sum(a*b for a, b in zip(x, y))


def no_C3_C5(adj):
    # In a C3,C5-free graph, each distance-one and distance-two
    # neighborhood is independent; the converse also holds.
    n = len(adj)
    masks = [sum(1 << j for j in a) for a in adj]
    for v in range(n):
        one = masks[v]
        two = 0
        for u in adj[v]:
            two |= masks[u]
        two &= ~(1 << v)
        for S in (one, two):
            T = S
            while T:
                b = T & -T
                u = b.bit_length() - 1
                if masks[u] & S:
                    return False
                T -= b
    return True


def example(q=31, multiplicity=100):
    assert q % 2 == 1 and q >= 17
    points = [
        rational_circle_point(2*math.pi*j/q)
        for j in range(q)
    ]
    assert all(dot(p, p) == 1 for p in points)

    step = (q-1)//2
    edges = {
        tuple(sorted((j, (j+step) % q)))
        for j in range(q)
    }
    F = nx.Graph()
    F.add_nodes_from(range(q))
    F.add_edges_from(edges)
    assert nx.is_connected(F)
    assert all(d == 2 for _, d in F.degree())
    assert not nx.is_bipartite(F)  # This F has chromatic number 3.

    eta2 = max(
        2 + 2*dot(points[u], points[v])
        for u, v in edges
    )
    alpha = Q(4, 25)
    assert 25*eta2 < 4             # 5 eta < 2
    assert 9*eta2 < 4*alpha*alpha  # 3 eta < 2 alpha

    caps = [
        {j for j, y in enumerate(points) if dot(x, y) > alpha}
        for x in points
    ]
    r = min(map(len, caps))
    assert r > 0

    for x in F:
        for a in F[x]:
            for b in F[a]:
                for z in F[b]:
                    assert caps[x].isdisjoint(caps[z])

    # Weighted template; independent blow-ups give actual graphs.
    labels = [
        ('X', i, x) for i in range(3) for x in range(q)
    ]
    labels += [
        ('Y', i, j) for i in range(3) for j in range(q)
    ]
    labels += [('Z', i, 0) for i in range(3)]
    idx = {v: i for i, v in enumerate(labels)}
    adj = [set() for _ in labels]

    def edge(a, b):
        u, v = idx[a], idx[b]
        assert u != v
        adj[u].add(v)
        adj[v].add(u)

    for x, y in edges:
        for i in range(3):
            for j in range(3):
                if i != j:
                    edge(('X', i, x), ('X', j, y))

    for i in range(3):
        for x in range(q):
            for j in caps[x]:
                edge(('X', i, x), ('Y', i, j))
        for j in range(q):
            edge(('Y', i, j), ('Z', i, 0))

    assert no_C3_C5(adj)

    # Verify the F -> odd-third-power map.
    for x, y in edges:
        walk = [
            idx[('X', 0, x)], idx[('X', 1, y)],
            idx[('X', 2, x)], idx[('X', 0, y)]
        ]
        assert all(
            b in adj[a] for a, b in zip(walk, walk[1:])
        )

    weights = [
        1 if t == 'X'
        else multiplicity if t == 'Y'
        else r*multiplicity
        for t, _, _ in labels
    ]
    n = sum(weights)
    degrees = [
        sum(weights[j] for j in a) for a in adj
    ]
    delta = min(degrees)
    assert delta >= r*multiplicity

    # A blow-up maps to its template. Thus the odd-cycle checks
    # above also certify the blow-up's absence of C3 and C5.
    print("Exact lower-construction certificate:")
    print("  core cycle length =", q, "; cap minimum =", r)
    print("  template vertices =", len(adj),
          "(all C3/C5 tests passed)")
    print("  blow-up n =", n, "; delta =", delta,
          "; delta/n =", Q(delta, n))


def check_upper_set_lemma():
    graphs = triples = 0

    # All graphs without isolated vertices, up to seven vertices.
    for R in nx.graph_atlas_g():
        m = len(R)
        if not m or min(dict(R.degree()).values()) == 0:
            continue
        adj = [set(R[v]) for v in range(m)]
        graphs += 1
        d = min(map(len, adj))
        sets = []

        for mask in range(1, 1 << m):
            S = {i for i in range(m) if mask >> i & 1}
            if len(S) < 2*d:
                continue
            U = set().union(*(adj[i] for i in S))
            if S & U:  # S must be independent.
                continue
            assert len(U) >= d
            sets.append((S, U))

        for (A, UA), (B, UB), (C, UC) in itertools.combinations(
                sets, 3):
            if UA & UB or UA & UC or UB & UC:
                continue
            if A & UB or A & UC or B & UC:
                continue
            six = [A, B, C, UA, UB, UC]
            assert all(
                not X & Y
                for X, Y in itertools.combinations(six, 2)
            )
            assert m >= sum(map(len, six)) >= 9*d
            triples += 1

    # Nonvacuous equality configuration: three disjoint K_{2,1}'s.
    R = nx.Graph()
    R.add_edges_from([
        (0, 2), (1, 2), (3, 5),
        (4, 5), (6, 8), (7, 8)
    ])
    assert min(dict(R.degree()).values()) == 1
    assert no_C3_C5([set(R[v]) for v in range(9)])

    A, B, C = {0, 1}, {3, 4}, {6, 7}
    UA, UB, UC = {2}, {5}, {8}
    six = [A, B, C, UA, UB, UC]
    for S, U in [(A, UA), (B, UB), (C, UC)]:
        assert set().union(*(set(R[v]) for v in S)) == U
    assert all(
        not X & Y for X, Y in itertools.combinations(six, 2)
    )
    assert sum(map(len, six)) == 9

    print("Upper set lemma:", graphs, "atlas graphs checked;",
          triples, "qualifying triples;",
          "9-vertex equality certificate passed.")


def check_extension():
    count = 0
    for H in nx.graph_atlas_g():
        k = len(H)
        if k > 5 or any(nx.triangles(H).values()):
            continue

        for mask in range(1 << k):
            J = nx.Graph()
            J.add_nodes_from(range(2*k+1))
            for a, b in H.edges():
                for x in range(2):
                    for y in range(2):
                        if not (x == y == 1):
                            J.add_edge(2*a+x, 2*b+y)
            J.add_edges_from(
                (2*k, 2*a+1)
                for a in range(k) if mask >> a & 1
            )
            assert not any(nx.triangles(J).values())
            count += 1

    print("Triangle-free extension:", count,
          "finite checks passed.")


if __name__ == "__main__":
    example()
    check_upper_set_lemma()
    check_extension()
```

I ran this code successfully. Its output was:

```text
Exact lower-construction certificate:
  core cycle length = 31 ; cap minimum = 13
  template vertices = 189 (all C3/C5 tests passed)
  blow-up n = 13293 ; delta = 1304 ; delta/n = 1304/13293
Upper set lemma: 1043 atlas graphs checked; 0 qualifying triples; 9-vertex equality certificate passed.
Triangle-free extension: 595 finite checks passed.
```

The zero qualifying triples in orders at most seven is consistent with the proved requirement \(m\ge9d\); the separate nine-vertex configuration checks equality nonvacuously.

**Conclusion:** both required halves are proved, and the exact requested infimum is \(\boxed{1/9}\). Nothing remains to establish for the stated question.
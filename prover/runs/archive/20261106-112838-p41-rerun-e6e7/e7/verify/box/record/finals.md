# agent_1: last reply

The missing lower-bound construction can be supplied explicitly; my earlier stop was premature. The exact value is
\[
\boxed{b(d,k)=d-2\qquad(d\ge3,\ k\ge1).}
\]

The lower-bound examples below are **1-decomposable**, and the obstruction rules out completion even by complexes with connected positive-dimensional links. Thus the same examples work for every \(k\ge1\).

## 1. Elementary lemmas

Write \(\operatorname{skel}_q\Gamma=\{G\in\Gamma:|G|\le q+1\}\), with \(\operatorname{skel}_{-1}\Gamma=\{\varnothing\}\). Joins are taken on disjoint vertex sets.

### Lemma 1: Basic preservation properties

For a pure \(k\)-decomposable complex:

1. every link and every skeleton is \(k\)-decomposable;
2. coning preserves \(k\)-decomposability;
3. there is an ordering of its facets whose nonempty prefixes are \(k\)-decomposable;
4. if its dimension is positive, its graph is connected.

These follow directly by induction on a decomposition. Here are the details relevant to possible boundary cases.

For a skeleton, let \(\sigma\) be a shedding face. If \(|\sigma|>q+1\), then
\[
\operatorname{skel}_q\Gamma
=\operatorname{skel}_q(\operatorname{del}_\sigma\Gamma).
\]
Otherwise its deletion and link are respectively
\[
\operatorname{skel}_q(\operatorname{del}_\sigma\Gamma),
\qquad
\operatorname{skel}_{q-|\sigma|}(\operatorname{lk}_\sigma\Gamma).
\]
Skeletons of simplices are vertex-decomposable, by successively shedding vertices.

For links, fix a face \(\tau\). If \(\sigma\subseteq\tau\), work inside \(\operatorname{lk}_\sigma\Gamma\). If \(\sigma\cup\tau\) is not a face, then
\[
\operatorname{lk}_\tau\Gamma
=\operatorname{lk}_\tau(\operatorname{del}_\sigma\Gamma).
\]
In the remaining case, \(\sigma\setminus\tau\) is a shedding face of \(\operatorname{lk}_\tau\Gamma\); its deletion is
\(\operatorname{lk}_\tau(\operatorname{del}_\sigma\Gamma)\), and its link is obtained by linking \(\tau\setminus\sigma\) inside \(\operatorname{lk}_\sigma\Gamma\).

For facet prefixes, first order the facets of the deletion, then the facets \(\sigma\cup H\), where \(H\) runs through a suitable prefix ordering of the link. During the second part, \(\sigma\) remains a shedding face.

For connectedness, the deletion is connected inductively. If \(|\sigma|\ge2\), every vertex already belongs to the deletion. If \(\sigma=\{v\}\), the new vertex \(v\) is adjacent to a vertex of its nonempty link.

### Lemma 2: Filling a complete boundary

If \(\Gamma\) is pure \(e\)-dimensional and \(k\)-decomposable, and \(F\) is a missing \((e+1)\)-set with
\[
2^F\setminus\{F\}\subseteq\Gamma,
\]
then \(\Gamma\cup2^F\) is \(k\)-decomposable.

Indeed, take a shedding face \(\sigma\). If \(\sigma\not\subseteq F\), fill \(F\) recursively in the deletion; the link is unchanged. If \(\sigma\subseteq F\), the deletion is unchanged, and the link gains \(F\setminus\sigma\), whose boundary is already present. Zero-dimensional complexes provide the base case.

### Lemma 3: A sufficiently large simplex core

For any complex \(X\) disjoint from \(C\), if \(|C|\ge e+1\), then
\[
\operatorname{skel}_e(2^C*X)
\]
is vertex-decomposable.

Shed vertices of \(X\). Every deletion retains the same simplex core, so remains pure of dimension \(e\); every link has the same core and dimension \(e-1\). The terminal complex is a skeleton of a simplex.

### Lemma 4: A necessary condition for adding a facet

Let \(\Gamma\) be pure \(d\)-dimensional and \(F\) a missing \((d+1)\)-set. Put
\[
R(F,\Gamma)=\{x\in F:F\setminus\{x\}\in\Gamma\}.
\]
If \(\Gamma\cup2^F\) is \(k\)-decomposable, then
\[
R(F,\Gamma)\notin\Gamma. \tag{1}
\]

Suppose instead that \(R=R(F,\Gamma)\in\Gamma\). No existing ridge of \(F\) contains \(R\). Extend \(R\) to an inclusion-maximal face \(\tau\) of \(\Gamma\cap2^F\). Thus \(|\tau|\le d-1\).

By maximality, the two pieces in
\[
\operatorname{lk}_\tau(\Gamma\cup2^F)
=
\operatorname{lk}_\tau\Gamma\ \cup\ 2^{F\setminus\tau}
\]
have disjoint vertex sets. Both have vertices, and this link has positive dimension. It is disconnected, contradicting Lemma 1. This proves (1).

---

## 2. Upper bound: \(b(d,k)\le d-2\)

We prove this by induction, starting in dimension two.

### Dimension two

Choose an original vertex \(a\). Whenever \(au\) and \(uv\) are edges but \(av\) is missing, add the triangle \(auv\). Its new edge \(av\) is a shedding face: deleting it recovers the preceding complex, and its link is the simplex on \(u\). Since \(k\ge1\), this preserves \(k\)-decomposability.

Connectedness of the graph lets us repeat this until \(a\) is adjacent to every vertex.

Now add every missing triangle \(auv\):

- if \(uv\) is missing, it is a shedding edge with link the simplex on \(a\);
- otherwise the entire boundary of \(auv\) is present, so Lemma 2 applies.

The graph is now complete. Every remaining triangle has its entire boundary present, so Lemma 2 finishes the completion. No new vertices were used.

### Inductive step

Let \(\Delta\) have dimension \(d\ge3\), and let
\[
S=\operatorname{skel}_{d-1}\Delta.
\]
Choose a new vertex \(a\). Using a \(k\)-decomposable-prefix ordering of the facets \(H\) of \(S\), add \(a\cup H\). At each step \(a\) is a shedding vertex, with deletion \(\Delta\) and link the corresponding prefix. This reaches
\[
\Delta\cup(a*S).
\]

By induction, complete \(S\) using \(d-3\) further new vertices. Let \(S_j\) be its successive intermediate complexes. Lift every added facet \(H\) to \(a\cup H\).

Every lifted intermediate complex
\[
\Delta\cup(a*S_j) \tag{2}
\]
is \(k\)-decomposable: start with the \(k\)-decomposable cone \(a*S_j\), then add the original facets of \(\Delta\). Their entire boundaries belong to \(S\subseteq S_j\), so Lemma 2 applies.

At the end, all facets containing \(a\) are present. Consequently every missing facet not containing \(a\) has its entire boundary present and can be added by Lemma 2.

The number of new vertices is \(1+(d-3)=d-2\).

---

## 3. An explicit finite complex for the lower bound

Let \(D\) be the two-dimensional complex on \(\{0,\ldots,9\}\) with the following 36 triangles; a string such as \(058\) denotes \(\{0,5,8\}\):
\[
\begin{array}{rrrrrrrrrrrr}
058&137&125&129&289&169&018&038&379&578&029&023\\
016&234&458&136&014&567&459&157&346&026&268&267\\
123&349&468&056&579&149&079&147&247&378&258&356.
\end{array} \tag{3}
\]

It has these three properties:

- **(D1)** its graph is complete;
- **(D2)** every four vertices contain at most two of its triangles;
- **(D3)** it can be reduced to a tree by repeatedly deleting a free edge together with its unique containing triangle.

For complete reproducibility, the Python below checks all three properties exactly. One valid sequence of free edges is
\[
\begin{split}
&04,07,09,18,01,35,69,16,36,46,48,45,59,68,79,39,34,24,\\
&27,26,02,03,06,05,23,13,37,47,14,17,15,12,25,28,56,57.
\end{split}
\]
The remaining tree edges are
\[
08,\ 19,\ 29,\ 38,\ 49,\ 58,\ 67,\ 78,\ 89.
\]

## 4. The lower-bound examples are 1-decomposable

Fix \(d\ge3\). Replace each vertex \(v\) of \(D\) by a disjoint block \(B_v\) of **\(d\) vertices**. Define
\[
\Delta^{(d)}
=
\left\{
G\subseteq\bigcup_v B_v:
|G|\le d+1,\ 
\{v:G\cap B_v\ne\varnothing\}\in D
\right\}. \tag{4}
\]
The set in braces is called the block support of \(G\).

We prove that \(\Delta^{(d)}\) is pure \(d\)-dimensional and 1-decomposable, by reversing the collapses in (D3).

### The expanded tree

Start with the tree remaining after the collapses. Its expansion (4) is vertex-decomposable.

Start from one tree edge: its expansion is the \(d\)-skeleton of a simplex. Attach the remaining tree vertices in leaf order. If the new leaf \(v\) has neighbor \(u\), introduce its clones one at a time. For a new clone \(x\), its deletion is the preceding complex, and its link is
\[
\operatorname{skel}_{d-1}
2^{B_u\cup\{\text{previously introduced clones of }v\}}.
\]
This is vertex-decomposable. There are at least \(d\) link vertices, so the deletion remains pure of dimension \(d\).

### Reversing a free-edge collapse

Suppose the collapse deleted the free edge \(ab\) and triangle \(abc\). In reverse, let
\[
A=B_a,\qquad B=B_b,\qquad C=B_c.
\]
Before this reverse step, the edges \(ac,bc\) are present, but \(ab\) is not.

Order the \(d^2\) pairs in \(A\times B\). Allow these cross-edges one at a time, adding all faces on \(A\cup B\cup C\) whose \(A\)-\(B\) pairs have already been allowed, truncated to dimension \(d\).

When the new cross-edge \(e=\{x,y\}\) is allowed:

- deleting \(e\) gives exactly the preceding complex;
- its link has the form
  \[
  \operatorname{skel}_{d-2}(2^C*X)
  \]
  for a complex \(X\) on the remaining vertices of \(A\cup B\);
- this link is vertex-decomposable by Lemma 3, since \(|C|=d\);
- purity is preserved: every genuinely new face uses vertices from both \(A\) and \(B\), and can be extended to cardinality \(d+1\) using \(C\).

Thus \(e\) is a shedding edge. After all \(d^2\) pairs have been allowed, the reverse collapse is complete.

Reversing all 36 collapses proves that \(\Delta^{(d)}\) is 1-decomposable. It is therefore \(k\)-decomposable for every \(k\ge1\).

---

## 5. Fewer than \(d-2\) new vertices cannot work

Let \(0\le r\le d-3\), and suppose that a completion of \(\Delta^{(d)}\) using \(r\) new vertices were possible.

In the final skeleton there are facets whose old-vertex block support is not a face of \(D\). Let \(F\) be the **first** such added facet, and let \(\Gamma\) be the preceding complex.

Put
\[
S=F\cap V(\Delta^{(d)}),\qquad
P=\{v:S\cap B_v\ne\varnothing\}.
\]
Then
\[
|S|\ge d+1-r\ge4,\qquad P\notin D. \tag{5}
\]

Every face of \(\Gamma\) has old block support in \(D\), by the choice of \(F\).

Consider
\[
R=R(F,\Gamma)=\{x\in F:F\setminus\{x\}\in\Gamma\}.
\]
A vertex in \(R\):

- cannot be new, because removing a new vertex leaves the forbidden old support \(P\);
- must be the sole old vertex of its block in \(F\), for the same reason.

We now show \(|R|\le2\).

- If \(|P|\ge5\), deleting one block still leaves at least four blocks, not a face of the two-dimensional \(D\). Thus \(R=\varnothing\).
- If \(|P|=4\), each member of \(R\) corresponds to a triangle of \(D\) on \(P\). Property (D2) gives \(|R|\le2\).
- If \(|P|=3\), it is a missing triangle. Since \(|S|\ge4\), at most two of its three blocks occur only once. Again \(|R|\le2\).

By (D1), **every set of at most two old vertices is already a face of \(\Delta^{(d)}\)**. Hence
\[
R\in\Delta^{(d)}\subseteq\Gamma.
\]
Lemma 4 now says that \(\Gamma\cup2^F\) cannot be \(k\)-decomposable, a contradiction.

Therefore no completion exists with \(r\le d-3\), proving
\[
b(d,k)\ge d-2.
\]
Together with the upper bound, this proves the asserted equality.

---

## 6. Executable checks

The following is standard-library-only Python. It:

- checks the finite seed (3), including all 210 four-vertex sets and all 36 free-edge collapses;
- constructs and audits the prescribed lower-bound decomposition, checking actual facet/ridge deletion identities and the exact simplex-core form of every new link;
- checks the forbidden-support invariant by exhaustive occupancy enumeration;
- independently recognizes \(k\)-decomposability recursively and checks every intermediate complex produced by the upper-bound algorithm on the stated finite tests.

I executed it successfully. Its output includes:
```text
upper exhaustive: 1642 inputs; 7040 additions
upper sampled: 3 30 inputs; 663 additions
upper sampled: 4 12 inputs; 534 additions
lower 3 3591 facets; 24 vertex steps; 324 edge steps
lower 4 24984 facets; 32 vertex steps; 576 edge steps
lower 5 166950 facets; 40 vertex steps; 900 edge steps
```
The proofs above establish the unbounded statements; these are exact checks of the finite data and instantiated constructions, not substitutes for those proofs.

```python
from itertools import combinations, product
from collections import Counter
from functools import lru_cache
from random import Random

def sk(W, q):
    return {frozenset(c) for c in combinations(sorted(W), q)}

def faces(fs):
    return set().union(
        *(sk(f, q) for f in fs for q in range(len(f) + 1))
    )

def norm(fs):
    fs = set(fs)
    return frozenset(f for f in fs if not any(f < g for g in fs))

# Exact recursive recognizer. A successful return is a decomposition.
@lru_cache(None)
def certificate(fs, k):
    if len(fs) == 1:
        return ()
    if not fs or len({len(f) for f in fs}) != 1:
        return None
    q = len(next(iter(fs)))
    ff = faces(fs)
    candidates = sorted(
        (s for s in ff if 0 < len(s) <= k + 1),
        key=lambda s: (len(s), sorted(s))
    )
    for s in candidates:
        D = norm(f for f in ff if not s <= f)
        if not D or any(len(f) != q for f in D):
            continue
        L = norm(f - s for f in fs if s <= f)
        if (certificate(D, k) is not None and
                certificate(L, k) is not None):
            return s, D, L
    return None

def prefix(fs, k):
    c = certificate(fs, k)
    assert c is not None
    if not c:
        return list(fs)
    s, D, L = c
    return prefix(D, k) + [s | h for h in prefix(L, k)]

# Explicit upper-bound ordering.
def upper(fs, k, A):
    fs = norm(fs)
    d = len(next(iter(fs))) - 1
    V = set().union(*fs)
    assert len(A) == d - 2 and not V.intersection(A)
    present, order = set(fs), []

    def add(f):
        f = frozenset(f)
        if f not in present:
            present.add(f)
            order.append(f)

    if d == 2:
        a = min(V)
        E = set().union(*(sk(f, 2) for f in fs))
        N = {a} | {v for v in V if frozenset((a, v)) in E}
        while N != V:
            e = next(e for e in E if len(e & N) == 1)
            u = next(iter(e & N))
            v = next(iter(e - N))
            add((a, u, v))
            E.add(frozenset((a, v)))
            N.add(v)
        for u, v in combinations(sorted(V - {a}), 2):
            add((a, u, v))
    else:
        a = A[0]
        S = norm(h for f in fs for h in sk(f, d))
        for h in prefix(S, k):
            add(h | {a})
        for h in upper(S, k, A[1:]):
            add(h | {a})

    for f in sk(V | set(A), d + 1):
        add(f)
    return order

def check_upper(fs, k, A):
    fs = norm(fs)
    d = len(next(iter(fs))) - 1
    V = set().union(*fs) | set(A)
    assert certificate(fs, k) is not None
    order = upper(fs, k, A)
    for f in order:
        assert f not in fs
        fs = fs | {f}
        assert certificate(fs, k) is not None
    assert fs == frozenset(sk(V, d + 1))
    return len(order)

T = {frozenset(map(int, s)) for s in """
058 137 125 129 289 169 018 038 379 578 029 023
016 234 458 136 014 567 459 157 346 026 268 267
123 349 468 056 579 149 079 147 247 378 258 356
""".split()}

def seed():
    E = set().union(*(sk(t, 2) for t in T))
    tt = set(T)
    assert E == sk(range(10), 2)
    assert all(sum(t <= Q for t in T) <= 2
               for Q in sk(range(10), 4))

    collapses = []
    while tt:
        choices = [
            (e, t)
            for e in sorted(E, key=lambda e: sorted(e))
            for t in tt
            if e < t and sum(e < u for u in tt) == 1
        ]
        assert choices
        e, t = choices[0]
        E.remove(e)
        tt.remove(t)
        collapses.append((e, t))

    reached = {0}
    while True:
        new = reached | {v for e in E if e & reached for v in e}
        if new == reached:
            break
        reached = new
    assert len(E) == 9 and len(reached) == 10
    assert len(collapses) == 36
    return E, collapses

# Audit an explicit lower-bound decomposition using actual facets.
def check_lower(d):
    tree, collapses = seed()
    B = [set(range(d*v, d*(v+1))) for v in range(10)]
    q = d + 1
    first = min(tree, key=lambda e: sorted(e))
    present = sk(set().union(*(B[v] for v in first)), q)
    ridges = Counter(h for f in present for h in sk(f, d))

    def add(new):
        assert not (new & present)
        for f in new:
            for h in sk(f, d):
                ridges[h] += 1
        present.update(new)

    # Expanded-tree vertex-decomposition certificate.
    reached = set(first)
    vs = es = 0
    while len(reached) < 10:
        u, v = next(
            (next(iter(e & reached)), next(iter(e - reached)))
            for e in tree if len(e & reached) == 1
        )
        old = set()
        for x in sorted(B[v]):
            L = sk(B[u] | old, d)
            new = {h | {x} for h in L}
            assert all(h in ridges for h in L)
            add(new)
            old.add(x)
            vs += 1
        reached.add(v)

    # Reverse collapses: each step has an actual shedding edge.
    for e, t in reversed(collapses):
        a, b = sorted(e)
        c = next(iter(t - e))
        A, Bb, C = B[a], B[b], B[c]
        allowed = set()
        region = sk(A | Bb | C, q)

        for x, y in product(sorted(A), sorted(Bb)):
            edge = frozenset((x, y))
            allowed.add(edge)
            new = {
                f for f in region
                if edge <= f and all(
                    frozenset((aa, bb)) in allowed
                    for aa in f & A for bb in f & Bb
                )
            }
            assert new

            # Every new face omitting an endpoint is already old:
            # deletion of edge is exactly the preceding complex.
            assert all(f - {x} in ridges and f - {y} in ridges
                       for f in new)

            # Exact link = truncated join with simplex core C.
            L = {f - edge for f in new}
            X = {h - C for h in L}
            assert L == {
                h | z for h in X for z in sk(C, d - 1 - len(h))
            }
            assert all(
                g in X for h in X for j in range(len(h) + 1)
                for g in sk(h, j)
            )
            add(new)
            es += 1

    # Independent direct generation of the intended final complex.
    expected = set().union(*(
        sk(set().union(*(B[v] for v in t)), q) for t in T
    ))
    assert present == expected
    print("lower", d, len(present), "facets;",
          vs, "vertex steps;", es, "edge steps")

# Exhaust every relevant block-occupancy pattern.
def check_patterns(d):
    count = 0
    for s in (3, 4):
        for P in sk(range(10), s):
            if s == 3 and P in T:
                continue
            P = sorted(P)
            for counts in product(range(1, d + 1), repeat=s):
                if not 4 <= sum(counts) <= d + 1:
                    continue
                R = {
                    v for v, c in zip(P, counts)
                    if c == 1 and
                    (s == 3 or frozenset(set(P) - {v}) in T)
                }
                assert len(R) <= 2
                count += 1
    print("buffer patterns", d, count)

if __name__ == "__main__":
    count = steps = 0
    ff = list(sk(range(5), 3))
    for mask in range(1, 1 << len(ff)):
        fs = frozenset(f for j, f in enumerate(ff) if mask >> j & 1)
        for k in (1, 2):
            if certificate(fs, k) is not None:
                steps += check_upper(fs, k, [])
                count += 1
    print("upper exhaustive:", count, "inputs;", steps, "additions")

    rng = Random(20260401)
    for d, n, trials in [(3, 6, 40), (4, 6, 12)]:
        ff = sorted(sk(range(n), d + 1), key=lambda f: sorted(f))
        count = steps = 0
        for _ in range(trials):
            fs = frozenset(rng.sample(
                ff, rng.randrange(1, len(ff) + 1)
            ))
            if certificate(fs, 1) is not None:
                steps += check_upper(
                    fs, 1, list(range(n, n + d - 2))
                )
                count += 1
        print("upper sampled:", d, count,
              "inputs;", steps, "additions")

    for d in (3, 4, 5):
        check_lower(d)
    for d in range(3, 11):
        check_patterns(d)
```

# agent_2: last reply

The lower bound is now proved completely.

Use the checked ten-vertex complex \(D\) with complete graph, 36 triangles, at most two triangles on every four vertices, and a free-edge collapse sequence to a tree. Replace every vertex by a block of \(d\) vertices and take the \(d\)-skeleton.

- Reversing the collapses proves this expansion is **1-decomposable**: restore cross-block edges individually; each is a shedding edge whose link has a sufficiently large simplex factor.
- With \(r\le d-3\) additional vertices, consider the first added facet whose old block support is not a face of \(D\). It contains at least four old vertices. At most two vertices can index existing ridges of that facet. Their set is already an original face, contradicting the necessary pure-ridge attachment condition.

Thus \(b(d,k)\ge d-2\) for every \(k\ge1\). Together with the team's completed upper bound,
\[
\boxed{b(d,k)=d-2}.
\]

Independent verification files:
- `workspace/lower_seed_agent2.json`
- `workspace/verify_obstruction_agent2.py`

The latter verifies the seed, all 36 elementary collapses, and obstruction patterns through \(d=12\). Agents 3 and 4 additionally checked actual decomposition certificates in dimensions \(3,4,5\). Nothing remains mathematically; agent 1 is assembling the complete presentation.

# agent_3: last reply

The proof is now complete: \(\boxed{b(d,k)=d-2}\) for every \(d\ge3,\ k\ge1\).

My completed contributions are:

- A constructive upper-bound algorithm, including the zero-buffer two-dimensional base case.
- An explicit ten-vertex lower-bound seed with 36 triangles, together with a checked sequence of 36 free-edge collapses to a tree.
- The dimension-independent lower construction: replace each seed vertex by a \(d\)-vertex simplex and take the \(d\)-skeleton. Reverse-collapse crossing-edge decompositions prove this complex is \(1\)-decomposable.
- The first-forbidden-support argument proving that fewer than \(d-2\) fresh vertices cannot permit completion.

Reproducible code and certificates:
- `workspace/upper_agent3.py`
- `workspace/lower_seed_agent3.json`
- `workspace/lower_verified_agent3.py`

The lower verifier explicitly audited:
\[
\begin{array}{c|r|r|r}
d&\text{facets}&\text{vertex steps}&\text{edge steps}\\\hline
3&3591&24&324\\
4&24984&32&576\\
5&166950&40&900
\end{array}
\]
Every deletion identity and link description was checked. Teammates independently verified both the construction and the obstruction. Nothing remains mathematically; agent_1 is assembling the integrated proof.

# agent_4: last reply

The proof is now complete.

I independently verified the decisive lower construction using clone blocks of size \(d\), including:

- the reverse-collapse edge-decomposition argument;
- the obstruction with every \(r\le d-3\);
- actual intermediate face sets and exact recursive \(1\)-decomposability checks of all edge links for \(d=3,4\).

The executable certificate is `workspace/verify_lower_agent4.py`. Its checked instances have:

| \(d\) | Vertices | Facets | Edge-decomposition steps |
|---|---:|---:|---:|
| 3 | 30 | 3,591 | 324 |
| 4 | 40 | 24,984 | 576 |

Combined with the completed upper-bound proof, this establishes
\[
\boxed{b(d,k)=d-2\qquad(d\ge3,\ k\ge1).}
\]

I posted the complete verification status on Slack; nothing remains mathematically.
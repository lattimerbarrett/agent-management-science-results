# agent_1: last reply

\[
\boxed{F(d)=d-3\qquad(d\ge 8).}
\]

In fact, the supremum is attained by the Boolean lattice \(B_3\). We will prove
\[
\dim(B_3\times Q_d)=d
\]
and, for every finite poset \(P\) of dimension \(t\ge3\),
\[
\dim(P\times Q_d)\le t+d-3.
\]

Some small finite counts enter the proof. The Python at the end computes them from their definitions, using exact arithmetic; it also checks the numerical inequalities used below. No table of Dedekind numbers or of \(\lambda(k)\) is assumed.

## 1. Intersecting families and the lower bound

An inclusion-maximal intersecting family \(\mathcal H\subseteq 2^{[k]}\) is an upset and satisfies
\[
A\in\mathcal H\quad\Longleftrightarrow\quad [k]\setminus A\notin\mathcal H. \tag{1}
\]
Indeed, upward closure follows from maximality. If \(A\notin\mathcal H\), some member of \(\mathcal H\) is disjoint from \(A\), and upward closure then puts \(A^c\) in \(\mathcal H\).

Write \(Q(n)\) for the inclusion poset of the singletons and pairs of \([n]\).

### Lemma 1
If \(n\ge3\) and \(\dim Q(n)\le k\), then \(n\le\lambda(k)\).

**Proof.** Take \(k\) linear extensions realizing \(Q(n)\), repeating extensions if necessary, and restrict them to its singleton elements. These give permutations \(\pi_1,\ldots,\pi_k\) of \([n]\).

For distinct \(v,w\), put
\[
S(v,w)=\{c:v\text{ occurs after }w\text{ in }\pi_c\}.
\]
For three distinct vertices \(v,u,w\), some extension reverses the incomparable pair
\((\{v\},\{u,w\})\). Thus
\[
S(v,u)\cap S(v,w)\ne\varnothing. \tag{2}
\]
This also implies \(S(v,u)\ne\varnothing\). Consequently, for each \(v\), the sets \(S(v,w)\), \(w\ne v\), form an intersecting family. Extend it to a maximal intersecting family \(\mathcal H_v\) on \([k]\).

For \(v\ne w\), these maximal families are different: one contains \(S(v,w)\), and the other contains its complement \(S(w,v)\). Hence \(n\le\lambda(k)\). ∎

Taking \(n=M_d=\lambda(d-1)+1\) gives
\[
\dim Q_d\ge d. \tag{3}
\]

Since \(B_3\) has dimension \(3\), and \(B_3\times Q_d\) contains a copy of \(Q_d\),
\[
F(d)\ge d-3. \tag{4}
\]

The other half of the proof is the matching upper bound.

## 2. Labeled permutation arrays

We need the following concrete device.

A **three-labeled array on \(n\) vertices with \(k\) rows** consists of:

* in every row, a permutation of the vertices;
* in every row, a label in \(\{1,2,3\}\) attached to each vertex.

It must satisfy:

1. For distinct \(v,w\) and every label \(i\), some row puts \(v\) after \(w\) and gives \(v\) label \(i\).
2. For distinct \(v,u,w\), some row puts \(v\) after both \(u,w\).

### Lemma 2
If such an array exists, then, for every \(P\) of dimension \(t\ge3\),
\[
\dim(P\times Q(n))\le t+k-3. \tag{5}
\]

**Proof.** Let \(L_1,\ldots,L_t\) realize \(P\).

For each array row, group the elements \((p,A)\) according to the last vertex of \(A\) in that row. Order the groups in the row’s vertex order. If a group’s vertex has label \(i\), order that group primarily by \(L_i\) on \(p\), breaking ties by any linear extension of inclusion on the sets \(A\) in the group. This is a linear extension of \(P\times Q(n)\).

Add \(t-3\) more extensions, primarily ordered by \(L_4,\ldots,L_t\) on \(P\).

We check that these extensions realize the product. Suppose
\[
(p,A)\not\le(p',B).
\]

If \(A\not\subseteq B\), choose \(v\in A\setminus B\). When \(B\) is a pair, property 2 supplies a row putting \(v\) after both vertices of \(B\). When \(B\) is a singleton, the same follows by adding a third vertex. In either case the group of \(A\) is after the group of \(B\), independently of \(p,p'\).

It remains that \(A\subseteq B\) and \(p\not\le p'\). Choose \(i\) with \(p'<_{L_i}p\). If \(i\ge4\), the corresponding added extension works.

If \(i\le3\), property 1 supplies a row in which \(A,B\) have the same last vertex and that vertex has label \(i\):

* if \(A=\{v\}\subset B=\{v,w\}\), put \(v\) after \(w\);
* if \(A=B=\{v,w\}\), again put \(v\) after \(w\);
* if \(A=B=\{v\}\), property 1 guarantees a row giving \(v\) label \(i\).

Within their common group, \(L_i\) puts \((p',B)\) before \((p,A)\). ∎

Thus it suffices to construct a three-labeled array with \(d\) rows on at least \(\lambda(d-1)+1\) vertices.

## 3. Constructing arrays from intersecting families

Partition the row set into three nonempty groups
\[
[k]=G_1\mathbin{\dot\cup}G_2\mathbin{\dot\cup}G_3.
\]
Call a subset \(A\subseteq[k]\) **permitted** if
\[
\varnothing\ne A\cap G_i\ne G_i\qquad(i=1,2,3). \tag{6}
\]
The permitted sets are closed under complementation.

### Lemma 3
The number of maximal intersecting families of permitted sets is a lower bound for the number of vertices in a three-labeled array with \(k\) rows.

**Proof.** A maximal intersecting family of permitted sets is upward closed among permitted sets and selects exactly one from each complementary pair, by the proof of (1).

Use these families as vertices. List the complementary pairs of permitted sets in a fixed order. In row \(c\), order the vertices lexicographically by their choices from these pairs, preferring the member containing \(c\).

If two families \(\mathcal H,\mathcal K\) first differ on \(\{A,A^c\}\), where \(A\in\mathcal H\), then their comparison signature is exactly
\[
\{c:\mathcal H\text{ is after }\mathcal K\text{ in row }c\}=A. \tag{7}
\]
Give every vertex label \(i\) in rows belonging to \(G_i\).

Every comparison signature meets all three groups, so property 1 holds. The two signatures for comparisons from a fixed vertex belong to its intersecting family, so they intersect; this is property 2. ∎

Here are useful lower bounds for the number in Lemma 3.

### Even number of rows

Let \(k=2r\). Include all permitted sets larger than \(r\), exclude all smaller ones, and independently choose one set from each complementary pair of permitted \(r\)-sets. This gives
\[
2^{L_k}\quad\text{families},\qquad
L_k=\frac12\#\{\text{permitted }r\text{-sets}\}. \tag{8}
\]

### Odd number of rows

Let \(k=2r+1\). Fix a row \(a\), and let \(\mathcal T\) be any collection of permitted \(r\)-sets containing \(a\). Define a family by:

* selecting precisely \(\mathcal T\) at size \(r\);
* selecting an \((r+1)\)-set precisely when its complement is not in \(\mathcal T\);
* selecting all permitted larger sets, and no permitted smaller sets.

Because the members of \(\mathcal T\) intersect, this is a maximal intersecting family. Therefore we obtain
\[
2^{L_k}\quad\text{families},\qquad
L_k=\max_a\#\{\text{permitted }r\text{-sets containing }a\}. \tag{9}
\]

We use balanced group sizes throughout (8)–(9).

## 4. A bound on the number of Boolean upsets

Let \(D(m)\) be the number of upsets—or, equivalently, ideals—of \(2^{[m]}\).

Restricting a maximal intersecting family on \([m+1]\) to the sets avoiding \(m+1\) gives a bijection with intersecting upsets of \(2^{[m]}\). The inverse is specified by (1). In particular,
\[
\lambda(m+1)\le D(m). \tag{10}
\]

We will use the bound
\[
D(m)\le 3^{\binom m{\lfloor m/2\rfloor}}. \tag{11}
\]
For completeness, here is a proof.

There is an ordered symmetric-chain decomposition of \(2^{[m]}\) with this property:

> For every three consecutive elements \(x<y<z\) of a chain, the other middle element of the diamond \([x,z]\) lies on an earlier chain.

Construct it recursively. From an old chain \(C=(x_1,\ldots,x_\ell)\), form
\[
C^+=(x_1,\ldots,x_\ell,x_\ell\cup\{m\}),\qquad
C^-=(x_1\cup\{m\},\ldots,x_{\ell-1}\cup\{m\}),
\]
omitting an empty \(C^-\). Sort by increasing chain length, retaining parent order to break ties.

The diamond property follows inductively. For an internal triple of \(C^+\), use the old alternate middle element; for its final triple, use the corresponding element of \(C^-\). For a triple of \(C^-\), the old alternate element lies in a chain whose length is either smaller or equal; its new chain is consequently earlier. Symmetry ensures that in the equal-length case the alternate element is not the old chain’s top.

Now reveal an upset’s values chain by chain. On the current chain, values not forced by earlier chains form a consecutive segment. That segment has at most two elements: otherwise the diamond property and the already known alternate middle element force one of its extremes. Hence there are at most three possibilities per chain. There are exactly \(\binom m{\lfloor m/2\rfloor}\) symmetric chains, proving (11).

## 5. Enough vertices for every \(d\ge10\)

For balanced group sizes, (8)–(9) give the following exponents:
\[
\begin{array}{c|rrrrrrrrrrr}
d&10&11&12&13&14&15&16&17&18&19&20\\ \hline
L_d&90&164&396&690&1550&2800&6100&11008&23710&42805&90895.
\end{array} \tag{12}
\]
These are just binomial-coefficient sums, computed in the code.

### The cases \(10\le d\le13\)

The exact finite computation below gives
\[
D(7)=2\,414\,682\,040\,998.
\]
An ideal of \(B_{m+1}\) is a comparable pair of ideals of \(B_m\). Consequently
\[
D(m+1)\le\frac{D(m)^2+D(m)}2\le D(m)^2.
\]
The displayed value gives
\[
D(8)<2^{82}.
\]
Thus, for \(10\le d\le13\),
\[
\lambda(d-1)\le D(d-2)<2^{82\cdot2^{d-10}}\le2^{L_d}. \tag{13}
\]
This supplies the required \(\lambda(d-1)+1\) vertices.

### All \(d\ge14\)

We claim
\[
L_d>\frac85\binom{d-2}{\lfloor(d-2)/2\rfloor}. \tag{14}
\]
The values in (12) verify \(14\le d\le20\).

For even \(d\ge18\), put \(s=\lfloor d/3\rfloor\ge6\). A uniformly random \(d/2\)-set misses, or contains, a specified group of size at least \(s\) with probability at most \(2^{-s}\). A union bound gives
\[
L_d\ge \frac12(1-6\cdot2^{-s})\binom d{d/2}.
\]
Dividing by \(\binom{d-2}{(d-2)/2}\), the ratio is at least
\[
\frac{493}{288}>\frac85. \tag{15}
\]

For odd \(d=2r+1\ge21\), condition on a fixed row being selected in an \(r\)-set. Put \(s=\lfloor d/3\rfloor\ge7\). For either group not containing that row, the probabilities of being entirely selected or entirely omitted are at most
\[
2^{-s}\quad\text{and}\quad (11/20)^s,
\]
respectively. For the group containing the fixed row, the probability of being entirely selected is at most \(2^{-(s-1)}\). Therefore
\[
\frac{L_d}{\binom{d-2}{(d-3)/2}}
\ge
\frac{20}{11}\left(1-\frac1{32}-2(11/20)^7\right)
>\frac85. \tag{16}
\]
This proves (14).

Since \(3^5<2^8\), equations (10), (11), and (14) yield
\[
\lambda(d-1)
\le D(d-2)
\le3^{\binom{d-2}{\lfloor(d-2)/2\rfloor}}
<2^{L_d}.
\]
Again Lemma 3 provides enough vertices.

## 6. The cases \(d=8,9\)

These require two small, explicit constructions.

### Eight rows

Let \(T_3\) be the poset of nonempty proper subsets of \([3]\). For group sizes \((2,3,3)\), the number of maximal intersecting families of permitted sets is
\[
D(T_3\times T_3)=783\,558. \tag{17}
\]
Here \(D(R)\) means the number of ideals of \(R\).

To see the equality, name the two rows in the size-two group \(a,b\). An arbitrary upset \(K\) of \(T_3\times T_3\) specifies the permitted members containing \(a\), while the members containing \(b\) are specified by complementarity (1). This is a bijection.

We can concatenate two copies of this construction, giving
\[
2\cdot783\,558=1\,567\,116 \tag{18}
\]
vertices. Here are the details ensuring that the labels still work.

For the first copy use
\[
G_1=\{1,2\},\quad G_2=\{3,4,5\},\quad G_3=\{6,7,8\},
\]
and put \(A=\{1,2,3,6\}\). Thus \(A\) contains \(G_1\) and meets all three groups. For the second copy, permute the groups so that \(A^c\) contains its size-two group and meets its other two groups.

In rows in \(A\), put the first copy after the second; in the other rows reverse these blocks. Retain the internal orders and labels.

For comparisons between copies, the signatures \(A,A^c\) meet every relevant label group. For a triple with one comparison internal to a copy and one external, the signatures intersect because the external signature contains an entire group of that copy. Thus both array properties hold.

The computation below gives
\[
\lambda(7)=1\,422\,564<1\,567\,116.
\]
So eight rows suffice.

### Nine rows

Use three groups of size three. Consider the permitted four-element subsets, and join two when they are disjoint. Any independent set \(\mathcal T\) in this graph gives a maximal intersecting family exactly as in the odd construction above.

It is enough to use the induced graph on those four-sets containing at least one of two specified rows in the first group. This graph has \(63\) vertices. Its number of independent sets is
\[
5\,556\,381\,987\,840. \tag{19}
\]
The exact deletion recurrence computing this appears below.

By (10),
\[
\lambda(8)\le D(7)=2\,414\,682\,040\,998,
\]
so (19) is more than enough.

We have now constructed, for every \(d\ge8\), a three-labeled array with \(d\) rows on at least \(M_d\) vertices. Deleting surplus vertices preserves its properties.

Lemma 2 proves
\[
\dim(P\times Q_d)\le\dim P+d-3.
\]
Together with (4), this proves the answer.

## 7. Exact Python verification

Here is a complete runnable script.

For clarity, the less immediate finite count is \(D(7)\). The script counts monotone maps
\[
B_3\longrightarrow J(B_4),
\]
where \(J(B_4)\) is the \(168\)-element ideal lattice of \(B_4\). Such maps count ideals of \(B_7\), reversing one factor if necessary. After choosing the image of the top and the images of the three atoms, the bottom and the three coatoms can be counted independently. That is precisely the sum in `dedekind7`.

The independent-set calculation uses
\[
I(G)=I(G-v)+I(G-N[v]),
\]
and multiplies over connected components. Thus its output is a count, not a search heuristic.

```python
from functools import lru_cache
from itertools import product
from math import comb, prod
from fractions import Fraction
import numpy as np


# All ideals of B_n, encoded as bit masks.
def ideals(n):
    if n == 0:
        return [0, 1]
    old = ideals(n - 1)
    h = 1 << (n - 1)
    return [
        a | (b << h)
        for a in old for b in old
        if (a & b) == b
    ]


# Count D(7) as monotone maps B_3 -> J(B_4).
def dedekind7():
    m = np.array(ideals(4), dtype=np.int64)
    assert len(m) == 168
    n = len(m)

    index = np.zeros(1 << 16, dtype=np.int64)
    index[m] = np.arange(n)
    le = (m[:, None] & m[None, :]) == m[:, None]
    lower = le.sum(axis=0)
    join = index[m[:, None] | m[None, :]]

    ans = 0
    for top in range(n):
        J = np.flatnonzero(le[:, top])
        M = m[J]

        # interval[x] = number of ideals between x and top.
        interval = le[:, J].sum(axis=1)
        B = interval[join[np.ix_(J, J)]]

        for i in J:
            A = interval[join[i, J]]
            bottom = lower[
                index[m[i] & M[:, None] & M[None, :]]
            ]
            # All intermediate int64 sums are at most 168**6.
            ans += int(
                (B * A[:, None] * A[None, :] * bottom).sum()
            )
    return ans


# lambda(7) = number of intersecting upsets of B_6.
def lambda7():
    I = np.array(ideals(5), dtype=np.uint32)

    def reverse32(x):
        x = ((x >> 1) & 0x55555555) | \
            ((x & 0x55555555) << 1)
        x = ((x >> 2) & 0x33333333) | \
            ((x & 0x33333333) << 2)
        x = ((x >> 4) & 0x0f0f0f0f) | \
            ((x & 0x0f0f0f0f) << 4)
        x = ((x >> 8) & 0x00ff00ff) | \
            ((x & 0x00ff00ff) << 8)
        return (x >> 16) | (x << 16)

    R = reverse32(I)
    ans = D6 = 0
    for a in I:
        comparable = (I & a) == I
        D6 += int(comparable.sum())

        # For the ideal D=(a,b), its complementary upset
        # is intersecting iff D union complement_image(D)
        # is the whole cube; equivalently a | reverse32(b)
        # is all ones.
        ans += int(
            (comparable & ((a | R) == 0xffffffff)).sum()
        )

    assert D6 == 7828354
    return ans


# Ideals of T_3 = B_3 with minimum and maximum deleted.
def proper3_ideals():
    E = list(range(1, 7))
    return [
        m for m in range(64)
        if all(
            not (m >> i & 1) or
            all(
                (a & b) != b or (m >> j & 1)
                for j, b in enumerate(E)
            )
            for i, a in enumerate(E)
        )
    ]


def base8():
    I = proper3_ideals()
    assert len(I) == 18

    # T_3 has three minimal and three maximal elements.
    # Choose images of the minimal elements in J(T_3);
    # independently count the possible maximal images.
    C = [
        [
            sum(((a | b) & z) == (a | b) for z in I)
            for b in I
        ]
        for a in I
    ]
    return sum(
        C[i][j] * C[i][k] * C[j][k]
        for i in range(18)
        for j in range(18)
        for k in range(18)
    )


# Independent sets in the specified 63-vertex graph.
def base9():
    V = [
        x for x in product(range(1, 7), repeat=3)
        if sum(a.bit_count() for a in x) == 4
        and (x[0] & 3)
    ]
    assert len(V) == 63

    adj = [
        sum(
            1 << j
            for j, y in enumerate(V)
            if all((a & b) == 0 for a, b in zip(x, y))
        )
        for x in V
    ]

    @lru_cache(None)
    def count(mask):
        if mask == 0:
            return 1

        # Find a component.
        seen = front = mask & -mask
        while front:
            b = front & -front
            front -= b
            new = adj[b.bit_length() - 1] & mask & ~seen
            seen |= new
            front |= new

        if seen != mask:
            return count(seen) * count(mask ^ seen)

        remaining = mask
        vertex, degree = -1, -1
        while remaining:
            b = remaining & -remaining
            remaining -= b
            v = b.bit_length() - 1
            d = (adj[v] & mask).bit_count()
            if d > degree:
                vertex, degree = v, d

        b = 1 << vertex
        return (
            count(mask ^ b)
            + count(mask & ~(b | adj[vertex]))
        )

    return count((1 << len(V)) - 1)


# Exponents in (8)-(9), for balanced group sizes.
def exponent(d):
    sizes = [d // 3 + (j < d % 3) for j in range(3)]
    r = d // 2

    if d % 2 == 0:
        N = sum(
            prod(comb(a, b) for a, b in zip(sizes, x))
            for x in product(*(range(1, a) for a in sizes))
            if sum(x) == r
        )
        assert N % 2 == 0
        return N // 2

    return max(
        sum(
            prod(
                comb(a - (i == j), b - (i == j))
                for i, (a, b) in enumerate(zip(sizes, x))
            )
            for x in product(*(range(1, a) for a in sizes))
            if sum(x) == r
        )
        for j in range(3)
    )


# Ordered symmetric-chain decomposition from the proof.
def chains(n):
    if n == 0:
        return [[0]]
    out = []
    bit = 1 << (n - 1)
    for C in chains(n - 1):
        out.append(C + [C[-1] | bit])
        if len(C) > 1:
            out.append([x | bit for x in C[:-1]])
    return sorted(out, key=len)  # Stable: parent order breaks ties.


def check_chains(n):
    C = chains(n)
    assert len(C) == comb(n, n // 2)
    owner = {}

    for i, chain in enumerate(C):
        assert (
            chain[0].bit_count() + chain[-1].bit_count() == n
        )
        for x in chain:
            assert x not in owner
            owner[x] = i
        for a, b in zip(chain, chain[1:]):
            assert a & b == a
            assert (a ^ b).bit_count() == 1

    assert len(owner) == 1 << n

    for i, chain in enumerate(C):
        for a, b, c in zip(chain, chain[1:], chain[2:]):
            other = a | (c ^ b)
            assert other != b
            assert owner[other] < i


if __name__ == "__main__":
    D7 = dedekind7()
    lam7 = lambda7()
    N8 = base8()
    N9 = base9()

    assert D7 == 2414682040998
    assert lam7 == 1422564
    assert N8 == 783558
    assert N9 == 5556381987840

    assert 2 * N8 >= lam7 + 1
    assert N9 >= D7 + 1
    assert (D7 * D7 + D7) // 2 < 2**82

    for d in range(10, 14):
        assert exponent(d) >= 82 * 2**(d - 10)

    for d in range(14, 21):
        assert (
            5 * exponent(d)
            > 8 * comb(d - 2, (d - 2) // 2)
        )

    assert Fraction(493, 288) > Fraction(8, 5)
    odd_lower = Fraction(20, 11) * (
        1 - Fraction(1, 32)
        - 2 * Fraction(11, 20)**7
    )
    assert odd_lower > Fraction(8, 5)
    assert 3**5 < 2**8

    for n in range(11):
        check_chains(n)

    # Check the two-block concatenation for d=8.
    groups = [{0, 1}, {2, 3, 4}, {5, 6, 7}]
    A = {0, 1, 2, 5}
    permutation = dict(zip(
        [0, 1, 2, 5, 3, 4, 6, 7],
        [3, 4, 6, 7, 0, 1, 2, 5]
    ))
    other_groups = [
        {permutation[x] for x in g} for g in groups
    ]
    Ac = set(range(8)) - A

    assert all(A & g for g in groups)
    assert any(g <= A for g in groups)
    assert all(Ac & g for g in other_groups)
    assert any(g <= Ac for g in other_groups)

    print("D(7) =", D7)
    print("lambda(7) =", lam7)
    print("d=8, one block =", N8, "; two blocks =", 2*N8)
    print("d=9 construction =", N9)
    print(
        "Exponents d=10,...,20:",
        [exponent(d) for d in range(10, 21)]
    )
    print("All checks passed.")
```

Its output is:
```text
D(7) = 2414682040998
lambda(7) = 1422564
d=8, one block = 783558 ; two blocks = 1567116
d=9 construction = 5556381987840
Exponents d=10,...,20: [90, 164, 396, 690, 1550, 2800, 6100, 11008, 23710, 42805, 90895]
All checks passed.
```

Thus both required halves are proved: the lower bound \(d-3\), attained at \(P=B_3\), and the universal upper bound \(d-3\). Nothing remains unresolved.
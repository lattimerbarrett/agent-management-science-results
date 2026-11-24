# agent_1: last reply

\[
\boxed{F(d)=d-3\qquad(d\ge8).}
\]

I give a proof with finite computational certificates. The Python below was executed: all its assertions passed. In particular, it **computes**, rather than assumes, the three enumeration results used in the proof.

Write \(Q(N)\) for the inclusion poset of the singletons and pairs of \([N]\).

## 1. The lower bound

We first prove the implication
\[
\dim Q(N)\le r\quad\Longrightarrow\quad N\le\lambda(r)
\qquad(N\ge3).                                      \tag{1}
\]

Suppose \(L_1,\dots,L_r\) realize \(Q(N)\), and restrict them to its singletons, obtaining permutations \(\pi_1,\dots,\pi_r\) of \([N]\).

For any distinct \(a,b,c\), some extension puts \(\{b,c\}\) before \(\{a\}\). Consequently, some \(\pi_i\) puts \(a\) after both \(b,c\). Call this the **three-suitable property**.

For \(a\ne b\), put
\[
S(a,b)=\{i\in[r]:a\text{ is after }b\text{ in }\pi_i\}.
\]
For fixed \(a\), the family
\[
\mathcal H_a=\{S(a,b):b\ne a\}
\]
is intersecting, by the three-suitable property. Extend it to a maximal intersecting family \(\mathcal F_a\) on \([r]\). If \(a\ne b\), then
\[
S(a,b)\cap S(b,a)=\varnothing,
\]
so \(\mathcal F_a\ne\mathcal F_b\). This proves (1).

In particular, for
\[
N=\lambda(d-1)+1
\]
we have
\[
\dim Q(N)\ge d.                                      \tag{2}
\]

Taking any three-dimensional poset \(P\), its product with \(Q(N)\) contains a copy of \(Q(N)\). Hence
\[
F(d)\ge d-3.                                         \tag{3}
\]

The rest of the proof establishes the matching upper bound.

---

## 2. An upper-bound criterion

We will construct \(d\) permutations of \([N]\), together with maps
\[
c_a:[d]\longrightarrow[3]\qquad(a\in[N]),
\]
having these two properties:

* **Three-suitability:** each element of each triple is last in some permutation.
* **Local coverage:** for every \(a\ne b\) and every \(j\in[3]\), some \(i\) satisfies
  \[
  a\text{ is after }b\text{ in }\pi_i,\qquad c_a(i)=j. \tag{4}
  \]

These properties imply
\[
\dim([m]^3\times Q(N))\le d\qquad(m\ge2).             \tag{5}
\]

Here and below, \([m]\) in a product denotes a chain. To prove (5), let \(r_i(a)\) be the rank of \(a\) in \(\pi_i\). For a singleton \(A=\{a\}\), set \(t_i(A)=a\); for a pair \(A=\{a,b\}\), let \(t_i(A)\) be its later endpoint in \(\pi_i\). Define
\[
f_i(x,A)=r_i(t_i(A))+
 \frac{x_{c_{t_i(A)}(i)}}{m+1},
 \qquad x\in[m]^3.                                  \tag{6}
\]

These maps are order-preserving. Indeed, if \(A\subseteq B\), their integer parts either increase, or agree and use the same coordinate of \(x\).

They also reflect the product order:

* Three-suitability, including its consequence that both orders of every pair occur, shows that
  \[
  A\nsubseteq B\ \Longrightarrow\
  r_i(t_i(A))>r_i(t_i(B))\text{ for some }i.
  \]
* If \(A\subseteq B\) but \(x_j>y_j\), local coverage supplies an \(i\) for which the integer parts in (6) agree and the fractional parts use coordinate \(j\). For a strict incidence, use (4) at its singleton endpoint. For equal singletons or equal pairs, use either an auxiliary vertex or the two endpoints.

Thus (6) is an order embedding into a product of \(d\) chains, proving (5).

Now let \(p=\dim P\ge3\). A realizer embeds \(P\) into \([m]^p\) for some \(m\). Using (5) on three coordinates and keeping the other \(p-3\) coordinates gives
\[
\dim(P\times Q(N))\le p-3+d.                         \tag{7}
\]
Therefore our task is to construct permutations satisfying the two properties for at least \(\lambda(d-1)+1\) vertices.

---

## 3. A tree construction

The following elementary device supplies the permutations.

Consider a finite binary tree. Label each internal node by a subset \(A\subseteq[d]\). At this node:

* coordinate \(i\in A\) orders the left subtree before the right subtree;
* coordinate \(i\notin A\) orders the right subtree before the left subtree.

This recursively defines \(d\) permutations of the leaves.

For a leaf \(v\), record \(A\) when its path takes the right branch, and \(A^c\) when it takes the left branch. Denote the resulting family by \(\mathcal H_v\).

**Tree lemma.** Suppose, for every leaf \(v\),

1. \(\mathcal H_v\) is intersecting;
2. there is a partition of \([d]\) into three classes such that every member of \(\mathcal H_v\) meets all three classes.

Then the leaf permutations are three-suitable and satisfy local coverage.

**Proof.** For two leaves, the coordinates putting \(v\) after the other leaf are exactly the recorded set at their first separating node. Condition 2 therefore gives local coverage.

For a triple, consider its first separating node. If the designated leaf is alone on one side, its recorded set makes it last in some coordinate. Otherwise, intersect its recorded set at this node with its recorded set where it separates from the remaining leaf. Condition 1 makes this intersection nonempty. ∎

Here is a useful way to obtain such trees. A maximal intersecting family \(\mathcal F\) is upward closed and contains exactly one of \(A,A^c\), for every \(A\). Given a collection of distinct maximal intersecting families, query their memberships in complement pairs, suppressing queries that do not split the current collection. The leaves are the families, and every recorded path set belongs to its leaf family.

Consequently:

> If a collection of maximal intersecting families agree on all subsets except those that split a fixed three-part partition, its members give the required permutations.

A set **splits** a partition when it meets each class and so does its complement.

---

## 4. General constructions with many leaves

Partition \([d]\) as evenly as possible into three classes, placing point \(1\) in a smallest class. Put \(k=\lfloor d/2\rfloor\), and let
\[
m(d)=\#\{A\subseteq[d]: |A|=k,\ 1\in A,\
                    A\text{ splits the partition}\}.               \tag{8}
\]

There is a construction with \(2^{m(d)}\) leaves.

### Even \(d=2k\)

Include all sets of size greater than \(k\), exclude all sets of size less than \(k\), and choose one member of each complementary pair of \(k\)-sets. These choices always give a maximal intersecting family.

Vary the choices on the splitting complement pairs, and fix all other choices. There are \(2^{m(d)}\) families, and the preceding tree construction applies.

### Odd \(d=2k+1\)

Let \(\mathcal J\) be any intersecting collection of splitting \(k\)-sets. Define
\[
\mathcal F_{\mathcal J}
=\mathcal J
 \cup\{A:|A|=k+1,\ A^c\notin\mathcal J\}
 \cup\{A:|A|\ge k+2\}.                               \tag{9}
\]
This is an upward-closed, self-complementary, intersecting family, hence maximal intersecting.

Taking arbitrary subcollections of the splitting \(k\)-sets containing point \(1\) gives \(2^{m(d)}\) families.

More generally, for odd \(d\), we may use **all independent sets of the disjointness graph on splitting \(k\)-sets** in (9). We use this improvement twice below.

---

## 5. The finite small cases

Let \(D(n)\) denote the number of antichains of subsets of \([n]\), equivalently the number of upward-closed families.

We need the following computed values:
\[
\begin{aligned}
\lambda(7)&=1\,422\,564,\\
\lambda(8)&=229\,809\,982\,112,\\
D(7)&=2\,414\,682\,040\,998.                          \tag{10}
\end{aligned}
\]

For completeness, the relation used to compute the first two values is
\[
\lambda(n+1)
=\#\{\text{intersecting upward-closed families on }[n]\}.             \tag{11}
\]
Indeed, if \(\mathcal H\) is such a family, the slices of the corresponding maximal intersecting family on \([n+1]\) are
\[
\mathcal H,\qquad
\mathcal H^*=\{A\subseteq[n]:A^c\notin\mathcal H\}.
\]
The condition \(\mathcal H\subseteq\mathcal H^*\) is exactly intersectingness. Minimal members identify upward-closed intersecting families with intersecting antichains.

### \(d=8\)

Use the 35 complement pairs of four-element subsets of \([8]\). Any choices from distinct pairs are automatically intersecting.

There are 280 partitions of \([8]\) into classes of sizes \(2,3,3\). We construct a binary tree by querying the 35 pairs in the order specified in the code. At a node, retain the partitions in which every recorded path set meets all three classes. Split when both answers leave a nonempty collection; otherwise skip the query.

Every leaf therefore satisfies the tree lemma. The exact recurrence in the code gives
\[
1\,932\,672>\lambda(7)+1                              \tag{12}
\]
leaves.

### \(d=9\)

Partition into three classes of size three. A splitting four-set has class sizes \(2,1,1\). Divide these sets into three parts according to the doubled class; each part has 27 members.

The disjointness graph between the first two parts consists of nine six-cycles. Choose one vertex \(z\) in the third part. It has four neighbors in four different cycles.

A six-cycle has 18 independent sets, and a five-vertex path has 13. Thus the number of independent sets using either no third-part vertex, or exactly the fixed vertex \(z\), is
\[
18^9+13^4\,18^5
=252\,327\,242\,016
>\lambda(8)+1.                                       \tag{13}
\]
Apply (9).

### \(10\le d\le19\)

We use
\[
D(n+1)\le D(n)^2,                                    \tag{14}
\]
which follows by taking the two slices of an upward-closed family. Also, (11) gives \(\lambda(n+1)\le D(n)\).

For \(d=10,12,\dots,19\), the code verifies exactly
\[
2^{m(d)}>
D(7)^{\,2^{d-9}}+1
\ge\lambda(d-1)+1.                                   \tag{15}
\]

For \(d=11\), use classes of sizes \(3,4,4\). There are 164 splitting five-sets containing point \(1\), and 116 containing point \(2\) but not point \(1\), where these points lie in the class of size three. Each collection is intersecting. Each member of the second collection is disjoint from at most six members of the first.

The number of independent sets in their disjointness graph is therefore at least
\[
2^{164}(1+2^{-6})^{116}
>D(7)^4+1
\ge\lambda(10)+1.                                    \tag{16}
\]
Again use (9). All inequalities here are checked with integers or exact fractions.

---

## 6. An effective antichain bound for the remaining cases

Here is the bound used to finish the proof. Its derivation is included so that no asymptotic enumeration theorem is needed.

Put
\[
w=\binom n{\lfloor n/2\rfloor},\qquad
L=2n+2,\qquad N=2^n-L,
\]
and
\[
\alpha=\lfloor n/2\rfloor+1,\qquad
\beta=\binom{\lceil n/2\rceil+1}{2}.
\]
Define, for \(x\ge1\),
\[
\delta_n(x)=\max\left\{
 \alpha(x-1),\
 2\beta(1-2/x),\
 \beta(x-3)
\right\}.                                           \tag{17}
\]
Let \(\rho(t)>1\) be the solution of
\[
\rho(t)^t(\rho(t)-1)=1.
\]
Then
\[
\boxed{\displaystyle
\log_2D(n)\le
L+w\left(1+\int_1^{N/w}
                \log_2\rho(\delta_n(x))\,dx\right).}   \tag{18}
\]

### Proof of (18)

Remove the bottom two and top two levels of the Boolean lattice, leaving \(N\) vertices. Let \(G\) be their comparability graph.

Use a symmetric chain decomposition, randomly permuted by a uniform permutation of the ground set. There are \(w\) chains. For comparable sets of ranks \(a<b\), the probability that they occur in the same chain is
\[
\frac1{\binom{\max(b,n-a)}{b-a}}.                     \tag{19}
\]
This follows by counting chains meeting both ranks and using transitivity of the symmetric group on comparable pairs of fixed ranks.

For vertices of \(G\), (19) is at most \(1/\alpha\); when the rank difference is at least two, it is at most \(1/\beta\).

Let \(U\) be any \(u\)-vertex induced subgraph. If the chains contain \(\ell_1,\dots,\ell_w\) members of \(U\), then
\[
\sum_i\binom{\ell_i}{2}
 \ge\frac12(u^2/w-u).
\]
There are at least \(u-2w\) within-chain pairs whose rank difference is at least two. Another lower bound for their number is
\[
\frac12(u^2/w-3u),
\]
obtained by subtracting at most \(u\) consecutive-rank pairs.

Taking expectations and then average degrees shows that \(U\) has a vertex of degree at least
\[
\delta_n(u/w).                                      \tag{20}
\]

Now count independent sets by branching on such a vertex:
\[
I(U)=I(U-v)+I(U-N[v]).
\]
For \(u\le w\), use \(I(U)\le2^u\). For \(u>w\), an inductive upper bound is
\[
2^w\prod_{j=w+1}^{u}\rho(\delta_n(j/w)).
\]
To verify the induction, note that these successive factors are nonincreasing, and use
\[
\rho(t)^{-1}+\rho(t)^{-t-1}=1.
\]
Taking logarithms and bounding the decreasing right-endpoint sum by its integral gives the parenthesized expression in (18). Finally, allow arbitrary membership on the \(L\) removed vertices, multiplying by at most \(2^L\). ∎

### The finite interval \(18\le n\le99\)

The program evaluates a rigorous upper bound for the integral in (18), using:

* a left Riemann sum of mesh \(1/1024\);
* degree bounds rounded downward to multiples of \(1/16\);
* certified upper bounds on \(\log_2\rho(t)\).

Each root bound \(q\) is certified by
\[
2^{qt}(2^q-1)\ge1.
\]
Sage's outward-rounded interval arithmetic verifies this inequality. The final comparisons are between exact rational numbers.

For every \(18\le n\le99\), the result is
\[
\log_2D(n)<m(n+2).                                   \tag{21}
\]
The smallest certified normalized margin is greater than \(0.0392\), at \(n=19\).

Thus the general construction works for \(20\le d\le101\).

### All \(n\ge100\)

Let \(W\) be the inverse of \(z\mapsto ze^z\). From
\[
e^{t\log\rho(t)}(e^{\log\rho(t)}-1)=1
\]
and \(e^x-1\ge x\), we obtain
\[
\log\rho(t)\le W(t)/t.
\]
Also,
\[
\int_0^T\frac{W(t)}t\,dt
=W(T)+\tfrac12W(T)^2.
\]

Use the first term of (17) up to \(x=4\), and the third thereafter. Since
\[
\alpha\ge n/2,\quad \beta\ge n^2/8,\quad
N/w\le n+1,
\]
the integral in (18) is at most
\[
\frac{2}{n\log2}
 \left(\log(3n)+\frac{\log^2(3n)}2\right)
+
\frac{8}{n^2\log2}
 \left(3\log n+\frac{9\log^2n}{2}\right).              \tag{22}
\]
Both terms decrease for \(n\ge100\). At \(100\), their sum is less than \(0.77\); furthermore \(L/w<0.001\). Thus
\[
\log_2D(n)<1.771w\qquad(n\ge100).                    \tag{23}
\]

On the other hand, before imposing the splitting conditions, the number \(m_0\) of \(k\)-sets containing point \(1\) satisfies
\[
m_0/w\ge2-\frac4{d+1},\qquad d=n+2.
\]
Conditioning on membership of point \(1\), a union bound over the five possible failures to split gives
\[
m(d)\ge m_0\left(1-5(3/5)^{\lfloor d/3\rfloor-1}\right).
\]
For \(d\ge102\), this is greater than \(1.9w\). Together with (23),
\[
2^{m(d)}>D(d-2)\ge\lambda(d-1).
\]
Since these are integers, the construction has at least \(\lambda(d-1)+1\) leaves.

This finishes the required constructions for every \(d\ge8\).

---

## 7. Python verification

This is self-contained Python using Sage only for **certified interval arithmetic**. The enumerations and all combinatorial counts use ordinary exact integer arithmetic.

```python
from functools import lru_cache
from itertools import combinations, product
from math import comb
from fractions import Fraction
import gc

# Count antichains. With intersecting=True, also prohibit disjoint members.
# Vertices are subsets, and adj[i] is the CLOSED conflict neighborhood.
def count_families(n, intersecting):
    vals = list(range(1 if intersecting else 0, 1 << n))
    adj = [
        sum(1 << i for i, b in enumerate(vals)
            if (a & b) in (a, b)
            or (intersecting and (a & b) == 0))
        for a in vals
    ]

    @lru_cache(8_000_000)
    def rec(mask):
        if not mask:
            return 1

        m = mask
        isolated = 0
        best = -1
        vertex = None
        while m:
            bit = m & -m
            m -= bit
            i = bit.bit_length() - 1
            degree = (adj[i] & mask).bit_count()
            if degree == 1:
                isolated |= bit
            if degree > best:
                best, vertex = degree, i

        if isolated:
            return (1 << isolated.bit_count()) * rec(mask & ~isolated)

        # A component factorization is an exact optimization.
        if best <= 6:
            component = 0
            boundary = mask & -mask
            while boundary:
                component |= boundary
                neighbors = 0
                m = boundary
                while m:
                    bit = m & -m
                    m -= bit
                    neighbors |= adj[bit.bit_length() - 1]
                boundary = neighbors & mask & ~component
            if component != mask:
                return rec(component) * rec(mask ^ component)

        return (rec(mask & ~(1 << vertex))
                + rec(mask & ~adj[vertex]))

    answer = rec((1 << len(vals)) - 1)
    rec.cache_clear()
    gc.collect()
    return answer


def groups_of(sizes):
    ans = []
    offset = 0
    for s in sizes:
        ans.append(((1 << s) - 1) << offset)
        offset += s
    return ans


def split(A, groups):
    return all((A & G) and (G & ~A) for G in groups)


# Inclusion-exclusion evaluates (8), without enumerating 2^d subsets.
def mvalue(d):
    sizes = sorted(d // 3 + (j < d % 3) for j in range(3))
    groups = groups_of(sizes)
    answer = 0

    for choices in product((-1, 0, 1), repeat=3):
        inc, exc, sign = 1, 0, 1  # point 0 must be included
        for G, choice in zip(groups, choices):
            if choice == 0:       # prohibit G being entirely included
                inc |= G
                sign = -sign
            elif choice == 1:     # prohibit G being entirely excluded
                exc |= G
                sign = -sign

        if inc & exc:
            continue
        k = d // 2 - inc.bit_count()
        remaining = d - (inc | exc).bit_count()
        if 0 <= k <= remaining:
            answer += sign * comb(remaining, k)
    return answer


def eight_certificate():
    full = 255
    partitions = []
    for pair in combinations(range(8), 2):
        A = sum(1 << i for i in pair)
        rest = [i for i in range(8) if not (A >> i) & 1]
        for triple in combinations(rest, 3):
            B = sum(1 << i for i in triple)
            C = full ^ A ^ B
            if B < C:
                partitions.append((A, B, C))
    assert len(partitions) == 280

    # One representative of every complementary pair of four-sets.
    queries = [
        209,101,39,169,53,89,165,77,177,83,147,141,
        27,23,51,113,225,105,149,163,57,15,153,71,
        43,99,85,201,195,197,29,75,45,135,139
    ]
    assert len(set(queries)) == 35
    assert all(A & 1 and A.bit_count() == 4 for A in queries)

    def cover(A):
        return sum(
            1 << i for i, partition in enumerate(partitions)
            if all(A & G for G in partition)
        )

    masks = [(cover(A), cover(full ^ A)) for A in queries]

    @lru_cache(None)
    def leaves(S, j):
        assert S
        if j == len(masks):
            return 1
        p, q = masks[j]
        left, right = S & p, S & q
        if not left or not right:
            return leaves(S, j + 1)
        return leaves(left, j + 1) + leaves(right, j + 1)

    answer = leaves((1 << len(partitions)) - 1, 0)
    assert answer == 1_932_672
    return answer


def nine_certificate():
    groups = groups_of([3, 3, 3])
    sets = [
        sum(1 << i for i in C)
        for C in combinations(range(9), 4)
    ]
    parts = [
        [A for A in sets
         if split(A, groups) and (A & groups[j]).bit_count() == 2]
        for j in range(3)
    ]
    assert list(map(len, parts)) == [27, 27, 27]

    vertices = parts[0] + parts[1]
    adj = [
        {j for j, B in enumerate(vertices) if not (A & B)}
        for A in vertices
    ]

    remaining = set(range(54))
    components = []
    while remaining:
        C = {next(iter(remaining))}
        while True:
            D = C | set().union(*(adj[i] for i in C))
            if D == C:
                break
            C = D
        components.append(C)
        remaining -= C

    assert len(components) == 9
    assert all(
        len(C) == 6 and all(len(adj[i]) == 2 for i in C)
        for C in components
    )

    z = parts[2][0]
    neighbors = {i for i, A in enumerate(vertices) if not (A & z)}
    assert len(neighbors) == 4
    assert sorted(len(C & neighbors) for C in components) == [0]*5+[1]*4

    def independent_count(n, edges):
        return sum(
            all(not ((mask >> a) & 1 and (mask >> b) & 1)
                for a, b in edges)
            for mask in range(1 << n)
        )

    assert independent_count(6, {(i, (i+1) % 6) for i in range(6)}) == 18
    assert independent_count(5, {(i, i+1) for i in range(4)}) == 13

    return 18**9 + 13**4 * 18**5


def eleven_certificate():
    groups = groups_of([3, 4, 4])
    sets = [
        sum(1 << i for i in C)
        for C in combinations(range(11), 5)
    ]
    valid = [A for A in sets if split(A, groups)]
    A = [s for s in valid if s & 1]
    B = [s for s in valid if not (s & 1) and s & 2]

    assert len(A) == 164
    assert len(B) == 116
    assert max(sum(not (a & b) for a in A) for b in B) <= 6
    return Fraction(2**164 * 65**116, 64**116)


def finite_container_checks():
    from sage.all import RealIntervalField

    RF = RealIntervalField(100)
    denominator = 1 << 16

    # Input D16 represents the degree bound D16/16.
    # Return h certifying log_2 rho(D16/16) <= h/denominator.
    @lru_cache(None)
    def root_log_upper(D16):
        if D16 == 0:
            return denominator

        D = RF(D16) / 16
        lo, hi = 0, denominator
        while hi - lo > 1:
            mid = (lo + hi) // 2
            q = RF(mid) / denominator
            value = RF(2)**(q * D) * (RF(2)**q - 1)
            if value.lower() >= 1:
                hi = mid
            else:
                lo = mid

        q = RF(hi) / denominator
        assert (RF(2)**(q * D) * (RF(2)**q - 1)).lower() >= 1
        return hi

    mesh_denominator = 1024
    margins = []

    for n in range(18, 100):
        w = comb(n, n // 2)
        N = (1 << n) - 2*n - 2
        alpha = n // 2 + 1
        beta = comb((n + 1) // 2 + 1, 2)
        B = mesh_denominator

        bins = (B*(N-w) + w-1) // w
        total = 0
        for j in range(bins):
            # x = 1+j/B. Round delta_n(x) DOWN to multiples of 1/16.
            a = 16 * alpha * j // B
            b = 32 * beta * (j-B) // (B+j)
            c = 16 * beta * (j-2*B) // B
            total += root_log_upper(max(a, b, c, 0))

        upper = (
            Fraction(2*n + 2 + w)
            + Fraction(w * total, B * denominator)
        )
        m = mvalue(n + 2)
        assert m > upper, (n, m, upper)
        margins.append((n, Fraction(m, w) - upper/w))

    # Constants in the proof for n >= 100.
    assert RF(2).log() > RF(69)/100
    assert RF(100).log() < RF(461)/100
    assert RF(300).log() < RF(571)/100

    bound = Fraction(2, 69) * (
        Fraction(571, 100) + Fraction(571, 100)**2 / 2
    )
    bound += Fraction(8, 6900) * (
        3*Fraction(461, 100)
        + Fraction(9, 2)*Fraction(461, 100)**2
    )
    assert bound < Fraction(77, 100)
    assert Fraction(2*101**2, 2**100) < Fraction(1, 1000)
    assert (
        (2-Fraction(4, 103)) * (1-5*Fraction(3, 5)**33)
        > Fraction(19, 10)
    )

    worst = min(margins, key=lambda item: item[1])
    print("Container checks passed; smallest normalized margin:",
          worst[0], float(worst[1]))


def main():
    lambda7 = count_families(6, True)
    lambda8 = count_families(7, True)
    D7 = count_families(7, False)

    assert (lambda7, lambda8, D7) == (
        1_422_564, 229_809_982_112, 2_414_682_040_998
    )
    print("lambda(7), lambda(8), D(7):", lambda7, lambda8, D7)

    C8 = eight_certificate()
    C9 = nine_certificate()
    C11 = eleven_certificate()
    assert C8 > lambda7 + 1
    assert C9 > lambda8 + 1

    for n in range(8, 18):
        upper = D7 ** (1 << (n-7))
        if n == 9:
            assert C11 > upper + 1
        else:
            assert 2**mvalue(n+2) > upper + 1

    print("All small-d constructions passed.")
    finite_container_checks()
    print("All computational certificates passed.")


if __name__ == "__main__":
    main()
```

## 8. Conclusion

The constructions establish (5) with
\[
N=\lambda(d-1)+1
\]
for every \(d\ge8\). Therefore (7) gives
\[
\dim(P\times Q_d)-\dim P\le d-3
\]
for every admissible \(P\). The reverse inequality was proved in (3).

Thus
\[
\boxed{F(d)=d-3\quad\text{for every integer }d\ge8.}
\]

In fact, the supremum is attained: for every three-dimensional finite poset \(P\),
\[
\dim(P\times Q_d)=d.
\]
**This proves the requested result completely; no cases remain.**
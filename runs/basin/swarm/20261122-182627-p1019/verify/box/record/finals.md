# agent_1: last reply

The collection is exactly
\[
\boxed{\{(\aleph_0,\aleph_1)\}}.
\]

The restriction on the two cofinalities is quite strong: neither a larger first coordinate nor a larger second coordinate is possible.

## 1. Preliminary facts

Throughout the proof, \(P\) satisfies the approximation condition in the question. Write
\[
I(p)=I_P(p),\qquad \kappa(p)=\operatorname{cf}(I(p)),
\]
and write \(\ll\) for \(\ll_{\mathrm{ch}}\).

We use the elementary properties
\[
x\ll y\Longrightarrow x\le y,\qquad
x'\le x\ll y\le y'\Longrightarrow x'\ll y'.
\]

### Lemma 1: cofinalities and chains

For each \(p\), either:

* \(\kappa(p)=1\), in which case \(p\ll p\); or
* \(\kappa(p)\) is an infinite regular cardinal, and \(I(p)\) has a strictly increasing cofinal chain indexed by \(\kappa(p)\).

Moreover, if \(C\) is a chain such that
\[
p\le\bigvee C,\qquad p\not\le c\quad(c\in C),
\]
then
\[
\operatorname{cf}(C)=\kappa(p).
\tag{1}
\]

Consequently,
\[
p\le q,\quad \kappa(p)\ne\kappa(q)
\quad\Longrightarrow\quad p\ll q.
\tag{2}
\]

**Proof.**
A poset having a cofinal chain has the same cofinality as that chain. A chain has cofinality \(1\), or infinite regular cofinality; in the latter case it has a strictly increasing well-ordered cofinal subset of that length.

If \(I(p)\) has a maximum, its supremum shows that the maximum is \(p\). This gives the first assertion.

For (1), the case \(\kappa(p)=1\) is impossible because \(p\ll p\). Put \(\kappa=\kappa(p)\), and choose an increasing cofinal chain \((k_\xi)_{\xi<\kappa}\) in \(I(p)\). Every \(k_\xi\) lies below a member of \(C\). On the other hand, for each \(c\in C\), the set
\[
\{\xi:k_\xi\le c\}
\]
is bounded in \(\kappa\), since otherwise \(p\le c\).

Put \(\mu=\operatorname{cf}(C)\). Covering \(\kappa\) by the bounded sets associated with a cofinal subset of \(C\) gives \(\kappa\le\mu\). If \(\kappa<\mu\), choose \(c_\xi\in C\) above \(k_\xi\). These \(\kappa\) members have an upper bound in \(C\), which would lie above \(p\). Thus \(\mu=\kappa\).

Finally, a chain witnessing the failure of \(p\ll q\), where \(p\le q\), avoids both \(\uparrow p\) and \(\uparrow q\). Equation (1) would give \(\kappa(p)=\kappa(q)\). ∎

We will repeatedly use this special consequence: if a strictly increasing chain of regular length \(\mu\) has supremum \(r\), not attained in the chain, then
\[
\kappa(r)=\mu.
\tag{3}
\]

### Lemma 2: chain-closed lower sets are directed-closed

In any dcpo, a lower set closed under suprema of nonempty chains is closed under suprema of directed sets.

**Proof.**
Use induction on the cardinality of a directed set \(D\) contained in the lower set.

Finite directed sets have a maximum. Countable directed sets have a cofinal increasing sequence. For uncountable \(|D|=\mu\), choose an increasing family
\[
(D_\alpha)_{\alpha<\mu}
\]
of nonempty directed subsets covering \(D\), each of cardinality less than \(\mu\). Such a family is obtained by enumerating \(D\) and closing under a chosen binary upper-bound operation. At stage \(\alpha\), its size can be kept at most \(\max(\aleph_0,|\alpha|)\).

By induction, every \(\bigvee D_\alpha\) belongs to the lower set. Their increasing chain has supremum \(\bigvee D\), so this belongs as well. ∎

### Lemma 3: a rectangular refinement

Suppose
\[
p_0\le p_1\le\cdots,\qquad \kappa(p_n)=\kappa
\]
for an infinite regular cardinal \(\kappa\). There are elements
\[
y_{\xi n}\in I(p_n)\qquad(\xi<\kappa,\ n<\omega)
\]
increasing in both coordinates, such that
\[
\bigvee_{\xi<\kappa}y_{\xi n}=p_n
\quad(n<\omega).
\tag{4}
\]

**Proof.**
Choose a cofinal \(\kappa\)-chain in each \(I(p_n)\). Recursively, first on \(\xi\), then on \(n\), choose \(y_{\xi n}\) above:

* the \(\xi\)-th member of that cofinal chain;
* all \(y_{\eta n}\), \(\eta<\xi\);
* \(y_{\xi,n-1}\), when \(n>0\).

All these elements belong to \(I(p_n)\). There are fewer than \(\kappa\) of them, so its cofinal \(\kappa\)-chain supplies an upper bound in \(I(p_n)\). ∎

## 2. Two chain-closure steps suffice

For a nonempty lower set \(X\), define
\[
T(X)=
\{p:\text{some chain }C\subseteq X\text{ satisfies }p\le\bigvee C\}.
\]
The approximation assumption gives the useful identity
\[
p\in T(X)\quad\Longleftrightarrow\quad I(p)\subseteq X.
\tag{5}
\]
Indeed, the forward implication follows from the definition of \(\ll\); for the reverse implication, use the chain \(K_p\subseteq I(p)\).

Let \(L\) be a nonempty directed lower set, and put
\[
L_1=T(L),\qquad L_2=T(L_1).
\]

### Lemma 4: the exceptional second layer

If
\[
p\in L_2\setminus L_1,
\]
then
\[
\kappa(p)=\aleph_1.
\]
Furthermore,
\[
a\in I(p)\setminus L\quad\Longrightarrow\quad\kappa(a)=\aleph_0.
\tag{6}
\]

**Proof.**
By (5), \(I(p)\subseteq L_1\), but \(I(p)\not\subseteq L\). Fix any
\[
a\in I(p)\setminus L.
\]
Let \(\lambda=\kappa(p)\). It is not \(1\), since that would put \(p\in I(p)\subseteq L_1\).

Choose a strictly increasing cofinal chain
\[
(x_\eta)_{\eta<\lambda}\subseteq I(p)
\]
and discard an initial segment so that \(a\le x_\eta\) throughout. Each \(x_\eta\in L_1\), so \(I(x_\eta)\subseteq L\). Therefore \(a\not\ll x_\eta\). By (2),
\[
\kappa(x_\eta)=\kappa(a)=:\kappa.
\tag{7}
\]
Also \(\kappa\ne1\), since \(a\ll a\le x_\eta\) would contradict \(a\not\ll x_\eta\).

Suppose first that \(\lambda>\aleph_0\). Take a strictly increasing countable subsequence and let \(r\) be its supremum. This subsequence is bounded by a later \(x_\eta\), so \(r\in L_1\). Since \(a\le r\) and \(a\notin L\), (5) gives \(a\not\ll r\). Thus, by (2) and (3),
\[
\kappa=\kappa(r)=\aleph_0.
\]
If \(\lambda>\aleph_1\), the same argument using a subsequence of length \(\omega_1\) gives \(\kappa=\aleph_1\), a contradiction. Hence in this case \(\lambda=\aleph_1\), as required.

It remains to exclude \(\lambda=\aleph_0\). Write the cofinal chain as \((x_n)\).

If \(\kappa=\aleph_0\), every \(I(x_n)\subseteq L\) has a countable cofinal chain. Directedness of \(L\) lets us choose an increasing sequence in \(L\) dominating, successively, finite portions of all these chains. Its supremum lies above every \(x_n\), hence above \(p\). This puts \(p\in L_1\), a contradiction.

If \(\kappa>\aleph_0\), apply Lemma 3 to \((x_n)\). All \(y_{\xi n}\) belong to \(L\). Set
\[
r_\xi=\bigvee_{n<\omega}y_{\xi n}.
\]
No \(r_\xi\) lies above \(a\): otherwise the countable chain \((y_{\xi n})_n\), which avoids \(\uparrow a\), would contradict (1), because \(\kappa(a)>\aleph_0\). But \((r_\xi)_{\xi<\kappa}\) is a chain with supremum \(p\), contradicting \(a\ll p\).

Thus \(\lambda=\aleph_0\) is impossible. The argument applies to every \(a\in I(p)\setminus L\), proving (6). ∎

### Lemma 5: \(L_2\) is chain-closed

**Proof.**
Let \(C\subseteq L_2\) be a chain.

If \(C\cap L_1\) is cofinal in \(C\), then \(\bigvee C\in T(L_1)=L_2\). Otherwise, replace \(C\) by a cofinal tail outside \(L_1\). All its members then have \(\kappa=\aleph_1\), by Lemma 4.

If this tail has uncountable cofinality, choose a strictly increasing countable sequence in it and a later member bounding the sequence. Its supremum \(r\) lies in \(L_2\setminus L_1\), but (3) gives \(\kappa(r)=\aleph_0\), contradicting Lemma 4.

We are left with a countable cofinal sequence
\[
p_0<p_1<\cdots
\]
in \(L_2\setminus L_1\). Apply Lemma 3 with \(\kappa=\aleph_1\), and set
\[
r_\xi=\bigvee_{n<\omega}y_{\xi n}.
\]
Here \(I(p_n)\subseteq L_1\), so \(r_\xi\in L_2\). In fact \(r_\xi\in L_1\): otherwise Lemma 4 would give \(\kappa(r_\xi)=\aleph_1\), whereas its defining countable chain either attains its supremum in \(L_1\), or gives \(\kappa(r_\xi)=\aleph_0\) by (1).

Consequently,
\[
\bigvee C=\bigvee_{\xi<\omega_1}r_\xi\in T(L_1)=L_2.
\]
∎

Combining Lemmas 2 and 5 gives
\[
\boxed{L_2=\downarrow\bigvee L.}
\tag{8}
\]
One inclusion is immediate. For the other, the chain-closed lower set \(L_2\) contains the directed set \(L\), hence contains its supremum.

## 3. Necessity of \((\aleph_0,\aleph_1)\)

Suppose
\[
a\ll_{\mathrm{ch}}b,\qquad a\not\ll_{\mathrm{dir}}b.
\]
Choose a directed witness \(D\) with
\[
b\le\bigvee D,\qquad a\not\le d\quad(d\in D).
\]
Put \(L=\downarrow D\). Then \(a\notin L\), and (8) gives \(b\in L_2\).

We cannot have \(b\in L_1\), because (5) would imply \(I(b)\subseteq L\), contrary to \(a\in I(b)\setminus L\). Thus
\[
b\in L_2\setminus L_1.
\]
Lemma 4 now gives
\[
\boxed{\kappa(a)=\aleph_0,\qquad \kappa(b)=\aleph_1.}
\]

## 4. A ZFC example realizing the pair

We construct an auxiliary directed poset \(A\) with these properties:

1. every principal lower set is finite;
2. every proper ideal is countable;
3. \(A\) has cardinality \(\aleph_1\).

Here an ideal means a nonempty directed lower set.

### 4.1 Coherent finite sets

There exist finite sets
\[
F_n(\beta)\subseteq\beta+1
\qquad(\beta<\omega_1,\ n<\omega)
\]
such that
\[
\begin{split}
&\beta\in F_n(\beta),\qquad F_n(\beta)\subseteq F_{n+1}(\beta),\\
&\bigcup_nF_n(\beta)=\beta+1,\\
&\alpha\in F_n(\beta)
 \Longrightarrow
 F_n(\alpha)=F_n(\beta)\cap(\alpha+1).
\end{split}
\tag{9}
\]

Here is a transfinite-recursive construction, included to make the example entirely explicit.

Set \(F_n(0)=\{0\}\). For \(\beta>0\), choose a surjection \(e:\omega\to\beta\), and put
\[
\alpha_k=\max\{e(0),\ldots,e(k)\}.
\]
Choose strictly increasing integers \(n_k\) so that
\[
\{e(0),\ldots,e(k)\}\cup\{\alpha_{k-1}:k>0\}
 \subseteq F_{n_k}(\alpha_k).
\]
This is possible by the already constructed exhaustion property below \(\beta\). Define
\[
F_n(\beta)=
\begin{cases}
\{\beta\},&n<n_0,\\
F_n(\alpha_k)\cup\{\beta\},&n_k\le n<n_{k+1}.
\end{cases}
\]
Finiteness, exhaustion, and coherence follow immediately by induction. At a transition between successive blocks, monotonicity follows from
\[
\alpha_{k-1}\in F_{n_k}(\alpha_k)
\]
and the coherence already established below \(\beta\).

### 4.2 The auxiliary poset

Let
\[
A=\{s_n:n<\omega\}\cup
  \{t_{\alpha,n}:\alpha<\omega_1,\ n<\omega\}.
\]
Define
\[
s_n\le s_m\iff n\le m,
\]
\[
s_n\le t_{\beta,m}\iff n\le m,
\]
and
\[
t_{\alpha,n}\le t_{\beta,m}
\iff n\le m\text{ and }\alpha\in F_m(\beta).
\tag{10}
\]
No \(t_{\alpha,n}\) lies below an \(s_m\).

The properties in (9) prove transitivity; antisymmetry follows from
\(F_m(\beta)\subseteq\beta+1\). The exhaustion property proves directedness.

Every principal lower set is finite. Explicitly,
\[
\downarrow t_{\beta,m}
=
\{s_n:n\le m\}\cup
\{t_{\alpha,n}:\alpha\in F_m(\beta),\ n\le m\}.
\tag{11}
\]

Put
\[
a_0=\{s_n:n<\omega\}.
\]

We next verify that every proper ideal \(J\) of \(A\) is countable.

* If \(a_0\not\subseteq J\), the second coordinates of its elements are bounded. Let their maximum be \(m\). Elements of second coordinate \(m\) are cofinal in \(J\). Apart from a possible \(s_m\), they form a chain: if \(t_{\alpha,m}\) and \(t_{\beta,m}\) have a common upper bound \(t_{\gamma,m}\), coherence in (9) makes them comparable. Every chain in \(A\) is countable, because principal lower sets are finite. Thus \(J\) is countable.

* If \(a_0\subseteq J\) and \(t_{\alpha,n}\in J\), directedness with the \(s_m\)'s shows that \(t_{\alpha,m}\in J\) for every \(m\). Exhaustion in (9) then shows that \(J\) contains every column indexed below \(\alpha\). Consequently,
  \[
  J=a_0\cup\{t_{\alpha,n}:\alpha<\gamma,\ n<\omega\}
  \]
  for some \(\gamma\le\omega_1\). If \(J\ne A\), then \(\gamma<\omega_1\), so \(J\) is countable.

### 4.3 Take the ideal completion

Let \(P\) be the poset of all ideals of \(A\), ordered by inclusion. Directed suprema are unions, so \(P\) is a dcpo. Its greatest element is
\[
b=A.
\]
Let \(a=a_0\), viewed as an element of \(P\).

For \(u\in A\), the principal ideal \(\downarrow_Au\) is compact in \(P\).

Every proper ideal \(J\) is countable, so it has an increasing cofinal sequence \((u_n)\). Therefore
\[
J=\bigvee_n\downarrow_Au_n.
\]
It follows that
\[
I_P(J)=
\downarrow_P\{\downarrow_Au:u\in J\}.
\tag{12}
\]
Indeed, the inclusion from right to left follows from compactness; the reverse inclusion follows by applying the chain-way-below definition to \((\downarrow_Au_n)\). Thus every proper \(J\) satisfies the required approximation condition.

For the top element, we claim
\[
I_P(b)=P\setminus\{b\}.
\tag{13}
\]
If a chain of proper ideals has union \(A\), it cannot have countable cofinality: each proper ideal is countable. Hence every countable ideal is contained in some member of that chain. This proves that every proper ideal is chain-way-below \(b\).

On the other hand, the proper ideals
\[
J_\gamma=a_0\cup
 \{t_{\alpha,n}:\alpha<\gamma,\ n<\omega\},
 \qquad \gamma<\omega_1,
\]
form a cofinal chain in \(P\setminus\{b\}\) whose supremum is \(b\). Thus \(b\not\ll_{\mathrm{ch}}b\), proving (13). This also verifies the approximation condition at \(b\).

The ideal \(a\) is nonprincipal and countably generated, so (12) gives
\[
\operatorname{cf}(I_P(a))=\aleph_0.
\]
The chain \((J_\gamma)_{\gamma<\omega_1}\) and countability of all proper ideals give
\[
\operatorname{cf}(I_P(b))=\aleph_1.
\]

Finally, \(a\ll_{\mathrm{ch}}b\) by (13), but the directed family
\[
\{\downarrow_Au:u\in A\}
\]
has supremum \(b\), and none of its members contains \(a\), by (11). Hence
\[
a\not\ll_{\mathrm{dir}}b.
\]

This realizes the required pair.

## 5. Executable checks

No finite computation can verify a statement quantified over all ordinals below \(\omega_1\); those steps were proved above. The following Python actually constructs exact instances of (9), including ordinals beyond \(\omega\), and checks:

* finiteness, monotonicity, exhaustion witnesses, and coherence;
* the auxiliary order axioms and actual common upper bounds;
* the fixed-height comparability used in the ideal classification;
* both way-below definitions by exhaustive subset enumeration on a finite instance.

Ordinals below \(\omega^2\) are represented exactly by pairs \((b,t)\), meaning \(\omega b+t\).

```python
from functools import lru_cache

def enum(beta, k):
    """A surjection omega -> beta, for 0 < beta < omega^2."""
    b, t = beta
    if b == 0:
        assert t > 0
        return (0, min(k, t - 1))
    if k < t:
        return (b, k)
    q, r = divmod(k - t, b)
    return (r, q)

@lru_cache(None)
def F(beta, n):
    if beta == (0, 0):
        return frozenset([beta])

    seen = set()
    previous_alpha = None
    previous_level = -1
    active = None
    k = 0

    while True:
        seen.add(enum(beta, k))
        alpha = max(seen)
        level = previous_level + 1
        required = seen | (
            {previous_alpha} if previous_alpha is not None else set()
        )
        while not required.issubset(F(alpha, level)):
            level += 1

        if level > n:
            return (frozenset([beta]) if active is None
                    else F(active, n) | {beta})

        active = alpha
        previous_alpha, previous_level = alpha, level
        k += 1

def finite_subset_checks():
    ordinals = [(b, t) for b in range(4) for t in range(9)]
    checks = 0

    for beta in ordinals:
        for n in range(7):
            B = F(beta, n)
            assert beta in B
            assert all(alpha <= beta for alpha in B)
            assert B.issubset(F(beta, n + 1))
            for alpha in B:
                assert F(alpha, n) == frozenset(
                    x for x in B if x <= alpha
                )
                checks += 1

    largest_witness = 0
    for beta in ordinals:
        for alpha in ordinals:
            if alpha <= beta:
                n = 0
                while alpha not in F(beta, n):
                    n += 1
                    assert n < 500
                largest_witness = max(largest_witness, n)

    return checks, largest_witness

# s_n = ('s', n); t_{alpha,n} = ('t', alpha, n).
def height(x):
    return x[-1]

def le(x, y):
    if x[0] == 's':
        return height(x) <= height(y)
    if y[0] == 's':
        return False
    return (height(x) <= height(y)
            and x[1] in F(y[1], height(y)))

def check_poset(ordinals, levels):
    A = [('s', n) for n in range(levels)]
    A += [('t', alpha, n)
          for alpha in ordinals for n in range(levels)]
    N = len(A)
    rows = [{j for j, y in enumerate(A) if le(x, y)} for x in A]

    for i in range(N):
        assert i in rows[i]
        for j in rows[i]:
            assert i == j or i not in rows[j]
            assert rows[j].issubset(rows[i])

    fixed_height_checks = 0
    for n in range(levels):
        for gamma in ordinals:
            lower = [alpha for alpha in ordinals
                     if alpha in F(gamma, n)]
            for alpha in lower:
                for beta in lower:
                    assert (alpha in F(beta, n)
                            or beta in F(alpha, n))
                    fixed_height_checks += 1

    largest_level = 0
    for x in A:
        for y in A:
            indices = [z[1] for z in (x, y) if z[0] == 't']
            if not indices:
                z = ('s', max(height(x), height(y)))
            else:
                beta = max(indices)
                m = max(height(x), height(y))
                while not all(alpha in F(beta, m)
                              for alpha in indices):
                    m += 1
                z = ('t', beta, m)
                largest_level = max(largest_level, m)
            assert le(x, z) and le(y, z)

    return N, fixed_height_checks, largest_level

def exhaustive_finite_dcpo():
    A = [('s', n) for n in range(2)]
    A += [('t', (0, alpha), n)
          for alpha in range(3) for n in range(2)]
    N = len(A)
    subsets = [
        {i for i in range(N) if mask >> i & 1}
        for mask in range(1, 1 << N)
    ]

    def below(i, j):
        return le(A[i], A[j])

    def directed(S):
        return all(
            any(below(i, k) and below(j, k) for k in S)
            for i in S for j in S
        )

    def chain(S):
        return all(below(i, j) or below(j, i)
                   for i in S for j in S)

    def sup(S):
        upper = [j for j in range(N)
                 if all(below(i, j) for i in S)]
        least = [j for j in upper
                 if all(below(j, k) for k in upper)]
        assert len(least) == 1
        return least[0]

    directed_sets = [S for S in subsets if directed(S)]
    chains = [S for S in subsets if chain(S)]
    relations = []

    for sets in (chains, directed_sets):
        tests = [(S, sup(S)) for S in sets]
        relation = {
            (a, b) for a in range(N) for b in range(N)
            if all(
                not below(b, s)
                or any(below(a, c) for c in S)
                for S, s in tests
            )
        }
        relations.append(relation)

    order = {(a, b) for a in range(N) for b in range(N)
             if below(a, b)}
    assert relations[0] == relations[1] == order

    ideals = [
        D for D in directed_sets
        if all(j in D for i in D for j in range(N) if below(j, i))
    ]
    for D in ideals:
        TD = {
            p for C in chains if C.issubset(D)
            for p in range(N) if below(p, sup(C))
        }
        assert TD == D

    return N, len(subsets), len(chains), len(directed_sets), len(ideals)

print(finite_subset_checks())
print(check_poset(
    [(b, t) for b in range(3) for t in range(5)], 4
))
print(exhaustive_finite_dcpo())
```

The executed output was:

```text
(1959, 26)
(64, 1562, 9)
(8, 255, 71, 181, 8)
```

Thus the proof excludes every pair except \((\aleph_0,\aleph_1)\), and the ZFC construction realizes that pair. Nothing remains unresolved.
# agent_1: last reply

The missing construction can be carried out. The answer is
\[
\boxed{\mathcal E=
\bigl\{(\Pi,m):m\ge2\bigr\}
\;\cup\;
\bigl\{(\Sigma,m):m\ge3\bigr\}.}
\]

The main point is to construct a \(\Pi^0_2\) set whose skip does not have cototal degree. I give that construction below, without using the recent existence result as a black box.

Write
\[
K_X=\{e:e\in\Gamma_e(X)\},\qquad S(X)=\overline{K_X}=X^\diamond,
\]
and use the usual computable join \(X\oplus Y\).

## 1. Preliminary facts

Enumeration operators are monotone, compose effectively, and satisfy
\[
K_X\equiv_e X. \tag{1}
\]
Also, if \(Y\leq_e X\), then
\[
\overline Y\leq_m S(X). \tag{2}
\]
For (2), given \(Y=\Gamma_i(X)\), uniformly obtain an index \(h(i,y)\) for the operator that outputs all of \(\omega\) if \(y\in\Gamma_i(Z)\), and outputs nothing otherwise. Then
\[
y\notin Y\iff h(i,y)\in S(X).
\]

We need the following characterization:
\[
\mathbf d_e(Y)\text{ is cototal}
\iff
\exists i,j\quad
Y=\Gamma_i\bigl(\overline{\Gamma_j(Y)}\bigr). \tag{3}
\]
For the forward implication, take \(C\equiv_e Y\) with \(C\leq_e\overline C\), and compose the relevant reductions. Conversely, if
\[
C=\Gamma_j(Y),\qquad Y=\Gamma_i(\overline C),
\]
then \(Y\oplus C\equiv_e Y\), and \(\overline{Y\oplus C}\) enumerates first \(Y\), using its \(\overline C\) column, and then \(C\). Thus \(Y\oplus C\leq_e\overline{Y\oplus C}\).

Enumerate all operator pairs computably, and put
\[
H_e(Y)=\Gamma_{i(e)}
          \bigl(\overline{\Gamma_{j(e)}(Y)}\bigr).
\]
Every \(H_e\) is antitone:
\[
Y\subseteq Z\implies H_e(Z)\subseteq H_e(Y). \tag{4}
\]
Consequently,
\[
G_e(X)=H_e(S(X))
\]
is monotone in \(X\).

By (3), our construction must arrange
\[
S(A)\ne H_e(S(A))\qquad\text{for every }e. \tag{5}
\]

## 2. The arithmetical lower boundary

Let \(K\) be an ordinary c.e. complete halting set and \(H=\overline K\).

Every \(\Sigma^0_2\) set is enumeration reducible to \(H\). Indeed, if
\[
x\in X\iff\exists u\,\forall v\,R(x,u,v),
\]
choose computable \(f\) with
\[
f(x,u)\in K\iff\exists v\,\neg R(x,u,v).
\]
Then
\[
x\in X\iff\exists u\,[f(x,u)\in H].
\]

For \(X\in\Sigma^0_2\), set \(B=X\oplus K\). We have \(B\equiv_e X\), and
\[
\overline B=\overline X\oplus H
\]
enumerates \(X\) using \(H\), and enumerates \(K\) without an oracle. Hence \(B\leq_e\overline B\): every \(\Sigma^0_2\) degree is cototal.

Moreover, the skip of a cototal degree is total. If \(B\equiv_e X\) and \(B\leq_e\overline B\), then by (2),
\[
X\leq_e B\leq_e\overline B\leq_e S(X).
\]
Using (1),
\[
\overline{S(X)}=K_X\leq_e X\leq_e S(X).
\]
Thus \(S(X)\) itself is a total set.

It follows that no \(\Sigma^0_2\) set is a witness. This also excludes \(\Sigma^0_1\) and \(\Pi^0_1\).

We will also use:
\[
X\in\Pi^0_2\implies \mathbf d_e(X)\text{ is weakly cototal}. \tag{6}
\]
Again take \(B=X\oplus K\). Since \(\overline X\in\Sigma^0_2\),
\[
\overline B=\overline X\oplus H\equiv_e H,
\]
whose degree is total. This proves (6).

## 3. Two effective observations for the construction

First, if \(B\) is computable, then \(S(B)\) is uniformly \(\Pi^0_1\), and
\[
z\notin\Gamma_j(S(B))
\]
is uniformly \(\Pi^0_2\).

Here is an explicit normal form. Fix computable finite stage approximations \(W_j[s]\) and \(K_B[t]\). Then
\[
z\notin\Gamma_j(S(B))
\iff
\forall s\,\exists t\
\forall (z,E)\in W_j[s]\;
[E\cap K_B[t]\ne\varnothing]. \tag{7}
\]
The last quantifier ranges over a finite, effectively known collection.

Second, finite conjunctions and finite disjunctions of \(\Pi^0_2\) predicates are uniformly \(\Pi^0_2\), including when the finite number of predicates depends computably on the input. For example,
\[
\bigvee_{\ell<N}\forall u\,\exists v\,R_\ell(u,v)
\iff
\forall(u_0,\ldots,u_{N-1})\,
\exists(v_0,\ldots,v_{N-1})\,
\bigvee_{\ell<N}R_\ell(u_\ell,v_\ell).
\tag{8}
\]

## 4. A computable tree of intervals

A node \(\sigma\) carries a computable set \(L_\sigma\) and a computable reservoir \(R_\sigma\), disjoint from \(L_\sigma\), with a computable bijection
\[
\nu_\sigma:\omega\longrightarrow R_\sigma.
\]
All these objects, including membership in their ranges, will be uniform in \(\sigma\).

At the root,
\[
L_\varnothing=\varnothing,\qquad R_\varnothing=\omega,\qquad
\nu_\varnothing(n)=n.
\]

Use the Cantor pairing function \(\langle j,t\rangle\), which satisfies
\(\langle j,t\rangle\ge j,t\). Partition \(R_\sigma\) into
\[
\begin{aligned}
D_\sigma&=\{d_{\sigma,j}:j\in\omega\},
&d_{\sigma,j}&=\nu_\sigma(3j),\\
V_\sigma&=\{v_{\sigma,t}:t\in\omega\},
&v_{\sigma,t}&=\nu_\sigma(3t+1),\\
R_{\sigma,j}&=\{\rho_{\sigma,j}(t):t\in\omega\},
&\rho_{\sigma,j}(t)&=\nu_\sigma(3\langle j,t\rangle+2).
\end{aligned}
\]

The children are indexed by \(\infty,0,1,2,\ldots\).

For the \(\infty\)-child, put
\[
L_{\sigma\infty}=L_\sigma,\qquad
R_{\sigma\infty}=V_\sigma,\qquad
\nu_{\sigma\infty}(t)=v_{\sigma,t}.
\]

Index pairs consisting of an integer \(k\) and a subset \(p\subseteq\{0,\ldots,k-1\}\) by
\[
r=r(k,p)=2^{k+1}-2-p,
\tag{9}
\]
where \(p\) is read as its binary code. Thus increasing \(r\) lists increasing \(k\), and within a fixed \(k\), decreasing \(p\). Write \(k(r),p(r)\) for the inverse decoding. Notice that \(k(r)\le r\).

For such an \(r\), define the computable set
\[
B_{\sigma,r}
=
L_\sigma
\cup
\{v_{\sigma,t}:t\ge k(r)\text{ or }t\in p(r)\}
\cup
\bigcup_{j>r}R_{\sigma,j}.
\tag{10}
\]
The \(r\)-child has
\[
\begin{aligned}
L_{\sigma r}
   &=B_{\sigma,r}\cup\{d_{\sigma,j}:j\ge r\},\\
R_{\sigma r}&=R_{\sigma,r},\\
\nu_{\sigma r}(t)&=\rho_{\sigma,r}(t).
\end{aligned}
\tag{11}
\]
These definitions are all computable and preserve disjointness of the lower set and reservoir.

Finally, obtain a computable index \(x_\sigma\) such that
\[
\Gamma_{x_\sigma}(X)=
\begin{cases}
\omega,&X\cap D_\sigma\ne\varnothing,\\
\varnothing,&X\cap D_\sigma=\varnothing.
\end{cases}
\]
In particular,
\[
x_\sigma\in S(X)\iff X\cap D_\sigma=\varnothing. \tag{12}
\]

## 5. Bounded-witness tests and the \(\Pi^0_2\) definition

At node \(\sigma\), let \(e=|\sigma|\), so the node addresses \(H_e\).

For \(r=r(k,p)\), let \(T_{\sigma,r}\) say that there is a finite set \(F\), of code at most \(k\), such that
\[
(x_\sigma,F)\in W_{i(e)}[k]
\quad\text{and}\quad
F\cap\Gamma_{j(e)}(S(B_{\sigma,r}))=\varnothing.
\tag{13}
\]
This is uniformly \(\Pi^0_2\), by (7) and finite closure. It implies
\[
x_\sigma\in H_e(S(B_{\sigma,r})).
\tag{14}
\]

An important preservation property is that, with \(\sigma,k\) fixed, enlarging \(B_{\sigma,r}\) preserves a witnessing \(F\) in (13). Indeed, enlarging \(B\) shrinks \(S(B)\), hence shrinks \(\Gamma_{j(e)}(S(B))\).

We now define predicates \(a_\sigma(n)\). Put
\[
Q_{\sigma,r}
=
T_{\sigma,r}\ \wedge\
\bigwedge_{t\in p(r)}a_{\sigma\infty}(t).
\tag{15}
\]
Define
\[
\begin{aligned}
a_\sigma(3j)
   &\iff\bigvee_{r\le j}Q_{\sigma,r},\\[1mm]
a_\sigma(3t+1)
   &\iff a_{\sigma\infty}(t)
       \ \vee\
       \bigvee_{r:\,k(r)\le t}Q_{\sigma,r},\\[1mm]
a_\sigma(3\langle j,t\rangle+2)
   &\iff
       \bigvee_{r<j}Q_{\sigma,r}
       \ \vee\
       \bigl(Q_{\sigma,j}\wedge a_{\sigma j}(t)\bigr).
\end{aligned}
\tag{16}
\]
Every disjunction displayed here is finite.

These are **well-founded effective definitions**, not an appeal to an arithmetical fixed-point theorem. To compute a \(\Pi^0_2\) formula for \(a_\sigma(n)\), recursively expand (15)–(16). Every recursive call \(a_\tau(u)\) has \(u<n\):

* At \(n=3j\), the gates use \(u<k(r)\le r\le j\).
* At \(n=3t+1\), they use \(u<k(r)\le t\), and the direct child call has argument \(t<n\).
* At \(n=3\langle j,t\rangle+2\), the gates use \(u<k(r)\le r\le j<n\), and \(t<n\).

Thus strong induction on \(n\), using (7)–(8), proves that \(a_\sigma(n)\) is uniformly \(\Pi^0_2\), with no set parameters.

Set
\[
A_\sigma=L_\sigma\cup\{\nu_\sigma(n):a_\sigma(n)\}.
\tag{17}
\]
In particular,
\[
A=A_\varnothing\in\Pi^0_2. \tag{18}
\]

## 6. The interval identity and the true child

The finite definitions imply the identity
\[
A_\sigma
=
A_{\sigma\infty}\ \cup\
\bigcup_{\{r:Q_{\sigma,r}\}} A_{\sigma r}.
\tag{19}
\]

Importantly, (19) is a **derived identity**, not our definition of \(A_\sigma\); defining the sets by that infinite union would not establish their \(\Pi^0_2\) complexity.

To verify (19), inspect the partition of \(R_\sigma\):

* A diagonal marker \(d_{\sigma,j}\) belongs to a positive child's lower set exactly for \(r\le j\).
* A point of \(R_{\sigma,j}\) belongs to every positive child with \(r<j\), to child \(j\) according to its own predicate, and to none with \(r>j\).
* At \(v_{\sigma,t}\), a positive child contributes either because \(k(r)\le t\), or because \(t\in p(r)\). In the latter case, the gate in (15) already puts that point into \(A_{\sigma\infty}\).

These are precisely the three lines of (16).

If there is no true \(Q_{\sigma,r}\), (19) gives
\[
A_\sigma=A_{\sigma\infty}. \tag{20}
\]

Otherwise, let \(r=r(k,p)\) be the least true test. Then
\[
p=\{t<k:a_{\sigma\infty}(t)\}. \tag{21}
\]
The gate gives inclusion from left to right. If it were proper, let \(p^*\) be the set on the right. Because \(p^*\supsetneq p\), its index \(r^*=r(k,p^*)\) is less than \(r\), and
\[
B_{\sigma,r}\subseteq B_{\sigma,r^*}.
\]
The same bounded witness preserves \(T_{\sigma,r^*}\), and its prefix gate holds. This contradicts minimality of \(r\).

Equation (21) implies
\[
A_{\sigma\infty}\subseteq B_{\sigma,r}.
\tag{22}
\]
Furthermore, if \(s>r\) and \(Q_{\sigma,s}\) holds, then
\[
A_{\sigma s}\subseteq L_{\sigma r}. \tag{23}
\]
For the \(R_{\sigma,j}\) and diagonal-marker parts this follows directly from \(s>r\). For the \(V_\sigma\) part, \(k(s)\ge k(r)\), and every selected prefix bit in \(p(s)\) is a true bit of \(A_{\sigma\infty}\); below \(k(r)\), (21) therefore puts it in \(p(r)\).

Since \(A_{\sigma r}\) contains \(L_{\sigma r}\), (19), (22), and (23) yield
\[
A_\sigma=A_{\sigma r}. \tag{24}
\]

Thus every node has a **true child** carrying exactly the same set: its \(\infty\)-child if no test holds, and otherwise its least true positive child.

## 7. Every node diagonalizes

Let \(e=|\sigma|\).

### Positive true-child case

Suppose \(Q_{\sigma,r}\) is the least true test. By (24),
\[
A_\sigma=A_{\sigma r}\supseteq B_{\sigma,r},
\]
and \(A_\sigma\) contains all \(d_{\sigma,j}\) for \(j\ge r\). Thus, by (12),
\[
x_\sigma\notin S(A_\sigma).
\]
On the other hand, (14), monotonicity of \(G_e(X)=H_e(S(X))\), and
\(B_{\sigma,r}\subseteq A_\sigma\) give
\[
x_\sigma\in H_e(S(A_\sigma)).
\]
So the two sets differ.

### Negative true-child case

Suppose no \(Q_{\sigma,r}\) holds. Then
\[
A_\sigma=A_{\sigma\infty},
\]
so \(A_\sigma\cap D_\sigma=\varnothing\), and therefore
\[
x_\sigma\in S(A_\sigma).
\]

Assume for a contradiction that
\[
x_\sigma\in H_e(S(A_\sigma)).
\]
Choose a finite witnessing \(F\), and choose \(k\) large enough that its code is at most \(k\) and its output rule has appeared by stage \(k\). Put
\[
p=\{t<k:a_{\sigma\infty}(t)\},\qquad r=r(k,p).
\]
Then \(A_\sigma\subseteq B_{\sigma,r}\). Hence
\[
S(B_{\sigma,r})\subseteq S(A_\sigma),
\]
so the same \(F\) remains disjoint from
\(\Gamma_{j(e)}(S(B_{\sigma,r}))\). Thus \(T_{\sigma,r}\) holds. Its prefix gate holds by the choice of \(p\), giving \(Q_{\sigma,r}\), a contradiction.

Therefore in this case too,
\[
S(A_\sigma)\ne H_e(S(A_\sigma)). \tag{25}
\]

Starting at the root and repeatedly taking the true child gives a node \(\sigma_e\) at every level \(e\), with
\[
A=A_{\sigma_e}.
\]
Equation (25) then establishes (5) for every \(e\). By (3),
\[
\boxed{\mathbf d_e(A^\diamond)\text{ is not cototal}.} \tag{26}
\]

Together with (18) and (6), this is the required \(\Pi^0_2\) weakly cototal witness.

## 8. Completing the classification

The witness just constructed belongs to every \(\Pi^0_m\), \(m\ge2\), and every \(\Sigma^0_m\), \(m\ge3\), by adding dummy quantifiers.

Section 2 excluded \(\Sigma^0_1,\Sigma^0_2,\Pi^0_1\). These are exactly the remaining cases. Therefore
\[
\boxed{\mathcal E=
\{(\Pi,m):m\ge2\}\cup\{(\Sigma,m):m\ge3\}.}
\]

## 9. Python checks

The infinite assertions above are mathematical proofs, not conclusions drawn from finite experiments. The following code checks the construction's finite algebra and numerical recursion, and actually constructs the finite positive-Boolean formula DAGs underlying (15)–(16). It does not pretend to decide the resulting \(\Pi^0_2\) predicates.

I ran it successfully. In particular, it checked 100,000 recursion ranks, 9,472 interval-union instances, and all finite Boolean tables used in the displayed two-predicate \(\Pi^0_2\) normal-form identity.

```python
from itertools import product
from math import isqrt
from functools import lru_cache

def pair(a, b):
    return (a+b)*(a+b+1)//2 + b

def unpair(z):
    w = (isqrt(8*z+1)-1)//2
    b = z-w*(w+1)//2
    return w-b, b

def decode(r):
    k = (r+1).bit_length()-1
    p = (1 << (k+1))-2-r
    assert 0 <= p < (1 << k)
    return k, p

# Numerical partition and strict recursion-rank checks.
for n in range(100000):
    if n % 3 == 0:
        j = n//3
        k, p = decode(j)
        assert k <= j
        assert k == 0 or k-1 < n
    elif n % 3 == 1:
        t = n//3
        assert t < n
        assert t == 0 or t-1 < n
    else:
        j, t = unpair(n//3)
        assert 3*pair(j, t)+2 == n
        assert j < n and t < n
        k, p = decode(j)
        assert k == 0 or k-1 < n
print("100000 reservoir/rank checks passed")

# Exhaustive finite interval model:
# k <= 2; seven positive children; two V-coordinates.
K = 2
M = (1 << (K+1))-1
D = [1 << j for j in range(M)]
V = [1 << (M+t) for t in range(K)]
R = [1 << (M+K+j) for j in range(M)]

B, lower, upper = [], [], []
for r in range(M):
    k, p = decode(r)
    b = sum(V[t] for t in range(K)
            if t >= k or ((p >> t) & 1))
    b |= sum(R[j] for j in range(r+1, M))
    lo = b | sum(D[j] for j in range(r, M))
    B.append(b)
    lower.append(lo)
    upper.append(lo | R[r])

models = unions = 0
for a in range(1 << K):
    aneg = sum(V[t] for t in range(K) if (a >> t) & 1)
    for q in range(1 << M):
        valid = True
        for r in range(M):
            if not ((q >> r) & 1):
                continue
            k, p = decode(r)
            if p & ~a:                 # Prefix gate.
                valid = False
                break
            for s in range(M):
                ell, h = decode(s)
                if ell == k and not (p & ~h) and not (h & ~a):
                    assert not (B[r] & ~B[s])
                    if not ((q >> s) & 1):
                        valid = False  # Same-k witness preservation.
                        break
            if not valid:
                break
        if not valid:
            continue

        models += 1
        active = [r for r in range(M) if (q >> r) & 1]
        if active:
            r0 = min(active)
            k, p = decode(r0)
            assert p == a & ((1 << k)-1)
            assert not (aneg & ~lower[r0])
            for s in active[1:]:
                assert not (upper[s] & ~lower[r0])

        # All choices inside the positive child reservoirs.
        for choices in range(1 << M):
            children = [
                lower[r] | (R[r] if (choices >> r) & 1 else 0)
                for r in range(M)
            ]
            union = aneg
            for r in active:
                union |= children[r]
            assert union == (children[active[0]] if active else aneg)
            unions += 1

print(models, "admissible test models;",
      unions, "child-union checks passed")

# Exhaustive finite checks of uniform Pi_2 AND/OR normal forms.
def pi2(table):
    return all(any(row) for row in table)

matrices = [
    ((a, b), (c, d))
    for a, b, c, d in product((False, True), repeat=4)
]
for A, Bm in product(matrices, repeat=2):
    for use_or in (False, True):
        op = (lambda a,b: a or b) if use_or else (
             lambda a,b: a and b)
        lhs = op(pi2(A), pi2(Bm))
        rhs = all(
            any(op(A[u][v], Bm[w][z])
                for v, z in product(range(2), repeat=2))
            for u, w in product(range(2), repeat=2)
        )
        assert lhs == rhs
print("512 Pi_2 closure normal-form checks passed")

# Exhaustive antitonicity check for all monotone maps P(2)->P(2).
maps = [
    f for f in product(range(4), repeat=4)
    if all((a & ~b) or not (f[a] & ~f[b])
           for a in range(4) for b in range(4))
]
for phi, psi in product(maps, repeat=2):
    h = [phi[3 ^ psi[a]] for a in range(4)]
    assert all((a & ~b) or not (h[b] & ~h[a])
               for a in range(4) for b in range(4))
print(len(maps)**2, "antitonicity checks passed")

# Construct the finite positive-Boolean Pi_2 formula DAGs.
# ("T", node, r) labels the atomic Pi_2 test (13).
calls = 0

@lru_cache(None)
def formula(node, n):
    global calls
    calls += 1

    def child(label, t):
        assert t < n, (node, n, label, t)
        return formula(node+(label,), t)

    def Q(r):
        k, p = decode(r)
        return (
            "AND", ("T", node, r),
            tuple(child(-1, t)
                  for t in range(k) if (p >> t) & 1)
        )

    if n % 3 == 0:
        j = n//3
        return ("OR", tuple(Q(r) for r in range(j+1)))

    if n % 3 == 1:
        t = n//3
        return (
            "OR", child(-1, t),
            tuple(Q(r) for r in range((1 << (t+1))-1))
        )

    j, t = unpair(n//3)
    return (
        "OR", tuple(Q(r) for r in range(j)),
        ("AND", Q(j), child(j, t))
    )

for n in range(25):
    formula((), n)

print("Formula DAGs for inputs 0..24 constructed;",
      calls, "recursive nodes checked")
```

**Proved:** the exact set \(\mathcal E\), including the \(\Pi^0_2\) existence construction and every excluded case. **Left:** nothing for the stated classification.
# agent_1: the whole run

[user message]
Let \(\omega=\{0,1,2,\ldots\}\), and write \(\overline X=\omega\setminus X\). Fix a standard effective enumeration \((W_e)_{e\in\omega}\) of all computably enumerable sets of pairs \((x,F)\), where \(x\in\omega\) and \(F\subseteq\omega\) is finite, using a computable coding of finite sets. Define
\[
\Gamma_e(B)=\{x:\exists F\subseteq B\text{ finite }\ ((x,F)\in W_e)\}.
\]
Write \(A\leq_e B\) if \(A=\Gamma_e(B)\) for some \(e\), and write \(A\equiv_e B\) if both \(A\leq_e B\) and \(B\leq_e A\). The enumeration degree of \(A\) is \(\mathbf d_e(A)=\{B:B\equiv_e A\}\). Define the skip of \(A\) by
\[
A^\diamond=\omega\setminus\{e:e\in\Gamma_e(A)\}.
\]
An enumeration degree \(\mathbf a\) is **total** if it contains a set \(B\) with \(\overline B\leq_e B\), and **cototal** if it contains a set \(B\) with \(B\leq_e\overline B\). It is **weakly cototal** if it contains a set \(B\) such that \(\mathbf d_e(\overline B)\) is total.

For each integer \(m\geq1\), a set belongs to \(\Sigma_m^0\), respectively \(\Pi_m^0\), if its membership relation can be expressed using \(m\) alternating blocks of quantifiers over \(\omega\), beginning with an existential, respectively universal, block, applied to a computable predicate. Dummy quantified variables are allowed, and no set parameters are allowed. Treat \(\Sigma\) and \(\Pi\) as labels, with \(\sigma_m^0\) denoting the corresponding class.

Determine the exact set
\[
\mathcal E=\left\{(\sigma,m)\in\{\Sigma,\Pi\}\times\{1,2,3,\ldots\}:\exists A\in\sigma_m^0\ \bigl[\mathbf d_e(A)\text{ is weakly cototal and }\mathbf d_e(A^\diamond)\text{ is not cototal}\bigr]\right\}.
\]

The answer was proved recently, so it is not an open problem: your task is to find it and prove it, completely, and to write Python that really computes or checks every step that can be checked. Printing what you believe is not evidence. Arriving at an answer that settles less than the question asks (a partial or conditional answer, "not known") is not acceptable, and neither is conceding: when an approach fails, try another.

Proving it means showing that the answer is right in every case the question covers, and that no other answer is.

Stop only when your proof is complete. When you stop, write in that response what you proved, and what is left.

## response 1
[reasoning summary]
**Exploring enumeration degrees**

I'm thinking about Σ2 sets and how they can be enumerated using 0'. It leads me to wonder about the nature of non-total possible Δ2 quasimimal sets. I'm curious if all Δ2 enumeration degrees are cototal. This raises interesting questions about the relationships between these concepts and how they interact in set theory. There’s a lot to unpack here, and I'm eager to explore these ideas further!

[reasoning summary]
**Evaluating set definitions**

I'm thinking about the total set B and its relationship with the enumeration function f. So, if there's an enumeration function where the range of B is involved and f is less than or equal to the computability of B, that means the total of f could also be represented in B. Hmm, if f can enumerate B, then that suggests something interesting about the computational complexity of B and its relationship with co-c.e. properties. I'll need to consider this more!

[reasoning summary]
**Exploring computational thresholds**

I'm considering an effective method for choosing a threshold cut that has high computability—specifically AΠ2 by left-c.e0' real—while avoiding all Π? comparisons. The antichains property seems to allow for "quasiminimal" constructions through left-c.e in 0' cuts. I wonder if this approach could actually yield A cototal itself? It's an interesting avenue to explore, as it could lead to some significant findings in this area.

[reasoning summary]
**Exploring theorem citation**

I'm considering how to introduce a theorem and prove it by referencing a full theorem, which isn't self-contained but still complete with regard to general math axioms. Even though they may disallow partial conditional answers, invoking an established theorem could work since it's not conditional. I need to ensure my answer is determinate and correct, so I'll look into citing the theorem accurately, perhaps by referencing the "Π2 noncototal-skip theorem."

[tool call: read_scratchpad]

[tool result]
```
(scratchpad.py is empty)
```

## response 2
[reasoning summary]
**Exploring computability concepts**

I'm diving into some complex computability theory here. I'm wondering if a maximal c.e. (computably enumerable) complement can exist without any infinite Σ2 subset. If A is 0'-immune, it seems that skipping A might not be cototal. I could prove this with finite changes and inclusion of S. It seems like S_K has some relationship with 0', and I might need to look into extracting finite information from S. It's intriguing to consider if S being cototal leads to constructing a positive A using 0'.

[tool call: write_scratchpad]
content:
```
from itertools import product

# Finite enumeration operators, represented by all monotone maps P(n)->P(n).
def monotone_maps(n):
    N = 1 << n
    return [f for f in product(range(N), repeat=N)
            if all((a & ~b) or not (f[a] & ~f[b])
                   for a in range(N) for b in range(N))]

n = 2
N = 1 << n
mask = N - 1
maps = monotone_maps(n)
checks = 0
for phi in maps:
    for psi in maps:
        h = [phi[mask ^ psi[a]] for a in range(N)]
        # Phi(complement Psi(.)) is antitone.
        assert all((a & ~b) or not (h[b] & ~h[a])
                   for a in range(N) for b in range(N))
        fixed = [a for a in range(N) if h[a] == a]
        # Its distinct fixed points are incomparable.
        assert all(a == b or ((a & ~b) and (b & ~a))
                   for a in fixed for b in fixed)
        checks += 1
print('Monotone maps:', len(maps))
print('Operator pairs checked:', checks)

# Check the Boolean identities behind the representative A join K.
# Here even positions code A and odd positions code K.
def join(a, b, n):
    return sum(((a >> i) & 1) << (2*i) |
               ((b >> i) & 1) << (2*i+1) for i in range(n))
for a in range(N):
    for k in range(N):
        assert (((1 << (2*n)) - 1) ^ join(a,k,n)) == join(mask ^ a,mask ^ k,n)
print('Join/complement identity checked on all 16 input pairs.')

# Exhaustively check that adding one unused leading or trailing block
# has the claimed semantic effect for a nonempty finite quantifier domain.
def quantify(vals, qs):
    vals = list(vals)
    for q in reversed(qs):
        vals = [(any if q == 'E' else all)(vals[i:i+2])
                for i in range(0, len(vals), 2)]
    return vals[0]
for qs in [('E',), ('A',), ('E','A'), ('A','E')]:
    for table in product((False, True), repeat=2**len(qs)):
        value = quantify(table, qs)
        for q in ('E','A'):
            assert quantify(table + table, (q,)+qs) == value
            expanded = [v for v in table for _ in range(2)]
            assert quantify(expanded, qs+(q,)) == value
print('All leading/trailing dummy-block checks passed (block lengths 1 and 2).')

```

[tool result]
```
Wrote scratchpad.py (54 lines).
```

## response 3
[tool call: run_scratchpad]

[tool result]
```
[exit code 0, 0.0s]
--- stdout ---
Monotone maps: 36
Operator pairs checked: 1296
Join/complement identity checked on all 16 input pairs.
All leading/trailing dummy-block checks passed (block lengths 1 and 2).

--- stderr ---
(empty)
```

## response 4
[message]
I can prove the exclusions and reduce the existence part to a precise \(\Pi^0_2\) construction, but I do not have a complete proof of that construction. Thus I cannot honestly claim a complete solution.

Here is the reduction, including the arithmetical boundary it establishes.

### 1. No \(\Sigma^0_2\) set can be a witness

Put
\[
K_A=\{e:e\in\Gamma_e(A)\},
\qquad A^\diamond=\overline{K_A}.
\]
Universality and the parameter theorem give
\[
K_A\equiv_e A.
\]
They also give, whenever \(B\leq_e A\),
\[
\overline B\leq_m A^\diamond. \tag{1}
\]
Indeed, if \(B=\Gamma_i(A)\), uniformly obtain an index \(h(i,x)\) for the operator that outputs all of \(\omega\) exactly when \(x\in\Gamma_i(X)\). Then
\[
x\notin B
\iff h(i,x)\notin\Gamma_{h(i,x)}(A).
\]

Consequently, **the skip of a cototal degree is total**. To see this, choose \(B\equiv_e A\) with \(B\leq_e\overline B\). By (1),
\[
A\leq_e B\leq_e\overline B\leq_e A^\diamond.
\]
Thus
\[
\overline{A^\diamond}=K_A\leq_e A\leq_e A^\diamond,
\]
so \(A^\diamond\) itself is a total set.

Now let \(K\) be an ordinary computably enumerable complete halting set, and put \(H=\overline K\). Every \(\Sigma^0_2\) set is enumeration reducible to \(H\). Explicitly, if
\[
x\in A\iff \exists u\,\forall v\,R(x,u,v)
\]
with \(R\) computable, choose a computable \(f\) such that
\[
f(x,u)\in K\iff \exists v\,\neg R(x,u,v).
\]
Then
\[
x\in A\iff \exists u\,[f(x,u)\in H],
\]
which is an enumeration reduction.

For such an \(A\), let \(B=A\oplus K\). Since \(K\) is c.e.,
\[
B\equiv_e A.
\]
Moreover,
\[
\overline B=\overline A\oplus H
\]
enumerates \(H\), hence \(A\), and it enumerates \(K\) without any oracle. Therefore
\[
B\leq_e\overline B.
\]
So every \(\Sigma^0_2\) degree is cototal, and its skip is total, hence cototal.

Because
\[
\Sigma^0_1\cup\Pi^0_1\subseteq\Sigma^0_2,
\]
this proves
\[
\boxed{\mathcal E\subseteq
\bigl(\{\Pi\}\times\{2,3,\ldots\}\bigr)
\ \cup\
\bigl(\{\Sigma\}\times\{3,4,\ldots\}\bigr).} \tag{2}
\]

### 2. Every \(\Pi^0_2\) degree is weakly cototal

Suppose \(A\in\Pi^0_2\), and again let \(B=A\oplus K\). We have \(B\equiv_e A\), while
\[
\overline B=\overline A\oplus H.
\]
Here \(\overline A\in\Sigma^0_2\), so \(\overline A\leq_e H\). Hence
\[
\overline B\equiv_e H.
\]
The set \(H\) is total because its complement \(K\) is c.e. Thus \(\mathbf d_e(\overline B)\) is total, proving that \(\mathbf d_e(A)\) is weakly cototal.

### 3. The exact missing existence statement

The following statement would turn (2) into equality:
\[
\boxed{\exists A\in\Pi^0_2\quad
\mathbf d_e(A^\diamond)\text{ is not cototal}.} \tag{*}
\]

Indeed, Section 2 would supply weak cototality automatically. Dummy quantifiers would then place the same witness in every \(\Pi^0_m\), \(m\geq2\), and every \(\Sigma^0_m\), \(m\geq3\).

Thus the proposed exact classification
\[
\mathcal E=
\bigl(\{\Pi\}\times\{2,3,\ldots\}\bigr)
\cup
\bigl(\{\Sigma\}\times\{3,4,\ldots\}\bigr)
\]
is **equivalent to \((*)\)**, given the arguments above. I have not proved \((*)\), so I am not presenting this equality as a proved answer.

### Python checks

I ran exhaustive finite checks of the join/complement identity and dummy-quantifier operations used above. These checks verify those finite identities, not the missing infinitary construction.

```python
from itertools import product

def join(a, b, n):
    return sum(
        (((a >> i) & 1) << (2*i))
        | (((b >> i) & 1) << (2*i + 1))
        for i in range(n)
    )

n = 2
mask = (1 << n) - 1
for a in range(1 << n):
    for b in range(1 << n):
        assert (
            ((1 << (2*n)) - 1) ^ join(a, b, n)
        ) == join(mask ^ a, mask ^ b, n)

def quantify(table, quantifiers):
    values = list(table)
    for q in reversed(quantifiers):
        operation = any if q == "E" else all
        values = [
            operation(values[i:i+2])
            for i in range(0, len(values), 2)
        ]
    return values[0]

for qs in [("E",), ("A",), ("E", "A"), ("A", "E")]:
    for table in product((False, True), repeat=2**len(qs)):
        original = quantify(table, qs)
        for q in ("E", "A"):
            # An unused leading variable.
            assert quantify(table + table, (q,) + qs) == original

            # An unused trailing variable.
            expanded = [value for value in table for _ in range(2)]
            assert quantify(expanded, qs + (q,)) == original

print("All checks passed.")
```

**Proved:** the exclusions in (2), weak cototality of every \(\Pi^0_2\) degree, and the reduction of the complete classification to \((*)\).

**Left:** a complete proof of the \(\Pi^0_2\) noncototal-skip existence theorem.

[user message]
Stopping isn't an option without proving the result

## response 5
[reasoning summary]
**Evaluating construction parameters**

I'm considering how to construct A as a product of all single requirements A_e, adding code so that S(A) aligns with joining S(A_e). Each H utilizes global other columns, but they might function as computable parameters. If those other columns in A_e are not computable, could their skips be zero? I'm thinking about how to manage S_e — while they are not fixed by H_e, could still total to zero when joined uniformly? If finite injury R_e reduces outcomes of S_e to zero, the uniform joint total might be higher. I might use uniform zero-approximation for other parts.

[message]
I found a way to address the missing construction. It uses a computable tree of intervals, with bounded-witness tests arranged so that membership in the final set remains \(\Pi^0_2\). I’ll check the interval identities and the recursion’s well-foundedness before presenting the proof.

[tool call: write_scratchpad]
content:
```
from itertools import product
from math import isqrt


def pair(a, b):
    return (a+b)*(a+b+1)//2+b


def unpair(z):
    w = (isqrt(8*z+1)-1)//2
    b = z-w*(w+1)//2
    return w-b, b


def decode(r):
    k = (r+1).bit_length()-1
    p = (1 << (k+1))-2-r
    assert 0 <= p < (1 << k)
    return k, p


# Check the numerical recursion measures and the reservoir partition.
for n in range(100000):
    tag = n % 3
    if tag == 0:
        j = n//3
        k, p = decode(j)
        assert k <= j
        assert k == 0 or k-1 < n
    elif tag == 1:
        t = n//3
        assert t < n
        assert t == 0 or t-1 < n
    else:
        j, t = unpair(n//3)
        assert 3*pair(j,t)+2 == n
        assert j < n and t < n
        k, p = decode(j)
        assert k == 0 or k-1 < n
print('100000 reservoir/rank checks passed')

# Finite interval model: k <= 2, seven positive children,
# two negative-reservoir coordinates, and seven diagonal markers.
K = 2
M = (1 << (K+1))-1
D = [1 << j for j in range(M)]
V = [1 << (M+t) for t in range(K)]
R = [1 << (M+K+j) for j in range(M)]
B, lower, upper = [], [], []
for r in range(M):
    k, p = decode(r)
    b = sum(V[t] for t in range(K) if t >= k or ((p >> t) & 1))
    b |= sum(R[j] for j in range(r+1, M))
    lo = b | sum(D[j] for j in range(r, M))
    B.append(b)
    lower.append(lo)
    upper.append(lo | R[r])

# An arbitrary negative-child set and an arbitrary set of positive tests.
# The only hypotheses used are the positive prefix gate and monotonicity
# within each fixed k-block.
models = 0
unions = 0
for a in range(1 << K):
    aneg = sum(V[t] for t in range(K) if (a >> t) & 1)
    for q in range(1 << M):
        valid = True
        for r in range(M):
            if not ((q >> r) & 1):
                continue
            k, p = decode(r)
            if p & ~a:
                valid = False
                break
            for s in range(M):
                ell, h = decode(s)
                if ell == k and not (p & ~h) and not (h & ~a):
                    assert not (B[r] & ~B[s])
                    if not ((q >> s) & 1):
                        valid = False
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
        for choices in range(1 << M):
            children = [lower[r] | (R[r] if ((choices >> r) & 1) else 0)
                        for r in range(M)]
            union = aneg
            for r in active:
                union |= children[r]
            assert union == (children[active[0]] if active else aneg)
            unions += 1
print(f'{models} admissible test models and {unions} child-union checks passed')

# Exhaustive finite checks of the Pi_2 conjunction/disjunction normal forms.
def pi2(table):
    return all(any(row) for row in table)

matrices = [((a,b),(c,d)) for a,b,c,d in product((False,True), repeat=4)]
for A, Bm in product(matrices, repeat=2):
    for use_or in (False, True):
        op = (lambda a,b: a or b) if use_or else (lambda a,b: a and b)
        lhs = op(pi2(A), pi2(Bm))
        rhs = all(any(op(A[u][v], Bm[w][z])
                      for v,z in product(range(2), repeat=2))
                  for u,w in product(range(2), repeat=2))
        assert lhs == rhs
print('512 Pi_2 finite-closure normal-form checks passed')

# Check antitonicity of Phi(complement Psi(.)) for all monotone
# maps P({0,1})->P({0,1}).
N = 4
maps = [f for f in product(range(N), repeat=N)
        if all((a & ~b) or not (f[a] & ~f[b])
               for a in range(N) for b in range(N))]
for phi, psi in product(maps, repeat=2):
    h = [phi[3 ^ psi[a]] for a in range(N)]
    assert all((a & ~b) or not (h[b] & ~h[a])
               for a in range(N) for b in range(N))
print(f'{len(maps)**2} antitonicity checks passed')

```

[tool result]
```
Wrote scratchpad.py (130 lines).
```

## response 6
[tool call: run_scratchpad]

[tool result]
```
[exit code 0, 0.1s]
--- stdout ---
100000 reservoir/rank checks passed
74 admissible test models and 9472 child-union checks passed
512 Pi_2 finite-closure normal-form checks passed
1296 antitonicity checks passed

--- stderr ---
(empty)
```

## response 7
[tool call: edit_scratchpad]
old_string:
```
print(f'{len(maps)**2} antitonicity checks passed')

```
new_string:
```
print(f'{len(maps)**2} antitonicity checks passed')

# Construct the finite positive Boolean Pi_2 formula DAGs.
# ('T', node, r) is the atomic Pi_2 bounded-witness test in the proof.
# All other leaves are obtained by strictly lower-rank recursion.
from functools import lru_cache
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
        return ('AND', ('T', node, r),
                tuple(child(-1, t) for t in range(k) if (p >> t) & 1))
    if n % 3 == 0:
        j = n//3
        return ('OR', tuple(Q(r) for r in range(j+1)))
    if n % 3 == 1:
        t = n//3
        return ('OR', child(-1,t),
                tuple(Q(r) for r in range((1 << (t+1))-1)))
    j,t = unpair(n//3)
    return ('OR', tuple(Q(r) for r in range(j)),
            ('AND', Q(j), child(j,t)))

for n in range(25):
    formula((),n)
print(f'Pi_2 formula DAGs for inputs 0..24 constructed; {calls} recursive nodes checked')

```

[tool result]
```
Edited scratchpad.py (1 replacement).
```

## response 8
[tool call: run_scratchpad]

[tool result]
```
[exit code 0, 0.1s]
--- stdout ---
100000 reservoir/rank checks passed
74 admissible test models and 9472 child-union checks passed
512 Pi_2 finite-closure normal-form checks passed
1296 antitonicity checks passed
Pi_2 formula DAGs for inputs 0..24 constructed; 52 recursive nodes checked

--- stderr ---
(empty)
```

## response 9
[message]
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

# agent_1: last reply

Put
\[
K_X=\{e:e\in\Gamma_e(X)\},
\]
so that \(X^\diamond=\overline{K_X}\). We prove
\[
\boxed{\mathcal E=\{(\Pi,m):m\ge2\}\cup\{(\Sigma,m):m\ge3\}.}
\]

The lower-bound construction below uses \(0'\), but the resulting set is parameter-free \(\Pi^0_2\). In particular, this is an effective construction, not a Baire-category existence argument.

## 1. Basic operator facts

We will use the following facts, including their uniform versions.

### Fact 1
For every \(X\),
\[
K_X\equiv_e X,\qquad \overline X\leq_m X^\diamond.
\]

Indeed, \(K_X\leq_e X\) is obtained by collecting the diagonal axioms:
\[
(e,F)\text{ is an axiom }\iff (e,F)\in W_e.
\]
For the converse, computably obtain an index \(g(n)\) for the operator that outputs all of \(\omega\) if its input contains \(n\), and outputs nothing otherwise. Then
\[
n\in X\iff g(n)\in K_X.
\]
Taking complements also proves the second assertion.

### Fact 2
If \(X\leq_e Y\), then \(X^\diamond\leq_m Y^\diamond\).

Suppose \(X=\Gamma_j(Y)\). Given \(e\), computably obtain an index \(f(e)\) for the operator which outputs all numbers exactly when
\[
e\in\Gamma_e(\Gamma_j(\text{input})).
\]
Consequently,
\[
e\in K_X\iff f(e)\in K_Y.
\]
Thus skip is well-defined on enumeration degrees.

### Fact 3
\[
\boxed{\mathbf d_e(X)\text{ is cototal}\iff X\leq_e X^\diamond.} \tag{1}
\]

For the forward implication, choose \(B\equiv_e X\) with \(B\leq_e\overline B\). Facts 1 and 2 give
\[
X\leq_e B\leq_e\overline B\leq_m B^\diamond\equiv_e X^\diamond.
\]

Conversely, if \(X\leq_e X^\diamond\), then
\[
K_X\leq_e X\leq_e X^\diamond=\overline{K_X}.
\]
Since \(K_X\equiv_e X\), this is a cototal representative of \(\mathbf d_e(X)\).

## 2. The exclusion: every \(\Sigma^0_2\) set has cototal skip

In fact, weak cototality is unnecessary for this half.

Let \(K=0'\), the ordinary halting set. Every \(\Sigma^0_2\) set is enumeration reducible to \(\overline K\). Explicitly, if
\[
x\in A\iff \exists u\,\forall v\,R(x,u,v)
\]
with \(R\) computable, the set
\[
H=\{(x,u):\forall v\,R(x,u,v)\}
\]
is co-c.e., hence many-one reducible to \(\overline K\), and \(A\) is its existential projection.

Also, uniformly for every \(X\),
\[
\overline K\leq_m X^\diamond. \tag{2}
\]
To see this, use operators which ignore their input and output all numbers precisely when a specified ordinary machine halts.

Therefore, if \(A\in\Sigma^0_2\) and \(C=A^\diamond\),
\[
\overline C=K_A\leq_e A\leq_e\overline K\leq_e C. \tag{3}
\]
In particular, \(C\oplus\overline C\equiv_e C\), and swapping the two tags reduces this join to its complement. Thus \(\mathbf d_e(C)\) is cototal.

This excludes every \(\Sigma^0_1\) and \(\Sigma^0_2\) set, and also every \(\Pi^0_1\) set because \(\Pi^0_1\subseteq\Sigma^0_2\).

## 3. The construction for the lower bound

We construct \(D\) c.e. in \(K\) such that, for \(A=\overline D\),

1. \(\mathbf d_e(D)\) is total;
2. writing \(C=A^\diamond\),
   \[
   C\ne\Gamma_e(C^\diamond)\quad\text{for every }e. \tag{4}
   \]

Then \(A\in\Pi^0_2\), its degree is weakly cototal, and (1) and (4) imply that \(\mathbf d_e(A^\diamond)\) is not cototal.

The important device is **conditional refutation**: a candidate may be rejected using a computable set larger than the final \(A\). Its refutation is required to become valid only in the case that all candidates at that node are rejected. This permits fixed, genuinely c.e. control operators.

### 3.1 Coding total information into \(D\)

Computably divide \(\omega\) into a coding domain and a working domain.

The coding domain has coordinates
\[
(n,b,k),\qquad n,k\in\omega,\quad b\in\{0,1\}.
\]
We put coding points into \(D\) only when
\[
b=\chi_K(n),
\]
and eventually put at least one such point into \(D\) for every \(n\).

Let
\[
T=\{(n,\chi_K(n)):n\in\omega\}.
\]
This is a total set, equivalent to \(K\oplus\overline K\). Projection of coding points gives
\[
T\leq_e D. \tag{5}
\]
All of \(D\) will be c.e. in \(K\), so
\[
D\leq_e T. \tag{6}
\]
Here we use the elementary fact that any \(K\)-oracle enumeration can be compiled into an enumeration operator with oracle \(K\oplus\overline K\): a finite oracle computation has a finite positive certificate in that total oracle.

Thus (5) and (6) will make \(\mathbf d_e(D)\) total.

### 3.2 Working regions and fixed control indices

Nodes are finite strings over
\[
\{\infty\}\cup\omega.
\]
The working domain has coordinates \((\sigma,k)\), where \(\sigma\) is a node and \(k\in\omega\). Set
\[
\begin{aligned}
B_\sigma&=\{(\sigma,k):k\in\omega\},\\
P_\sigma&=\{(\tau,k):\sigma\preceq\tau\},\\
L_\sigma&=B_\sigma\cup\bigcup_{j\in\omega}P_{\sigma^\frown j}
          =P_\sigma\setminus P_{\sigma^\frown\infty}.
\end{aligned}
\]
All these sets are uniformly computable. Partition each \(B_\sigma\) into uniformly computable infinite sets
\[
B_\sigma=\bigsqcup_{j\in\omega}R_{\sigma,j}.
\]

Computably choose \(x_\sigma\) such that
\[
\Gamma_{x_\sigma}(X)=
\begin{cases}
\omega,&X\cap B_\sigma\ne\varnothing,\\
\varnothing,&X\cap B_\sigma=\varnothing.
\end{cases}
\]
These are ordinary enumeration operators: enumerate \((u,\{p\})\) for every \(u\) and every \(p\in B_\sigma\). Hence
\[
\boxed{x_\sigma\in C\iff B_\sigma\subseteq D.} \tag{7}
\]
No oracle-dependent enumeration of control axioms is involved.

Define the uniformly computable set
\[
Z_\sigma=
\bigcup\left\{
L_\rho:
\rho\prec\sigma\text{ and the next symbol of }\sigma\text{ after }\rho
\text{ is }\infty
\right\}. \tag{8}
\]
Along the eventual true path, \(Z_\sigma\) will be contained in \(D\).

A node \(\sigma\) of length \(e\) works against \(\Gamma_e\).

### 3.3 Candidates and positive restraints

Fix a computable listing \((G_j)\) of all finite sets.

At node \(\sigma\), a candidate \(j\) becomes available when
\[
(x_\sigma,G_j)\in W_e,\qquad e=|\sigma|.
\]
There is at most one active candidate. Rejected candidates are recorded permanently and never activated again.

To make \(G_j\subseteq C^\diamond\), we must ensure, for every \(y\in G_j\) and every axiom \((y,H)\in W_y\), that
\[
H\cap K_A\ne\varnothing. \tag{9}
\]
Indeed, (9) says \(y\notin\Gamma_y(C)\), or \(y\in C^\diamond\).

We meet (9) by protecting finite positive witnesses: if
\[
(z,F)\in W_z,\qquad F\subseteq A,
\]
then preserving \(F\) inside \(A\) ensures \(z\in K_A\).

At any finite construction stage only finitely many finite sets are protected. Protections belonging to a paused \(\infty\)-subtree are retained, not discarded.

### 3.4 Planned whole-set enumerations

We allow declarations putting a whole computable region into \(D\). At any finite stage, the **planned** set \(D_s\) is a finite union of computable regions and finitely many points. It is therefore computable, uniformly from its finite stage parameters.

Each declared region is enumerated into the actual \(K\)-c.e. set by dovetailing. The union of the planned sets equals the set actually enumerated.

Write
\[
A_s=\omega\setminus D_s.
\]
For any computable \(Q\), membership in \(K_Q\) is decidable by \(K\): search for a finite \(Q\)-witness. Thus all the decisions below are \(K\)-effective.

### 3.5 The action at a node

At a visit to \(\sigma\), first activate the least available unrejected candidate if there is no active candidate.

Suppose \(j\) is active. Fairly process one as-yet-unprocessed obligation
\[
y\in G_j,\qquad (y,H)\in W_y.
\]
Use the computable test set
\[
Q=A_s\setminus\bigl(Z_\sigma\cup B_\sigma
                         \cup P_{\sigma^\frown j}\bigr). \tag{10}
\]

Using \(K\), decide whether
\[
H\cap K_Q\ne\varnothing. \tag{11}
\]

* If (11) holds, find \(z\in H\) and a finite \(F\subseteq Q\) with
  \((z,F)\in W_z\), and protect \(F\).
* If (11) fails:
  1. release this candidate’s protections and all protections owned by nodes extending \(\sigma^\frown j\);
  2. declare
     \[
     R_{\sigma,j}\cup P_{\sigma^\frown j}\subseteq D;
     \]
  3. mark \(j\) rejected;
  4. take outcome \(\infty\).

If the active candidate is not rejected, take outcome \(j\), even when no new obligation is currently available.

If there is no active candidate, take outcome \(\infty\).

Whenever outcome \(\infty\) is taken, additionally put into \(D\) all points of \(L_\sigma\) whose global codes are at most the current stage number. Then visit the \(\infty\)-child. When outcome \(j\) is taken, visit the \(j\)-child.

**Background enumeration into \(L_\sigma\) occurs only at \(\infty\)-visits.** In particular, it stops if a candidate survives forever.

At global stage \(s\), start at the root and make at most \(s+1\) recursive node visits. Queues of available candidates and obligations are handled fairly using the ordinary c.e. approximations through stage \(s\).

Finally, satisfy coding requirement \(n=s\): choose
\[
(n,\chi_K(n),k)
\]
outside every currently protected finite set and put it into \(D\). Such a \(k\) exists because only finitely many points are protected.

This completes the construction.

## 4. Verification of the construction

### 4.1 No retained positive protection is destroyed

Every new protection at \(\sigma\), while candidate \(j\) is active, is disjoint from
\[
D_s\cup Z_\sigma\cup B_\sigma\cup P_{\sigma^\frown j}. \tag{12}
\]

We verify inductively that subsequent enumerations into \(D\) avoid every protection that has not explicitly been released.

Consider an action at a visited node \(\sigma\). Its working-domain deletions lie in \(L_\sigma\).

* **Protections owned by ancestors.**  
  If an ancestor is being followed through a finite outcome \(j\), its protections avoid the whole corresponding child region, including the action at \(\sigma\). If it is being followed through \(\infty\), its current candidate protections have already been released.

* **Protections owned by descendants.**  
  On a refutation, all protections in the deleted finite-child subtree are released first. Retained protections in the \(\infty\)-subtree avoid \(L_\sigma\), because \(L_\sigma\) is included in their \(Z\)-set. At an idle \(\infty\)-visit, no finite-child subtree has retained protections.

* **Protections owned by incomparable nodes.**  
  At their longest common ancestor, the only possible retained case is that the protection’s owner lies in the \(\infty\)-subtree and the current action lies in a finite-child subtree. The former protection’s \(Z\)-set contains that entire finite-child region. The reverse configuration cannot have a retained finite-child protection: it was released when that candidate was rejected.

These cases also show that declaring \(R_{\sigma,j}\cup P_{\sigma^\frown j}\subseteq D\) is safe after the indicated releases. Coding points are explicitly chosen outside all retained protections.

Consequently, any protection that is never released is contained in the final \(A\).

### 4.2 Effectiveness and weak cototality

Each stage is effective in \(K\), including the tests (11). Thus \(D\) is c.e. in \(K\), so \(D\in\Sigma^0_2\) and
\[
A=\overline D\in\Pi^0_2.
\]
This is parameter-free: a \(K\)-oracle enumeration has a \(\Sigma^0_2\) description by quantifying over finite computations and the correctness of their finitely many oracle answers.

The coding requirements establish (5), while \(D\) being c.e. in \(K\) establishes (6). Therefore \(\mathbf d_e(\overline A)=\mathbf d_e(D)\) is total, and \(\mathbf d_e(A)\) is weakly cototal.

### 4.3 The true path

Starting at the root, recursively choose a child of every infinitely visited node as follows.

* If it has infinitely many \(\infty\)-visits, choose its \(\infty\)-child.
* Otherwise, one candidate \(j\) is eventually active forever; choose its \(j\)-child.

The chosen child is visited infinitely often. This gives a node of every finite length.

If \(\sigma\) takes true outcome \(\infty\), its unbounded background enumerations give
\[
L_\sigma\subseteq D. \tag{13}
\]
It follows from (8) that every true-path node satisfies
\[
Z_\sigma\subseteq D. \tag{14}
\]

### 4.4 Diagonalization at a true-path node

Let \(\sigma\) be the true-path node of length \(e\).

#### Case I: a candidate \(j\) survives forever

Every obligation for \(G_j\) is eventually processed. Its protected witnesses are never released, so by §4.1 they lie in \(A\). Therefore (9) holds for every relevant \(y,H\), giving
\[
G_j\subseteq C^\diamond.
\]
Since \((x_\sigma,G_j)\in W_e\),
\[
x_\sigma\in\Gamma_e(C^\diamond). \tag{15}
\]

On the other hand, \(R_{\sigma,j}\) retains an infinite tail in \(A\). Before activation it suffered only finitely many background cuts; it was not previously rejected; the node’s background stops while \(j\) remains active. True-path ancestors never delete its entire region, and descendant actions do not touch its bank. Thus \(B_\sigma\not\subseteq D\), and (7) gives
\[
x_\sigma\notin C. \tag{16}
\]
Equations (15)–(16) give the required inequality.

#### Case II: the true outcome is \(\infty\)

Every available candidate is eventually activated and rejected. By (13),
\[
B_\sigma\subseteq D,
\]
so \(x_\sigma\in C\).

Consider a rejected candidate \(j\). Its rejection supplied \(y\in G_j\) and \((y,H)\in W_y\) such that
\[
H\cap K_Q=\varnothing
\]
for the test set (10) at that rejection stage.

In the final construction,
\[
A\subseteq Q:
\]
\(A\subseteq A_s\) by monotonicity; \(Z_\sigma\subseteq D\) by (14); \(B_\sigma\subseteq D\) in this case; and \(P_{\sigma^\frown j}\) was declared a subset of \(D\) on rejection. Hence
\[
H\cap K_A=\varnothing,
\qquad\text{so }H\subseteq C.
\]
The axiom \((y,H)\in W_y\) now implies \(y\notin C^\diamond\). Thus \(G_j\not\subseteq C^\diamond\).

Every candidate is invalid, and therefore
\[
x_\sigma\notin\Gamma_e(C^\diamond),
\]
whereas \(x_\sigma\in C\).

Both cases prove
\[
C\ne\Gamma_e(C^\diamond).
\]
There is a true-path node of every length, so this holds for all \(e\). By (1), \(\mathbf d_e(C)\) is not cototal.

This proves the required \(\Pi^0_2\) existence theorem.

## 5. Determining all labels and levels

The constructed \(A\) belongs to every \(\Pi^0_m\) for \(m\ge2\), and to every \(\Sigma^0_m\) for \(m\ge3\), by dummy quantifier blocks.

Section 2 excludes \(\Sigma^0_1,\Sigma^0_2\), and \(\Pi^0_1\). Consequently,
\[
\boxed{\mathcal E=\{(\Pi,m):m\ge2\}\cup\{(\Sigma,m):m\ge3\}.}
\]

## 6. Executable checks

The following self-contained Python checks the finite algebraic identities used in the upper proof and exhaustively checks the restraint-preservation geometry on the depth-four tree with outcomes \(\{\infty,0,1\}\).

The tree check considers all compatible configurations of a visited node and an owner of a retained protection. It verifies that every proposed deletion lies in that owner’s required exclusion set. It overestimates a rejected candidate’s bank deletion by deleting the whole bank, making the safety test stronger.

These checks do not purport to execute \(0'\) or replace the infinite true-path proof above.

```python
from itertools import product

def upper_checks():
    U = set(range(2))
    subsets = [
        frozenset(x for x in U if m >> x & 1)
        for m in range(4)
    ]
    normal = diagonal = joins = 0

    # Existential projection of a universal predicate.
    for bits in product((0, 1), repeat=8):
        R = dict(zip(product(U, repeat=3), bits))
        H = {
            (x, u) for x, u in product(U, repeat=2)
            if all(R[x, u, v] for v in U)
        }
        A = {
            x for x in U
            if any(all(R[x, u, v] for v in U) for u in U)
        }
        assert A == {x for x, u in H}
        normal += 1

    # Exhaust all enumeration-operator tables on two-point oracles.
    axioms = list(product(U, subsets))
    rows = [
        [a for k, a in enumerate(axioms) if m >> k & 1]
        for m in range(256)
    ]

    def image(row, A):
        return {x for x, F in row if F <= A}

    # Flattening the diagonal gives K_A <=e A.
    for r0, r1 in product(rows, repeat=2):
        rs = [r0, r1]
        flat = [
            (i, F) for i in U
            for x, F in rs[i] if x == i
        ]
        for A in subsets:
            assert image(flat, A) == {
                i for i in U if i in image(rs[i], A)
            }
            diagonal += 1

    # Tagged join with the complement is self-complementary.
    for A, row in product(subsets, rows):
        if image(row, A) == U - A:
            T = {(0, x) for x in A} | {
                (1, x) for x in U - A
            }
            assert {
                (1 - b, x)
                for b, x in set(product(U, U)) - T
            } == T
            joins += 1

    return normal, diagonal, joins


def tree_checks(depth=4):
    INF = -1
    outcomes = (INF, 0, 1)
    nodes = [
        s for d in range(depth + 1)
        for s in product(outcomes, repeat=d)
    ]
    U = set(nodes)  # One representative per bank suffices here.

    def pref(a, b):
        return b[:len(a)] == a

    def region(s):
        return {t for t in U if pref(s, t)}

    def body(s):
        return {s} | set().union(
            *(region(s + (j,)) for j in (0, 1))
        )

    def Z(s):
        return set().union(*(
            body(s[:i])
            for i, x in enumerate(s) if x == INF
        ))

    def exclusion(s, j):
        return Z(s) | {s} | region(s + (j,))

    def merge(c, k, v):
        if k in c and c[k] != v:
            return False
        c[k] = v
        return True

    bg = failures = 0

    for s in nodes:
        if len(s) >= depth:
            continue

        assert body(s).isdisjoint(region(s + (INF,)))
        assert body(s) | region(s + (INF,)) == region(s)

        for failure in (False, True):
            for j in ((0, 1) if failure else (None,)):
                # Outcomes necessary for the current visit.
                current = {
                    s[:i]: (None if x == INF else x)
                    for i, x in enumerate(s)
                }
                current[s] = j

                # Whole-bank deletion overestimates R_{s,j}.
                deleted = (
                    {s} | region(s + (j,))
                    if failure else body(s)
                )

                for t in nodes:
                    # These protections are explicitly released.
                    if t == s:
                        continue
                    if failure and pref(s + (j,), t):
                        continue

                    for k in (0, 1):
                        c = dict(current)
                        possible = merge(c, t, k)

                        # A retained finite-child protection requires
                        # its parent's finite candidate still active.
                        for i, x in enumerate(t):
                            if x != INF:
                                possible = (
                                    merge(c, t[:i], x) and possible
                                )

                        if possible:
                            assert deleted <= exclusion(t, k)
                            if failure:
                                failures += 1
                            else:
                                bg += 1

    for t in nodes:
        for i, x in enumerate(t):
            if x == INF:
                assert body(t[:i]) <= Z(t)

    return len(nodes), bg, failures


if __name__ == "__main__":
    print("upper:", upper_checks())
    print("tree:", tree_checks())
```

Actual output:
```text
upper: (256, 262144, 161)
tree: (121, 3200, 6400)
```

# agent_2: last reply

Completed my assigned components:

- Proved every \(\Sigma^0_2\) set has a total—and therefore cototal—skip.
- Proved \(\mathbf d_e(X)\) is cototal iff \(X\leq_e X^\diamond\).
- Verified the lower construction’s restraint preservation and infinite true-path argument, including effectiveness and weak cototality coding.
- Wrote and executed exhaustive finite checks in:
  - `workspace/agent2_order_checks.py`
  - `workspace/agent2_tree_checks.py`

The team’s proof is complete; agent_1 is assembling the full solution and runnable verification code.

# agent_3: last reply

Completed my assigned work:

- Proved the stronger upper bound: **every \(\Sigma_2^0\) set has a skip whose degree is total**, hence cototal.
- Developed the fixed-bank conditional-refutation mechanism resolving the lower construction’s ordinary-c.e. indexing obstacle.
- Independently audited the complete lower construction, including effectiveness, restraint preservation, and true-path verification.
- Wrote and executed finite exhaustive checks in:
  - `workspace/agent3_upper_checks.py`
  - `workspace/agent3_tree_checks.py`
- Independently reran all five teammates’ checking modules; every assertion passed.

The team’s proof is complete. Agent 1 is assembling the final proof and self-contained Python checks.

# agent_4: last reply

Independent audit of the repaired lower construction is complete.

The construction uses fixed computable banks \(B_\sigma\), so its skip indices are genuinely ordinary effective indices—not \(0'\)-dependent axioms. The conditional-refutation tree handles infinite restraints, with background deletion restricted to \(\infty\)-visits. The true-path argument establishes a \(\Pi^0_2\) set \(A\) satisfying
\[
\overline A\equiv_e T(0')
\quad\text{and}\quad
A^\diamond\not\leq_e A^{\diamond\diamond}.
\]
Thus \(A\) is weakly cototal, while \(A^\diamond\) is not cototal, using
\[
\mathbf d_e(X)\text{ cototal}\iff X\leq_e X^\diamond.
\]

The upper half proves that every \(\Sigma^0_2\) set has total skip. Hierarchy padding therefore gives exactly
\[
\boxed{\mathcal E=\{(\Pi,m):m\ge2\}\cup\{(\Sigma,m):m\ge3\}.}
\]

My executable dynamic restraint check, `workspace/agent4_tree_checks.py`, passed 400,000 node-action safety assertions. The lead has the complete proof outline and all independent audits for assembly.
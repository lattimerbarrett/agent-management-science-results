#1 agent_1: Put \(h=g-1\). The answer is independent of the curve, including its genus:
\[
\boxed{\displaystyle
\mathcal E_X=\{(n,\star):n\geq4,\quad
\star\in\{\mathrm{Hod},\mathrm{Dol},\mathrm{dR}\}\}.}
\]

An important point in the proof is that an incidence in the Dolbeault fiber does not, by itself, imply an incidence in the de Rham fiber. We prove the latter using a deformation calculation.

## 1. Full-chain components and their dimensions

Write \(d_i=\deg L_i\), and put
\[
m_i=2h+d_{i+1}-d_i.
\]
A degree vector \(d=(d_1,\ldots,d_n)\) occurs for a stable full chain precisely when
\[
\sum_i d_i=0,\qquad m_i\geq0,\qquad
\sum_{i=1}^j d_i>0\quad(1\leq j<n).                    \tag{1}
\]
Indeed, over the function field a full chain is a single nilpotent Jordan block. Its invariant subspaces are the tails. Thus stability is exactly the last set of inequalities.

For a vector satisfying (1), the corresponding fixed locus is
\[
P_d\cong
\operatorname{Pic}^{d_1}(X)\times
\prod_{i=1}^{n-1}\operatorname{Sym}^{m_i}(X).           \tag{2}
\]
Explicitly, choose \(L_1\) and effective divisors \(D_i\) of degrees \(m_i\), and set
\[
L_{i+1}=L_iK_X^{-1}(D_i).
\]
The nonzero maps are then determined up to the automorphisms of the line bundles.

In particular, \(P_d\) is connected and proper, and
\[
\dim P_d=g+\sum_i m_i
       =g+2h(n-1)+d_n-d_1.                            \tag{3}
\]
It is a component of the **full** fixed locus. To justify this last assertion, in the stable fixed locus the ranks and weights of the Hodge decomposition are locally constant. Consequently, (2) is open there. It is also proper, hence closed in the full fixed locus. Since the stable locus is open, it is open and closed in the full fixed locus.

Let
\[
N=n^2h+1.
\]
The standard attracting-set dimension formulas are
\[
\begin{aligned}
\dim S_{P_d}^{\mathrm{Dol}}
 &=N+\dim P_d,\\
\dim S_{P_d}^{\mathrm{dR}}
 &=N+\dim P_d,\\
\dim S_{P_d}^{\mathrm{Hod}}
 &=N+\dim P_d+1.                                     \tag{4}
\end{aligned}
\]
Here all three attracting sets are irreducible.

For completeness, these statements follow from the smooth stable locus and the Białynicki–Birula theorem. An object with stable limit is itself stable. The Dolbeault tangent space has dimension \(2N\), and its symplectic form has weight one. The tangent weights pair as \(w,1-w\), so there are exactly \(N\) positive weights. In Hodge moduli there is one additional positive direction, namely \(\lambda\), of weight one. On an attracting affine fiber, \(\lambda\) is a nonzero linear coordinate among the weight-one coordinates. Its fibers therefore have the asserted dimensions and are irreducible.

It follows from (3)–(4) that
\[
\dim S_{P_d}^{\star}=\dim S_{P_e}^{\star}
\quad\Longleftrightarrow\quad
d_1-d_n=e_1-e_n.                                    \tag{5}
\]

We will also use the following elementary observation.

**Equal-dimension observation.** If two distinct irreducible locally closed sets have the same dimension, neither can be contained in the closure of the other.

Otherwise their closures would be the same irreducible variety, and the two locally closed sets would contain disjoint dense open subsets of that variety. Thus, in our constructions, once a nonempty incidence is established, its being proper follows automatically.

## 2. Why ranks two and three are excluded

We recall the weight test for attracting sets.

**Weight test.** Let a quasiprojective variety have a linearized ample line bundle, and let \(P,Q\) be distinct proper fixed components. If the line bundle has the same weight on \(P\) and \(Q\), then
\[
\overline{S_P}\cap S_Q=\varnothing.                  \tag{6}
\]

To see this, take an equivariant projective embedding given by a power of the line bundle. Points attracted to \(P\) have a specified lowest nonzero weight coordinate. On the open set where this weight coordinate is nonzero, projection to its weight space sends \(S_P\) to \(P\). Since \(P\) is proper, the same holds on its closure. A point attracted to a different component of the same weight cannot belong to that closure.

For Hodge moduli, the determinant-of-cohomology GIT polarization has, at a full chain, weight
\[
A+B\sum_{i=1}^n(i-1)d_i,\qquad B\ne0,               \tag{7}
\]
where \(A,B\) do not depend on \(d\). One can calculate this directly using a scalar-invariant determinant line
\[
\bigl(\det R\Gamma(V\otimes A_0)\bigr)^{\otimes n}
\otimes
(\det V_x)^{-\chi(V\otimes A_0)}.
\]
Give \(L_i\) weight \(i-1\). The terms involving \(\deg A_0+1-g\) cancel, leaving
\(n\sum(i-1)d_i\), up to the choice of the ample dual and a positive power. This is the usual determinant polarization in the Quot construction, also for the family of \(\lambda\)-connections.

In rank two, equality in (5) determines the entire degree vector. By (2), there cannot be distinct components of that degree vector.

In rank three,
\[
2d_1+d_2=d_1-d_3,
\]
so equality in (5) implies equality of the weights in (7). The weight test excludes incidence in Hodge moduli.

It also excludes incidence in either fiber: a fiberwise closure is contained in the closure in Hodge moduli. We have proved
\[
(n,\star)\notin\mathcal E_X\qquad(n=2,3).             \tag{8}
\]

## 3. The components used in every rank at least four

Fix \(n\geq4\), and take
\[
q=(1,1,\underbrace{0,\ldots,0}_{n-4},-1,-1).
\]
Set
\[
p=q-e_2+e_3.                                       \tag{9}
\]
Both vectors satisfy (1). Only the second prefix sum changes, from two to one.

Their arrow degrees satisfy
\[
m(p)=m(q)+(-1,2,-1,0,\ldots,0).                     \tag{10}
\]
The first and third entries of \(m(q)\) are positive. In particular, the right side is nonnegative. The endpoints in (9) are unchanged, so
\[
\dim S_{P_p}^{\star}=\dim S_{P_q}^{\star}
\quad\text{for all three }\star.                    \tag{11}
\]

Choose a point \(x\in X\). We choose a chain in \(P_q\) with these extra properties:
\[
\begin{array}{ll}
\theta_1\text{ vanishes simply at }x,&
L_2L_1^{-1}\not\cong\mathcal O_X,\\
\theta_2(x)\ne0,&
\theta_3\text{ vanishes simply at }x.               \tag{12}
\end{array}
\]
These choices are possible on every curve in the question.

Indeed, \(m_1(q)=2h\). Choose an effective divisor \(D_1\) of degree \(2h\), containing \(x\) simply, such that
\[
\mathcal O_X(D_1)\not\cong K_X.
\]
Such divisors exist because the Abel map on divisors containing \(x\) is not constant. Then
\[
L_2L_1^{-1}=K_X^{-1}(D_1)
\]
is a nontrivial degree-zero line bundle. Choose \(D_2\) avoiding \(x\), and \(D_3\) containing \(x\) simply. Their required degrees are nonnegative, and the degree of \(D_3\) is positive. All remaining divisors are arbitrary.

Denote this chain by \(Q_0\).

## 4. The Dolbeault incidence

Inside the bundle of \(Q_0\), replace \(L_2\) by \(L_2(-x)\). Call the resulting bundle \(W\), and denote its induced Higgs field by \(\phi\).

The Higgs field preserves \(W\), by the first condition in (12). Locally at \(x\), the second and third arrows of \(W\) vanish. Thus \(\phi(x)\) is zero on the plane
\[
U=L_2(-x)_x\oplus L_{3,x}.
\]
For each line \(\ell\subset U\), take the upper elementary modification
\[
W\subset E_\ell\subset W(x),\qquad E_\ell/W=\ell.
\]
Because \(\phi(x)\ell=0\), the Higgs field extends holomorphically to \(E_\ell\).

Let \(e_2,e_3\) be bases for the two summands of \(U\), and put
\[
\ell_t=\mathbb C(e_2+t e_3).
\]
For \(t=0\), the modified Higgs bundle is \(Q_0\). For \(t\ne0\), the natural saturated full filtration has degree vector \(p\). Its graded arrow divisors are
\[
D_1-x,\qquad D_2+2x,\qquad D_3-x,\qquad D_4,\ldots.
\]
They are all effective and all arrows are nonzero. Its associated graded is therefore a stable full chain in \(P_p\). Consequently,
\[
(E_{\ell_t},\phi)\in S_{P_p}^{\mathrm{Dol}}\quad(t\ne0),
\qquad
(E_{\ell_0},\phi)=Q_0\in P_q.
\]
Hence
\[
Q_0\in
\overline{S_{P_p}^{\mathrm{Dol}}}\cap S_{P_q}^{\mathrm{Dol}}.       \tag{13}
\]

The same point gives an incidence in Hodge moduli. Together with (11) and the equal-dimension observation, this proves the required statement for \(\mathrm{Dol}\) and \(\mathrm{Hod}\).

## 5. Deforming the incidence to nonzero \(\lambda\)

Here is the deformation calculation needed for the de Rham fiber.

### 5.1 Local equations

Use a coordinate \(z\) at \(x\) and a flag-compatible frame of \(W\), fixed modulo \(z^2\). On the plane with basis \(e_2,e_3\), write
\[
\ell_t=\mathbb C(e_2+t e_3).
\]
Consider logarithmic \(\lambda\)-connections on \(W\), with residue
\[
R_{\lambda,t}
=\lambda(e_2+t e_3)e_2^*.                            \tag{14}
\]
Thus
\[
R_{\lambda,t}^2=\lambda R_{\lambda,t},\qquad
\operatorname{tr}R_{\lambda,t}=\lambda,\qquad
R_{\lambda,t}\ell_t=\lambda\ell_t.
\]

Require the following:

* the connection matrix is upper Hessenberg, i.e. it satisfies Griffiths transversality for the full filtration of \(W\);
* its third subdiagonal symbol vanishes at \(x\);
* if its local matrix is
  \[
  \lambda d+\left(\frac{R_{\lambda,t}}z+M_0+O(z)\right)dz,
  \]
  then
  \[
  M_0\ell_t\subset\ell_t.                           \tag{15}
  \]

These are algebraic conditions. More explicitly, the restrictions on \(M_0\) are
\[
(M_0)_{43}=0,\quad
(M_0)_{12}+t(M_0)_{13}=0,
\]
\[
(M_0)_{32}+t(M_0)_{33}
-t(M_0)_{22}-t^2(M_0)_{23}=0.                       \tag{16}
\]
Their ranks are constant near \(t=0\).

Conditions (14)–(15) say exactly that the connection extends holomorphically to the upper modification \(E_{\ell_t}\). Indeed, in the modified lattice the additional generator is \((e_2+t e_3)/z\). Its double pole cancels because \(R_{\lambda,t}\ell_t=\lambda\ell_t\), and its remaining complementary simple pole vanishes precisely by (15).

The vanishing of the third symbol ensures Griffiths transversality for the induced filtrations on \(E_{\ell_t}\).

### 5.2 The obstruction group

We verify that the above local conditions admit simultaneous global deformations in \(\lambda\) and \(t\).

The auxiliary Higgs bundle \((W,\phi)\) has degree \(-1\) and is stable. Its invariant tails have negative integral degrees, so their slopes are strictly below \(-1/n\).

Write \(W=\bigoplus M_i\), where
\[
M_2=L_2(-x),\qquad M_i=L_i\quad(i\ne2).
\]
Let \(\mathcal A\) be the sheaf of upper-triangular endomorphisms. With the frame fixed modulo \(z^2\), the infinitesimal automorphism sheaf is
\[
\mathcal A(-2x).
\]
At \((\lambda,t)=(0,0)\), the homogeneous connection variations form the sheaf \(\mathcal B\) of upper-Hessenberg \(K_X\)-valued matrices, with the additional requirements that the entries
\[
(1,2),\quad(3,2),\quad(4,3)                          \tag{17}
\]
vanish at \(x\).

The deformation complex is therefore
\[
\mathcal C^\bullet:
\mathcal A(-2x)\xrightarrow{[\phi,\;]}
\mathcal B.                                         \tag{18}
\]
As usual, a Čech lifting calculation places the obstruction to extending a deformation across a square-zero thickening in
\(\mathbb H^2(\mathcal C^\bullet)\). The local conditions themselves are unobstructed because (16) has constant rank.

We claim
\[
\mathbb H^2(\mathcal C^\bullet)\cong\mathbb C,
\quad\text{and trace induces this isomorphism}.       \tag{19}
\]

Here are the details. By Serre duality, a dual obstruction is represented by a section \(f\) of \(\mathcal B^*\otimes K_X\), with the commutator condition dual to (18).

For ordinary upper-Hessenberg matrices, such an \(f\) is represented by a lower-triangular matrix together with its first upper diagonal. The three conditions (17) additionally permit simple poles in the transposed positions
\[
(2,1),\quad(2,3),\quad(3,4).
\]
The first of these cannot occur:
\[
H^0\!\left(\operatorname{Hom}(M_1,M_2)(x)\right)
=
H^0(L_2L_1^{-1})=0                                 \tag{20}
\]
by (12).

Let \(f_i\) denote the entries on the first upper diagonal and let \(\phi_i\) be the nonzero subdiagonal arrows of \(\phi\). The diagonal commutator equations are, successively,
\[
\phi_1f_1=0,\quad
\phi_2f_2-\phi_1f_1=0,\quad\ldots,\quad
-\phi_{n-1}f_{n-1}=0.
\]
Thus all \(f_i\) vanish, including the permitted meromorphic ones. What remains is an actual holomorphic lower-triangular endomorphism commuting with \(\phi\). Stability of \((W,\phi)\) makes it scalar. Conversely, scalar endomorphisms give the trace obstruction. This proves (19). Fixing the determinant and determinant connection removes it.

There is no determinant obstruction to the prescribed residues: \(\deg W=-1\), and
\(\operatorname{tr}R_{\lambda,t}=\lambda\). A line bundle of degree \(-1\) has a logarithmic connection with one residue \(1\); multiplying by \(\lambda\) supplies the required determinant \(\lambda\)-connection. This is the degree–residue criterion.

We conclude that the moduli problem defined by (14)–(16), with fixed determinant connection, is smooth over the \((\lambda,t)\)-plane at our point.

### 5.3 The resulting de Rham boundary

On the axis \(\lambda=0\), the constant Higgs bundle \((W,\phi)\), with the varying lines \(\ell_t\), is already a family satisfying all the conditions. Smoothness extends it, étale locally, to a two-parameter algebraic family. One may see this directly by taking étale coordinates for a smooth morphism and extending the coordinates of the given section on \(\lambda=0\).

Upper modification gives a family of holomorphic \(\lambda\)-connections on \(E_{\ell_t}\).

* Along \(t=0\), its full filtration has degree vector \(q\).
* Along \(t\ne0\), it has degree vector \(p\).
* Nonvanishing of all graded arrows is open. It holds on the original Higgs family, and hence on the needed dense open part of the two-parameter family.

Consequently, for a general nonzero value \(a\) of \(\lambda\), a point of \(S_{P_q}^{\lambda=a}\) is a limit, in that same fiber, of points of \(S_{P_p}^{\lambda=a}\). Scaling the connection by \(a^{-1}\) identifies this fiber with the de Rham fiber. Therefore
\[
\overline{S_{P_p}^{\mathrm{dR}}}
\cap S_{P_q}^{\mathrm{dR}}\ne\varnothing.              \tag{21}
\]
By (11) and irreducibility, this intersection is proper.

This finishes the existence proof in every rank \(n\geq4\), in all three indicated moduli spaces.

## 6. Python verification

The geometric ingredients above are the Białynicki–Birula theorem, determinant-of-cohomology polarization, and deformation theory on a curve. The following code checks the algebraic calculations used in applying them:

* the local residue and elementary-modification equations;
* the three exceptional entries in the dual obstruction calculation;
* the full rank of the diagonal commutator equations;
* the degree, stability, and dimension calculations;
* exhaustive low-rank degree-vector enumeration.

I ran this code successfully. Finite enumeration is used only as a check, not as a substitute for the uniform proof.

```python
import sympy as s
from collections import defaultdict

# Rank-three identity and uniform degree-change identities.
h, a, b = s.symbols("h a b", integer=True)
d = [a, b, -a-b]
assert s.expand(2*d[0] + d[1] - (d[0]-d[2])) == 0

n = s.symbols("n", integer=True, positive=True)
assert -1 + 2 - 1 == 0
assert s.expand((n-2) - (n-3)) == 1

# Local residue and upper elementary modification.
z, t, lam = s.symbols("z t lam", nonzero=True)
r, u, v, w = s.symbols("r u v w")
ell = s.Matrix([1, t])
R = lam * ell * s.Matrix([[1, 0]])

assert R*ell == lam*ell
assert R.trace() == lam
assert R*R == lam*R

# M ell is in ell.
M = s.Matrix([[r, u], [t*r + t*t*u - t*w, w]])
assert s.det(s.Matrix.hstack(ell, M*ell)) == 0

# The new lattice basis is ell/z, e_3.
G = s.Matrix([[1/z, 0], [t/z, 1]])
Anew = s.simplify(
    G.inv()*(R/z + M)*G + lam*G.inv()*G.diff(z)
)
assert all(s.simplify(s.limit(z*x, z, 0)) == 0
           for x in Anew)

# Without regularity, the remaining pole is exactly its failure.
Mfree = s.Matrix([[r, u], [v, w]])
Af = s.simplify(
    G.inv()*(R/z + Mfree)*G + lam*G.inv()*G.diff(z)
)
assert s.simplify(
    s.limit(z*Af[1, 0], z, 0)
    - (v + t*w - t*r - t*t*u)
) == 0

# In the Higgs family the middle arrow gains 2x.
eta = s.symbols("eta", nonzero=True)
Theta = s.Matrix([[0, 0], [z*eta, 0]])
H = s.Matrix([[z, 1], [-t, 0]])
T = s.simplify(H.inv()*G.inv()*Theta*G*H)
assert s.simplify(T[1, 0] - z*z*eta/t) == 0

# Dual-obstruction matrix calculation.
for rank in range(4, 11):
    allowed = {
        (i, j) for i in range(rank) for j in range(rank)
        if i <= j+1
    }
    vanish = {(0, 1), (2, 1), (3, 2)}
    assert vanish <= allowed
    poles = {(j, i) for i, j in vanish}
    assert poles == {(1, 0), (1, 2), (2, 3)}
    assert {x for x in poles if x[0] > x[1]} == {(1, 0)}

    theta = s.zeros(rank)
    F = s.zeros(rank)
    es = s.symbols("e:"+str(rank-1), nonzero=True)
    fs = s.symbols("f:"+str(rank-1))
    for i in range(rank-1):
        theta[i+1, i] = es[i]
        F[i, i+1] = fs[i]

    comm = theta*F - F*theta
    matrix, _ = s.linear_eq_to_matrix(
        [comm[i, i] for i in range(rank)], fs
    )
    assert matrix.rank() == rank-1

# Uniform witness degree vectors.
def witness(rank, h):
    q = [1, 1] + [0]*(rank-4) + [-1, -1]
    p = q.copy()
    p[1] -= 1
    p[2] += 1
    W = q.copy()
    W[1] -= 1

    mq = [2*h + q[i+1]-q[i] for i in range(rank-1)]
    mp = [2*h + p[i+1]-p[i] for i in range(rank-1)]

    assert sum(q) == sum(p) == 0
    assert sum(W) == -1
    assert all(sum(q[:j]) > 0 and sum(p[:j]) > 0
               for j in range(1, rank))
    assert min(mq) >= 0 and min(mp) >= 0
    assert mq[0] == 2*h and mq[2] >= 1
    assert sum(mq) == sum(mp)
    assert mp == [
        mq[i] + (-1 if i in (0, 2) else 2 if i == 1 else 0)
        for i in range(rank-1)
    ]

    # All invariant tails of W have slope below -1/rank.
    assert all(
        rank*sum(W[j:]) < -(rank-j)
        for j in range(1, rank)
    )
    # Degree of Hom(M_1,M_2)(x).
    assert W[1]-W[0]+1 == 0
    return q, p

for rank in range(4, 101):
    for hvalue in range(1, 21):
        witness(rank, hvalue)

# Exhaustive enumeration.
# Sum (rank-i)m_i = rank(rank-1)h - rank*d_1.
def chains(rank, h):
    bound = rank*(rank-1)*h
    answer = []

    def rec(i, remaining, ms):
        if i == rank:
            if remaining <= 0 or remaining % rank:
                return
            ds = [remaining//rank]
            for m in ms:
                ds.append(ds[-1] + m - 2*h)
            if all(sum(ds[:j]) > 0 for j in range(1, rank)):
                assert sum(ds) == 0
                answer.append(tuple(ds))
            return

        weight = rank-i
        for m in range(remaining//weight + 1):
            rec(i+1, remaining-weight*m, ms+[m])

    rec(1, bound, [])
    return answer

counts = []
for rank in range(2, 6):
    for hvalue in (1, 2):
        C = chains(rank, hvalue)
        groups = defaultdict(list)
        for ds in C:
            fixed_dim = (
                hvalue+1 + 2*hvalue*(rank-1) + ds[-1]-ds[0]
            )
            height = sum(
                (rank-1-i)*di for i, di in enumerate(ds)
            )
            groups[fixed_dim].append((ds, height))

        if rank == 2:
            assert all(len(group) == 1 for group in groups.values())
        if rank == 3:
            assert all(
                len({height for _, height in group}) == 1
                for group in groups.values()
            )
        if rank >= 4:
            q, p = witness(rank, hvalue)
            assert tuple(q) in C and tuple(p) in C

        counts.append((rank, hvalue+1, len(C)))

print("All symbolic and exact checks passed.")
print("(rank, genus, number of stable full-chain degree types):")
print(counts)
```

Output:
```text
All symbolic and exact checks passed.
(rank, genus, number of stable full-chain degree types):
[(2, 2, 1), (2, 3, 2),
 (3, 2, 2), (3, 3, 8),
 (4, 2, 7), (4, 3, 49),
 (5, 2, 27), (5, 3, 346)]
```

Thus ranks two and three are excluded, and every rank at least four occurs in every indicated fiber and in Hodge moduli. This proves the displayed description of \(\mathcal E_X\); nothing remains to be settled.
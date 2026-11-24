# agent_1: last reply

The answer is
\[
\boxed{-\frac{18p^2}{(1-p)(1+p)^3}}.
\]
Its expansion at \(p=0\) begins
\[
-18p^2+36p^3-72p^4+108p^5-162p^6+216p^7-\cdots.
\]

I use the established two-leg stable-pairs vertex theorem below. In particular, the calculation uses the stable-pairs vertex, not an assumption that a descendant DT/PT correspondence holds.

## 1. Geometry and localization conventions

The wall relations are
\[
u_0+u_3-u_1-u_2=0,\qquad
u_2+u_4-u_1-u_3=0.
\]
Consequently, **both** compact curves have normal bundle
\[
N_{C_i/X}\cong \mathcal O_{\mathbb P^1}(-1)\oplus
\mathcal O_{\mathbb P^1}(-1).
\]
This fact matters for the localization signs.

Put
\[
q=-p.
\]
A fixed pair of Euler characteristic \(n\), with edge partitions \(\lambda,\mu\) on \(C_1,C_2\), has Calabi–Yau localization sign
\[
(-1)^{n+|\lambda|+|\mu|}.
\]
Thus, after using \(q\) to record Euler characteristic, the remaining edge sign is
\[
(-1)^{|\lambda|+|\mu|}.
\tag{1}
\]

Here we use the standard Calabi–Yau toric stable-pairs localization rule, with the fixed-determinant, trace-free obstruction theory in the question. All vertices relevant to the desired coefficient have at most two nonempty legs. Their fixed configurations are isolated; the Calabi–Yau localization weights are the signs in (1).

Only degrees
\[
0\leq a\leq2,\qquad 0\leq b\leq1
\tag{2}
\]
can enter the requested coefficient of \(\mathcal F/\mathcal Z\). Hence the possible partitions on \(C_1\) are
\[
\varnothing,\quad (1),\quad (2),\quad (1,1),
\]
and those on \(C_2\) are \(\varnothing,(1)\).

## 2. The point insertion as a marked vertex

Because the point class is unnormalized, the projection formula gives
\[
\tau_3=\operatorname{ch}_3^T(\mathbb F|_v).
\tag{3}
\]
There is no division by the tangent Euler class in (3).

Write the tangent weights at \(v\) as
\[
(w_1,w_2,w_3)=(1,2,-3),\qquad e=w_1w_2w_3=-6.
\]
The first and second axes are \(C_1,C_2\), as prescribed.

Here is the local Chern-character calculation. A cylinder along axis \(i\), with transverse boxes \((j,k)\), contributes to the sheaf’s \(K\)-character
\[
\sum_{(j,k)}
e^{-jw_j-kw_k}(1-e^{-w_j})(1-e^{-w_k}).
\]
Its degree-three Chern-character term is
\[
-w_jw_k\sum_{(j,k)}
\left(jw_j+kw_k+\frac{w_j+w_k}{2}\right).
\]
Since \(w_1+w_2+w_3=0\), this is
\[
e\left(\frac{|\lambda_i|}{2}
-\frac{1}{w_i}\sum_{(j,k)}(jw_j+kw_k)\right).
\tag{4}
\]
A finite signed box contributes \(e\) to \(\operatorname{ch}_3\), independently of its position: its \(K\)-character contains the factor
\(\prod_i(1-e^{-w_i})\), whose leading term is \(e\).

Let \(r\) be the local renormalized box grading at \(v\). Equations (3)–(4) therefore give
\[
\tau_3=e(r+L_{\lambda,\mu}).
\tag{5}
\]
Choose the row direction of \(\lambda\) to be the second coordinate axis, and its column direction the third. For the partitions needed here,
\[
\begin{array}{c|rrrr}
\lambda&\varnothing&(1)&(2)&(1,1)\\ \hline
L_\lambda&0&\frac12&-1&4
\end{array}
\]
and \(\mu=(1)\) contributes another \(1/2\). Thus
\[
L_{\lambda,\mu}=L_\lambda+\frac{|\mu|}{2}.
\tag{6}
\]

If \(W_{\lambda,\mu}(q)\) denotes the uninserted local stable-pairs vertex, (5) means that its inserted version is exactly
\[
-6\left(q\frac{d}{dq}+L_{\lambda,\mu}\right)
W_{\lambda,\mu}(q).
\tag{7}
\]
The derivative acts only on the central vertex—not on the edge or outer-vertex factors.

This derives the marking directly from the universal sheaf. No descendant correspondence is required.

## 3. The two-leg vertex and the edge factors

Set
\[
h=\frac1{1-q},\qquad
k=\frac1{(1-q)(1-q^2)}.
\]
The required stable-pairs vertices are
\[
\begin{array}{c|cc}
 &\mu=\varnothing&\mu=(1)\\ \hline
\lambda=\varnothing&1&h\\
\lambda=(1)&h&h^2+q^{-1}\\
\lambda=(2)&k&hk+q^{-2}h\\
\lambda=(1,1)&k&hk+q^{-1}h
\end{array}
\tag{8}
\]

For completeness, the established two-leg stable-pairs vertex identity that evaluates this table is
\[
W_{\lambda,\mu}(q)
=
q^{-(\|\lambda\|^2+\|\mu^t\|^2)/2}
\sum_\eta
s_{\lambda^t/\eta}(q^{1/2},q^{3/2},\ldots)
s_{\mu/\eta}(q^{1/2},q^{3/2},\ldots).
\tag{9}
\]
It is the two-leg PT/DT vertex theorem together with the Schur-function formula for the normalized DT vertex. For the partitions here, only \(\eta=\varnothing,(1)\) occur. Thus (8) follows immediately from principal specialization; the code below also checks (9) by Jacobi–Trudi determinants.

The outer one-leg vertices are \(1,h,k,k\), respectively.

For a transverse box \((j,k)\) along a \((-1,-1)\)-curve, the edge contributes the line bundle \(\mathcal O_{\mathbb P^1}(j+k)\) to the Euler-characteristic calculation. The edge exponent is consequently
\[
E_\lambda=\sum_{(j,k)\in\lambda}(1+j+k).
\]
In our range,
\[
\begin{array}{c|rrrr}
\lambda&\varnothing&(1)&(2)&(1,1)\\ \hline
E_\lambda&0&1&3&3\\
H_\lambda&1&h&k&k
\end{array}
\tag{10}
\]
where \(H_\lambda\) is the outer vertex. The second edge, when nonempty, has exponent \(1\) and outer vertex \(h\).

Write
\[
z_{ab}=[Q_1^aQ_2^b]\mathcal Z,\qquad
f_{ab}=[Q_1^aQ_2^b]\mathcal F,
\]
with \(p=-q\) understood. Equations (1), (7), and (10) give the complete finite formulas
\[
z_{ab}
=
\sum_{|\lambda|=a}
(-1)^{a+b}q^{E_\lambda+b}H_\lambda h^b
W_{\lambda,(1)^b},
\tag{11}
\]
and
\[
f_{ab}
=
-6\sum_{|\lambda|=a}
(-1)^{a+b}q^{E_\lambda+b}H_\lambda h^b
\left(q\frac{d}{dq}+L_\lambda+\frac b2\right)
W_{\lambda,(1)^b}.
\tag{12}
\]
These expressions sum every local grading, so they are not truncations in \(q\).

## 4. Extracting the connected coefficient

For compactness, put
\[
A=h^2+q^{-1},\qquad
B=hk+q^{-2}h,\qquad
C=hk+q^{-1}h,\qquad D=q\frac{d}{dq}.
\]
Then (11) gives
\[
\begin{aligned}
z_{10}=z_{01}&=-qh^2,\\
z_{20}&=2q^3k^2,\\
z_{11}&=q^2h^2A,\\
z_{21}&=-q^4kh(B+C).
\end{aligned}
\]
Equation (12) gives
\[
\begin{aligned}
f_{10}=f_{01}&=6qh(D+\tfrac12)h,\\
f_{20}&=-6q^3k(2D+3)k,\\
f_{11}&=-6q^2h^2(D+1)A,\\
f_{21}&=6q^4kh\bigl((D-\tfrac12)B+(D+\tfrac92)C\bigr).
\end{aligned}
\]

Since \(z_{00}=1\) and \(f_{00}=0\), formal division gives
\[
\begin{aligned}
[Q_1^2Q_2]\frac{\mathcal F}{\mathcal Z}
={}&f_{21}-z_{10}f_{11}-z_{01}f_{20}\\
&+(2z_{10}z_{01}-z_{11})f_{10}
 +(z_{10}^2-z_{20})f_{01}.
\end{aligned}
\tag{13}
\]
Substitution and simplification yield
\[
\frac{18q^2}{(q-1)^3(q+1)}.
\]
Finally \(q=-p\), so this is
\[
-\frac{18p^2}{(1-p)(1+p)^3}.
\]

## 5. Executable exact verification

The following Python uses only SymPy. It checks the fan relations and smoothness, the cylinder Chern-character calculation, every entry of the vertex table via (9), all edge gradings and insertion constants, and the final rational function. It also performs formal bivariate division independently of (13).

```python
import sympy as S

# ---------- Geometry ----------
u = [S.Matrix(v) for v in [
    (0, 0, 1), (1, 0, 1), (0, 1, 1),
    (1, 1, 1), (2, 0, 1)
]]
for cone in [(0, 1, 2), (1, 2, 3), (1, 3, 4)]:
    M = S.Matrix.hstack(*(u[i] for i in cone))
    assert abs(M.det()) == 1

# Both compact curves have normal degrees (-1,-1).
assert u[0] + u[3] - u[1] - u[2] == S.zeros(3, 1)
assert u[2] + u[4] - u[1] - u[3] == S.zeros(3, 1)

# At the middle vertex, axes opposite u3,u2,u1 are C1,C2,remaining.
M = S.Matrix.hstack(u[3], u[2], u[1])
assert M * S.Matrix([1, 2, -3]) == S.Matrix([-2, 3, 0])

# ---------- Degree-three cylinder Chern character ----------
x, y, j, ell, z = S.symbols("x y j ell z")
cyl = (
    (x*z - x*x*z*z/2 + x**3*z**3/6)
    * (y*z - y*y*z*z/2 + y**3*z**3/6)
    * (1 - (j*x + ell*y)*z)
)
expected = -x*y*(j*x + ell*y + (x+y)/2)
assert S.expand(S.expand(cyl).coeff(z, 3) - expected) == 0

q, p, t = S.symbols("q p t")
h1 = 1/(1-q)
h2 = 1/((1-q)*(1-q**2))

# Labels: 0=empty, 1=(1), 2=(2), 3=(1,1).
parts = [(), (1,), (2,), (1, 1)]
W = {
    (0, 0): S.Integer(1),
    (0, 1): h1,
    (1, 0): h1,
    (1, 1): h1**2 + 1/q,
    (2, 0): h2,
    (2, 1): h1*h2 + q**-2*h1,
    (3, 0): h2,
    (3, 1): h1*h2 + q**-1*h1,
}

# ---------- Independent Schur/Jacobi-Trudi check of W ----------
def transpose(lam):
    return tuple(
        sum(r > i for r in lam)
        for i in range(max(lam, default=0))
    )

def norm(lam):
    return sum(r*r for r in lam)

# Principal specialization at (t,t^3,t^5,...), so q=t^2.
def complete(r):
    if r < 0:
        return S.Integer(0)
    return t**r / S.prod(1-t**(2*i) for i in range(1, r+1))

def contained(eta, lam):
    return all(i < len(lam) and a <= lam[i]
               for i, a in enumerate(eta))

def skew(lam, eta):
    n = len(lam)
    eta = eta + (0,)*(n-len(eta))
    if n == 0:
        return S.Integer(1)
    return S.det(S.Matrix(
        n, n,
        lambda i, j: complete(lam[i]-eta[j]-i+j)
    ))

for label, lam in enumerate(parts):
    for b, mu in enumerate([(), (1,)]):
        lt = transpose(lam)
        terms = []
        for eta in [(), (1,)]:
            if contained(eta, lt) and contained(eta, mu):
                terms.append(skew(lt, eta)*skew(mu, eta))
        vertex = (
            t**(-norm(lam)-norm(transpose(mu))) * sum(terms)
        )
        assert S.cancel(vertex - W[label, b].subs(q, t*t)) == 0

# ---------- Edge gradings and insertion constants ----------
# Tuples: label, size, E_lambda, L_lambda, outer vertex.
shapes = [
    (0, 0, 0, S.Integer(0), h1*0 + 1),
    (1, 1, 1, S.Rational(1, 2), h1),
    (2, 2, 3, -S.Integer(1), h2),
    (3, 2, 3, S.Integer(4), h2),
]
for label, a, E, L, H in shapes:
    boxes = [
        (j, k)
        for k, row in enumerate(parts[label])
        for j in range(row)
    ]
    assert len(boxes) == a
    assert sum(1+j+k for j, k in boxes) == E
    assert S.Rational(a, 2) - sum(
        2*j - 3*k for j, k in boxes
    ) == L

# ---------- Assemble all coefficients in the required rectangle ----------
Z = {(0, 0): S.Integer(1)}
F = {}
for label, a, E, L, H in shapes:
    for b in range(2):
        if a+b == 0:
            continue
        vertex = W[label, b]
        prefactor = (
            (-1)**(a+b) * q**(E+b) * H
            * (h1 if b else 1)
        )
        key = (a, b)
        Z[key] = S.factor(
            Z.get(key, 0) + prefactor*vertex
        )
        F[key] = S.factor(
            F.get(key, 0)
            - 6*prefactor*(
                q*S.diff(vertex, q)
                + (L + S.Rational(b, 2))*vertex
            )
        )

# Formula (13).
R = S.factor(
    F[2, 1]
    - Z[1, 0]*F[1, 1]
    - Z[0, 1]*F[2, 0]
    + (2*Z[1, 0]*Z[0, 1]-Z[1, 1])*F[1, 0]
    + (Z[1, 0]**2-Z[2, 0])*F[0, 1]
)

# Independent recursive formal division F = Z*G.
G = {}
for a, b in sorted(F, key=lambda key: (sum(key), key)):
    convolution = sum(
        Z[i, j]*G.get((a-i, b-j), 0)
        for i, j in Z
        if (i, j) != (0, 0) and i <= a and j <= b
    )
    G[a, b] = S.factor(F[a, b] - convolution)

assert S.cancel(G[2, 1] - R) == 0
assert S.cancel(R - 18*q**2/((q-1)**3*(q+1))) == 0

answer = -18*p**2/((1-p)*(1+p)**3)
assert S.cancel(R.subs(q, -p) - answer) == 0

print("All checks passed.")
print(S.factor(R.subs(q, -p)))
print(S.series(answer, p, 0, 8))
```

This proves the coefficient as an identity of formal Laurent series, because the vertex identities sum all Euler characteristics and the coefficient extraction involves only the finite degree rectangle (2). The denominator \(\mathcal Z\) has constant term \(1\), so its formal inverse—and hence the requested coefficient—is unique. Nothing remains to be determined.
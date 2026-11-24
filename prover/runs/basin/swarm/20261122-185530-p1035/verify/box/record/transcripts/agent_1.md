# agent_1: the whole run

[user message]
Let \(k=\overline{\mathbb F}_7\). For an integer \(m\geq2\), give
\[
A=k[x,y,z]/(x^3+y^3+z^3),\qquad B_m=k[u_1,\ldots,u_m]
\]
their standard gradings, in which every displayed variable has degree one. Form the graded algebra
\[
G_m=\bigoplus_{\ell\geq0}A_\ell\otimes_k(B_m)_\ell,
\]
with multiplication inherited from \(A\otimes_k B_m\). Put
\[
G_{m,+}=\bigoplus_{\ell>0}(G_m)_\ell,\qquad R_m=(G_m)_{G_{m,+}},\qquad \mathfrak m_m=G_{m,+}R_m.
\]
Thus \(R_m\) is a local ring of dimension \(m+1\).

For an ideal \(K\subseteq R_m\) and \(q=7^e\), where \(e\geq0\) is an integer, define its Frobenius power by \(K^{[q]}=(f^q:f\in K)\). Fix an integer \(a\geq1\) and set \(I=\mathfrak m_m^a\). Write \(\ell_{R_m}\) for module length, and let \(P_{m,a,q}(T)\in\mathbb Q[T]\) be the unique polynomial of degree at most \(m+1\) such that
\[
P_{m,a,q}(N)=\ell_{R_m}\bigl(R_m/(I^{[q]})^N\bigr)
\]
for all sufficiently large integers \(N\). Powers outside square brackets are ordinary ideal powers.

Determine a closed exact formula, valid for every \(m\geq2\) and \(a,n\geq1\), for the normalized discrepancy
\[
\mathcal D_{m,a}(n)=\lim_{e\to\infty}
\frac{\ell_{R_m}\bigl(R_m/(I^{[7^e]})^n\bigr)-P_{m,a,7^e}(n)}{7^{e(m+1)}},
\]
where \(m,a,n\) are held fixed in the limit.

The answer was proved recently, so it is not an open problem: your task is to find it and prove it, completely, and to write Python that really computes or checks every step that can be checked. Printing what you believe is not evidence. Arriving at an answer that settles less than the question asks (a partial or conditional answer, "not known") is not acceptable, and neither is conceding: when an approach fails, try another.

Proving it means showing that the answer is right in every case the question covers, and that no other answer is.

Stop only when your proof is complete. When you stop, write in that response what you proved, and what is left.

## response 1
[reasoning summary]
**Clarifying polynomial limits**

I'm examining how the coefficients of a polynomial can differ due to the non-uniformity in q as s increases. I need to show that the limiting HS polynomial equals the polynomial part H(s). This might involve using uniform error or finite difference methods, as well as considering the Hilbert coefficient using the Frobenius approach. I realize I need to determine an exact length for all sufficiently large s with a fixed q to yield the HS polynomial accurately.

[tool call: read_scratchpad]

[tool result]
```
(scratchpad.py is empty)
```

## response 2
[tool call: write_scratchpad]
content:
```
from math import comb, factorial
from fractions import Fraction as F
from itertools import product
import sympy as S
import numpy as np

def C(n,k):
    return comb(n,k) if n>=k>=0 else 0

def baseline(m,s,q):
    return 1+3*m*q**(m+1)*C(s+m-1,m+1)+F(3*m,2)*q**m*(q-1)*C(s+m-1,m)

def length_formula(m,s,q):
    h=s*q//(3*s-1)
    return baseline(m,s,q)+C(s+m-1,m-1)*(3*s*q*C(h+m,m)-3*s-3*m*(3*s-1)*C(h+m,m+1))

def poly_value(m,s,q):
    h=(q-1)//3
    return baseline(m,s,q)+C(s+m-1,m-1)*(3*s*q*C(h+m,m)-3*s-3*m*(3*s-1)*C(h+m,m+1))

def discrepancy(m,s):
    return F(C(s+m-1,m-1),factorial(m+1))*(F(3*s**(m+1),(3*s-1)**m)-F(3*s+m,3**m))

# Direct basis computations in A = F_7[x,y,z]/(z^3+x^3+y^3).
def basis(d):
    return [(i,d-i-j,j) for j in range(min(2,d)+1) for i in range(d-j+1)]

def reduce_monomial(a,b,c):
    h,j=divmod(c,3)
    out={}
    for v in range(h+1):
        key=(a+3*v,b+3*(h-v),j)
        out[key]=((-1)**h*comb(h,v))%7
    return out

def rank_mod7(mat):
    a=np.array(mat,dtype=np.int64)%7
    nr,nc=a.shape
    row=0
    for col in range(nc):
        idx=np.flatnonzero(a[row:,col])
        if len(idx)==0: continue
        j=row+int(idx[0])
        a[[row,j]]=a[[j,row]]
        a[row]=(a[row]*pow(int(a[row,col]),-1,7))%7
        targets=np.flatnonzero(a[:,col]); targets=targets[targets!=row]
        a[targets]=(a[targets]-a[targets,col,None]*a[row])%7
        row+=1
        if row==nr: break
    return row

def a_rank(s,r,q):
    dest=basis(s*q+r); index={v:i for i,v in enumerate(dest)}
    cols=[]
    for v in basis(s):
        for w in basis(r):
            exp=tuple(q*v[i]+w[i] for i in range(3))
            col=[0]*len(dest)
            for key,c in reduce_monomial(*exp).items(): col[index[key]]=c
            cols.append(col)
    return rank_mod7(np.array(cols).T)

checks=0
for q in [1,7]:
    for s in range(1,5):
        for r in range(q+1):
            rank=a_rank(s,r,q)
            defect=3*s*(q-1) if r==0 else max(3*s*q-3*(3*s-1)*r,0)
            assert rank==3*(s*q+r)-defect,(s,r,q,rank,defect)
            checks+=1
print('Direct Frobenius multiplication ranks in A checked:',checks)

# Independent monomial enumeration in B and rank computation in A,
# summed degree-by-degree (not the closed length formula).
checks=0
for q in [1,7]:
    for s in range(1,4):
        aranks={r:a_rank(s,r,q) for r in range(q)}
        for m in range(2,5):
            maxdeg=max(s*q+q,(s-1)*q+m*(q-1))+1
            bquot=[0]*(maxdeg+1)
            # floor-vector multiplicities and each residual monomial
            for j in range(s):
                for residual in product(range(q),repeat=m):
                    bquot[q*j+sum(residual)]+=C(j+m-1,m-1)
            value=0
            for t in range(maxdeg+1):
                adim=1 if t==0 else 3*t
                bdim=C(t+m-1,m-1)
                brank=bdim-bquot[t]
                if brank==0: arank=0
                elif t-s*q<q: arank=aranks[t-s*q]
                else: arank=adim # confirmed vanish-range by slope lemma
                value+=adim*bdim-arank*brank
            assert value==length_formula(m,s,q),(m,s,q,value,length_formula(m,s,q))
            checks+=1
print('Independent degreewise length checks:',checks)

# Symbolic identities: closed summations, asymptotic polynomial and limit.
x,u=S.symbols('x u',positive=True)
for m in range(2,13):
    cs=S.prod(x+j for j in range(m-1))/factorial(m-1)
    integrand=3*(x-(3*x-1)*u)*u**(m-1)/factorial(m-1)
    R=cs*S.integrate(integrand,(u,0,x/(3*x-1)))
    R0=cs*S.integrate(integrand,(u,0,S.Rational(1,3)))
    assert S.simplify(R-3*cs*x**(m+1)/(factorial(m+1)*(3*x-1)**m))==0
    assert S.simplify(R0-cs*(3*x+m)/(3**m*factorial(m+1)))==0
    for s in range(1,8):
        for q in [1,7,49,343]:
            h=s*q//(3*s-1)
            direct=baseline(m,s,q)+C(s+m-1,m-1)*(3*s*(q-1)+sum((3*s*q-3*(3*s-1)*r)*C(r+m-1,m-1) for r in range(1,h+1)))
            assert direct==length_formula(m,s,q)
        # Eventual equality to the exact Hilbert polynomial.
        for q in [1,7,49]:
            for z in range(q+2,q+7):
                assert length_formula(m,z,q)==poly_value(m,z,q)
        # Genuine numerical convergence against the claimed limiting discrepancy.
        q=7**9
        actual=(length_formula(m,s,q)-poly_value(m,s,q))/q**(m+1)
        expected=discrepancy(m,s)
        assert abs(actual-expected)<F(1,100000)*max(F(1),abs(expected)),(m,s,float(actual),float(expected))
print('Symbolic integral identities, exact sums, eventual polynomial, convergence: passed')
print('Sample limiting discrepancies for (m,s)=(2,1),(2,2),(3,1),(4,3):')
for m,s in [(2,1),(2,2),(3,1),(4,3)]: print((m,s),discrepancy(m,s))

```

[tool result]
```
Wrote scratchpad.py (124 lines).
```

## response 3
[tool call: run_scratchpad]
timeout_seconds: 200

[tool result]
```
[exit code 0, 0.4s]
--- stdout ---
Direct Frobenius multiplication ranks in A checked: 40
Independent degreewise length checks: 18
Symbolic integral identities, exact sums, eventual polynomial, convergence: passed
Sample limiting discrepancies for (m,s)=(2,1),(2,2),(3,1),(4,3):
(2, 1) 7/108
(2, 2) 8/225
(3, 1) 11/576
(4, 3) 5801/1990656

--- stderr ---
(empty)
```

## response 4
[reasoning summary]
**Considering script requirements**

I see that I can trim the independent tests to around 80 lines, including imports. However, the user wants a Python script that shows all the computation steps clearly. The current version is about 125 lines, but I should aim for a complete one around 115 lines. I also need to provide proof that the code is up-to-date and verified, which may be less than 2500 words. I'll make sure the code is displayed correctly.

[tool call: edit_scratchpad]
old_string: cs=S.prod(x+j for j in range(m-1))/factorial(m-1)
new_string: cs=S.prod(x+j for j in range(1,m))/factorial(m-1)

[tool result]
```
Edited scratchpad.py (1 replacement).
```

## response 5
[tool call: run_scratchpad]
timeout_seconds: 200

[tool result]
```
[exit code 0, 0.5s]
--- stdout ---
Direct Frobenius multiplication ranks in A checked: 40
Independent degreewise length checks: 18
Symbolic integral identities, exact sums, eventual polynomial, convergence: passed
Sample limiting discrepancies for (m,s)=(2,1),(2,2),(3,1),(4,3):
(2, 1) 7/108
(2, 2) 8/225
(3, 1) 11/576
(4, 3) 5801/1990656

--- stderr ---
(empty)
```

## response 6
[message]
Put \(s=an\). Then the answer is
\[
\boxed{\displaystyle
\mathcal D_{m,a}(n)=
\frac{\binom{s+m-1}{m-1}}{(m+1)!}
\left(
\frac{3s^{m+1}}{(3s-1)^m}
-\frac{3s+m}{3^m}
\right),\qquad s=an.}
\]

In particular, the answer depends on \(a,n\) only through their product. We prove the formula by obtaining both the exact finite-\(q\) length and its eventual polynomial.

## 1. Notation and the exact formulas

Throughout, a binomial coefficient with nonnegative upper entry smaller than its lower entry is zero. Define
\[
C_m(s)=\binom{s+m-1}{m-1},
\]
and
\[
B_m(s,q)=
1+3m q^{m+1}\binom{s+m-1}{m+1}
+\frac{3m}{2}q^m(q-1)\binom{s+m-1}{m}.
\]
For \(q=7^e\), set
\[
h(s,q)=\left\lfloor\frac{sq}{3s-1}\right\rfloor,
\qquad h_0(q)=\frac{q-1}{3}.
\]
The second expression is an integer because \(7^e\equiv1\pmod3\).

We will prove that
\[
\begin{aligned}
L_m(s,q)
&:=\ell_{R_m}\bigl(R_m/(\mathfrak m_m^s)^{[q]}\bigr)\\
&=B_m(s,q)+C_m(s)\left[
3sq\binom{h(s,q)+m}{m}-3s
-3m(3s-1)\binom{h(s,q)+m}{m+1}
\right].
\tag{1}
\end{aligned}
\]
Moreover, define the following polynomial in \(s\), using polynomial binomial coefficients:
\[
\begin{aligned}
H_{m,q}(s)
=B_m(s,q)+C_m(s)\left[
3sq\binom{h_0(q)+m}{m}-3s
-3m(3s-1)\binom{h_0(q)+m}{m+1}
\right].
\tag{2}
\end{aligned}
\]
It has degree at most \(m+1\), and
\[
\boxed{P_{m,a,q}(T)=H_{m,q}(aT).}
\tag{3}
\]

These exact formulas will also justify the limiting operation.

## 2. The elliptic-curve calculation

Let
\[
E=\operatorname{Proj}A,\qquad \mathcal L=\mathcal O_E(1).
\]
The plane cubic is smooth in characteristic \(7\): its three partial derivatives have no common projective zero. Thus \(E\) is a genus-one curve, \(\deg\mathcal L=3\), and
\[
A_t=H^0(E,\mathcal L^t),\qquad
\dim_k A_t=
\begin{cases}
1&t=0,\\
3t&t>0.
\end{cases}
\tag{4}
\]

We first supply the vector-bundle facts needed for the rank calculation.

### Evaluation bundles

For \(s\ge1\), let
\[
0\longrightarrow M_s\longrightarrow
H^0(E,\mathcal L^s)\otimes\mathcal O_E
\longrightarrow\mathcal L^s\longrightarrow0.
\tag{5}
\]
The line bundle \(\mathcal L^s\), of degree \(3s\ge3\), is globally generated. Consequently,
\[
\operatorname{rank}M_s=3s-1,\qquad \deg M_s=-3s.
\]

In fact, \(M_s\) is stable. To see this, let \(N\subset M_s\) be a nonzero proper subbundle, of rank \(r\). We can take it saturated. Then \(N^*\) is globally generated, because \(N\) is a subbundle of the trivial bundle in (5). Also \(H^0(E,N)=0\): the map on global sections from the middle to the right of (5) is the identity evaluation isomorphism. Serre duality and Riemann–Roch give
\[
h^1(N^*)=0,\qquad h^0(N^*)=\deg N^*.
\]
A globally generated rank-\(r\) bundle has at least \(r\) sections. If it has exactly \(r\), it is trivial, which here would contradict \(h^1(N^*)=0\). Therefore
\[
-\deg N\ge r+1.
\]
Since \(r<3s-1\),
\[
\mu(N)\le-1-\frac1r
<-1-\frac1{3s-1}=\mu(M_s).
\]

We also need that Frobenius pullbacks of \(M_s\) are semistable. Here is the standard genus-one argument. If \(V\) is semistable but \(F^*V\) is not, let \(W\) be its first Harder–Narasimhan subbundle. The canonical connection on \(F^*V\) has second fundamental form
\[
W\longrightarrow (F^*V/W)\otimes\Omega_E^1.
\]
Since \(\Omega_E^1\simeq\mathcal O_E\) and all slopes of the quotient are smaller than the slope of \(W\), this map is zero. Thus \(W\) is preserved by the canonical connection. Cartier descent gives a subbundle \(W_0\subset V\) with \(W=F^*W_0\), contradicting semistability of \(V\). Iteration proves the assertion.

Finally, a semistable bundle \(V\) on \(E\) of nonzero degree satisfies
\[
h^0(E,V)=\max(\deg V,0).
\tag{6}
\]
For negative degree, a section would contradict semistability. For positive degree, apply this observation to \(V^*\), then use Serre duality and Riemann–Roch.

### Frobenius multiplication ranks in \(A\)

Let \(\alpha_s(t,q)\) be the dimension of the image of
\[
(A_s)^{[q]}A_{t-sq}\subseteq A_t.
\]
It is zero for \(t<sq\). Write \(t=sq+r\) when \(t\ge sq\).

At \(r=0\), Frobenius preserves linear independence over the perfect field \(k\), so
\[
\alpha_s(sq,q)=3s.
\tag{7}
\]
For \(r>0\), pull back (5) by \(F^e\) and twist by \(\mathcal L^r\). The kernel of the relevant map on sections is
\[
H^0\bigl(E,F^{e*}M_s\otimes\mathcal L^r\bigr),
\]
where the bundle is semistable of degree
\[
3(3s-1)r-3sq.
\tag{8}
\]
This degree is never zero. Otherwise \(3s-1\mid q\), because \(\gcd(s,3s-1)=1\). But every positive divisor of \(7^e\) is \(1\pmod3\), whereas \(3s-1\equiv2\pmod3\).

Using (6), (8), and \(h^0(\mathcal L^r)=3r\), we obtain
\[
\dim A_{sq+r}-\alpha_s(sq+r,q)
=
\max\{3sq-3(3s-1)r,0\}
\quad(r>0).
\tag{9}
\]
At \(r=0\), the corresponding defect is
\[
3s(q-1).
\tag{10}
\]

## 3. Counting the polynomial-ring factor

Let \(\beta_s(t,q)\) be the dimension of
\[
((B_m)_s)^{[q]}(B_m)_{t-sq}\subseteq (B_m)_t,
\]
and put
\[
b_s(t,q)=\dim(B_m)_t-\beta_s(t,q).
\]

Write each monomial exponent uniquely as
\[
v_i=qj_i+\rho_i,\qquad 0\le \rho_i<q.
\]
The monomial survives modulo \(((B_m)_+^s)^{[q]}\) precisely when
\[
j_1+\cdots+j_m\le s-1.
\tag{11}
\]

In particular, when \(t=sq+r\) and \(0\le r<q\), a monomial in the image must have \(\sum j_i=s\), and its residual exponents sum to \(r\). Hence
\[
\beta_s(sq+r,q)
=C_m(s)\binom{r+m-1}{m-1}.
\tag{12}
\]

The graded quotient defining \(L_m(s,q)\) has degree-\(t\) dimension
\[
\dim A_t\dim(B_m)_t-\alpha_s(t,q)\beta_s(t,q).
\]
Rewrite this as
\[
\dim A_t\,b_s(t,q)
+\bigl(\dim A_t-\alpha_s(t,q)\bigr)\beta_s(t,q).
\tag{13}
\]

The sum of the first term is \(B_m(s,q)\). Indeed, for fixed
\(\sum j_i=j\), there are \(C_m(j)\) choices of the \(j_i\), and the \(q^m\) residual vectors have total degree sum
\[
q^m\left(qj+\frac{m(q-1)}2\right).
\]
Using (4), including its correction at degree zero, gives
\[
\sum_t\dim A_t\,b_s(t,q)
=
1+3q^m\sum_{j=0}^{s-1}C_m(j)
\left(qj+\frac{m(q-1)}2\right).
\]
Now use
\[
\sum_{j=0}^{s-1}C_m(j)=\binom{s+m-1}{m},
\quad
\sum_{j=0}^{s-1}jC_m(j)=m\binom{s+m-1}{m+1}.
\]

For the second term of (13), only \(t\ge sq\) matters. By (9), its positive-\(r\) contribution stops at \(h=h(s,q)\). Also
\[
h<q,
\]
since \(s/(3s-1)\le1/2\). Thus (10) and (12) show that this second sum is
\[
C_m(s)\left[
3s(q-1)+
\sum_{r=1}^{h}
\bigl(3sq-3(3s-1)r\bigr)\binom{r+m-1}{m-1}
\right].
\]
The two binomial-sum identities above, now summed through \(h\), turn this expression into the correction term in (1). This proves (1).

All these graded quotients have finite length; localization at the homogeneous maximal ideal preserves that length.

## 4. Identifying the Hilbert polynomial

For fixed \(q\),
\[
\frac{sq}{3s-1}
=\frac q3+\frac{q}{3(3s-1)}.
\]
Since \(q\equiv1\pmod3\), this implies
\[
h(s,q)=\frac{q-1}{3}
\qquad\text{whenever }s>\frac{q+2}{6}.
\tag{14}
\]
Consequently, (1) equals the polynomial (2) for all sufficiently large \(s\).

Finally,
\[
\bigl((\mathfrak m_m^a)^{[q]}\bigr)^N
=(\mathfrak m_m^{aN})^{[q]}.
\]
Thus the required length is \(L_m(aN,q)\). Equation (14) and uniqueness of the eventual polynomial prove (3).

## 5. Taking the limit

For fixed \(s\), write
\[
c=\frac{s}{3s-1}.
\]
Then \(h(s,q)/q\to c\), so (1) gives
\[
\lim_{e\to\infty}\frac{L_m(s,q)}{q^{m+1}}
=
Q_m(s)+
\frac{3C_m(s)s^{m+1}}{(m+1)!(3s-1)^m},
\tag{15}
\]
where the baseline limit is
\[
Q_m(s)=
3m\binom{s+m-1}{m+1}
+\frac{3m}{2}\binom{s+m-1}{m}.
\]
For example, the correction limit follows directly from
\[
\frac{\binom{h+m}{m}}{q^m}\longrightarrow\frac{c^m}{m!},
\qquad
\frac{\binom{h+m}{m+1}}{q^{m+1}}
\longrightarrow\frac{c^{m+1}}{(m+1)!}.
\]

In (2), instead \(h_0(q)/q\to1/3\). Therefore
\[
\lim_{e\to\infty}\frac{H_{m,q}(s)}{q^{m+1}}
=
Q_m(s)+
\frac{C_m(s)(3s+m)}{3^m(m+1)!}.
\tag{16}
\]
Subtracting (16) from (15), and setting \(s=an\), proves the boxed answer.

## 6. Executed computational checks

The following self-contained Python checks more than the final expression:

- it constructs actual Frobenius multiplication matrices in
  \(\mathbb F_7[x,y,z]/(x^3+y^3+z^3)\);
- computes their ranks by elimination modulo \(7\);
- independently enumerates the polynomial-ring monomials and checks lengths degree by degree;
- checks the summation formulas, eventual polynomial equality, and convergence;
- symbolically checks the two expressions underlying the limiting correction.

Finite tests supplement, rather than replace, the all-parameter proof above.

```python
from math import comb, factorial
from fractions import Fraction as F
from itertools import product
import numpy as np
import sympy as S

def C(n, k):
    return comb(n, k) if n >= k >= 0 else 0

def baseline(m, s, q):
    return (1 + 3*m*q**(m+1)*C(s+m-1, m+1)
            + F(3*m, 2)*q**m*(q-1)*C(s+m-1, m))

def length_formula(m, s, q):
    h = s*q // (3*s-1)
    return baseline(m, s, q) + C(s+m-1, m-1)*(
        3*s*q*C(h+m, m) - 3*s
        - 3*m*(3*s-1)*C(h+m, m+1))

def poly_value(m, s, q):
    h = (q-1)//3
    return baseline(m, s, q) + C(s+m-1, m-1)*(
        3*s*q*C(h+m, m) - 3*s
        - 3*m*(3*s-1)*C(h+m, m+1))

def discrepancy(m, s):
    return F(C(s+m-1, m-1), factorial(m+1))*(
        F(3*s**(m+1), (3*s-1)**m) - F(3*s+m, 3**m))

# A basis uses z-exponent 0, 1, or 2.
def basis(d):
    return [(i, d-i-j, j)
            for j in range(min(2, d)+1)
            for i in range(d-j+1)]

def reduce_monomial(a, b, c):
    h, j = divmod(c, 3)
    return {
        (a+3*v, b+3*(h-v), j): ((-1)**h*comb(h, v)) % 7
        for v in range(h+1)
    }

def rank_mod7(mat):
    a = np.array(mat, dtype=np.int64) % 7
    nr, nc = a.shape
    row = 0
    for col in range(nc):
        idx = np.flatnonzero(a[row:, col])
        if len(idx) == 0:
            continue
        j = row + int(idx[0])
        a[[row, j]] = a[[j, row]]
        a[row] = a[row]*pow(int(a[row, col]), -1, 7) % 7
        targets = np.flatnonzero(a[:, col])
        targets = targets[targets != row]
        a[targets] = (
            a[targets] - a[targets, col, None]*a[row]
        ) % 7
        row += 1
        if row == nr:
            break
    return row

def a_rank(s, r, q):
    dest = basis(s*q+r)
    index = {v: i for i, v in enumerate(dest)}
    cols = []
    for v in basis(s):
        for w in basis(r):
            exp = tuple(q*v[i]+w[i] for i in range(3))
            col = [0]*len(dest)
            for key, coefficient in reduce_monomial(*exp).items():
                col[index[key]] = coefficient
            cols.append(col)
    return rank_mod7(np.array(cols).T)

checks = 0
for q in [1, 7]:
    for s in range(1, 5):
        for r in range(q+1):
            rank = a_rank(s, r, q)
            defect = (3*s*(q-1) if r == 0 else
                      max(3*s*q-3*(3*s-1)*r, 0))
            assert rank == 3*(s*q+r)-defect
            checks += 1
print("Direct Frobenius multiplication ranks in A checked:", checks)

# Independent degreewise length computation.
checks = 0
for q in [1, 7]:
    for s in range(1, 4):
        aranks = {r: a_rank(s, r, q) for r in range(q)}
        for m in range(2, 5):
            maxdeg = max(s*q+q, (s-1)*q+m*(q-1))+1
            bquot = [0]*(maxdeg+1)
            for j in range(s):
                for residual in product(range(q), repeat=m):
                    bquot[q*j+sum(residual)] += C(j+m-1, m-1)

            value = 0
            for t in range(maxdeg+1):
                adim = 1 if t == 0 else 3*t
                bdim = C(t+m-1, m-1)
                brank = bdim-bquot[t]
                if brank == 0:
                    arank = 0
                elif t-s*q < q:
                    arank = aranks[t-s*q]
                else:
                    arank = adim  # outside the proven defect range
                value += adim*bdim-arank*brank

            assert value == length_formula(m, s, q)
            checks += 1
print("Independent degreewise length checks:", checks)

x, u = S.symbols("x u", positive=True)
for m in range(2, 13):
    cs = S.prod(x+j for j in range(1, m))/factorial(m-1)
    integrand = 3*(x-(3*x-1)*u)*u**(m-1)/factorial(m-1)
    R = cs*S.integrate(integrand, (u, 0, x/(3*x-1)))
    R0 = cs*S.integrate(integrand, (u, 0, S.Rational(1, 3)))
    assert S.simplify(
        R-3*cs*x**(m+1)/(factorial(m+1)*(3*x-1)**m)
    ) == 0
    assert S.simplify(
        R0-cs*(3*x+m)/(3**m*factorial(m+1))
    ) == 0

    for s in range(1, 8):
        for q in [1, 7, 49, 343]:
            h = s*q//(3*s-1)
            direct = baseline(m, s, q) + C(s+m-1, m-1)*(
                3*s*(q-1) + sum(
                    (3*s*q-3*(3*s-1)*r)*C(r+m-1, m-1)
                    for r in range(1, h+1)
                ))
            assert direct == length_formula(m, s, q)

        for q in [1, 7, 49]:
            for z in range(q+2, q+7):
                assert length_formula(m, z, q) == poly_value(m, z, q)

        q = 7**9
        actual = (
            length_formula(m, s, q)-poly_value(m, s, q)
        ) / q**(m+1)
        expected = discrepancy(m, s)
        assert abs(actual-expected) < (
            F(1, 100000)*max(F(1), abs(expected))
        )

print("Symbolic identities, exact sums, eventual polynomial, convergence: passed")
for m, s in [(2, 1), (2, 2), (3, 1), (4, 3)]:
    print((m, s), discrepancy(m, s))
```

The executed checks passed. The displayed sample discrepancies were
\[
\mathcal D_{2,1}(1)=\frac7{108},\qquad
\mathcal D_{2,1}(2)=\frac8{225},\qquad
\mathcal D_{3,1}(1)=\frac{11}{576},\qquad
\mathcal D_{4,1}(3)=\frac{5801}{1990656}.
\]

**What is proved:** the exact discrepancy formula for every \(m\ge2\) and \(a,n\ge1\), together with exact finite-Frobenius length and Hilbert-polynomial formulas. **Nothing remains unresolved for the question.**

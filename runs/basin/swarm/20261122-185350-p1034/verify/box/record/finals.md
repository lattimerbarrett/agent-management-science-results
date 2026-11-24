# agent_1: last reply

The tuple is
\[
\boxed{(d,k_1,k_2,k_3,k_4,k_5,k_6)=(1,0,1,1,1,2,2)}.
\]
In particular, the drop in Alexander degree does **not** give the sequence \(k_j=j-1\).

I give an exact-arithmetic computation certificate below. All divisibility tests in it are over \(\mathbb Q(A,q)\), not numerical samples. Finite-field evaluations are used only to certify **nondivisibility**.

## 1. The colored-pretzel evaluation used

Here is the square-root-free version of the symmetric-color pretzel fusion formula. Specifying it also fixes the framing and crossing conventions needed for the computation.

Put \(h=q-q^{-1}\), and define
\[
U(n)=\frac{\prod_{i=-1}^{n-2}(D_i/h)}{[n]!},
\qquad
d_r=\frac{\prod_{i=0}^{r-1}(D_i/h)}{[r]!}.
\]
Empty products are \(1\). The two sets of fusion-channel dimensions are
\[
\begin{split}
\Delta_{r,m}
&=\frac{[2m+1]}{[r+m+1]![r-m]!}
 \prod_{i=0}^{r+m-1}\frac{D_i}{h}
 \prod_{i=-1}^{r-m-2}\frac{D_i}{h},
 \qquad 0\le m\le r,\\
\overline\Delta_0&=1,\\
\overline\Delta_m
&=\frac{D_{2m-1}D_{-1}\prod_{i=0}^{m-2}D_i^2}
 {h^{2m}[m]!^2},
 \qquad m>0.
\end{split}
\]
Define the rational recoupling coefficients
\[
\begin{split}
a^{(r)}_{km}
={}&
\frac{(-1)^{r+k+m}[2m+1]([k]![m]!)^2[r-k]![r-m]!}
 {[r+k+1]![r+m+1]!}\\
&\quad{}\times
\sum_{z=\max(r+m,r+k)}^{\min(r+k+m,2r)}
\frac{(-1)^z[z+1]!}
 {[2r-z]!\bigl([z-r-k]![z-r-m]![r+k+m-z]!\bigr)^2}
\frac{U(r-m)U(z+1)}
 {U(r+k+1)U(z-r-m)}
\end{split}
\]
and
\[
b^{(r)}_{km}
=\frac{\overline\Delta_m}{\Delta_{r,k}}a^{(r)}_{mk},
\qquad
\mu_m=(-Aq^{m-1})^m.
\]

The odd-antiparallel pretzel fusion formula is
\[
\boxed{\quad
H_r\bigl(P(p_1,\ldots,p_s)\bigr)
=
\frac1{d_r}\sum_{k=0}^r\Delta_{r,k}
 \prod_{\nu=1}^s
 \left(\sum_{m=0}^r b^{(r)}_{km}\mu_m^{p_\nu}\right),
\quad}                                                    \tag{1}
\]
when \(s\) and all the \(p_\nu\) are odd, as here.

For completeness, the recoupling input behind (1) is the usual symmetric-color quantum Racah evaluation: the channels in \([r]\otimes[r]\) are \([r+m,r-m]\), with dimensions \(\Delta_{r,m}\); those in \([r]\otimes\overline{[r]}\) have dimensions \(\overline\Delta_m\). In rationally normalized trivalent bases, the change-of-channel matrix is \(a\), and its inverse is its dimension-weighted transpose \(b\). The displayed factorial sum is the symmetric-color Racah coefficient in this normalization. Inserting these channel resolutions at each box gives its finger coefficient
\(\sum_m b_{km}\mu_m^{p}\). Gluing the fingers gives the trace \(\Delta_{r,k}\), and reduction divides by \(d_r\), proving (1).

These conventions can also be checked without any square-root choices:
\[
ab=I,\qquad a^{(r)}_{0m}=\frac{\Delta_{r,m}}{d_r},
\]
and the one-crossing fingers satisfy
\[
\sum_m b^{(r)}_{km}\mu_m^{\pm1}
=
\left((-1)^{r-k}A^r q^{r^2-k(k+1)}\right)^{\pm1}.       \tag{2}
\]
The latter are the zero-framed inverse parallel-braid eigenvalues. This is the appropriate sign here: in the oriented odd pretzel the strands in each box are oppositely oriented. For example, (1) gives
\[
H_1(P(1,1,1))=A^2(q^2+q^{-2})-A^4.
\]
Thus (1) uses the box convention in the question, not an independently chosen convention for the sign of an oriented crossing. The code also checks the identities above for every color used.

## 2. Exact results and why they determine the maxima

Apply (1) with \((-3,-3,3,5,7)\), and then solve the triangular identities in the question, in increasing order of \(r\).

For the resulting values, put
\[
Z_j=\frac{G_j}{\prod_{i=0}^{k_j-1}D_i}.
\]
The exact computation gives the following certificates. Denominators are listed up to an overall sign.

\[
\begin{array}{c|c|r|c|r}
j&k_j&
\#\text{ terms in numerator of }Z_j&
\text{denominator of }Z_j&
 Z_j(2^{-k_j},2)\pmod {1009}\\ \hline
1&0&24&q^2A^2&2\\
2&1&155&q^{12}A^4&62\\
3&1&507&q^{31}A^7&625\\
4&1&1229&q^{59}A^{10}&856\\
5&2&2251&q^{95}A^{12}&915\\
6&2&3963&q^{141}A^{15}&599
\end{array}                                                    \tag{3}
\]

Every denominator in (3) is a monomial, so every \(Z_j\) belongs to \(R\). This proves the required divisibility.

On the other hand, if \(D_{k_j}\) divided \(Z_j\) in \(R\), then \(Z_j\) would vanish at \(A=q^{-k_j}\). Each last-column entry is nonzero. These evaluations are legitimate because the denominators are monomials and \(2\ne0\) in \(\mathbb F_{1009}\). They prove that the next factor does not divide. Any longer initial product would contain that next factor, so the values of \(k_j\) in (3) are maximal.

At \(A=1\), the same exact computation gives
\[
H_1(1,q)=5-2(q^2+q^{-2}).
\]
Consequently
\[
\Delta_K(t)=5-2(t+t^{-1}),\qquad d=1.                    \tag{4}
\]
This is symmetric and has value \(1\) at \(t=1\), as required.

## 3. Reproducible Python certificate

The following is Python using SageMath, with no external files or additional packages needed. It constructs the rational functions, solves all six triangular equations, verifies Laurentness and maximality, checks the recoupling normalizations, and checks (4).

```python
from sage.all import *
from functools import lru_cache

# Everything through the divisibility tests is exact over QQ.
P = PolynomialRing(QQ, names=("q", "A"))
E = P.fraction_field()
q, A = map(E, P.gens())
h = q - 1/q

sage_prod = prod
def product(xs):
    return sage_prod(xs, E(1))

@lru_cache(None)
def bracket(n):
    return (q**n - q**(-n))/h

@lru_cache(None)
def factorial(n):
    assert n >= 0
    return product(bracket(i) for i in range(1, n+1))

def D(i):
    return A*q**i - 1/(A*q**i)

@lru_cache(None)
def U(n):
    assert n >= 0
    return product(D(i)/h for i in range(-1, n-1))/factorial(n)

@lru_cache(None)
def dimension(r):
    return product(D(i)/h for i in range(r))/factorial(r)

@lru_cache(None)
def Delta(r, m):
    return (
        bracket(2*m+1)
        * product(D(i)/h for i in range(r+m))
        * product(D(i)/h for i in range(-1, r-m-1))
        / (factorial(r+m+1)*factorial(r-m))
    )

@lru_cache(None)
def barDelta(m):
    if m == 0:
        return E(1)
    return (
        D(2*m-1)*D(-1)
        * product(D(i)**2 for i in range(m-1))
        / (h**(2*m)*factorial(m)**2)
    )

@lru_cache(None)
def a(r, k, m):
    prefactor = (
        (-1)**(r+k+m)*bracket(2*m+1)
        * (factorial(k)*factorial(m))**2
        * factorial(r-k)*factorial(r-m)
        / (factorial(r+k+1)*factorial(r+m+1))
    )
    ans = E(0)
    for z in range(max(r+m, r+k), min(r+k+m, 2*r)+1):
        ans += (
            (-1)**z*factorial(z+1)
            / (
                factorial(2*r-z)
                * (
                    factorial(z-r-k)
                    * factorial(z-r-m)
                    * factorial(r+k+m-z)
                )**2
            )
            * U(r-m)*U(z+1)/(U(r+k+1)*U(z-r-m))
        )
    return prefactor*ans

@lru_cache(None)
def b(r, k, m):
    return barDelta(m)*a(r, m, k)/Delta(r, k)

def mu(m):
    return (-A*q**(m-1))**m

def finger(r, k, p):
    return sum(b(r, k, m)*mu(m)**p for m in range(r+1))

@lru_cache(None)
def H(r):
    parameters = (-3, -3, 3, 5, 7)
    return (
        sum(
            Delta(r, k)
            * product(finger(r, k, p) for p in parameters)
            for k in range(r+1)
        )
        / dimension(r)
    )

def coefficient(r, j):
    return (
        factorial(r)/(factorial(j)*factorial(r-j))
        * D(-1)
        * product(D(r+i-1) for i in range(1, j+1))
    )

def is_laurent(x):
    # A reduced rational function is Laurent iff its denominator
    # is a nonzero monomial.
    return len(x.denominator().monomials()) == 1

F = GF(1009)
def nonzero_witness(x, k):
    values = (F(2), F(2)**(-k))  # variable order is q, A
    n = x.numerator().change_ring(F)(*values)
    d = x.denominator().change_ring(F)(*values)
    assert d != 0
    return n/d

G = {}
computed_k = []
certificate = []

for r in range(1, 7):
    # Solve the triangular identity, rather than assuming any
    # formula or factorization pattern for G_r.
    remainder = H(r) - 1
    for j in range(1, r):
        remainder -= coefficient(r, j)*G[j]
    G[r] = remainder/coefficient(r, r)

    assert H(r) == 1 + sum(
        coefficient(r, j)*G[j] for j in range(1, r+1)
    )
    assert G[r] != 0
    assert is_laurent(H(r))
    assert is_laurent(G[r])

    # Find the initial differential product exactly.
    z = G[r]
    k = 0
    while (
        z.numerator()(q=q, A=q**(-k)) == 0
        and z.numerator()(q=q, A=-q**(-k)) == 0
    ):
        z /= D(k)
        k += 1

    # This is an exact divisibility certificate.
    assert is_laurent(z)
    assert G[r] == product(D(i) for i in range(k))*z

    # This proves that the next differential does not divide.
    witness = nonzero_witness(z, k)
    assert witness != 0

    computed_k.append(k)
    certificate.append((
        r, k, len(z.numerator().monomials()),
        str(z.denominator()), ZZ(witness)
    ))

    # Exact checks on the recoupling normalization.
    assert sum(Delta(r, k) for k in range(r+1)) == dimension(r)**2
    assert sum(barDelta(k) for k in range(r+1)) == dimension(r)**2

    for k in range(r+1):
        assert a(r, 0, k) == Delta(r, k)/dimension(r)
        eigenvalue = (-1)**(r-k)*A**r*q**(r*r-k*(k+1))
        for p in (-1, 1):
            assert finger(r, k, p) == eigenvalue**p

    for k in range(r+1):
        for ell in range(r+1):
            assert sum(
                a(r, k, m)*b(r, m, ell) for m in range(r+1)
            ) == ZZ(k == ell)

# Alexander polynomial and its normalization.
alexander_q = H(1)(A=1)
assert alexander_q == 5 - 2*(q**2 + q**(-2))
assert alexander_q(q=1) == 1

T = LaurentPolynomialRing(QQ, "t")
t = T.gen()
alexander_t = 5 - 2*(t + t**(-1))
assert alexander_t(t=1) == 1
assert alexander_t == alexander_t(t=t**(-1))
d = max(alexander_t.exponents())

print("j, k_j, numerator terms of Z_j, denominator, witness")
for row in certificate:
    print(row)
print("tuple =", (d, *computed_k))
```

The computed last line is
```text
tuple = (1, 0, 1, 1, 1, 2, 2)
```

Thus the Alexander degree, all six divisibilities, and the failure of every next differential factor have been proved. Nothing remains for the tuple asked for.
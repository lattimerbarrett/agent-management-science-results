# agent_1: the whole run

[user message]
Let
\[
F=(f_1,f_2,f_3)=(y,zy-x^2,z^2+x^2y+zy^2+x^3),\qquad f=f_1f_2f_3.
\]
Consider the parameter hyperplane
\[
H=\{(s_1,s_2,s_3)\in\mathbb C^3:2s_1+6s_2+8s_3+27=0\}.
\]
For \(s\in H\), write \(\beta=s_2+1\) and \(\gamma=s_3+1\). Let \(U\subset H\) consist of the parameters satisfying
\[
\beta,\ \gamma,\ \beta+\gamma+\tfrac32,\ \beta+2\gamma+\tfrac32,\ 2(\beta+\gamma+1)\notin\mathbb Z.
\]

Let \(a,c\) be independent indeterminates, put
\[
Q_2=c-a^{-1},\qquad Q_3=c^2+c+a^{-1},
\]
and define the localization
\[
R=\mathbb C[a,a^{-1},c,c^{-1},Q_2^{-1},Q_3^{-1},(c+a^{-1})^{-1}].
\]
Write \(\Omega_R^j\) for the algebraic differential \(j\)-forms over \(\mathbb C\), with exterior differential \(d\). For each \(s\in U\), set
\[
\theta_s=-\frac{27}{2}\frac{da}{a}+s_2\frac{dQ_2}{Q_2}+s_3\frac{dQ_3}{Q_3},
\qquad
\mathcal H_s=\frac{\Omega_R^2}{\{d\eta+\theta_s\wedge\eta:\eta\in\Omega_R^1\}},
\]
where the quotient is taken as a complex vector space.

For an independent formal variable \(b\), define a complex-linear map \(J_s:\mathbb C[x,y,z]\to\mathcal H_s\) by
\[
J_s(\psi)=\left[-a^3[b^{18}]\left(\psi(ab^3,ab^2,a^2b^4c)\left(1+\frac{a^{-1}b}{Q_3}\right)^{s_3}\right)\,da\wedge dc\right].
\]
Here \([b^{18}]\) denotes coefficient extraction in \(R[[b]]\), the outer brackets denote the class in \(\mathcal H_s\), and formal powers are interpreted by
\[
(1+T)^{s_3}=\sum_{n\ge0}\frac{s_3(s_3-1)\cdots(s_3-n+1)}{n!}T^n,
\]
with empty product equal to \(1\). Define
\[
W_s=\operatorname{span}_{\mathbb C}\{J_s(f\psi):\psi\in\mathbb C[x,y,z]\}\subseteq\mathcal H_s.
\]
Let \(\mathcal E\) be the Zariski closure in \(\mathbb C^3\) of
\[
\{s\in U:W_s\ne\mathcal H_s\}.
\]
What is the reduced Gröbner basis of the vanishing ideal \(I(\mathcal E)\subset\mathbb C[s_1,s_2,s_3]\) for the lexicographic monomial order \(s_1\succ s_2\succ s_3\)?

The answer was proved recently, so it is not an open problem: your task is to find it and prove it, completely, and to write Python that really computes or checks every step that can be checked. Printing what you believe is not evidence. Arriving at an answer that settles less than the question asks (a partial or conditional answer, "not known") is not acceptable, and neither is conceding: when an approach fails, try another.

Proving it means showing that the answer is right in every case the question covers, and that no other answer is.

Stop only when your proof is complete. When you stop, write in that response what you proved, and what is left.

## response 1
[tool call: read_scratchpad]

[tool result]
```
(scratchpad.py is empty)
```

## response 2
[reasoning summary]
**Evaluating symbolic checks**

I'm considering how to handle a finite symbolic lemma check in general, especially for rational proofs in 1D. I'm thinking of checking leading coefficients and doing calculations through symbolic identities. I must be careful not to overpromise on the analytic proof's countability—code isn't necessary for now. Instead, I plan to run a robust script to manage this effectively. Just aiming to keep everything clear and straightforward!

[tool call: write_scratchpad]
content:
```
import sympy as sp
B,G = sp.symbols('B G')
t,c,u,v,a,b,x,y,z = sp.symbols('t c u v a b x y z')
s1,s2,s3=sp.symbols('s1 s2 s3')
half=sp.Rational(1,2)
def check(expr):
    assert sp.cancel(expr)==0, sp.factor(expr)
P=c-t; Q=c*c+c+t
# Coordinate maps, inverse maps, and all factors defining the localizations.
forward={t:u*(1+u)*v,c:(1+u)*v}
inverse={u:t/c,v:c*c/(c+t)}
for w in (u,v): check(w.subs(inverse).subs(forward, simultaneous=True)-w)
for w in (t,c): check(w.subs(forward).subs(inverse, simultaneous=True)-w)
check(P.subs(forward, simultaneous=True)-(1-u)*(1+u)*v)
check(Q.subs(forward, simultaneous=True)-(1+u)**2*v*(v+1))
check((c+t).subs(forward, simultaneous=True)-(1+u)**2*v)
check((u-1).subs(inverse)+P/c)
check((u+1).subs(inverse)-(c+t)/c)
check((v+1).subs(inverse)-Q/(c+t))
jac=sp.det(sp.Matrix([[sp.diff(forward[w],j) for j in (u,v)] for w in (t,c)]))
check(jac-(1+u)**2*v)
# Pullback of f and every monomial that could contribute.
f=y*(z*y-x*x)*(z*z+x*x*y+z*y*y+x**3)
sub={x:a*b**3,y:a*b**2,z:a*a*b**4*c}
Q2=c-1/a; Q3=c*c+c+1/a
fsub=sp.expand(f.subs(sub, simultaneous=True))
check(fsub-a**8*b**16*Q2*Q3*(1+b/(a*Q3)))
monomials=[(i,j,k) for i in range(7) for j in range(10) for k in range(5) if 3*i+2*j+4*k<=2]
assert monomials==[(0,0,0),(0,1,0)]
# All other monomials have weighted degree >2 and cannot contribute.
formal=sum(sp.prod(G-1-j for j in range(n))/sp.factorial(n)*(b/(a*Q3))**n for n in range(3))
def Jcoefficient(psi):
    return sp.factor(-a**3*sp.expand(fsub*psi.subs(sub, simultaneous=True)*formal).coeff(b,18))
j0=Jcoefficient(sp.Integer(1)); jy=Jcoefficient(y)
check(j0+G*(G-1)/2*a**9*Q2/Q3)
check(jy+a**12*Q2*Q3)
# t=1/a changes the volume by -t^-2; the first gauge is g.
g=P*Q*t**-14
check(jy.subs(a,1/t)*(-t**-2)/g-1)
check(j0.subs(a,1/t)*(-t**-2)/g-G*(G-1)/2*t**3/Q**2)
# Connection after first gauge.
old=[sp.Rational(27,2)/t+(B-1)*sp.diff(P,t)/P+(G-1)*sp.diff(Q,t)/Q,
     (B-1)*sp.diff(P,c)/P+(G-1)*sp.diff(Q,c)/Q]
new=[-half/t+B*sp.diff(P,t)/P+G*sp.diff(Q,t)/Q,
     B*sp.diff(P,c)/P+G*sp.diff(Q,c)/Q]
for i,w in enumerate((t,c)): check(old[i]+sp.diff(g,w)/g-new[i])
C=B+2*G+sp.Rational(3,2)
D=B+G+half
S=2*B+2*G+1
omega_u=-half/u+B/(u-1)+C/(u+1)
omega_v=D/v+G/(v+1)
# Pullback and second gauge, by the Jacobian.
for w,target in [(u,omega_u),(v,omega_v)]:
    pulled=sum(new[i].subs(forward, simultaneous=True)*sp.diff(forward[r],w) for i,r in enumerate((t,c)))
    check(pulled+sp.diff(jac,w)/jac-target)
check((t**3/Q**2).subs(forward, simultaneous=True)-u**3/(u+1)*v/(v+1)**2)
# Explicit one-variable exactness certificates.
Lu=lambda h: sp.diff(h,u)+omega_u*h
Lv=lambda h: sp.diff(h,v)+omega_v*h
Pu=u*(u-1)*(u+1)
check(Lu(Pu)-((S+3)*u*u+(B-C)*u-half))
check(Lu(u*(u-1))-((S+2)*u-half-2*C+2*C/(u+1)))
K=-(D+1)*(D+G+1)/(G*(G-1))
hv=(v/(v+1)+(D+1)/G*v)/(G-1)
check(v/(v+1)**2-K-Lv(hv))
A0=1/(2*(S+3))-1/(4*C)
A1=(C-B)/(S+3)-G/C
hu=Pu/(S+3)-u*(u-1)/(2*C)
check(u**3/(u+1)-A0-A1*u-Lu(hu))
N=6*B+8*G*G+8*G+9
check(A1-N/(4*C*(S+3)))
# Matrix of the two generators in the tensor-product basis (1,u) tensor 1.
M=sp.Matrix([[1,G*(G-1)/2*K*A0],[0,G*(G-1)/2*K*A1]])
check(M.det()+(D+1)*N/(8*(S+3)))
# Nonintegrality conditions imply all nonzero denominators used above.
check(D+1-(B+G+sp.Rational(3,2)))
check(C-(B+2*G+sp.Rational(3,2)))
check(S+1-2*(B+G+1))
check(D+G-(C-1))
# Check the infinite-family leading-coefficient formulas used in the lemma.
lam,k,r=sp.symbols('lam k r')
w=sp.symbols('w', nonzero=True)
check((-k+lam)-(lam-k))
# d(w^-k)+lam/w*w^-k has leading coefficient lam-k.
check((sp.diff(w**(-k),w)+lam/w*w**(-k))*w**(k+1)-(lam-k))
# d(P*z^n)+omega*P*z^n: leading coefficient n+m+sum(lambda).
n=sp.symbols('n')
for roots,ls in [([0,1,-1],[-half,B,C]),([0,-1],[D,G])]:
    Z=sp.symbols('Z'); poly=sp.prod(Z-r for r in roots)
    numerator=sp.diff(poly,Z)+sum(l*sp.cancel(poly/(Z-r)) for r,l in zip(roots,ls))+n*sp.cancel(poly/Z)
    check(sp.Poly(sp.expand(numerator),Z).LC()-(n+len(roots)+sum(ls)))
# Translate, compute the reduced lexicographic Groebner basis, and check ideals.
H=2*s1+6*s2+8*s3+27
Ns=sp.expand(N.subs({B:s2+1,G:s3+1}))
gb=sp.groebner([H,Ns],s1,s2,s3,order='lex')
expected=[s1-4*s3**2-8*s3-2,s2+sp.Rational(4,3)*s3**2+4*s3+sp.Rational(31,6)]
assert list(gb)==expected
for p in [H,Ns]: assert gb.reduce(p)[1]==0
# On the exceptional parabola every excluded condition is nonconstant.
Bcurve=-(8*G**2+8*G+9)/6
conditions=[B,G,B+G+sp.Rational(3,2),B+2*G+sp.Rational(3,2),2*(B+G+1)]
for p in conditions:
    assert sp.Poly(sp.expand(p.subs(B,Bcurve)),G).degree()>0
# Polynomial parametrization verifies that the curve has prime ideal.
par={s3:G-1,s2:Bcurve-1,s1:(4*s3**2+8*s3+2).subs(s3,G-1)}
for p in expected: check(p.subs(par, simultaneous=True))
print('All symbolic checks passed.')
print('Exceptional polynomial in beta,gamma:',N)
print('Generator determinant:',sp.factor(M.det()))
print('Reduced lexicographic Groebner basis:',list(gb))

```

[tool result]
```
Wrote scratchpad.py (110 lines).
```

## response 3
[tool call: run_scratchpad]

[tool result]
```
[exit code 1, 0.4s]
--- stdout ---
(empty)
--- stderr ---
Traceback (most recent call last):
  File "scratchpad.py", line 97, in <module>
    assert list(gb)==expected
           ^^^^^^^^^^^^^^^^^^
AssertionError

```

## response 4
[tool call: edit_scratchpad]
old_string: gb=sp.groebner([H,Ns],s1,s2,s3,order='lex')
new_string: gb=sp.groebner([H,Ns],s1,s2,s3,order='lex',domain=sp.QQ)

[tool result]
```
Edited scratchpad.py (1 replacement).
```

## response 5
[tool call: run_scratchpad]

[tool result]
```
[exit code 0, 0.5s]
--- stdout ---
All symbolic checks passed.
Exceptional polynomial in beta,gamma: 6*B + 8*G**2 + 8*G + 9
Generator determinant: -(2*B + 2*G + 3)*(6*B + 8*G**2 + 8*G + 9)/(32*(B + G + 2))
Reduced lexicographic Groebner basis: [s1 - 4*s3**2 - 8*s3 - 2, s2 + 4*s3**2/3 + 4*s3 + 31/6]

--- stderr ---
(empty)
```

## response 6
[reasoning summary]
**Verifying calculations and code**

I need to verify the determinant prefactor and check the determinant formula. It appears that the determinant format is correct, and I should focus on the dependence on J without needing extra coordinates. 

The final proof alongside the code should ideally fit within 6000 tokens, though there's flexibility with the 14k token limit. I will aim to streamline the code to about 80 lines while ensuring all essential checks are included. The final script will provide clarity on the calculations performed.

**Reviewing final version and definitions**

I need to run a final, concise version or include the original full code, which may be lengthy but is fine. It's important to ensure the scalar definitions for theta and v, as well as the Jacob gauge, are valid and include the necessary units in the localized ring. I should explain the two gauge isomorphism forms and consider the lemma about variable sums. 

I’ll check if the numerator’s leading coefficient enables polynomial dimension independence, ensuring our sums don't vanish and remain valid. All these details are essential for clarity in the proof as we proceed.

**Exploring density and polynomials**

I'm considering the density of gamma, noting that it transcends real and complex numbers. It exists countably but is excluded along a parabola formed by nonconstant rational polynomials, which are infinite. 

I need to address the ideal of prime triangular quotients in C[s3], using Groebner bases with a monic pair of leading elements s1 and s2 that are mutually prime. This ultimately leads to a reduced form directly related to s3.

[message]
The reduced Gröbner basis is
\[
\boxed{\left\{
s_1-4s_3^2-8s_3-2,\qquad
s_2+\frac43s_3^2+4s_3+\frac{31}{6}
\right\}.}
\]

We prove this by identifying \(\mathcal H_s\) with a tensor product of two one-variable twisted de Rham quotients. In these coordinates, the two generators of \(W_s\) admit explicit reductions.

## 1. The two possible generators of \(W_s\)

Throughout, write
\[
B=\beta=s_2+1,\qquad G=\gamma=s_3+1.
\]
Under the substitution in the definition of \(J_s\),
\[
f(ab^3,ab^2,a^2b^4c)
=a^8b^{16}Q_2Q_3\left(1+\frac{a^{-1}b}{Q_3}\right).
\]
The weights of \(x,y,z\) are respectively \(3,2,4\). Thus a monomial \(\psi\) can contribute to \(J_s(f\psi)\) only if its weight is at most \(2\). The only such monomials are \(1,y\). Consequently,
\[
W_s=\operatorname{span}\{J_s(f),J_s(fy)\}.
\]
Coefficient extraction gives
\[
\begin{aligned}
J_s(f)&=\left[-\frac{G(G-1)}2a^9\frac{Q_2}{Q_3}\,da\wedge dc\right],\\
J_s(fy)&=\left[-a^{12}Q_2Q_3\,da\wedge dc\right].
\end{aligned}
\tag{1}
\]

## 2. Coordinates separating the connection

Put
\[
t=a^{-1},\qquad P=c-t,\qquad Q=c^2+c+t.
\]
The original connection form becomes
\[
\theta=\frac{27}{2}\frac{dt}{t}
 +(B-1)\frac{dP}{P}+(G-1)\frac{dQ}{Q}.
\]
For an invertible element \(g\), division of forms by \(g\) identifies the connection \(\theta\) with \(\theta+d\log g\). Take
\[
g=t^{-14}PQ.
\]
The new connection is
\[
\theta'=-\frac12\frac{dt}{t}+B\frac{dP}{P}+G\frac{dQ}{Q}.
\]
Since \(da=-t^{-2}dt\), the two classes in (1), after this identification, are
\[
[dt\wedge dc],\qquad
\frac{G(G-1)}2\left[\frac{t^3}{Q^2}\,dt\wedge dc\right],
\tag{2}
\]
in the order \(J_s(fy),J_s(f)\).

Now set
\[
u=\frac tc,\qquad v=\frac{c^2}{c+t}.
\]
Their inverse formulas are
\[
c=(1+u)v,\qquad t=u(1+u)v.
\]
In particular,
\[
\begin{aligned}
P&=(1-u)(1+u)v,\\
Q&=(1+u)^2v(v+1),\\
c+t&=(1+u)^2v,\\
dt\wedge dc&=(1+u)^2v\,du\wedge dv.
\end{aligned}
\tag{3}
\]
These formulas identify the ring \(R\) with
\[
A_u\otimes_{\mathbb C}A_v,
\]
where
\[
\begin{aligned}
A_u&=\mathbb C[u,u^{-1},(u-1)^{-1},(u+1)^{-1}],\\
A_v&=\mathbb C[v,v^{-1},(v+1)^{-1}].
\end{aligned}
\]

Apply one more gauge identification, dividing by the Jacobian
\[
h=(1+u)^2v.
\]
Define
\[
C=B+2G+\frac32,\qquad D=B+G+\frac12.
\]
The resulting connection separates:
\[
\omega=\omega_u+\omega_v,
\]
with
\[
\omega_u=-\frac12\frac{du}{u}
 +B\frac{du}{u-1}+C\frac{du}{u+1},
\qquad
\omega_v=D\frac{dv}{v}+G\frac{dv}{v+1}.
\tag{4}
\]
The generators (2) become
\[
[du\wedge dv],\qquad
\frac{G(G-1)}2
\left[\frac{u^3}{u+1}\frac{v}{(v+1)^2}\,du\wedge dv\right].
\tag{5}
\]

## 3. The dimensions and bases, valid for every \(s\in U\)

We use the following elementary reduction fact.

**One-variable reduction lemma.** Let
\[
A=\mathbb C[z,(z-r_1)^{-1},\ldots,(z-r_m)^{-1}],\qquad
L=\frac d{dz}+\sum_{i=1}^m\frac{\lambda_i}{z-r_i}.
\]
If every \(\lambda_i\) and also \(\Lambda=\sum_i\lambda_i\) is nonintegral, then
\[
A/L(A)
\]
has basis \(1,z,\ldots,z^{m-2}\).

Indeed, a pole of order \(k\ge2\) can be eliminated using \(L((z-r_i)^{-(k-1)})\), whose leading coefficient at that pole is
\(\lambda_i-(k-1)\ne0\). Simple poles can then be eliminated using polynomial interpolation and \(\lambda_i\ne0\).

Conversely, if \(L(h)\) is polynomial, the same leading-pole argument shows that \(h\) is polynomial. Absence of simple poles then forces
\[
h=\prod_i(z-r_i)\,q(z).
\]
For \(q\) of degree \(n\), its image has degree \(n+m-1\), with leading coefficient multiplied by
\[
n+m+\Lambda\ne0.
\]
Thus precisely the asserted polynomial basis remains.

Apply the lemma to (4). For the \(u\)-connection the residues are
\[
-\frac12,\ B,\ C,
\]
whose sum is
\[
S:=2B+2G+1.
\]
For the \(v\)-connection they are \(D,G\), whose sum is \(C-1\).

Every required nonintegrality follows from the definition of \(U\):
\[
B,\ G,\ D,\ C,\ S\notin\mathbb Z.
\]
Therefore the one-variable quotients have bases
\[
\{[du],[u\,du]\},\qquad \{[dv]\},
\]
respectively.

The top-degree quotient of the separated complex is their tensor product: explicitly, its relations are
\[
L_u(A_u)\otimes A_v+A_u\otimes L_v(A_v).
\]
Hence
\[
\dim_{\mathbb C}\mathcal H_s=2
\]
for every \(s\in U\), with basis represented in the final coordinates by
\[
du\wedge dv,\qquad u\,du\wedge dv.
\tag{6}
\]

## 4. Exact reductions of the generators

Write
\[
L_u=\frac d{du}-\frac1{2u}+\frac B{u-1}+\frac C{u+1},
\qquad
L_v=\frac d{dv}+\frac Dv+\frac G{v+1}.
\]

First, in the \(v\)-quotient,
\[
\left[\frac{v}{(v+1)^2}\right]=K[1],
\qquad
K=-\frac{(D+1)(D+G+1)}{G(G-1)}.
\tag{7}
\]
An explicit exactness certificate is
\[
\frac{v}{(v+1)^2}-K
=L_v\left(
\frac{\displaystyle\frac v{v+1}+\frac{D+1}{G}v}{G-1}
\right).
\]
All denominators here are nonzero on \(U\).

For the \(u\)-reduction, let \(P_u=u(u-1)(u+1)\). Direct differentiation gives
\[
\begin{aligned}
L_u(P_u)&=(S+3)u^2+(B-C)u-\frac12,\\
L_u(u(u-1))&=(S+2)u-\frac12-2C+\frac{2C}{u+1}.
\end{aligned}
\]
It follows that
\[
\left[\frac{u^3}{u+1}\right]=A_0[1]+A_1[u],
\tag{8}
\]
where
\[
A_0=\frac1{2(S+3)}-\frac1{4C},
\qquad
A_1=\frac{C-B}{S+3}-\frac GC.
\]
More explicitly,
\[
\frac{u^3}{u+1}-A_0-A_1u
=L_u\left(\frac{P_u}{S+3}-\frac{u(u-1)}{2C}\right).
\]
The coefficient determining linear independence is
\[
A_1=
\frac{6B+8G^2+8G+9}{4C(S+3)}.
\tag{9}
\]

Relative to (6), the columns of the two generators in (5) form the matrix
\[
M=
\begin{pmatrix}
1&\dfrac{G(G-1)}2KA_0\\[2mm]
0&\dfrac{G(G-1)}2KA_1
\end{pmatrix}.
\]
Since \(D+G+1=C\), its determinant simplifies to
\[
\det M
=-\frac{(D+1)(6B+8G^2+8G+9)}{8(S+3)}.
\tag{10}
\]
On \(U\), both \(D+1\) and \(S+3\) are nonzero. We have therefore proved the exact, pointwise equivalence
\[
\boxed{\quad
W_s\ne\mathcal H_s
\iff
6\beta+8\gamma^2+8\gamma+9=0,
\qquad s\in U.
\quad}
\tag{11}
\]

## 5. Closure and reduced Gröbner basis

In the original parameters, the polynomial in (11) is
\[
N=6s_2+8s_3^2+24s_3+31.
\]
Thus the exceptional parameters in \(U\) lie on the curve
\[
2s_1+6s_2+8s_3+27=0,\qquad N=0.
\tag{12}
\]

They are Zariski dense in this curve. To see this, parametrize it by \(G=\gamma\), with
\[
B=-\frac{8G^2+8G+9}{6}.
\]
Each of
\[
B,\quad G,\quad B+G+\frac32,\quad B+2G+\frac32,\quad 2(B+G+1)
\]
is then a nonconstant polynomial in \(G\) with rational coefficients. The excluded integrality conditions remove only countably many values of \(G\), so the remaining set is infinite and hence Zariski dense in this affine line.

Consequently, \(\mathcal E\) is exactly the curve (12). Solving its equations gives
\[
s_2=-\frac43s_3^2-4s_3-\frac{31}{6},
\qquad
s_1=4s_3^2+8s_3+2.
\]
Its ideal is prime, since the coordinate ring is \(\mathbb C[s_3]\). The two displayed monic equations have leading monomials \(s_1,s_2\), and their tails involve only \(s_3\). They therefore constitute the reduced lexicographic Gröbner basis stated above.

## 6. Executable symbolic verification

The following Python/SymPy code checks the coordinate inverses, localization factors, Jacobian, coefficient extraction, both gauge transformations, exactness certificates, determinant, nonintegrality expressions, density-polynomial conditions, and Gröbner basis. It was executed successfully.

```python
import sympy as sp

B, G = sp.symbols("B G")
t, c, u, v, a, b, x, y, z = sp.symbols("t c u v a b x y z")
s1, s2, s3 = sp.symbols("s1 s2 s3")
half = sp.Rational(1, 2)

def check(expr):
    assert sp.cancel(expr) == 0, sp.factor(expr)

P = c - t
Q = c*c + c + t

# Coordinate maps and inverse maps.
forward = {t: u*(1+u)*v, c: (1+u)*v}
inverse = {u: t/c, v: c*c/(c+t)}

for w in (u, v):
    check(w.subs(inverse).subs(forward, simultaneous=True) - w)
for w in (t, c):
    check(w.subs(forward).subs(inverse, simultaneous=True) - w)

# Factors defining the localizations.
check(P.subs(forward, simultaneous=True) - (1-u)*(1+u)*v)
check(Q.subs(forward, simultaneous=True) - (1+u)**2*v*(v+1))
check((c+t).subs(forward, simultaneous=True) - (1+u)**2*v)
check((u-1).subs(inverse) + P/c)
check((u+1).subs(inverse) - (c+t)/c)
check((v+1).subs(inverse) - Q/(c+t))

jac = sp.det(sp.Matrix([
    [sp.diff(forward[w], j) for j in (u, v)]
    for w in (t, c)
]))
check(jac - (1+u)**2*v)

# Pullback of f and the two possible contributing monomials.
f = y*(z*y-x*x)*(z*z+x*x*y+z*y*y+x**3)
sub = {x: a*b**3, y: a*b**2, z: a*a*b**4*c}
Q2 = c - 1/a
Q3 = c*c + c + 1/a
fsub = sp.expand(f.subs(sub, simultaneous=True))
check(fsub - a**8*b**16*Q2*Q3*(1+b/(a*Q3)))

monomials = [
    (i, j, k)
    for i in range(7) for j in range(10) for k in range(5)
    if 3*i + 2*j + 4*k <= 2
]
assert monomials == [(0, 0, 0), (0, 1, 0)]

# Only terms through b^2 in the formal power can contribute.
formal = sum(
    sp.prod(G-1-j for j in range(n))/sp.factorial(n)
    * (b/(a*Q3))**n
    for n in range(3)
)

def Jcoefficient(psi):
    expression = fsub * psi.subs(sub, simultaneous=True) * formal
    return sp.factor(-a**3 * sp.expand(expression).coeff(b, 18))

j0 = Jcoefficient(sp.Integer(1))
jy = Jcoefficient(y)
check(j0 + G*(G-1)/2*a**9*Q2/Q3)
check(jy + a**12*Q2*Q3)

# First gauge and transformation of the two forms.
g = P*Q*t**-14
check(jy.subs(a, 1/t)*(-t**-2)/g - 1)
check(j0.subs(a, 1/t)*(-t**-2)/g
      - G*(G-1)/2*t**3/Q**2)

old = [
    sp.Rational(27, 2)/t
    + (B-1)*sp.diff(P, t)/P + (G-1)*sp.diff(Q, t)/Q,
    (B-1)*sp.diff(P, c)/P + (G-1)*sp.diff(Q, c)/Q
]
new = [
    -half/t + B*sp.diff(P, t)/P + G*sp.diff(Q, t)/Q,
    B*sp.diff(P, c)/P + G*sp.diff(Q, c)/Q
]
for i, w in enumerate((t, c)):
    check(old[i] + sp.diff(g, w)/g - new[i])

C = B + 2*G + sp.Rational(3, 2)
D = B + G + half
S = 2*B + 2*G + 1
omega_u = -half/u + B/(u-1) + C/(u+1)
omega_v = D/v + G/(v+1)

# Coordinate pullback and second gauge.
for w, target in [(u, omega_u), (v, omega_v)]:
    pulled = sum(
        new[i].subs(forward, simultaneous=True)
        * sp.diff(forward[r], w)
        for i, r in enumerate((t, c))
    )
    check(pulled + sp.diff(jac, w)/jac - target)

check((t**3/Q**2).subs(forward, simultaneous=True)
      - u**3/(u+1)*v/(v+1)**2)

# Exactness certificates.
Lu = lambda h: sp.diff(h, u) + omega_u*h
Lv = lambda h: sp.diff(h, v) + omega_v*h
Pu = u*(u-1)*(u+1)

check(Lu(Pu) - ((S+3)*u*u + (B-C)*u - half))
check(Lu(u*(u-1))
      - ((S+2)*u - half - 2*C + 2*C/(u+1)))

K = -(D+1)*(D+G+1)/(G*(G-1))
hv = (v/(v+1) + (D+1)/G*v)/(G-1)
check(v/(v+1)**2 - K - Lv(hv))

A0 = 1/(2*(S+3)) - 1/(4*C)
A1 = (C-B)/(S+3) - G/C
hu = Pu/(S+3) - u*(u-1)/(2*C)
check(u**3/(u+1) - A0 - A1*u - Lu(hu))

N = 6*B + 8*G*G + 8*G + 9
check(A1 - N/(4*C*(S+3)))

M = sp.Matrix([
    [1, G*(G-1)/2*K*A0],
    [0, G*(G-1)/2*K*A1]
])
check(M.det() + (D+1)*N/(8*(S+3)))

# Expressions used to apply the nonintegrality assumptions.
check(D+1 - (B+G+sp.Rational(3, 2)))
check(C - (B+2*G+sp.Rational(3, 2)))
check(S+1 - 2*(B+G+1))
check(D+G - (C-1))

# Symbolic leading coefficients in the one-variable lemma.
lam, k = sp.symbols("lam k")
w = sp.symbols("w", nonzero=True)
check(
    (sp.diff(w**(-k), w) + lam/w*w**(-k))*w**(k+1)
    - (lam-k)
)

n, Z = sp.symbols("n Z")
for roots, residues in [
    ([0, 1, -1], [-half, B, C]),
    ([0, -1], [D, G])
]:
    poly = sp.prod(Z-r for r in roots)
    numerator = (
        sp.diff(poly, Z)
        + sum(l*sp.cancel(poly/(Z-r))
              for r, l in zip(roots, residues))
        + n*sp.cancel(poly/Z)
    )
    check(
        sp.Poly(sp.expand(numerator), Z).LC()
        - (n + len(roots) + sum(residues))
    )

# Original parameter equations and reduced lex Groebner basis.
H = 2*s1 + 6*s2 + 8*s3 + 27
Ns = sp.expand(N.subs({B: s2+1, G: s3+1}))
gb = sp.groebner(
    [H, Ns], s1, s2, s3, order="lex", domain=sp.QQ
)
expected = [
    s1 - 4*s3**2 - 8*s3 - 2,
    s2 + sp.Rational(4, 3)*s3**2 + 4*s3
       + sp.Rational(31, 6)
]
assert list(gb) == expected
for p in [H, Ns]:
    assert gb.reduce(p)[1] == 0

# None of the excluded conditions is constant on the curve.
Bcurve = -(8*G**2 + 8*G + 9)/6
conditions = [
    B, G, B+G+sp.Rational(3, 2),
    B+2*G+sp.Rational(3, 2), 2*(B+G+1)
]
for p in conditions:
    assert sp.Poly(sp.expand(p.subs(B, Bcurve)), G).degree() > 0

# Verify the curve parametrization.
par = {
    s3: G-1,
    s2: Bcurve-1,
    s1: (4*s3**2 + 8*s3 + 2).subs(s3, G-1)
}
for p in expected:
    check(p.subs(par, simultaneous=True))

print("All symbolic checks passed.")
print("Exceptional polynomial in beta,gamma:", N)
print("Generator determinant:", sp.factor(M.det()))
print("Reduced lexicographic Groebner basis:", list(gb))
```

Its output is
```text
All symbolic checks passed.
Exceptional polynomial in beta,gamma: 6*B + 8*G**2 + 8*G + 9
Generator determinant: -(2*B + 2*G + 3)*(6*B + 8*G**2 + 8*G + 9)/(32*(B + G + 2))
Reduced lexicographic Groebner basis: [s1 - 4*s3**2 - 8*s3 - 2, s2 + 4*s3**2/3 + 4*s3 + 31/6]
```

Thus the exceptional condition has been proved for **every parameter in \(U\)**, its Zariski closure has been determined, and the requested reduced Gröbner basis has been computed and checked. Nothing remains unresolved.

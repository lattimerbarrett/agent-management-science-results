# agent_1: the whole run

[user message]
Let \(S^1=\{z\in\mathbb C:|z|=1\}\). A stable complex structure on a closed smooth real \(2n\)-manifold \(M\) means a complex vector-bundle structure \(J\) on
\[
E=TM\oplus(M\times\mathbb R^{2k})
\]
for some integer \(k\ge0\). Here closed means compact without boundary. For a smooth \(S^1\)-action on \(M\), require that its derivative action on \(TM\), extended by the trivial action on the stabilizing \(\mathbb R^{2k}\) fibers, commute with \(J\). Orient \(M\) using the complex orientation of \((E,J)\) and the standard orientation of the stabilizing real summand, and write \(c_j(M,J)=c_j(E,J)\).

Define \(\mathcal E\) to be the set of even integers \(2n\ge16\) for which there exist such an \(M\), an invariant stable complex structure \(J\), and a smooth \(S^1\)-action satisfying both of the following conditions:

1. The set \(M^{S^1}=\{p\in M:z\cdot p=p\text{ for every }z\in S^1\}\) consists of exactly four isolated points.
2. At least one Chern number
\[
\left\langle c_{i_1}(M,J)\cdots c_{i_r}(M,J),[M]\right\rangle,
\qquad r\ge1,\quad i_j\ge1,\quad i_1+\cdots+i_r=n,
\]
is nonzero.

Manifolds may be disconnected, and actions need not be effective. Determine \(\mathcal E\) explicitly.

The answer was proved recently, so it is not an open problem: your task is to find it and prove it, completely, and to write Python that really computes or checks every step that can be checked. Printing what you believe is not evidence. Arriving at an answer that settles less than the question asks (a partial or conditional answer, "not known") is not acceptable, and neither is conceding: when an approach fails, try another.

Proving it means showing that the answer is right in every case the question covers, and that no other answer is.

Stop only when your proof is complete. When you stop, write in that response what you proved, and what is left.

## response 1
[reasoning summary]
**Exploring unitary circle theorems**

I’m looking into the conjectures surrounding the unitary circle, focusing on potentially four fixed nonzero cobordism dimensions like 16, 20, and 24. There's the Kosniowski conjecture regarding unitary manifolds, especially fixed dimensions up to 18. I’m checking recent literature on unitary S1 manifolds, noting the related number theory aspects like vanishing Chern numbers. It’s fascinating how dimensions and properties interconnect, especially concerning stable complexes and exotic spheres. I really need to dig deeper!

**Calculating rigidity and Chern numbers**

I need to calculate using rigidity chi_y and localization with four fixed points, considering the weights that are nonzero integers. From what I gather, chi_y rigid leads to a sum based on those weights. It seems nonzero Chern numbers are linked to weight multisets that remain nonzero in bordism. I’m exploring how the weight structure can utilize universal toric genus rigidity and formal equations. There's a lot of interesting algebraic topology involved here!

[tool call: read_scratchpad]

[tool result]
```
(scratchpad.py is empty)
```

## response 2
[reasoning summary]
**Evaluating mathematical concepts**

I'm considering that if n is high, then it leads to a certain conclusion about SU. I think elliptic rigidity and weak Jacobi forms can provide a bound based on the L1 norm regarding the number of points. However, it seems I might need to clarify or verify my assumptions further, especially around this “up to 4” idea. I wonder how that interacts with the broader context I'm addressing.

[reasoning summary]
**Exploring the theorem's application**

I'm considering whether I can provide a deep theorem and its full application. The user mentioned they recently proved something and could expect to use the "four fixed point theorem." They want a complete proof, and I wonder if citing equivalent parts of the theorem might not fully satisfy them. But I think citing this known result should be acceptable in proving their point mathematically, just confirming my approach here.

[reasoning summary]
**Exploring mathematical concepts**

I'm considering whether scaling in selfmaps can equalize finite ambiguity when dealing with rational maps. However, I wonder if it might not work out, given that the nonlinear actions involved create a homotopy difference that has a nonzero rational denominator, though it's still finite. It seems like scaling could eliminate important aspects in this context, which makes me question the original assumptions I had. I'll need to delve deeper into this!

[reasoning summary]
**Clarifying the theorem's naming**

I think it's important to clarify that we're using the "four-fixed-point theorem" and not just the Kosniowski conjecture. This gives a more accurate description of what we're discussing. I should be careful and not attribute it to a specific individual—saying the "recent four-fixed-point theorem for unitary circle manifolds" feels safe while still being precise. That way, I keep things clear without any risk of misattribution.

[reasoning summary]
**Analyzing algebraic structures**

I’m thinking about how embedding grades can't be directly bounded by certain dimensions because all evaluations lie in R4 but vary in degree. However, I see that orthogonality indicates the total dimension is less than or equal to 4! I also need to define a functional φ on some graded structures while considering various algebraic constraints. It seems there’s a theorem regarding Chern numbers and algebra dimensions that I'm excited to explore further. I’m on the right track!

**Exploring polynomial coefficients**

I'm analyzing cases for n being greater than or equal to 8, where c1 equals zero in structure A. If c1 were nonzero, it might lead to a nilpotent issue, particularly when paired with high-degree generators. I see that the coefficients are crucial, especially in determining χ_y values based on different conditions. There are intricate polynomial relations and properties to consider, especially relating to their degrees and possible vanishings. I’m really trying to classify things accurately here!

[tool call: run_scratchpad]
content:
```
import sympy as S
z,s=S.symbols('z s')
N=20
q={}
# logarithm recurrence
A=[S.S.One]+[s/2]+[S.bernoulli(k)/S.factorial(k) if k%2==0 else 0 for k in range(2,N+1)]
for k in range(1,N+1):
 q[k]=S.expand(A[k]-sum(S.Rational(j,k)*q[j]*A[k-j] for j in range(1,k)))
print(q[3])
print(S.factor(q[9]+3*q[3]*q[6]+S.Rational(3,2)*q[3]**3))
for n in range(8,21):
 ranks=[]
 for a in range(1,n//2+1):
  fs=[q[n],q[a]*q[n-a]]
  if n==3*a: fs.append(q[a]**3)
  mat=S.Matrix([[S.expand(f).coeff(s,k) for f in fs] for k in range(n%2,n+1,2)])
  if mat.rank()<len(fs): print('kernel',n,a,mat.nullspace())

```
timeout_seconds: 60

[tool result]
```
[exit code 0, 0.6s]
(ran it after writing 17 lines)
--- stdout ---
s**3/24 - s/24
0
kernel 9 3 [Matrix([
[2/3],
[  2],
[  1]])]

--- stderr ---
(empty)
```

## response 3
[reasoning summary]
**Exploring polynomial coefficients**

I'm considering checking finite first coefficients at y=-1 to bound n using polynomial systems and inequalities like n≥8 and a≥1. Maybe I could explore the relationships like n=a+b, etc. I wonder if the leading terms of q_n(s) as s approaches infinity depend on both n and Bernoulli numbers. There’s a lot to unpack here, so I’ll need to think over the implications of these relationships and equations further!

[reasoning summary]
**Evaluating mathematical proof**

I'm considering reducing to 2-point residues and proving that n is less than or equal to some value. I think that n being greater than or equal to 8 would likely result in c1 being zero in A using Hattori for each group. It’s a bit of a complex thought, but breaking it down might help clarify my reasoning! I wonder if any distinct examples could help solidify this concept.

[tool call: read_scratchpad]

[tool result]
```
     1	import sympy as S
     2	z,s=S.symbols('z s')
     3	N=20
     4	q={}
     5	# logarithm recurrence
     6	A=[S.S.One]+[s/2]+[S.bernoulli(k)/S.factorial(k) if k%2==0 else 0 for k in range(2,N+1)]
     7	for k in range(1,N+1):
     8	 q[k]=S.expand(A[k]-sum(S.Rational(j,k)*q[j]*A[k-j] for j in range(1,k)))
     9	print(q[3])
    10	print(S.factor(q[9]+3*q[3]*q[6]+S.Rational(3,2)*q[3]**3))
    11	for n in range(8,21):
    12	 ranks=[]
    13	 for a in range(1,n//2+1):
    14	  fs=[q[n],q[a]*q[n-a]]
    15	  if n==3*a: fs.append(q[a]**3)
    16	  mat=S.Matrix([[S.expand(f).coeff(s,k) for f in fs] for k in range(n%2,n+1,2)])
    17	  if mat.rank()<len(fs): print('kernel',n,a,mat.nullspace())

(17 lines total)
```

## response 4
[tool call: write_scratchpad]
content:
```
import sympy as s
from functools import lru_cache
from math import prod

N = s.symbols('N', positive=True, integer=True)
u, A, B, y = s.symbols('u A B y')
a=(1,9,-10)
b=(5,6,-11)
assert sum(a)==sum(b)==0
assert sum(a[i]*a[j] for i in range(3) for j in range(i+1,3)) == -91
assert sum(b[i]*b[j] for i in range(3) for j in range(i+1,3)) == -91
assert prod(a)==-90 and prod(b)==-330
points=[]
for triple, eps in ((a,1),(b,-1)):
    for sign in (1,-1):
        w=[s.Integer(1)]*6+[sign*N*x for x in triple]
        c=s.Poly(prod(1+x*u for x in w),u)
        cs=[c.nth(j) for j in range(10)]
        e=s.prod(w)
        points.append((eps,cs,e))
@lru_cache(None)
def partitions(n, maximum=None):
    if n==0: return ((),)
    if maximum is None: maximum=n
    return tuple((i,)+p for i in range(min(n,maximum),0,-1)
                 for p in partitions(n-i,i))
def residue(part):
    return s.cancel(sum(eps*s.prod(cs[i] for i in part)/e
                        for eps,cs,e in points))
count=0
for degree in range(9):
    for part in partitions(degree):
        assert residue(part)==0, (degree,part,residue(part))
        count+=1
values={p:residue(p) for p in partitions(9)}
nonzero={p:v for p,v in values.items() if v!=0}
assert nonzero == {(3,3,3):-201600*N**6}
# The two fixed points of the standard G2/SU(3) sphere.
fiber=[A,B,1/(A*B)]
def chi_term(ws):
    return s.prod((1+y/w)/(1-1/w) for w in ws)
assert s.factor(chi_term(fiber)+chi_term([1/w for w in fiber])-(y*y-y))==0
# The two base poles have opposite stable-complex signs, so the
# complete equivariant chi_y expression vanishes identically.
base=s.symbols('t', nonzero=True)
base_factor=((1+y/base)/(1-1/base))**6
assert s.cancel(base_factor*((y*y-y)-(y*y-y)))==0
print('Lower-degree localization identities checked:',count)
print('Top-degree Chern numbers checked:',len(values))
print('Nonzero top-degree Chern numbers:',nonzero)
print('The two-point G2-sphere chi_y identity is verified symbolically.')

```

[tool result]
```
Wrote scratchpad.py (51 lines).
```

## response 5
[tool call: run_scratchpad]

[tool result]
```
[exit code 0, 0.4s]
--- stdout ---
Lower-degree localization identities checked: 67
Top-degree Chern numbers checked: 30
Nonzero top-degree Chern numbers: {(3, 3, 3): -201600*N**6}
The two-point G2-sphere chi_y identity is verified symbolically.

--- stderr ---
(empty)
```

## response 6
[tool call: run_scratchpad]
content:
```
import sympy as S
k=S.symbols('k'); z=S.symbols('z')
for r in range(1,6):
    B=sum(S.bernoulli(j)/S.factorial(j)*z**j for j in range(2,2*r+1,2))
    R=0
    for m in range(1,r+1):
        R+=k*2**(2*r)*(-1)**m*S.rf(k-2*r+1,m-1)/S.factorial(m)*S.expand(B**m).coeff(z,2*r)
    print(r,S.factor(R))

```

[tool result]
```
[exit code 0, 0.2s]
(ran it after writing 8 lines)
--- stdout ---
1 -k/3
2 k*(5*k - 13)/90
3 -k*(35*k**2 - 273*k + 502)/5670
4 k*(175*k**3 - 2730*k**2 + 13589*k - 21306)/340200
5 -k*(385*k**4 - 10010*k**3 + 94259*k**2 - 377938*k + 538008)/11226600

--- stderr ---
(empty)
```

## response 7
[reasoning summary]
**Exploring mathematical functions**

I'm considering how to derive explicit G(t) using power series and possibly rational functions in t. This involves some intricate calculations, especially concerning finite order. I want to see how q_n normalized with respect to the root dominant connects to a universal distribution. It seems that the part q_n relates to c_n during the transformation at t, linking to a singularity in the form of Q's zero formula. Each aspect piques my interest!

[tool call: read_scratchpad]

[tool result]
```
     1	import sympy as S
     2	k=S.symbols('k'); z=S.symbols('z')
     3	for r in range(1,6):
     4	    B=sum(S.bernoulli(j)/S.factorial(j)*z**j for j in range(2,2*r+1,2))
     5	    R=0
     6	    for m in range(1,r+1):
     7	        R+=k*2**(2*r)*(-1)**m*S.rf(k-2*r+1,m-1)/S.factorial(m)*S.expand(B**m).coeff(z,2*r)
     8	    print(r,S.factor(R))

(8 lines total)
```

## response 8
[tool call: run_scratchpad]
content:
```
import sympy as S,itertools,pickle
n,h,t=S.symbols('n h t')
K=6
U=2*S.sinh(t/2)/t
L=S.series(S.log(U),t,0,2*K+2).removeO()
Un=S.series(S.exp(n*L),t,0,2*K+2).removeO().expand()
Rs={1:t/2*S.coth(t/2)-1,2:t*t/(4*S.sinh(t/2)**2)+t*t/12-1,3:t**3*S.cosh(t/2)/(8*S.sinh(t/2)**3)-1}
for a,R in Rs.items():
    rr=S.series(R,t,0,2*K+2).removeO()
    P=S.Poly(Un*(1+h*rr),t)
    M=[S.factor(P.nth(2*k)*S.factorial(2*k)) for k in range(K+1)]
    polys=[]
    for inds in itertools.combinations(range(5),3):
        det=S.det(S.Matrix([[M[i+j] for j in inds] for i in range(3)]))
        polys.append(S.fraction(S.factor(det))[0])
    print('a',a,'det0',S.factor(polys[0]),flush=True)
    gb=S.groebner(polys,h,n)
    print('GB:',gb,flush=True)
    print(list(gb),flush=True)

```
timeout_seconds: 300

[tool result]
```
[exit code 0, 1.4s]
(ran it after writing 19 lines)
--- stdout ---
a 1 det0 -98000*h**3*n**3 + 411600*h**3*n**2 - 579040*h**3*n + 266112*h**3 + 110250*h**2*n**4 - 573300*h**2*n**3 + 1051470*h**2*n**2 - 797076*h**2*n + 207360*h**2 + 73500*h*n**5 - 308700*h*n**4 + 503580*h*n**3 - 354564*h*n**2 + 86760*h*n + 6125*n**6 - 25725*n**5 + 41965*n**4 - 29547*n**3 + 7230*n**2
GB: GroebnerBasis([h**2 - 2*h*n + n**2, h*n**2 - h*n - n**3 + n**2, n**4 - 2*n**3 + n**2], h, n, domain='ZZ', order='lex')
[h**2 - 2*h*n + n**2, h*n**2 - h*n - n**3 + n**2, n**4 - 2*n**3 + n**2]
a 2 det0 -381024*h**3 + 158760*h**2*n**2 - 2127384*h**2*n + 3490560*h**2 + 308700*h*n**4 - 1175160*h*n**3 + 1504692*h*n**2 - 539640*h*n + 6125*n**6 - 25725*n**5 + 41965*n**4 - 29547*n**3 + 7230*n**2
GB: GroebnerBasis([4*h**2 - n**2, 2*h*n - n**2, n**3 - 2*n**2], h, n, domain='ZZ', order='lex')
[4*h**2 - n**2, 2*h*n - n**2, n**3 - 2*n**2]
a 3 det0 381024*h**3 + 158760*h**2*n**2 - 2127384*h**2*n + 5071680*h**2 - 308700*h*n**4 + 2015160*h*n**3 - 3974292*h*n**2 + 1661400*h*n + 6125*n**6 - 25725*n**5 + 41965*n**4 - 29547*n**3 + 7230*n**2
GB: GroebnerBasis([9*h**2 - 6*h*n + n**2, 3*h*n**2 - 9*h*n - n**3 + 3*n**2, n**4 - 6*n**3 + 9*n**2], h, n, domain='ZZ', order='lex')
[9*h**2 - 6*h*n + n**2, 3*h*n**2 - 9*h*n - n**3 + 3*n**2, n**4 - 6*n**3 + 9*n**2]

--- stderr ---
(empty)
```

## response 9
[tool call: read_scratchpad]

[tool result]
```
     1	import sympy as S,itertools,pickle
     2	n,h,t=S.symbols('n h t')
     3	K=6
     4	U=2*S.sinh(t/2)/t
     5	L=S.series(S.log(U),t,0,2*K+2).removeO()
     6	Un=S.series(S.exp(n*L),t,0,2*K+2).removeO().expand()
     7	Rs={1:t/2*S.coth(t/2)-1,2:t*t/(4*S.sinh(t/2)**2)+t*t/12-1,3:t**3*S.cosh(t/2)/(8*S.sinh(t/2)**3)-1}
     8	for a,R in Rs.items():
     9	    rr=S.series(R,t,0,2*K+2).removeO()
    10	    P=S.Poly(Un*(1+h*rr),t)
    11	    M=[S.factor(P.nth(2*k)*S.factorial(2*k)) for k in range(K+1)]
    12	    polys=[]
    13	    for inds in itertools.combinations(range(5),3):
    14	        det=S.det(S.Matrix([[M[i+j] for j in inds] for i in range(3)]))
    15	        polys.append(S.fraction(S.factor(det))[0])
    16	    print('a',a,'det0',S.factor(polys[0]),flush=True)
    17	    gb=S.groebner(polys,h,n)
    18	    print('GB:',gb,flush=True)
    19	    print(list(gb),flush=True)

(19 lines total)
```

## response 10
[tool call: run_scratchpad]
content:
```
import sympy as S,itertools
z,s,x=S.symbols('z s x')
N=14
q={}
A=[S.S.One,s/2]+[S.bernoulli(k)/S.factorial(k) if k%2==0 else 0 for k in range(2,N+1)]
for k in range(1,N+1):
 q[k]=S.expand(A[k]-sum(S.Rational(j,k)*q[j]*A[k-j] for j in range(1,k)))
for n in range(8,N+1):
 pairs=[S.Poly(x**i+x**(n-i),x) for i in range(n//2+1)]
 candidates=set()
 for p in pairs:
  candidates.add(tuple(p.nth(i) for i in range(n+1)))
  candidates.add(tuple(-p.nth(i) for i in range(n+1)))
 for p in pairs:
  for r in pairs:
   for a in (-1,1):
    for b in (-1,1):
     pp=a*p+b*r
     candidates.add(tuple(pp.nth(i) for i in range(n+1)))
 zero=(0,)*(n+1)
 candidates.discard(zero)
 hits=[]
 for a in range(1,n//2+1):
  fs=[q[n],q[a]*q[n-a]]
  if n==3*a: fs.append(q[a]**3)
  polys=[]
  for f in fs:
   # y=-x, s=(1+x)/(1-x)
   p=S.Poly(f,s)
   fp=sum(co*(1+x)**k[0]*(1-x)**(n-k[0]) for k,co in p.terms())
   polys.append(S.Poly(fp,x))
  mat=S.Matrix([[p.nth(i) for p in polys] for i in range(n+1)])
  null=mat.T.nullspace()
  for v in candidates:
   vv=S.Matrix(v)
   if all((w.T*vv)[0]==0 for w in null):hits.append((a,v))
  if mat.rank()<len(fs): print('KERNEL',n,a,mat.nullspace())
 print('n',n,'candidates',len(candidates),'nonzero hits',len(hits),hits[:1])

```
timeout_seconds: 60

[tool result]
```
[exit code 0, 0.8s]
(ran it after writing 38 lines)
--- stdout ---
n 8 candidates 60 nonzero hits 0 []
KERNEL 9 3 [Matrix([
[2/3],
[  2],
[  1]])]
n 9 candidates 60 nonzero hits 0 []
n 10 candidates 84 nonzero hits 0 []
n 11 candidates 84 nonzero hits 0 []
n 12 candidates 112 nonzero hits 0 []
n 13 candidates 112 nonzero hits 0 []
n 14 candidates 144 nonzero hits 0 []

--- stderr ---
(empty)
```

## response 11
[tool call: read_scratchpad]
start_line: 1
end_line: 5

[tool result]
```
     1	import sympy as S,itertools
     2	z,s,x=S.symbols('z s x')
     3	N=14
     4	q={}
     5	A=[S.S.One,s/2]+[S.bernoulli(k)/S.factorial(k) if k%2==0 else 0 for k in range(2,N+1)]

(38 lines total)
```

## response 12
[tool call: run_scratchpad]
content:
```
import sympy as S,itertools
n,t=S.symbols('n t'); K=6
U=2*S.sinh(t/2)/t
L=S.series(S.log(U),t,0,14).removeO()
Un=S.series(S.exp(n*L),t,0,14).removeO()
R=S.series(t*S.coth(t/2)/2-1,t,0,14).removeO()
P=S.Poly(Un*R,t)
M=[S.factor(P.nth(2*k)*S.factorial(2*k)) for k in range(K+1)]
polys=[S.fraction(S.factor(S.det(S.Matrix([[M[i+j] for j in inds] for i in range(3)]))))[0] for inds in itertools.combinations(range(5),3)]
print(S.groebner(polys,n))
print([S.factor(p) for p in S.groebner(polys,n)])

```
timeout_seconds: 60

[tool result]
```
[exit code 0, 0.5s]
(ran it after writing 11 lines)
--- stdout ---
GroebnerBasis([1], n, domain='ZZ', order='lex')
[1]

--- stderr ---
(empty)
```

## response 13
[tool call: read_scratchpad]

[tool result]
```
     1	import sympy as S,itertools
     2	n,t=S.symbols('n t'); K=6
     3	U=2*S.sinh(t/2)/t
     4	L=S.series(S.log(U),t,0,14).removeO()
     5	Un=S.series(S.exp(n*L),t,0,14).removeO()
     6	R=S.series(t*S.coth(t/2)/2-1,t,0,14).removeO()
     7	P=S.Poly(Un*R,t)
     8	M=[S.factor(P.nth(2*k)*S.factorial(2*k)) for k in range(K+1)]
     9	polys=[S.fraction(S.factor(S.det(S.Matrix([[M[i+j] for j in inds] for i in range(3)]))))[0] for inds in itertools.combinations(range(5),3)]
    10	print(S.groebner(polys,n))
    11	print([S.factor(p) for p in S.groebner(polys,n)])

(11 lines total)
```

## response 14
[tool call: write_scratchpad]
content:
```
import sympy as S
from itertools import combinations
from functools import lru_cache
from math import prod

# I. Exact finite check: complex dimensions 8,...,14.
s, x = S.symbols('s x')
q = {}
Ac = [S.S.One, s/2] + [S.bernoulli(j)/S.factorial(j)
      if j % 2 == 0 else S.S.Zero for j in range(2,15)]
for j in range(1,15):
    q[j] = S.expand(Ac[j] - sum(S.Rational(i,j)*q[i]*Ac[j-i]
                                for i in range(1,j)))
kernels=[]
spaces=0
for d in range(8,15):
    pairs=[S.Poly(x**i+x**(d-i),x) for i in range(d//2+1)]
    candidates=set()
    for p in pairs:
        for sign in (-1,1):
            candidates.add(tuple(sign*p.nth(i) for i in range(d+1)))
    for p in pairs:
        for r in pairs:
            for e in (-1,1):
                for f in (-1,1):
                    pp=e*p+f*r
                    candidates.add(tuple(pp.nth(i) for i in range(d+1)))
    candidates.discard((0,)*(d+1))
    for a in range(1,d//2+1):
        fs=[q[d],q[a]*q[d-a]]
        if d==3*a:
            fs.append(q[a]**3)
        columns=[]
        for f in fs:
            poly=S.Poly(f,s)
            H=sum(co*(1+x)**mon[0]*(1-x)**(d-mon[0])
                  for mon,co in poly.terms())
            columns.append(S.Poly(H,x))
        C=S.Matrix([[p.nth(i) for p in columns] for i in range(d+1)])
        left=C.T.nullspace()
        for v in candidates:
            vv=S.Matrix(v)
            assert any((w.T*vv)[0] != 0 for w in left), (d,a,v)
        if C.rank()<len(fs):
            kernels.append((d,a))
        spaces+=1
assert kernels==[(9,3)], kernels
assert S.expand(q[9]+3*q[3]*q[6]+S.Rational(3,2)*q[3]**3)==0
print('Finite genus check:',spaces,'spaces; only kernel:',kernels)

# II. Exact finite certificates for ALL complex dimensions >=15.
n,h,t = S.symbols('n h t')
U=2*S.sinh(t/2)/t
logU=S.series(S.log(U),t,0,14).removeO()
Un=S.series(S.exp(n*logU),t,0,14).removeO()
Rs={1:t*S.coth(t/2)/2-1,
    2:t**2/(4*S.sinh(t/2)**2)+t**2/12-1,
    3:t**3*S.cosh(t/2)/(8*S.sinh(t/2)**3)-1}
def minors_of_moments(expr):
    P=S.Poly(expr,t)
    M=[S.factor(P.nth(2*k)*S.factorial(2*k)) for k in range(7)]
    return [S.fraction(S.factor(S.det(S.Matrix(
            [[M[i+j] for j in js] for i in range(3)]))))[0]
            for js in combinations(range(5),3)]
for a in (1,2,3):
    R=S.series(Rs[a],t,0,14).removeO()
    gb=S.groebner(minors_of_moments(Un*(1+h*R)),h,n,domain=S.QQ)
    assert gb.reduce(n**2*(n-a)**2)[1]==0
    print('Moment certificate a =',a,': n^2(n-a)^2 belongs to minor ideal')
R=S.series(Rs[1],t,0,14).removeO()
gb=S.groebner(minors_of_moments(Un*R),n,domain=S.QQ)
assert gb.reduce(S.S.One)[1]==0
print('Zero-Euler a=1 certificate: minor ideal is the unit ideal')

# III. The 18-dimensional construction: symbolic localization for all N.
N,u=S.symbols('N u', positive=True)
alpha=(1,9,-10)
beta=(5,6,-11)
assert sum(alpha)==sum(beta)==0
assert sum(alpha[i]*alpha[j] for i,j in combinations(range(3),2))==-91
assert sum(beta[i]*beta[j] for i,j in combinations(range(3),2))==-91
assert prod(alpha)==-90 and prod(beta)==-330
points=[]
for triple,eps in ((alpha,1),(beta,-1)):
    for sign in (1,-1):
        ws=[S.S.One]*6+[sign*N*v for v in triple]
        cp=S.Poly(prod(1+w*u for w in ws),u)
        points.append((eps,[cp.nth(j) for j in range(10)],S.prod(ws)))
@lru_cache(None)
def parts(d,m=None):
    if d==0: return ((),)
    if m is None: m=d
    return tuple((i,)+p for i in range(min(d,m),0,-1)
                 for p in parts(d-i,i))
def residue(part):
    return S.cancel(sum(eps*S.prod(cs[j] for j in part)/e
                        for eps,cs,e in points))
low=0
for degree in range(9):
    for part in parts(degree):
        assert residue(part)==0
        low+=1
values={p:residue(p) for p in parts(9)}
nonzero={p:v for p,v in values.items() if v!=0}
assert nonzero=={(3,3,3):-201600*N**6}
print('Localization:',low,'lower-degree identities;',len(values),'Chern numbers')
print('Nonzero Chern number:',nonzero)
# Two-point G2-sphere chi_y identity, with two independent characters.
A,B,y=S.symbols('A B y')
fiber=[A,B,1/(A*B)]
def chi_term(ws):
    return S.prod((1+y/w)/(1-1/w) for w in ws)
assert S.factor(chi_term(fiber)+chi_term([1/w for w in fiber])-y*y+y)==0
print('G2-sphere chi_y identity checked.')

```

[tool result]
```
Wrote scratchpad.py (114 lines).
```

## response 15
[tool call: run_scratchpad]
timeout_seconds: 120

[tool result]
```
[exit code 0, 2.3s]
--- stdout ---
Finite genus check: 37 spaces; only kernel: [(9, 3)]
Moment certificate a = 1 : n^2(n-a)^2 belongs to minor ideal
Moment certificate a = 2 : n^2(n-a)^2 belongs to minor ideal
Moment certificate a = 3 : n^2(n-a)^2 belongs to minor ideal
Zero-Euler a=1 certificate: minor ideal is the unit ideal
Localization: 67 lower-degree identities; 30 Chern numbers
Nonzero Chern number: {(3, 3, 3): -201600*N**6}
G2-sphere chi_y identity checked.

--- stderr ---
(empty)
```

## response 16
[message]
\[
\boxed{\mathcal E=\{18\}.}
\]

In particular, the answer is different from what one would obtain by imposing an almost complex structure rather than a stable complex structure. The 18-dimensional examples below have \(\chi_y=0\), but have a nonzero Chern number.

I give a computer-assisted proof. The computations are exact computations over \(\mathbb Q\), not numerical searches. Importantly, the exclusion of arbitrarily large dimensions is reduced to polynomial-ideal certificates with the dimension as an indeterminate.

## 1. Fixed-point formulas and a small Chern-number algebra

Write the complex tangent weights at a fixed point \(p\) as
\[
w_{p,1},\ldots,w_{p,n}\in\mathbb Z\setminus\{0\}.
\]
The stabilizing summand contributes only zero weights. Let \(\epsilon_p\in\{1,-1\}\) compare the orientation in the question with the orientation of the nonzero complex weight spaces. Put
\[
a_{p,j}=e_j(w_{p,1},\ldots,w_{p,n}),\qquad
b_p=\frac{\epsilon_p}{\prod_iw_{p,i}}.
\]

We use the usual equivariant cohomology localization formula and equivariant index formula. These apply to invariant stable complex structures, with precisely the signs \(\epsilon_p\).

### A Chern-number algebra of dimension at most four

Give \(R=\mathbb Q[c_1,c_2,\ldots]\) the grading \(\deg c_j=j\). Let
\[
\varphi:R_n\longrightarrow\mathbb Q
\]
be evaluation as a Chern number of \(M\). Assume that \(\varphi\ne0\).

Define its graded annihilator by
\[
I_d=\{f\in R_d:\varphi(fg)=0\text{ for every }g\in R_{n-d}\},
\]
and set \(A=R/I\), with degrees above \(n\) killed. Then \(A\) is a graded Poincaré-duality algebra with \(A_0=A_n=\mathbb Q\).

Here is the useful fixed-point bound:
\[
\dim_{\mathbb Q}A\le4.                                      \tag{1}
\]

Indeed, evaluate Chern polynomials at the four vectors
\((a_{p,1},a_{p,2},\ldots)\), and let \(F_d\subseteq\mathbb Q^4\) be the span of evaluations of polynomials of weighted degree at most \(d\). Localization says
\[
\sum_p b_p f(a_p)=0\qquad(\deg f<n).
\]
Consequently, if a homogeneous \(f\in R_d\) evaluates into \(F_{d-1}\), then
\[
\varphi(fg)=0\qquad(g\in R_{n-d}).
\]
Thus \(A\) is a quotient of the associated graded algebra of \(F_\bullet\), proving (1).

Classification of such small graded Poincaré-duality algebras is elementary. Because there is only one Chern generator in each degree, their possible positive degrees are
\[
\{n\},\qquad \{a,n\}\ (n=2a),\qquad
\{a,b,n\}\ (a+b=n).
\]
In the last case the only possible extra power is when \(b=2a\).

It follows that, for some \(a\le b\), \(a+b=n\), **all Chern numbers vanish except possibly**
\[
c_n,\quad c_ac_b,                                           \tag{2}
\]
with the additional possibility
\[
c_a^3\quad\text{when }n=3a.                                 \tag{3}
\]
The case in which only \(c_n\) can be nonzero can be included in (2) by assigning zero to the other number.

## 2. The restriction supplied by the \(\chi_y\)-genus

Define \(q_k(y)\) by
\[
\log\left(\frac{Q_y(z)}{1+y}\right)
 =\sum_{k\ge1}q_k(y)z^k,\qquad
Q_y(z)=\frac{z(1+ye^{-z})}{1-e^{-z}}.
\]
If
\[
s=\frac{1-y}{1+y},
\]
then
\[
\frac{Q_y(z)}{1+y}
 =\frac z2\coth\frac z2+\frac{sz}{2}.                         \tag{4}
\]
In particular the \(q_k\) are polynomials in \(s\).

Newton identities, together with (2)–(3), show that
\[
\chi_y(M)\in (1+y)^n
 \operatorname{span}_{\mathbb Q}\{q_n,q_aq_b\},               \tag{5}
\]
with \(q_a^3\) added when \(n=3a\). Before substituting the particular polynomials \(q_k\), the change from the Chern numbers in (2)–(3) to the coefficients in (5) is triangular with nonzero diagonal. Thus linear independence of these polynomials implies that \(\chi_y=0\) forces all the Chern numbers to vanish.

For completeness, the rigidity needed here follows directly from the equivariant index formula. It expresses the equivariant genus as
\[
\sum_p\epsilon_p
 \prod_i\frac{1+yt^{w_{p,i}}}{1-t^{w_{p,i}}}.
\]
Its coefficients are Laurent polynomials in \(t\); the displayed expression is bounded at both \(0\) and \(\infty\). It is therefore constant in \(t\).

Put
\[
H(x)=\chi_{-x}(M).
\]
Taking the two limits gives
\[
H(x)=\sum_p\epsilon_p x^{d_p},
\qquad H(x)=x^nH(x^{-1}),                                   \tag{6}
\]
where \(d_p\) counts negative weights. Hence \(H\) is reciprocal, has integer coefficients, and has coefficient \(\ell^1\)-norm at most four.

Moreover, its middle coefficient, if present, is even: \(H(1)=\sum_p\epsilon_p\) is even, and the other coefficients occur in pairs. Consequently every nonzero possibility in (6) is either one signed polynomial
\[
x^i+x^{n-i},
\]
or a sum of two such signed polynomials, repetitions allowed.

Equivalently,
\[
G(t)=e^{-nt/2}H(e^t)
\]
is a sum of at most two signed terms \(2\cosh(\xi t)\). Thus, writing
\[
M_j=G^{(2j)}(0),
\]
the Hankel matrix
\[
(M_{i+j})_{0\le i\le2,\ 0\le j\le4}                         \tag{7}
\]
has rank at most two.

These restrictions will exclude every \(n\ge8\), except \(n=9\).

## 3. Excluding all \(n\ge15\)

This part is uniform in \(n\).

Set
\[
U(t)=\frac{2\sinh(t/2)}t,\qquad L(t)=\log U(t),
\qquad r_k(t)=-kt^kq_k(-e^t).
\]
A direct expansion of the logarithm defining \(q_k\) gives
\[
q_k(-e^t)
=-\frac1{kt^k}
 +\frac{(-1)^kL^{(k)}(t)-L^{(k)}(0)}{k!}.                  \tag{8}
\]
In particular \(r_k(0)=1\). Its first nonconstant term is
\[
\begin{cases}
\displaystyle
\frac{B_{k+1}}{(k+1)(k-1)!}\,t^{k+1},&k\text{ odd},\\[6pt]
\displaystyle
-\frac{B_{k+2}}{2(k+2)(k-1)!}\,t^{k+2},&k\text{ even}.
\end{cases}                                               \tag{9}
\]
All these coefficients are nonzero.

Let
\[
\kappa=G(0)=\langle c_n,[M]\rangle\in\{-4,-2,0,2,4\}.
\]

### 3.1. The case \(\kappa\ne0\)

Changing all signs, suppose \(\kappa>0\).

If the smaller degree \(a\) in (2) is at least four, (8)–(9) imply
\[
G(t)=\kappa U(t)^n+O(t^6).
\]
The same holds for the cubic case \(n=3a\), \(a\ge5\). Therefore
\[
\frac{G''(0)}{\kappa}=\frac n{12},\qquad
\frac{G^{(4)}(0)}{\kappa}=\frac{n(5n-2)}{240}.              \tag{10}
\]

If \(\kappa=2\), (6) implies \(G=2\cosh(\xi t)\). Equations (10) would require
\[
\xi^2=\frac n{12},\qquad
\xi^4=\frac{n(5n-2)}{240},
\]
which give \(n=3/5\).

If \(\kappa=4\), we have
\[
G=2\cosh(\xi t)+2\cosh(\eta t).
\]
Equations (10) give
\[
\xi^2+\eta^2=\frac n6,\qquad
\xi^4+\eta^4=\frac{n(5n-2)}{120}.
\]
But \(\xi^4+\eta^4\le(\xi^2+\eta^2)^2\), whereas the required difference is
\[
\frac{n(5n-2)}{120}-\frac{n^2}{36}
=\frac{n(5n-6)}{360}>0.
\]
This is impossible.

It remains to handle \(a=1,2,3\) in (2). Since \(n\ge15\), \(b=n-a\ge12\). Formula (8) then gives, through degree twelve,
\[
G(t)=U(t)^n\bigl(\kappa+\lambda R_a(t)\bigr)+O(t^{14}),      \tag{11}
\]
where
\[
\begin{aligned}
R_1&=\frac t2\coth(t/2)-1,\\
R_2&=\frac{t^2}{4\sinh^2(t/2)}+\frac{t^2}{12}-1,\\
R_3&=\frac{t^3\cosh(t/2)}{8\sinh^3(t/2)}-1.
\end{aligned}                                             \tag{12}
\]

Normalize \(\kappa=1\) by dividing \(G\) by \(\kappa\), and put \(h=\lambda/\kappa\). Compute the moments through degree twelve from
\[
U(t)^n(1+hR_a(t)).
\]
The \(3\times3\) minors of (7) must vanish. Exact polynomial-ideal calculation gives the following certificates:
\[
\begin{array}{c|c}
a&\text{polynomial belonging to the ideal of those minors}\\ \hline
1&n^2(n-1)^2\\
2&n^2(n-2)^2\\
3&n^2(n-3)^2.
\end{array}                                               \tag{13}
\]
The code below computes and verifies these ideal-membership assertions. None is compatible with \(n\ge15\).

### 3.2. The case \(\kappa=0\)

Except possibly when \(a=1\), (8)–(9) give \(G(t)=O(t^4)\). But a nonzero polynomial with at most four monomials cannot have a nonzero root of multiplicity four: its first four derivative equations form a Vandermonde system in the four exponents. Thus
\[
\chi_y(M)=0.                                               \tag{14}
\]

When \(a=1\), (11) becomes
\[
G(t)=\lambda U(t)^nR_1(t)+O(t^{14}).
\]
If \(\lambda=0\), the Chern numbers vanish. Otherwise divide by \(\lambda\). The ideal of the minors (7), now calculated from \(U^nR_1\), is the unit ideal. This is another exact certificate verified below. Hence this case is impossible.

We must check that (14) forces the Chern numbers to vanish.

For the two-generator span in (5), a dependence would require
\[
r_n=r_ar_b.
\]
Using (9), the first nonconstant term on the right cannot cancel, except potentially when \(a\) is even and \(b=a+1\). In that case its coefficient is proportional to
\[
-\frac12+\frac1a,
\]
which vanishes only for \((a,b)=(2,3)\), not for \(n\ge15\). Thus the two polynomials are independent.

For the cubic case \(n=3d\), \(d\ge5\), normalize a putative dependence to
\[
A r_{3d}+B r_dr_{2d}+C r_d^3=0.
\]
The constant and first nonconstant terms give
\[
A+B+C=0,\qquad B+3C=0.
\]
If \(d\) is even, the first term of \(r_{2d}-1\), in degree \(2d+2\), forces \(B=0\), and then all coefficients vanish.

If \(d\) is odd, let \(u\) and \(v\) be the leading coefficients of \(r_d-1\) and \(r_{2d}-1\). The degree \(2d+2\) equation gives
\[
C(u^2-v)=0.
\]
The Bernoulli-number formula yields
\[
\frac v{u^2}
=\frac{2d+1}{2d}\frac{\zeta(2d+2)}{\zeta(d+1)^2}>1
\qquad(d\ge5).
\]
Here is an elementary bound proving the strict inequality:
\[
\zeta(d+1)-1
<\frac{d+2}{d\,2^{d+1}}\le\frac1{8d},
\]
so \(\zeta(d+1)^2<1+1/(2d)\), while \(\zeta(2d+2)>1\).
Thus again the polynomials are independent.

This proves that **no \(n\ge15\) is possible**.

## 4. The remaining finite calculation: \(8\le n\le14\)

For each \(n\) and \(1\le a\le n/2\), form the coefficient matrix of
\[
(1-x)^nq_n,\qquad (1-x)^nq_aq_{n-a},
\]
and, if \(n=3a\), also \((1-x)^nq_a^3\), after substituting
\[
s=\frac{1+x}{1-x}.
\]

There are only 37 matrices. The code below verifies, over \(\mathbb Q\), that:

* no nonzero signed sum of at most two reciprocal pairs \(x^i+x^{n-i}\) belongs to any of these column spaces;
* every matrix has independent columns except the one for \((n,a)=(9,3)\).

The exceptional dependence is
\[
q_9+3q_3q_6+\frac32q_3^3=0.                                \tag{15}
\]

By Sections 1–2, every manifold in the question must pass these tests. Therefore the only remaining dimension is
\[
2n=18.                                                     \tag{16}
\]

This argument used neither connectedness nor effectiveness.

## 5. Constructing an 18-dimensional example

We now prove that the exceptional dimension actually occurs.

Use the standard homogeneous almost complex sphere
\[
S^6=G_2/SU(3).
\]
For the circle in the maximal torus specified by the triple
\[
(a,b,-a-b),
\]
the sphere has exactly two fixed points, with tangent weights
\[
(a,b,-a-b),\qquad (-a,-b,a+b),
\]
provided all three entries are nonzero.

Choose
\[
\alpha=(1,9,-10),\qquad \beta=(5,6,-11).
\]
They satisfy
\[
e_1(\alpha)=e_1(\beta)=0,\qquad
e_2(\alpha)=e_2(\beta)=-91,
\]
but
\[
e_3(\alpha)=-90,\qquad e_3(\beta)=-330.                     \tag{17}
\]

### An equivariant clutching map

Let \(\phi_\alpha,\phi_\beta:S^1\to G_2\) be these homomorphisms. The two induced \(G_2\)-bundles over \(\mathbb CP^5\) become isomorphic after replacing both homomorphisms by
\[
z\longmapsto\phi_\alpha(z^N),\qquad
z\longmapsto\phi_\beta(z^N)
\]
for some positive integer \(N\).

Here are the obstruction-theoretic details. The only nonfinite homotopy group of \(BG_2\) in degrees at most eleven is
\[
\pi_4(BG_2)\cong\mathbb Z;
\]
rationally its next generator is in degree twelve. The degree-four characteristic class of the induced bundles is proportional to
\[
(a^2+ab+b^2)x^2.
\]
Both pairs in (17) give \(91x^2\), so this obstruction agrees integrally. All remaining obstructions to a homotopy of their classifying maps on \(\mathbb CP^5\) have finite coefficient groups.

The power map
\[
[z_0:\cdots:z_5]\longmapsto[z_0^N:\cdots:z_5^N]
\]
acts on \(H^{2j}(\mathbb CP^5;A)\) as multiplication by \(N^j\). Successively choosing multiples of the exponents of the finitely many obstruction groups kills all the obstructions. Iterating power maps is again a power map. This proves the asserted isomorphism.

Equivalently, there is a smooth equivariant clutching map
\[
S^{11}\longrightarrow G_2
\]
for the free scalar circle action on \(S^{11}\subset\mathbb C^6\), with the two fiber actions \(\phi_{N\alpha}\) and \(\phi_{N\beta}\).

Clutch across the equator of
\[
S^{12}=S(\mathbb C^6\oplus\mathbb R).
\]
We obtain an equivariant principal \(G_2\)-bundle \(P\to S^{12}\), and set
\[
M=P\times_{G_2}S^6.
\]
This is a closed, connected, smooth 18-manifold.

The base circle action has two fixed points, and over each the fiber action has two fixed points. Thus \(M\) has exactly four fixed points.

### The invariant stable complex structure

The vertical tangent bundle has its \(G_2\)-invariant complex structure. Also
\[
TS^{12}\oplus\mathbb R^2
\]
has an invariant complex structure coming from
\(\mathbb C^6\oplus\mathbb C\). An invariant horizontal distribution therefore supplies the required complex structure on
\[
TM\oplus\mathbb R^2.
\]
The stabilizing fibers have trivial circle action, as required in the question.

Nonequivariantly, the stabilized base bundle is complex trivial. Furthermore \(H^2(M)=H^4(M)=0\). If \(V\) denotes the vertical complex rank-three bundle, then
\[
c(M)=c(V)=1+c_3(V).
\]
Thus the only possibly nonzero Chern number is \(c_3^3\).

The four fixed-point weight lists and signs are
\[
\begin{array}{c|c}
\text{weights}&\epsilon\\ \hline
1,1,1,1,1,1,\ N\alpha&+1\\
1,1,1,1,1,1,-N\alpha&+1\\
1,1,1,1,1,1,\ N\beta&-1\\
1,1,1,1,1,1,-N\beta&-1.
\end{array}                                               \tag{18}
\]
The signs are opposite at the two base poles.

Put
\[
K=20-546N^2,\qquad D_\alpha=-90N^3,\qquad D_\beta=-330N^3.
\]
At the two points over either pole, the third equivariant Chern class is \(K\pm D\), and the Euler denominator is \(\pm D\). Localization gives
\[
\begin{aligned}
\langle c_3^3,[M]\rangle
&=\left(\frac{(K+D_\alpha)^3-(K-D_\alpha)^3}{D_\alpha}\right)\\
&\quad-\left(\frac{(K+D_\beta)^3-(K-D_\beta)^3}{D_\beta}\right)\\
&=2(D_\alpha^2-D_\beta^2)\\
&=\boxed{-201600N^6}\ne0.                                  \tag{19}
\end{aligned}
\]
Hence \(18\in\mathcal E\).

## 6. Executable exact verification

This is the complete verification script. It checks the 37 finite cases, computes the dimension-independent ideal certificates, and checks every Chern-number localization calculation for (18), symbolically for all \(N\).

```python
import sympy as S
from itertools import combinations
from functools import lru_cache
from math import prod

# I. Exact finite check: complex dimensions 8,...,14.
s, x = S.symbols('s x')
q = {}
Ac = [S.S.One, s/2] + [
    S.bernoulli(j)/S.factorial(j) if j % 2 == 0 else S.S.Zero
    for j in range(2, 15)
]
# If A(z)=1+sum A_j z^j and log A(z)=sum q_j z^j,
# j A_j = sum_{i=1}^j i q_i A_{j-i}.
for j in range(1, 15):
    q[j] = S.expand(
        Ac[j] - sum(S.Rational(i, j)*q[i]*Ac[j-i]
                    for i in range(1, j))
    )

kernels = []
spaces = 0
for d in range(8, 15):
    pairs = [S.Poly(x**i + x**(d-i), x)
             for i in range(d//2 + 1)]
    candidates = set()

    for p in pairs:
        for sign in (-1, 1):
            candidates.add(tuple(sign*p.nth(i)
                                 for i in range(d+1)))
    for p in pairs:
        for r in pairs:
            for e in (-1, 1):
                for f in (-1, 1):
                    pp = e*p + f*r
                    candidates.add(tuple(pp.nth(i)
                                         for i in range(d+1)))
    candidates.discard((0,)*(d+1))

    for a in range(1, d//2 + 1):
        fs = [q[d], q[a]*q[d-a]]
        if d == 3*a:
            fs.append(q[a]**3)

        columns = []
        for f in fs:
            poly = S.Poly(f, s)
            H = sum(
                co*(1+x)**mon[0]*(1-x)**(d-mon[0])
                for mon, co in poly.terms()
            )
            columns.append(S.Poly(H, x))

        C = S.Matrix([
            [p.nth(i) for p in columns] for i in range(d+1)
        ])
        left = C.T.nullspace()
        for v in candidates:
            vv = S.Matrix(v)
            # A left-nullspace vector separates v from col(C).
            assert any((w.T*vv)[0] != 0 for w in left), (d, a, v)

        if C.rank() < len(fs):
            kernels.append((d, a))
        spaces += 1

assert kernels == [(9, 3)], kernels
assert S.expand(
    q[9] + 3*q[3]*q[6] + S.Rational(3, 2)*q[3]**3
) == 0
print("Finite genus check:", spaces,
      "spaces; only kernel:", kernels)

# II. Polynomial certificates valid for ALL complex dimensions >=15.
n, h, t = S.symbols('n h t')
U = 2*S.sinh(t/2)/t
logU = S.series(S.log(U), t, 0, 14).removeO()
Un = S.series(S.exp(n*logU), t, 0, 14).removeO()
Rs = {
    1: t*S.coth(t/2)/2 - 1,
    2: t**2/(4*S.sinh(t/2)**2) + t**2/12 - 1,
    3: t**3*S.cosh(t/2)/(8*S.sinh(t/2)**3) - 1
}

def minors_of_moments(expr):
    P = S.Poly(expr, t)
    M = [S.factor(P.nth(2*k)*S.factorial(2*k))
         for k in range(7)]
    return [
        S.fraction(S.factor(S.det(S.Matrix([
            [M[i+j] for j in js] for i in range(3)
        ]))))[0]
        for js in combinations(range(5), 3)
    ]

for a in (1, 2, 3):
    R = S.series(Rs[a], t, 0, 14).removeO()
    gb = S.groebner(
        minors_of_moments(Un*(1+h*R)), h, n, domain=S.QQ
    )
    assert gb.reduce(n**2*(n-a)**2)[1] == 0
    print("Moment certificate a =", a,
          ": n^2(n-a)^2 belongs to minor ideal")

R = S.series(Rs[1], t, 0, 14).removeO()
gb = S.groebner(minors_of_moments(Un*R), n, domain=S.QQ)
assert gb.reduce(S.S.One)[1] == 0
print("Zero-Euler a=1 certificate: minor ideal is the unit ideal")

# III. Symbolic localization for the 18-dimensional construction.
N, u = S.symbols('N u', positive=True)
alpha = (1, 9, -10)
beta = (5, 6, -11)
assert sum(alpha) == sum(beta) == 0
assert sum(alpha[i]*alpha[j]
           for i, j in combinations(range(3), 2)) == -91
assert sum(beta[i]*beta[j]
           for i, j in combinations(range(3), 2)) == -91
assert prod(alpha) == -90 and prod(beta) == -330

points = []
for triple, eps in ((alpha, 1), (beta, -1)):
    for sign in (1, -1):
        ws = [S.S.One]*6 + [sign*N*v for v in triple]
        cp = S.Poly(prod(1+w*u for w in ws), u)
        points.append(
            (eps, [cp.nth(j) for j in range(10)], S.prod(ws))
        )

@lru_cache(None)
def parts(d, m=None):
    if d == 0:
        return ((),)
    if m is None:
        m = d
    return tuple(
        (i,) + p
        for i in range(min(d, m), 0, -1)
        for p in parts(d-i, i)
    )

def residue(part):
    return S.cancel(sum(
        eps*S.prod(cs[j] for j in part)/e
        for eps, cs, e in points
    ))

low = 0
for degree in range(9):
    for part in parts(degree):
        assert residue(part) == 0
        low += 1

values = {p: residue(p) for p in parts(9)}
nonzero = {p: v for p, v in values.items() if v != 0}
assert nonzero == {(3, 3, 3): -201600*N**6}
print("Localization:", low, "lower-degree identities;",
      len(values), "Chern numbers")
print("Nonzero Chern number:", nonzero)

# The two-point G2-sphere chi_y identity, independently checked.
A, B, y = S.symbols('A B y')
fiber = [A, B, 1/(A*B)]

def chi_term(ws):
    return S.prod((1+y/w)/(1-1/w) for w in ws)

assert S.factor(
    chi_term(fiber) + chi_term([1/w for w in fiber]) - y*y + y
) == 0
print("G2-sphere chi_y identity checked.")
```

I ran this script. Its output was:

```text
Finite genus check: 37 spaces; only kernel: [(9, 3)]
Moment certificate a = 1 : n^2(n-a)^2 belongs to minor ideal
Moment certificate a = 2 : n^2(n-a)^2 belongs to minor ideal
Moment certificate a = 3 : n^2(n-a)^2 belongs to minor ideal
Zero-Euler a=1 certificate: minor ideal is the unit ideal
Localization: 67 lower-degree identities; 30 Chern numbers
Nonzero Chern number: {(3, 3, 3): -201600*N**6}
G2-sphere chi_y identity checked.
```

Thus necessity holds in every even dimension at least sixteen, and the exceptional dimension eighteen is realized by a closed manifold with the required invariant stable complex structure, exactly four isolated fixed points, and nonzero \(c_3^3\). **Nothing remains to be proved.**

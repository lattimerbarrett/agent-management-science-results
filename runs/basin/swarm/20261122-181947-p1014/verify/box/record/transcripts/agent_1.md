# agent_1: the whole run

[user message]
For a finite group \(G\), let \(|G|\) denote its order and let \(k(G)\) denote its number of conjugacy classes. Define
\[
\mathcal E=\left\{p>451:\ p\text{ is prime and there exists a finite solvable group }G\text{ such that }p^2\mid |G|\text{ and }k(G)<\frac{49p+451}{60}\right\}.
\]
Determine \(\mathcal E\) exactly as an explicit set of primes.

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
[tool call: run_scratchpad]
content:
```
import sympy as s
from fractions import Fraction as F
ps=list(s.primerange(452,2732))
for d in [8,9,10,11,12]:
 print(d,[(p,(p-1)//d) for p in ps if (p-1)%(2*d)==0 and p%8==7 and ((p-1)//d)%3 and 4*F(p-1,d)+F(d*(p+1),24)<F(49*p+451,60)])

```
timeout_seconds: 60

[tool result]
```
[exit code 0, 0.2s]
(ran it after writing 5 lines)
--- stdout ---
8 []
9 [(631, 70), (991, 110), (1063, 118), (1279, 142), (1423, 158), (2143, 238), (2287, 254), (2503, 278), (2719, 302)]
10 []
11 []
12 []

--- stderr ---
(empty)
```

## response 3
[tool call: run_scratchpad]
content:
```
import sympy as s
p=s.symbols('p')
for d in [7,8,9,10,11,12]:
 B=4*(p-1)/d+s.Rational(d,24)*(p+1)
 print(d,s.factor((49*p+451)/60-B),s.solve_univariate_inequality(B<(49*p+451)/60,p))

```
timeout_seconds: 60

[tool result]
```
[exit code 0, 0.3s]
(ran it after writing 5 lines)
--- stdout ---
7 -(13*p - 2183)/280 (-oo < p) & (p < 2183/13)
8 -(p - 461)/60 (-oo < p) & (p < 461)
9 -(p - 2731)/360 (-oo < p) & (p < 2731)
10 15/2 (-oo < p) & (p < oo)
11 -(7*p - 9797)/1320 (-oo < p) & (p < 9797/7)
12 -(p - 441)/60 (-oo < p) & (p < 441)

--- stderr ---
(empty)
```

## response 4
[tool call: run_scratchpad]
content:
```
from fractions import Fraction as Q
from sympy import primerange, primitive_root
from math import isqrt, log

# The finite arithmetic search after the proved reduction.
def T(p): return Q(49*p+451,60)
def B(p,d): return 4*Q(p-1,d)+Q(d*(p+1),24)
found=[]
for d,upper in [(9,2731),(11,1400)]:
    rows=[]
    for p in primerange(452,upper):
        if (p-1)%(2*d): continue
        m=(p-1)//d
        if p%8==7 and m%3 and B(p,d)<T(p):
            rows.append(p); found.append(p)
    print('index',d,rows)
assert not [p for p in primerange(452,461) if (p-1)%16==0]
E=sorted(found)

# All computations below take place in GL(2,p), not in the huge affine group.
I=(1,0,0,1)
def mul(x,y,p):
    a,b,c,d=x; e,f,g,h=y
    return ((a*e+b*g)%p,(a*f+b*h)%p,(c*e+d*g)%p,(c*f+d*h)%p)
def scale(a,x,p): return tuple(a*z%p for z in x)
def add(*xs,p): return tuple(sum(v)%p for v in zip(*xs))
def inv(x,p):
    a,b,c,d=x; z=pow((a*d-b*c)%p,-1,p)
    return scale(z,(d,-b,-c,a),p)
def closure(gens,p):
    S={I}; todo=[I]
    for x in todo:
        for g in gens:
            y=mul(x,g,p)
            if y not in S: S.add(y); todo.append(y)
    return S

def conjugacy_count(H,gens,p):
    pairs=[(g,inv(g,p)) for g in gens]
    remaining=set(H); ans=0
    while remaining:
        x=next(iter(remaining)); orbit={x}; todo=[x]
        for y in todo:
            for g,gi in pairs:
                z=mul(mul(g,y,p),gi,p)
                if z not in orbit: orbit.add(z); todo.append(z)
        assert orbit<=remaining
        remaining.difference_update(orbit); ans+=1
    return ans

for p in E:
    m=(p-1)//9
    a=b=None
    for aa in range(p):
        for bb in range(p):
            if (aa*aa+bb*bb+1)%p==0:
                a,b=aa,bb; break
        if a is not None: break
    r=next(x for x in range(p) if x*x%p==2)
    i=(0,1,p-1,0); j=(a,b,b,-a%p); k=mul(i,j,p)
    t=scale(pow(2,-1,p),add(scale(-1,I,p),i,j,k,p=p),p)
    s=scale(pow(r,-1,p),add(i,j,p=p),p)
    O=closure([i,j,t,s],p)
    assert len(O)==48
    z=pow(int(primitive_root(p)),(p-1)//m,p)
    H={scale(pow(z,a,p),h,p) for a in range(m) for h in O}
    assert len(H)==24*m
    gens=[i,j,t,s,scale(z,I,p)]
    assert closure(gens,p)==H
    # Certify solvability via O/Q8 = S3 and H/O abelian.
    Q8=closure([i,j],p)
    assert len(Q8)==8 and Q8<=O
    assert all(mul(mul(g,x,p),inv(g,p),p) in Q8 for g in [t,s] for x in Q8)
    # O/Q8 has order 6, hence is solvable; scalar extension is solvable.
    for h in H-{I}:
        a,b,c,d=h
        assert ((a-1)*(d-1)-b*c)%p != 0
    kh=conjugacy_count(H,gens,p)
    assert kh==4*m
    assert (p*p-1)%len(H)==0
    kg=kh+(p*p-1)//len(H)
    assert kg<T(p)
    print(p,'m=',m,'|H|=',len(H),'k(H)=',kh,'k(G)=',kg,'bound=',T(p))
print('E =',E)

```
timeout_seconds: 600

[tool result]
```
[exit code 0, 0.3s]
(ran it after writing 84 lines)
--- stdout ---
index 9 [631, 991, 1063, 1279, 1423, 2143, 2287, 2503, 2719]
index 11 []
631 m= 70 |H|= 1680 k(H)= 280 k(G)= 517 bound= 3137/6
991 m= 110 |H|= 2640 k(H)= 440 k(G)= 812 bound= 4901/6
1063 m= 118 |H|= 2832 k(H)= 472 k(G)= 871 bound= 26269/30
1279 m= 142 |H|= 3408 k(H)= 568 k(G)= 1048 bound= 31561/30
1423 m= 158 |H|= 3792 k(H)= 632 k(G)= 1166 bound= 35089/30
2143 m= 238 |H|= 5712 k(H)= 952 k(G)= 1756 bound= 52729/30
2287 m= 254 |H|= 6096 k(H)= 1016 k(G)= 1874 bound= 56257/30
2503 m= 278 |H|= 6672 k(H)= 1112 k(G)= 2051 bound= 61549/30
2719 m= 302 |H|= 7248 k(H)= 1208 k(G)= 2228 bound= 66841/30
E = [631, 991, 1063, 1279, 1423, 2143, 2287, 2503, 2719]

--- stderr ---
(empty)
```

## response 5
[tool call: edit_scratchpad]
old_string:
```
# The finite arithmetic search after the proved reduction.

```
new_string:
```
# Base inequalities used in the uniform, all-dimensions estimates.
assert 216 < 4*451
assert 4**7 < 4*451**2
assert 24*4 < 4*451**2
assert 9 < 4*451
assert 16**2 < 4*451
assert 24**2*16 < 4*451**2
assert 384 < 451**2 and 64 < 451**2
# The finite arithmetic search after the proved reduction.

```

[tool result]
```
Edited scratchpad.py (1 replacement).
```

## response 6
[reasoning summary]
**Clarifying computational results**

I'm focusing on computational and analytical aspects here. It's important to state that these are classical structure results, not the recent assertion I'm pondering. This helps to avoid circular reasoning and keeps things clear. I think it's not strictly necessary to include this detail, but it would definitely strengthen my explanation! So, I'm making sure I communicate effectively while being mindful of the context I'm discussing.

[tool call: run_scratchpad]
content:
```
from sage.all import libgap
for n in range(2,301):
 if not libgap.NumberSmallGroups(n).sage()<1000: continue
 for j in range(1,int(libgap.NumberSmallGroups(n))+1):
  g=libgap.SmallGroup(n,j)
  if not bool(g.IsSolvableGroup()):continue
  f=g.FrattiniSubgroup(); nf=int(f.Size())
  if nf==1:continue
  fac=libgap.FactorsInt(n).sage()
  for p in set(fac):
   nq=n//nf
   if nq%p==0 and nq%(p*p)!=0:
    P=g.SylowSubgroup(p)
    if not bool(P.IsCyclic()):print('COUNTEREXAMPLE',n,j,p,nf,flush=True);raise SystemExit
print('no counterexample')
```
timeout_seconds: 600

[tool result]
```
[exit code 0, 2.8s]
(ran it after writing 15 lines)
--- stdout ---
no counterexample

--- stderr ---
(empty)
```

## response 7
[reasoning summary]
**Revisiting script issues**

Oh no, I accidentally overwrote the script! Now I’ve lost the current group script, but I think I can recreate it. I need to ensure that the final code actually runs properly again. I'm considering whether I can apply the general intersection property in Φ to find a solution. I’ll also compare it with the program allp to see what comes up. Let’s figure this out!

[tool call: edit_scratchpad]
old_string:
```
   if nq%p==0 and nq%(p*p)!=0:
    P=g.SylowSubgroup(p)
    if not bool(P.IsCyclic()):print('COUNTEREXAMPLE',n,j,p,nf,flush=True);raise SystemExit
```
new_string:
```
   P=g.SylowSubgroup(p)
   ip=libgap.Intersection(P,f)
   if not bool(libgap.IsSubgroup(P.FrattiniSubgroup(),ip)):
    print('COUNTEREXAMPLE general',n,j,p,nf,flush=True);raise SystemExit
```

[tool result]
```
Edited scratchpad.py (1 replacement).
```

## response 8
[tool call: run_scratchpad]
timeout_seconds: 600

[tool result]
```
[exit code 0, 3.3s]
--- stdout ---
no counterexample

--- stderr ---
(empty)
```

## response 9
[tool call: write_scratchpad]
content:
```
from fractions import Fraction as Q
from sympy import primerange, primitive_root

assert 216 < 4*451 and 4**7 < 4*451**2
assert 24*4 < 4*451**2 and 9 < 4*451
assert 16**2 < 4*451 and 24**2*16 < 4*451**2
assert 384 < 451**2 and 64 < 451**2

def T(p): return Q(49*p+451,60)
def B(p,d): return 4*Q(p-1,d)+Q(d*(p+1),24)
E=[]
for d,upper in [(9,2731),(11,1400)]:
    row=[]
    for p in primerange(452,upper):
        if (p-1)%(2*d): continue
        m=(p-1)//d
        if p%8==7 and m%3 and B(p,d)<T(p):
            row.append(p); E.append(p)
    print('index',d,':',row)
assert not [p for p in primerange(452,461) if (p-1)%16==0]
E.sort()

I=(1,0,0,1)
def mul(x,y,p):
    a,b,c,d=x; e,f,g,h=y
    return ((a*e+b*g)%p,(a*f+b*h)%p,
            (c*e+d*g)%p,(c*f+d*h)%p)
def scale(a,x,p): return tuple(a*z%p for z in x)
def add(*xs,p): return tuple(sum(v)%p for v in zip(*xs))
def inv(x,p):
    a,b,c,d=x
    return scale(pow((a*d-b*c)%p,-1,p),(d,-b,-c,a),p)
def closure(gens,p):
    S={I}; todo=[I]
    for x in todo:
        for g in gens:
            y=mul(x,g,p)
            if y not in S: S.add(y); todo.append(y)
    return S

def conjugacy_count(H,gens,p):
    pairs=[(g,inv(g,p)) for g in gens]
    remaining=set(H); ans=0
    while remaining:
        x=next(iter(remaining)); orbit={x}; todo=[x]
        for y in todo:
            for g,gi in pairs:
                z=mul(mul(g,y,p),gi,p)
                if z not in orbit: orbit.add(z); todo.append(z)
        assert orbit<=remaining
        remaining.difference_update(orbit); ans+=1
    return ans

for p in E:
    m=(p-1)//9
    a=b=None
    for aa in range(p):
        for bb in range(p):
            if (aa*aa+bb*bb+1)%p==0:
                a,b=aa,bb; break
        if a is not None: break
    r=next(x for x in range(p) if x*x%p==2)
    i=(0,1,p-1,0); j=(a,b,b,-a%p); k=mul(i,j,p)
    t=scale(pow(2,-1,p),add(scale(-1,I,p),i,j,k,p=p),p)
    s=scale(pow(r,-1,p),add(i,j,p=p),p)
    O=closure([i,j,t,s],p)
    assert len(O)==48
    z=pow(int(primitive_root(p)),(p-1)//m,p)
    H={scale(pow(z,a,p),h,p) for a in range(m) for h in O}
    assert len(H)==24*m
    gens=[i,j,t,s,scale(z,I,p)]
    assert closure(gens,p)==H
    Q8=closure([i,j],p)
    assert len(Q8)==8 and Q8<=O
    assert all(mul(mul(g,x,p),inv(g,p),p) in Q8
               for g in [t,s] for x in Q8)
    # O/Q8 has order 6; H is a central scalar extension of O.
    # Hence both O and H are solvable.
    for h in H-{I}:
        a,b,c,d=h
        assert ((a-1)*(d-1)-b*c)%p != 0
    kh=conjugacy_count(H,gens,p)
    assert kh==4*m
    assert (p*p-1)%len(H)==0
    kg=kh+(p*p-1)//len(H)
    assert kg<T(p)
    print(p, '|H| =',len(H),'k(H) =',kh,'k(G) =',kg)
print('E =',E)

```

[tool result]
```
Wrote scratchpad.py (88 lines).
```

## response 10
[tool call: run_scratchpad]
timeout_seconds: 600

[tool result]
```
[exit code 0, 0.3s]
--- stdout ---
index 9 : [631, 991, 1063, 1279, 1423, 2143, 2287, 2503, 2719]
index 11 : []
631 |H| = 1680 k(H) = 280 k(G) = 517
991 |H| = 2640 k(H) = 440 k(G) = 812
1063 |H| = 2832 k(H) = 472 k(G) = 871
1279 |H| = 3408 k(H) = 568 k(G) = 1048
1423 |H| = 3792 k(H) = 632 k(G) = 1166
2143 |H| = 5712 k(H) = 952 k(G) = 1756
2287 |H| = 6096 k(H) = 1016 k(G) = 1874
2503 |H| = 6672 k(H) = 1112 k(G) = 2051
2719 |H| = 7248 k(H) = 1208 k(G) = 2228
E = [631, 991, 1063, 1279, 1423, 2143, 2287, 2503, 2719]

--- stderr ---
(empty)
```

## response 11
[tool call: run_scratchpad]
content:
```
from sage.all import libgap
for n in [320,384,432,448,486,512,576,640,648,672,720,768,864,896,960,972,1152,1296,1344,1536,1728,1944]:
 ng=int(libgap.NumberSmallGroups(n))
 if ng>25000:continue
 for j in range(1,ng+1):
  g=libgap.SmallGroup(n,j)
  if not bool(g.IsSolvableGroup()):continue
  f=g.FrattiniSubgroup();nf=int(f.Size())
  if nf==1:continue
  for p in set(libgap.FactorsInt(n).sage()):
   P=g.SylowSubgroup(p);ip=libgap.Intersection(P,f)
   if not bool(libgap.IsSubgroup(P.FrattiniSubgroup(),ip)):
    print('COUNTEREXAMPLE',n,j,p,nf,'quotientp',int(g.FactorGroup(f).SylowSubgroup(p).Size()),flush=True);raise SystemExit
 print(n,'checked',ng,flush=True)
print('none')
```
timeout_seconds: 600

[tool result]
```
[exit code 0, 116.6s]
(ran it after writing 15 lines)
--- stdout ---
320 checked 1640
384 checked 20169
432 checked 775
448 checked 1396
486 checked 261
576 checked 8681
640 checked 21541
648 checked 757
672 checked 1280
720 checked 840
864 checked 4725
896 checked 19349
960 checked 11394
972 checked 900
1296 checked 3609
1344 checked 11720
COUNTEREXAMPLE 1944 2295 3 9 quotientp 27

--- stderr ---
(empty)
```

## response 12
[tool call: run_scratchpad]
content:
```
from sage.all import libgap
g=libgap.SmallGroup(1944,2295);f=g.FrattiniSubgroup();P=g.SylowSubgroup(3);Q=g.FactorGroup(f).SylowSubgroup(3)
print(P.StructureDescription(),Q.StructureDescription(),P.IsCyclic(),Q.IsCyclic())
print(g.StructureDescription(),g.FactorGroup(f).StructureDescription())

```
timeout_seconds: 60

[tool result]
```
[exit code 0, 1.5s]
(ran it after writing 4 lines)
--- stdout ---
C3 x ((C3 x C3 x C3) : C3) (C3 x C3) : C3 false false
((C3 x C3 x C3 x C3) : Q8) : C3 ((C3 x C3) : Q8) : C3

--- stderr ---
(empty)
```

## response 13
[message]
\[
\boxed{\mathcal E=\{631,\ 991,\ 1063,\ 1279,\ 1423,\ 2143,\ 2287,\ 2503,\ 2719\}.}
\]

The strict inequality in the question matters. In particular, a family associated with the integer \(10\) must be excluded without replacing \(<\) by \(\leq\).

I give the group-theoretic reduction, the remaining arithmetic, and executable verification code. The code constructs witnesses as matrix groups; it does not merely print the proposed answer.

## 1. Classical structural facts used

I use the following classical finite-group results.

1. **Frattini facts for solvable groups.**
   * If \(X\) is solvable and \(X/\Phi(X)\) has cyclic Sylow \(p\)-subgroups, then \(X\) has cyclic Sylow \(p\)-subgroups.
   * If \(X\) is solvable and \(\Phi(X)=1\), then \(F(X)\) is the direct product of the minimal normal subgroups of \(X\), and \(F(X)\) has a complement.

   These are standard consequences of the Gaschütz theory of Frattini extensions and complements. The first statement here is specifically about **cyclic Sylow subgroups**; no general assertion that \(\Phi(X)\cap P\leq\Phi(P)\) is being used.

2. **The primitive solvable linear-group structure theorem.**  
   Suppose that \(K\leq\mathrm{GL}_d(p)\) is solvable, irreducible and linearly primitive. There are a cyclic normal subgroup \(U\), positive integers \(e,f\) with \(ef\leq d\), and
   \[
   e=\prod_r r^{a_r},
   \qquad
   C(e)=e^2\prod_r|\mathrm{Sp}_{2a_r}(r)|,
   \tag{1}
   \]
   such that
   \[
   |U|\mid p^f-1,\qquad
   |K:U|\leq fC(e),\qquad
   |K:C_K(U)|\leq f.
   \tag{2}
   \]
   Empty products have value \(1\).

   This is the usual Fitting/symplectic structure theorem for solvable primitive linear groups: the noncyclic part of the Fitting subgroup is a central product of extraspecial groups, its quotient by the cyclic part has order \(e^2\), and its outer action embeds in the indicated symplectic groups. The field action has order at most \(f\). Only the consequences (1)–(2) are needed below.

3. A finite subgroup of \(\mathrm{PGL}_2\) of order prime to the characteristic is cyclic, dihedral, \(A_4,S_4\), or \(A_5\). In the solvable case \(A_5\) is absent.

These are classical structural results, not the recent bound asked about in the question.

Write
\[
T(p)=\frac{49p+451}{60}.
\]
For \(p>451\), we have \(T(p)<p\).

## 2. Reduction to an irreducible affine group

Fix \(p>451\), and suppose a solvable group satisfying the question exists. Choose one, \(G\), of minimum order.

First, its Sylow \(p\)-subgroups cannot be cyclic. Indeed, if \(P\) is cyclic and \(p^2\mid |P|\), fusion in \(P\) is controlled by \(N_G(P)\). The induced automorphism group is a \(p'\)-subgroup of \(\operatorname{Aut}(P)\), so has order at most \(p-1\). The \(p(p-1)\) elements of order \(p^2\) therefore give at least \(p\) conjugacy classes. Together with the identity,
\[
k(G)\geq p+1>T(p).
\tag{3}
\]

If \(\Phi(G)\ne1\) and \(p^2\mid |G/\Phi(G)|\), minimality, together with \(k(G)\geq k(G/\Phi(G))\), is a contradiction. Otherwise \(G/\Phi(G)\) has cyclic Sylow \(p\)-subgroups, so the first Frattini fact and (3) again give a contradiction. Thus
\[
\Phi(G)=1.
\]

Every minimal normal subgroup of \(G\) is a \(p\)-group: quotienting by a minimal normal \(q\)-subgroup with \(q\ne p\) would contradict minimality.

Consequently,
\[
G=V\rtimes H,\qquad V=F(G),
\]
where \(V\) is elementary abelian of \(p\)-power order and \(H\) acts faithfully and completely reducibly.

If \(G\) has two distinct minimal normal subgroups \(N_1,N_2\), write \(|G|_p=p^b\). Minimality gives
\[
|N_i|\geq p^{b-1}.
\]
Since \(N_1\cap N_2=1\), we obtain \(2(b-1)\leq b\), hence \(b=2\). Thus \(V\cong C_p^2\), its two constituents have dimension one, and \(H\) is abelian. In that case
\[
k(G)\geq |H|+\frac{p^2-1}{|H|}
\geq 2\sqrt{p^2-1}>p,
\]
another contradiction.

We have proved that
\[
G=V\rtimes H,\qquad V\cong\mathbb F_p^n,\quad n\geq2,
\tag{4}
\]
with \(H\) solvable and irreducible.

We will repeatedly use the elementary affine lower bound
\[
k(V\rtimes H)\geq k(H)+\frac{|V|-1}{|H|}.
\tag{5}
\]
For example, this follows from the little-groups formula on the characters of the abelian normal subgroup \(V\): each nonzero orbit contributes at least one class.

## 3. Only dimension two, with projective image \(S_4\), can occur

Here are the estimates that make this reduction uniform in the dimension.

### 3.1 Primitive linear groups

For \(C(e)\) in (1),
\[
C(1)=1,\qquad C(2)=24,\qquad C(3)=216,
\]
and
\[
C(e)\leq e^{\,2\log_2e+3}.
\tag{6}
\]
Indeed,
\[
|\mathrm{Sp}_{2a}(r)|<r^{2a^2+a},
\]
and \(a\leq\log_2e\).

For \(e\geq4\),
\[
e^{\,2\log_2e+3}<4\cdot451^{e-2}.
\tag{7}
\]
One way to check this for all real \(e\geq4\) is to take logarithms. The difference is positive at \(e=4\), and its derivative is
\[
\log451-\frac{4\log e/\log2+3}{e}>0.
\]
The fraction on the right is decreasing for \(e\geq4\).

Together with the displayed values of \(C(1),C(2),C(3)\), (7), and induction on \(f\), this gives
\[
f^2C(e)\leq4p^{d-2}\quad(d\geq3),
\tag{8}
\]
whenever \(ef\leq d\) and \(p>451\). For completeness, the small starting cases in this induction are
\[
216<4\cdot451,\qquad
4^7<4\cdot451^2,\qquad
4\cdot24<4\cdot451^2,\qquad
9<4\cdot451.
\]
For dimension two the corresponding bound is \(f^2C(e)\leq24\), and for dimension one it is \(1\).

If \(H\) is linearly primitive, (2) gives \(k(H)\geq |U|/f\). Consequently (5) and AM–GM give
\[
k(V\rtimes H)
\geq 2\sqrt{\frac{p^n-1}{f^2C(e)}}.
\tag{9}
\]
For \(n\geq3\), (8) makes the right-hand side larger than \(p-1\). Since the left-hand side is integral,
\[
k(V\rtimes H)\geq p.
\tag{10}
\]

### 3.2 Imprimitive linear groups

We also need to exclude linearly imprimitive \(H\).

A solvable permutation group of degree \(t\) has order at most \(4^{t-1}\). This follows by induction on block systems: a primitive solvable group has affine degree \(r^a\) and order at most
\[
r^{a^2+a}\leq4^{r^a-1}.
\]
The last inequality follows from \(a(a+1)\leq2(2^a-1)\), and monotonicity in \(r\geq2\).

Choose a system of \(t\geq2\) blocks of minimum block dimension \(d\), so \(n=dt\). The induced group \(K\) on a block is irreducible and primitive, and
\[
H\leq K\wr T
\]
for a solvable permutation group \(T\) of degree \(t\).

Apply (1)–(2) to \(K\), and put \(D=H\cap U^t\). Then
\[
|H:D|\leq(fC(e))^t|T|,
\qquad
|H:C_H(D)|\leq f^t|T|.
\]
Thus
\[
k(V\rtimes H)\geq
2\sqrt{\frac{p^{dt}-1}{(f^2C(e))^t|T|^2}}.
\tag{11}
\]

In every case the denominator in (11) is at most \(4p^{dt-2}\):

* If \(d=1,t=2\), use \(|T|\leq2\).
* If \(d=1,t\geq3\), use
  \[
  16^{t-1}\leq4p^{t-2}.
  \]
* If \(d=2\), use
  \[
  24^t16^{t-1}<4p^{2t-2}.
  \]
* If \(d\geq3\), use (8) and
  \[
  4^{t-1}16^{t-1}=64^{t-1}<p^{2t-2}.
  \]

The first terms of the two geometric inequalities are respectively
\(256<4\cdot451\) and \(24^2\cdot16<4\cdot451^2\); their subsequent ratios also satisfy the required inequalities.

Again (11) is larger than \(p-1\), so (10) holds.

Therefore our counterexample must have \(n=2\), and \(H\) is linearly primitive.

### 3.3 Projective image in dimension two

The primitive structure theorem in dimension two shows that \(p\nmid |H|\): here the only possible factors outside \(U\) divide \(24\), while \(|U|\mid p^f-1\) with \(f\leq2\).

Let \(Z=H\cap\mathbb F_p^\times I\), and put \(m=|Z|\). The projective image is cyclic, dihedral, \(A_4\), or \(S_4\).

If it is cyclic or dihedral, \(H\) has an abelian subgroup of index at most two. Hence \(k(H)\geq |H|/4\), and
\[
k(G)\geq\frac{|H|}{4}+\frac{p^2-1}{|H|}
\geq\sqrt{p^2-1}>p-1.
\]
This excludes those cases.

For projective image \(A_4\) or \(S_4\), \(m\) is even. In fact, lifts of the projective four-group contain \(Q_8\), including \(-I\).

Counting classes above the projective classes gives
\[
\begin{array}{c|c|c}
H/Z&|H|&k(H)\\ \hline
A_4&12m&7m/2\\
S_4&24m&4m.
\end{array}
\tag{12}
\]
Here is the class-count calculation. The identity projective class contributes \(m\) classes. Each projective involution class contributes \(m/2\) classes: the centralizer of a lift has projective index two in the projective centralizer, since distinct commuting projective involutions have anticommuting lifts. Each projective class of order three or four contributes \(m\) classes. There is one involution class and two order-three classes in \(A_4\), and two involution classes, one order-three class and one order-four class in \(S_4\).

For \(A_4\), (5) and (12) give
\[
k(G)\geq\frac{7m}{2}+\frac{p^2-1}{12m}
\geq2\sqrt{\frac{7(p^2-1)}{24}}>p.
\]

We have therefore proved the crucial reduction:
\[
\boxed{
G=\mathbb F_p^2\rtimes H,\quad
H/Z\cong S_4,\quad
m=|Z|\text{ even},\quad
|H|=24m,\quad k(H)=4m.
}
\tag{13}
\]

## 4. The extra contribution from fixed vectors

We need more than (5) in a few cases.

For a \(p'\)-subgroup \(H\leq\mathrm{GL}_2(p)\), each nonzero-vector stabilizer \(H_v\) is cyclic. Indeed, its action on \(V/\langle v\rangle\) is faithful, since the kernel would be a unipotent \(p\)-group.

The coprime affine class formula consequently gives
\[
k(V\rtimes H)
=
k(H)+\frac{p^2-1}{|H|}
+\frac1{|H|}
\sum_{v\ne0}\bigl(|H_v|^2-1\bigr).
\tag{14}
\]
One can obtain this from the little-groups formula on the dual of \(V\). The vector and dual actions have the same numbers of fixed points for every subgroup of \(H\), by complete reducibility, and hence the same stabilizer-orbit counts.

Thus, if at least six projective lines have stabilizers of order at least two,
\[
k(G)\geq4m+\frac{p^2-1}{24m}+\frac{3(p-1)}{4m}.
\tag{15}
\]
If at least eight lines have stabilizers of order at least three, the last contribution is instead at least
\[
\frac{8(p-1)}{3m}.
\tag{16}
\]

Put
\[
d=\frac{p-1}{m},\qquad
B_d(p)=\frac{4(p-1)}d+\frac{d(p+1)}{24}.
\tag{17}
\]
By (13)–(14),
\[
k(G)\geq B_d(p).
\tag{18}
\]

## 5. Restricting the integer \(d\)

Straight calculation gives
\[
\begin{array}{c|c}
d&T(p)-B_d(p)\\ \hline
7&(2183-13p)/280\\
8&(461-p)/60\\
9&(2731-p)/360\\
10&15/2\\
11&(9797-7p)/1320\\
12&(441-p)/60.
\end{array}
\tag{19}
\]

For \(p>451\), \(B_d(p)\) decreases for \(1\leq d\leq9\) and increases for \(d\geq10\). The rows \(d=7,12\) therefore exclude all \(d\leq7\) and \(d\geq12\).

For \(d=8\), (19) requires \(451<p<461\), so \(p=457\); but then \(m=(p-1)/8=57\) is odd, contrary to (13).

Only \(d=9,10,11\) remain.

### 5.1 Excluding \(d=10\)

Since \(m=(p-1)/10\) is even, \(p\equiv1\pmod{20}\), so \(p\equiv1\) or \(5\pmod8\).

If \(p\equiv1\pmod8\), then \(4\mid m\). The subgroup \(Q_8\leq H\) has three noncentral projective involutions. Their six eigenlines are distinct; since their eigenvalues are fourth roots of unity, they lie in the scalar subgroup of order \(m\). Each of these six lines consequently has nontrivial point stabilizer. From (15),
\[
k(G)\geq B_{10}(p)+\frac{3\cdot10}{4}=T(p),
\]
which excludes the strict inequality.

If \(p\equiv5\pmod8\), such an \(H\) cannot have scalar index \(10\). To see this, choose \(h\in H\) whose projective image has order four. It has eigenvalues \(\lambda,i\lambda\) in \(\mathbb F_p\), where \(i^2=-1\). Its square has the same projective image as a suitable \(q\in Q_8\), whose eigenvalues are \(i,-i\). Therefore \(h^2q^{-1}=sI\) with
\[
s=\pm i\lambda^2.
\]
Because \(p\equiv5\pmod8\), this scalar is a nonsquare. But \(sI\in Z\), whereas \(Z\), having even index \(10\) in \(\mathbb F_p^\times\), consists entirely of squares. This is impossible.

Thus \(d=10\) gives no member of \(\mathcal E\).

### 5.2 The odd indices \(d=9,11\)

For these indices,
\[
T(p)-B_d(p)<\frac{3d}{4}\qquad(p>451).
\tag{20}
\]

If a projective involution is split, its eigenvalues, after choosing a lift, have squares in the scalar group \(Z\). Since \(d\) is odd, its eigenvalues themselves lie in \(Z\). Thus its two eigenlines have nontrivial point stabilizer.

We recall the elementary splitting facts for projective \(S_4\):

* If \(p\equiv1\pmod4\), the three double transpositions are split.
* If \(p\equiv3\pmod8\), the six transpositions are split.
* If \(p\equiv7\pmod8\), the projective \(S_4\) is contained in \(\mathrm{PSL}_2(p)\).

For clarity, these follow from the determinant character to
\(\mathbb F_p^\times/(\mathbb F_p^\times)^2\). A projective involution is split precisely when minus its determinant is a square. Double transpositions lie in the kernel. Examining an order-four element in the split or nonsplit torus shows that the determinant character on \(S_4\) is nontrivial for \(p\equiv3,5\pmod8\), and trivial for \(p\equiv1,7\pmod8\).

In either of the first two cases there are at least six distinct split involution eigenlines. Equations (15) and (20) exclude the strict inequality. Hence necessarily
\[
p\equiv7\pmod8.
\tag{21}
\]

Let \(O\cong2.S_4\) be the inverse image of this projective \(S_4\) in \(\mathrm{SL}_2(p)\), the binary octahedral group. Because \(d\) is odd,
\[
H=ZO.
\tag{22}
\]
Indeed, any possible scalar twist would give a homomorphism from \(O\), whose abelianization has order two, to a cyclic group of odd order \(d\), and is therefore trivial.

If \(3\mid m\), the order-three projective elements give eight distinct eigenlines whose point stabilizers have order at least three. Equation (16) contributes \(8d/3\), more than the allowance in (20). Therefore
\[
3\nmid m.
\tag{23}
\]

Conversely, under (21)–(23), \(H=ZO\) is fixed-point-free on the nonzero vectors. The noncentral elements of \(O\) have eigenvalues of orders \(3,4,6\), or \(8\). But \(m\) has 2-part exactly \(2\), and \(3\nmid m\), so none of these eigenvalues belongs to \(Z\). Thus
\[
k(\mathbb F_p^2\rtimes H)=B_d(p).
\tag{24}
\]

We have reduced the entire problem to the following two finite searches:
\[
\begin{array}{ll}
d=9:&451<p<2731,\quad p\equiv7\pmod8,\quad
18\mid p-1,\quad 3\nmid (p-1)/9;\\[2mm]
d=11:&451<p<9797/7,\quad p\equiv7\pmod8,\quad
22\mid p-1,\quad 3\nmid (p-1)/11.
\end{array}
\tag{25}
\]
Here \(p\) must be prime.

The first line gives exactly the nine primes in the answer. The second gives none.

## 6. Explicit witnesses and executable verification

For each of the nine primes, take
\[
m=(p-1)/9,\qquad H=\langle Z,O\rangle,\qquad
G=\mathbb F_p^2\rtimes H.
\]
Then \(H\) is solvable: \(O\) has normal subgroup \(Q_8\), with quotient of order six, and adjoining scalar matrices is a central extension. Also,
\[
|H|=24m,\qquad k(H)=4m,
\]
and \(H\) is fixed-point-free on nonzero vectors. Therefore
\[
k(G)=4m+\frac{p^2-1}{24m}.
\]

The resulting class counts are
\[
\begin{array}{r|r}
p&k(G)\\ \hline
631&517\\
991&812\\
1063&871\\
1279&1048\\
1423&1166\\
2143&1756\\
2287&1874\\
2503&2051\\
2719&2228
\end{array}
\]
and each is strictly less than \(T(p)\).

Here is the verification code. Besides doing the finite searches, it constructs \(O\) and \(H\) as actual matrix groups over each prime field, enumerates their elements, counts \(H\)'s conjugacy classes by conjugation orbits, verifies solvability through the normal subgroup of order eight, and tests fixed-point-freeness element by element. Thus the affine class count is certified without enumerating the much larger affine group.

I ran this code successfully.

```python
from fractions import Fraction as Q
from sympy import primerange, primitive_root

# Starting inequalities for the uniform dimension estimates.
assert 216 < 4*451 and 4**7 < 4*451**2
assert 24*4 < 4*451**2 and 9 < 4*451
assert 16**2 < 4*451 and 24**2*16 < 4*451**2
assert 384 < 451**2 and 64 < 451**2

def T(p):
    return Q(49*p + 451, 60)

def B(p, d):
    return 4*Q(p-1, d) + Q(d*(p+1), 24)

# The complete finite search justified in (25).
E = []
for d, upper in [(9, 2731), (11, 1400)]:
    row = []
    for p in primerange(452, upper):
        if (p-1) % (2*d):
            continue
        m = (p-1)//d
        if p % 8 == 7 and m % 3 and B(p, d) < T(p):
            row.append(p)
            E.append(p)
    print("index", d, ":", row)

# The possible d=8 interval contains no admissible p.
assert not [
    p for p in primerange(452, 461)
    if (p-1) % 16 == 0
]
E.sort()

# Matrix entries are stored as (a,b,c,d), representing [[a,b],[c,d]].
I = (1, 0, 0, 1)

def mul(x, y, p):
    a,b,c,d = x
    e,f,g,h = y
    return (
        (a*e+b*g) % p, (a*f+b*h) % p,
        (c*e+d*g) % p, (c*f+d*h) % p
    )

def scale(a, x, p):
    return tuple(a*z % p for z in x)

def add(*xs, p):
    return tuple(sum(v) % p for v in zip(*xs))

def inv(x, p):
    a,b,c,d = x
    z = pow((a*d-b*c) % p, -1, p)
    return scale(z, (d,-b,-c,a), p)

def closure(gens, p):
    S = {I}
    todo = [I]
    for x in todo:
        for g in gens:
            y = mul(x, g, p)
            if y not in S:
                S.add(y)
                todo.append(y)
    return S

def conjugacy_count(H, gens, p):
    pairs = [(g, inv(g,p)) for g in gens]
    remaining = set(H)
    answer = 0
    while remaining:
        x = next(iter(remaining))
        orbit = {x}
        todo = [x]
        for y in todo:
            for g, gi in pairs:
                z = mul(mul(g,y,p), gi, p)
                if z not in orbit:
                    orbit.add(z)
                    todo.append(z)
        assert orbit <= remaining
        remaining.difference_update(orbit)
        answer += 1
    return answer

for p in E:
    m = (p-1)//9

    # Find a^2+b^2 = -1, giving quaternion generators i,j.
    a = b = None
    for aa in range(p):
        for bb in range(p):
            if (aa*aa + bb*bb + 1) % p == 0:
                a,b = aa,bb
                break
        if a is not None:
            break

    r = next(x for x in range(p) if x*x % p == 2)

    i = (0,1,p-1,0)
    j = (a,b,b,-a % p)
    k = mul(i,j,p)
    t = scale(
        pow(2,-1,p),
        add(scale(-1,I,p), i,j,k, p=p), p
    )
    s = scale(pow(r,-1,p), add(i,j,p=p), p)

    # Binary octahedral group.
    O = closure([i,j,t,s], p)
    assert len(O) == 48

    # Scalar subgroup of order m.
    z = pow(int(primitive_root(p)), (p-1)//m, p)
    H = {
        scale(pow(z,a,p), h, p)
        for a in range(m) for h in O
    }
    assert len(H) == 24*m

    gens = [i,j,t,s,scale(z,I,p)]
    assert closure(gens,p) == H

    # Solvability certificate: Q8 normal in O, quotient of order 6;
    # H is obtained from O by adjoining central scalars.
    Q8 = closure([i,j],p)
    assert len(Q8) == 8 and Q8 <= O
    assert all(
        mul(mul(g,x,p),inv(g,p),p) in Q8
        for g in [t,s] for x in Q8
    )

    # Every nonidentity element of H fixes no nonzero vector.
    for h in H - {I}:
        a,b,c,d = h
        assert ((a-1)*(d-1)-b*c) % p != 0

    # Actual conjugacy-orbit enumeration in H.
    kh = conjugacy_count(H,gens,p)
    assert kh == 4*m

    # Exact affine class count for a fixed-point-free action.
    assert (p*p-1) % len(H) == 0
    kg = kh + (p*p-1)//len(H)
    assert kg < T(p)

    print(p, "|H| =",len(H), "k(H) =",kh, "k(G) =",kg)

print("E =",E)
```

Its output is:

```text
index 9 : [631, 991, 1063, 1279, 1423, 2143, 2287, 2503, 2719]
index 11 : []
631 |H| = 1680 k(H) = 280 k(G) = 517
991 |H| = 2640 k(H) = 440 k(G) = 812
1063 |H| = 2832 k(H) = 472 k(G) = 871
1279 |H| = 3408 k(H) = 568 k(G) = 1048
1423 |H| = 3792 k(H) = 632 k(G) = 1166
2143 |H| = 5712 k(H) = 952 k(G) = 1756
2287 |H| = 6096 k(H) = 1016 k(G) = 1874
2503 |H| = 6672 k(H) = 1112 k(G) = 2051
2719 |H| = 7248 k(H) = 1208 k(G) = 2228
E = [631, 991, 1063, 1279, 1423, 2143, 2287, 2503, 2719]
```

The reduction proves that no other prime can occur, and the matrix constructions prove that every listed prime does occur. Thus the displayed set is exactly \(\mathcal E\); nothing remains to be settled.

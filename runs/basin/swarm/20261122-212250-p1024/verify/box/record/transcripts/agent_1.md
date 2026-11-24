# agent_1: the whole run

[user message]
Let \(g\geq2\) be an integer, and set
\[
r=\left\lfloor\frac{g+2}{3}\right\rfloor,\qquad k=g-r.
\]
Let \(C_g\) be the smooth projective completion over \(\mathbb C\) of the affine curve
\[
z^2=x^{2g+1}-1,
\]
and let \(p\) be its unique point over infinity. Choose the local parameter \(t\) at \(p\) satisfying
\[
x=t^{-2},\qquad z=t^{-(2g+1)}(1-t^{4g+2})^{1/2},
\]
where the square root has value \(1\) at \(t=0\).

For a nonzero vector \(b=(b_0,\ldots,b_{r-1})\in\mathbb C^r\), define
\[
\phi_b(t)=\sum_{j=0}^{r-1}b_jt^{-(2g-1-2j)}.
\]
Choose coordinate discs \(W_0\Subset W\) centered at \(p\), with \(t\) defined on a neighborhood of \(\overline W\), and put \(U=C_g\setminus\overline{W_0}\). Take product neighborhoods of the zero sections over \(U\) and \(W\), with fiber coordinates \(y_U\) and \(y_W\). After shrinking the fiber directions, glue them over \(U\cap W\), preserving the base point, by
\[
y_W=t^{-1}y_U\bigl(1+k\phi_b(t)y_U^k\bigr)^{-1/k}.
\]
The fractional power denotes the holomorphic branch whose value is \(1\) at \(y_U=0\).

Let \(X_b\) be the resulting smooth analytic surface germ along its zero section \(E\simeq C_g\). Its normal bundle is \(\mathcal O_{C_g}(-p)\), and contracting \(E\) gives a normal surface singularity \((V_b,0)\) with minimal good resolution \(f_b:(X_b,E)\to(V_b,0)\). For cohomology, take \(X_b\) to be the inverse image of a sufficiently small Stein representative of this singularity.

Write \(\mathcal I_E\) for the ideal sheaf of \(E\), and define the logarithmic tangent sheaf by
\[
S_b=\{D\in\Theta_{X_b}:D(\mathcal I_E)\subseteq\mathcal I_E\},
\]
where \(\Theta_{X_b}\) is the sheaf of holomorphic vector fields. Put \(L_b=\bigwedge^2S_b\) and \(h^1(X_b,\mathcal F)=\dim_{\mathbb C}H^1(X_b,\mathcal F)\). Determine the exact formula, as a function of \(g\) and the entire coefficient vector \(b\), for
\[
\Delta_b=h^1(X_b,\mathcal O_{X_b})-h^1(X_b,S_b)+h^1(X_b,L_b),
\]
for every allowed nonzero \(b\), including vectors with vanishing components.

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
[tool call: write_scratchpad]
content:
```
from fractions import Fraction
from math import comb
import sys
P=1000003

def polyadd(a,b,c=1):
    d=a.copy()
    for i,v in b.items():
        d[i]=(d.get(i,0)+c*v)%P
        if not d[i]: del d[i]
    return d

def polymul(a,b):
    d={}
    for i,v in a.items():
        for j,w in b.items(): d[i+j]=(d.get(i+j,0)+v*w)%P
    return {i:v for i,v in d.items() if v}

def add(a,b,c=1): return (polyadd(a[0],b[0],c),polyadd(a[1],b[1],c))
def scale(a,c): return ({i:v*c%P for i,v in a[0].items() if v*c%P},{i:v*c%P for i,v in a[1].items() if v*c%P})
def shift(a,n): return ({i+n:v for i,v in a[0].items()},{i+n:v for i,v in a[1].items()})
def mul(a,b):
    q=polymul(a[1],b[1])
    return (polyadd(polyadd(polymul(a[0],b[0]),q),{i+H:v for i,v in q.items()},-1),polyadd(polymul(a[0],b[1]),polymul(a[1],b[0])))
def valcoef(a,q):
    out=a[0].get(q,0)
    for e,v in a[1].items():
        if q>=e and (q-e)%H==0: out+=v*hcoef((q-e)//H)
    return out%P

def hcoef(n):
    c=1
    for i in range(n): c=c*(1-2*i)*pow(2*(i+1),-1,P)*(-1)%P
    return c

def mon(q,c=1): return ({q:c%P},{})
def afun(s):
    if s%2==0: return mon(-s)
    return ({},{-s:1})
def split(a,lam):
    # a=f+eta+t^-lam*w; f in A, eta in H1, w regular
    rem=(a[0].copy(),a[1].copy()); eta={}
    low=min([0]+list(rem[0])+list(rem[1]))
    for q in range(low,-lam):
        c=valcoef(rem,q)
        if not c: continue
        s=-q
        if (s>=0 and s%2==0) or s>=2*g+1:
            rem=add(rem,scale(afun(s),c),-1)
        else:
            eta[q]=c
            rem=add(rem,mon(q,c),-1)
    return eta,shift(rem,lam)

def rankmod(cols,rows):
    piv={}
    for c in cols:
        c={i:v%P for i,v in c.items() if v%P}
        while c:
            i=min(c); v=c[i]
            if i in piv:
                c=polyadd(c,piv[i],-v)
            else:
                piv[i]={j:w*pow(v,-1,P)%P for j,w in c.items()}; break
    return len(piv)

def calc(gg,b,kind,ret=False):
    global g,H
    g=gg; H=4*g+2; d=2*g-2; k=g-(g+2)//3; M=4*g-3
    phi=({-(2*g-1-2*j):v%P for j,v in enumerate(b) if v%P},{})
    phip=({e-1:e*v%P for e,v in phi[0].items()},{})
    kp=scale(phi,k)
    powers=[mon(0)]
    for j in range((M-1)//k): powers.append(mul(powers[-1],kp))
    def pw(alpha,a):
        c=1
        for j in range(a):c=c*(alpha-j)*pow(j+1,-1,P)%P
        return scale(powers[a],c)
    if kind=='S': inds=[(n,c) for n in range(M) for c in ['h','v']]
    else: inds=[(n,kind) for n in range(M)]
    size=len(inds); ls=[n-d if c in ['h','L'] else n for n,c in inds]
    R=[{} for i in inds]
    for j,(n,c) in enumerate(inds):
        alpha=-n*pow(k,-1,P)%P
        for a in range((M-1-n)//k+1):
            m=n+a*k
            if kind=='S':
                if c=='v': R[j][2*m+1]=shift(pw(alpha+1,a),-n)
                else:
                    R[j][2*m]=shift(pw(alpha,a),d-n)
                    vv=shift(pw(alpha,a),-n-1)
                    if a:
                        term=add(shift(kp,-1),phip)
                        vv=add(vv,shift(mul(pw(alpha,a-1),term),-n))
                    # multiply -h/2
                    R[j][2*m+1]=scale(mul(vv,({}, {0:1})),-pow(2,-1,P))
            else: R[j][m]=shift(pw(alpha+(kind=='L'),a),-n+(d if kind=='L' else 0))
    rows={}; h0=[]
    for i,lam in enumerate(ls):
        exps=[-s for s in range(1,2*g,2) if s>lam]+list(range(1,max(1,-lam)))
        for e in exps:rows[i,e]=len(rows)
        for s in range(max(-1,lam)+1):
            if s%2==0 or s>=2*g+1: h0.append((i,s))
    cols=[]
    for j,s in h0:
        w=shift(afun(s),ls[j]); vec={i:mul(v,w) for i,v in R[j].items() if i!=j}; col={}
        for i in range(j+1,size):
            if i not in vec: continue
            eta,w=split(vec[i],ls[i])
            for e,c in eta.items(): col[rows[i,e]]=c
            for l,v in R[i].items():
                if l!=i:vec[l]=add(vec.get(l,({},{})),mul(v,w),-1)
        if col:cols.append(col)
    rk=rankmod(cols,len(rows))
    return (rk,len(rows),len(h0),cols,rows) if ret else rk

if __name__=='__main__':
    for g in range(2,11):
        r=(g+2)//3
        bs=[[1]*r]+[[int(i==j) for i in range(r)] for j in range(r)]
        outs=[]
        for b in bs:
            rr=[calc(g,b,typ) for typ in ['O','S','L']]
            outs.append((b,rr,rr[1]-rr[0]-rr[2]))
        print(g,outs,flush=True)

```

[tool result]
```
Wrote scratchpad.py (125 lines).
```

## response 3
[tool call: run_scratchpad]
timeout_seconds: 200

[tool result]
```
[exit code 0, 0.2s]
--- stdout ---
2 [([1], [1, 3, 2], 0), ([1], [1, 3, 2], 0)]
3 [([1], [2, 5, 3], 0), ([1], [2, 5, 3], 0)]
4 [([1, 1], [5, 10, 6], -1), ([1, 0], [4, 9, 5], 0), ([0, 1], [5, 10, 6], -1)]
5 [([1, 1], [7, 14, 8], -1), ([1, 0], [5, 11, 6], 0), ([0, 1], [7, 14, 8], -1)]
6 [([1, 1], [9, 18, 10], -1), ([1, 0], [6, 13, 7], 0), ([0, 1], [9, 18, 10], -1)]
7 [([1, 1, 1], [14, 27, 15], -2), ([1, 0, 0], [8, 17, 9], 0), ([0, 1, 0], [13, 26, 14], -1), ([0, 0, 1], [14, 27, 15], -2)]
8 [([1, 1, 1], [17, 33, 18], -2), ([1, 0, 0], [9, 19, 10], 0), ([0, 1, 0], [15, 30, 16], -1), ([0, 0, 1], [17, 33, 18], -2)]
9 [([1, 1, 1], [20, 39, 21], -2), ([1, 0, 0], [10, 21, 11], 0), ([0, 1, 0], [17, 34, 18], -1), ([0, 0, 1], [20, 39, 21], -2)]
10 [([1, 1, 1, 1], [27, 52, 28], -3), ([1, 0, 0, 0], [12, 25, 13], 0), ([0, 1, 0, 0], [21, 42, 22], -1), ([0, 0, 1, 0], [26, 51, 27], -2), ([0, 0, 0, 1], [27, 52, 28], -3)]

--- stderr ---
(empty)
```

## response 4
[reasoning summary]
**Evaluating impossible Δ**

I'm wondering if the negative Δ could be impossible, and I'm thinking maybe it's a numerical code error with h0 affecting the scalar counts and formula. I suppose I should also check the baseline b, which I suspect should be set to zero. There seems to be a mix-up in how I'm approaching this, so I'll take a step back and double-check the calculations to ensure I'm on the right track.

[tool call: edit_scratchpad]
old_string: for g in range(2,11):
new_string: for g in range(2,8):

[tool result]
```
Edited scratchpad.py (1 replacement).
```

## response 5
[tool call: edit_scratchpad]
old_string: bs=[[1]*r]+[[int(i==j) for i in range(r)] for j in range(r)]
new_string: bs=[[0]*r,[1]*r]+[[int(i==j) for i in range(r)] for j in range(r)]

[tool result]
```
Edited scratchpad.py (1 replacement).
```

## response 6
[tool call: run_scratchpad]

[tool result]
```
[exit code 0, 0.1s]
--- stdout ---
2 [([0], [0, 1, 0], 1), ([1], [1, 3, 2], 0), ([1], [1, 3, 2], 0)]
3 [([0], [0, 1, 0], 1), ([1], [2, 5, 3], 0), ([1], [2, 5, 3], 0)]
4 [([0, 0], [0, 1, 0], 1), ([1, 1], [5, 10, 6], -1), ([1, 0], [4, 9, 5], 0), ([0, 1], [5, 10, 6], -1)]
5 [([0, 0], [0, 1, 0], 1), ([1, 1], [7, 14, 8], -1), ([1, 0], [5, 11, 6], 0), ([0, 1], [7, 14, 8], -1)]
6 [([0, 0], [0, 1, 0], 1), ([1, 1], [9, 18, 10], -1), ([1, 0], [6, 13, 7], 0), ([0, 1], [9, 18, 10], -1)]
7 [([0, 0, 0], [0, 1, 0], 1), ([1, 1, 1], [14, 27, 15], -2), ([1, 0, 0], [8, 17, 9], 0), ([0, 1, 0], [13, 26, 14], -1), ([0, 0, 1], [14, 27, 15], -2)]

--- stderr ---
(empty)
```

## response 7
[tool call: edit_scratchpad]
old_string:
```
if __name__=='__main__':
    for g in range(2,8):
        r=(g+2)//3
        bs=[[0]*r,[1]*r]+[[int(i==j) for i in range(r)] for j in range(r)]
        outs=[]
        for b in bs:
            rr=[calc(g,b,typ) for typ in ['O','S','L']]
            outs.append((b,rr,rr[1]-rr[0]-rr[2]))
        print(g,outs,flush=True)
```
new_string:
```
if __name__=='__main__':
    import itertools, collections
    for g in range(2,17):
        r=(g+2)//3
        bs=list(itertools.product([0,1,2],repeat=r)) if r<=4 else [[1]*r]+[[int(i==j) for i in range(r)] for j in range(r)]
        outs=collections.defaultdict(list)
        for b in bs:
            if not any(b): continue
            rr=[calc(g,b,typ) for typ in ['O','S','L']]
            outs[(max(i for i,v in enumerate(b) if v),rr[1]-rr[0]-rr[2])].append((b,rr))
        print(g,[(key,len(val),val[:2]) for key,val in outs.items()],flush=True)
```

[tool result]
```
Edited scratchpad.py (1 replacement).
```

## response 8
[tool call: run_scratchpad]
timeout_seconds: 200

[tool result]
```
[exit code 0, 6.1s]
--- stdout ---
2 [((0, 0), 2, [((1,), [1, 3, 2]), ((2,), [1, 3, 2])])]
3 [((0, 0), 2, [((1,), [2, 5, 3]), ((2,), [2, 5, 3])])]
4 [((1, -1), 6, [((0, 1), [5, 10, 6]), ((0, 2), [5, 10, 6])]), ((0, 0), 2, [((1, 0), [4, 9, 5]), ((2, 0), [4, 9, 5])])]
5 [((1, -1), 6, [((0, 1), [7, 14, 8]), ((0, 2), [7, 14, 8])]), ((0, 0), 2, [((1, 0), [5, 11, 6]), ((2, 0), [5, 11, 6])])]
6 [((1, -1), 6, [((0, 1), [9, 18, 10]), ((0, 2), [9, 18, 10])]), ((0, 0), 2, [((1, 0), [6, 13, 7]), ((2, 0), [6, 13, 7])])]
7 [((2, -2), 18, [((0, 0, 1), [14, 27, 15]), ((0, 0, 2), [14, 27, 15])]), ((1, -1), 6, [((0, 1, 0), [13, 26, 14]), ((0, 2, 0), [13, 26, 14])]), ((0, 0), 2, [((1, 0, 0), [8, 17, 9]), ((2, 0, 0), [8, 17, 9])])]
8 [((2, -2), 18, [((0, 0, 1), [17, 33, 18]), ((0, 0, 2), [17, 33, 18])]), ((1, -1), 6, [((0, 1, 0), [15, 30, 16]), ((0, 2, 0), [15, 30, 16])]), ((0, 0), 2, [((1, 0, 0), [9, 19, 10]), ((2, 0, 0), [9, 19, 10])])]
9 [((2, -2), 18, [((0, 0, 1), [20, 39, 21]), ((0, 0, 2), [20, 39, 21])]), ((1, -1), 6, [((0, 1, 0), [17, 34, 18]), ((0, 2, 0), [17, 34, 18])]), ((0, 0), 2, [((1, 0, 0), [10, 21, 11]), ((2, 0, 0), [10, 21, 11])])]
10 [((3, -3), 54, [((0, 0, 0, 1), [27, 52, 28]), ((0, 0, 0, 2), [27, 52, 28])]), ((2, -2), 18, [((0, 0, 1, 0), [26, 51, 27]), ((0, 0, 2, 0), [26, 51, 27])]), ((1, -1), 6, [((0, 1, 0, 0), [21, 42, 22]), ((0, 2, 0, 0), [21, 42, 22])]), ((0, 0), 2, [((1, 0, 0, 0), [12, 25, 13]), ((2, 0, 0, 0), [12, 25, 13])])]
11 [((3, -3), 54, [((0, 0, 0, 1), [31, 60, 32]), ((0, 0, 0, 2), [31, 60, 32])]), ((2, -2), 18, [((0, 0, 1, 0), [29, 57, 30]), ((0, 0, 2, 0), [29, 57, 30])]), ((1, -1), 6, [((0, 1, 0, 0), [23, 46, 24]), ((0, 2, 0, 0), [23, 46, 24])]), ((0, 0), 2, [((1, 0, 0, 0), [13, 27, 14]), ((2, 0, 0, 0), [13, 27, 14])])]
12 [((3, -3), 54, [((0, 0, 0, 1), [35, 68, 36]), ((0, 0, 0, 2), [35, 68, 36])]), ((2, -2), 18, [((0, 0, 1, 0), [32, 63, 33]), ((0, 0, 2, 0), [32, 63, 33])]), ((1, -1), 6, [((0, 1, 0, 0), [25, 50, 26]), ((0, 2, 0, 0), [25, 50, 26])]), ((0, 0), 2, [((1, 0, 0, 0), [14, 29, 15]), ((2, 0, 0, 0), [14, 29, 15])])]
13 [((4, -4), 2, [([1, 1, 1, 1, 1], [44, 85, 45]), ([0, 0, 0, 0, 1], [44, 85, 45])]), ((0, 0), 1, [([1, 0, 0, 0, 0], [16, 33, 17])]), ((1, -1), 1, [([0, 1, 0, 0, 0], [29, 58, 30])]), ((2, -2), 1, [([0, 0, 1, 0, 0], [38, 75, 39])]), ((3, -3), 1, [([0, 0, 0, 1, 0], [43, 84, 44])])]
14 [((4, -4), 2, [([1, 1, 1, 1, 1], [49, 95, 50]), ([0, 0, 0, 0, 1], [49, 95, 50])]), ((0, 0), 1, [([1, 0, 0, 0, 0], [17, 35, 18])]), ((1, -1), 1, [([0, 1, 0, 0, 0], [31, 62, 32])]), ((2, -2), 1, [([0, 0, 1, 0, 0], [41, 81, 42])]), ((3, -3), 1, [([0, 0, 0, 1, 0], [47, 92, 48])])]
15 [((4, -4), 2, [([1, 1, 1, 1, 1], [54, 105, 55]), ([0, 0, 0, 0, 1], [54, 105, 55])]), ((0, 0), 1, [([1, 0, 0, 0, 0], [18, 37, 19])]), ((1, -1), 1, [([0, 1, 0, 0, 0], [33, 66, 34])]), ((2, -2), 1, [([0, 0, 1, 0, 0], [44, 87, 45])]), ((3, -3), 1, [([0, 0, 0, 1, 0], [51, 100, 52])])]
16 [((5, -5), 2, [([1, 1, 1, 1, 1, 1], [65, 126, 66]), ([0, 0, 0, 0, 0, 1], [65, 126, 66])]), ((0, 0), 1, [([1, 0, 0, 0, 0, 0], [20, 41, 21])]), ((1, -1), 1, [([0, 1, 0, 0, 0, 0], [37, 74, 38])]), ((2, -2), 1, [([0, 0, 1, 0, 0, 0], [50, 99, 51])]), ((3, -3), 1, [([0, 0, 0, 1, 0, 0], [59, 116, 60])]), ((4, -4), 1, [([0, 0, 0, 0, 1, 0], [64, 125, 65])])]

--- stderr ---
(empty)
```

## response 9
[reasoning summary]
**Looking into parameter validation**

I need to run exact rational and symbolic checks to ensure there are no issues with the parameters. I'm wondering if I can adapt the P ring to use Sympy rational functions. It might be simpler to implement a new standalone version of the Sympy Laurent pair for coefficients, focusing on rational hcoef without modifications. I’ll aim for computations for g, possibly up to exactly 10. Let’s see how this unfolds!

[tool call: run_scratchpad]
timeout_seconds: 200

[tool result]
```
[exit code 0, 6.1s]
--- stdout ---
2 [((0, 0), 2, [((1,), [1, 3, 2]), ((2,), [1, 3, 2])])]
3 [((0, 0), 2, [((1,), [2, 5, 3]), ((2,), [2, 5, 3])])]
4 [((1, -1), 6, [((0, 1), [5, 10, 6]), ((0, 2), [5, 10, 6])]), ((0, 0), 2, [((1, 0), [4, 9, 5]), ((2, 0), [4, 9, 5])])]
5 [((1, -1), 6, [((0, 1), [7, 14, 8]), ((0, 2), [7, 14, 8])]), ((0, 0), 2, [((1, 0), [5, 11, 6]), ((2, 0), [5, 11, 6])])]
6 [((1, -1), 6, [((0, 1), [9, 18, 10]), ((0, 2), [9, 18, 10])]), ((0, 0), 2, [((1, 0), [6, 13, 7]), ((2, 0), [6, 13, 7])])]
7 [((2, -2), 18, [((0, 0, 1), [14, 27, 15]), ((0, 0, 2), [14, 27, 15])]), ((1, -1), 6, [((0, 1, 0), [13, 26, 14]), ((0, 2, 0), [13, 26, 14])]), ((0, 0), 2, [((1, 0, 0), [8, 17, 9]), ((2, 0, 0), [8, 17, 9])])]
8 [((2, -2), 18, [((0, 0, 1), [17, 33, 18]), ((0, 0, 2), [17, 33, 18])]), ((1, -1), 6, [((0, 1, 0), [15, 30, 16]), ((0, 2, 0), [15, 30, 16])]), ((0, 0), 2, [((1, 0, 0), [9, 19, 10]), ((2, 0, 0), [9, 19, 10])])]
9 [((2, -2), 18, [((0, 0, 1), [20, 39, 21]), ((0, 0, 2), [20, 39, 21])]), ((1, -1), 6, [((0, 1, 0), [17, 34, 18]), ((0, 2, 0), [17, 34, 18])]), ((0, 0), 2, [((1, 0, 0), [10, 21, 11]), ((2, 0, 0), [10, 21, 11])])]
10 [((3, -3), 54, [((0, 0, 0, 1), [27, 52, 28]), ((0, 0, 0, 2), [27, 52, 28])]), ((2, -2), 18, [((0, 0, 1, 0), [26, 51, 27]), ((0, 0, 2, 0), [26, 51, 27])]), ((1, -1), 6, [((0, 1, 0, 0), [21, 42, 22]), ((0, 2, 0, 0), [21, 42, 22])]), ((0, 0), 2, [((1, 0, 0, 0), [12, 25, 13]), ((2, 0, 0, 0), [12, 25, 13])])]
11 [((3, -3), 54, [((0, 0, 0, 1), [31, 60, 32]), ((0, 0, 0, 2), [31, 60, 32])]), ((2, -2), 18, [((0, 0, 1, 0), [29, 57, 30]), ((0, 0, 2, 0), [29, 57, 30])]), ((1, -1), 6, [((0, 1, 0, 0), [23, 46, 24]), ((0, 2, 0, 0), [23, 46, 24])]), ((0, 0), 2, [((1, 0, 0, 0), [13, 27, 14]), ((2, 0, 0, 0), [13, 27, 14])])]
12 [((3, -3), 54, [((0, 0, 0, 1), [35, 68, 36]), ((0, 0, 0, 2), [35, 68, 36])]), ((2, -2), 18, [((0, 0, 1, 0), [32, 63, 33]), ((0, 0, 2, 0), [32, 63, 33])]), ((1, -1), 6, [((0, 1, 0, 0), [25, 50, 26]), ((0, 2, 0, 0), [25, 50, 26])]), ((0, 0), 2, [((1, 0, 0, 0), [14, 29, 15]), ((2, 0, 0, 0), [14, 29, 15])])]
13 [((4, -4), 2, [([1, 1, 1, 1, 1], [44, 85, 45]), ([0, 0, 0, 0, 1], [44, 85, 45])]), ((0, 0), 1, [([1, 0, 0, 0, 0], [16, 33, 17])]), ((1, -1), 1, [([0, 1, 0, 0, 0], [29, 58, 30])]), ((2, -2), 1, [([0, 0, 1, 0, 0], [38, 75, 39])]), ((3, -3), 1, [([0, 0, 0, 1, 0], [43, 84, 44])])]
14 [((4, -4), 2, [([1, 1, 1, 1, 1], [49, 95, 50]), ([0, 0, 0, 0, 1], [49, 95, 50])]), ((0, 0), 1, [([1, 0, 0, 0, 0], [17, 35, 18])]), ((1, -1), 1, [([0, 1, 0, 0, 0], [31, 62, 32])]), ((2, -2), 1, [([0, 0, 1, 0, 0], [41, 81, 42])]), ((3, -3), 1, [([0, 0, 0, 1, 0], [47, 92, 48])])]
15 [((4, -4), 2, [([1, 1, 1, 1, 1], [54, 105, 55]), ([0, 0, 0, 0, 1], [54, 105, 55])]), ((0, 0), 1, [([1, 0, 0, 0, 0], [18, 37, 19])]), ((1, -1), 1, [([0, 1, 0, 0, 0], [33, 66, 34])]), ((2, -2), 1, [([0, 0, 1, 0, 0], [44, 87, 45])]), ((3, -3), 1, [([0, 0, 0, 1, 0], [51, 100, 52])])]
16 [((5, -5), 2, [([1, 1, 1, 1, 1, 1], [65, 126, 66]), ([0, 0, 0, 0, 0, 1], [65, 126, 66])]), ((0, 0), 1, [([1, 0, 0, 0, 0, 0], [20, 41, 21])]), ((1, -1), 1, [([0, 1, 0, 0, 0, 0], [37, 74, 38])]), ((2, -2), 1, [([0, 0, 1, 0, 0, 0], [50, 99, 51])]), ((3, -3), 1, [([0, 0, 0, 1, 0, 0], [59, 116, 60])]), ((4, -4), 1, [([0, 0, 0, 0, 1, 0], [64, 125, 65])])]

--- stderr ---
(empty)
```

## response 10
[tool call: read_scratchpad]

[tool result]
```
     1	from fractions import Fraction
     2	from math import comb
     3	import sys
     4	P=1000003
     5	
     6	def polyadd(a,b,c=1):
     7	    d=a.copy()
     8	    for i,v in b.items():
     9	        d[i]=(d.get(i,0)+c*v)%P
    10	        if not d[i]: del d[i]
    11	    return d
    12	
    13	def polymul(a,b):
    14	    d={}
    15	    for i,v in a.items():
    16	        for j,w in b.items(): d[i+j]=(d.get(i+j,0)+v*w)%P
    17	    return {i:v for i,v in d.items() if v}
    18	
    19	def add(a,b,c=1): return (polyadd(a[0],b[0],c),polyadd(a[1],b[1],c))
    20	def scale(a,c): return ({i:v*c%P for i,v in a[0].items() if v*c%P},{i:v*c%P for i,v in a[1].items() if v*c%P})
    21	def shift(a,n): return ({i+n:v for i,v in a[0].items()},{i+n:v for i,v in a[1].items()})
    22	def mul(a,b):
    23	    q=polymul(a[1],b[1])
    24	    return (polyadd(polyadd(polymul(a[0],b[0]),q),{i+H:v for i,v in q.items()},-1),polyadd(polymul(a[0],b[1]),polymul(a[1],b[0])))
    25	def valcoef(a,q):
    26	    out=a[0].get(q,0)
    27	    for e,v in a[1].items():
    28	        if q>=e and (q-e)%H==0: out+=v*hcoef((q-e)//H)
    29	    return out%P
    30	
    31	def hcoef(n):
    32	    c=1
    33	    for i in range(n): c=c*(1-2*i)*pow(2*(i+1),-1,P)*(-1)%P
    34	    return c
    35	
    36	def mon(q,c=1): return ({q:c%P},{})
    37	def afun(s):
    38	    if s%2==0: return mon(-s)
    39	    return ({},{-s:1})
    40	def split(a,lam):
    41	    # a=f+eta+t^-lam*w; f in A, eta in H1, w regular
    42	    rem=(a[0].copy(),a[1].copy()); eta={}
    43	    low=min([0]+list(rem[0])+list(rem[1]))
    44	    for q in range(low,-lam):
    45	        c=valcoef(rem,q)
    46	        if not c: continue
    47	        s=-q
    48	        if (s>=0 and s%2==0) or s>=2*g+1:
    49	            rem=add(rem,scale(afun(s),c),-1)
    50	        else:
    51	            eta[q]=c
    52	            rem=add(rem,mon(q,c),-1)
    53	    return eta,shift(rem,lam)
    54	
    55	def rankmod(cols,rows):
    56	    piv={}
    57	    for c in cols:
    58	        c={i:v%P for i,v in c.items() if v%P}
    59	        while c:
    60	            i=min(c); v=c[i]
    61	            if i in piv:
    62	                c=polyadd(c,piv[i],-v)
    63	            else:
    64	                piv[i]={j:w*pow(v,-1,P)%P for j,w in c.items()}; break
    65	    return len(piv)
    66	
    67	def calc(gg,b,kind,ret=False):
    68	    global g,H
    69	    g=gg; H=4*g+2; d=2*g-2; k=g-(g+2)//3; M=4*g-3
    70	    phi=({-(2*g-1-2*j):v%P for j,v in enumerate(b) if v%P},{})
    71	    phip=({e-1:e*v%P for e,v in phi[0].items()},{})
    72	    kp=scale(phi,k)
    73	    powers=[mon(0)]
    74	    for j in range((M-1)//k): powers.append(mul(powers[-1],kp))
    75	    def pw(alpha,a):
    76	        c=1
    77	        for j in range(a):c=c*(alpha-j)*pow(j+1,-1,P)%P
    78	        return scale(powers[a],c)
    79	    if kind=='S': inds=[(n,c) for n in range(M) for c in ['h','v']]
    80	    else: inds=[(n,kind) for n in range(M)]
    81	    size=len(inds); ls=[n-d if c in ['h','L'] else n for n,c in inds]
    82	    R=[{} for i in inds]
    83	    for j,(n,c) in enumerate(inds):
    84	        alpha=-n*pow(k,-1,P)%P
    85	        for a in range((M-1-n)//k+1):
    86	            m=n+a*k
    87	            if kind=='S':
    88	                if c=='v': R[j][2*m+1]=shift(pw(alpha+1,a),-n)
    89	                else:
    90	                    R[j][2*m]=shift(pw(alpha,a),d-n)
    91	                    vv=shift(pw(alpha,a),-n-1)
    92	                    if a:
    93	                        term=add(shift(kp,-1),phip)
    94	                        vv=add(vv,shift(mul(pw(alpha,a-1),term),-n))
    95	                    # multiply -h/2
    96	                    R[j][2*m+1]=scale(mul(vv,({}, {0:1})),-pow(2,-1,P))
    97	            else: R[j][m]=shift(pw(alpha+(kind=='L'),a),-n+(d if kind=='L' else 0))
    98	    rows={}; h0=[]
    99	    for i,lam in enumerate(ls):
   100	        exps=[-s for s in range(1,2*g,2) if s>lam]+list(range(1,max(1,-lam)))
   101	        for e in exps:rows[i,e]=len(rows)
   102	        for s in range(max(-1,lam)+1):
   103	            if s%2==0 or s>=2*g+1: h0.append((i,s))
   104	    cols=[]
   105	    for j,s in h0:
   106	        w=shift(afun(s),ls[j]); vec={i:mul(v,w) for i,v in R[j].items() if i!=j}; col={}
   107	        for i in range(j+1,size):
   108	            if i not in vec: continue
   109	            eta,w=split(vec[i],ls[i])
   110	            for e,c in eta.items(): col[rows[i,e]]=c
   111	            for l,v in R[i].items():
   112	                if l!=i:vec[l]=add(vec.get(l,({},{})),mul(v,w),-1)
   113	        if col:cols.append(col)
   114	    rk=rankmod(cols,len(rows))
   115	    return (rk,len(rows),len(h0),cols,rows) if ret else rk
   116	
   117	if __name__=='__main__':
   118	    import itertools, collections
   119	    for g in range(2,17):
   120	        r=(g+2)//3
   121	        bs=list(itertools.product([0,1,2],repeat=r)) if r<=4 else [[1]*r]+[[int(i==j) for i in range(r)] for j in range(r)]
   122	        outs=collections.defaultdict(list)
   123	        for b in bs:
   124	            if not any(b): continue
   125	            rr=[calc(g,b,typ) for typ in ['O','S','L']]
   126	            outs[(max(i for i,v in enumerate(b) if v),rr[1]-rr[0]-rr[2])].append((b,rr))
   127	        print(g,[(key,len(val),val[:2]) for key,val in outs.items()],flush=True)

(127 lines total)
```

## response 11
[reasoning summary]
**Exploring code evaluation strategy**

I'm thinking about the need for potentially negative values, which contradicts my previous assumptions. It’s important to build the final code accurately and run more symbolic cancellations instead of relying solely on full symbolic algebra. I can explore rational random numbers and roots for certain checks. I should also ensure that my code checks for the rank and valid relationships within dimensions, using sympy functions to handle determinants effectively. Incorporating fractions to keep it rational seems sufficient for my task.

**Building polynomial checks**

I need to include specific polynomial matrix transition checks using sympy for differentiation and to ensure Hankel's full symbolic checks across multiple sizes. I’ll confirm the minor determinants for specific row selections and consider various cases based on parameters. If conditions meet, I’ll take selective columns and rows to build a proper structure. The final code should be around 150 lines to illustrate these transformations clearly. I want to simplify the algebra into a class structure, aiming for around 160 lines total.

[tool call: write_scratchpad]
content:
```
from fractions import Fraction as Q
from functools import lru_cache
from itertools import product
import sympy as sp

# Exact Laurent algebra: pairs (P,Q) mean P(t)+Q(t)*h(t),
# where h^2=1-t^(4g+2). No series truncation is used.
def pa(a,b,c=1):
    z=a.copy()
    for i,v in b.items():
        z[i]=z.get(i,0)+c*v
        if not z[i]: del z[i]
    return z

def pm(a,b):
    z={}
    for i,v in a.items():
        for j,w in b.items(): z[i+j]=z.get(i+j,0)+v*w
    return {i:v for i,v in z.items() if v}

def add(a,b,c=1): return pa(a[0],b[0],c),pa(a[1],b[1],c)
def sc(a,c): return tuple({i:v*c for i,v in p.items() if v*c} for p in a)
def sh(a,n): return tuple({i+n:v for i,v in p.items()} for p in a)
def mon(n,c=1): return ({n:Q(c)} if c else {},{})
def mul(a,b):
    q=pm(a[1],b[1])
    return pa(pa(pm(a[0],b[0]),q),{i+H:v for i,v in q.items()},-1),pa(pm(a[0],b[1]),pm(a[1],b[0]))

@lru_cache(None)
def hc(n):
    return Q(1) if n==0 else hc(n-1)*Q(2*n-3,2*n)

def coeff(a,n):
    return a[0].get(n,0)+sum(v*hc((n-i)//H) for i,v in a[1].items() if n>=i and (n-i)%H==0)

def af(s):
    return mon(-s) if s%2==0 else ({},{-s:Q(1)})

def split(a,lam):
    # Returns eta,w with a = f + eta + t^(-lam)w,
    # f in A and w in C[[t]].
    a=(a[0].copy(),a[1].copy()); eta={}
    for n in range(min([0]+list(a[0])+list(a[1])),-lam):
        c=coeff(a,n)
        if not c: continue
        s=-n
        if (s>=0 and s%2==0) or s>=2*g+1:
            a=add(a,sc(af(s),c),-1)
        else:
            eta[n]=c
            a=add(a,mon(n,c),-1)
    w=sh(a,lam)
    # Check formal regularity, including cancellations between P and Qh.
    for n in range(min([0]+list(w[0])+list(w[1])),0):
        assert coeff(w,n)==0
    return eta,w

def rank(cols):
    piv={}
    for c in cols:
        c={i:Q(v) for i,v in c.items() if v}
        while c:
            i=min(c); v=c[i]
            if i in piv: c=pa(c,piv[i],-v)
            else:
                piv[i]={j:w/v for j,w in c.items()}; break
    return len(piv)

def cech(gg,b,kind):
    global g,H
    g=gg; H=4*g+2; d=2*g-2; k=g-(g+2)//3; M=2*d+1
    phi=({-(2*g-1-2*j):Q(v) for j,v in enumerate(b) if v},{})
    phip=({e-1:e*v for e,v in phi[0].items()},{})
    kp=sc(phi,k); powers=[mon(0)]
    for a in range((M-1)//k): powers.append(mul(powers[-1],kp))
    def power(alpha,a):
        c=Q(1)
        for j in range(a): c*=Q(alpha-j,j+1)
        return sc(powers[a],c)
    inds=[(n,c) for n in range(M) for c in ('h','v')] if kind=='S' else [(n,kind) for n in range(M)]
    lam=[n-d if c in ('h','L') else n for n,c in inds]
    R=[{} for _ in inds]
    for j,(n,c) in enumerate(inds):
        alpha=-Q(n,k)
        for a in range((M-1-n)//k+1):
            m=n+a*k
            if kind!='S':
                R[j][m]=sh(power(alpha+(kind=='L'),a),-n+(d if kind=='L' else 0))
            elif c=='v':
                R[j][2*m+1]=sh(power(alpha+1,a),-n)
            else:
                R[j][2*m]=sh(power(alpha,a),d-n)
                v=sh(power(alpha,a),-n-1)
                if a: v=add(v,sh(mul(power(alpha,a-1),add(sh(kp,-1),phip)),-n))
                R[j][2*m+1]=sc(mul(v,({}, {0:Q(1)})),-Q(1,2))
    rows={}; h0=[]
    for i,l in enumerate(lam):
        exps=[-s for s in range(1,2*g,2) if s>l]+list(range(1,max(1,-l)))
        for e in exps: rows[i,e]=len(rows)
        for s in range(max(-1,l)+1):
            if s%2==0 or s>=2*g+1: h0.append((i,s))
    cols=[]
    for j,s in h0:
        w=sh(af(s),lam[j])
        v={i:mul(p,w) for i,p in R[j].items() if i!=j}; col={}
        for i in range(j+1,len(inds)):
            if i not in v: continue
            eta,w=split(v[i],lam[i])
            for e,c in eta.items(): col[rows[i,e]]=c
            for ell,p in R[i].items():
                if ell!=i: v[ell]=add(v.get(ell,({},{})),mul(p,w),-1)
        cols.append(col)
    return len(rows)-rank(cols),rank(cols)

def checks():
    # Symbolically check the inverse fiber transition and its derivatives.
    t,u,k,F,Fp=sp.symbols('t u k F Fp',nonzero=True)
    # e_W=(1+kFu^k)e_U; dt|v(u)/u is the following expression.
    B=1+k*F*u**k
    logv_t=-1/t-Fp*u**k/B
    logv_e=1/B
    inv_e=sp.simplify(-logv_t/logv_e)
    assert sp.simplify(inv_e-(1/t+(k*F/t+Fp)*u**k))==0
    assert sp.simplify(logv_e*B)==1
    # Uniform symbolic pivot minors for every rectangular Hankel shape tested.
    for m in range(9):
        bs=sp.symbols('b:'+str(m+1))
        for a in range(1,m+5):
            for q in range(1,m+5):
                if max(a,q)<m+1: continue
                s=min(a,q,m+1)
                start=m-s+1
                mat=sp.Matrix(s,s,lambda i,j: bs[start+i+j] if start+i+j<=m else 0)
                assert sp.expand(mat.det()-(-1)**(s*(s-1)//2)*bs[m]**s)==0
    # Check the integer inequalities and the closed rank sum over a wide range.
    for g in range(2,301):
        r=(g+2)//3; k=g-r; d=2*g-2; N=d-k
        assert d<=3*k and N>=4*(r-1)
        for m in range(r):
            aa=[min(n//2+1,(N-n)//2+1,m+1) for n in range(N+1)]
            assert sum(aa[1:])==(m+1)*(g+r-1-2*m)-1
            assert aa[k]==m+1
    # Independent full-transition, exact-rational Cech computations.
    count=0
    for gg in range(2,13):
        r=(gg+2)//3
        vectors=list(product((-1,0,1),repeat=r)) if r<=3 else []
        vectors += [tuple(int(i==j) for i in range(r)) for j in range(r)]
        vectors += [tuple(Q((-2)**i,i+1) for i in range(r))]
        for b in vectors:
            if not any(b): continue
            m=max(i for i,v in enumerate(b) if v)
            R=(m+1)*(gg+r-1-2*m)-1
            vals=[cech(gg,b,c) for c in ('O','S','L')]
            expected=[(gg*gg-R,R),(6*gg*gg-7*gg+2-2*R+m,2*R+1-m),(5*gg*gg-7*gg+2-R,R+1)]
            assert vals==expected,(gg,b,vals,expected)
            assert vals[0][0]-vals[1][0]+vals[2][0]==-m
            count+=1
    print('All exact checks passed;',count,'full-transition examples.')

if __name__=='__main__': checks()

```

[tool result]
```
Wrote scratchpad.py (161 lines).
```

## response 12
[tool call: run_scratchpad]
timeout_seconds: 200

[tool result]
```
[killed after 200s timeout, 202.0s]
--- stdout ---
(empty)
--- stderr ---
Timeout (0:03:20)!
Thread 0x00000001f619e180 (most recent call first):
  File "__pow__"
```

## response 13
[tool call: edit_scratchpad]
old_string: for m in range(9):
new_string: for m in range(6):

[tool result]
```
Edited scratchpad.py (1 replacement).
```

## response 14
[tool call: edit_scratchpad]
old_string: mat.det()-(-1)**(s*(s-1)//2)*bs[m]**s
new_string: mat.det(method='domain-ge')-(-1)**(s*(s-1)//2)*bs[m]**s

[tool result]
```
Edited scratchpad.py (1 replacement).
```

## response 15
[tool call: edit_scratchpad]
old_string: for g in range(2,301):
new_string: for g in range(2,101):

[tool result]
```
Edited scratchpad.py (1 replacement).
```

## response 16
[tool call: run_scratchpad]
timeout_seconds: 200

[tool result]
```
[exit code 0, 3.6s]
--- stdout ---
All exact checks passed; 146 full-transition examples.

--- stderr ---
(empty)
```

## response 17
[reasoning summary]
**Explaining theorems**

I need to look into the theorem related to formal functions, although I won't provide a full proof since foundational aspects are permitted. It seems important to explain the small Stein inverse image properly. I believe formal functions guarantee isomorphism as a module of finite length, particularly when all elements of grad H1 vanish. This should clarify some nuances around these concepts for anyone interested in the depths of mathematical theory.

[reasoning summary]
**Evaluating code checks**

I'm looking into my concern that code "cech" only uses kind OSL, and I've confirmed that the proof checked via ranks OSL is sufficient. I verified symbolic minors and did derivative checks. However, I noted that it doesn't compute inverse transitions, but this seems trivial. While I could add more symmetry verifications, such as a wedge determinant or series formula, it's not crucial for the user. Existing checks are adequate, ensuring regularity every split is exact.

[message]
Put
\[
m=\max\{j:b_j\ne0\}.
\]
Then the answer is
\[
\boxed{\Delta_b=-m.}
\]
Thus the answer depends on the last nonzero component, not on the first nonzero component. In particular, it can be negative.

We prove this for every complex coefficient vector in the question. We also give an exact-arithmetic program which computes the cohomology directly from the full transition functions, independently of the final formula.

## 1. Some notation and the individual cohomology dimensions

Write
\[
d=2g-2,\qquad N=d-k=g+r-2,
\]
and set
\[
R=(m+1)(g+r-1-2m)-1.
\]
In fact, we will prove the stronger formulas
\[
\begin{aligned}
h^1(X_b,\mathcal O_{X_b})&=g^2-R,\\
h^1(X_b,S_b)&=6g^2-7g+2-2R+m,\\
h^1(X_b,L_b)&=5g^2-7g+2-R.
\end{aligned}                                                    \tag{1}
\]
Their alternating sum is \(-m\).

Hereafter all sheaves on a sufficiently small neighborhood of \(E\) can equivalently be considered on its formal completion. We justify the finite truncation used below.

## 2. Reduction to a finite cohomology calculation

Let \(\pi:X_b\to C_g\) be the projection preserved by the gluing. Along \(E\),
\[
\mathcal I_E^n/\mathcal I_E^{n+1}\simeq\mathcal O_{C_g}(np).
\]
There is an exact sequence
\[
0\longrightarrow\mathcal O_{C_g}
\longrightarrow S_b|_E
\longrightarrow\Theta_{C_g}
\longrightarrow0,
\]
and \(L_b|_E\simeq\Theta_{C_g}\).

The differential \(dx/z\) has divisor \(dp\). Consequently,
\[
\Theta_{C_g}\simeq\mathcal O_{C_g}(-dp).
\]
It follows that, for each of \(\mathcal O_{X_b},S_b,L_b\),
\[
H^1\!\left(E,\mathcal I_E^n\mathcal F/
                      \mathcal I_E^{n+1}\mathcal F\right)=0
\quad(n>2d).
\]
Indeed, this follows from Serre duality for the two line bundles
\(\mathcal O(np)\) and \(\mathcal O((n-d)p)\).

Thus the cohomology of the successive infinitesimal neighborhoods stabilizes at
\[
M=2d+1=4g-3.
\]
The theorem on formal functions, applied to the proper resolution over the Stein representative, gives
\[
H^1(X_b,\mathcal F)
 \simeq H^1\!\left(E,\mathcal F/\mathcal I_E^M\mathcal F\right).       \tag{2}
\]
Here the higher direct image is supported at the contracted point, so its completion is the same finite-dimensional vector space. This proves that the calculation below is finite and computes the analytic cohomology specified in the question.

## 3. Scalar Čech reduction on \(C_g\)

Set
\[
h(t)=(1-t^{4g+2})^{1/2},\qquad
A=\mathbb C[x,z]/(z^2-x^{2g+1}+1).
\]
The functions regular away from \(p\) have the basis
\[
x^a=t^{-2a},\qquad
zx^a=t^{-(2g+1+2a)}h(t).
\]
Thus the gap sequence at \(p\) is
\[
1,3,\ldots,2g-1.                                                   \tag{3}
\]

For the line bundle \(\mathcal O(\lambda p)\), a convenient basis for its first cohomology is
\[
\left\{t^{-(2i-1)}:1\le i\le g,\ 2i-1>\lambda\right\}
\ \cup\
\left\{t,t^2,\ldots,t^{-\lambda-1}\right\},                          \tag{4}
\]
where the second set is empty when \(\lambda\ge-1\).

Explicitly, any Laurent series can be reduced modulo
\[
A+t^{-\lambda}\mathbb C[[t]]
\]
to the span in (4): eliminate nongap poles using the displayed basis of \(A\), and then remove the part in \(t^{-\lambda}\mathbb C[[t]]\). This reduction can be chosen to preserve parity under \(t\mapsto-t\).

We use the following elementary consequence of this reduction. Suppose a vector bundle has a triangular transition matrix whose diagonal entries are \(t^{-\lambda_i}\). Eliminating the scalar Čech coboundaries gives a finite complex
\[
\bigoplus_i H^0\bigl(\mathcal O(\lambda_i p)\bigr)
 \xrightarrow{D}
\bigoplus_i H^1\bigl(\mathcal O(\lambda_i p)\bigr),                   \tag{5}
\]
and
\[
h^1=\sum_i h^1\bigl(\mathcal O(\lambda_i p)\bigr)-\operatorname{rank}D.
                                                                    \tag{6}
\]
This is ordinary block Gaussian elimination of the Čech differential. To construct a column of \(D\), begin with a diagonal global section, apply the off-diagonal transition terms, and repeatedly perform the scalar reduction above in increasing triangular order. This also describes the algorithm used in the code below.

## 4. The actual transition matrices

Abbreviate \(u=y_U\), \(v=y_W\), \(\phi=\phi_b\), and put
\[
P=1+k\phi u^k.
\]
Then
\[
v=t^{-1}uP^{-1/k}.
\]

On the \(U\)-chart let
\[
\epsilon_U=u\partial_u,\qquad
\delta_U(x)=z,\quad
\delta_U(z)=\frac{2g+1}{2}x^{2g},
\]
with \(\delta_U(u)=0\). On the \(W\)-chart let
\[
\epsilon_W=v\partial_v,\qquad
\eta_W=-\frac{h(t)}2\partial_t,
\]
where \(\partial_t\) holds \(v\) fixed. Since
\[
\delta_U(t)=-\frac12t^{-d}h(t),
\]
direct differentiation gives
\[
\begin{aligned}
\epsilon_W&=P\epsilon_U,\\
\eta_W&=t^d\delta_U
-\frac h2\left(\frac1t+
       \left(\frac{k\phi}{t}+\phi'\right)u^k\right)\epsilon_U,\\
\eta_W\wedge\epsilon_W&=t^dP\,\delta_U\wedge\epsilon_U.
\end{aligned}                                                       \tag{7}
\]

Let \(\mathcal T\) denote the vertical logarithmic tangent line bundle, and let
\(\mathcal Q=\pi^*\Theta_{C_g}\). There is an exact sequence
\[
0\longrightarrow\mathcal T\longrightarrow S_b
 \longrightarrow\mathcal Q\longrightarrow0.                        \tag{8}
\]

For each of the four line bundles
\(\mathcal O,\mathcal T,\mathcal Q,L_b\), its transition on the fiber-degree-\(n\) basis vector has the scalar form
\[
u^n t^{e-n}P^{\,c-n/k},                                             \tag{9}
\]
with the following values:
\[
\begin{array}{c|cc}
 &e&c\\ \hline
\mathcal O&0&0\\
\mathcal T&0&1\\
\mathcal Q&d&0\\
L_b&d&1.
\end{array}                                                        \tag{10}
\]
The diagonal summand in degree \(n\) is therefore
\(\mathcal O((n-e)p)\).

## 5. Why only the first nonlinear block affects the rank

Consider one of the scalar transitions (9). Put \(s=n-e\). A diagonal global section relevant to a nonlinear obstruction has
\[
0\le s\le N=d-k.
\]
Its basis consists only of \(1,x,\ldots,x^{\lfloor s/2\rfloor}\), since \(s<2g+1\).

The first nonlinear obstruction, from degree \(n\) to \(n+k\), is
\[
(kc-n)\,[\phi f]\in H^1\bigl(\mathcal O((s+k)p)\bigr).               \tag{11}
\]
All later terms increase fiber degree by multiples of \(k\).

We claim that the rank in (5) is the sum of the ranks of the first blocks (11). Here are the details that rule out hidden higher obstructions.

* Each multiplication by \(\phi\) reverses \(t\)-parity.
* The scalar reductions preserve parity.
* All obstruction targets reached from a global section have
  \(\lambda=s+ak>0\); their \(H^1\)-bases consist only of odd negative powers.
* Hence every second-order block is zero.
* From the definition of \(r\),
  \[
  d\le3k.
  \]
  Thus an odd block of order at least three can occur only when
  \(d=3k\), at order three, and from \(s=0\).

The last possible block cannot increase the rank. Its source is one-dimensional. For \(\mathcal O\) that source is the global constant and its entire column is zero. In the other three cases its first block is nonzero, and no other source contributes to that first target degree. It is already an isolated pivot column; any third-order entry in that column can be removed without changing the rank.

This proves the claim, including the borderline case \(d=3k\).

## 6. The first blocks are truncated Hankel matrices

For \(0\le s\le N\), let \(a_s\) be the rank of
\[
H^0(\mathcal O(sp))
 \xrightarrow{\ f\mapsto[\phi f]\ }
H^1(\mathcal O((s+k)p)).
\]
The source has dimension \(\lfloor s/2\rfloor+1\), and the target has dimension
\(\lfloor(N-s)/2\rfloor+1\). In the bases above, its matrix is
\[
(b_{i+\ell})_{\substack{0\le i<\lfloor(N-s)/2\rfloor+1\\
                       0\le\ell<\lfloor s/2\rfloor+1}},             \tag{12}
\]
with \(b_j=0\) for \(j>m\).

There are no additional contributions to (12) from eliminating nongap poles: the poles of \(\phi x^\ell\) have order less than \(4g+2\), so the \(h(t)-1\) correction produces only positive powers, which vanish in these targets.

We have
\[
N\ge4(r-1)\ge4m.
\]
Consequently at least one dimension of the rectangle (12) is at least \(m+1\). The last nonzero antidiagonal is \(b_m\). The appropriate square minor of size
\[
q=\min\left(\left\lfloor\frac s2\right\rfloor+1,\
             \left\lfloor\frac{N-s}2\right\rfloor+1,\
             m+1\right)
\]
has determinant
\[
(-1)^{q(q-1)/2}b_m^q\ne0.
\]
All larger minors vanish. Hence, uniformly for every allowed vector,
\[
a_s=
\min\left(\left\lfloor\frac s2\right\rfloor+1,\
          \left\lfloor\frac{N-s}2\right\rfloor+1,\
          m+1\right).                                             \tag{13}
\]
In particular,
\[
a_0=1,\qquad a_k=m+1.                                              \tag{14}
\]

Define \(R=\sum_{s=1}^N a_s\). Summing the two symmetric tails of (13) gives
\[
R=(m+1)(N+1-2m)-1
 =(m+1)(g+r-1-2m)-1,                                               \tag{15}
\]
as asserted earlier.

The coefficients \(kc-n\) in (11) now give the ranks of the reduced differentials:
\[
\begin{array}{c|c}
\text{line bundle}&\operatorname{rank}D\\ \hline
\mathcal O&R\\
\mathcal T&R+1-a_k=R-m\\
\mathcal Q&R+1\\
L_b&R+1.
\end{array}                                                        \tag{16}
\]
Indeed, \(\mathcal O\) omits \(s=0\), \(\mathcal T\) omits \(s=k\), and neither \(\mathcal Q\) nor \(L_b\) has a zero coefficient.

## 7. The extension defining \(S_b\)

One must still check that simply adding the two line-bundle ranks in (16) correctly handles (8).

After the same scalar Čech reductions, the differential for \(S_b\), with horizontal and vertical parts separated, has the form
\[
D_S=
\begin{pmatrix}
D_{\mathcal Q}&0\\
C&D_{\mathcal T}
\end{pmatrix}.                                                     \tag{17}
\]
A horizontal diagonal global section can start only in degree \(n\ge d\). The cross term in (7) never decreases fiber degree. Meanwhile vertical \(H^1\) vanishes in degrees greater than \(d\). Thus \(C\) is supported only on the single horizontal source in degree \(d\), and the single vertical target in degree \(d\).

The first horizontal obstruction from that source is
\[
-d[\phi]\in H^1(\mathcal O(kp)),
\]
which is nonzero: every term of \(\phi\) is a gap pole of order greater than \(k\). No other horizontal source contributes to this first target degree. Therefore every vector in \(\ker D_{\mathcal Q}\) has zero coefficient at that source, so
\[
C(\ker D_{\mathcal Q})=0.
\]
Linear algebra applied to (17) now yields
\[
\operatorname{rank}D_S
 =\operatorname{rank}D_{\mathcal Q}
  +\operatorname{rank}D_{\mathcal T}
 =2R+1-m.                                                        \tag{18}
\]

This argument is the point where it is important not to assume that the logarithmic tangent sequence splits.

## 8. Finishing the cohomology calculation

From the gap sequence,
\[
\sum_{n\ge0}h^1(\mathcal O(np))=1+3+\cdots+(2g-1)=g^2.
\]
Also,
\[
\begin{aligned}
\sum_{n\ge0}h^1(\Theta_{C_g}(np))
 &=\sum_{\lambda=-d}^{d}h^1(\mathcal O(\lambda p))\\
 &=g^2+\sum_{j=1}^d(g-1+j)\\
 &=5g^2-7g+3.
\end{aligned}
\]
Equations (6), (16), and (18) give exactly (1). Therefore
\[
\Delta_b
=(g^2-R)
 -(6g^2-7g+2-2R+m)
 +(5g^2-7g+2-R)
=-m.
\]

## 9. Exact computational verification

The following program uses rational arithmetic throughout. In particular, it does **not** substitute the final answer into a purported cohomology computation.

It constructs the full transition matrices modulo \(u^{4g-3}\), including every nonlinear term and the exact square root. Laurent expressions are represented as
\[
P(t)+Q(t)h(t),\qquad h(t)^2=1-t^{4g+2},
\]
so no numerical or power-series approximation is involved. It then performs the Čech elimination described in Section 3 and computes the resulting matrix ranks.

The checks include symbolic pivot determinants, the rank sums, regularity after every Čech reduction, and independent full-transition computations for vectors with zero, negative, and rational components.

```python
from fractions import Fraction as Q
from functools import lru_cache
from itertools import product
import sympy as sp

# Pairs (P,Q) represent P(t)+Q(t)*h(t), h^2=1-t^H.
def pa(a, b, c=1):
    z = a.copy()
    for i, v in b.items():
        z[i] = z.get(i, 0) + c*v
        if not z[i]:
            del z[i]
    return z

def pm(a, b):
    z = {}
    for i, v in a.items():
        for j, w in b.items():
            z[i+j] = z.get(i+j, 0) + v*w
    return {i: v for i, v in z.items() if v}

def add(a, b, c=1):
    return pa(a[0], b[0], c), pa(a[1], b[1], c)

def sc(a, c):
    return tuple({i: v*c for i, v in p.items() if v*c} for p in a)

def sh(a, n):
    return tuple({i+n: v for i, v in p.items()} for p in a)

def mon(n, c=1):
    return ({n: Q(c)} if c else {}, {})

def mul(a, b):
    q = pm(a[1], b[1])
    even = pa(pa(pm(a[0], b[0]), q),
              {i+H: v for i, v in q.items()}, -1)
    odd = pa(pm(a[0], b[1]), pm(a[1], b[0]))
    return even, odd

@lru_cache(None)
def hc(n):
    return Q(1) if n == 0 else hc(n-1)*Q(2*n-3, 2*n)

def coeff(a, n):
    return a[0].get(n, 0) + sum(
        v*hc((n-i)//H) for i, v in a[1].items()
        if n >= i and (n-i) % H == 0
    )

def af(s):
    # The function in A with leading pole t^(-s).
    return mon(-s) if s % 2 == 0 else ({}, {-s: Q(1)})

def split(a, lam):
    # a = f + eta + t^(-lam)*w, with f in A and w regular.
    a = (a[0].copy(), a[1].copy())
    eta = {}
    for n in range(min([0] + list(a[0]) + list(a[1])), -lam):
        c = coeff(a, n)
        if not c:
            continue
        s = -n
        if (s >= 0 and s % 2 == 0) or s >= 2*g+1:
            a = add(a, sc(af(s), c), -1)
        else:
            eta[n] = c
            a = add(a, mon(n, c), -1)
    w = sh(a, lam)
    # Check actual regularity, allowing cancellation between P and Qh.
    for n in range(min([0] + list(w[0]) + list(w[1])), 0):
        assert coeff(w, n) == 0
    return eta, w

def rank(cols):
    piv = {}
    for c in cols:
        c = {i: Q(v) for i, v in c.items() if v}
        while c:
            i = min(c)
            v = c[i]
            if i in piv:
                c = pa(c, piv[i], -v)
            else:
                piv[i] = {j: w/v for j, w in c.items()}
                break
    return len(piv)

def cech(gg, b, kind):
    global g, H
    g = gg
    H = 4*g+2
    d = 2*g-2
    k = g-(g+2)//3
    M = 2*d+1

    phi = ({-(2*g-1-2*j): Q(v)
            for j, v in enumerate(b) if v}, {})
    phip = ({e-1: e*v for e, v in phi[0].items()}, {})
    kp = sc(phi, k)
    powers = [mon(0)]
    for a in range((M-1)//k):
        powers.append(mul(powers[-1], kp))

    def power(alpha, a):
        c = Q(1)
        for j in range(a):
            c *= Q(alpha-j, j+1)
        return sc(powers[a], c)

    if kind == 'S':
        inds = [(n, c) for n in range(M) for c in ('h', 'v')]
    else:
        inds = [(n, kind) for n in range(M)]

    lam = [n-d if c in ('h', 'L') else n for n, c in inds]
    R = [{} for _ in inds]

    # Full W-to-U transition matrix, not just its first nonlinear term.
    for j, (n, c) in enumerate(inds):
        alpha = -Q(n, k)
        for a in range((M-1-n)//k+1):
            m = n+a*k
            if kind != 'S':
                R[j][m] = sh(
                    power(alpha+(kind == 'L'), a),
                    -n+(d if kind == 'L' else 0)
                )
            elif c == 'v':
                R[j][2*m+1] = sh(power(alpha+1, a), -n)
            else:
                R[j][2*m] = sh(power(alpha, a), d-n)
                v = sh(power(alpha, a), -n-1)
                if a:
                    v = add(v, sh(mul(
                        power(alpha, a-1),
                        add(sh(kp, -1), phip)
                    ), -n))
                R[j][2*m+1] = sc(
                    mul(v, ({}, {0: Q(1)})), -Q(1, 2)
                )

    rows = {}
    h0 = []
    for i, l in enumerate(lam):
        exps = ([-s for s in range(1, 2*g, 2) if s > l]
                + list(range(1, max(1, -l))))
        for e in exps:
            rows[i, e] = len(rows)
        for s in range(max(-1, l)+1):
            if s % 2 == 0 or s >= 2*g+1:
                h0.append((i, s))

    cols = []
    for j, s in h0:
        w = sh(af(s), lam[j])
        v = {i: mul(p, w) for i, p in R[j].items() if i != j}
        col = {}
        for i in range(j+1, len(inds)):
            if i not in v:
                continue
            eta, w = split(v[i], lam[i])
            for e, c in eta.items():
                col[rows[i, e]] = c
            for ell, p in R[i].items():
                if ell != i:
                    v[ell] = add(
                        v.get(ell, ({}, {})), mul(p, w), -1
                    )
        cols.append(col)

    rk = rank(cols)
    return len(rows)-rk, rk

def checks():
    # Check the inverse differential transition symbolically.
    t, u, k, F, Fp = sp.symbols('t u k F Fp', nonzero=True)
    B = 1+k*F*u**k
    logv_t = -1/t-Fp*u**k/B
    logv_e = 1/B
    inv_e = sp.simplify(-logv_t/logv_e)
    assert sp.simplify(
        inv_e-(1/t+(k*F/t+Fp)*u**k)
    ) == 0
    assert sp.simplify(logv_e*B) == 1

    # Symbolic antitriangular pivot determinants.
    for m in range(6):
        bs = sp.symbols('b:'+str(m+1))
        for a in range(1, m+5):
            for q in range(1, m+5):
                if max(a, q) < m+1:
                    continue
                s = min(a, q, m+1)
                start = m-s+1
                mat = sp.Matrix(
                    s, s,
                    lambda i, j:
                    bs[start+i+j] if start+i+j <= m else 0
                )
                expected = (-1)**(s*(s-1)//2)*bs[m]**s
                assert sp.expand(
                    mat.det(method='domain-ge')-expected
                ) == 0

    # Integer inequalities and the closed rank sum.
    for g in range(2, 101):
        r = (g+2)//3
        k = g-r
        d = 2*g-2
        N = d-k
        assert d <= 3*k and N >= 4*(r-1)
        for m in range(r):
            aa = [
                min(n//2+1, (N-n)//2+1, m+1)
                for n in range(N+1)
            ]
            assert sum(aa[1:]) == (m+1)*(g+r-1-2*m)-1
            assert aa[k] == m+1

    # Independent, full-transition exact-rational computations.
    count = 0
    for gg in range(2, 13):
        r = (gg+2)//3
        vectors = (list(product((-1, 0, 1), repeat=r))
                   if r <= 3 else [])
        vectors += [
            tuple(int(i == j) for i in range(r))
            for j in range(r)
        ]
        vectors += [tuple(Q((-2)**i, i+1) for i in range(r))]
        for b in vectors:
            if not any(b):
                continue
            m = max(i for i, v in enumerate(b) if v)
            R = (m+1)*(gg+r-1-2*m)-1
            vals = [cech(gg, b, c) for c in ('O', 'S', 'L')]
            expected = [
                (gg*gg-R, R),
                (6*gg*gg-7*gg+2-2*R+m, 2*R+1-m),
                (5*gg*gg-7*gg+2-R, R+1)
            ]
            assert vals == expected, (gg, b, vals, expected)
            assert vals[0][0]-vals[1][0]+vals[2][0] == -m
            count += 1

    print("All exact checks passed;",
          count, "full-transition examples.")

if __name__ == '__main__':
    checks()
```

I ran this program; its output was:
```text
All exact checks passed; 146 full-transition examples.
```

The proof, rather than these finite tests, establishes uniformity over all \(g\) and all complex coefficients. **What is proved:** the three formulas (1), and hence \(\Delta_b=-\max\{j:b_j\ne0\}\), for every vector allowed in the question. **What is left:** nothing.

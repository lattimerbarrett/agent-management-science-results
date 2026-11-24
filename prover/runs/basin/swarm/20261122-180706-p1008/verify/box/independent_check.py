import sympy as S
from pathlib import Path
from contextlib import redirect_stdout
import io
ns={}
with redirect_stdout(io.StringIO()):
    exec(compile(Path('agents/agent_1/scratchpad.py').read_text(), 'team', 'exec'), ns)
q=ns['q']; h=1/(1-q); k=1/((1-q)*(1-q*q))
# Independent PT module count. For one leg of thickness 2, the
# lengths of negative x tails satisfy 0<=a0<=a1; generating function k.
# A: two simple legs: Q has either no overlap box, or the overlap
# plus independently long negative x and negative y tails.
# B: doubled first leg in y: overlaps (0,0,0),(0,1,0).
# Q contains neither, just the second (one free tail), or both
# (two ordered x tails plus an independent y tail).
# C: doubled first leg in z: one overlap, one free z=1 x-tail.
# If overlap absent: only the free tail. If present: ordered x
# tails and independent y tail.
local={
 (0,0):S.Integer(1),(0,1):h,(1,0):h,(2,0):k,(3,0):k,
 (1,1):q**-1*(1+q*h*h),
 (2,1):q**-2*(1+q*h+q*q*k*h),
 (3,1):q**-1*(h+q*k*h)
}
for key in local:
    assert S.cancel(local[key]-ns['W'][key])==0
# Enumerate finite tail-length choices directly as a check of each
# rational series. r is renormalized degree, not length of Q.
N=14
for key in [(1,1),(2,1),(3,1)]:
    counts={}
    def add(r):
        if r<=N: counts[r]=counts.get(r,0)+1
    if key==(1,1):
        add(-1)
        for a in range(N+3):
            for b in range(N+3): add(a+b)
    elif key==(2,1):
        add(-2)
        for a in range(N+3): add(-1+a)
        for a0 in range(N+3):
            for a1 in range(a0,N+3):
                for b in range(N+3): add(a0+a1+b)
    else:
        for a in range(N+3): add(-1+a)
        for a0 in range(N+3):
            for a1 in range(a0,N+3):
                for b in range(N+3): add(a0+a1+b)
    ser=S.series(local[key],q,0,N+1).removeO().expand()
    for r in range(-2,N+1): assert ser.coeff(q,r)==counts.get(r,0), (key,r)
# Direct computation of all Chern contributions from tangent weights,
# including each transverse box, instead of using the supplied L table.
w=[S.Integer(1),S.Integer(2),S.Integer(-3)]; e=S.prod(w)
partboxes=[[],[(0,0)],[(0,0),(1,0)],[(0,0),(0,1)]]
z={(0,0):S.Integer(1)}; f={}
for idx,boxes in enumerate(partboxes):
    a=len(boxes)
    # -w2*w3*(j*w2+k*w3+(w2+w3)/2), summed over cylinder.
    cylinder=sum(-w[1]*w[2]*(j*w[1]+l*w[2]+(w[1]+w[2])/2) for j,l in boxes)
    edge=sum(1+j+l for j,l in boxes)
    outer=[1,h,k,k][idx]
    for b in [0,1]:
        if not a+b: continue
        cyl=cylinder+b*(-w[0]*w[2]*(w[0]+w[2])/2)
        pre=(-1)**(a+b)*q**(edge+b)*outer*h**b
        key=(a,b); vertex=local[idx,b]
        z[key]=z.get(key,0)+pre*vertex
        f[key]=f.get(key,0)+pre*(e*q*S.diff(vertex,q)+cyl*vertex)
# Truncated bivariate power series inverse via geometric sum.
def mul(A,B):
    C={}
    for (a,b),v in A.items():
        for (c,d),u in B.items():
            if a+c<=2 and b+d<=1:
                C[a+c,b+d]=C.get((a+c,b+d),0)+v*u
    return C
nonempty={key:-v for key,v in z.items() if key!=(0,0)}
inv={(0,0):S.Integer(1)}; term=inv.copy()
for j in range(1,4):
    term=mul(term,nonempty)
    for key,v in term.items(): inv[key]=inv.get(key,0)+v
R=S.factor(mul(f,inv)[2,1])
assert S.cancel(R-ns['R'])==0
print('Independent PT module counts, Chern calculation and formal inverse agree.')
print('R(q) =',R)

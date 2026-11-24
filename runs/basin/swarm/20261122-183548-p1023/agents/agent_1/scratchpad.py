from itertools import product
from math import gcd

def mul(g,h):
    a,b,c,d=g; e,f,j,k=h
    return ((a*e+b*j)%5,(a*f+b*k)%5,
            (c*e+d*j)%5,(c*f+d*k)%5)
def inv(g):
    a,b,c,d=g
    return (d,(-b)%5,(-c)%5,a)
G=[g for g in product(range(5),repeat=4)
   if (g[0]*g[3]-g[1]*g[2])%5==1]
assert len(G)==120
I=(1,0,0,1); t=(1,1,0,1)
assert all(mul(g,inv(g))==I for g in G)
seen=set(); orbits=[]
for g in G:
    if g in seen: continue
    O={g}; todo=[g]
    while todo:
        h=todo.pop()
        for k in (inv(h),mul(mul(t,h),inv(t))):
            if k not in O: O.add(k); todo.append(k)
    seen.update(O); orbits.append(sorted(O))
reps=[(0,1,4,j) for j in range(5)]+[(0,2,2,j) for j in range(5)]+[
    (1,0,0,1),(1,1,0,1),(1,2,0,1),(2,0,0,3),
    (4,0,0,4),(4,1,0,4),(4,2,0,4)]
assert [o[0] for o in orbits]==reps
r=17
assert len(orbits)==r and seen==set(G)
a=[len(o) for o in orbits]
b=[-2]*10+[1,2,2,10,1,2,2]
A=[2]*5+[-2]*5+[1,2,2,-10,1,2,2]
B=[-4]*5+[4]*5+[0]*7
x=[-4,7,-7,1,4,1,2,2,0,-2,-6,5,0,0,-15,10,0]
z=[1,2,2,0,-2,-4,7,-7,1,4,-6,0,5,0,-15,0,10]
def dot(v,w):return sum(c*d for c,d in zip(v,w))
T={}
for i in range(r):
    for j in range(r):
        counts={g:0 for g in G}
        for g in orbits[i]:
            for h in orbits[j]:counts[mul(g,h)]+=1
        coeff=[]
        for O in orbits:
            vals={counts[g] for g in O}
            assert len(vals)==1
            coeff.append(vals.pop())
        T[i,j]=coeff
        assert dot(a,coeff)==a[i]*a[j]
        assert dot(b,coeff)==b[i]*b[j]
        assert dot(A,coeff)==A[i]*A[j]+B[i]*B[j]
        assert dot(B,coeff)==A[i]*B[j]+B[i]*A[j]+B[i]*B[j]
for i in range(r):
    for j in range(r):assert T[i,j]==T[j,i]
e=[int(k==10) for k in range(r)]
assert (dot(a,e),dot(b,e),dot(A,e),dot(B,e))==(1,1,1,0)
assert sum(b)==sum(A)==sum(B)==0
assert sum(a)==120
for i in range(r):
    assert B[i]%4==0
    assert (A[i]-b[i])%4==0
    assert (a[i]-b[i])%3==0
    assert (a[i]-A[i]-3*B[i])%5==0
    assert a[i]+5*b[i]-6*A[i]-3*B[i]==(120 if i==13 else 0)
xz=[sum(x[i]*z[j]*T[i,j][k] for i in range(r) for j in range(r))
    for k in range(r)]
assert xz==[20+c for c in e]
assert dot(a,x)==dot(a,z)==49
answer=[u for u in range(120) if gcd(u,120)==1
        and u%24 in (1,23) and u*u%5==1]
assert answer==[1,49,71,119]
print('All orbit, ring-homomorphism, congruence, and unit checks passed.')
print('Image:',answer)

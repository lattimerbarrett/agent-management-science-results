"""Certified stable quadratic-reduction seed at ambient dimension 19.
This is an algebraic seed only; it does not establish the PDE gluing theorem.
"""
import sys
sys.path.insert(0,'workspace')
import agent3_odd_gram_checks as c
from fractions import Fraction as F

n=19;m=18
N=10000

def Mmatrix(q,degree):
    ids=range(max(0,2-q),degree+1)
    out=[]
    for i in ids:
        row=[]
        for j in ids:
            v=c.point(0)
            for s,ci in c.coefficients(q,i).items():
                for t,cj in c.coefficients(q,j).items():
                    v=c.plus(v,c.times(c.point(ci*cj),c.base_interval(n,q,s,t,N)))
            row.append(v)
        out.append(row)
    return out

M1=Mmatrix(1,3);M2=Mmatrix(2,3);M3=Mmatrix(3,2)

def bilinear(a,M,b):
    v=c.point(0)
    for i,x in enumerate(a):
        for j,y in enumerate(b):v=c.plus(v,c.times(c.times(x,y),M[i][j]))
    return v

def smul(a,b):return [c.times(c.point(a),x) for x in b]
def matweight(M,f):return [[c.times(c.point(f(i,j)),v) for j,v in enumerate(row)] for i,row in enumerate(M)]
K=matweight(M2,lambda i,j:i+j+1)
T=matweight(M2,lambda i,j:(i+j)*(i+j+1))
rest=[F(-230,499),F(46,821),F(-1,722)]
a=[c.point(1)]+[c.point(v) for v in rest]
negative=bilinear(a,K,a)
assert negative[1]<0
print('Negative dilation witness certified:',tuple(map(float,negative)))

lo=F(10803424,10**7);hi=F(10803426,10**7)
alo=[c.point(lo)]+[c.point(v) for v in rest]
ahi=[c.point(hi)]+[c.point(v) for v in rest]
Plo=bilinear(alo,K,alo);Phi=bilinear(ahi,K,ahi)
assert Plo[1]<0 and Phi[0]>0
print('Dilation root bracket by IVT:',lo,hi)
a=[(lo,hi)]+[c.point(v) for v in rest]
scale_hessian=c.neg(bilinear(a,T,a))
assert scale_hessian[0]>0
assert bilinear(a,M2,a)[0]>0 # Hence reduced energy is negative.
print('Positive scale-Hessian half bracket:',tuple(map(float,scale_hessian)))
# Harmonic decomposition of d_a(P2 f), where P2=x1^2-x2^2.
# P3a=x_a P2-|x|^2 d_a P2/(m+2).
# Norm ratios to ||P2||^2:
# ||d_aP2||^2=m+2, ||P3a||^2=3/(m+4)-1/(m+2), a=1,2;
# 0 and 1/(m+4), respectively, for a>2.
g=[c.times(c.point(1+F(2*i,m+2)),x) for i,x in enumerate(a)]
fp=[c.times(c.point(i),a[i]) for i in range(1,4)]
for special in (True,False):
    z=1 if special else 0
    r1=m+2 if special else 0
    r3=F(3,m+4)-F(1,m+2) if special else F(1,m+4)
    b=[c.point(0) for _ in range(4)]
    for i in range(3):b[i]=c.times(c.point(2+4*z),fp[i])
    for i in range(2,4):
        b[i-1]=c.plus(b[i-1],c.times(c.point(F(4+8*z,m+4)*i*(i-1)),a[i]))
    H=c.neg(c.plus(c.plus(c.times(c.point(r1),bilinear(g[1:],M1,g[1:])),c.times(c.point(r3),bilinear(smul(2,fp),M3,smul(2,fp)))),bilinear(a,M2,b)))
    assert H[0]>0
    print('Positive translation Hessian bracket; special=',special,':',tuple(map(float,H)))
# Reflection symmetries give zero mixed translation derivatives and zero
# mixed translation-scale derivatives. Swapping x1,x2 gives equal special
# diagonal entries; O(m-2) invariance gives equality of remaining entries.
print('All algebraic stable-seed assertions passed.')

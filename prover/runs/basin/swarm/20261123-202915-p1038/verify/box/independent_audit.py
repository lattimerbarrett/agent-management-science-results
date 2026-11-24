import mpmath as mp
from fractions import Fraction as F
mp.mp.dps=100

def multiply(p,q):
    out=[mp.mpc(0)]*(len(p)+len(q)-1)
    for i,x in enumerate(p):
        for j,y in enumerate(q):out[i+j]+=x*y
    return out

def direct_row(Q,i):
    p=[mp.mpc(1)]
    for j in range(len(Q)):
        if i==j:continue
        lo,hi=sorted((i,j))
        z=Q[hi][0]-Q[lo][0];w=Q[hi][1]-Q[lo][1]
        d=z+mp.sqrt(z*z+abs(w)**2)
        p=multiply(p,[1,-mp.conj(w)/d] if i==lo else [w/d,1])
    return p+[0]*(len(Q)-len(p))

def c(r,z):return r/(z+mp.sqrt(z*z+r*r))

def test_rotation(m):
    k=2*m; h=mp.mpf('0.3');r=mp.mpf('1.1');R=mp.mpf('2.7')
    lows=[-mp.mpf('0.5')-mp.mpf('0.2')*(k-j) for j in range(k)]
    ups=[mp.mpf(3)+mp.mpf('0.1')*j for j in range(k)]
    zz=[mp.exp(2*mp.pi*mp.j*j/m) for j in range(m)]
    Q=[(x,mp.mpc(0)) for x in lows]+[(0,r*z) for z in zz]+[(h,R*z) for z in zz]+[(x,mp.mpc(0)) for x in ups]
    S=[mp.mpc(1)]
    for j in range(1,m): S=multiply(S,[1,mp.j*mp.exp(-mp.pi*mp.j*j/m)])
    A=S[:];B=S[:]
    for x in lows:
        A=multiply(A,[c(r,-x),1]);B=multiply(B,[c(R,h-x),1])
    for x in ups:
        A=multiply(A,[1,c(r,x)]);B=multiply(B,[1,c(R,x-h)])
    for z in zz:
        d=h+mp.sqrt(h*h+R*R+r*r-2*r*R*z.real)
        A=multiply(A,[1,-mp.conj((R*z-r)/d)])
        B=multiply(B,[(R-r*z)/d,1])
    worst=mp.mpf(0)
    for offset,core in [(k,A),(k+m,B)]:
        for j in range(m):
            direct=direct_row(Q,offset+j)
            expected=[x*zz[j]**(-e) for e,x in enumerate(core)]
            pivot=max(range(len(expected)),key=lambda e:abs(expected[e]))
            scalar=direct[pivot]/expected[pivot]
            err=max(abs(x-scalar*y) for x,y in zip(direct,expected))/max(map(abs,direct))
            worst=max(worst,err)
    print('m',m,'all ring rows agree up to scalars; relative error',mp.nstr(worst,5))
    assert worst<mp.mpf('1e-90')

for m in (1,2,3,4,5,7):test_rotation(m)
# Check sign orientation with random exact rational axes and hand-built duals.
for K in (1,2,3,5):
    m=3; al=mp.mpf('.5');be=mp.mpf('.99');de=mp.mpf('.006');ep=mp.mpf('.5');p=2**m;q=(1/be)**m;u=de**m;v=ep**m
    C=mp.matrix(2*K+2)
    for j in range(2*K):
        row=[1,-al**m-be**m,(al*be)**m] if j<K else [u*v,-u-v,1]
        for t,z in enumerate(row):C[j,j+t]=z
    for e in range(2*K+2):
        C[2*K,e]=mp.mpf(e+1)**2
        C[2*K+1,e]=mp.mpf(e+2)**3
    def dual(t):
        x=[t**j for j in range(K+2)]
        for j in range(K,2*K):x.append((u+v)*x[-1]-u*v*x[-2])
        # above appended one extra, since initial already includes x_{K+1}
        return x[:2*K+2]
    a=dual(p);b=dual(q)
    assert max(abs(sum(C[i,j]*a[j] for j in range(C.cols))) for i in range(2*K))<mp.mpf('1e-80')
    D=sum(C[2*K,j]*a[j] for j in range(C.cols))*sum(C[2*K+1,j]*b[j] for j in range(C.cols))-sum(C[2*K,j]*b[j] for j in range(C.cols))*sum(C[2*K+1,j]*a[j] for j in range(C.cols))
    E=mp.matrix([[C[i,j] for j in range(2,2*K+2)] for i in range(2*K)])
    err=abs(mp.det(C)*(q-p)-mp.det(E)*D)
    assert err<mp.mpf('1e-75')
print('Dual recurrence and orientation independently checked.')
